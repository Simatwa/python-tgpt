import unittest
import tests.base as base
from pytgpt.leo import LEO
from pytgpt.leo import AsyncLEO


class TestLeo(base.llmBase):
    def setUp(self):
        self.bot = LEO()
        self.prompt = base.prompt


class TestAsyncLeo(base.AsyncProviderBase):

    def setUp(self):
        self.bot = AsyncLEO()
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
