import unittest
import tests.base as base
from pytgpt.perplexity import PERPLEXITY


class TestPerplexity(base.llmBase):
    def setUp(self):
        self.bot = PERPLEXITY()
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
