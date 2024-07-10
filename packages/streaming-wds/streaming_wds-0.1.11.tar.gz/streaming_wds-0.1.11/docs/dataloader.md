# Dataloader

[Streaming-wds Index](./README.md#streaming-wds-index) / Dataloader

> Auto-generated documentation for [dataloader](../streaming_wds/dataloader.py) module.

- [Dataloader](#dataloader)
  - [StreamingDataLoader](#streamingdataloader)
    - [StreamingDataLoader().load_state_dict](#streamingdataloader()load_state_dict)
    - [StreamingDataLoader().state_dict](#streamingdataloader()state_dict)
  - [patch_collate_fn](#patch_collate_fn)

## StreamingDataLoader

[Show source in dataloader.py:34](../streaming_wds/dataloader.py#L34)

#### Signature

```python
class StreamingDataLoader(DataLoader):
    def __init__(
        self,
        dataset: StreamingWebDataset,
        batch_size: int = 1,
        num_workers: int = 0,
        prefetch_factor: Optional[int] = None,
        shuffle: Optional[bool] = None,
        drop_last: Optional[bool] = False,
        collate_fn: Optional[Callable] = None,
        *args: Any,
        **kwargs: Any
    ) -> None: ...
```

#### See also

- [StreamingWebDataset](./dataset.md#streamingwebdataset)

### StreamingDataLoader().load_state_dict

[Show source in dataloader.py:105](../streaming_wds/dataloader.py#L105)

#### Signature

```python
def load_state_dict(self, obj: Dict[str, Any]) -> None: ...
```

### StreamingDataLoader().state_dict

[Show source in dataloader.py:95](../streaming_wds/dataloader.py#L95)

#### Signature

```python
def state_dict(self) -> Dict[str, Any]: ...
```



## patch_collate_fn

[Show source in dataloader.py:12](../streaming_wds/dataloader.py#L12)

#### Signature

```python
def patch_collate_fn(collate_fn: Callable) -> Callable: ...
```