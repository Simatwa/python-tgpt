import unittest
import types
import os

prompt = "This is a prompt"


class llmBase(unittest.TestCase):
    def setUp(self):
        """Override this"""
        self.bot = None
        self.prompt = prompt

    def test_ask_non_stream(self):
        """Ask non-stream"""
        resp = self.bot.ask(self.prompt)
        self.assertIsInstance(resp, dict)

    def test_ask_stream(self):
        """Ask stream"""
        resp = self.bot.ask(self.prompt, stream=True)
        self.assertIsInstance(resp, types.GeneratorType)
        for value in resp:
            self.assertIsInstance(value, dict)

    def test_ask_stream_raw(self):
        """Ask stream raw"""
        resp = self.bot.ask(self.prompt, True, True)
        self.assertIsInstance(resp, types.GeneratorType)

        for count, value in enumerate(resp):
            self.assertIsInstance(value, str)

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
