import logging
import math
from abc import ABC, abstractmethod
from typing import List, Tuple

import torch

from streaming_wds.types import StateDict, WorkerInfo
from streaming_wds.utils import (
    get_global_world_size,
    isolate_rng,
)

logger = logging.getLogger(__name__)


class ShardMutator(ABC):
    """Abstract base class for shard mutators."""

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


class OrderByStride(ShardMutator):
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


class ShardShuffler(ShardMutator):
    """Deterministically shuffle paths."""

    @staticmethod
    def apply(paths: list[str]) -> list[str]:
        with isolate_rng():
            generator = torch.Generator()
            generator.manual_seed(torch.initial_seed())
            paths = [paths[i] for i in torch.randperm(len(paths), generator=generator)]
        return paths


class WorkerShardSplitter(ShardMutator):
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
        return WorkerShardSplitter._split(
            paths, num_shards=get_global_world_size(), shard_idx=worker_info.rank
        )


class ComputeWorkerInfos:
    @staticmethod
    def apply(
        global_world_size: int, worker_infos: List[WorkerInfo], resume: bool = False
    ) -> List[WorkerInfo]:
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
                # progress_in_chunk = current_start - original_wi.start
                idx = max(current_start, min(original_wi.idx, end - 1))
            else:
                idx = current_start

            new_worker_info = WorkerInfo(
                start=current_start, end=end, rank=i, idx=idx, resume=resume
            )
            new_worker_infos.append(new_worker_info)
            current_start = end

        return new_worker_infos
