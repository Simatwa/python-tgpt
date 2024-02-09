import unittest
import tests.base as base
from pytgpt.gpt4all import GPT4ALL
from os import getenv


class TestGpt4all(base.llmBase):
    def setUp(self):
        self.bot = GPT4ALL(getenv("model_path"))
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
