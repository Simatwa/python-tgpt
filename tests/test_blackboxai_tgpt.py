import unittest
import tests.base as base
from pytgpt.blackboxai import BLACKBOXAI
from pytgpt.blackboxai import AsyncBLACKBOXAI


class TestBlackboxai(base.llmBase):
    def setUp(self):
        self.bot = BLACKBOXAI()
        self.prompt = base.prompt


class TestAsyncBlackboxai(base.AsyncProviderBase):

    def setUp(self):
        self.bot = AsyncBLACKBOXAI()
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
