import logging
import os
import tarfile
import threading
from queue import Queue

import pyarrow as pa

from streaming_wds.core.cache import LocalShardLRUCache

logger = logging.getLogger(__name__)


class ShardExtractor:
    """
    A class for extracting shards and processing their contents.

    This class handles the extraction of shards from a local cache, processes their
    contents, and puts the extracted samples into an output queue.

    Attributes:
        input_queue (Queue): Queue for incoming shard extraction requests.
        output_queue (Queue): Queue for outputting extracted samples.
        stop_event (threading.Event): Event to signal stopping of the extraction process.
        buffer_size (int): Maximum buffer size for memory management.
        cache (LocalShardLRUCache): Local cache for storing and retrieving shards.
        input_finish_event (threading.Event): Event to signal completion of input.
        output_finish_event (threading.Event): Event to signal completion of output.
    """

    def __init__(
        self,
        *,
        input_queue: Queue,
        output_queue: Queue,
        stop_event: threading.Event,
        input_finish_event: threading.Event,
        output_finish_event: threading.Event,
        cache: LocalShardLRUCache,
        buffer_size: int = 2 << 30,  # 1GB in bytes
    ):
        """
        Initialize the ShardExtractor.

        Args:
            input_queue (Queue): Queue for incoming shard extraction requests.
            output_queue (Queue): Queue for outputting extracted samples.
            stop_event (threading.Event): Event to signal stopping of the extraction process.
            input_finish_event (threading.Event): Event to signal completion of input.
            output_finish_event (threading.Event): Event to signal completion of output.
            cache (LocalShardLRUCache): Local cache for storing and retrieving shards.
            buffer_size (int, optional): Maximum buffer size for memory management. Defaults to 1GB.
        """
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.stop_event = stop_event
        self.buffer_size = buffer_size
        self.cache = cache

        self.input_finish_event = input_finish_event
        self.output_finish_event = output_finish_event

    def extract_shard(self, shard_idx: int, shard_key: str, rank: int):
        """
        Extract and process a single shard.

        This method extracts the contents of a shard, processes its files, and yields
        the aggregated data for each sample in the shard.

        Args:
            shard_idx (int): The index of the shard.
            shard_key (str): The key of the shard in the cache.
            rank (int): The rank of the worker processing this shard.

        Yields:
            dict: A dictionary containing the aggregated data for each sample in the shard.

        Raises:
            Exception: If the shard is not found in the cache.
        """
        self.cache.acquire_shard_lock(shard_key)
        logger.debug(f"Acquired lock for shard {shard_key}")

        try:
            file_path = self.cache.get_shard_path(shard_key, check_exists=True)
            if not file_path:
                logger.error(f"Shard {shard_key} not found in cache")
                raise Exception(f"Shard {shard_key} not found in cache")

            # if pa.total_allocated_bytes() > self.buffer_size:
            #     logger.debug("Exceeded memory buffer quota. Sleeping for 1 seconds")
            #     time.sleep(5)

            logger.debug(f"Extracting shard {shard_key} at {file_path}")
            with open(file_path, "rb") as f:
                # Streaming mode with automatic compression detection
                tar = tarfile.open(fileobj=f, mode="r|*")
                current_key = None
                aggregated = {}

                for member in tar:
                    if member.isfile():
                        key, ext = os.path.splitext(member.name)

                        if key != current_key:
                            if aggregated:
                                yield aggregated
                            current_key = key
                            aggregated = {}

                        extracted_file = tar.extractfile(member)
                        if extracted_file:
                            content = extracted_file.read()
                            aggregated[ext] = pa.py_buffer(content)
                            aggregated["__wds_shard_idx__"] = shard_idx
                            aggregated["__wds_sample_key__"] = current_key
                            aggregated["__wds_global_rank__"] = rank

                if aggregated:
                    yield aggregated

        except Exception as e:
            logger.error(f"Error extracting shard {shard_key}: {e}")
            import traceback

            logger.error(traceback.format_exc())
        finally:
            self.cache.release_shard_lock(shard_key)

    def run(self, rank: int):
        """
        Run the shard extraction process.

        This method continuously extracts shards from the input queue, processes them,
        and puts the extracted samples into the output queue until the stop event is set.

        Args:
            rank (int): The rank of the worker running this extraction process.
        """
        while not self.stop_event.is_set():
            if self.input_queue.empty() and self.input_finish_event.is_set():
                logger.debug("No more downloads to extract. Exiting")
                self.output_finish_event.set()

            shard_idx, shard_key = self.input_queue.get()
            for sample in self.extract_shard(shard_idx, shard_key, rank):
                logger.debug(
                    f"Processed key {sample['__wds_sample_key__']} files from {shard_key}"
                )
                self.output_queue.put(sample)

            self.input_queue.task_done()
