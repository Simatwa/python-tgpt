from pytgpt.base import Provider, AsyncProvider
from pytgpt.koboldai import KOBOLDAI, AsyncKOBOLDAI
from pytgpt.phind import PHIND, AsyncPHIND
from pytgpt.perplexity import PERPLEXITY
from pytgpt.gpt4free import GPT4FREE, AsyncGPT4FREE
from pytgpt.gpt4free.utils import TestProviders
from pytgpt.auto.errors import AllProvidersFailure
from pytgpt.utils import Conversation
from pytgpt.async_providers import tgpt_mapper as async_provider_map
from typing import AsyncGenerator

from typing import Union
from typing import Any
import logging


provider_map: dict[str, Union[KOBOLDAI, PHIND, PERPLEXITY, GPT4FREE]] = {
    "phind": PHIND,
    "perplexity": PERPLEXITY,
    "koboldai": KOBOLDAI,
    "gpt4free": GPT4FREE,
}


class AUTO(Provider):
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
        exclude: list[str] = [],
    ):
        """Instantiates AUTO

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
            exclude(list[str], optional): List of providers to be excluded. Defaults to [].
        """
        self.provider: Union[KOBOLDAI, PHIND, PERPLEXITY, GPT4FREE] = None
        self.provider_name: str = None
        self.is_conversation = is_conversation
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.intro = intro
        self.filepath = filepath
        self.update_file = update_file
        self.proxies = proxies
        self.history_offset = history_offset
        self.act = act
        self.exclude = exclude

    @property
    def last_response(self) -> dict[str, Any]:
        return self.provider.last_response

    @property
    def conversation(self) -> Conversation:
        return self.provider.conversation

    def ask(
        self,
        prompt: str,
        stream: bool = False,
        raw: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
        run_new_test: bool = False,
    ) -> dict:
        """Chat with AI

        Args:
            prompt (str): Prompt to be send.
            stream (bool, optional): Flag for streaming response. Defaults to False.
            raw (bool, optional): Stream back raw response as received. Defaults to False.
            optimizer (str, optional): Prompt optimizer name - `[code, shell_command]`. Defaults to None.
            conversationally (bool, optional): Chat conversationally when using optimizer. Defaults to False.
            run_new_test (bool, optional): Perform new test on g4f-based providers. Defaults to False.
        Returns:
           dict : {}
        """
        ask_kwargs: dict[str, Union[str, bool]] = {
            "prompt": prompt,
            "stream": stream,
            "raw": raw,
            "optimizer": optimizer,
            "conversationally": conversationally,
        }

        # tgpt-based providers
        for provider_name, provider_obj in provider_map.items():
            # continue
            if provider_name in self.exclude:
                continue
            try:
                self.provider_name = f"tgpt-{provider_name}"
                self.provider = provider_obj(
                    is_conversation=self.is_conversation,
                    max_tokens=self.max_tokens,
                    timeout=self.timeout,
                    intro=self.intro,
                    filepath=self.filepath,
                    update_file=self.update_file,
                    proxies=self.proxies,
                    history_offset=self.history_offset,
                    act=self.act,
                )

                def for_stream():
                    for chunk in self.provider.ask(**ask_kwargs):
                        yield chunk

                def for_non_stream():
                    return self.provider.ask(**ask_kwargs)

                return for_stream() if stream else for_non_stream()

            except Exception as e:
                logging.debug(
                    f"Failed to generate response using provider {provider_name} - {e}"
                )

        # g4f-based providers

        for provider_info in TestProviders(timeout=self.timeout).get_results(
            run=run_new_test
        ):
            if provider_info["name"] in self.exclude:
                continue
            try:
                self.provider_name = f"g4f-{provider_info['name']}"
                self.provider = GPT4FREE(
                    provider=provider_info["name"],
                    is_conversation=self.is_conversation,
                    max_tokens=self.max_tokens,
                    intro=self.intro,
                    filepath=self.filepath,
                    update_file=self.update_file,
                    proxies=self.proxies,
                    history_offset=self.history_offset,
                    act=self.act,
                )

                def for_stream():
                    for chunk in self.provider.ask(**ask_kwargs):
                        yield chunk

                def for_non_stream():
                    return self.provider.ask(**ask_kwargs)

                return for_stream() if stream else for_non_stream()

            except Exception as e:
                logging.debug(
                    f"Failed to generate response using GPT4FREE-based provider {provider_name} - {e}"
                )

        raise AllProvidersFailure(
            "None of the providers generated response successfully."
        )

    def chat(
        self,
        prompt: str,
        stream: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
        run_new_test: bool = False,
    ) -> str:
        """Generate response `str`
        Args:
            prompt (str): Prompt to be send.
            stream (bool, optional): Flag for streaming response. Defaults to False.
            optimizer (str, optional): Prompt optimizer name - `[code, shell_command]`. Defaults to None.
            conversationally (bool, optional): Chat conversationally when using optimizer. Defaults to False.
            run_new_test (bool, optional): Perform new test on g4f-based providers. Defaults to False.
        Returns:
            str: Response generated
        """

        def for_stream():
            for response in self.ask(
                prompt,
                True,
                optimizer=optimizer,
                conversationally=conversationally,
                run_new_test=run_new_test,
            ):
                yield self.get_message(response)

        def for_non_stream():
            ask_response = self.ask(
                prompt,
                False,
                optimizer=optimizer,
                conversationally=conversationally,
                run_new_test=run_new_test,
            )
            return self.get_message(ask_response)

        return for_stream() if stream else for_non_stream()

    def get_message(self, response: dict) -> str:
        """Retrieves message only from response

        Args:
            response (dict): Response generated by `self.ask`

        Returns:
            str: Message extracted
        """
        assert self.provider is not None, "Chat with AI first"
        return self.provider.get_message(response)


class AsyncAUTO(AsyncProvider):
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
        exclude: list[str] = [],
    ):
        """Instantiates AsyncAUTO

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
            exclude(list[str], optional): List of providers to be excluded. Defaults to [].
        """
        self.provider: Union[
            AsyncKOBOLDAI,
            AsyncPHIND,
            AsyncGPT4FREE,
        ] = None
        self.provider_name: str = None
        self.is_conversation = is_conversation
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.intro = intro
        self.filepath = filepath
        self.update_file = update_file
        self.proxies = proxies
        self.history_offset = history_offset
        self.act = act
        self.exclude = exclude

    @property
    def last_response(self) -> dict[str, Any]:
        return self.provider.last_response

    @property
    def conversation(self) -> Conversation:
        return self.provider.conversation

    async def ask(
        self,
        prompt: str,
        stream: bool = False,
        raw: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
        run_new_test: bool = False,
    ) -> dict | AsyncGenerator:
        """Chat with AI asynchronously.

        Args:
            prompt (str): Prompt to be send.
            stream (bool, optional): Flag for streaming response. Defaults to False.
            raw (bool, optional): Stream back raw response as received. Defaults to False.
            optimizer (str, optional): Prompt optimizer name - `[code, shell_command]`. Defaults to None.
            conversationally (bool, optional): Chat conversationally when using optimizer. Defaults to False.
            run_new_test (bool, optional): Perform new test on g4f-based providers. Defaults to False.
        Returns:
           dict|AsyncGenerator : ai response.
        """
        ask_kwargs: dict[str, Union[str, bool]] = {
            "prompt": prompt,
            "stream": stream,
            "raw": raw,
            "optimizer": optimizer,
            "conversationally": conversationally,
        }

        # tgpt-based providers
        for provider_name, provider_obj in async_provider_map.items():
            if provider_name in self.exclude:
                continue
            try:
                self.provider_name = f"tgpt-{provider_name}"
                self.provider = provider_obj(
                    is_conversation=self.is_conversation,
                    max_tokens=self.max_tokens,
                    timeout=self.timeout,
                    intro=self.intro,
                    filepath=self.filepath,
                    update_file=self.update_file,
                    proxies=self.proxies,
                    history_offset=self.history_offset,
                    act=self.act,
                )

                async def for_stream():
                    async_ask = await self.provider.ask(**ask_kwargs)
                    async for chunk in async_ask:
                        yield chunk

                async def for_non_stream():
                    return await self.provider.ask(**ask_kwargs)

                return for_stream() if stream else await for_non_stream()

            except Exception as e:
                logging.debug(
                    f"Failed to generate response using provider {provider_name} - {e}"
                )

        # g4f-based providers

        for provider_info in TestProviders(timeout=self.timeout).get_results(
            run=run_new_test
        ):
            if provider_info["name"] in self.exclude:
                continue
            try:
                self.provider_name = f"g4f-{provider_info['name']}"
                self.provider = AsyncGPT4FREE(
                    provider=provider_info["name"],
                    is_conversation=self.is_conversation,
                    max_tokens=self.max_tokens,
                    intro=self.intro,
                    filepath=self.filepath,
                    update_file=self.update_file,
                    proxies=self.proxies,
                    history_offset=self.history_offset,
                    act=self.act,
                )

                async def for_stream():
                    async_ask = await self.provider.ask(**ask_kwargs)
                    async for chunk in async_ask:
                        yield chunk

                async def for_non_stream():
                    return await self.provider.ask(**ask_kwargs)

                return for_stream() if stream else await for_non_stream()

            except Exception as e:
                logging.debug(
                    f"Failed to generate response using GPT4FREE-base provider {provider_name} - {e}"
                )

        raise AllProvidersFailure(
            "None of the providers generated response successfully."
        )

    async def chat(
        self,
        prompt: str,
        stream: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
        run_new_test: bool = False,
    ) -> str | AsyncGenerator:
        """Generate response `str` asynchronously.
        Args:
            prompt (str): Prompt to be send.
            stream (bool, optional): Flag for streaming response. Defaults to False.
            optimizer (str, optional): Prompt optimizer name - `[code, shell_command]`. Defaults to None.
            conversationally (bool, optional): Chat conversationally when using optimizer. Defaults to False.
            run_new_test (bool, optional): Perform new test on g4f-based providers. Defaults to False.
        Returns:
            str|AsyncGenerator: Response generated
        """

        async def for_stream():
            async_ask = await self.ask(
                prompt,
                True,
                optimizer=optimizer,
                conversationally=conversationally,
                run_new_test=run_new_test,
            )
            async for response in async_ask:
                yield await self.get_message(response)

        async def for_non_stream():
            ask_response = await self.ask(
                prompt,
                False,
                optimizer=optimizer,
                conversationally=conversationally,
                run_new_test=run_new_test,
            )
            return await self.get_message(ask_response)

        return for_stream() if stream else await for_non_stream()

    async def get_message(self, response: dict) -> str:
        """Retrieves message only from response

        Args:
            response (dict): Response generated by `self.ask`

        Returns:
            str: Message extracted
        """
        assert self.provider is not None, "Chat with AI first"
        return await self.provider.get_message(response)


if __name__ == "__main__":
    import asyncio

    async def main():
        ai = AsyncAUTO()
        async_chat = await ai.chat("hello there", True)
        async for response in async_chat:
            print(response)

    asyncio.run(main())
