# Downloader

[Streaming-wds Index](../README.md#streaming-wds-index) / [Core](./index.md#core) / Downloader

> Auto-generated documentation for [core.downloader](../../streaming_wds/core/downloader.py) module.

- [Downloader](#downloader)
  - [ShardDownloader](#sharddownloader)
    - [ShardDownloader().find_shards](#sharddownloader()find_shards)
    - [ShardDownloader().get_shard](#sharddownloader()get_shard)
    - [ShardDownloader().num_shards](#sharddownloader()num_shards)
    - [ShardDownloader().prefetch_shards](#sharddownloader()prefetch_shards)
    - [ShardDownloader().run](#sharddownloader()run)
  - [count_shards](#count_shards)

## ShardDownloader

[Show source in downloader.py:40](../../streaming_wds/core/downloader.py#L40)

A class for downloading shards from S3 and managing the download process.

This class handles the downloading of shards from S3, caching them locally,
and managing the download queue for multiple workers.

#### Attributes

- `s3` *boto3.client* - The S3 client for interacting with AWS S3.
- `shards` *Optional[List[str]]* - List of shard keys to be downloaded.
- `cache` *LocalShardLRUCache* - Local cache for storing downloaded shards.
- `input_queue` *Queue* - Queue for incoming shard download requests.
- `output_queue` *Queue* - Queue for outputting downloaded shard information.
- `stop_event` *threading.Event* - Event to signal stopping of the download process.
- `finish_event` *threading.Event* - Event to signal completion of downloads.
- `bucket` *str* - The S3 bucket name.
- `key_prefix` *str* - The prefix for S3 keys.

#### Signature

```python
class ShardDownloader:
    def __init__(
        self,
        remote: str,
        session: Session,
        input_queue: Queue,
        output_queue: Queue,
        stop_event: threading.Event,
        finish_event: threading.Event,
        cache: LocalShardLRUCache,
    ): ...
```

### ShardDownloader().find_shards

[Show source in downloader.py:112](../../streaming_wds/core/downloader.py#L112)

Find all shards in the S3 bucket with the given prefix.

#### Returns

- `List[str]` - A list of shard keys.

#### Signature

```python
def find_shards(self): ...
```

### ShardDownloader().get_shard

[Show source in downloader.py:128](../../streaming_wds/core/downloader.py#L128)

Get the shard from the cache if it exists, otherwise download it.

#### Arguments

- `key` *str* - The S3 key of the shard.

#### Returns

- `str` - The local path to the shard file, or None if download failed.

#### Signature

```python
def get_shard(self, key: str) -> str: ...
```

### ShardDownloader().num_shards

[Show source in downloader.py:97](../../streaming_wds/core/downloader.py#L97)

Get the number of shards.

#### Returns

- `int` - The number of shards.

#### Signature

```python
def num_shards(self): ...
```

### ShardDownloader().prefetch_shards

[Show source in downloader.py:162](../../streaming_wds/core/downloader.py#L162)

Prefetch multiple shards in parallel.

#### Arguments

- `keys` *List[str]* - List of S3 keys to prefetch.

#### Signature

```python
def prefetch_shards(self, keys: List[str]): ...
```

### ShardDownloader().run

[Show source in downloader.py:174](../../streaming_wds/core/downloader.py#L174)

Run the shard downloading process for a worker.

#### Arguments

- `worker_info` *WorkerInfo* - Information about the worker.

#### Raises

- `RuntimeError` - If setup() was not called before run().

#### Signature

```python
def run(self, rank, worker_infos: List[WorkerInfo], shuffle: bool = False): ...
```



## count_shards

[Show source in downloader.py:17](../../streaming_wds/core/downloader.py#L17)

Helper function to count the number of shards in a dataset outside of the ShardDownloader.

#### Returns

- `List[str]` - A list of shard keys.

#### Signature

```python
def count_shards(remote: str, session: Session) -> List[str]: ...
```
