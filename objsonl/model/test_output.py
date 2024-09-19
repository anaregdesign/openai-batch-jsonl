from logging import Logger, getLogger, DEBUG
from unittest import TestCase

from objsonl.model.output import BatchOutput


class TestBatchOutput(TestCase):
    logger: Logger = getLogger(__name__)
    logger.setLevel(DEBUG)

    def test_load(self):
        try:
            output = BatchOutput.load("../../sample/output.jsonl")
            self.logger.debug(output)

        except Exception as e:
            self.fail(e)
