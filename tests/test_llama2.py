import unittest
import tests.base as base
from pytgpt.llama2 import LLAMA2


class TestLlama2(base.llmBase):
    def setUp(self):
        self.bot = LLAMA2()
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
