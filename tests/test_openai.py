import unittest
import tests.base as base
from os import getenv
from pytgpt.openai import OPENAI
from pytgpt.openai import AsyncOPENAI


class TestOpenai(base.llmBase):
    def setUp(self):
        self.bot = OPENAI(getenv("OPENAI_API_KEY"))
        self.prompt = base.prompt


class TestAsyncOpenai(base.AsyncProviderBase):

    def setUp(self):
        self.bot = AsyncOPENAI()
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
