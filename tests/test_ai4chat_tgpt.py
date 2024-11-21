import unittest
import tests.base as base
from pytgpt.ai4chat import AI4CHAT
from pytgpt.ai4chat import AsyncAI4CHAT


class TestPhind(base.llmBase):
    def setUp(self):
        self.bot = AI4CHAT()
        self.prompt = base.prompt


class TestAsyncPhind(base.AsyncProviderBase):

    def setUp(self):
        self.bot = AsyncAI4CHAT()
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
