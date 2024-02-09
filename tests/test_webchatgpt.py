import unittest
import tests.base as base
from os import getenv
from pytgpt.webchatgpt import WEBCHATGPT


class TestWebchatgpt(base.llmBase):
    def setUp(self):
        self.bot = WEBCHATGPT(getenv("openai_cookie_file"))
        self.prompt = base.prompt


if __name__ == "__main__":
    unittest.main()
