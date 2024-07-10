import logging
from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from torch.utils.data import DataLoader

from .core.sharder import compute_worker_infos, distribute_worker_infos
from .core.types import StateDict
from .dataset import StreamingWebDataset
from .utils import get_dist_world_size

logger = logging.getLogger(__name__)


def patch_collate_fn(collate_fn: Callable) -> Callable:
    """
    Patch a collate function to exclude certain WebDataset-specific keys from collation.

    This function takes a collate function and returns a new function that wraps the original.
    The new function removes specific keys (__wds_global_rank__, __wds_shard_idx__, and
    __wds_sample_key__) from the input dictionaries before collation, then adds them back
    to the collated output. It also checks that each item in the batch is a dictionary.

    Args:
        collate_fn (Callable): The original collate function to be patched. This function
                               should take a list of dictionaries and return a single
                               dictionary with collated values.

    Returns:
        Callable: A new collate function that wraps the original, excluding specific keys
                  from collation and re-adding them to the output.

    Raises:
        TypeError: If any item in the input batch is not a dictionary.

    Example:
        >>> def original_collate(batch):
        ...     return {k: [d[k] for d in batch] for k in batch[0]}
        >>> patched_collate = patch_collate_fn(original_collate)
        >>> batch = [
        ...     {"data": 1, "__wds_global_rank__": 0},
        ...     {"data": 2, "__wds_global_rank__": 1}
        ... ]
        >>> result = patched_collate(batch)
        >>> print(result)
        {'data': [1, 2], '__wds_global_rank__': [0, 1]}
    """

    def patched_collate(
        batch: Union[List[Dict[str, Any]], List[Tuple]],
    ) -> Union[Dict[str, List[Any]], Tuple[List[Any]]]:
        if all(isinstance(item, dict) for item in batch):
            # Keys to exclude from collation
            exclude_keys = [
                "__wds_global_rank__",
                "__wds_shard_idx__",
                "__wds_sample_key__",
            ]
            excluded_values = {key: [] for key in exclude_keys}

            # Remove excluded keys from each item in the batch
            filtered_batch = []
            for item in batch:
                filtered_item = {}
                for key, value in item.items():
                    if key in exclude_keys:
                        excluded_values[key].append(value)
                    else:
                        filtered_item[key] = value
                filtered_batch.append(filtered_item)

            # Call the original collate function on the filtered batch
            collated = collate_fn(filtered_batch)

            # Add back the excluded keys
            for key in exclude_keys:
                if excluded_values[key]:
                    collated[key] = excluded_values[key]

        elif all(isinstance(item, tuple) for item in batch):
            ranks = [item[-3] for item in batch]
            shard_indices = [item[-2] for item in batch]
            sample_keys = [item[-1] for item in batch]

            batch = [item[:-3] for item in batch]
            collated = collate_fn(batch)
            collated = (*collated, ranks, shard_indices, sample_keys)

        else:
            raise ValueError(
                "The input batch should contain either dictionaries or tuples."
            )

        return collated

    return patched_collate


class StreamingDataLoader(DataLoader):
    __doc__ = DataLoader.__doc__

    def __init__(
        self,
        dataset: StreamingWebDataset,
        *args: Any,
        num_workers: int = 0,
        shuffle: Optional[bool] = None,
        collate_fn: Optional[Callable] = None,
        **kwargs: Any,
    ) -> None:  # pyright: ignore
        if not isinstance(dataset, (StreamingWebDataset)):
            raise RuntimeError(
                "The provided dataset should be an instance of StreamingWebDataset."
                f" Found {dataset}."
            )

        self.num_shards = dataset.num_shards
        self.global_world_size = get_dist_world_size() * num_workers or 1

        self._worker_infos = compute_worker_infos(
            num_shards=self.num_shards, global_world_size=self.global_world_size
        )
        self._max_idx_for_worker: Dict[int, int] = defaultdict(lambda: 0)

        dataset.set_worker_infos(self._worker_infos)
        dataset.clear_worker_components()

        if shuffle is not None:
            dataset.set_shuffle(shuffle)

        if collate_fn is not None:
            collate_fn = patch_collate_fn(collate_fn)

        super().__init__(
            dataset,
            *args,
            num_workers=num_workers,
            collate_fn=collate_fn,
            **kwargs,
        )

    def __iter__(self) -> Any:
        self.global_world_size = get_dist_world_size() * self.num_workers or 1
        logger.debug(f"Initializing dataset with world size: {self.global_world_size}")

        self._worker_infos = compute_worker_infos(
            num_shards=self.num_shards, global_world_size=self.global_world_size
        )
        self.dataset.set_worker_infos(self._worker_infos)

        for batch in super().__iter__():
            if isinstance(batch, dict):
                source_ranks = batch.pop("__wds_global_rank__")
                shard_indices = batch.pop("__wds_shard_idx__")
                _ = batch.pop("__wds_sample_key__")
            elif isinstance(batch, (tuple, list)):
                source_ranks, shard_indices, _ = batch[-3:]
                batch = batch[:-3]
            else:
                raise ValueError(
                    "The input batch should contain either dictionaries or tuples. "
                    f"Found {type(batch)}"
                )
            # update the max index for each worker
            for source_rank, shard_idx in zip(source_ranks, shard_indices):
                self._max_idx_for_worker[source_rank] = max(
                    self._max_idx_for_worker[source_rank], shard_idx
                )

            yield batch

    def state_dict(self) -> Dict[str, Any]:
        # update the worker_infos with the max index
        for worker_info in self._worker_infos:
            worker_info.idx = self._max_idx_for_worker[worker_info.rank]

        return StateDict(
            num_shards=self.num_shards,
            worker_infos=self.worker_infos,
        ).to_dict()

    def load_state_dict(self, obj: Dict[str, Any]) -> None:
        state_dict = StateDict.from_dict(obj)
        if state_dict.num_shards != self.num_shards:
            raise RuntimeError(
                f"Number of shards in the state_dict ({state_dict.num_shards}) "
                f"does not match the number of shards in the dataset ({self.num_shards})."
            )
        distributed_worker_infos = distribute_worker_infos(
            self.global_world_size, state_dict.worker_infos, resume=True
        )
        self.dataset.set_worker_infos(distributed_worker_infos)
