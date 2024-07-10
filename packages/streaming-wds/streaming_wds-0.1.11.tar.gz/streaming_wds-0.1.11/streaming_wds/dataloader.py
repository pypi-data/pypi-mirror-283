from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional, cast

from torch import Tensor
from torch.utils.data import DataLoader

from .core.types import StateDict
from .dataset import StreamingWebDataset
from .utils import get_dist_world_size


def patch_collate_fn(collate_fn: Callable) -> Callable:
    def _collate_fn(batch: List[Dict[str, Any]]) -> Dict[str, Any]:
        source_ranks = [item.pop("__wds_global_rank__") for item in batch]
        shard_indices = [item.pop("__wds_shard_idx__") for item in batch]
        sample_keys = [item.pop("__wds_sample_key__") for item in batch]

        collated_batch = collate_fn(batch)

        if not isinstance(collated_batch, dict):
            raise RuntimeError(
                f"Expected collate_fn to return a dictionary. Found {type(collated_batch)}."
            )

        collated_batch["__wds_global_rank__"] = source_ranks
        collated_batch["__wds_shard_idx__"] = shard_indices
        collated_batch["__wds_sample_key__"] = sample_keys

        return collate_fn(collated_batch) if collate_fn is not None else collated_batch

    return _collate_fn


class StreamingDataLoader(DataLoader):
    __doc__ = DataLoader.__doc__

    def __init__(
        self,
        dataset: StreamingWebDataset,
        *args: Any,
        batch_size: int = 1,
        num_workers: int = 0,
        prefetch_factor: Optional[int] = None,
        shuffle: Optional[bool] = None,
        drop_last: Optional[bool] = False,
        collate_fn: Optional[Callable] = None,
        **kwargs: Any,
    ) -> None:  # pyright: ignore
        if not isinstance(dataset, (StreamingWebDataset)):
            raise RuntimeError(
                "The provided dataset should be an instance of StreamingWebDataset."
                f" Found {dataset}."
            )

        self._worker_infos = dataset.get_worker_infos(
            get_dist_world_size() * num_workers or 1
        )
        self._max_idx_for_worker: Dict[int, int] = defaultdict(lambda: 0)

        if shuffle is not None:
            dataset.set_shuffle(shuffle)

        if drop_last is not None:
            dataset.set_drop_last(drop_last)

        if collate_fn is not None:
            collate_fn = patch_collate_fn(collate_fn)

        super().__init__(
            dataset,
            *args,
            batch_size=batch_size,
            num_workers=num_workers,
            prefetch_factor=(10 if num_workers > 0 else None)
            if prefetch_factor is None
            else prefetch_factor,
            collate_fn=collate_fn,
            **kwargs,
        )

    def __iter__(self) -> Any:
        for batch in super().__iter__():
            source_ranks = cast(Tensor, batch.pop("__wds_global_rank__")).tolist()
            shard_indices = cast(Tensor, batch.pop("__wds_shard_idx__")).tolist()
            _ = cast(List[str], batch.pop("__wds_sample_key__"))

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
            global_world_size=get_dist_world_size() * self.num_workers,
            worker_infos=self.worker_infos,
        ).to_dict()

    def load_state_dict(self, obj: Dict[str, Any]) -> None:
        self.dataset.load_state_dict(StateDict(**obj))
