import unittest
import tests.base as base
from os import getenv
from pytgpt.openai import OPENAI


class TestOpenai(base.llmBase):
    def setUp(self):
        self.bot = OPENAI(getenv("OPENAI_API_KEY"))
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
