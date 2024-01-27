import unittest
import tests.base as base
from pytgpt.fakeopen import FAKEOPEN


class TestBard(base.llmBase):
    def setUp(self):
        self.bot = FAKEOPEN()
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
