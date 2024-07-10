import logging
import os
import random
import shutil
import time
from contextlib import contextmanager
from pathlib import Path
from queue import Queue
from typing import Generator, Optional
from urllib.parse import urlparse

import numpy as np
import torch
import torch.distributed as dist
from filelock import FileLock, Timeout

logger = logging.getLogger(__name__)


@contextmanager
def isolate_rng(include_cuda: bool = True) -> Generator[None, None, None]:
    """A context manager that resets the global random state on exit to what it was before entering.

    It supports isolating the states for PyTorch, Numpy, and Python built-in random number generators.

    Args:
        include_cuda: Whether to allow this function to also control the `torch.cuda` random number generator.
            Set this to ``False`` when using the function in a forked process where CUDA re-initialization is
            prohibited.

    Example:
        >>> import torch
        >>> torch.manual_seed(1)  # doctest: +ELLIPSIS
        <torch._C.Generator object at ...>
        >>> with isolate_rng():
        ...     [torch.rand(1) for _ in range(3)]
        [tensor([0.7576]), tensor([0.2793]), tensor([0.4031])]
        >>> torch.rand(1)
        tensor([0.7576])

    """
    python_state = random.getstate()
    numpy_state = np.random.get_state()
    torch_state = torch.get_rng_state()
    cuda_state = (
        torch.cuda.get_rng_state_all()
        if include_cuda and torch.cuda.is_available()
        else None
    )

    try:
        yield
    finally:
        random.setstate(python_state)
        np.random.set_state(numpy_state)
        torch.set_rng_state(torch_state)
        if cuda_state is not None:
            torch.cuda.set_rng_state_all(cuda_state)


def get_global_world_size() -> int:
    """
    Get the total number of workers across all distributed processes and data loader workers.

    Returns:
        int: The global world size, which is the product of the distributed world size
             and the number of data loader workers.
    """
    curr_mp_world_size = (
        torch.utils.data.get_worker_info().num_workers
        if torch.utils.data.get_worker_info()
        else 1
    )
    if dist.is_initialized():
        return dist.get_world_size() * curr_mp_world_size
    return curr_mp_world_size


def get_dist_world_size() -> int:
    """
    Get the number of processes in the distributed training setup.

    Returns:
        int: The number of distributed processes if distributed training is initialized,
             otherwise 1.
    """
    if dist.is_initialized():
        return dist.get_world_size()
    return 1


def get_mp_world_size() -> int:
    """
    Get the number of worker processes for the current DataLoader.

    Returns:
        int: The number of worker processes if running in a DataLoader worker,
             otherwise 1.
    """
    return (
        torch.utils.data.get_worker_info().num_workers
        if torch.utils.data.get_worker_info()
        else 1
    )


def get_dist_rank() -> int:
    """
    Get the rank of the current process in the distributed training setup.

    Returns:
        int: The rank of the current process if distributed training is initialized,
             otherwise 0.
    """
    if dist.is_initialized():
        return dist.get_rank()
    return 0


def get_mp_rank() -> int:
    """
    Get the rank of the current DataLoader worker process.

    Returns:
        int: The rank of the current DataLoader worker if running in a worker process,
             otherwise 0.
    """
    return (
        torch.utils.data.get_worker_info().id
        if torch.utils.data.get_worker_info()
        else 0
    )


def get_global_rank() -> int:
    """
    Get the global rank of the current process, considering both distributed training
    and DataLoader workers.

    Returns:
        int: The global rank of the current process.
    """
    curr_mp_world_size = get_mp_world_size()
    curr_mp_rank = get_mp_rank()
    curr_dist_rank = get_dist_rank()

    return curr_dist_rank * curr_mp_world_size + curr_mp_rank


def empty_queue(queue: Queue):
    """
    Empty a queue by removing and discarding all its items.

    Args:
        queue (Queue): The queue to be emptied.
    """
    while not queue.empty():
        try:
            queue.get_nowait()
        except Exception:
            pass
        queue.task_done()


@contextmanager
def cache_lock(remote: str, split: Optional[str] = None, rank: Optional[int] = None):
    """
    A context manager that uses a file lock to ensure the code within is executed only once.

    This function creates a lock file based on the remote URL and split, and attempts to acquire
    a lock on this file. If successful, it yields True, indicating that the calling process
    should execute the code within the context. If unsuccessful, it yields False, indicating
    that the calling process should skip the code within the context.

    Args:
        remote (str): The remote URL of the dataset.
        split (Optional[str]): The split name of the dataset, if applicable.

    Yields:
        bool: True if the lock was acquired (indicating the process should execute the code),
              False otherwise.

    Example:
        with cache_lock("https://example.com/data", "train") as acquired:
            if acquired:
                # This code will only be executed by one process
                download_and_process_data()
    """
    if split:
        remote = os.path.join(remote, split)
    if rank is not None:
        remote = os.path.join(remote, str(rank))

    parsed_uri = urlparse(remote)
    bucket = parsed_uri.netloc
    key_prefix = parsed_uri.path.lstrip("/")
    lock_file = Path.home() / ".cache" / "streaming_wds" / f"{bucket}_{key_prefix}.lock"

    lock_file.parent.mkdir(parents=True, exist_ok=True)
    lock = FileLock(str(lock_file))

    try:
        with lock.acquire(timeout=1):
            yield True  # Lock acquired, this process should handle the code within the context
            # Ensure the lock is held for a minimum duration
            time.sleep(0.1)
    except Timeout:
        yield False  # Lock not acquired, this process should not handle the code within the context
    finally:
        if lock_file.exists():
            try:
                lock_file.unlink()  # Remove the lock file
            except OSError:
                pass  # Ignore errors if the file can't be removed
        if dist.is_initialized():
            dist.barrier()


def clear_stale_caches(remote: str, split: Optional[str] = None):
    """
    Clear stale caches for a specific remote and split.

    This function deletes the cache directory for the given remote and split.

    Args:
        remote (str): The remote URL of the dataset.
        split (str): The split name of the dataset.

    Returns:
        bool: True if the cache was successfully cleared, False otherwise.
    """

    with cache_lock(remote, split):
        if split is not None:
            remote = os.path.join(remote, split)

        parsed_uri = urlparse(remote)
        bucket = parsed_uri.netloc
        key_prefix = parsed_uri.path.lstrip("/")
        cache_dir = Path.home() / ".cache" / "streaming_wds" / bucket / key_prefix

        if cache_dir.exists():
            try:
                shutil.rmtree(cache_dir)
                logger.info(f"Cleared cache for remote {remote} at {cache_dir}")
            except OSError:
                pass
        else:
            logger.info(f"No cache found for remote {remote} at {cache_dir}")
