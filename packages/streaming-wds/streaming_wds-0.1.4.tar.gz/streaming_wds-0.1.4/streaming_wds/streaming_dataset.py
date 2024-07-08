import io
import logging
import math
import os
import tarfile
import threading
from queue import Empty, Queue
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import boto3
import pyarrow as pa
import torch
from torch.utils.data import IterableDataset

from .decoders import no_decoder, select_decoder
from .utils import isolate_rng

logging.getLogger('botocore.configprovider').setLevel(logging.WARNING)

class StreamingWebDataset(IterableDataset):
    def __init__(
        self,
        remote: str,
        split: Optional[str] = None,
        profile: str = "default",
        prefetch: int = 2,
        shuffle: bool = False,
        max_workers: int = 2,
        schema: Dict[str, str] = {},
    ):
        self.remote = os.path.join(remote, split) if split else remote
        self.prefetch = prefetch
        self.shuffle = shuffle
        self.max_workers = max(2, (max_workers + 1) // 2 * 2)
        self.decoders = {k: select_decoder(v) for (k, v) in schema.items()}

        parsed_uri = urlparse(self.remote)
        self.bucket = parsed_uri.netloc
        self.key_prefix = parsed_uri.path.lstrip("/")

        self.session = boto3.Session(profile_name=profile)
        self.paths = []

        self.download_queue = Queue()
        self.extract_queue = Queue(maxsize=prefetch)
        self.extracted = Queue()

        self._current_shard_idx = 0
        self._current_key_idx = 0

        self._resume_from_shard_idx = 0
        self._resume_from_key_idx = 0
        self._num_workers = None

        self.stop_event = threading.Event()
        self.workers = []

    def setup(self):
        if not self.paths:
            s3 = self.session.client("s3")
            paginator = s3.get_paginator("list_objects_v2")
            for result in paginator.paginate(Bucket=self.bucket, Prefix=self.key_prefix):
                for content in result.get("Contents", []):
                    if content["Key"].endswith(".tar"):
                        self.paths.append(content["Key"])

            self.paths.sort()
            worker_paths = self._get_worker_paths()

            if self.shuffle:
                with isolate_rng():
                    generator = torch.Generator()
                    generator.manual_seed(torch.initial_seed())
                    worker_paths = [
                        worker_paths[i]
                        for i in torch.randperm(len(worker_paths), generator=generator)
                    ]

            for path in worker_paths:
                self.download_queue.put(path)

    def _get_worker_paths(self):
        worker_info = torch.utils.data.get_worker_info()
        if worker_info is None:
            return self.paths
        else:
            per_worker = int(math.ceil(len(self.paths) / float(worker_info.num_workers)))
            worker_id = worker_info.id
            start = worker_id * per_worker
            end = min(start + per_worker, len(self.paths))
            return self.paths[start:end]

    def download_worker(self):
        s3 = self.session.client('s3')
        idx = 0
        while not self.stop_event.is_set():
            if idx != 0 and self.download_queue.empty():
                self.extract_queue.put((None, None))
                self._resume_from_shard_idx = 0
                break
            try:
                path = self.download_queue.get(timeout=1)
                if idx < self._resume_from_shard_idx:
                    idx += 1
                    continue

                response = s3.get_object(Bucket=self.bucket, Key=path)
                body = response['Body'].read()

                self.extract_queue.put((idx, body))
                idx += 1
                self._resume_from_shard_idx = 0
            except Empty:  # Changed from Queue.Empty to Empty
                continue
            finally:
                self.download_queue.task_done()

    def extract_worker(self):
        while not self.stop_event.is_set():
            try:
                path_idx, body = self.extract_queue.get(timeout=1)

                if path_idx is None and body is None:
                    # Signal to stop
                    self.extract_queue.task_done()
                    break

                tar = tarfile.open(fileobj=io.BytesIO(body), mode="r")
                current_key, key_idx = None, 0
                aggregated = {}

                sorted_members = sorted(tar.getmembers(), key=lambda m: m.name)
                for member in sorted_members:
                    if member.isfile():
                        key, ext = os.path.splitext(member.name)

                        if key != current_key:
                            if aggregated and key_idx >= self._resume_from_key_idx:
                                self.extracted.put(aggregated)
                            current_key = key
                            key_idx += 1
                            aggregated = {}

                        aggregated[ext] = pa.py_buffer(tar.extractfile(member).read())
                        aggregated["__key_idx__"] = key_idx
                        aggregated["__path_idx__"] = path_idx
                if aggregated:
                    self.extracted.put(aggregated)
                self._resume_from_key_idx = 0
                
                # Mark the task as done after processing the entire tar file
                self.extract_queue.task_done()

            except Empty:
                continue
            except Exception as e:
                print(f"Error in extract_worker: {e}")
                # You might want to add more robust error handling here

    def load_state_dict(self, state_dict):
        torch.set_rng_state(state_dict["rng"])
        self._num_workers = state_dict["num_workers"]
        self._resume_from_shard_idx = state_dict["current_shard_idx"]
        self._resume_from_key_idx = state_dict["current_key_idx"]

        self._current_key_idx = self._resume_from_key_idx
        self._current_shard_idx = self._resume_from_shard_idx

    def state_dict(self):
        return {
            "rng": torch.get_rng_state(),
            "num_workers": self._num_workers,
            "current_shard_idx": self._current_shard_idx,
            "current_key_idx": self._current_key_idx,
        }

    def __getitem__(self, index) -> Any:
        return {
            k: self.decoders.get(k, no_decoder)(v.to_pybytes())
            for k, v in self.current_sample.items()
        }

    def __iter__(self):
        self.setup()
        self.stop_event.clear()
        self.workers = [
            threading.Thread(target=self.download_worker)
            for _ in range(self.max_workers // 2)
        ] + [
            threading.Thread(target=self.extract_worker)
            for _ in range(self.max_workers // 2)
        ]

        for worker in self.workers:
            worker.start()

        try:
            while not self.stop_event.is_set():
                try:
                    sample = self.extracted.get(timeout=1)
                    self._current_path_idx = sample["__path_idx__"]
                    self._current_key_idx = sample["__key_idx__"]
                    sample.pop("__path_idx__", None)
                    sample.pop("__key_idx__", None)
                    self.current_sample = sample

                    yield self.__getitem__(0)
                except Empty:  # Changed from Queue.Empty to Empty
                    if (
                        self.download_queue.empty()
                        and self.extract_queue.empty()
                        and self.extracted.empty()
                    ):
                        break
        finally:
            self.stop_event.set()
            for worker in self.workers:
                worker.join()

    def __del__(self):
        self.stop_event.set()
        for worker in self.workers:
            if worker.is_alive():
                worker.join()
