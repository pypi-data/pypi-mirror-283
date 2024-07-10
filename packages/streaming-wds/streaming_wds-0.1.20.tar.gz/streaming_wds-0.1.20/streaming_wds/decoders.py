import io
import pickle
from functools import partial
from typing import Any, Callable, Dict, Literal

import logging
import numpy as np
import PIL
import PIL.Image
import torch

logger = logging.getLogger(__name__)


def decode_text(value: bytes) -> str:
    return value.decode("utf-8")


def decode_jpeg(
    value: bytes, format: Literal["np"] | Literal["PIL"] = "np"
) -> PIL.Image.Image | np.ndarray:
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
        raise ImportError(
            "msgpack is not installed. Please install it using 'pip install msgpack'."
        )

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


_decoder_registry: Dict[str, Callable[[bytes], Any]] = {
    "txt": decode_text,
    "jpg": decode_jpeg,
    "PIL": partial(decode_jpeg, format="PIL"),
    "json": decode_json,
    "npy": decode_numpy,
    "msgpack": decode_msgpack,
    "torch": decode_torch,
    "pickle": decode_pickle,
    "mp4": mp4_decoder,
    "bytes": no_decoder,
}


def register_decoder(format: str, decoder: Callable[[bytes], Any]) -> None:
    """
    Register a new decoder for a given format.

    Args:
        format (str): The format identifier for the decoder.
        decoder (Callable[[bytes], Any]): The decoder function.
    """
    _decoder_registry[format] = decoder


def select_decoder(f: str) -> Callable[[bytes], Any]:
    try:
        return _decoder_registry[f]
    except KeyError:
        logger.debug(f"No decoder found for format {f}. Returning bytes.")
        return no_decoder(f)
