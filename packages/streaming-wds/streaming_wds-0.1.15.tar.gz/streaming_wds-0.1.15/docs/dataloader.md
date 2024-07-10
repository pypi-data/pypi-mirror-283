# Dataloader

[Streaming-wds Index](./README.md#streaming-wds-index) / Dataloader

> Auto-generated documentation for [dataloader](../streaming_wds/dataloader.py) module.

- [Dataloader](#dataloader)
  - [StreamingDataLoader](#streamingdataloader)
    - [StreamingDataLoader().load_state_dict](#streamingdataloader()load_state_dict)
    - [StreamingDataLoader().state_dict](#streamingdataloader()state_dict)
  - [patch_collate_fn](#patch_collate_fn)

## StreamingDataLoader

[Show source in dataloader.py:88](../streaming_wds/dataloader.py#L88)

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

[Show source in dataloader.py:162](../streaming_wds/dataloader.py#L162)

#### Signature

```python
def load_state_dict(self, obj: Dict[str, Any]) -> None: ...
```

### StreamingDataLoader().state_dict

[Show source in dataloader.py:152](../streaming_wds/dataloader.py#L152)

#### Signature

```python
def state_dict(self) -> Dict[str, Any]: ...
```



## patch_collate_fn

[Show source in dataloader.py:15](../streaming_wds/dataloader.py#L15)

Patch a collate function to exclude certain WebDataset-specific keys from collation.

This function takes a collate function and returns a new function that wraps the original.
The new function removes specific keys (__wds_global_rank__, __wds_shard_idx__, and
__wds_sample_key__) from the input dictionaries before collation, then adds them back
to the collated output. It also checks that each item in the batch is a dictionary.

#### Arguments

- `collate_fn` *Callable* - The original collate function to be patched. This function
                       should take a list of dictionaries and return a single
                       dictionary with collated values.

#### Returns

- `Callable` - A new collate function that wraps the original, excluding specific keys
          from collation and re-adding them to the output.

#### Raises

- `TypeError` - If any item in the input batch is not a dictionary.

#### Examples

```python
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
```

#### Signature

```python
def patch_collate_fn(collate_fn: Callable) -> Callable: ...
```
