from pytgpt.openai import AsyncOPENAI, OPENAI

model = "deepseek-chat"
"""Default model"""

available_models = ("deepseek-reasoner", model)


class DEEPSEEK(OPENAI):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("model", model)
        super().__init__(*args, **kwargs)
        self.chat_endpoint = "https://api.deepseek.com/chat/completions"


class AsyncDEEPSEEK(AsyncOPENAI):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("model", model)
        super().__init__(*args, **kwargs)
        self.chat_endpoint = "https://api.deepseek.com/chat/completions"
