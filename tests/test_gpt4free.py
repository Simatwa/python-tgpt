import unittest
import tests.base as base
from pytgpt.gpt4free import GPT4FREE


class TestGpt4free(base.llmBase):
    def setUp(self):
        self.bot = GPT4FREE()
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
