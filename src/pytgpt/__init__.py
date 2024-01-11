from .utils import appdir

__version__ = "0.2.2"
__author__ = "Smartwa"
__repo__ = "https://github.com/Simatwa/python-tgpt"

available_providers = ["leo", "openai", "fakeopen", "opengpt", "koboldai"]

__all__ = [
    "appdir",
    "imager",
] + available_providers
