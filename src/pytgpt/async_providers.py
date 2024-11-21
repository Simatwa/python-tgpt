from pytgpt.phind import AsyncPHIND
from pytgpt.openai import AsyncOPENAI
from pytgpt.koboldai import AsyncKOBOLDAI
from pytgpt.groq import AsyncGROQ
from pytgpt.blackboxai import AsyncBLACKBOXAI
from pytgpt.novita import AsyncNOVITA
from pytgpt.ai4chat import AsyncAI4CHAT
from pytgpt.gpt4free import AsyncGPT4FREE

mapper: dict[str, object] = {
    "phind": AsyncPHIND,
    "koboldai": AsyncKOBOLDAI,
    "blackboxai": AsyncBLACKBOXAI,
    "gpt4free": AsyncGPT4FREE,
    "groq": AsyncGROQ,
    "openai": AsyncOPENAI,
    "novita": AsyncNOVITA,
}

tgpt_mapper: dict[str, object] = {
    "phind": AsyncPHIND,
    "koboldai": AsyncKOBOLDAI,
    "blackboxai": AsyncBLACKBOXAI,
    "ai4chat": AsyncAI4CHAT,
}
