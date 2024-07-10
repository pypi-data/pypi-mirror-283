# Dataset

[Streaming-wds Index](./README.md#streaming-wds-index) / Dataset

> Auto-generated documentation for [dataset](../streaming_wds/dataset.py) module.

- [Dataset](#dataset)
  - [StreamingWebDataset](#streamingwebdataset)
    - [StreamingWebDataset().get_worker_infos](#streamingwebdataset()get_worker_infos)
    - [StreamingWebDataset().global_rank](#streamingwebdataset()global_rank)
    - [StreamingWebDataset().initialize_worker_components](#streamingwebdataset()initialize_worker_components)
    - [StreamingWebDataset().load_state_dict](#streamingwebdataset()load_state_dict)
    - [StreamingWebDataset().num_shards](#streamingwebdataset()num_shards)
    - [StreamingWebDataset().process_sample](#streamingwebdataset()process_sample)
    - [StreamingWebDataset().reset](#streamingwebdataset()reset)
    - [StreamingWebDataset().reset_global_rank](#streamingwebdataset()reset_global_rank)
    - [StreamingWebDataset().set_drop_last](#streamingwebdataset()set_drop_last)
    - [StreamingWebDataset().set_shuffle](#streamingwebdataset()set_shuffle)
    - [StreamingWebDataset().state_dict](#streamingwebdataset()state_dict)

## StreamingWebDataset

[Show source in dataset.py:29](../streaming_wds/dataset.py#L29)

#### Signature

```python
class StreamingWebDataset(IterableDataset):
    def __init__(
        self,
        remote: str,
        split: Optional[str] = None,
        profile: str = "default",
        buffer_size: int = 2,
        drop_last: bool = True,
        shuffle: bool = False,
        max_workers: int = 2,
        schema: Dict[str, str] = {},
        cache_limit_bytes: int = 2 << 30,
    ): ...
```

### StreamingWebDataset().get_worker_infos

[Show source in dataset.py:142](../streaming_wds/dataset.py#L142)

#### Signature

```python
def get_worker_infos(
    self, global_world_size: int, num_shards: Optional[int] = None
) -> List[WorkerInfo]: ...
```

#### See also

- [WorkerInfo](core/types.md#workerinfo)

### StreamingWebDataset().global_rank

[Show source in dataset.py:152](../streaming_wds/dataset.py#L152)

#### Signature

```python
@property
def global_rank(self): ...
```

### StreamingWebDataset().initialize_worker_components

[Show source in dataset.py:60](../streaming_wds/dataset.py#L60)

#### Signature

```python
def initialize_worker_components(self): ...
```

### StreamingWebDataset().load_state_dict

[Show source in dataset.py:129](../streaming_wds/dataset.py#L129)

#### Signature

```python
def load_state_dict(self, state_dict: StateDict, global_world_size: int): ...
```

#### See also

- [StateDict](core/types.md#statedict)

### StreamingWebDataset().num_shards

[Show source in dataset.py:93](../streaming_wds/dataset.py#L93)

#### Signature

```python
@property
def num_shards(self): ...
```

### StreamingWebDataset().process_sample

[Show source in dataset.py:172](../streaming_wds/dataset.py#L172)

Override this method to process the sample before decoding

#### Signature

```python
def process_sample(self, sample: Dict[str, bytes]) -> Dict[str, bytes]: ...
```

### StreamingWebDataset().reset

[Show source in dataset.py:97](../streaming_wds/dataset.py#L97)

#### Signature

```python
def reset(self, global_world_size: int, state_dict: Optional[StateDict] = None): ...
```

#### See also

- [StateDict](core/types.md#statedict)

### StreamingWebDataset().reset_global_rank

[Show source in dataset.py:158](../streaming_wds/dataset.py#L158)

#### Signature

```python
def reset_global_rank(self): ...
```

### StreamingWebDataset().set_drop_last

[Show source in dataset.py:139](../streaming_wds/dataset.py#L139)

#### Signature

```python
def set_drop_last(self, drop_last: bool): ...
```

### StreamingWebDataset().set_shuffle

[Show source in dataset.py:136](../streaming_wds/dataset.py#L136)

#### Signature

```python
def set_shuffle(self, shuffle: bool): ...
```

### StreamingWebDataset().state_dict

[Show source in dataset.py:120](../streaming_wds/dataset.py#L120)

#### Signature

```python
def state_dict(self): ...
```