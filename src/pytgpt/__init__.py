import g4f
from importlib import metadata
import logging

try:
    __version__ = metadata.version("python-tgpt")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"

__author__ = "Smartwa"
__repo__ = "https://github.com/Simatwa/python-tgpt"

tgpt_providers = [
    "auto",
    "openai",
    "koboldai",
    "phind",
    "blackboxai",
    "gpt4all",
    "g4fauto",
    "poe",
    "groq",
    "perplexity",
    "novita",
    "ai4chat",
]

gpt4free_providers = [
    provider.__name__ for provider in g4f.Provider.__providers__  # if provider.working
]

available_providers = tgpt_providers + gpt4free_providers

__all__ = [
    "appdir",
    "imager",
] + available_providers

logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("websocket").setLevel(logging.ERROR)
