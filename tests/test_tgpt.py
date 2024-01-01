import unittest
import types
from tgpt import TGPT


class TestTgpt(unittest.TestCase):
    def setUp(self):
        self.bot = TGPT()
        self.prompt = "Hello there"

    def test_ask_non_stream(self):
        """Ask non-stream"""
        resp = self.bot.ask(self.prompt)
        self.assertIsInstance(resp, dict)
        self.assertIsNotNone(resp.get("completion"))

    def test_ask_stream(self):
        """Ask stream"""
        resp = self.bot.ask(self.prompt, stream=True)
        self.assertIsInstance(resp, types.GeneratorType)
        for value in resp:
            self.assertIsInstance(value, dict)
            self.assertIsNotNone(value.get("completion"))

    def test_ask_stream_raw(self):
        """Ask stream raw"""
        resp = self.bot.ask(self.prompt, True, True)
        self.assertIsInstance(resp, types.GeneratorType)

        for count, value in enumerate(resp):
            self.assertIsInstance(value, str)
            if count == 1:
                self.assertIn("data:", value)
                self.assertTrue(value.strip().startswith("data:"))

    def test_get_message(self):
        """Response retrieval"""
        resp = self.bot.ask(self.prompt)
        self.assertIsInstance(self.bot.get_message(resp), str)

    def test_chat_non_stream(self):
        """Chat non-stream"""
        resp = self.bot.chat(self.prompt)
        self.assertIs(type(resp), str, f"{resp} is not str")

    def test_chat_stream(self):
        """Chat stream"""
        resp = self.bot.chat(self.prompt, stream=True)
        self.assertIsInstance(resp, types.GeneratorType)
        for value in resp:
            self.assertIsInstance(value, str)

    def test_optimizer_usage(self):
        """Code optimization"""
        resp = self.bot.chat(self.prompt, optimizer="code")
        self.assertIsInstance(resp, str)

    def test_last_response(self):
        """Last response availability"""
        self.bot.chat(self.prompt)
        self.assertIsInstance(self.bot.last_response, dict)


if __name__ == "__main__":
    unittest.main()
