from pytgpt.phind import AsyncPHIND
from pytgpt.yepchat import AsyncYEPCHAT
from pytgpt.opengpt import AsyncOPENGPT
from pytgpt.openai import AsyncOPENAI
from pytgpt.koboldai import AsyncKOBOLDAI
from pytgpt.groq import AsyncGROQ
from pytgpt.blackboxai import AsyncBLACKBOXAI
from pytgpt.novita import AsyncNOVITA
from pytgpt.gpt4free import AsyncGPT4FREE

mapper: dict[str, object] = {
    "phind": AsyncPHIND,
    "opengpt": AsyncOPENGPT,
    "koboldai": AsyncKOBOLDAI,
    "blackboxai": AsyncBLACKBOXAI,
    "gpt4free": AsyncGPT4FREE,
    "yepchat": AsyncYEPCHAT,
    "groq": AsyncGROQ,
    "openai": AsyncOPENAI,
    "novita": AsyncNOVITA,
}

tgpt_mapper: dict[str, object] = {
    "phind": AsyncPHIND,
    "opengpt": AsyncOPENGPT,
    "koboldai": AsyncKOBOLDAI,
    "blackboxai": AsyncBLACKBOXAI,
    "yepchat": AsyncYEPCHAT,
}
