from dataclasses import dataclass
from typing import List
from typing import Optional

import pandas as pd

from objsonl.model.input import Batch
from objsonl.model.input import Body
from objsonl.model.input import Detail
from objsonl.model.input import Line
from objsonl.model.input import Message
from objsonl.model.input import SystemMessage
from objsonl.model.input import UserMessage
from objsonl.model.input import UserMessageWithImage

__ALL__ = [
    "JsonlBuilder",
]


@dataclass(frozen=True)
class JsonlBuilder:
    url: str
    model: str
    max_tokens: int = None
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

    def build_pandas(self, data: pd.DataFrame, custom_id: str, message: str, image_url: str = None) -> Batch:
        lines: List[Line] = []
        for i, row in data.fillna("").iterrows():
            m: Message = UserMessage(
                content=row[message]
            ) if image_url is None else UserMessageWithImage.of(
                text=row[message],
                image_url=row[image_url],
                detail=Detail.AUTO
            )
            line: Line = self.build(custom_id=row[custom_id], messages=[m])
            lines.append(line)

        return Batch(lines)
