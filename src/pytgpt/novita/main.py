from pytgpt.openai import OPENAI, AsyncOPENAI
from pytgpt.exceptions import UnsupportedModelError

model = "meta-llama/llama-3.1-8b-instruct"

available_models = [
    "meta-llama/llama-3.1-8b-instruct",
    "meta-llama/llama-3.1-70b-instruct",
    "meta-llama/llama-3.1-405b-instruct",
    "meta-llama/llama-3-8b-instruct",
    "meta-llama/llama-3-70b-instruct",
    "gryphe/mythomax-l2-13b",
    "google/gemma-2-9b-it",
    "mistralai/mistral-nemo",
    "microsoft/wizardlm-2-8x22b",
    "mistralai/mistral-7b-instruct",
    "microsoft/wizardlm-2-7b",
    "openchat/openchat-7b",
    "nousresearch/hermes-2-pro-llama-3-8b",
    "sao10k/l3-70b-euryale-v2.1",
    "cognitivecomputations/dolphin-mixtral-8x22b",
    "jondurbin/airoboros-l2-70b",
    "lzlv_70b",
    "nousresearch/nous-hermes-llama2-13b",
    "teknium/openhermes-2.5-mistral-7b",
    "sophosympatheia/midnight-rose-70b",
    "meta-llama/llama-3.1-8b-instruct-bf16",
    "qwen/qwen-2.5-72b-instruct",
    "sao10k/l31-70b-euryale-v2.2",
    "qwen/qwen-2-7b-instruct",
    "qwen/qwen-2-72b-instruct",
]


class NOVITA(OPENAI):
    """Novita AI provider"""

    def __init__(self, *args, **kwargs):
        model_choice = kwargs.setdefault("model", model)
        if not model_choice in available_models:
            raise UnsupportedModelError(
                f"Model '{model_choice}' is not yet supported. Choose from {available_models}"
            )
        super().__init__(*args, **kwargs)
        self.chat_endpoint = "https://api.novita.ai/v3/openai/chat/completions"


class AsyncNOVITA(AsyncOPENAI):
    """Async Novita AI provider"""

    def __init__(self, *args, **kwargs):
        model_choice = kwargs.setdefault("model", model)
        if not model_choice in available_models:
            raise UnsupportedModelError(
                f"Model '{model_choice}' is not yet supported. Choose from {available_models}"
            )
        super().__init__(*args, **kwargs)
        self.chat_endpoint = "https://api.novita.ai/v3/openai/chat/completions"
