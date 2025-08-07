import re
import json
import yaml
import httpx
import random
import requests
import string
from pytgpt.utils import Optimizers
from pytgpt.utils import Conversation
from pytgpt.utils import AwesomePrompts
from pytgpt.base import Provider, AsyncProvider
import pytgpt.exceptions as exceptions
from typing import AsyncGenerator

session = requests.Session()

default_model = "k2"


def generate_random_number(size: int = 19) -> str:
    choices = random.choices(string.digits * 5, k=size)
    return "".join(choices)


class KIMI(Provider):
    def __init__(
        self,
        is_conversation: bool = True,
        max_tokens: int = 600,
        timeout: int = 30,
        intro: str = None,
        filepath: str = None,
        update_file: bool = True,
        proxies: dict = {},
        history_offset: int = 10250,
        act: str = None,
        model: str = default_model,
        quiet: bool = False,
    ):
        """Constructor for KIMI

        Args:
            is_conversation (bool, optional): Flag for chatting conversationally. Defaults to True
            max_tokens (int, optional): Maximum number of tokens to be generated upon completion. Defaults to 600.
            timeout (int, optional): Http request timeout. Defaults to 30.
            intro (str, optional): Conversation introductory prompt. Defaults to None.
            filepath (str, optional): Path to file containing conversation history. Defaults to None.
            update_file (bool, optional): Add new prompts and responses to the file. Defaults to True.
            proxies (dict, optional): Http request proxies. Defaults to {}.
            history_offset (int, optional): Limit conversation history to this number of last texts. Defaults to 10250.
            act (str|int, optional): Awesome prompt key or index. (Used as intro). Defaults to None.
            model (str, optional): Model name. Defaults to "Phind Model".
            quiet (bool, optional): Ignore web search-results and yield final response only. Defaults to False.
        """
        self.max_tokens_to_sample = max_tokens
        self.is_conversation = is_conversation
        self.stream_chunk_size = 64
        self.timeout = timeout
        self.last_response = {}
        self.model = model
        self.quiet = quiet
        self.device_id = generate_random_number()
        self.traffic_id = generate_random_number()

        session.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/133.0",
            "Accept": "*/*",
            "priority": "u=1, i",
            "origin": "https://www.kimi.com",
            "x-language": "en-US",
            "x-msh-device-id": self.device_id,
            "x-msh-platform": "web",
            "x-traffic-id": self.traffic_id,
        }

        self.access_token = self.get_access_token()
        session.headers["Authorization"] = f"Bearer {self.access_token}"
        self.chat_id = self.get_chat_id()

        session.headers["referer"] = f"https://www.kimi.com/chat/{self.chat_id}"

        self.chat_endpoint = (
            f"https://www.kimi.com/api/chat/{self.chat_id}/completion/stream"
        )

        self.__available_optimizers = (
            method
            for method in dir(Optimizers)
            if callable(getattr(Optimizers, method)) and not method.startswith("__")
        )
        Conversation.intro = (
            AwesomePrompts().get_act(
                act, raise_not_found=True, default=None, case_insensitive=True
            )
            if act
            else intro or Conversation.intro
        )
        self.conversation = Conversation(
            is_conversation, self.max_tokens_to_sample, filepath, update_file
        )
        self.conversation.history_offset = history_offset
        session.proxies = proxies

    def get_access_token(self) -> str:
        headers = {
            "referer": "https://www.kimi.com/",
        }
        resp = session.post(
            "https://www.kimi.com/api/device/register", json={}, headers=headers
        )
        resp.raise_for_status()
        token = resp.json()["access_token"]
        assert token, f"Failed to fetch access_token -{token}"
        return token

    def get_chat_id(self) -> str:
        resp = session.post(
            "https://www.kimi.com/api/chat",
            json={
                "name": "Unnamed Chat",
                "born_from": "home",
                "kimiplus_id": "kimi",
                "is_example": False,
                "source": "web",
                "tags": [],
            },
        )
        if not resp.ok:
            print(session.headers)
            print(resp.text)
        resp.raise_for_status()
        return resp.json()["id"]

    def ask(
        self,
        prompt: str,
        stream: bool = False,
        raw: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
    ) -> dict:
        """Chat with AI

        Args:
            prompt (str): Prompt to be send.
            stream (bool, optional): Flag for streaming response. Defaults to False.
            raw (bool, optional): Stream back raw response as received. Defaults to False.
            optimizer (str, optional): Prompt optimizer name - `[code, shell_command]`. Defaults to None.
            conversationally (bool, optional): Chat conversationally when using optimizer. Defaults to False.
        Returns:
           dict : {}
        ```json
        {
            "id": "chatcmpl-r0wujizf2i2xb60mjiwt",
            "object": "chat.completion.chunk",
            "created": 1706775384,
            "model": "trt-llm-phind-model-serving",
            "choices": [
                {
                    "index": 0,
                    "delta": {
                        "content": "Hello! How can I assist you with your programming today?"
                        },
                    "finish_reason": null
                }
            ]
        }
        ```
        """
        conversation_prompt = self.conversation.gen_complete_prompt(prompt)
        if optimizer:
            if optimizer in self.__available_optimizers:
                conversation_prompt = getattr(Optimizers, optimizer)(
                    conversation_prompt if conversationally else prompt
                )
            else:
                raise Exception(
                    f"Optimizer is not one of {self.__available_optimizers}"
                )

        payload = {
            "message_history": [
                {"content": conversation_prompt, "metadata": {}, "role": "user"}
            ],
            "requested_model": self.model,
            "user_input": prompt,
        }

        payload = {
            "KimiPlusID": "kimi",
            "Extend": {
                "Sidebar": True,
            },
            "Model": self.model,
            "UseSearch": True,
            "Refs": [],
            "History": [],
            "SceneLabels": [],
            "UseSemanticMemory": False,
            "UseDeepResearch": False,
            "Messages": [
                # {
                #    "Content": self.conversation.intro,
                #    "Role": "system",
                # },
                {
                    "Content": conversation_prompt,
                    "Role": "user",
                },
            ],
        }

        def for_stream():
            response = session.post(
                self.chat_endpoint, json=payload, stream=False, timeout=self.timeout
            )
            if not response.ok:
                raise exceptions.FailedToGenerateResponseError(
                    f"Failed to generate response - ({response.status_code}, {response.reason}) - {response.text}"
                )
            streaming_text = ""
            for value in response.iter_lines(
                decode_unicode=True,
                chunk_size=self.stream_chunk_size,
            ):
                try:
                    modified_value = re.sub("data:", "", value)
                    json_modified_value = json.loads(modified_value)
                    retrieved_text = self.get_message(json_modified_value)
                    if not retrieved_text:
                        continue
                    streaming_text += retrieved_text
                    formatted_response = dict(text=streaming_text)
                    self.last_response = formatted_response
                    yield value if raw else formatted_response
                except json.decoder.JSONDecodeError:
                    pass
            self.conversation.update_chat_history(
                prompt, self.get_message(self.last_response)
            )

        def for_non_stream():
            for _ in for_stream():
                pass
            return self.last_response

        return for_stream() if stream else for_non_stream()

    def chat(
        self,
        prompt: str,
        stream: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
    ) -> str:
        """Generate response `str`
        Args:
            prompt (str): Prompt to be send.
            stream (bool, optional): Flag for streaming response. Defaults to False.
            optimizer (str, optional): Prompt optimizer name - `[code, shell_command]`. Defaults to None.
            conversationally (bool, optional): Chat conversationally when using optimizer. Defaults to False.
        Returns:
            str: Response generated
        """

        def for_stream():
            for response in self.ask(
                prompt, True, optimizer=optimizer, conversationally=conversationally
            ):
                yield self.get_message(response)

        def for_non_stream():
            return self.get_message(
                self.ask(
                    prompt,
                    False,
                    optimizer=optimizer,
                    conversationally=conversationally,
                )
            )

        return for_stream() if stream else for_non_stream()

    def get_message(self, response: dict) -> str:
        """Retrieves message only from response

        Args:
            response (dict): Response generated by `self.ask`

        Returns:
            str: Message extracted
        """
        assert isinstance(response, dict), "Response should be of dict data-type only"
        return response.get("text", "")


class AsyncKIMI(AsyncProvider):
    def __init__(
        self,
        is_conversation: bool = True,
        max_tokens: int = 600,
        timeout: int = 30,
        intro: str = None,
        filepath: str = None,
        update_file: bool = True,
        proxies: dict = {},
        history_offset: int = 10250,
        act: str = None,
        model: str = default_model,
        quiet: bool = False,
    ):
        """Instantiates PHIND

        Args:
            is_conversation (bool, optional): Flag for chatting conversationally. Defaults to True
            max_tokens (int, optional): Maximum number of tokens to be generated upon completion. Defaults to 600.
            timeout (int, optional): Http request timeout. Defaults to 30.
            intro (str, optional): Conversation introductory prompt. Defaults to None.
            filepath (str, optional): Path to file containing conversation history. Defaults to None.
            update_file (bool, optional): Add new prompts and responses to the file. Defaults to True.
            proxies (dict, optional): Http request proxies. Defaults to {}.
            history_offset (int, optional): Limit conversation history to this number of last texts. Defaults to 10250.
            act (str|int, optional): Awesome prompt key or index. (Used as intro). Defaults to None.
            model (str, optional): Model name. Defaults to "Phind Model".
            quiet (bool, optional): Ignore web search-results and yield final response only. Defaults to False.
        """
        self.max_tokens_to_sample = max_tokens
        self.is_conversation = is_conversation
        self.chat_endpoint = "https://https.extension.phind.com/agent/"
        self.stream_chunk_size = 64
        self.timeout = timeout
        self.last_response = {}
        self.model = model
        self.quiet = quiet

        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "",
            "Accept": "*/*",
            "Accept-Encoding": "Identity",
        }

        self.__available_optimizers = (
            method
            for method in dir(Optimizers)
            if callable(getattr(Optimizers, method)) and not method.startswith("__")
        )
        Conversation.intro = (
            AwesomePrompts().get_act(
                act, raise_not_found=True, default=None, case_insensitive=True
            )
            if act
            else intro or Conversation.intro
        )
        self.conversation = Conversation(
            is_conversation, self.max_tokens_to_sample, filepath, update_file
        )
        self.conversation.history_offset = history_offset
        self.session = httpx.AsyncClient(headers=self.headers, proxies=proxies)

    async def ask(
        self,
        prompt: str,
        stream: bool = False,
        raw: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
        synchronous_generator=False,
    ) -> dict | AsyncGenerator:
        """Asynchronously Chat with AI

        Args:
            prompt (str): Prompt to be send.
            stream (bool, optional): Flag for streaming response. Defaults to False.
            raw (bool, optional): Stream back raw response as received. Defaults to False.
            optimizer (str, optional): Prompt optimizer name - `[code, shell_command]`. Defaults to None.
            conversationally (bool, optional): Chat conversationally when using optimizer. Defaults to False.
        Returns:
           dict|AsyncGenerator : ai content.
        ```json
        {
            "id": "chatcmpl-r0wujizf2i2xb60mjiwt",
            "object": "chat.completion.chunk",
            "created": 1706775384,
            "model": "trt-llm-phind-model-serving",
            "choices": [
                {
                    "index": 0,
                    "delta": {
                        "content": "Hello! How can I assist you with your programming today?"
                        },
                    "finish_reason": null
                }
            ]
        }
        ```
        """
        conversation_prompt = self.conversation.gen_complete_prompt(prompt)
        if optimizer:
            if optimizer in self.__available_optimizers:
                conversation_prompt = getattr(Optimizers, optimizer)(
                    conversation_prompt if conversationally else prompt
                )
            else:
                raise Exception(
                    f"Optimizer is not one of {self.__available_optimizers}"
                )

        payload = {
            "additional_extension_context": "",
            "allow_magic_buttons": True,
            "is_vscode_extension": True,
            "message_history": [
                {"content": conversation_prompt, "metadata": {}, "role": "user"}
            ],
            "requested_model": self.model,
            "user_input": prompt,
        }

        async def for_stream():
            async with self.session.stream(
                "POST",
                self.chat_endpoint,
                json=payload,
                timeout=self.timeout,
            ) as response:
                if (
                    not response.is_success
                    or not response.headers.get("Content-Type")
                    == "text/event-stream; charset=utf-8"
                ):
                    raise exceptions.FailedToGenerateResponseError(
                        f"Failed to generate response - ({response.status_code}, {response.reason_phrase})"
                    )
                streaming_text = ""
                async for value in response.aiter_lines():
                    try:
                        modified_value = re.sub("data:", "", value)
                        json_modified_value = json.loads(modified_value)
                        retrieved_text = await self.get_message(json_modified_value)
                        if not retrieved_text:
                            continue
                        streaming_text += retrieved_text
                        json_modified_value["choices"][0]["delta"][
                            "content"
                        ] = streaming_text
                        self.last_response.update(json_modified_value)
                        yield value if raw else json_modified_value
                    except json.decoder.JSONDecodeError:
                        pass
                self.conversation.update_chat_history(
                    prompt, await self.get_message(self.last_response)
                )

        async def for_non_stream():
            async for _ in for_stream():
                pass
            return self.last_response

        return (
            for_stream()
            if stream and not synchronous_generator
            else await for_non_stream()
        )

    async def chat(
        self,
        prompt: str,
        stream: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
    ) -> str | AsyncGenerator:
        """Generate response `str`
        Args:
            prompt (str): Prompt to be send.
            stream (bool, optional): Flag for streaming response. Defaults to False.
            optimizer (str, optional): Prompt optimizer name - `[code, shell_command]`. Defaults to None.
            conversationally (bool, optional): Chat conversationally when using optimizer. Defaults to False.
        Returns:
            str|AsyncGenerator: Response generated
        """

        async def for_stream():
            ask_resp = await self.ask(
                prompt, True, optimizer=optimizer, conversationally=conversationally
            )
            async for response in ask_resp:
                yield await self.get_message(response)

        async def for_non_stream():
            return await self.get_message(
                await self.ask(
                    prompt,
                    False,
                    optimizer=optimizer,
                    conversationally=conversationally,
                )
            )

        return for_stream() if stream else await for_non_stream()

    async def get_message(self, response: dict) -> str:
        """Retrieves message only from response

        Args:
            response (dict): Response generated by `self.ask`

        Returns:
            str: Message extracted
        """
        assert isinstance(response, dict), "Response should be of dict data-type only"
        if response.get("type", "") == "metadata":
            return

        delta: dict = response["choices"][0]["delta"]

        if not delta:
            return ""

        elif delta.get("function_call"):
            if self.quiet:
                return ""

            function_call: dict = delta["function_call"]
            if function_call.get("name"):
                return function_call["name"]
            elif function_call.get("arguments"):
                return function_call.get("arguments")

        elif delta.get("metadata"):
            if self.quiet:
                return ""
            return yaml.dump(delta["metadata"])

        else:
            return (
                response["choices"][0]["delta"].get("content")
                if response["choices"][0].get("finish_reason") is None
                else ""
            )


if __name__ == "__main__":
    bot = PHIND()

    def main():
        resp = bot.ask("hello")
        for value in resp:
            print(value)

    async def asyncmain():
        bot = AsyncPHIND()
        resp = await bot.chat("hello", False)
        print(resp)
        # async for value in resp:
        #    print(value)

    main()
    import asyncio

    asyncio.run(asyncmain())
