from dataclasses import dataclass
from typing import List
from typing import Optional

from objsonl.model import Body
from objsonl.model import Line
from objsonl.model import Message
from objsonl.model import SystemMessage

__ALL__ = [
    "JsonlBuilder",
]


@dataclass(frozen=True)
class JsonlBuilder:
    url: str
    model: str
    max_tokens: int
    system_message: Optional[str] = None

    def build(self, custom_id: str, messages: List[Message]) -> Line:
        sys = [SystemMessage(self.system_message)] if self.system_message else []

        return Line(
            custom_id=custom_id,
            method="POST",
            url=self.url,
            body=Body(
                model=self.model,
                messages=sys + messages,
                max_tokens=self.max_tokens,
            )
        )
