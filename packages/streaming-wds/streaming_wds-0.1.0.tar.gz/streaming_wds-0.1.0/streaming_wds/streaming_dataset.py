import asyncio
import io
import math
import os
import tarfile
from contextlib import suppress
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import pyarrow as pa
import torch
from aiobotocore.session import AioSession
from torch.utils.data import IterableDataset

from .decoders import select_decoder
from .utils import isolate_rng


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

        self.session = AioSession(profile=profile)
        self.paths = []  # This will be populated in the setup method

        self.download_queue = asyncio.Queue()
        self.extract_queue = asyncio.Queue(maxsize=prefetch)
        self.extracted = asyncio.Queue()

        self._current_shard_idx = 0
        self._current_key_idx = 0

        self._resume_from_shard_idx = 0
        self._resume_from_key_idx = 0
        self._num_workers = None

        self.loop = None
        self.workers = []
        self.stop_event = asyncio.Event()

    async def setup(self):
        if not self.paths:
            async with self.session.create_client("s3") as client:
                paginator = client.get_paginator("list_objects_v2")
                async for result in paginator.paginate(
                    Bucket=self.bucket, Prefix=self.key_prefix
                ):
                    for content in result.get("Contents", []):
                        if content["Key"].endswith(".tar"):
                            self.paths.append(content["Key"])

            # Populate the download queue
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
                await self.download_queue.put(path)

    def _get_worker_paths(self):
        worker_info = torch.utils.data.get_worker_info()
        if worker_info is None:
            # Single-process data loading, use the whole dataset
            return self.paths
        else:
            # In a worker process, split the paths
            per_worker = int(
                math.ceil(len(self.paths) / float(worker_info.num_workers))
            )
            worker_id = worker_info.id
            start = worker_id * per_worker
            end = min(start + per_worker, len(self.paths))
            return self.paths[start:end]

    async def download_worker(self):
        async with self.session.create_client("s3") as client:
            idx = 0
            while not self.stop_event.is_set():
                if idx != 0 and self.download_queue.empty():
                    await self.extract_queue.put((None, None))
                    self.download_queue.task_done()
                    self._resume_from_shard_idx = 0
                    break
                try:
                    path = await self.download_queue.get()
                    if idx < self._resume_from_shard_idx:
                        idx += 1
                        continue

                    response = await client.get_object(Bucket=self.bucket, Key=path)
                    body = await response["Body"].read()

                    await self.extract_queue.put((idx, body))
                    idx += 1
                    self._resume_from_shard_idx = 0
                except asyncio.CancelledError:
                    break
                finally:
                    self.download_queue.task_done()

    async def extract_worker(self):
        while not self.stop_event.is_set():
            try:
                path_idx, body = await self.extract_queue.get()

                if path_idx is None and body is None:
                    # Final element reached
                    self.extract_queue.task_done()
                    break

                try:
                    tar = tarfile.open(fileobj=io.BytesIO(body), mode="r")
                    current_key, key_idx = None, 0
                    aggregated = {}

                    # Sort the members in the tar first
                    sorted_members = sorted(tar.getmembers(), key=lambda m: m.name)
                    for member in sorted_members:
                        if member.isfile():
                            key, ext = os.path.splitext(member.name)

                            if key != current_key:
                                if aggregated and key_idx >= self._resume_from_key_idx:
                                    await self.extracted.put(aggregated)
                                current_key = key
                                key_idx += 1
                                aggregated = {}

                            aggregated[ext] = pa.py_buffer(
                                tar.extractfile(member).read()
                            )
                            aggregated["__key_idx__"] = key_idx
                            aggregated["__path_idx__"] = path_idx
                    if aggregated:
                        await self.extracted.put(aggregated)
                    self._resume_from_key_idx = 0
                finally:
                    # Ensure we always mark the task as done, even if an exception occurs
                    self.extract_queue.task_done()
            except asyncio.CancelledError:
                break
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

    async def __aiter__(self):
        await self.setup()
        self.stop_event.clear()
        self.workers = [
            asyncio.create_task(self.download_worker())
            for _ in range(self.max_workers // 2)
        ] + [
            asyncio.create_task(self.extract_worker())
            for _ in range(self.max_workers // 2)
        ]

        try:
            while not self.stop_event.is_set():
                try:
                    sample = await asyncio.wait_for(self.extracted.get(), timeout=1)
                    self._current_path_idx = sample["__path_idx__"]
                    self._current_key_idx = sample["__key_idx__"]
                    sample.pop("__path_idx__", None)
                    sample.pop("__key_idx__", None)
                    self.current_sample = sample

                    yield self.__getitem__(0)
                except asyncio.TimeoutError:
                    if (
                        self.download_queue.empty()
                        and self.extract_queue.empty()
                        and self.extracted.empty()
                    ):
                        break
        finally:
            self.stop_event.set()
            for worker in self.workers:
                worker.cancel()
            with suppress(asyncio.CancelledError):
                await asyncio.gather(*self.workers, return_exceptions=True)

    def __iter__(self):
        if self.loop is None or self.loop.is_closed():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

        return AsyncIterator(self.__aiter__(), self.loop)

    def __del__(self):
        if hasattr(self, "loop") and self.loop and not self.loop.is_closed():
            try:
                if self.loop.is_running():
                    self.loop.call_soon_threadsafe(self.stop_event.set)
                    self.loop.call_soon_threadsafe(
                        lambda: asyncio.gather(*self.workers, return_exceptions=True)
                    )
                else:
                    future = asyncio.run_coroutine_threadsafe(
                        self._cleanup(), self.loop
                    )
                    future.result()
            except Exception:
                # Log any exceptions that occur during cleanup
                logger.exception("Error during cleanup in __del__")
            finally:
                # We don't close the loop here, as it may be shared or still in use
                pass

    async def _cleanup(self):
        await self.stop_event.set()
        await asyncio.gather(*self.workers, return_exceptions=True)


class AsyncIterator:
    def __init__(self, async_generator, loop):
        self.async_generator = async_generator
        self.loop = loop
        self._aiter = None

    def __iter__(self):
        return self

    def __next__(self):
        if self._aiter is None:
            self._aiter = self.async_generator.__aiter__()

        try:
            return self.loop.run_until_complete(self._aiter.__anext__())
        except StopAsyncIteration:
            self._aiter = None
            raise StopIteration

    def __del__(self):
        if self._aiter is not None:
            self.loop.run_until_complete(self._aiter.aclose())
