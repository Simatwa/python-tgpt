import unittest
import tests.base as base
from pytgpt.gpt4free import GPT4FREE
from pytgpt.gpt4free import AsyncGPT4FREE


class TestGpt4free(base.llmBase):
    def setUp(self):
        self.bot = GPT4FREE()
        self.prompt = base.prompt


class TestAsyncGpt4free(base.AsyncProviderBase):

    def setUp(self):
        self.bot = AsyncGPT4FREE()
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
