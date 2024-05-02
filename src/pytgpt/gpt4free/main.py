from pytgpt.utils import Optimizers
from pytgpt.utils import Conversation
from pytgpt.utils import AwesomePrompts
from pytgpt.base import Provider, AsyncProvider
from pytgpt import available_providers
import g4f
import pytgpt.exceptions as exceptions
from typing import AsyncGenerator

g4f.debug.version_check = False

working_providers = available_providers

completion_allowed_models = [
    "code-davinci-002",
    "text-ada-001",
    "text-babbage-001",
    "text-curie-001",
    "text-davinci-002",
    "text-davinci-003",
]

default_models = {
    "completion": "text-davinci-003",
    "chat_completion": "gpt-3.5-turbo",
}

default_provider = "Koala"


class GPT4FREE(Provider):
    def __init__(
        self,
        provider: str = default_provider,
        is_conversation: bool = True,
        auth: str = None,
        max_tokens: int = 600,
        model: str = None,
        chat_completion: bool = False,
        ignore_working: bool = False,
        timeout: int = 30,
        intro: str = None,
        filepath: str = None,
        update_file: bool = True,
        proxies: dict = {},
        history_offset: int = 10250,
        act: str = None,
    ):
        """Initialies GPT4FREE

        Args:
            provider (str, optional): gpt4free based provider name. Defaults to Koala.
            is_conversation (bool, optional): Flag for chatting conversationally. Defaults to True.
            auth (str, optional): Authentication value for the provider incase it needs. Defaults to None.
            max_tokens (int, optional): Maximum number of tokens to be generated upon completion. Defaults to 600.
            model (str, optional): LLM model name. Defaults to text-davinci-003|gpt-3.5-turbo.
            chat_completion(bool, optional): Provide native auto-contexting (conversationally). Defaults to False.
            ignore_working (bool, optional): Ignore working status of the provider. Defaults to False.
            timeout (int, optional): Http request timeout. Defaults to 30.
            intro (str, optional): Conversation introductory prompt. Defaults to None.
            filepath (str, optional): Path to file containing conversation history. Defaults to None.
            update_file (bool, optional): Add new prompts and responses to the file. Defaults to True.
            proxies (dict, optional): Http request proxies. Defaults to {}.
            history_offset (int, optional): Limit conversation history to this number of last texts. Defaults to 10250.
            act (str|int, optional): Awesome prompt key or index. (Used as intro). Defaults to None.
        """
        assert provider in available_providers, (
            f"Provider '{provider}' is not yet supported. "
            f"Try others like {', '.join(available_providers)}"
        )
        if model is None:
            model = (
                default_models["chat_completion"]
                if chat_completion
                else default_models["completion"]
            )

        elif not chat_completion:
            assert model in completion_allowed_models, (
                f"Model '{model}' is not yet supported for completion. "
                f"Try other models like {', '.join(completion_allowed_models)}"
            )
        self.is_conversation = is_conversation
        self.max_tokens_to_sample = max_tokens
        self.stream_chunk_size = 64
        self.timeout = timeout
        self.last_response = {}

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
            False if chat_completion else is_conversation,
            self.max_tokens_to_sample,
            filepath,
            update_file,
        )
        self.conversation.history_offset = history_offset
        self.model = model
        self.provider = provider
        self.chat_completion = chat_completion
        self.ignore_working = ignore_working
        self.auth = auth
        self.proxy = None if not proxies else list(proxies.values())[0]
        self.__chat_class = g4f.ChatCompletion if chat_completion else g4f.Completion

    def __str__(self):
        return f"GPTFREE(provider={self.provider})"

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
          "text" : "How may I help you today?"
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

        def payload():
            if self.chat_completion:
                return dict(
                    model=self.model,
                    provider=self.provider,  # g4f.Provider.Aichat,
                    messages=[{"role": "user", "content": conversation_prompt}],
                    stream=stream,
                    ignore_working=self.ignore_working,
                    auth=self.auth,
                    proxy=self.proxy,
                    timeout=self.timeout,
                )

            else:
                return dict(
                    model=self.model,
                    prompt=conversation_prompt,
                    provider=self.provider,
                    stream=stream,
                    ignore_working=self.ignore_working,
                    auth=self.auth,
                    proxy=self.proxy,
                    timeout=self.timeout,
                )

        def format_response(response):
            return dict(text=response)

        def for_stream():
            previous_chunks = ""
            response = self.__chat_class.create(**payload())

            for chunk in response:
                previous_chunks += chunk
                formatted_resp = format_response(previous_chunks)
                self.last_response.update(formatted_resp)
                yield previous_chunks if raw else formatted_resp

            self.conversation.update_chat_history(
                prompt,
                previous_chunks,
            )

        def for_non_stream():
            response = self.__chat_class.create(**payload())
            formatted_resp = format_response(response)

            self.last_response.update(formatted_resp)
            self.conversation.update_chat_history(prompt, response)

            return response if raw else formatted_resp

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
        return response["text"]


class AsyncGPT4FREE(AsyncProvider):
    def __init__(
        self,
        provider: str = default_provider,
        is_conversation: bool = True,
        auth: str = None,
        max_tokens: int = 600,
        model: str = None,
        ignore_working: bool = False,
        timeout: int = 30,
        intro: str = None,
        filepath: str = None,
        update_file: bool = True,
        proxies: dict = {},
        history_offset: int = 10250,
        act: str = None,
    ):
        """Initialies GPT4FREE

        Args:
            provider (str, optional): gpt4free based provider name. Defaults to Koala.
            is_conversation (bool, optional): Flag for chatting conversationally. Defaults to True.
            auth (str, optional): Authentication value for the provider incase it needs. Defaults to None.
            max_tokens (int, optional): Maximum number of tokens to be generated upon completion. Defaults to 600.
            model (str, optional): LLM model name. Defaults to text-davinci-003|gpt-3.5-turbo.
            ignore_working (bool, optional): Ignore working status of the provider. Defaults to False.
            timeout (int, optional): Http request timeout. Defaults to 30.
            intro (str, optional): Conversation introductory prompt. Defaults to None.
            filepath (str, optional): Path to file containing conversation history. Defaults to None.
            update_file (bool, optional): Add new prompts and responses to the file. Defaults to True.
            proxies (dict, optional): Http request proxies. Defaults to {}.
            history_offset (int, optional): Limit conversation history to this number of last texts. Defaults to 10250.
            act (str|int, optional): Awesome prompt key or index. (Used as intro). Defaults to None.
        """
        assert provider in available_providers, (
            f"Provider '{provider}' is not yet supported. "
            f"Try others like {', '.join(available_providers)}"
        )
        if model is None:
            model = default_models["chat_completion"]

        self.is_conversation = is_conversation
        self.max_tokens_to_sample = max_tokens
        self.stream_chunk_size = 64
        self.timeout = timeout
        self.last_response = {}

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
            is_conversation,
            self.max_tokens_to_sample,
            filepath,
            update_file,
        )
        self.conversation.history_offset = history_offset
        self.model = model
        self.provider = provider
        self.ignore_working = ignore_working
        self.auth = auth
        self.proxy = None if not proxies else list(proxies.values())[0]

    def __str__(self):
        return f"AsyncGPTFREE(provider={self.provider})"

    async def ask(
        self,
        prompt: str,
        stream: bool = False,
        raw: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
    ) -> dict | AsyncGenerator:
        """Chat with AI asynchronously.

        Args:
            prompt (str): Prompt to be send.
            stream (bool, optional): Flag for streaming response. Defaults to False.
            raw (bool, optional): Stream back raw response as received. Defaults to False.
            optimizer (str, optional): Prompt optimizer name - `[code, shell_command]`. Defaults to None.
            conversationally (bool, optional): Chat conversationally when using optimizer. Defaults to False.
        Returns:
           dict|AsyncGenerator : ai content
        ```json
        {
          "text" : "How may I help you today?"
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

        payload = dict(
            model=self.model,
            provider=self.provider,  # g4f.Provider.Aichat,
            messages=[{"role": "user", "content": conversation_prompt}],
            stream=True,
            ignore_working=self.ignore_working,
            auth=self.auth,
            proxy=self.proxy,
            timeout=self.timeout,
        )

        async def format_response(response):
            return dict(text=response)

        async def for_stream():
            previous_chunks = ""
            response = g4f.ChatCompletion.create_async(**payload)

            async for chunk in response:
                previous_chunks += chunk
                formatted_resp = await format_response(previous_chunks)
                self.last_response.update(formatted_resp)
                yield previous_chunks if raw else formatted_resp

            self.conversation.update_chat_history(
                prompt,
                previous_chunks,
            )

        async def for_non_stream():
            async for _ in for_stream():
                pass
            return self.last_response

        return for_stream() if stream else await for_non_stream()

    async def chat(
        self,
        prompt: str,
        stream: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
    ) -> dict | AsyncGenerator:
        """Generate response `str` asynchronously.
        Args:
            prompt (str): Prompt to be send.
            stream (bool, optional): Flag for streaming response. Defaults to False.
            optimizer (str, optional): Prompt optimizer name - `[code, shell_command]`. Defaults to None.
            conversationally (bool, optional): Chat conversationally when using optimizer. Defaults to False.
        Returns:
            str|AsyncGenerator: Response generated
        """

        async def for_stream():
            async_ask = await self.ask(
                prompt, True, optimizer=optimizer, conversationally=conversationally
            )
            async for response in async_ask:
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
        return response["text"]


if __name__ == "__main__":
    bot = GPT4FREE()

    def main():
        resp = bot.ask("hello")
        for value in resp:
            print(value)

    async def asyncmain():
        bot = AsyncGPT4FREE("Blackbox")
        print(type(await bot.ask("hello", True)))
        exit()
        while True:
            resp = await bot.chat(input(">>"), False)
            print(resp)
            # async for value in resp:
            #    print(value)

    # main()
    import asyncio

    asyncio.run(asyncmain())
