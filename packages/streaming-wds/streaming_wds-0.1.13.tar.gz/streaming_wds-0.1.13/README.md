# streaming-wds (Streaming WebDataset)

`streaming-wds` is a Python library that enables efficient streaming of WebDataset-format datasets from boto3-compliant object stores for PyTorch. It's designed to handle large-scale datasets with ease, especially in distributed training contexts.


## Features

- Streaming of WebDataset-format data from S3-compatible object stores
- Efficient sharding of data across both torch distributed workers and dataloader multiprocessing workers
- Supports mid-epoch resumption when used with `StreamingDataLoader`
- Blazing fast data loading with local caching and explicit control over memory consumption
- Customizable decoding of dataset elements via `StreamingDataset.process_sample`

## Installation

You can install `streaming-wds` using pip:

```bash
pip install streaming-wds
```

## Quick Start
Here's a basic example of how to use streaming-wds:

```python
from streaming_wds import StreamingWebDataset, StreamingDataLoader

# Create the dataset
dataset = StreamingWebDataset(
    remote="s3://your-bucket/your-dataset",
    split="train",
    profile="your_aws_profile",
    shuffle=True,
    max_workers=4,
    schema={".jpg": "PIL", ".json": "json"}
)

# or use a custom processing function
import torchvision.transforms.v2 as T

class ImageNetWebDataset(StreamingWebDataset):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transforms = T.Compose([
            T.ToImage(),
            T.Resize((64,)),
            T.ToDtype(torch.float32),
            T.Normalize(mean=(128,), std=(128,)),
        ])

    def process_sample(self, sample):
        sample[".jpg"] = self.transforms(sample[".jpg"])
        return sample

# Create a StreamingDataLoader for mid-epoch resumption
dataloader = StreamingDataLoader(dataset, batch_size=32, num_workers=4)

# Iterate through the data
for batch in dataloader:
    # Your training loop here
    pass

# You can save the state for resumption
state_dict = dataloader.state_dict()

# Later, you can resume from this state
dataloader.load_state_dict(state_dict)
```


## Configuration

- `remote` (str): The S3 URI of the dataset.
- `split` (Optional[str]): The dataset split (e.g., "train", "val", "test"). Defaults to None.
- `profile` (str): The AWS profile to use for authentication. Defaults to "default".
- `shuffle` (bool): Whether to shuffle the data. Defaults to False.
- `max_workers` (int): Maximum number of worker threads for download and extraction. Defaults to 2.
- `schema` (Dict[str, str]): A dictionary defining the decoding method for each data field. Defaults to {}.
- `memory_buffer_limit_bytes` (Union[Bytes, int, str]): The maximum size of the memory buffer in bytes per worker. Defaults to "2GB".
- `file_cache_limit_bytes` (Union[Bytes, int, str]): The maximum size of the file cache in bytes per worker. Defaults to "2GB".


## Contributing
Contributions to streaming-wds are welcome! Please feel free to submit a Pull Request.

## License
MIT License
