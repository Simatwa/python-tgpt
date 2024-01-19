from .utils import appdir

__version__ = "0.3.1"
__author__ = "Smartwa"
__repo__ = "https://github.com/Simatwa/python-tgpt"

gpt4free_providers = [
    "AItianhuSpace",
    "AiChatOnline",
    "Aura",
    "Bard",
    "Bing",
    "ChatBase",
    "ChatForAi",
    "Chatgpt4Online",
    "ChatgptAi",
    "ChatgptDemo",
    "ChatgptNext",
    "Chatxyz",
    "DeepInfra",
    "FakeGpt",
    "FreeChatgpt",
    "GPTalk",
    "GeekGpt",
    "GeminiProChat",
    "Gpt6",
    "GptChatly",
    "GptForLove",
    "GptGo",
    "GptTalkRu",
    "Hashnode",
    "HuggingChat",
    "Koala",
    "Liaobots",
    "Llama2",
    "MyShell",
    "OnlineGpt",
    "OpenaiChat",
    "PerplexityAi",
    "Phind",
    "Pi",
    "Poe",
    "Raycast",
    "TalkAi",
    "Theb",
    "ThebApi",
    "You",
    "Yqcloud",
]
available_providers = ["leo", "openai", "fakeopen", "opengpt", "koboldai", "bard"] + gpt4free_providers

__all__ = [
    "appdir",
    "imager",
] + available_providers
