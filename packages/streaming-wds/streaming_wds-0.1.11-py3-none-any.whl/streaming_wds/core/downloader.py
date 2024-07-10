import logging
import threading
from queue import Queue
from typing import List, Optional
from urllib.parse import urlparse

from boto3 import Session
from botocore.exceptions import ClientError

from streaming_wds.core.cache import LocalShardLRUCache
from streaming_wds.core.sharder import GetWorkerSplit, OrderByStride, Shuffle
from streaming_wds.core.types import StateDict, WorkerInfo

logger = logging.getLogger(__name__)


class ShardDownloader:
    """
    A class for downloading shards from S3 and managing the download process.

    This class handles the downloading of shards from S3, caching them locally,
    and managing the download queue for multiple workers.

    Attributes:
        s3 (boto3.client): The S3 client for interacting with AWS S3.
        shards (Optional[List[str]]): List of shard keys to be downloaded.
        cache (LocalShardLRUCache): Local cache for storing downloaded shards.
        input_queue (Queue): Queue for incoming shard download requests.
        output_queue (Queue): Queue for outputting downloaded shard information.
        stop_event (threading.Event): Event to signal stopping of the download process.
        finish_event (threading.Event): Event to signal completion of downloads.
        bucket (str): The S3 bucket name.
        key_prefix (str): The prefix for S3 keys.
    """

    def __init__(
        self,
        *,
        remote: str,
        session: Session,
        input_queue: Queue,
        output_queue: Queue,
        stop_event: threading.Event,
        finish_event: threading.Event,
        cache: LocalShardLRUCache,
    ):
        """
        Initialize the ShardDownloader.

        Args:
            remote (str): The remote S3 uri.
            session (Session): The boto3 session.
            input_queue (Queue): Queue for incoming shard download requests.
            output_queue (Queue): Queue for outputting downloaded shard information.
            stop_event (threading.Event): Event to signal stopping of the download process.
            finish_event (threading.Event): Event to signal completion of downloads.
            cache (LocalShardLRUCache): Local cache for storing downloaded shards.
        """
        self.s3 = session.client("s3")
        self.shards: Optional[List[str]] = None
        self.cache = cache

        self.input_queue = input_queue
        self.output_queue = output_queue
        self.stop_event = stop_event
        self.finish_event = finish_event

        self._called_setup = False

        parsed_uri = urlparse(remote)
        self.bucket = parsed_uri.netloc
        self.key_prefix = parsed_uri.path.lstrip("/")

    def num_shards(self):
        """
        Get the number of shards.

        Returns:
            int: The number of shards.
        """
        if self.shards is not None:
            return len(self.shards)

        elif not hasattr(self, "_cached_num_shards"):
            self._cached_num_shards = len(self.find_shards())

        return self._cached_num_shards

    def reset(self):
        """Reset the ShardDownloader state."""
        self._called_setup = False
        self.shards = None

    def find_shards(self):
        """
        Find all shards in the S3 bucket with the given prefix.

        Returns:
            List[str]: A list of shard keys.
        """
        shard_keys = []
        paginator = self.s3.get_paginator("list_objects_v2")
        for result in paginator.paginate(Bucket=self.bucket, Prefix=self.key_prefix):
            for content in result.get("Contents", []):
                if content["Key"].endswith(".tar"):
                    shard_keys.append(content["Key"])

        return shard_keys

    def get_shard(self, key: str) -> str:
        """
        Get the shard from the cache if it exists, otherwise download it.

        Args:
            key (str): The S3 key of the shard.

        Returns:
            str: The local path to the shard file, or None if download failed.
        """
        cached_path = self.cache.get_shard(key)
        if cached_path:
            logger.debug(f"Shard {key} found in cache")
            return cached_path

        logger.debug(f"Shard {key} not in cache, downloading")
        try:
            # Get file size
            response = self.s3.head_object(Bucket=self.bucket, Key=key)
            file_size = response["ContentLength"]
            shard_path = self.cache.add_shard(key, file_size)

            self.cache.acquire_shard_lock(key)
            self.s3.download_file(
                Bucket=self.bucket,
                Key=key,
                Filename=shard_path,
            )
            self.cache.release_shard_lock(key)
            return key
        except ClientError as e:
            logger.error(f"Error downloading shard {key}: {e}")
            return None

    def prefetch_shards(self, keys: List[str]):
        """
        Prefetch multiple shards in parallel.

        Args:
            keys (List[str]): List of S3 keys to prefetch.
        """
        # This is a placeholder for a more advanced prefetching mechanism
        # You could implement this using threads or asyncio for parallel downloads
        for key in keys:
            self.get_shard(key)

    def setup(
        self,
        rank: int,
        worker_infos: List[WorkerInfo],
        state_dict: Optional[StateDict] = None,
        shuffle: bool = False,
    ):
        """
        Set up the ShardDownloader for a specific worker.

        Args:
            rank (int): The rank of the worker.
            worker_infos (List[WorkerInfo]): Information about all workers.
            state_dict (Optional[StateDict]): The state dictionary for resuming.
            shuffle (bool): Whether to shuffle the shards.
        """
        if self.shards is None:
            self.shards = self.find_shards()

            if shuffle:
                self.shards = Shuffle.apply(self.shards)

            if state_dict:
                self.shards = OrderByStride.apply(self.shards, state_dict)

            self.shards = GetWorkerSplit.apply(self.shards, worker_infos[rank])

        for shard in self.shards:
            self.input_queue.put(shard)

        self._called_setup = True

    def run(
        self,
        worker_info: WorkerInfo,
    ):
        """
        Run the shard downloading process for a worker.

        Args:
            worker_info (WorkerInfo): Information about the worker.

        Raises:
            RuntimeError: If setup() was not called before run().
        """
        if not self._called_setup:
            raise RuntimeError("setup() must be called before run()")

        local_idx = 0
        while not self.stop_event.is_set():
            if self.input_queue.empty():
                break

            # Get the shard
            shard = self.input_queue.get()
            shard_idx = worker_info.start + local_idx

            # Shard-level mid-epoch resumption
            if worker_info.resume and shard_idx < worker_info.idx:
                logger.debug(f"Skipping shard {shard} as it was already processed")
                self.input_queue.task_done()
                continue

            # Download the shard
            shard = self.get_shard(shard)
            if shard:
                self.output_queue.put((shard_idx, shard))
            else:
                logger.debug(f"Failed to download shard: {shard}")

            self.input_queue.task_done()

        logger.debug("All shards downloaded. Exiting.")
        self.finish_event.set()
        self._called_setup = False
