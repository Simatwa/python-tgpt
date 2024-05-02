import unittest
import tests.base as base
from pytgpt.koboldai import KOBOLDAI
from pytgpt.koboldai import AsyncKOBOLDAI


class TestKoboldai(base.llmBase):
    def setUp(self):
        self.bot = KOBOLDAI()
        self.prompt = base.prompt


class TestAsyncKoboldai(base.AsyncProviderBase):

    async def setUp(self):
        self.bot = AsyncKOBOLDAI()
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
