import unittest
import tests.base as base
from pytgpt.koboldai import KOBOLDAI


class TestLeo(base.llmBase):
    def setUp(self):
        self.bot = KOBOLDAI()
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
