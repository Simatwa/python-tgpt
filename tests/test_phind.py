import unittest
import tests.base as base
from pytgpt.phind import PHIND


class TestPhind(base.llmBase):
    def setUp(self):
        self.bot = PHIND()
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
