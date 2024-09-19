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
        model="gpt-4o-batch",
        max_tokens=4096,
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
                {"key": "id1", "text": "What's in the image?", "img": "https://placehold.co/600x400/000000/FF0000/png"},
                {"key": "id2", "text": "What's in the image?", "img": "https://placehold.co/600x400/000000/00FF00/png"},
                {"key": "id3", "text": "What's in the image?", "img": "https://placehold.co/600x400/000000/0000FF/png"},
            ]
        )

        try:
            batch = self.builder.build_pandas(
                data=df,
                custom_id="key",
                message="text",
                image_url="img",
            )
            batch.save("input.jsonl")
            for line in batch.lines:
                self.logger.debug(line.as_json())

        except Exception as e:
            self.fail(e)
