from logging import Logger, getLogger, DEBUG
from unittest import TestCase

import pandas as pd

from objsonl.builder import JsonlBuilder
from objsonl.model.input import UserMessageWithImage


class TestJsonlBuilder(TestCase):
    logger: Logger = getLogger(__name__)
    logger.setLevel(DEBUG)
    builder: JsonlBuilder = JsonlBuilder(
        url="/chat/completions",
        model="gpt-4o",
        max_tokens=8192,
        system_message="You are the assistant who is talking to the user.",
    )

    def test_build(self):
        try:
            line = self.builder.build(
                custom_id="custom_id",
                messages=[
                    UserMessageWithImage.of(
                        text="What's in the image?",
                        image_url="https://example.com/image.jpg",
                    ),
                ]
            )
            self.logger.debug(line.as_json())

        except Exception as e:
            self.fail(e)

    def test_build_pandas(self):
        df: pd.DataFrame = pd.DataFrame(
            [
                {"key": "id1", "text": "Hello, how are you?", "img": "https://example.com/image1.jpg"},
                {"key": "id2", "text": "I'm good, how about you?", "img": "https://example.com/image2.jpg"},
                {"key": "id3", "text": "What's in the image?", "img": "https://example.com/image3.jpg"},
            ]
        )

        try:
            batch = self.builder.build_pandas(
                data=df,
                custom_id="key",
                message="text",
                image_url="img",
            )
            for line in batch.lines:
                self.logger.debug(line.as_json())

        except Exception as e:
            self.fail(e)
