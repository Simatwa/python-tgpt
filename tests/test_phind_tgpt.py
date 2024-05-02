import unittest
import tests.base as base
from pytgpt.phind import PHIND
from pytgpt.phind import AsyncPHIND


class TestPhind(base.llmBase):
    def setUp(self):
        self.bot = PHIND()
        self.prompt = base.prompt


class TestAsyncPhind(base.AsyncProviderBase):

    def setUp(self):
        self.bot = AsyncPHIND()
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
