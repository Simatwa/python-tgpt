import unittest
import tests.base as base
from os import getenv
from pytgpt.deepseek import DEEPSEEK
from pytgpt.deepseek import AsyncDEEPSEEK

API_KEY = getenv("DEEPSEEK_API_KEY")


class TestDeepseek(base.llmBase):
    def setUp(self):
        self.bot = DEEPSEEK(API_KEY)
        self.prompt = base.prompt


class TestAsyncDeepSeek(base.AsyncProviderBase):

    def setUp(self):
        self.bot = AsyncDEEPSEEK(API_KEY)
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
