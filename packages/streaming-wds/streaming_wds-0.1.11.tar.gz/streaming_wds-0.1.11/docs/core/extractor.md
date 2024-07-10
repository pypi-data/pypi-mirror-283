# Extractor

[Streaming-wds Index](../README.md#streaming-wds-index) / [Core](./index.md#core) / Extractor

> Auto-generated documentation for [core.extractor](../../streaming_wds/core/extractor.py) module.

- [Extractor](#extractor)
  - [ShardExtractor](#shardextractor)
    - [ShardExtractor().extract_shard](#shardextractor()extract_shard)
    - [ShardExtractor().run](#shardextractor()run)

## ShardExtractor

[Show source in extractor.py:14](../../streaming_wds/core/extractor.py#L14)

A class for extracting shards and processing their contents.

This class handles the extraction of shards from a local cache, processes their
contents, and puts the extracted samples into an output queue.

#### Attributes

- `input_queue` *Queue* - Queue for incoming shard extraction requests.
- `output_queue` *Queue* - Queue for outputting extracted samples.
- `stop_event` *threading.Event* - Event to signal stopping of the extraction process.
- `buffer_size` *int* - Maximum buffer size for memory management.
- `cache` *LocalShardLRUCache* - Local cache for storing and retrieving shards.
- `input_finish_event` *threading.Event* - Event to signal completion of input.
- `output_finish_event` *threading.Event* - Event to signal completion of output.

#### Signature

```python
class ShardExtractor:
    def __init__(
        self,
        input_queue: Queue,
        output_queue: Queue,
        stop_event: threading.Event,
        input_finish_event: threading.Event,
        output_finish_event: threading.Event,
        cache: LocalShardLRUCache,
        buffer_size: int = 2 << 30,
    ): ...
```

### ShardExtractor().extract_shard

[Show source in extractor.py:63](../../streaming_wds/core/extractor.py#L63)

Extract and process a single shard.

This method extracts the contents of a shard, processes its files, and yields
the aggregated data for each sample in the shard.

#### Arguments

- `shard_idx` *int* - The index of the shard.
- `shard_key` *str* - The key of the shard in the cache.
- `rank` *int* - The rank of the worker processing this shard.

#### Yields

- `dict` - A dictionary containing the aggregated data for each sample in the shard.

#### Raises

- `Exception` - If the shard is not found in the cache.

#### Signature

```python
def extract_shard(self, shard_idx: int, shard_key: str, rank: int): ...
```

### ShardExtractor().run

[Show source in extractor.py:130](../../streaming_wds/core/extractor.py#L130)

Run the shard extraction process.

This method continuously extracts shards from the input queue, processes them,
and puts the extracted samples into the output queue until the stop event is set.

#### Arguments

- `rank` *int* - The rank of the worker running this extraction process.

#### Signature

```python
def run(self, rank: int): ...
```