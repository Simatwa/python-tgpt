import unittest
import tests.base as base
from pytgpt.leo import LEO


class TestLeo(base.llmBase):
    def setUp(self):
        self.bot = LEO()
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
