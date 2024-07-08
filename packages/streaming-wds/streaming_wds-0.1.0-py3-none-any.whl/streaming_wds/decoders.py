import io
import pickle
from functools import partial
from typing import Any, Callable, Literal

import numpy as np
import PIL
import PIL.Image
import torch


def decode_text(value: bytes) -> str:
    return value.decode("utf-8")


def decode_jpeg(
    value: bytes, format: Literal["np"] | Literal["PIL"] = "np"
) -> PIL.Image.Image | np.ndarray:
    import io

    import numpy as np
    import PIL.Image

    if format == "PIL":
        return PIL.Image.open(io.BytesIO(value))

    return np.asarray(PIL.Image.open(io.BytesIO(value)))


def decode_json(value: bytes) -> dict[str, Any]:
    import json

    return json.loads(value)


def decode_numpy(value: bytes) -> np.ndarray:
    return np.load(io.BytesIO(value))


def decode_msgpack(value: bytes) -> Any:
    try:
        import msgpack
    except ImportError:
        raise ImportError("msgpack is not installed. Please install it using 'pip install msgpack'.")

    return msgpack.unpackb(value, raw=False)


def decode_torch(value: bytes) -> Any:
    import io


    return torch.load(io.BytesIO(value))


def decode_pickle(value: bytes) -> Any:
    return pickle.loads(value)


def mp4_decoder(value: bytes) -> bytes:
    return value


def no_decoder(value: bytes) -> bytes:
    return value


def select_decoder(f: str) -> Callable[[bytes], Any]:
    if f == "txt":
        return decode_text
    if f == "jpg":
        return decode_jpeg
    if f == "PIL":
        return partial(decode_jpeg, format="PIL")
    if f == "json":
        return decode_json
    if f == "npy":
        return decode_numpy
    if f == "msgpack":
        return decode_msgpack
    if f == "torch":
        return decode_torch
    if f == "pickle":
        return decode_pickle
    if f == "mp4":
        return mp4_decoder
    if f == "bytes":
        return no_decoder
    raise ValueError(f"Unknown format: {f}")