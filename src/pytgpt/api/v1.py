from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response, StreamingResponse
from fastapi.encoders import jsonable_encoder
from json import dumps
from pydantic import BaseModel, validator, PositiveInt
from typing import Union, Any, Generator
from pytgpt import gpt4free_providers

# providers
from pytgpt.leo import LEO
from pytgpt.opengpt import OPENGPT
from pytgpt.koboldai import KOBOLDAI
from pytgpt.phind import PHIND
from pytgpt.llama2 import LLAMA2
from pytgpt.blackboxai import BLACKBOXAI
from pytgpt.perplexity import PERPLEXITY
from pytgpt.gpt4free import GPT4FREE

provider_map = {
    "leo": LEO,
    "opengpt": OPENGPT,
    "koboldai": KOBOLDAI,
    "phind": PHIND,
    "llama2": LLAMA2,
    "blackboxai": BLACKBOXAI,
    "perplexity": PERPLEXITY,
}

supported_providers = list(provider_map.keys()) + gpt4free_providers

app = APIRouter()


class UserPayload(BaseModel):
    prompt: str
    provider: str = "phind"
    # is_conversation: bool = False
    whole: bool = False
    max_tokens: PositiveInt = 600
    timeout: PositiveInt = 30
    proxy: Union[str, None] = None

    @validator("provider")
    def validate_provider(provider: str) -> object:
        if provider not in supported_providers:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Provider '{provider}' is not one of [{', '.join(supported_providers)}]",
            )
        return provider


class ProviderResponse(BaseModel):
    """
    - `provider` : Provider name that generated response.
    - `text` : Response to the prompt.
    - `detail` : Any other special info.
    - `model` : Model used to generate response.
    """

    provider: Union[str, None] = None
    text: Union[str, None] = None
    body: Union[dict, None] = None
    detail: Union[Any, None] = None
    model: Union[str, None] = None


def init_provider(payload: UserPayload) -> object:
    return provider_map.get(payload.provider, GPT4FREE)(
        is_conversation=False,  # payload.is_conversation,
        max_tokens=payload.max_tokens,
        timeout=payload.timeout,
        proxies=(
            {
                "https": payload.proxy,
            }
            if payload.proxy
            else {}
        ),
    )


@app.post("/nostream", name="no-stream")
async def non_stream(payload: UserPayload) -> ProviderResponse:
    """No response streaming.

    - `prompt` : User query.
    - `provider` : LLM provider name.
    - `whole` : Return whole response body instead of text only.
    - `max_tokens` : Maximum number of tokens to be generated upon completion.
    - `timeout` : Http request timeout.
    - `proxy` : Http request proxy.
    """
    try:
        provider_obj: LEO = init_provider(payload)
        ai_generated_text: str = provider_obj.chat(payload.prompt)
        return ProviderResponse(
            provider=payload.provider,
            text=None if payload.whole else ai_generated_text,
            body=provider_obj.last_response if payload.whole else None,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


def generate_streaming_response(payload: UserPayload) -> Generator:

    try:
        provider_obj: LEO = init_provider(payload)

        for text in provider_obj.chat(payload.prompt, stream=True):
            response = ProviderResponse(
                provider=payload.provider,
                text=None if payload.whole else text,
                body=provider_obj.last_response if payload.whole else None,
            )
            yield dumps(jsonable_encoder(response)) + "\n"

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@app.post("/stream", name="stream", response_model=ProviderResponse)
async def stream(payload: UserPayload) -> Any:
    """Stream back response as received.

    - `prompt` : User query.
    - `provider` : LLM provider name.
    - `whole` : Return whole response body instead of text only.
    - `max_tokens` : Maximum number of tokens to be generated upon completion.
    - `timeout` : Http request timeout.
    - `proxy` : Http request proxy.
    """
    return StreamingResponse(
        generate_streaming_response(payload),
        media_type="text/event-stream",
    )
