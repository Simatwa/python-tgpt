import unittest
import tests.base as base
from pytgpt.auto import AUTO
from pytgpt.auto import AsyncAUTO


class TestAuto(base.llmBase):
    def setUp(self):
        self.bot = AUTO()
        self.prompt = base.prompt


class TestAsyncAuto(base.AsyncProviderBase):

    def setUp(self):
        self.bot = AsyncAUTO()
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
