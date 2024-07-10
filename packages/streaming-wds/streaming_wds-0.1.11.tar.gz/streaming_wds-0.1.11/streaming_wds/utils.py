import random
from contextlib import contextmanager
from queue import Queue
from typing import Generator

import numpy as np
import torch
import torch.distributed as dist


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
