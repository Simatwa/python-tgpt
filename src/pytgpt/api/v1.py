from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import Response, StreamingResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from json import dumps
from pydantic import BaseModel, field_validator, PositiveInt
from typing import Union, Any, AsyncGenerator
from pytgpt import gpt4free_providers
from uuid import uuid4
from .utils import api_exception_handler

# providers
from pytgpt.gpt4free import AsyncGPT4FREE
from pytgpt.auto import AsyncAUTO
from pytgpt.imager import AsyncImager
from pytgpt.imager import AsyncProdia
from pytgpt.utils import Audio
from pytgpt.async_providers import tgpt_mapper as provider_map
from pytgpt.utils import api_static_image_dir

provider_map.update({"auto": AsyncAUTO})

image_providers = {"default": AsyncImager, "prodia": AsyncProdia}

supported_providers = list(provider_map.keys()) + gpt4free_providers

app = APIRouter()


class ProvidersModel(BaseModel):
    tgpt: list[str] = list(provider_map.keys())
    g4f: list[str] = gpt4free_providers

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "tgpt": [
                        "phind",
                        "opengpt",
                        "koboldai",
                    ],
                    "g4f": [
                        "Koala",
                        "Blackbox",
                        "FreeChatgpt",
                    ],
                }
            ]
        }
    }


class TextGenerationPayload(BaseModel):
    prompt: str
    provider: str = "auto"
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
                    "provider": "auto",
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

    @field_validator("provider")
    def validate_provider(provider: str) -> object:
        if provider not in supported_providers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=dict(
                    message=f"Provider '{provider}' is not one of [{', '.join(supported_providers)}]",
                ),
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
    provider: Union[str, None] = "default"

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "prompt": "Sunset view from ISS",
                    "amount": 2,
                    "proxy": {
                        "http": "socks4://54.248.238.110:80",
                        "https": "socks4://54.248.238.110:80",
                    },
                    "timeout": 30,
                    "provider": "default",
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

    @field_validator("amount")
    def validate_amount(amount: int) -> PositiveInt:
        if amount > 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=dict(
                    message=f"Amount {amount} is out of range : 1-10",
                ),
            )
        return amount

    @field_validator("provider")
    def validate_provider(provider: Union[str, None]) -> str:

        if provider is not None and not provider in image_providers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=dict(
                    message=f"Image provider '{provider}' is not one of [{', '.join(list(image_providers.keys()))}]",
                ),
            )
        return "default" if provider is None else provider


class ImageBytesPayload(BaseModel):
    prompt: str
    proxy: Union[dict[str, str], None] = None
    timeout: PositiveInt = 30
    provider: Union[str, None] = "default"

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "prompt": "Alan Walker performing",
                    "proxy": {
                        "http": "socks4://199.229.254.129:4145",
                        "https": "socks4://199.229.254.129:4145",
                    },
                    "timeout": 30,
                    "provider": "default",
                },
                {"prompt": "Developed Nairobi in 3050", "proxy": None, "timeout": 30},
            ]
        }
    }

    @field_validator("provider")
    def validate_provider(provider: Union[str, None]) -> str:
        if provider is not None and not provider in image_providers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=dict(
                    message=f"Image provider '{provider}' is not one of [{', '.join(list(image_providers.keys()))}]",
                ),
            )
        return "default" if provider is None else provider


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


class TextToAudioPayload(BaseModel):
    message: str
    voice: Union[str, None] = "en-US-Wavenet-C"
    proxy: Union[dict[str, str], None] = None
    timeout: int = 30
    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "There is a place for people like you.",
                "voice": "en-US-Wavenet-C",
                "proxy": {
                    "http": "socks4://199.229.254.129:4145",
                    "https": "socks4://199.229.254.129:4145",
                },
                "timeout": 30,
            }
        }
    }

    @field_validator("voice")
    def validate_voice(voice) -> str:
        if not voice in Audio.all_voices:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=dict(
                    message=f"Voice '{voice}' is not one of '[{', '.join(Audio.all_voices)}]"
                ),
            )
        return "en-US-Wavenet-C" if not voice else voice


class TextToAudioResponse(BaseModel):
    """
    - `url` : Link to generated audio file.
    """

    url: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "url": "http://localhost:8000/static/audios/f9d4233f-9b78-4d87-bc27-5d2ab928f673.mp3",
            }
        }
    }


async def init_provider(payload: TextGenerationPayload) -> object:
    return provider_map.get(payload.provider, AsyncGPT4FREE)(
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
@api_exception_handler
async def non_stream(payload: TextGenerationPayload) -> ProviderResponse:
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
    provider_obj: AsyncGPT4FREE = await init_provider(payload)
    ai_generated_text: str = await provider_obj.chat(payload.prompt)
    return ProviderResponse(
        provider=(
            provider_obj.provider_name
            if payload.provider == "auto"
            else payload.provider
        ),
        text=ai_generated_text,
        body=provider_obj.last_response if payload.whole else None,
    )


async def generate_streaming_response(payload: TextGenerationPayload) -> AsyncGenerator:
    provider_obj = await init_provider(payload)
    async_chat = await provider_obj.chat(payload.prompt, stream=True)
    async for text in async_chat:
        response = ProviderResponse(
            provider=(
                provider_obj.provider_name
                if payload.provider == "auto"
                else payload.provider
            ),
            text=text,
            body=provider_obj.last_response if payload.whole else None,
        )
        yield dumps(jsonable_encoder(response)) + "\n"


@app.post("/chat/stream", name="stream", response_model=ProviderResponse)
@api_exception_handler
async def stream(payload: TextGenerationPayload) -> Any:
    """Stream back response as received.

    - `prompt` : User query.
    - `provider` : LLM provider name.
    - `whole` : Return whole response body instead of text only.
    - `max_tokens` : Maximum number of tokens to be generated upon completion.
    - `timeout` : Http request timeout.
    - `proxy` : Http request proxy.

    **NOTE** :
       - *Example values are modified for illustration purposes.*
       - *Ensure `proxy` value is correct otherwise make it `null`*
    """
    return StreamingResponse(
        generate_streaming_response(payload),
        media_type="text/event-stream",
    )


@app.post("/image", name="prompt-to-image")
@api_exception_handler
async def generate_image(payload: ImagePayload, request: Request) -> ImageResponse:
    """Generate images from prompt

    - `prompt` : Image description
    - `amount` : Images to be generated. Maximum of 10.
    - `timeout` : Http request timeout.
    - `proxy` : Http request proxies.
    - `provider` : Image provider name ie. *[default, prodia]*

    **NOTE** : *Ensure `proxy` value is correct otherwise make it `null`*
    """
    host = f"{request.url.scheme}://{request.url.netloc}"
    image_gen_obj = image_providers.get(payload.provider)(
        timeout=payload.timeout, proxies=payload.proxy
    )
    image_generator = await image_gen_obj.generate(
        prompt=payload.prompt, amount=payload.amount, stream=True
    )
    image_urls = await image_gen_obj.save(
        image_generator,
        name=uuid4().__str__(),
        dir=api_static_image_dir,
        filenames_prefix=f"{host}/static/images/",
    )
    return ImageResponse(urls=image_urls)


@app.post("/image/bytes", name="prompt-to-image (bytes)")
@api_exception_handler
async def generate_image(payload: ImageBytesPayload, request: Request) -> Response:
    """Generate images from prompt and return raw bytes

    - `prompt` : Image description
    - `timeout` : Http request timeout.
    - `proxy` : Http request proxies.
    - `provider` : Image provider name ie. *[default, prodia]*

    **Only one image is generated.**

    **NOTE** : *Ensure `proxy` value is correct otherwise make it `null`*
    """
    image_gen_obj = image_providers.get(payload.provider)(
        timeout=payload.timeout, proxies=payload.proxy
    )
    image_list = await image_gen_obj.generate(prompt=payload.prompt)
    response = Response(
        image_list[0],
        media_type=f"image/{image_gen_obj.image_extension}",
    )
    response.headers["Content-Disposition"] = (
        f"attachment; filename={payload.prompt[:25]+'...' if len(payload.prompt)>25 else payload.prompt}.{image_gen_obj.image_extension}"
    )
    return response


@app.get("/image/bytes", name="prompt-to-image (bytes)")
@api_exception_handler
async def generate_image_return_bytes(
    prompt: str,
    proxy: Union[str, None] = None,
    timeout: int = 30,
    provider: str = "default",
):
    """Generate images from prompt and return raw bytes

    - `prompt` : Image description
    - `timeout` : Http request timeout.
    - `proxy` : Http request proxies.
    - `provider` : Image provider name ie. *[default, prodia]*

    **Only one image is generated.**

    **NOTE** : *Ensure `proxy` value is correct otherwise make it `null`*
    """
    image_gen_obj = image_providers.get(provider, "default")(
        timeout=timeout, proxies={"https": proxy} if proxy else {}
    )
    image_list = await image_gen_obj.generate(prompt=prompt)
    response = Response(
        image_list[0],
        media_type=f"image/{image_gen_obj.image_extension}",
    )
    response.headers["Content-Disposition"] = (
        f"attachment; filename={prompt[:25]+'...' if len(prompt)>25 else prompt}.{image_gen_obj.image_extension}"
    )
    return response


@app.get("/image/bytes/redirect", name="prompt-to-image (bytes - redirect) ")
@api_exception_handler
async def redirect_image_generation(prompt: str):
    """Redirect image generation request to [pollinations.ai](https://pollinations.ai)"""
    return RedirectResponse(
        f"https://image.pollinations.ai/prompt/{prompt}",
    )


@app.post("/voice", name="text-to-voice")
@api_exception_handler
async def text_to_audio(
    payload: TextToAudioPayload, request: Request
) -> TextToAudioResponse:
    """Vocalize text

    - `message` : Text to be synthesised.
    - `voice` :  The voice to use for speech synthesis.
    - `timeout` : Http request timeout in seconds.
    - `proxy` : Http request proxy.

    **NOTE** : *Ensure `proxy` value is correct otherwise make it `null`*
    """
    host = f"{request.url.scheme}://{request.url.netloc}"
    filename = uuid4().__str__() + ".mp3"
    await Audio.async_text_to_audio(
        message=payload.message,
        voice=payload.voice,
        proxies=payload.proxy,
        timeout=payload.timeout,
        save_to=Audio.cache_dir.joinpath(filename).as_posix(),
    )
    return TextToAudioResponse(url=f"{host}/static/audios/" + filename)


@app.get("/voice", name="text-to-voice (bytes)")
@api_exception_handler
async def text_to_audio_bytes(
    message: str,
    voice: str = "en-US-Wavenet-C",
    timeout: int = 30,
    proxy: Union[str, None] = None,
):
    """Return raw audio

    - `message` : Text to be synthesised.
    - `voice` :  The voice to use for speech synthesis.
    - `timeout` : Http request timeout in seconds.
    - `proxy` : Http request proxy.

    **NOTE** : *Ensure `proxy` value is correct otherwise make it `null`*
    """
    image_bytes = await Audio.async_text_to_audio(
        message=message,
        voice=voice if voice in Audio.all_voices else "en-US-Wavenet-C",
        proxies={"https": proxy} if proxy else {},
        timeout=timeout,
    )
    return Response(
        content=image_bytes,
        media_type="audio/mpeg",
        headers={
            "Content-Disposition": f"attachment; filename={uuid4().__str__()}.mp3"
        },
    )
