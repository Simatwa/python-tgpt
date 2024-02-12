from WebChatGPT import ChatGPT
from WebChatGPT.utils import get_message
from pytgpt.base import Provider
from pytgpt.utils import Conversation
from pytgpt.utils import Optimizers
from pytgpt.utils import AwesomePrompts

default_model = "text-davinci-002-render-sha"


class WEBCHATGPT(Provider):
    def __init__(
        self,
        cookie_file: str,
        model: str = default_model,
        proxy: dict = {},
        timeout: int = 30,
        filepath: str = None,
        update_file: str = True,
        intro: str = None,
        act: str = None,
    ):
        """Initializes WEBCHATGPT

        Args:
            cookie_file (str): Path to `chat.openai.com.cookies.json` file
            model (str, optional): Modl name. Default to text-davinci-002-render-sha.
            proxy (dict, optional): Http request proxy. Defaults to {}.
            timeout (int, optional): Http request timeout. Defaults to 30.
            filepath (str, optional): Path to save the chat history. Defaults to None.
            update_file (str, optional): Flag for controlling chat history updates. Defaults to True.
            intro (str, optional): Conversation introductory prompt. Defaults to None.
            act (str|int, optional): Awesome prompt key or index. (Used as intro). Defaults to None.
        """
        self.session = ChatGPT(cookie_path=cookie_file, model=model, timeout=timeout)
        self.session.session.proxies = proxy
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
            status=False, filepath=filepath, update_file=update_file
        )

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
                optimizer (str, optional): Prompt optimizer name - `[code, shell_command]`. Defeaults to None
                conversationally (bool, optional): Chat conversationally when using optimizer. Defaults to False.
            Returns:
               dict : {}
        ```json
        {
            "message": {
                "id": "2c98d9ff-495c-4f08-af9e-affbd17xxxxx",
                "author": {
                    "role": "assistant",
                    "name": null,
                    "metadata": {}
                },
                "create_time": 1702666802.823688,
                "update_time": null,
                "content": {
                    "content_type": "text",
                    "parts": [
                        "Of course, your privacy matters! I don't store or remember our conversations once they're completed, so your information is kept confidential. If there's anything specific you'd like to discuss or if you have any concerns, feel free to let me know. I'm here to assist you!"
                    ]
                },
                "status": "finished_successfully",
                "end_turn": true,
                "weight": 1.0,
                "metadata": {
                    "finish_details": {
                        "type": "stop",
                        "stop_tokens": [
                            100260
                        ]
                    },
                    "inline_gizmo_id": null,
                    "is_complete": true,
                    "message_type": "next",
                    "model_slug": "text-davinci-002-render-sha",
                    "parent_id": "7bf27013-a47a-438c-ae17-0ee846b4xxxx",
                    "timestamp_": "absolute"
                },
                "recipient": "all"
            },
            "conversation_id": "affdda8c-588c-4342-9869-26c5bd7xxxxx",
            "error": null
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

        def for_stream():
            for response in self.session.ask(prompt, stream=True, raw_response=raw):
                if raw:
                    yield response
                else:
                    self.last_response.update(response)
                    yield response

            self.conversation.update_chat_history(
                prompt,
                self.get_message(self.last_response),
                force=True,
            )

        def for_non_stream():
            # let's make use of stream
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
        return get_message(response)
