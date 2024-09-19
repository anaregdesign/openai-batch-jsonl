import json
from abc import ABCMeta
from dataclasses import dataclass, asdict
from enum import Enum
from typing import List, Optional

__ALL__ = [
    "Message",
    "SystemMessage",
    "UserMessage",
    "AssistantMessage",
    "UserMessageWithImage",
    "Detail",
    "ImageURL",
    "Content",
    "Body",
    "Line",
    "Batch",
]


class Message(metaclass=ABCMeta):
    pass


@dataclass(frozen=True)
class SystemMessage(Message):
    content: str
    role: str = "system"


@dataclass(frozen=True)
class UserMessage(Message):
    content: str
    role: str = "user"


@dataclass(frozen=True)
class AssistantMessage(Message):
    content: str
    role: str = "assistant"


class Detail(str, Enum):
    LOW = "low"
    HIGH = "high"
    AUTO = "auto"


@dataclass(frozen=True)
class ImageURL:
    url: str
    detail: Optional[Detail] = None


@dataclass(frozen=True)
class Content:
    type: str
    text: Optional[str]
    image_url: Optional[ImageURL]

    def __post_init__(self):
        if self.text is not None and self.image_url is not None:
            raise ValueError("Either text or image_url must be None")


@dataclass(frozen=True)
class UserMessageWithImage(Message):
    content: List[Content]
    role: str = "user"

    @staticmethod
    def of(text: str, image_url: str, detail: Detail = Detail.AUTO) -> "UserMessageWithImage":
        return UserMessageWithImage(
            [Content("text", text, None), Content("image_url", None, ImageURL(image_url, detail))])


@dataclass(frozen=True)
class Body:
    model: str
    messages: List[Message]
    max_tokens: int


@dataclass(frozen=True)
class InputLine:
    custom_id: str
    method: str
    url: str
    body: Body

    def as_dict(self) -> dict:
        return asdict(self, dict_factory=lambda x: {k: v for k, v in x if v is not None})

    def as_json(self, ensure_ascii: bool = False) -> str:
        return json.dumps(self.as_dict(), ensure_ascii=ensure_ascii)


@dataclass(frozen=True)
class BatchInput:
    lines: List[InputLine]

    def save(self, path: str, ensure_ascii: bool = False):
        with open(path, "w") as f:
            for line in self.lines:
                f.write(line.as_json(ensure_ascii=ensure_ascii) + "\n")
