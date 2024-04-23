import unittest
import tests.base as base
from pytgpt.auto import AUTO


class TestAuto(base.llmBase):
    def setUp(self):
        self.bot = AUTO()
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
