from pytgpt.phind import PHIND
from pytgpt.koboldai import KOBOLDAI
from pytgpt.blackboxai import BLACKBOXAI
from pytgpt.ai4chat import AI4CHAT
from pytgpt.gpt4free import GPT4FREE
from pytgpt.auto import AUTO


tgpt_mapper: dict[str, object] = {
    "phind": PHIND,
    "koboldai": KOBOLDAI,
    "blackboxai": BLACKBOXAI,
    "ai4chat": AI4CHAT,
    "auto": AUTO,
    "gpt4free": GPT4FREE,
}
