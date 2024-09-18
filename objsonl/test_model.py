from logging import Logger, getLogger
from unittest import TestCase

from objsonl.model import Line, Body, UserMessage, AssistantMessage, SystemMessage, UserMessageWithImage, Detail

_logger: Logger = getLogger(__name__)

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
    def test_as_dict(self):
        _logger.info(line.as_dict())

    def test_as_json(self):
        _logger.info(line.as_json())
