# Types

[Streaming-wds Index](../README.md#streaming-wds-index) / [Core](./index.md#core) / Types

> Auto-generated documentation for [core.types](../../streaming_wds/core/types.py) module.

- [Types](#types)
  - [Bytes](#bytes)
  - [StateDict](#statedict)
    - [StateDict.from_dict](#statedictfrom_dict)
    - [StateDict().to_dict](#statedict()to_dict)
  - [WorkerInfo](#workerinfo)
    - [WorkerInfo.default](#workerinfodefault)
    - [WorkerInfo.from_dict](#workerinfofrom_dict)
    - [WorkerInfo().local_idx](#workerinfo()local_idx)
    - [WorkerInfo().to_dict](#workerinfo()to_dict)

## Bytes

[Show source in types.py:68](../../streaming_wds/core/types.py#L68)

#### Signature

```python
class Bytes:
    def __init__(self, value: Union[int, str, "Bytes"]): ...
```



## StateDict

[Show source in types.py:49](../../streaming_wds/core/types.py#L49)

#### Signature

```python
class StateDict: ...
```

### StateDict.from_dict

[Show source in types.py:59](../../streaming_wds/core/types.py#L59)

#### Signature

```python
@classmethod
def from_dict(cls, d: Dict[str, Any]): ...
```

### StateDict().to_dict

[Show source in types.py:53](../../streaming_wds/core/types.py#L53)

#### Signature

```python
def to_dict(self) -> Dict[str, Any]: ...
```



## WorkerInfo

[Show source in types.py:7](../../streaming_wds/core/types.py#L7)

#### Signature

```python
class WorkerInfo: ...
```

### WorkerInfo.default

[Show source in types.py:15](../../streaming_wds/core/types.py#L15)

#### Signature

```python
@staticmethod
def default(dataset_len: int): ...
```

### WorkerInfo.from_dict

[Show source in types.py:37](../../streaming_wds/core/types.py#L37)

#### Signature

```python
@classmethod
def from_dict(cls, d: Dict[str, Any]): ...
```

### WorkerInfo().local_idx

[Show source in types.py:24](../../streaming_wds/core/types.py#L24)

#### Signature

```python
@property
def local_idx(self) -> int: ...
```

### WorkerInfo().to_dict

[Show source in types.py:28](../../streaming_wds/core/types.py#L28)

#### Signature

```python
def to_dict(self): ...
```
