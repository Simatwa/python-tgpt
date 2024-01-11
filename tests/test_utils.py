import unittest
import os
from pytgpt.utils import Optimizers
from pytgpt.utils import Conversation
from pytgpt.utils import AwesomePrompts


class TestOptimizers(unittest.TestCase):
    def setUp(self):
        self.optimizer = Optimizers
        self.prompt = "This is a prompt example"

    def test_code_optimization(self):
        """Test code prompt optimization"""
        prompt = self.optimizer.code(self.prompt)

        self.assertIn(self.prompt, prompt)

    def test_shell_command_optimization(self):
        """Test shell-command prompt optimization"""

        prompt = self.optimizer.shell_command(self.prompt)
        self.assertIn(self.prompt, prompt)


class TestConversation(unittest.TestCase):
    def setUp(self):
        self.intro = "This is a test intro prompt"
        Conversation.intro = self.intro
        self.conversation = Conversation()
        self.user_prompt = "Hello there"
        self.llm_response = "Hello how may I help you?"
        self.filepath = "test-path.txt"

    def get_file_content(self) -> str:
        if not os.path.exists(self.filepath):
            return ""
        with open(self.filepath) as fh:
            return fh.read()

    def test_intro_in_prompt(self):
        """Test intro presence in chat_history"""
        self.assertEqual(self.intro, self.conversation.chat_history)

    def test_history_based_prompt_generation(self):
        """Test combination of chat_history and new user prompt"""
        new_prompt = self.conversation.gen_complete_prompt(self.user_prompt)
        self.assertIn(self.user_prompt, new_prompt)

    def test_update_chat_history(self):
        """Test success of chat history updation"""
        self.conversation.update_chat_history(self.user_prompt, self.llm_response)

    def test_saving_chat_history_in_file(self):
        """Test saving chat history in .txt file"""
        self.conversation = Conversation(filepath=self.filepath)
        self.assertTrue(os.path.exists(self.filepath))
        before_history_text = self.get_file_content()
        self.conversation.update_chat_history(self.user_prompt, self.llm_response)
        after_history_text = self.get_file_content()
        self.assertNotEqual(before_history_text, after_history_text)

    def test_prompt_offset_after_long_chat(self):
        """Test truncating lengthy chats"""
        self.conversation.history_offset = 30
        for _ in range(5):
            self.conversation.update_chat_history(self.user_prompt, self.llm_response)
        generated_prompt = self.conversation.gen_complete_prompt(self.user_prompt)
        self.assertEqual(self.conversation.chat_history, generated_prompt)

    def tearDown(self):
        if os.path.exists(self.filepath):
            os.remove(self.filepath)


class TestAwesomePrompt(unittest.TestCase):
    def setUp(self):
        self.awesome = AwesomePrompts()
        self.intro = "This is an intro example"
        self.key = "Excel Sheet"

    def test_all_acts_presence(self):
        """Tests all-acts availability"""
        self.assertIsInstance(self.awesome.all_acts, dict)

    def test_get_act_by_string(self):
        """Tests accessibility of act by str key"""
        self.assertIsNotNone(self.awesome.get_act(self.key, default=None))

    def test_get_act_by_int(self):
        """Test accessibility of act by int"""
        self.assertIsNotNone(self.awesome.get_act(1, default=None))

    def test_get_act_by_string_case_insensitive(self):
        """Test awesome search case-insensitively"""
        self.assertIsNotNone(
            self.awesome.get_act(self.key.lower(), case_insensitive=True)
        )

    # @unittest.expectedFailure
    def test_get_act_by_string_case_sensitive(self):
        """Test awesome search case-sensitively"""
        self.assertIsNotNone(
            self.awesome.get_act(self.key, default=None, case_insensitive=False)
        )

    def test_get_act_by_string_unavailable_key(self):
        """Test get_act raises KeyError"""
        with self.assertRaises(KeyError):
            self.awesome.get_act(
                "Som ranDom sTrInG here", default=None, raise_not_found=True
            )


if __name__ == "__main__":
    unittest.main()
