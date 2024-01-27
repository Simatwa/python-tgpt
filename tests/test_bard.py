import unittest
import tests.base as base
from os import getenv
from pytgpt.bard import BARD


class TestBard(base.llmBase):
    def setUp(self):
        self.bot = BARD(getenv("bard_cookie_file"))
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
