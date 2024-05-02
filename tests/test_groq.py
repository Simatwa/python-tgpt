import unittest
import tests.base as base
from os import getenv
from pytgpt.groq import GROQ
from pytgpt.groq import AsyncGROQ


class TestGroq(base.llmBase):
    def setUp(self):
        self.bot = GROQ(getenv("GROQ_API_KEY"))
        self.prompt = base.prompt


class TestAsyncGroq(base.AsyncProviderBase):

    def setUp(self):
        self.bot = AsyncGROQ(getenv("GROQ_API_KEY"))
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
