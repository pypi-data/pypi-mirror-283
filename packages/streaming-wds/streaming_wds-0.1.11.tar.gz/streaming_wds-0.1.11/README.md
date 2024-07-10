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
    prefetch=2,
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

- `remote`: The S3 URI of your dataset
- `split`: The dataset split (e.g., "train", "val", "test")
- `profile`: The AWS profile to use for authentication
- `buffer_size`: The size of the buffer for each worker
- `shuffle`: Whether to shuffle the data
- `max_workers`: Maximum number of worker threads for download and extraction
- `schema`: A dictionary defining the decoding method for each data field
- `cache_limit_bytes`: The maximum size of the file cache in bytes. This should be fairly large to prevent frequent cache evictions.
- `process_sample`: Implement this function to customize the processing of each sample (for example: torchvision transforms)


## Contributing
Contributions to streaming-wds are welcome! Please feel free to submit a Pull Request.

## License
MIT License
