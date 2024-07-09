import io
import logging
import os
import tarfile
import threading
from queue import Empty, Queue
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import boto3
import pyarrow as pa
from torch.utils.data import IterableDataset

from streaming_wds.sharder import (
    ComputeWorkerInfos,
    OrderByStride,
    ShardShuffler,
    WorkerShardSplitter,
)
from streaming_wds.types import StateDict, WorkerInfo
from streaming_wds.utils import (
    get_global_rank,
    get_global_world_size,
)

from .decoders import no_decoder, select_decoder

logging.getLogger("botocore.configprovider").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class StreamingWebDataset(IterableDataset):
    def __init__(
        self,
        remote: str,
        split: Optional[str] = None,
        profile: str = "default",
        buffer_size: int = 2,
        drop_last: bool = True,
        shuffle: bool = False,
        max_workers: int = 2,
        schema: Dict[str, str] = {},
    ):
        self.remote = os.path.join(remote, split) if split else remote
        self.buffer_size = buffer_size
        self.drop_last = drop_last
        self.shuffle = shuffle
        self.max_workers = max(2, (max_workers + 1) // 2 * 2)

        if not schema:
            logger.warning("No schema provided. Decoding will be skipped.")
        self.decoders = {k: select_decoder(v) for (k, v) in schema.items()}

        parsed_uri = urlparse(self.remote)
        self._bucket = parsed_uri.netloc
        self._key_prefix = parsed_uri.path.lstrip("/")

        self._session = boto3.Session(profile_name=profile)

        self._state_dict: Optional[StateDict] = None
        self._worker_infos: List[WorkerInfo] = []
        self._worker_info: Optional[WorkerInfo] = None

        self._download_queue: Queue[str] = Queue()
        self._extract_queue: Queue[bytes] = Queue(maxsize=buffer_size)
        self._extracted: Queue[Dict[str, bytes]] = Queue()

        self._workers = []
        self._stop_event = threading.Event()
        self._download_finished_event = threading.Event()

        self._shards: List[str] = []

    @property
    def num_shards(self):
        """Return the number of shards in the dataset"""
        if self._shards:
            return len(self._shards)

        elif not hasattr(self, "_cached_num_shards"):
            self._cached_num_shards = len(self._resolve_shards())

        return self._cached_num_shards

    def state_dict(self):
        logger.warning(
            "This should be called from StreamingDataLoader instead. Only use this when running the dataset by itself."
        )
        return StateDict(
            global_world_size=get_global_world_size(),
            worker_infos=self._worker_infos,
        )

    def load_state_dict(self, state_dict: StateDict, global_world_size: int):
        logger.warning(
            "This should be called from StreamingDataLoader instead. Only use this when running the dataset by itself."
        )
        self._state_dict = state_dict
        self._worker_infos = ComputeWorkerInfos.apply(
            global_world_size,
            state_dict.worker_infos,
        )
        self._shards = []
        self._reset()

    def _resolve_shards(self):
        dataset_shards = []
        s3 = self._session.client("s3")
        paginator = s3.get_paginator("list_objects_v2")
        for result in paginator.paginate(Bucket=self._bucket, Prefix=self._key_prefix):
            for content in result.get("Contents", []):
                if content["Key"].endswith(".tar"):
                    dataset_shards.append(content["Key"])

        return dataset_shards

    def set_shuffle(self, shuffle: bool):
        self.shuffle = shuffle

    def set_drop_last(self, drop_last: bool):
        self.drop_last = drop_last

    def get_worker_infos(
        self, global_world_size: int, num_shards: Optional[int] = None
    ) -> List[WorkerInfo]:
        if self._worker_infos:
            return self._worker_infos

        return ComputeWorkerInfos.apply(
            global_world_size, [WorkerInfo.default(num_shards or self.num_shards)]
        )

    @property
    def global_rank(self):
        if not hasattr(self, "_cached_global_worker_rank"):
            self._cached_global_worker_rank = get_global_rank()
        return self._cached_global_worker_rank

    def _reset(self):
        # clear events
        self._stop_event.clear()
        self._download_finished_event.clear()

        # empty queues
        self._download_queue = Queue()
        self._extract_queue = Queue(maxsize=self.buffer_size)
        self._extracted = Queue()

    def _setup(self):
        self._reset()

        if not self._shards:
            self._shards = self._resolve_shards()
            if self.shuffle:
                self._shards = ShardShuffler.apply(self._shards)

            if not self._worker_infos:
                self._worker_infos = self.get_worker_infos(get_global_world_size())
                self._worker_info = self._worker_infos[self.global_rank]

            if self._state_dict:
                self._shards = OrderByStride.apply(self._shards, self._state_dict)

            self._shards = WorkerShardSplitter.apply(self._shards, self._worker_info)

        for path in self._shards:
            self._download_queue.put(path)

    def _download_worker(self):
        s3 = self._session.client("s3")
        shard_idx = self._worker_info.start

        while not self._stop_event.is_set():
            try:
                path = self._download_queue.get(timeout=1)
                if shard_idx < self._worker_info.idx:
                    shard_idx += 1
                    continue

                response = s3.get_object(Bucket=self._bucket, Key=path)
                body = response["Body"].read()

                self._extract_queue.put((shard_idx, body))
                shard_idx += 1
            except Empty:
                # since we load all the shards into the queue before starting the workers
                # we can safely assume that if the queue is empty, we are done
                self._worker_info.idx = self._worker_info.start
                self._download_finished_event.set()
            finally:
                self._download_queue.task_done()

    def _extract_worker(self):
        while not self._stop_event.is_set():
            try:
                shard_idx, body = self._extract_queue.get(timeout=1)

                tar = tarfile.open(fileobj=io.BytesIO(body), mode="r")
                current_key = None
                aggregated = {}

                sorted_members = sorted(tar.getmembers(), key=lambda m: m.name)
                for member in sorted_members:
                    if member.isfile():
                        key, ext = os.path.splitext(member.name)

                        if key != current_key:
                            if aggregated:
                                self._extracted.put(aggregated)
                            current_key = key
                            aggregated = {}

                        aggregated[ext] = pa.py_buffer(tar.extractfile(member).read())
                        aggregated["__wds_shard_idx__"] = shard_idx
                        aggregated["__wds_global_rank"] = self.global_rank
                if aggregated:
                    self._extracted.put(aggregated)

                # Mark the task as done after processing the entire tar file
                self._extract_queue.task_done()

            except Empty:
                if self._download_finished_event.is_set():
                    break
            except Exception as e:
                print(f"Error in extract_worker: {e}")
                # You might want to add more robust error handling here

    def _decode_sample(self, sample: Dict[str, bytes]) -> Dict[str, Any]:
        decoded_sample = {}
        for key, value in sample.items():
            if isinstance(value, pa.Buffer):
                value = value.to_pybytes()
            decoded_sample[key] = self.decoders.get(key, no_decoder)(value)
        return decoded_sample

    def process_sample(self, sample: Dict[str, bytes]) -> Dict[str, bytes]:
        """Override this method to process the sample before decoding"""
        return sample

    def __iter__(self):
        self._setup()
        self._workers = [
            threading.Thread(target=self._download_worker)
            for _ in range(self.max_workers // 2)
        ] + [
            threading.Thread(target=self._extract_worker)
            for _ in range(self.max_workers // 2)
        ]

        for worker in self._workers:
            worker.start()

        try:
            while not self._stop_event.is_set():
                try:
                    sample = self._extracted.get(timeout=1)
                    sample = self._decode_sample(sample)
                    sample = self.process_sample(sample)

                    self._worker_info.idx = max(
                        sample["__wds_shard_idx__"], self._worker_info.idx
                    )
                    yield sample

                except Empty:
                    if (
                        self._download_queue.empty()
                        and self._extract_queue.empty()
                        and self._extracted.empty()
                    ):
                        break
        finally:
            self._stop_event.set()
            for worker in self._workers:
                worker.join()

    def __del__(self):
        self._stop_event.set()
        for worker in self._workers:
            if worker.is_alive():
                worker.join()
