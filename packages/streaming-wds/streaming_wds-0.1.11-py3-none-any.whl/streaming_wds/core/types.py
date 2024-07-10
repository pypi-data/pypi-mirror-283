from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class WorkerInfo:
    start: int  # global start index
    end: int  # global end index

    rank: int = 0  # global rank
    idx: int = 0  # max global idx
    resume: bool = False

    @staticmethod
    def default(dataset_len: int):
        return WorkerInfo(
            start=0,
            end=dataset_len - 1,
            rank=0,
            idx=0,
        )

    @property
    def local_idx(self) -> int:
        return self.idx - self.start


@dataclass
class StateDict:
    global_world_size: int
    worker_infos: List[WorkerInfo]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dist_world_size": self.dist_world_size,
            "mp_world_size": self.mp_world_size,
            "worker_infos": [w.__dict__ for w in self.worker_infos],
        }
