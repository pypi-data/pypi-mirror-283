# Sharder

[Streaming-wds Index](../README.md#streaming-wds-index) / [Core](./index.md#core) / Sharder

> Auto-generated documentation for [core.sharder](../../streaming_wds/core/sharder.py) module.

- [Sharder](#sharder)
  - [GetWorkerSplit](#getworkersplit)
    - [GetWorkerSplit.apply](#getworkersplitapply)
  - [OrderByStride](#orderbystride)
    - [OrderByStride.apply](#orderbystrideapply)
  - [ShardListMutator](#shardlistmutator)
    - [ShardListMutator().apply](#shardlistmutator()apply)
  - [Shuffle](#shuffle)
    - [Shuffle.apply](#shuffleapply)
  - [distribute_worker_infos](#distribute_worker_infos)

## GetWorkerSplit

[Show source in sharder.py:71](../../streaming_wds/core/sharder.py#L71)

#### Signature

```python
class GetWorkerSplit(ShardListMutator): ...
```

#### See also

- [ShardListMutator](#shardlistmutator)

### GetWorkerSplit.apply

[Show source in sharder.py:85](../../streaming_wds/core/sharder.py#L85)

#### Signature

```python
@staticmethod
def apply(paths: List[str], worker_info: WorkerInfo) -> List[str]: ...
```



## OrderByStride

[Show source in sharder.py:36](../../streaming_wds/core/sharder.py#L36)

#### Signature

```python
class OrderByStride(ShardListMutator): ...
```

#### See also

- [ShardListMutator](#shardlistmutator)

### OrderByStride.apply

[Show source in sharder.py:37](../../streaming_wds/core/sharder.py#L37)

#### Signature

```python
@staticmethod
def apply(paths: List[str], state_dict: StateDict) -> List[str]: ...
```



## ShardListMutator

[Show source in sharder.py:17](../../streaming_wds/core/sharder.py#L17)

Abstract base class for shard list mutators.

#### Signature

```python
class ShardListMutator(ABC): ...
```

### ShardListMutator().apply

[Show source in sharder.py:20](../../streaming_wds/core/sharder.py#L20)

Apply the mutation to the list of shard paths.

#### Arguments

- `paths` *List[str]* - The list of shard paths to mutate.
- `*args` - Variable length argument list.
- `**kwargs` - Arbitrary keyword arguments.

#### Returns

- `List[str]` - The mutated list of shard paths.

#### Signature

```python
@abstractmethod
def apply(self, paths: List[str], *args, **kwargs) -> List[str]: ...
```



## Shuffle

[Show source in sharder.py:59](../../streaming_wds/core/sharder.py#L59)

Deterministically shuffle paths.

#### Signature

```python
class Shuffle(ShardListMutator): ...
```

#### See also

- [ShardListMutator](#shardlistmutator)

### Shuffle.apply

[Show source in sharder.py:62](../../streaming_wds/core/sharder.py#L62)

#### Signature

```python
@staticmethod
def apply(paths: list[str]) -> list[str]: ...
```



## distribute_worker_infos

[Show source in sharder.py:92](../../streaming_wds/core/sharder.py#L92)

Distribute the workload from a list of previous worker infos across a new world size.

This function takes a list of previous WorkerInfo objects and redistributes their
workload across a potentially different number of workers (global_world_size).
It ensures that the total range of indices is preserved and distributed as evenly
as possible among the new set of workers.

#### Arguments

- `global_world_size` *int* - The new total number of workers.
- `worker_infos` *List[WorkerInfo]* - List of previous WorkerInfo objects.
- `resume` *bool, optional* - Whether to resume from previous state. Defaults to False.

#### Returns

- `List[WorkerInfo]` - A new list of WorkerInfo objects distributed across the new world size.

#### Raises

- `ValueError` - If global_world_size is greater than the total range of indices.

#### Signature

```python
def distribute_worker_infos(
    global_world_size: int, worker_infos: List[WorkerInfo], resume: bool = False
) -> List[WorkerInfo]: ...
```