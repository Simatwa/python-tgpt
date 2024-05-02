import unittest
import tests.base as base
from pytgpt.llama2 import LLAMA2
from pytgpt.llama2 import AsyncLLAMA2


class TestLlama2(base.llmBase):
    def setUp(self):
        self.bot = LLAMA2()
        self.prompt = base.prompt


class TestAsyncLlama2(base.AsyncProviderBase):

    def setUp(self):
        self.bot = AsyncLLAMA2()
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
