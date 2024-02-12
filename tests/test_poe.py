import unittest
import tests.base as base
from pytgpt.poe import POE


class TestPoe(base.llmBase):
    def setUp(self):
        self.bot = POE()
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
