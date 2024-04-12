from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import Response, StreamingResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from json import dumps
from pydantic import BaseModel, validator, PositiveInt
from typing import Union, Any, Generator
from pytgpt import gpt4free_providers
from uuid import uuid4

# providers
from pytgpt.leo import LEO
from pytgpt.opengpt import OPENGPT
from pytgpt.koboldai import KOBOLDAI
from pytgpt.phind import PHIND
from pytgpt.llama2 import LLAMA2
from pytgpt.blackboxai import BLACKBOXAI
from pytgpt.perplexity import PERPLEXITY
from pytgpt.gpt4free import GPT4FREE
from pytgpt.imager import Imager
from pytgpt.utils import api_static_image_dir

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


class ProvidersModel(BaseModel):
    tgpt: list[str] = list(provider_map.keys())
    g4f: list[str] = gpt4free_providers

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "tgpt": ["phind", "opengpt", "koboldai"],
                    "g4f": [
                        "Koala",
                        "FreeGPT",
                        "You",
                    ],
                }
            ]
        }
    }


class UserPayload(BaseModel):
    prompt: str
    provider: str = "phind"
    # is_conversation: bool = False
    whole: bool = False
    max_tokens: PositiveInt = 600
    timeout: PositiveInt = 30
    proxy: Union[dict[str, str], None] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "prompt": "Hello there",
                    "provider": "phind",
                    "whole": False,
                    "max_tokens": 600,
                    "timeout": 30,
                    "proxy": {
                        "http": "socks4://38.54.6.39:4000",
                        "https": "socks4://38.54.6.39:4000",
                    },
                }
            ]
        }
    }

    @validator("provider")
    def validate_provider(provider: str) -> object:
        if provider not in supported_providers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
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
    model: Union[str, None] = "default"

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "provider": "phind",
                    "text": "How can I help you today?",
                    "body": {
                        "id": "chatcmpl-qnml7olyfeq5kw2r7pue",
                        "object": "chat.completion.chunk",
                        "created": 1712895194,
                        "model": "trt-llm-phind-model-34b-8k-context",
                        "choices": [
                            {
                                "index": 0,
                                "delta": {"content": "How can I help you today?"},
                                "finish_reason": None,
                            }
                        ],
                        "detail": None,
                        "model": None,
                    },
                    "detail": "TypeError: NetworkError when attempting to fetch resource.",
                    "model": "default",
                },
            ],
        },
    }


class ImagePayload(BaseModel):
    prompt: str
    amount: PositiveInt = 1
    proxy: Union[dict[str, str], None] = None
    timeout: PositiveInt = 30

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "prompt": "Mount Everest view from ISS",
                    "amount": 2,
                    "proxy": {
                        "http": "socks4://54.248.238.110:80",
                        "https": "socks4://54.248.238.110:80",
                    },
                    "timeout": 30,
                },
                {
                    "prompt": "Developed Nairobi in 3050",
                    "amount": 2,
                    "proxy": None,
                    "timeout": 30,
                },
            ]
        }
    }

    @validator("amount")
    def validate_amount(amount: int) -> PositiveInt:
        if amount > 10:
            raise HTTPException(
                status=status.HTTP_400_BAD_REQUEST,
                detail=f"Amount {amount} is out of range : 1-10",
            )
        return amount


class ImageBytesPayload(BaseModel):
    prompt: str
    proxy: Union[dict[str, str], None] = None
    timeout: PositiveInt = 30

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "prompt": "Jay Z performing",
                    "proxy": {
                        "http": "socks4://199.229.254.129:4145",
                        "https": "socks4://199.229.254.129:4145",
                    },
                    "timeout": 30,
                },
                {"prompt": "Developed Nairobi in 3050", "proxy": None, "timeout": 30},
            ]
        }
    }


class ImageBytesResponse(BaseModel):
    image: bytes


class ImageResponse(BaseModel):
    """
    - `urls` : List of urls
    """

    urls: list[str]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "urls": [
                        "http://localhost:8000/static/images/80e374cc-4546-4650-8203-533a04a9c06a.jpeg",
                        "http://localhost:8000/static/images/80e374cc-4546-4650-8203-533a04a9c06a_1.jpeg",
                    ]
                }
            ]
        }
    }


def init_provider(payload: UserPayload) -> object:
    return provider_map.get(payload.provider, GPT4FREE)(
        is_conversation=False,  # payload.is_conversation,
        max_tokens=payload.max_tokens,
        timeout=payload.timeout,
        proxies=payload.proxy,
    )


@app.get(
    "/chat/providers",
)
async def llm_providers() -> ProvidersModel:
    """LLM providers for text generation

    - `tgpt` : List of [python-tgpt](https://github.com/Simatwa/tgpt2)-based providers.
    - `g4f` : List of [gpt4free](https://github.com/xtekky/gpt4free)-based providers.

    **Warning** : Not all of *g4f-based* providers are functional.
    """
    return ProvidersModel()


@app.post("/chat/nostream", name="no-stream")
async def non_stream(payload: UserPayload) -> ProviderResponse:
    """No response streaming.

    - `prompt` : User query.
    - `provider` : LLM provider name.
    - `whole` : Return whole response body instead of text only.
    - `max_tokens` : Maximum number of tokens to be generated upon completion.
    - `timeout` : Http request timeout.
    - `proxy` : Http request proxy.

    *Ensure `proxy` value is correct otherwise make it `null`*

    **NOTE** : Example values are modified for illustration purposes.
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


@app.post("/chat/stream", name="stream", response_model=ProviderResponse)
async def stream(payload: UserPayload) -> Any:
    """Stream back response as received.

    - `prompt` : User query.
    - `provider` : LLM provider name.
    - `whole` : Return whole response body instead of text only.
    - `max_tokens` : Maximum number of tokens to be generated upon completion.
    - `timeout` : Http request timeout.
    - `proxy` : Http request proxy.

    *Ensure `proxy` value is correct otherwise make it `null`*

    **NOTE** : Example values are modified for illustration purposes.
    """
    return StreamingResponse(
        generate_streaming_response(payload),
        media_type="text/event-stream",
    )


@app.post("/image", name="prompt-to-image")
async def generate_image(payload: ImagePayload, request: Request) -> ImageResponse:
    """Generate images from prompt

    - `prompt` : Image description
    - `amount` : Images to be generated. Maximum of 10.
    - `timeout` : Http request timeout.
    - `proxy` : Http request proxies.

    *Ensure `proxy` value is correct otherwise make it `null`*
    """
    try:
        host = f"{request.url.scheme}://{request.url.netloc}"
        image_gen_obj = Imager(timeout=payload.timeout, proxies=payload.proxy)
        image_generator = image_gen_obj.generate(
            prompt=payload.prompt, amount=payload.amount, stream=True
        )
        image_urls = image_gen_obj.save(
            image_generator,
            name=uuid4().__str__(),
            dir=api_static_image_dir,
            filenames_prefix=f"{host}/static/images/",
        )
        return ImageResponse(urls=image_urls)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/image/bytes", name="prompt-to-image (bytes)")
async def generate_image(payload: ImageBytesPayload, request: Request) -> Response:
    """Generate images from prompt and return raw bytes

    - `prompt` : Image description
    - `timeout` : Http request timeout.
    - `proxy` : Http request proxies.

    **Only one image is generated.**

    **NOTE** : *Ensure `proxy` value is correct otherwise make it `null`*
    """
    try:
        image_gen_obj = Imager(timeout=payload.timeout, proxies=payload.proxy)
        image_list = image_gen_obj.generate(prompt=payload.prompt)
        response = Response(
            image_list[0],
            media_type="image/jpeg",
        )
        response.headers["Content-Disposition"] = (
            f"attachment; filename={payload.prompt[:25]+'...' if len(payload.prompt)>25 else payload.prompt}.jpeg"
        )
        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/image/bytes", name="prompt-to-image (bytes)")
async def redirect_image_generation(
    prompt: str, proxy: Union[str, None] = None, timeout: int = 30
):
    """Generate images from prompt and return raw bytes

    - `prompt` : Image description
    - `timeout` : Http request timeout.
    - `proxy` : Http request proxies.

    **Only one image is generated.**

    **NOTE** : *Ensure `proxy` value is correct otherwise make it `null`*
    """
    try:
        image_gen_obj = Imager(
            timeout=timeout, proxies={"https": proxy} if proxy else {}
        )
        image_list = image_gen_obj.generate(prompt=prompt)
        response = Response(
            image_list[0],
            media_type="image/jpeg",
        )
        response.headers["Content-Disposition"] = (
            f"attachment; filename={prompt[:25]+'...' if len(prompt)>25 else prompt}.jpeg"
        )
        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.get("/image/bytes/redirect", name="prompt-to-image (bytes - redirect) ")
async def redirect_image_generation(prompt: str):
    """Redirect image generation request to [pollinations.ai](https://pollinations.ai)"""
    return RedirectResponse(
        f"https://image.pollinations.ai/prompt/{prompt}",
    )
