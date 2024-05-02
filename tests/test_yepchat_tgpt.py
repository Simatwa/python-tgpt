import unittest
import tests.base as base
from pytgpt.yepchat import YEPCHAT
from pytgpt.yepchat import AsyncYEPCHAT


class TestYepchat(base.llmBase):
    def setUp(self):
        self.bot = YEPCHAT()
        self.prompt = base.prompt


class TestAsyncYepchat(base.AsyncProviderBase):

    def setUp(self):
        self.bot = AsyncYEPCHAT()
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
