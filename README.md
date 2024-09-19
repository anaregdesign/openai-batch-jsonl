# openai-batch-jsonl

This is a Jsonl file building tool for OpanAI's Batch Endpoint API.

[OpenAI Batch Endpoint](https://platform.openai.com/docs/guides/batch/overview) handles data in line-delimited JSON
format (jsonl).
This tool helps to handle jsonl file.

# Installation

## add to existing project

```bash
poetry add git+ssh://git@github.com:anaregdesign/openai-batch-jsonl.git
```

## Install to local environment

```bash
poetry install git+ssh://git@github.com:anaregdesign/openai-batch-jsonl.git
```

# Usage

```python
import pandas as pd
from objsonl import JsonlBuilder

# Example data
df: pd.DataFrame = pd.DataFrame(
    [
        {"key": "id1", "text": "What's in the image?", "img": "https://placehold.co/600x400/000000/FF0000/png"},
        {"key": "id2", "text": "What's in the image?", "img": "https://placehold.co/600x400/000000/00FF00/png"},
        {"key": "id3", "text": "What's in the image?", "img": "https://placehold.co/600x400/000000/0000FF/png"},
    ]
)
builder: JsonlBuilder = JsonlBuilder(
    url="/chat/completions",  # OpenAI's endpoint
    model="gpt-4o-batch",  # model name or deployment name
    max_tokens=4096,  # Maximum number of tokens to generate
    system_message="You are the assistant who is describing input images",  # Common message for all prompts
)

batch = builder.build_pandas(
    data=df,
    custom_id="key",  # Column name for custom_id
    message="text",  # Column name for message
    image_url="img",  # Column name for image_url
)
batch.save("input.jsonl")
```

then we can use the generated jsonl file as input for OpenAI's Batch Endpoint API.

```json lines
{"custom_id": "id1", "method": "POST", "url": "/chat/completions", "body": {"model": "gpt-4o-batch", "messages": [{"content": "You are the assistant who is talking to the user.", "role": "system"}, {"content": [{"type": "text", "text": "What's in the image?"}, {"type": "image_url", "image_url": {"url": "https://placehold.co/600x400/000000/FF0000/png", "detail": "auto"}}], "role": "user"}], "max_tokens": 4096}}
{"custom_id": "id2", "method": "POST", "url": "/chat/completions", "body": {"model": "gpt-4o-batch", "messages": [{"content": "You are the assistant who is talking to the user.", "role": "system"}, {"content": [{"type": "text", "text": "What's in the image?"}, {"type": "image_url", "image_url": {"url": "https://placehold.co/600x400/000000/00FF00/png", "detail": "auto"}}], "role": "user"}], "max_tokens": 4096}}
{"custom_id": "id3", "method": "POST", "url": "/chat/completions", "body": {"model": "gpt-4o-batch", "messages": [{"content": "You are the assistant who is talking to the user.", "role": "system"}, {"content": [{"type": "text", "text": "What's in the image?"}, {"type": "image_url", "image_url": {"url": "https://placehold.co/600x400/000000/0000FF/png", "detail": "auto"}}], "role": "user"}], "max_tokens": 4096}}
```

# Links

* https://python-poetry.org/
