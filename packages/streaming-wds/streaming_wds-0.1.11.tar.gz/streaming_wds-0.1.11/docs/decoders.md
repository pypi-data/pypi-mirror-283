# Decoders

[Streaming-wds Index](./README.md#streaming-wds-index) / Decoders

> Auto-generated documentation for [decoders](../streaming_wds/decoders.py) module.

- [Decoders](#decoders)
  - [decode_jpeg](#decode_jpeg)
  - [decode_json](#decode_json)
  - [decode_msgpack](#decode_msgpack)
  - [decode_numpy](#decode_numpy)
  - [decode_pickle](#decode_pickle)
  - [decode_text](#decode_text)
  - [decode_torch](#decode_torch)
  - [mp4_decoder](#mp4_decoder)
  - [no_decoder](#no_decoder)
  - [register_decoder](#register_decoder)
  - [select_decoder](#select_decoder)

## decode_jpeg

[Show source in decoders.py:18](../streaming_wds/decoders.py#L18)

#### Signature

```python
def decode_jpeg(
    value: bytes, format: Literal["np"] | Literal["PIL"] = "np"
) -> PIL.Image.Image | np.ndarray: ...
```



## decode_json

[Show source in decoders.py:32](../streaming_wds/decoders.py#L32)

#### Signature

```python
def decode_json(value: bytes) -> dict[str, Any]: ...
```



## decode_msgpack

[Show source in decoders.py:42](../streaming_wds/decoders.py#L42)

#### Signature

```python
def decode_msgpack(value: bytes) -> Any: ...
```



## decode_numpy

[Show source in decoders.py:38](../streaming_wds/decoders.py#L38)

#### Signature

```python
def decode_numpy(value: bytes) -> np.ndarray: ...
```



## decode_pickle

[Show source in decoders.py:59](../streaming_wds/decoders.py#L59)

#### Signature

```python
def decode_pickle(value: bytes) -> Any: ...
```



## decode_text

[Show source in decoders.py:14](../streaming_wds/decoders.py#L14)

#### Signature

```python
def decode_text(value: bytes) -> str: ...
```



## decode_torch

[Show source in decoders.py:53](../streaming_wds/decoders.py#L53)

#### Signature

```python
def decode_torch(value: bytes) -> Any: ...
```



## mp4_decoder

[Show source in decoders.py:63](../streaming_wds/decoders.py#L63)

#### Signature

```python
def mp4_decoder(value: bytes) -> bytes: ...
```



## no_decoder

[Show source in decoders.py:67](../streaming_wds/decoders.py#L67)

#### Signature

```python
def no_decoder(value: bytes) -> bytes: ...
```



## register_decoder

[Show source in decoders.py:85](../streaming_wds/decoders.py#L85)

Register a new decoder for a given format.

#### Arguments

- `format` *str* - The format identifier for the decoder.
decoder (Callable[[bytes], Any]): The decoder function.

#### Signature

```python
def register_decoder(format: str, decoder: Callable[[bytes], Any]) -> None: ...
```



## select_decoder

[Show source in decoders.py:96](../streaming_wds/decoders.py#L96)

#### Signature

```python
def select_decoder(f: str) -> Callable[[bytes], Any]: ...
```