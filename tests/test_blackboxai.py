import unittest
import tests.base as base
from pytgpt.blackboxai import BLACKBOXAI


class TestBlackboxai(base.llmBase):
    def setUp(self):
        self.bot = BLACKBOXAI()
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
