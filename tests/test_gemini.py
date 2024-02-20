import unittest
import tests.base as base
from os import getenv
from pytgpt.gemini import GEMINI


class TestBard(base.llmBase):
    def setUp(self):
        self.bot = GEMINI(getenv("bard_cookie_file"))
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
