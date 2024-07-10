import logging
import math
from abc import ABC, abstractmethod
from typing import List, Tuple

import torch

from streaming_wds.core.types import StateDict, WorkerInfo
from streaming_wds.utils import (
    get_global_world_size,
    isolate_rng,
)

logger = logging.getLogger(__name__)


class ShardListMutator(ABC):
    """Abstract base class for shard list mutators."""

    @abstractmethod
    def apply(self, paths: List[str], *args, **kwargs) -> List[str]:
        """
        Apply the mutation to the list of shard paths.

        Args:
            paths (List[str]): The list of shard paths to mutate.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            List[str]: The mutated list of shard paths.
        """
        pass


class OrderByStride(ShardListMutator):
    @staticmethod
    def apply(paths: List[str], state_dict: StateDict) -> List[str]:
        prev_world_size = state_dict.global_world_size
        curr_world_size = get_global_world_size()

        if prev_world_size == curr_world_size:
            return paths  # No reordering needed if world size hasn't changed

        # Reorder paths to account for the new stride
        reordered_paths = []
        for i in range(curr_world_size):
            j = 0
            while i + j * curr_world_size < len(paths):
                old_index = (
                    i * prev_world_size // curr_world_size + j * prev_world_size
                ) % len(paths)
                reordered_paths.append(paths[old_index])
                j += 1

        return reordered_paths


class Shuffle(ShardListMutator):
    """Deterministically shuffle paths."""

    @staticmethod
    def apply(paths: list[str]) -> list[str]:
        with isolate_rng():
            generator = torch.Generator()
            generator.manual_seed(torch.initial_seed())
            paths = [paths[i] for i in torch.randperm(len(paths), generator=generator)]
        return paths


class GetWorkerSplit(ShardListMutator):
    @staticmethod
    def _split(
        paths: List[str],
        num_shards: int,
        shard_idx: int,
    ) -> Tuple[List[str], WorkerInfo]:
        per_shard = int(math.ceil(len(paths) / float(num_shards)))
        start = shard_idx * per_shard
        end = min(start + per_shard, len(paths))
        paths = paths[start:end]

        return paths

    @staticmethod
    def apply(paths: List[str], worker_info: WorkerInfo) -> List[str]:
        return GetWorkerSplit._split(
            paths, num_shards=get_global_world_size(), shard_idx=worker_info.rank
        )


def distribute_worker_infos(
    global_world_size: int, worker_infos: List[WorkerInfo], resume: bool = False
) -> List[WorkerInfo]:
    """
    Distribute the workload from a list of previous worker infos across a new world size.

    This function takes a list of previous WorkerInfo objects and redistributes their
    workload across a potentially different number of workers (global_world_size).
    It ensures that the total range of indices is preserved and distributed as evenly
    as possible among the new set of workers.

    Args:
        global_world_size (int): The new total number of workers.
        worker_infos (List[WorkerInfo]): List of previous WorkerInfo objects.
        resume (bool, optional): Whether to resume from previous state. Defaults to False.

    Returns:
        List[WorkerInfo]: A new list of WorkerInfo objects distributed across the new world size.

    Raises:
        ValueError: If global_world_size is greater than the total range of indices.
    """
    if global_world_size == len(worker_infos):
        return [
            WorkerInfo(
                start=wi.start,
                end=wi.end,
                rank=wi.rank,
                idx=wi.idx,
                resume=resume,
            )
            for wi in worker_infos
        ]

    # Calculate the total range of indices
    total_range = sum(wi.end - wi.start for wi in worker_infos)

    # Check if global_world_size is greater than total_range
    if global_world_size > total_range:
        raise ValueError(
            f"Global world size ({global_world_size}) is greater than "
            f"the total range of indices ({total_range}). "
            "Cannot distribute workload across all workers. "
            "Consider reducing the number of DataLoader workers "
            "or increase the number of shards in your dataset."
        )
    # Calculate the new chunk size for each worker
    chunk_size = math.ceil(total_range / global_world_size)

    new_worker_infos = []
    current_start = 0
    original_wi_index = 0

    for i in range(global_world_size):
        end = min(current_start + chunk_size, total_range)

        # Find the correct idx from the original worker_infos
        while (
            original_wi_index < len(worker_infos)
            and worker_infos[original_wi_index].end <= current_start
        ):
            original_wi_index += 1

        if original_wi_index < len(worker_infos):
            original_wi = worker_infos[original_wi_index]
            idx = max(current_start, min(original_wi.idx, end - 1))
        else:
            idx = current_start

        new_worker_info = WorkerInfo(
            start=current_start, end=end, rank=i, idx=idx, resume=resume
        )
        new_worker_infos.append(new_worker_info)
        current_start = end

    return new_worker_infos
