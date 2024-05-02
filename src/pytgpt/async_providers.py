from pytgpt.phind import AsyncPHIND
from pytgpt.yepchat import AsyncYEPCHAT
from pytgpt.opengpt import AsyncOPENGPT
from pytgpt.openai import AsyncOPENAI
from pytgpt.llama2 import AsyncLLAMA2
from pytgpt.leo import AsyncLEO
from pytgpt.koboldai import AsyncKOBOLDAI
from pytgpt.groq import AsyncGROQ

mapper: dict[str, object] = {
    "phind": AsyncPHIND,
    "yepchat": AsyncYEPCHAT,
    "opengpt": AsyncOPENGPT,
    "openai": AsyncOPENAI,
    "llama2": AsyncLLAMA2,
    "leo": AsyncLEO,
    "koboldai": AsyncKOBOLDAI,
    "groq": AsyncGROQ,
}

tgpt_mapper: dict[str, object] = {
    "phind": AsyncPHIND,
    "yepchat": AsyncYEPCHAT,
    "opengpt": AsyncOPENGPT,
    "llama2": AsyncLLAMA2,
    "koboldai": AsyncKOBOLDAI,
}
