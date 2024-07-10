import logging
import os
import threading
from queue import Queue
from typing import Any, Dict, List, Optional

import boto3
import pyarrow as pa
from torch.utils.data import IterableDataset

from .core.cache import LocalShardLRUCache
from .core.downloader import ShardDownloader
from .core.extractor import ShardExtractor
from .core.sharder import (
    ComputeWorkerInfos,
    distribute_worker_infos,
)
from .core.types import StateDict, WorkerInfo
from .decoders import no_decoder, select_decoder
from .utils import (
    get_global_rank,
    get_global_world_size,
)

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
        cache_limit_bytes: int = 2 << 30,  # 2GB in bytes
    ):
        self.remote = os.path.join(remote, split) if split else remote
        self.buffer_size = buffer_size
        self.drop_last = drop_last
        self.shuffle = shuffle
        self.max_workers = max(2, (max_workers + 1) // 2 * 2)
        self.cache_limit_bytes = cache_limit_bytes

        if not schema:
            logger.warning("No schema provided. Decoding will be skipped.")
        self.decoders = {k: select_decoder(v) for (k, v) in schema.items()}

        self._session = boto3.Session(profile_name=profile)

        self._state_dict: Optional[StateDict] = None
        self._worker_infos: List[WorkerInfo] = []

        self.initialize_worker_components()

    def initialize_worker_components(self):
        self.reset_global_rank()

        self._download_queue: Queue[str] = Queue()
        self._extract_queue: Queue[bytes] = Queue(maxsize=self.buffer_size)
        self._samples_queue: Queue[Dict[str, bytes]] = Queue()

        self._workers = []
        self._stop_event = threading.Event()
        self._download_finished_event = threading.Event()
        self._dataset_finished_event = threading.Event()

        self.cache = LocalShardLRUCache(
            self.remote, self.global_rank, self.cache_limit_bytes
        )
        self.downloader = ShardDownloader(
            remote=self.remote,
            session=self._session,
            input_queue=self._download_queue,
            output_queue=self._extract_queue,
            stop_event=self._stop_event,
            finish_event=self._download_finished_event,
            cache=self.cache,
        )
        self.extractor = ShardExtractor(
            input_queue=self._extract_queue,
            output_queue=self._samples_queue,
            stop_event=self._stop_event,
            input_finish_event=self._download_finished_event,
            output_finish_event=self._dataset_finished_event,
            cache=self.cache,
        )

    @property
    def num_shards(self):
        return self.downloader.num_shards()

    def reset(self, global_world_size: int, state_dict: Optional[StateDict] = None):
        self.initialize_worker_components()

        if state_dict:
            self._worker_infos = state_dict.worker_infos
            self._worker_infos = distribute_worker_infos(
                global_world_size,
                self._worker_infos,
            )
        elif not self._worker_infos:
            self._worker_infos = [WorkerInfo.default(self.num_shards)]

        self._worker_infos = distribute_worker_infos(
            global_world_size,
            self._worker_infos,
            resume=state_dict is not None,
        )

        # setup downloader
        self.downloader.setup(
            self.global_rank, self._worker_infos, state_dict, self.shuffle
        )

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
        self.downloader.reset()
        self.reset(state_dict)

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

    def reset_global_rank(self):
        self._cached_global_worker_rank = get_global_rank()

    def _decode_sample(self, sample: Dict[str, bytes]) -> Dict[str, Any]:
        decoded_sample = {}
        for key, value in sample.items():
            if isinstance(value, pa.Buffer):
                ref = value
                value = value.to_pybytes()
                del ref  # we've copied the memory, free it

            decoded_sample[key] = self.decoders.get(key, no_decoder)(value)
        return decoded_sample

    def process_sample(self, sample: Dict[str, bytes]) -> Dict[str, bytes]:
        """Override this method to process the sample before decoding"""
        return sample

    def __iter__(self):
        self.reset(get_global_world_size())

        self._workers = [
            threading.Thread(
                target=self.downloader.run,
                args=(self._worker_infos[self.global_rank],),
            )
            for _ in range(self.max_workers // 2)
        ] + [
            threading.Thread(
                target=self.extractor.run,
                args=(self.global_rank,),
            )
            for _ in range(self.max_workers // 2)
        ]

        for worker in self._workers:
            worker.start()

        try:
            while not self._stop_event.is_set():
                if self._dataset_finished_event.is_set():
                    logger.debug("Dataset finished")
                    break

                sample = self._samples_queue.get()
                sample = self._decode_sample(sample)

                # Extract internal keys
                internal_keys = {
                    "__wds_global_rank__": sample.pop("__wds_global_rank__", None),
                    "__wds_shard_idx__": sample.pop("__wds_shard_idx__", None),
                    "__wds_sample_key__": sample.pop("__wds_sample_key__", None),
                }

                # Process the sample
                sample = self.process_sample(sample)

                # Check if internal keys were reintroduced
                for key in internal_keys:
                    if key in sample:
                        raise ValueError(
                            f"Internal key '{key}' was reintroduced in process_sample method."
                        )

                # Put back internal keys
                sample.update(internal_keys)

                # Update worker info
                self._worker_infos[self.global_rank].idx = max(
                    internal_keys["__wds_shard_idx__"],
                    self._worker_infos[self.global_rank].idx,
                )

                yield sample
                self._samples_queue.task_done()

        except Exception as e:
            logger.error(f"Error in dataset: {e}")
            self._stop_event.set()
            for worker in self._workers:
                worker.join()
            raise e

        finally:
            self._stop_event.set()
            for worker in self._workers:
                worker.join()

    def __del__(self):
        self._stop_event.set()
        for worker in self._workers:
            if worker.is_alive():
                worker.join()
