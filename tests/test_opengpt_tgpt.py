import unittest
import tests.base as base
from pytgpt.opengpt import OPENGPT
from pytgpt.opengpt import AsyncOPENGPT


class TestOpengpt(base.llmBase):
    def setUp(self):
        self.bot = OPENGPT()
        self.prompt = base.prompt


class TestAsyncOpenai(base.AsyncProviderBase):

    def setUp(self):
        self.bot = AsyncOPENGPT()
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
