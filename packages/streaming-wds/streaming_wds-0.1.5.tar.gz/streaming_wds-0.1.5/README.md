# streaming-wds (Streaming WebDataset)

`streaming-wds` is a Python library that enables efficient streaming of WebDataset-format datasets from boto3-compliant object stores for PyTorch. It's designed to handle large-scale datasets with ease, especially in distributed training contexts.

Note: this was a weekend project and is not yet optimized for production use. Feedback & contributions welcome, especially for performance improvements.

## Features

- Streaming of WebDataset-format data from S3-compatible object stores
- Sharding of data across workers
- Supports mid-epoch resumption when used with `StreamingDataLoader`
- Efficient prefetching and parallel processing of data
- Customizable decoding of dataset elements

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
- `prefetch`: Number of samples to prefetch
- `shuffle`: Whether to shuffle the data
- `max_workers`: Maximum number of worker threads for download and extraction
- `schema`: A dictionary defining the decoding method for each data field

## Mid-Epoch Resumption
When used with `StatefulDataLoader` from `torchdata`, streaming-wds supports mid-epoch resumption. This is particularly useful for long-running training jobs that may be interrupted.

## Contributing
Contributions to streaming-wds are welcome! Please feel free to submit a Pull Request.

## License
MIT License

## Acknowledgements
This project was inspired by the WebDataset format and built to work seamlessly with PyTorch and torchdata.
