# Types

[Streaming-wds Index](../README.md#streaming-wds-index) / [Core](./index.md#core) / Types

> Auto-generated documentation for [core.types](../../streaming_wds/core/types.py) module.

- [Types](#types)
  - [StateDict](#statedict)
    - [StateDict().to_dict](#statedict()to_dict)
  - [WorkerInfo](#workerinfo)
    - [WorkerInfo.default](#workerinfodefault)
    - [WorkerInfo().local_idx](#workerinfo()local_idx)

## StateDict

[Show source in types.py:29](../../streaming_wds/core/types.py#L29)

#### Signature

```python
class StateDict: ...
```

### StateDict().to_dict

[Show source in types.py:33](../../streaming_wds/core/types.py#L33)

#### Signature

```python
def to_dict(self) -> Dict[str, Any]: ...
```



## WorkerInfo

[Show source in types.py:6](../../streaming_wds/core/types.py#L6)

#### Signature

```python
class WorkerInfo: ...
```

### WorkerInfo.default

[Show source in types.py:14](../../streaming_wds/core/types.py#L14)

#### Signature

```python
@staticmethod
def default(dataset_len: int): ...
```

### WorkerInfo().local_idx

[Show source in types.py:23](../../streaming_wds/core/types.py#L23)

#### Signature

```python
@property
def local_idx(self) -> int: ...
```