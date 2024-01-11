import unittest
import tests.base as base
from pytgpt.opengpt import OPENGPT


class TestLeo(base.llmBase):
    def setUp(self):
        self.bot = OPENGPT()
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
