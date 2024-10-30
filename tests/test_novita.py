import unittest
import tests.base as base
from os import getenv
from pytgpt.novita import NOVITA
from pytgpt.novita import AsyncNOVITA

API_KEY = getenv("NOVITA_API_KEY")


class TestOpenai(base.llmBase):
    def setUp(self):
        self.bot = NOVITA(API_KEY)
        self.prompt = base.prompt


class TestAsyncOpenai(base.AsyncProviderBase):

    def setUp(self):
        self.bot = AsyncNOVITA(API_KEY)
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
