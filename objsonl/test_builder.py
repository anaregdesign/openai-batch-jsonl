from logging import Logger, getLogger, DEBUG
from unittest import TestCase

from objsonl.builder import JsonlBuilder
from objsonl.model import UserMessageWithImage


class TestJsonlBuilder(TestCase):
    logger: Logger = getLogger(__name__)
    logger.setLevel(DEBUG)

    def test_build(self):
        builder: JsonlBuilder = JsonlBuilder(
            url="/chat/completions",
            model="gpt-4o",
            max_tokens=8192,
            system_message="You are the assistant who is talking to the user.",
        )

        line = builder.build(
            custom_id="custom_id",
            messages=[
                UserMessageWithImage.of(
                    text="What's in the image?",
                    image_url="https://example.com/image.jpg",
                ),
            ]
        )
        self.logger.debug(line.as_json())
