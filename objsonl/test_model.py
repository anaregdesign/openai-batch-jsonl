from logging import Logger, getLogger, DEBUG
from unittest import TestCase

from objsonl.model import AssistantMessage
from objsonl.model import Body
from objsonl.model import Detail
from objsonl.model import Line
from objsonl.model import SystemMessage
from objsonl.model import UserMessage
from objsonl.model import UserMessageWithImage

line: Line = Line(
    custom_id="custom_id",
    method="POST",
    url="/chat/completions",
    body=Body(
        model="gpt-4o",
        messages=[
            SystemMessage("You are the assistant who is talking to the user."),
            UserMessage("Hello, how are you?"),
            AssistantMessage("I'm good, how about you?"),
            UserMessageWithImage.of(
                text="What's in the image?",
                image_url="https://example.com/image.jpg",
                detail=Detail.AUTO,
            ),
        ],
        max_tokens=8192,
    )
)


class TestLine(TestCase):
    logger: Logger = getLogger(__name__)
    logger.setLevel(DEBUG)

    def test_as_dict(self):
        try:
            self.logger.debug(line.as_dict())

        except Exception as e:
            self.fail(e)

    def test_as_json(self):
        try:
            self.logger.debug(line.as_json())

        except Exception as e:
            self.fail(e)
