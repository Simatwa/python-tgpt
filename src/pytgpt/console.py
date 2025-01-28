import pytgpt
import click
import cmd
import logging
import os
import sys
import clipman
import re
import rich
import getpass
import json
import datetime
import time
import subprocess
from threading import Thread as thr
from functools import wraps

# rich

from rich.panel import Panel
from rich.style import Style
from rich.markdown import Markdown
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import Progress

from typing import Iterable

# pytgpt

from pytgpt.utils import Optimizers
from pytgpt.utils import default_path
from pytgpt.utils import AwesomePrompts
from pytgpt.utils import RawDog
from pytgpt.imager import Imager
from pytgpt.imager import Prodia
from pytgpt.utils import Audio
from pytgpt.utils import suggest_query

# colorama
from colorama import Fore
from colorama import init as init_colorama

from dotenv import load_dotenv

# prompt-toolkit
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import ThreadedCompleter, Completer, Completion
from prompt_toolkit.document import Document

init_colorama(autoreset=True)

load_dotenv()  # loads .env variables

logging.basicConfig(
    format="%(asctime)s - %(levelname)s : %(message)s ",  # [%(module)s,%(lineno)s]", # for debug purposes
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

try:
    clipman.init()
except Exception as e:
    logging.debug(f"Dropping clipman in favor of pyperclip - {(e)}")
    import pyperclip

    clipman.set = pyperclip.copy
    clipman.get = pyperclip.paste


class this:
    """Console's common variables"""

    rich_code_themes = ["monokai", "paraiso-dark", "igor", "vs", "fruity", "xcode"]

    default_provider = "auto"

    getExc = lambda e: e.args[1] if len(e.args) > 1 else str(e)

    context_settings = dict(auto_envvar_prefix="PYTGPT")

    image_providers_map: dict[str, object] = {"default": Imager, "prodia": Prodia}

    talk_to_me_voice = "en-US-Wavenet-C"

    """Console utils"""

    @staticmethod
    def run_system_command(
        command: str, exit_on_error: bool = True, stdout_error: bool = True
    ):
        """Run commands against system
        Args:
            command (str): shell command
            exit_on_error (bool, optional): Exit on error. Defaults to True.
            stdout_error (bool, optional): Print out the error. Defaults to True.

        Returns:
            tuple : (is_successfull, object[Exception|Subprocess.run])
        """
        try:
            # Run the command and capture the output
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            return (True, result)
        except subprocess.CalledProcessError as e:
            # Handle error if the command returns a non-zero exit code
            if stdout_error:
                click.secho(f"Error Occurred: while running '{command}'", fg="yellow")
                click.secho(e.stderr, fg="red")
            sys.exit(e.returncode) if exit_on_error else None
            return (False, e)

    def g4f_providers_in_dict(
        url=True,
        working=True,
        stream=False,
        context=False,
        gpt35=False,
        gpt4=False,
        selenium=False,
    ):
        from pytgpt import g4f
        import g4f.Provider.selenium as selenium_based

        selenium_based_providers: list = dir(selenium_based)
        hunted_providers = []
        required_attrs = (
            "url",
            "working",
            "supports_gpt_35_turbo",
            "supports_gpt_4",
            "supports_stream",
            "supports_message_history",
        )

        def sanitize_provider(provider: object):
            for attr in required_attrs:
                if not hasattr(provider, attr):
                    setattr(provider, attr, False)

            return provider

        for provider_name, provider_class in g4f.Provider.__map__.items():
            provider = sanitize_provider(provider_class)
            provider_meta = dict(name=provider_name)
            if url:
                provider_meta["url"] = provider.url
            if working:
                provider_meta["working"] = provider.working
            if stream:
                provider_meta["stream"] = provider.supports_stream
            if context:
                provider_meta["context"] = provider.supports_message_history
            if gpt35:
                provider_meta["gpt35_turbo"] = provider.supports_gpt_35_turbo
            if gpt4:
                provider_meta["gpt4"] = provider.supports_gpt_4
            if selenium:
                try:
                    selenium_based_providers.index(provider_meta["name"])
                    value = True
                except ValueError:
                    value = False
                provider_meta["non_selenium"] = value

            hunted_providers.append(provider_meta)

        return hunted_providers

    @staticmethod
    def stream_output(
        iterable: Iterable,
        title: str = "",
        is_markdown: bool = True,
        style: object = Style(),
        transient: bool = False,
        title_generator: object = None,
        title_generator_params: dict = {},
        code_theme: str = "monokai",
        vertical_overflow: str = "ellipsis",
    ) -> None:
        """Stdout streaming response

        Args:
           iterable (Iterable): Iterable containing contents to be stdout
           title (str, optional): Content title. Defaults to ''.
           is_markdown (bool, optional): Flag for markdown content. Defaults to True.
           style (object, optional): `rich.style` instance. Defaults to Style().
           transient (bool, optional): Flag for transient. Defaults to False.
           title_generator (object, optional): Function for generating title. Defaults to None.
           title_generator_params (dict, optional): Kwargs for `title_generator` function. Defaults to {}.
           code_theme (str, optional): Theme for styling codes. Defaults to `monokai`
           vertical_overflow (str, optional): Vertical overflow behaviour on content display. Defaultss to ellipsis.
        """
        render_this = ""
        with Live(
            render_this,
            transient=transient,
            refresh_per_second=8,
            vertical_overflow=vertical_overflow,
        ) as live:
            for entry in iterable:
                render_this += entry
                live.update(
                    Panel(
                        (
                            Markdown(entry, code_theme=code_theme)
                            if is_markdown
                            else entry
                        ),
                        title=title,
                        style=style,
                    )
                )
        if title_generator:
            title = title_generator(**title_generator_params)
            live.update(
                Panel(
                    Markdown(entry, code_theme=code_theme) if is_markdown else entry,
                    title=title,
                    style=style,
                )
            )

    @staticmethod
    def clear_history_file(file_path, is_true):
        """When --new flag is True"""
        if is_true and os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                logging.error(
                    f"Failed to clear previous chat history - {this.getExc(e)}"
                )

    @staticmethod
    def handle_exception(func):
        """Safely handles cli-based exceptions and exit status-codes"""

        @wraps(func)
        def decorator(*args, **kwargs):
            try:
                exit_status = func(*args, **kwargs)
            except Exception as e:
                exit_status = False
                logging.error(this.getExc(e))
            finally:
                sys.exit(0 if exit_status not in (False, "") else 1)

        return decorator


class busy_bar:
    querying = None
    __spinner = (
        (),
        ("-", "\\", "|", "/"),
        (
            "█■■■■",
            "■█■■■",
            "■■█■■",
            "■■■█■",
            "■■■■█",
        ),
        ("⣾ ", "⣽ ", "⣻ ", "⢿ ", "⡿ ", "⣟ ", "⣯ ", "⣷ "),
    )
    spin_index = 0
    sleep_time = 0.1

    @classmethod
    def __action(
        cls,
    ):
        while cls.querying:
            for spin in cls.__spinner[cls.spin_index]:
                print(" " + spin, end="\r", flush=True)
                if not cls.querying:
                    break
                time.sleep(cls.sleep_time)

    @classmethod
    def start_spinning(
        cls,
    ):
        try:
            cls.querying = True
            t1 = thr(
                target=cls.__action,
                args=(),
            )
            t1.start()
        except Exception as e:
            cls.querying = False
            logging.debug(this.getExc(e))
            t1.join()

    @classmethod
    def stop_spinning(cls):
        """Stop displaying busy-bar"""
        if cls.querying:
            cls.querying = False
            time.sleep(cls.sleep_time)

    @classmethod
    def run(cls, help: str = "Exception", index: int = None, immediate: bool = False):
        """Handle function exceptions safely why showing busy bar

        Args:
            help (str, optional): Message to be shown incase of an exception. Defaults to ''.
            index (int, optional): Busy bars spin index. Defaults to `default`.
            immediate (bool, optional): Start the spinning immediately. Defaults to False.
        """
        if isinstance(index, int):
            cls.spin_index = index

        def decorator(func):
            @wraps(func)  # Preserves function metadata
            def main(*args, **kwargs):
                try:
                    if immediate:
                        cls.start_spinning()
                    return func(*args, **kwargs)
                except KeyboardInterrupt:
                    cls.stop_spinning()
                    return
                except EOFError:
                    cls.querying = False
                    sys.exit(logging.info("Stopping program"))
                except Exception as e:
                    logging.error(f"{help} - {this.getExc(e)}")
                finally:
                    cls.stop_spinning()

            return main

        return decorator


class CustomCompleter(Completer):
    """Suggests query based on user prompts"""

    def __init__(
        self,
        caller: object,
        suggestions_limit: int = 15,
        special_commands: list[str] = [],
    ):
        self.suggestions_limit = suggestions_limit
        self.caller = caller
        self.special_commands = special_commands

    def get_completions(self, document: Document, complete_event):
        word = document.text
        if word and self.suggestions_limit > 0 and not word.startswith("./"):
            completions = []
            first_word = word.strip().split(" ")[0]
            if first_word in self.special_commands:
                completions.append(
                    Completion(
                        f"{first_word} [RESERVED] "
                        + getattr(self.caller, f"do_{first_word}").__doc__
                    )
                )
                return completions
            for count, suggestion in enumerate(
                suggest_query(word, timeout=2, die_silently=True), start=1
            ):
                completions.append(Completion(suggestion, start_position=-len(word)))
                if count >= self.suggestions_limit:
                    break
            return completions
        return []


class Main(cmd.Cmd):
    intro = (
        "Welcome to AI Chat in terminal. "
        "Type 'help' or 'h' for usage info.\n"
        f"Submit any bug at {pytgpt.__repo__}/issues/new/choose"
    )

    def __init__(
        self,
        max_tokens,
        temperature,
        top_k,
        top_p,
        model,
        auth,
        timeout,
        disable_conversation,
        filepath,
        update_file,
        intro,
        history_offset,
        awesome_prompt,
        proxy_path,
        provider,
        quiet=False,
        chat_completion=False,
        ignore_working=False,
        rawdog=False,
        internal_exec=False,
        confirm_script=False,
        interpreter="python",
        suggestions_limit=15,
        non_interactive=False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if proxy_path:
            with open(proxy_path) as fh:
                proxies = json.load(fh)
        else:
            proxies = {}

        try:
            getOr = lambda option, default: option if option else default

            if rawdog:

                self.RawDog = RawDog(
                    quiet=quiet,
                    internal_exec=internal_exec,
                    confirm_script=confirm_script,
                    interpreter=interpreter,
                    prettify=True,
                )
                intro = self.RawDog.intro_prompt
                getpass.getuser = lambda: "RawDog"

            if provider == "auto":
                from pytgpt.auto import AUTO

                self.bot = AUTO(
                    is_conversation=disable_conversation,
                    max_tokens=max_tokens,
                    timeout=timeout,
                    intro=intro,
                    filepath=filepath,
                    update_file=update_file,
                    proxies=proxies,
                    history_offset=history_offset,
                    act=awesome_prompt,
                )

            elif provider == "g4fauto":
                from pytgpt.gpt4free.utils import TestProviders

                test = TestProviders(quiet=quiet, timeout=timeout)
                g4fauto = test.best if ignore_working else test.auto
                if isinstance(g4fauto, str):
                    provider = "g4f-" + g4fauto
                    from pytgpt.gpt4free import GPT4FREE

                    self.bot = GPT4FREE(
                        provider=g4fauto,
                        auth=auth,
                        max_tokens=max_tokens,
                        model=model,
                        chat_completion=chat_completion,
                        ignore_working=ignore_working,
                        timeout=timeout,
                        intro=intro,
                        filepath=filepath,
                        update_file=update_file,
                        proxies=proxies,
                        history_offset=history_offset,
                        act=awesome_prompt,
                    )
                else:
                    raise Exception(
                        "No working g4f provider found. "
                        "Consider running 'pytgpt gpt4free test -y' first"
                    )

            elif provider == "openai":
                assert auth, (
                    "OpenAI's API-key is required. " "Use the flag `--key` or `-k`"
                )
                from pytgpt.openai import main

                self.bot = main.OPENAI(
                    api_key=auth,
                    is_conversation=disable_conversation,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    presence_penalty=top_p,
                    frequency_penalty=top_k,
                    top_p=top_p,
                    model=getOr(model, main.model),
                    timeout=timeout,
                    intro=intro,
                    filepath=filepath,
                    update_file=update_file,
                    proxies=proxies,
                    history_offset=history_offset,
                    act=awesome_prompt,
                )

            elif provider == "koboldai":
                from pytgpt.koboldai import KOBOLDAI

                self.bot = KOBOLDAI(
                    is_conversation=disable_conversation,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    timeout=timeout,
                    intro=intro,
                    filepath=filepath,
                    update_file=update_file,
                    proxies=proxies,
                    history_offset=history_offset,
                    act=awesome_prompt,
                )

            elif provider == "phind":
                import pytgpt.phind.main as phind

                self.bot = phind.PHIND(
                    is_conversation=disable_conversation,
                    max_tokens=max_tokens,
                    timeout=timeout,
                    intro=intro,
                    filepath=filepath,
                    update_file=update_file,
                    proxies=proxies,
                    history_offset=history_offset,
                    act=awesome_prompt,
                    model=getOr(model, phind.default_model),
                    quiet=quiet,
                )

            elif provider == "blackboxai":

                from pytgpt.blackboxai import BLACKBOXAI

                self.bot = BLACKBOXAI(
                    is_conversation=disable_conversation,
                    max_tokens=max_tokens,
                    timeout=timeout,
                    intro=intro,
                    filepath=filepath,
                    update_file=update_file,
                    proxies=proxies,
                    history_offset=history_offset,
                    act=awesome_prompt,
                )

            elif provider == "gpt4all":
                assert auth, (
                    "Path to LLM (.gguf or .bin) file is required. "
                    "Download models from <https://gpt4all.io>. "
                    "Use the flag `--key` or `-k`"
                )

                from pytgpt.gpt4all import GPT4ALL

                self.bot = GPT4ALL(
                    model=auth,
                    is_conversation=disable_conversation,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    presence_penalty=top_p,
                    frequency_penalty=top_k,
                    top_p=top_p,
                    intro=intro,
                    filepath=filepath,
                    update_file=update_file,
                    history_offset=history_offset,
                    act=awesome_prompt,
                )

            elif provider == "poe":
                assert auth, (
                    "Path to poe.com.cookies.json file or 'p-b' cookie-value is required. "
                    "Use the flag `--key` or `-k`"
                )
                from pytgpt.poe import POE, default_model

                self.bot = POE(
                    cookie=auth,
                    model=getOr(model, default_model),
                    proxy=bool(proxies),
                    timeout=timeout,
                    filepath=filepath,
                    update_file=update_file,
                    intro=intro,
                    act=awesome_prompt,
                )

            elif provider in pytgpt.gpt4free_providers:
                from pytgpt.gpt4free import GPT4FREE

                self.bot = GPT4FREE(
                    provider=provider,
                    is_conversation=disable_conversation,
                    auth=auth,
                    max_tokens=max_tokens,
                    model=model,
                    chat_completion=chat_completion,
                    ignore_working=ignore_working,
                    timeout=timeout,
                    intro=intro,
                    filepath=filepath,
                    update_file=update_file,
                    proxies=proxies,
                    history_offset=history_offset,
                    act=awesome_prompt,
                )

            elif provider == "groq":
                assert auth, (
                    "GROQ's API-key is required. " "Use the flag `--key` or `-k`"
                )
                from pytgpt.groq import main

                self.bot = main.GROQ(
                    api_key=auth,
                    is_conversation=disable_conversation,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    presence_penalty=top_p,
                    frequency_penalty=top_k,
                    top_p=top_p,
                    model=getOr(model, main.model),
                    timeout=timeout,
                    intro=intro,
                    filepath=filepath,
                    update_file=update_file,
                    proxies=proxies,
                    history_offset=history_offset,
                    act=awesome_prompt,
                )

            elif provider == "perplexity":
                from pytgpt.perplexity import PERPLEXITY

                self.bot = PERPLEXITY(
                    is_conversation=disable_conversation,
                    max_tokens=max_tokens,
                    timeout=timeout,
                    intro=intro,
                    filepath=filepath,
                    update_file=update_file,
                    proxies=proxies,
                    history_offset=history_offset,
                    act=awesome_prompt,
                    quiet=quiet,
                )

            elif provider == "novita":
                assert auth, (
                    "Novita's API-key is required. " "Use the flag `--key` or `-k`"
                )
                from pytgpt.novita import main

                self.bot = main.NOVITA(
                    api_key=auth,
                    is_conversation=disable_conversation,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    presence_penalty=top_p,
                    frequency_penalty=top_k,
                    top_p=top_p,
                    model=getOr(model, main.model),
                    timeout=timeout,
                    intro=intro,
                    filepath=filepath,
                    update_file=update_file,
                    proxies=proxies,
                    history_offset=history_offset,
                    act=awesome_prompt,
                )
            elif provider == "ai4chat":
                from pytgpt.ai4chat import main

                self.bot = main.AI4CHAT(
                    is_conversation=disable_conversation,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    presence_penalty=top_p,
                    frequency_penalty=top_k,
                    top_p=top_p,
                    model=getOr(model, main.model),
                    timeout=timeout,
                    intro=intro,
                    filepath=filepath,
                    update_file=update_file,
                    proxies=proxies,
                    history_offset=history_offset,
                    act=awesome_prompt,
                )

            elif provider == "deepseek":
                assert auth, (
                    "DeepSeek's API-key is required. " "Use the flag `--key` or `-k`"
                )
                from pytgpt.deepseek import main

                self.bot = main.DEEPSEEK(
                    api_key=auth,
                    is_conversation=disable_conversation,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    presence_penalty=top_p,
                    frequency_penalty=top_k,
                    top_p=top_p,
                    model=getOr(model, main.model),
                    timeout=timeout,
                    intro=intro,
                    filepath=filepath,
                    update_file=update_file,
                    proxies=proxies,
                    history_offset=history_offset,
                    act=awesome_prompt,
                )

            else:
                raise NotImplementedError(
                    f"The provider `{provider}` is not yet implemented."
                )

        except Exception as e:
            logging.error(this.getExc(e))
            click.secho("Quitting", fg="red")
            sys.exit(1)
        self.prettify = True
        self.color = "cyan"
        self.code_theme = "monokai"
        self.quiet = quiet
        self.vertical_overflow = "ellipsis"
        self.disable_stream = False
        self.provider = provider
        self.disable_coloring = False
        self.internal_exec = internal_exec
        self.confirm_script = confirm_script
        self.interpreter = interpreter
        self.rawdog = rawdog
        self.read_aloud = False
        self.read_aloud_voice = "Brian"
        self.path_to_last_response_audio = None
        if not non_interactive:
            self.completer_session = PromptSession(
                "",
                completer=ThreadedCompleter(
                    CustomCompleter(
                        self,
                        suggestions_limit,
                        [
                            "cd",
                            "copy_this",
                            "h",
                            "last_response",
                            "rawdog",
                            "settings",
                            "with_copied",
                            "clear",
                            "exec",
                            "help",
                            "load",
                            "reread",
                            "shell",
                            "code",
                            "exit",
                            "history",
                            "new_intro",
                            "reset",
                            "sys",
                        ],
                    )
                ),
            )
        self.__init_time = time.time()
        self.__start_time = time.time()
        self.__end_time = time.time()

    @property
    def get_provider(self):
        if self.provider == "auto" and self.bot.provider_name is not None:
            return self.bot.provider_name
        else:
            return self.provider

    @property
    def prompt(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        def find_range(start, end, hms: bool = False):
            in_seconds = round(end - start, 1)
            return (
                str(datetime.timedelta(seconds=in_seconds)).split(".")[0].zfill(8)
                if hms
                else in_seconds
            )

        if not self.disable_coloring:
            cmd_prompt = (
                f"╭─[`{Fore.CYAN}{getpass.getuser().capitalize()}@pyTGPT]`"
                f"(`{Fore.MAGENTA}{self.get_provider})`"
                f"~[`{Fore.LIGHTWHITE_EX}🕒{Fore.BLUE}{current_time}-`"
                f"{Fore.LIGHTWHITE_EX}💻{Fore.RED}{find_range(self.__init_time, time.time(), True)}-`"
                f"{Fore.LIGHTWHITE_EX}⚡{Fore.YELLOW}{find_range(self.__start_time, self.__end_time)}s]`"
                # f"\n╰─>"
            )
            whitelist = ["[", "]", "~", "-", "(", ")"]
            for character in whitelist:
                cmd_prompt = cmd_prompt.replace(character + "`", Fore.RESET + character)
            return cmd_prompt

        else:
            return (
                f"╭─[{getpass.getuser().capitalize()}@pyTGPT]({self.get_provider})"
                f"~[🕒{current_time}"
                f"-💻{find_range(self.__init_time, time.time(), True)}"
                f"-⚡{find_range(self.__start_time, self.__end_time)}s]"
                # "\n╰─>"
            )

    def cmdloop(self, intro=None):
        """Repeatedly issue a prompt, accept input, parse an initial prefix
        off the received input, and dispatch to action methods, passing them
        the remainder of the line as argument.

        """

        self.preloop()
        if self.use_rawinput and self.completekey:
            try:
                import readline

                self.old_completer = readline.get_completer()
                readline.set_completer(self.complete)
                if hasattr(readline, "backend") and readline.backend == "editline":
                    if self.completekey == "tab":
                        # libedit uses "^I" instead of "tab"
                        command_string = "bind ^I rl_complete"
                    else:
                        command_string = f"bind {self.completekey} rl_complete"
                else:
                    command_string = f"{self.completekey}: complete"
                readline.parse_and_bind(command_string)
            except ImportError:
                pass
        try:
            if intro is not None:
                self.intro = intro
            if self.intro:
                self.stdout.write(str(self.intro) + "\n")
            stop = None
            while not stop:
                if self.cmdqueue:
                    line = self.cmdqueue.pop(0)
                else:
                    if self.use_rawinput:
                        try:
                            print(self.prompt, end="")
                            line = self.completer_session.prompt("\n╰─>")
                        except EOFError:
                            line = "EOF"
                    else:
                        self.stdout.write(self.prompt)
                        self.stdout.flush()
                        line = self.stdin.readline()
                        if not len(line):
                            line = "EOF"
                        else:
                            line = line.rstrip("\r\n")
                line = self.precmd(line)
                stop = self.onecmd(line)
                stop = self.postcmd(stop, line)
            self.postloop()
        finally:
            if self.use_rawinput and self.completekey:
                try:
                    import readline

                    readline.set_completer(self.old_completer)
                except ImportError:
                    pass

    def output_bond(
        self,
        title: str,
        text: str,
        color: str = "cyan",
        frame: bool = True,
        is_json: bool = False,
    ):
        """Print prettified output

        Args:
            title (str): Title
            text (str): Info to be printed
            color (str, optional): Output color. Defaults to "cyan".
            frame (bool, optional): Add frame. Defaults to True.
        """
        if is_json:
            text = f"""
```json
{json.dumps(text,indent=4)}
```
"""
        rich.print(
            Panel(
                Markdown(text, code_theme=self.code_theme),
                title=title.title(),
                style=Style(
                    color=color,
                    frame=frame,
                ),
            ),
        )
        if is_json and click.confirm("Do you wish to save this"):
            default_path = title + ".json"
            save_to = click.prompt(
                "Enter path to save to", default=default_path, type=click.STRING
            )
            with open(save_to, "a") as fh:
                json.dump(text, fh, indent=4)
            click.secho(f"Successfuly saved to `{save_to}`", fg="green")

    def do_h(self, line):
        """Show help info in tabular form"""
        table = Table(
            title="Help info",
            show_lines=True,
        )
        table.add_column("No.", style="white", justify="center")
        table.add_column("Command", style="yellow", justify="left")
        table.add_column("Function", style="cyan")
        command_methods = [
            getattr(self, method)
            for method in dir(self)
            if callable(getattr(self, method)) and method.startswith("do_")
        ]
        command_methods.append(self.default)
        command_methods.reverse()
        for no, method in enumerate(command_methods):
            table.add_row(
                str(no + 1),
                method.__name__[3:] if not method == self.default else method.__name__,
                method.__doc__,
            )
        Console().print(table)

    @busy_bar.run("Settings saved")
    def do_settings(self, line):
        """Configure settings"""
        self.prettify = click.confirm(
            "\nPrettify markdown response", default=self.prettify
        )
        busy_bar.spin_index = click.prompt(
            "Spin bar index [0: None, 1:/, 2:■█■■■, 3:⣻]",
            default=busy_bar.spin_index,
            type=click.IntRange(0, 3),
        )
        self.color = click.prompt(
            "Response stdout font color", default=self.color or "white"
        )
        self.code_theme = Prompt.ask(
            "Enter code_theme", choices=this.rich_code_themes, default=self.code_theme
        )
        self.vertical_overflow = Prompt.ask(
            "\nVertical overflow behaviour",
            choices=["ellipsis", "visible", "crop"],
            default=self.vertical_overflow,
        )
        self.bot.max_tokens_to_sample = click.prompt(
            "\nMaximum tokens to sample",
            type=click.INT,
            default=self.bot.max_tokens_to_sample,
        )
        self.bot.temperature = click.prompt(
            "Temperature", type=click.FLOAT, default=self.bot.temperature
        )
        self.bot.top_k = click.prompt(
            "Chance of topic being repeated, top_k",
            type=click.FLOAT,
            default=self.bot.top_k,
        )
        self.bot.top_p = click.prompt(
            "Sampling threshold during inference time, top_p",
            type=click.FLOAT,
            default=self.bot.top_p,
        )
        self.bot.model = click.prompt(
            "Model name", type=click.STRING, default=self.bot.model
        )

    @busy_bar.run(help="System error")
    def do_copy_this(self, line):
        """Copy last response
        Usage:
           copy_this:
               text-copied = {whole last-response}
           copy_this code:
               text-copied = {All codes in last response}
        """
        if self.bot.last_response:
            global last_response
            last_response = self.bot.get_message(self.bot.last_response)
            if not "code" in line:
                clipman.set(last_response)
                click.secho("Last response copied successfully!", fg="cyan")
                return

            # Copies just code
            sanitized_codes = []
            code_blocks = re.findall(r"```.*?```", last_response, re.DOTALL)
            for code_block in code_blocks:
                new_code_block = re.sub(
                    "^```.*$", "", code_block.strip(), flags=re.MULTILINE
                )
                if bool(new_code_block.strip()):
                    sanitized_codes.append(new_code_block)
            if sanitized_codes:
                if len(sanitized_codes) > 1:
                    if not click.confirm("Do you wish to copy all codes"):
                        for index, code in enumerate(sanitized_codes):
                            rich.print(
                                Panel(
                                    Markdown(
                                        code_blocks[index], code_theme=self.code_theme
                                    ),
                                    title=f"Index : {index}",
                                    title_align="left",
                                )
                            )

                        clipman.set(
                            sanitized_codes[
                                click.prompt(
                                    "Enter code index",
                                    type=click.IntRange(0, len(sanitized_codes) - 1),
                                )
                            ]
                        )
                        click.secho("Code copied successfully", fg="cyan")
                    else:
                        clipman.set("\n\n".join(sanitized_codes))
                        click.secho(
                            f"All {len(sanitized_codes)} codes copied successfully!",
                            fg="cyan",
                        )
                else:
                    clipman.set(sanitized_codes[0])
                    click.secho("Code copied successfully!", fg="cyan")
            else:
                click.secho("No code found in the last response!", fg="red")
        else:
            click.secho("Chat with AI first.", fg="yellow")

    @busy_bar.run()
    def do_with_copied(self, line):
        """Attach last copied text to the prompt
        Usage:
            from_copied:
                 prompt = {text-copied}
            from_copied Debug this code:
                 prompt = Debug this code {newline} {text-copied}
        """
        issued_prompt = (
            f"{line}\n{clipman.get()}" if bool(line.strip()) else clipman.get()
        )
        click.secho(issued_prompt, fg="yellow")
        if click.confirm("Do you wish to proceed"):
            self.default(issued_prompt)

    @busy_bar.run()
    def do_code(self, line):
        """Enhance prompt for code generation
        usage :
              code <Code description>
        """
        self.default(Optimizers.code(line))

    @busy_bar.run()
    def do_shell(self, line):
        """Enhance prompt for system command (shell) generation
        Usage:
             shell <Action to be accomplished>
        """
        self.default(Optimizers.shell_command(line))
        if click.confirm("Do you wish to run the command(s) generated in your system"):
            self.do_sys(self.bot.get_message(self.bot.last_response))

    @busy_bar.run("While changing directory")
    def do_cd(self, line):
        """Change directory
        Usage :
             cd <path-to-directory>
        """
        assert line, "File path is required"
        os.chdir(line)

    def do_clear(self, line):
        """Clear console"""
        sys.stdout.write("\u001b[2J\u001b[H")
        sys.stdout.flush()

    @busy_bar.run("While handling history")
    def do_history(self, line):
        """Show current conversation history"""
        history = self.bot.conversation.chat_history
        formatted_history = re.sub(
            "\nLLM :",
            "\n\n**LLM** :",
            re.sub("\nUser :", "\n\n**User** :", history),
        )
        self.output_bond("Chat History", formatted_history, self.color)
        if click.confirm("Do you wish to save this chat"):
            save_to = click.prompt(
                "Enter path/file-name", default=f"{self.provider}-chat.txt"
            )
            with open(save_to, "a") as fh:
                fh.write(history)
            click.secho(f"Conversation saved successfully to '{save_to}'", fg="cyan")

    @busy_bar.run("while resetting conversation")
    def do_reset(self, line):
        """Start new conversation thread"""
        self.bot.conversation.chat_history = click.prompt(
            "Introductory prompt", default=self.bot.conversation.intro
        )
        if hasattr(self.bot, "reset"):
            self.bot.reset()
        click.secho("Conversation reset successfully. New one created.", fg="cyan")

    @busy_bar.run("while loading conversation")
    def do_load(self, line):
        """Load conversation history from file"""
        history_file = click.prompt("Enter path to history path", default=line)
        if not os.path.isfile(history_file):
            click.secho(f"Path `{history_file}` does not exist!", fg="red")
            return
        with open(history_file) as fh:
            self.bot.conversation.chat_history = fh.read()
        click.secho("Conversation loaded successfully.", fg="cyan")

    def do_last_response(self, line):
        """Show whole last response in json format"""
        self.output_bond(
            "Last Response",
            self.bot.last_response,
            is_json=True,
        )

    @busy_bar.run(help="While rereading aloud", index=3, immediate=True)
    def do_reread(self, line):
        """Reread aloud last ai response"""
        if not self.path_to_last_response_audio:
            raise Exception("Path to last response audio is null")
        Audio.play(self.path_to_last_response_audio)

    @busy_bar.run()
    def do_exec(self, line):
        """Exec python code in last response with RawDog"""
        last_response = self.bot.get_message(self.bot.last_response)
        assert last_response, "Last response is null"
        assert "```python" in last_response, "Last response has no python code"
        if self.rawdog:
            self.RawDog.main(last_response)
        else:
            rawdog = RawDog(
                quiet=self.quiet,
                internal_exec=self.internal_exec,
                confirm_script=self.confirm_script,
                interpreter=self.interpreter,
                prettify=self.prettify,
            )
            rawdog.main(last_response)

    @busy_bar.run()
    def do_rawdog(self, line):
        """Repeat executing last rawdog's python code"""
        assert self.rawdog, "Session not in rawdog mode. Restart with --rawdog"
        self.default(self.bot.get_message(self.bot.last_response))

    @busy_bar.run()
    def do_new_intro(self, line):
        """Set new chat intro"""
        print("Current intro:")
        click.secho(f"{self.bot.conversation.intro}", fg="cyan")
        if not line:
            line = click.prompt("Enter new chat intro")
        self.bot.conversation.intro = line
        print("New chat intro set successfully:")
        click.secho(f"{line}", fg="green")

    @busy_bar.run()
    def default(self, line, exit_on_error: bool = False, normal_stdout: bool = False):
        """Chat with LLM"""
        if not bool(line):
            return
        if line.startswith("./"):
            os.system(line[2:])

        elif self.rawdog:
            self.__start_time = time.time()
            busy_bar.start_spinning()
            ai_response = self.bot.chat(line, stream=False)
            busy_bar.stop_spinning()
            is_feedback = self.RawDog.main(ai_response)
            if is_feedback:
                return self.default(is_feedback)
            self.__end_time = time.time()

        else:
            self.__start_time = time.time()
            try:

                def generate_response():
                    # Ensure response is yielded
                    def for_stream():
                        return self.bot.chat(line, stream=True)

                    def for_non_stream():
                        yield self.bot.chat(line, stream=False)

                    return for_non_stream() if self.disable_stream else for_stream()

                busy_bar.start_spinning()
                generated_response = generate_response()

                if normal_stdout or not self.prettify and not self.disable_stream:
                    # Resolves : https://github.com/Simatwa/python-tgpt/issues/42 & 43
                    cached_response: str = ""
                    if not normal_stdout:
                        busy_bar.stop_spinning()
                    for response in generated_response:
                        offset = len(cached_response)
                        print(response[offset:], end="")
                        cached_response = response
                    if not normal_stdout:
                        # Interactive prompt
                        print("")
                    return

                if self.quiet:
                    busy_bar.stop_spinning()
                    console_ = Console()
                    with Live(
                        console=console_,
                        refresh_per_second=16,
                        vertical_overflow=self.vertical_overflow,
                    ) as live:
                        for response in generated_response:
                            live.update(
                                Markdown(response, code_theme=self.code_theme)
                                if self.prettify
                                else response
                            )
                else:
                    busy_bar.stop_spinning()
                    this.stream_output(
                        generated_response,
                        title="AI Response",
                        is_markdown=self.prettify,
                        style=Style(
                            color=self.color,
                        ),
                        code_theme=self.code_theme,
                        vertical_overflow=self.vertical_overflow,
                    )
            except (KeyboardInterrupt, EOFError):
                busy_bar.stop_spinning()
                print("")
                return False  # Exit cmd

            except Exception as e:
                # logging.exception(e)
                busy_bar.stop_spinning()
                logging.error(this.getExc(e))
                if exit_on_error:
                    sys.exit(1)

            else:
                self.post_default()

            finally:
                self.__end_time = time.time()

    @busy_bar.run(help="While reading aloud", immediate=True, index=3)
    def post_default(self):
        """Actions to be taken after upon successfull complete response generation triggered by `default` function"""
        last_text: str = self.bot.get_message(self.bot.last_response)
        if self.read_aloud and last_text is not None:
            # Talk back to user
            self.path_to_last_response_audio = Audio.text_to_audio(
                last_text, voice=self.read_aloud_voice, auto=True
            )
            Audio.play(self.path_to_last_response_audio)

    def do_sys(self, line):
        """Execute system commands
        shortcut [./<command>]
        Usage:
            sys <System command>
                  or
             ./<System command>
        """
        os.system(line)

    def do_exit(self, line):
        """Quit this program"""
        if click.confirm("Are you sure to exit"):
            click.secho("^-^ Okay Goodbye!", fg="yellow")
            return True


class EntryGroup:
    """Entry commands"""

    # @staticmethod
    @click.group()
    @click.version_option(
        pytgpt.__version__, "-v", "--version", package_name="pytgpt", prog_name="pytgpt"
    )
    @click.help_option("-h", "--help")
    def tgpt2_():
        pass

    @staticmethod
    @tgpt2_.group()
    @click.help_option("-h", "--help")
    def utils():
        """Utility endpoint for pytgpt"""
        pass

    @staticmethod
    @tgpt2_.group()
    @click.help_option("-h", "--help")
    def gpt4free():
        """Discover gpt4free models, providers etc"""
        pass

    @staticmethod
    @tgpt2_.group()  # For awesome-prompts
    @click.help_option("-h", "--help")
    def awesome():
        """Perform CRUD operations on awesome-prompts"""
        pass

    @staticmethod
    @tgpt2_.group()
    @click.help_option("-h", "--help")
    def api():
        """FastAPI control endpoint"""
        pass

    @staticmethod
    @tgpt2_.group()
    @click.help_option("-h", "--help")
    def bot():
        """Telegram bot interface control"""
        pass


class ChatInteractive:
    """Interactive command"""

    @staticmethod
    @click.command(context_settings=this.context_settings)
    @click.option(
        "-m",
        "--model",
        help="Model name for text-generation",  # default="llama-2-13b-chat"
    )
    @click.option(
        "-t",
        "--temperature",
        help="Charge of the generated text's randomness",
        type=click.FloatRange(0, 1),
        default=0.2,
    )
    @click.option(
        "-mt",
        "--max-tokens",
        help="Maximum number of tokens to be generated upon completion",
        type=click.INT,
        default=600,
    )
    @click.option(
        "-tp",
        "--top-p",
        help="Sampling threshold during inference time",
        type=click.FLOAT,
        default=0.999,
    )
    @click.option(
        "-tk",
        "--top-k",
        help="Chance of topic being repeated",
        type=click.FLOAT,
        default=0,
    )
    @click.option(
        "-k",
        "--key",
        help="LLM API access key or auth value or path to LLM with provider.",
    )
    @click.option(
        "-ct",
        "--code-theme",
        help="Theme for displaying codes in response",
        type=click.Choice(this.rich_code_themes),
        default="monokai",
    )
    @click.option(
        "-bi",
        "--busy-bar-index",
        help="Index of busy bar icon : [0: None, 1:/, 2:■█■■■, 3:⣻]",
        type=click.IntRange(0, 3),
        default=3,
    )
    @click.option("-fc", "--font-color", help="Stdout font color")
    @click.option(
        "-to", "--timeout", help="Http requesting timeout", type=click.INT, default=30
    )
    @click.argument("prompt", required=False)
    @click.option(
        "--prettify/--raw",
        help="Flag for prettifying markdowned response",
        default=True,
    )
    @click.option(
        "-dc",
        "--disable-conversation",
        is_flag=True,
        default=True,  # is_conversation = True
        help="Disable chatting conversationally (Stable)",
    )
    @click.option(
        "-fp",
        "--filepath",
        type=click.Path(),
        default=os.path.join(default_path, "chat-history.txt"),
        help="Path to chat history - new will be created incase doesn't exist",
    )
    @click.option(
        "--update-file/--retain-file",
        help="Controls updating chat history in file",
        default=True,
    )
    @click.option(
        "-i",
        "--intro",
        help="Conversation introductory prompt",
    )
    @click.option(
        "-ho",
        "--history-offset",
        help="Limit conversation history to this number of last texts",
        type=click.IntRange(100, 16000),
        default=10250,
    )
    @click.option(
        "-ap",
        "--awesome-prompt",
        default="0",
        callback=lambda ctx, param, value: (
            int(value) if str(value).isdigit() else value
        ),
        help="Awesome prompt key or index. Alt. to intro",
    )
    @click.option(
        "-pp",
        "--proxy-path",
        type=click.Path(exists=True),
        help="Path to .json file containing proxies",
    )
    @click.option(
        "-p",
        "--provider",
        type=click.Choice(pytgpt.available_providers),
        default=this.default_provider,
        help="Name of LLM provider.",
        metavar=(
            f"[{'|'.join(pytgpt.tgpt_providers)}] etc, "
            "run 'pytgpt gpt4free list providers -w' to "
            "view more providers and 'pytgpt gpt4free test -y' "
            "for advanced g4f providers test"
        ),
    )
    @click.option(
        "-sl",
        "--suggestions-limit",
        type=click.INT,
        help="Prompt suggestions limit - 0 to disable suggestion",
        default=15,
    )
    @click.option(
        "-vo",
        "--vertical-overflow",
        help="Vertical overflow behaviour on content display",
        type=click.Choice(["visible", "crop", "ellipsis"]),
        default="ellipsis",
    )
    @click.option(
        "-w",
        "--whole",
        is_flag=True,
        default=False,
        help="Disable streaming response",
    )
    @click.option(
        "-q",
        "--quiet",
        is_flag=True,
        help="Flag for controlling response-framing and response verbosity",
        default=False,
    )
    @click.option(
        "-n",
        "--new",
        help="Overwrite the filepath contents",
        is_flag=True,
    )
    @click.option(
        "-wc",
        "--with-copied",
        is_flag=True,
        help="Postfix prompt with last copied text",
    )
    @click.option(
        "-nc", "--no-coloring", is_flag=True, help="Disable intro prompt font-coloring"
    )
    @click.option(
        "-cc",
        "--chat-completion",
        is_flag=True,
        help="Provide native context for gpt4free providers",
    )
    @click.option(
        "-iw",
        "--ignore-working",
        is_flag=True,
        help="Ignore working status of the provider",
    )
    @click.option(
        "-rd",
        "--rawdog",
        is_flag=True,
        help="Generate and auto-execute Python scripts - (experimental)",
    )
    @click.option(
        "-ix",
        "--internal-exec",
        is_flag=True,
        help="RawDog : Execute scripts with exec function instead of out-of-script interpreter",
    )
    @click.option(
        "-cs",
        "--confirm-script",
        is_flag=True,
        help="RawDog : Give consent to generated scripts prior to execution",
    )
    @click.option(
        "-int",
        "--interpreter",
        default="python",
        help="RawDog : Python's interpreter name",
    )
    @click.option(
        "-ttm",
        "--talk-to-me",
        is_flag=True,
        help="Audiolize responses upon complete generation",
    )
    @click.option(
        "-ttmv",
        "--talk-to-me-voice",
        help="The voice to use for speech synthesis",
        type=click.Choice(Audio.all_voices),
        metavar="|".join(Audio.all_voices[:8]),
        default=this.talk_to_me_voice,
    )
    @click.help_option("-h", "--help")
    def interactive(
        model,
        temperature,
        max_tokens,
        top_p,
        top_k,
        key,
        code_theme,
        busy_bar_index,
        font_color,
        timeout,
        prompt,
        prettify,
        disable_conversation,
        filepath,
        update_file,
        intro,
        history_offset,
        awesome_prompt,
        proxy_path,
        provider,
        suggestions_limit,
        vertical_overflow,
        whole,
        quiet,
        new,
        with_copied,
        no_coloring,
        chat_completion,
        ignore_working,
        rawdog,
        internal_exec,
        confirm_script,
        interpreter,
        talk_to_me,
        talk_to_me_voice,
    ):
        """Chat with AI interactively (Default)"""
        this.clear_history_file(filepath, new)
        bot = Main(
            max_tokens,
            temperature,
            top_k,
            top_p,
            model,
            key,
            timeout,
            disable_conversation,
            filepath,
            update_file,
            intro,
            history_offset,
            awesome_prompt,
            proxy_path,
            provider,
            quiet,
            chat_completion,
            ignore_working,
            rawdog=rawdog,
            internal_exec=internal_exec,
            confirm_script=confirm_script,
            interpreter=interpreter,
            suggestions_limit=suggestions_limit,
        )
        busy_bar.spin_index = busy_bar_index
        bot.code_theme = code_theme
        bot.color = font_color
        bot.disable_coloring = no_coloring
        bot.prettify = prettify
        bot.vertical_overflow = vertical_overflow
        bot.disable_stream = whole
        bot.read_aloud = talk_to_me
        bot.read_aloud_voice = talk_to_me_voice
        if prompt:
            if with_copied:
                prompt = prompt + "\n" + clipman.get()
            bot.default(prompt)
        bot.cmdloop()


class ChatGenerate:
    """Generate command"""

    @staticmethod
    @click.command(context_settings=this.context_settings)
    @click.option(
        "-m",
        "--model",
        help="Model name for text-generation",
    )
    @click.option(
        "-t",
        "--temperature",
        help="Charge of the generated text's randomness",
        type=click.FloatRange(0, 1),
        default=0.2,
    )
    @click.option(
        "-mt",
        "--max-tokens",
        help="Maximum number of tokens to be generated upon completion",
        type=click.INT,
        default=600,
    )
    @click.option(
        "-tp",
        "--top-p",
        help="Sampling threshold during inference time",
        type=click.FLOAT,
        default=0.999,
    )
    @click.option(
        "-tk",
        "--top-k",
        help="Chance of topic being repeated",
        type=click.FLOAT,
        default=0,
    )
    @click.option(
        "-k",
        "--key",
        help="LLM API access key or auth value or path to LLM with provider.",
    )
    @click.option(
        "-ct",
        "--code-theme",
        help="Theme for displaying codes in response",
        type=click.Choice(this.rich_code_themes),
        default="monokai",
    )
    @click.option(
        "-bi",
        "--busy-bar-index",
        help="Index of busy bar icon : [0: None, 1:/, 2:■█■■■, 3:⣻]",
        type=click.IntRange(0, 3),
        default=3,
    )
    @click.option(
        "-fc",
        "--font-color",
        help="Stdout font color",
    )
    @click.option(
        "-to", "--timeout", help="Http requesting timeout", type=click.INT, default=30
    )
    @click.argument("prompt", required=False)
    @click.option(
        "--prettify/--raw",
        help="Flag for prettifying markdowned response",
        default=True,
    )
    @click.option(
        "-w",
        "--whole",
        is_flag=True,
        default=False,
        help="Disable streaming response",
    )
    @click.option(
        "-c",
        "--code",
        is_flag=True,
        default=False,
        help="Optimize prompt for code generation",
    )
    @click.option(
        "-s",
        "--shell",
        is_flag=True,
        default=False,
        help="Optimize prompt for shell command generation",
    )
    @click.option(
        "-dc",
        "--disable-conversation",
        is_flag=True,
        default=True,  # is_conversation = True
        help="Disable chatting conversationally (Stable)",
    )
    @click.option(
        "-fp",
        "--filepath",
        type=click.Path(),
        default=os.path.join(default_path, "chat-history.txt"),
        help="Path to chat history - new will be created incase doesn't exist",
    )
    @click.option(
        "--update-file/--retain-file",
        help="Controls updating chat history in file",
        default=True,
    )
    @click.option(
        "-i",
        "--intro",
        help="Conversation introductory prompt",
    )
    @click.option(
        "-ho",
        "--history-offset",
        help="Limit conversation history to this number of last texts",
        type=click.IntRange(100, 16000),
        default=10250,
    )
    @click.option(
        "-ap",
        "--awesome-prompt",
        default="0",
        callback=lambda ctx, param, value: (
            int(value) if str(value).isdigit() else value
        ),
        help="Awesome prompt key or index. Alt. to intro",
    )
    @click.option(
        "-pp",
        "--proxy-path",
        type=click.Path(exists=True),
        help="Path to .json file containing proxies",
    )
    @click.option(
        "-p",
        "--provider",
        type=click.Choice(pytgpt.available_providers),
        default=this.default_provider,
        help="Name of LLM provider.",
        metavar=(
            f"[{'|'.join(pytgpt.tgpt_providers)}] etc, "
            "run 'pytgpt gpt4free list providers -w' to "
            "view more providers and 'pytgpt gpt4free test -y' "
            "for advanced g4f providers test"
        ),
    )
    @click.option(
        "-vo",
        "--vertical-overflow",
        help="Vertical overflow behaviour on content display",
        type=click.Choice(["visible", "crop", "ellipsis"]),
        default="ellipsis",
    )
    @click.option(
        "-q",
        "--quiet",
        is_flag=True,
        help="Flag for controlling response-framing and response verbosity",
        default=False,
    )
    @click.option(
        "-n",
        "--new",
        help="Override the filepath contents",
        is_flag=True,
    )
    @click.option(
        "-wc",
        "--with-copied",
        is_flag=True,
        help="Postfix prompt with last copied text",
    )
    @click.option(
        "-iw",
        "--ignore-working",
        is_flag=True,
        help="Ignore working status of the provider",
    )
    @click.option(
        "-rd",
        "--rawdog",
        is_flag=True,
        help="Generate and auto-execute Python scripts - (experimental)",
    )
    @click.option(
        "-ix",
        "--internal-exec",
        is_flag=True,
        help="RawDog : Execute scripts with exec function instead of out-of-script interpreter",
    )
    @click.option(
        "-cs",
        "--confirm-script",
        is_flag=True,
        help="RawDog : Give consent to generated scripts prior to execution",
    )
    @click.option(
        "-int",
        "--interpreter",
        default="python",
        help="RawDog : Python's interpreter name",
    )
    @click.option(
        "-ttm",
        "--talk-to-me",
        is_flag=True,
        help="Audiolize responses upon complete generation",
    )
    @click.option(
        "-ttmv",
        "--talk-to-me-voice",
        help="The voice to use for speech synthesis",
        type=click.Choice(Audio.all_voices),
        metavar="|".join(Audio.all_voices[:8]),
        default=this.talk_to_me_voice,
    )
    @click.help_option("-h", "--help")
    def generate(
        model,
        temperature,
        max_tokens,
        top_p,
        top_k,
        key,
        code_theme,
        busy_bar_index,
        font_color,
        timeout,
        prompt,
        prettify,
        whole,
        code,
        shell,
        disable_conversation,
        filepath,
        update_file,
        intro,
        history_offset,
        awesome_prompt,
        proxy_path,
        provider,
        vertical_overflow,
        quiet,
        new,
        with_copied,
        ignore_working,
        rawdog,
        internal_exec,
        confirm_script,
        interpreter,
        talk_to_me,
        talk_to_me_voice,
    ):
        """Generate a quick response with AI"""
        this.clear_history_file(filepath, new)
        bot = Main(
            max_tokens,
            temperature,
            top_k,
            top_p,
            model,
            key,
            timeout,
            disable_conversation,
            filepath,
            update_file,
            intro,
            history_offset,
            awesome_prompt,
            proxy_path,
            provider,
            quiet,
            ignore_working=ignore_working,
            rawdog=rawdog,
            internal_exec=internal_exec,
            confirm_script=confirm_script,
            interpreter=interpreter,
            non_interactive=True,
        )
        prompt = prompt if prompt else ""
        copied_placeholder = "{{copied}}"
        stream_placeholder = "{{stream}}"

        if with_copied or copied_placeholder in prompt:
            last_copied_text = clipman.get()
            assert last_copied_text, "No copied text found, issue prompt"

            if copied_placeholder in prompt:
                prompt = prompt.replace(copied_placeholder, last_copied_text)

            else:
                sep = "\n" if prompt else ""
                prompt = prompt + sep + last_copied_text

        if not prompt and sys.stdin.isatty():  # No prompt issued and no piped input
            help_info = (
                "Usage: pytgpt generate [OPTIONS] PROMPT\n"
                "Try 'pytgpt generate --help' for help.\n"
                "Error: Missing argument 'PROMPT'."
            )
            click.secho(
                help_info
            )  # Let's try to mimic the click's missing argument help info
            sys.exit(1)

        if not sys.stdin.isatty():  # Piped input detected - True
            # Let's try to read piped input
            stream_text = click.get_text_stream("stdin").read()
            if stream_placeholder in prompt:
                prompt = prompt.replace(stream_placeholder, stream_text)
            else:
                prompt = prompt + "\n" + stream_text if prompt else stream_text

        assert stream_placeholder not in prompt, (
            "No piped input detected ~ " + stream_placeholder
        )
        assert copied_placeholder not in prompt, (
            "No copied text found ~ " + copied_placeholder
        )

        prompt = Optimizers.code(prompt) if code else prompt
        prompt = Optimizers.shell_command(prompt) if shell else prompt
        busy_bar.spin_index = (
            0 if any([quiet, sys.stdout.isatty() == False]) else busy_bar_index
        )
        bot.code_theme = code_theme
        bot.color = font_color
        bot.prettify = prettify
        bot.vertical_overflow = vertical_overflow
        bot.disable_stream = whole
        bot.read_aloud = talk_to_me
        bot.read_aloud_voice = talk_to_me_voice
        bot.default(prompt, True, normal_stdout=(sys.stdout.isatty() == False))


class Awesome:
    """Awesome commands"""

    @staticmethod
    @click.command(context_settings=this.context_settings)
    @click.option(
        "-r",
        "--remote",
        help="Remote source to update from",
        default=AwesomePrompts.awesome_prompt_url,
    )
    @click.option(
        "-o",
        "--output",
        help="Path to save the prompts",
        default=AwesomePrompts.awesome_prompt_path,
    )
    @click.option(
        "-n", "--new", is_flag=True, help="Override the existing contents in path"
    )
    @click.help_option("-h", "--help")
    @this.handle_exception
    def update(remote, output, new):
        """Update awesome-prompts from remote source."""
        AwesomePrompts.awesome_prompt_url = remote
        AwesomePrompts.awesome_prompt_path = output
        AwesomePrompts().update_prompts_from_online(new)
        click.secho(
            f"Prompts saved to - '{AwesomePrompts.awesome_prompt_path}'", fg="cyan"
        )

    @staticmethod
    @click.command(context_settings=this.context_settings)
    @click.argument(
        "key",
        required=True,
        type=click.STRING,
    )
    @click.option(
        "-d", "--default", help="Return this value if not found", default=None
    )
    @click.option(
        "-c",
        "--case-sensitive",
        default=True,
        flag_value=False,
        help="Perform case-sensitive search",
    )
    @click.option(
        "-f",
        "--file",
        type=click.Path(exists=True),
        help="Path to existing prompts",
        default=AwesomePrompts.awesome_prompt_path,
    )
    @click.help_option("-h", "--help")
    @this.handle_exception
    def search(
        key,
        default,
        case_sensitive,
        file,
    ):
        """Search for a particular awesome-prompt by key or index"""
        AwesomePrompts.awesome_prompt_path = file
        resp = AwesomePrompts().get_act(
            key,
            default=default,
            case_insensitive=case_sensitive,
        )
        if resp:
            click.secho(resp)
            return resp != default

    @staticmethod
    @click.command(context_settings=this.context_settings)
    @click.option("-n", "--name", required=True, help="Prompt name")
    @click.option("-p", "--prompt", required=True, help="Prompt value")
    @click.option(
        "-f",
        "--file",
        type=click.Path(exists=True),
        help="Path to existing prompts",
        default=AwesomePrompts.awesome_prompt_path,
    )
    @click.help_option("-h", "--help")
    @this.handle_exception
    def add(name, prompt, file):
        """Add new prompt to awesome-prompt list"""
        AwesomePrompts.awesome_prompt_path = file
        return AwesomePrompts().add_prompt(name, prompt)

    @staticmethod
    @click.command(context_settings=this.context_settings)
    @click.argument("name")
    @click.option(
        "--case-sensitive",
        is_flag=True,
        flag_value=False,
        default=True,
        help="Perform name case-sensitive search",
    )
    @click.option(
        "-f",
        "--file",
        type=click.Path(exists=True),
        help="Path to existing prompts",
        default=AwesomePrompts.awesome_prompt_path,
    )
    @click.help_option("-h", "--help")
    @this.handle_exception
    def delete(name, case_sensitive, file):
        """Delete a specific awesome-prompt"""
        AwesomePrompts.awesome_prompt_path = file
        return AwesomePrompts().delete_prompt(name, case_sensitive)

    @staticmethod
    @click.command(context_settings=this.context_settings)
    @click.option(
        "-j",
        "--json",
        is_flag=True,
        help="Display prompts in json format",
    )
    @click.option(
        "-i",
        "--indent",
        type=click.IntRange(1, 20),
        help="Json format indentation level",
        default=4,
    )
    @click.option(
        "-x",
        "--index",
        is_flag=True,
        help="Display prompts with their corresponding indexes",
    )
    @click.option("-c", "--color", help="Prompts stdout font color")
    @click.option("-o", "--output", type=click.Path(), help="Path to save the prompts")
    @click.help_option("-h", "--help")
    def whole(json, indent, index, color, output):
        """Stdout all awesome prompts"""
        ap = AwesomePrompts()
        awesome_prompts = ap.all_acts if index else ap.get_acts()

        if json:
            # click.secho(formatted_awesome_prompts, fg=color)
            rich.print_json(data=awesome_prompts, indent=indent)

        else:
            awesome_table = Table(show_lines=True, title="All Awesome-Prompts")
            awesome_table.add_column("index", justify="center", style="yellow")
            awesome_table.add_column("Act Name/Index", justify="left", style="cyan")
            awesome_table.add_column(
                "Prompt",
                style=color,
            )
            for index, key_value in enumerate(awesome_prompts.items()):
                awesome_table.add_row(str(index), str(key_value[0]), key_value[1])
            rich.print(awesome_table)

        if output:
            from json import dump

            with open(output, "w") as fh:
                dump(awesome_prompts, fh, indent=4)


class Gpt4free:
    """Commands for gpt4free"""

    @staticmethod
    @click.command(context_settings=this.context_settings)
    @busy_bar.run(index=1, immediate=True)
    @click.help_option("-h", "--help")
    def version():
        """Check current installed version of gpt4free"""
        version_string = this.run_system_command("pip show g4f")[1].stdout.split("\n")[
            1
        ]
        click.secho(version_string, fg="cyan")

    @staticmethod
    @click.command(context_settings=this.context_settings)
    @click.help_option("-h", "--help")
    @click.option(
        "-e",
        "--extra",
        help="Extra required dependencies category",
        multiple=True,
        type=click.Choice(
            ["all", "image", "webdriver", "openai", "api", "gui", "none"]
        ),
        default=["all"],
    )
    @click.option("-l", "--log", is_flag=True, help="Stdout installation logs")
    @click.option(
        "-s",
        "--sudo",
        is_flag=True,
        flag_value="sudo ",
        help="Install with sudo privileges",
    )
    @busy_bar.run(index=1, immediate=True)
    def update(extra, log, sudo):
        """Update GPT4FREE package (Models, Providers etc)"""
        if "none" in extra:
            command = f"{sudo or ''}pip install --upgrade g4f"
        else:
            command = f"{sudo or ''}pip install --upgrade g4f[{','.join(extra)}]"
        is_successful, response = this.run_system_command(command)
        if log and is_successful:
            click.echo(response.stdout)
        version_string = this.run_system_command("pip show g4f")[1].stdout.split("\n")[
            1
        ]
        click.secho(f"GPT4FREE updated successfully - {version_string}", fg="cyan")

    @staticmethod
    @click.command("list", context_settings=this.context_settings)
    @click.argument("target")
    @click.option("-w", "--working", is_flag=True, help="Restrict to working providers")
    @click.option("-u", "--url", is_flag=True, help="Restrict to providers with url")
    @click.option(
        "-s", "--stream", is_flag=True, help="Restrict to providers supporting stream"
    )
    @click.option(
        "-c",
        "--context",
        is_flag=True,
        help="Restrict to providers supporing context natively",
    )
    @click.option(
        "-35",
        "--gpt35",
        is_flag=True,
        help="Restrict to providers supporting gpt3.5_turbo model",
    )
    @click.option(
        "-4", "--gpt4", is_flag=True, help="Restrict to providers supporting gpt4 model"
    )
    @click.option(
        "-se",
        "--selenium",
        is_flag=True,
        help="Restrict to selenium dependent providers",
    )
    @click.option("-j", "--json", is_flag=True, help="Format output in json")
    @click.help_option("-h", "--help")
    def show(target, working, url, stream, context, gpt35, gpt4, selenium, json):
        """List available models and providers"""
        available_targets = ["models", "providers"]
        assert (
            target in available_targets
        ), f"Target must be one of [{', '.join(available_targets)}]"
        if target == "providers":
            hunted_providers = list(
                set(
                    map(
                        lambda provider: (
                            provider["name"] if all(list(provider.values())) else None
                        ),
                        this.g4f_providers_in_dict(
                            url=url,
                            working=working,
                            stream=stream,
                            context=context,
                            gpt35=gpt35,
                            gpt4=gpt4,
                            selenium=selenium,
                        ),
                    )
                )
            )
            while None in hunted_providers:
                hunted_providers.remove(None)

            hunted_providers.sort()
            if json:
                rich.print_json(data=dict(providers=hunted_providers), indent=4)

            else:
                table = Table(show_lines=True)
                table.add_column("No.", style="yellow", justify="center")
                table.add_column("Provider", style="cyan")
                for no, provider in enumerate(hunted_providers):
                    table.add_row(str(no), provider)
                rich.print(table)
        else:
            models = dict(
                Bard=[
                    "palm",
                ],
                HuggingFace=[
                    "h2ogpt-gm-oasst1-en-2048-falcon-7b-v3",
                    "h2ogpt-gm-oasst1-en-2048-falcon-40b-v1",
                    "h2ogpt-gm-oasst1-en-2048-open-llama-13b",
                    "gpt-neox-20b",
                    "oasst-sft-1-pythia-12b",
                    "oasst-sft-4-pythia-12b-epoch-3.5",
                    "santacoder",
                    "bloom",
                    "flan-t5-xxl",
                ],
                Anthropic=[
                    "claude-instant-v1",
                    "claude-v1",
                    "claude-v2",
                ],
                Cohere=[
                    "command-light-nightly",
                    "command-nightly",
                ],
                OpenAI=[
                    "code-davinci-002",
                    "text-ada-001",
                    "text-babbage-001",
                    "text-curie-001",
                    "text-davinci-002",
                    "text-davinci-003",
                    "gpt-3.5-turbo-16k",
                    "gpt-3.5-turbo-16k-0613",
                    "gpt-4-0613",
                ],
                Replicate=[
                    "llama13b-v2-chat",
                    "llama7b-v2-chat",
                ],
            )
            for provider in pytgpt.g4f.Provider.__providers__:
                if hasattr(provider, "models"):
                    models[provider.__name__] = provider.models
            if json:
                for key, value in models.items():
                    while None in value:
                        value.remove(None)
                    value.sort()
                    models[key] = value

                rich.print_json(data=models, indent=4)
            else:
                table = Table(show_lines=True)
                table.add_column("No.", justify="center", style="white")
                table.add_column("Base Provider", style="cyan")
                table.add_column("Model(s)", style="yellow")
                for count, provider_models in enumerate(models.items()):
                    models = provider_models[1]
                    models.sort()
                    table.add_row(str(count), provider_models[0], "\n".join(models))
                rich.print(table)

    @staticmethod
    @click.command(context_settings=this.context_settings)
    @click.argument("port", type=click.INT, required=False)
    @click.option(
        "-a", "--address", help="Host on this particular address", default="127.0.0.1"
    )
    @click.option("-d", "--debug", is_flag=True, help="Start server in debug mode")
    @click.option(
        "-o", "--open", is_flag=True, help="Proceed to the interface immediately"
    )
    @click.help_option("-h", "--help")
    def gui(port, address, debug, open):
        """Launch gpt4free web interface"""
        from g4f.gui import run_gui

        port = port or 8000
        t1 = thr(
            target=run_gui,
            args=(
                address,
                port,
                debug,
            ),
        )
        # run_gui(host=address, port=port, debug=debug)
        t1.start()
        if open:
            click.launch(f"http://{address}:{port}")
        t1.join()

    @staticmethod
    @click.command(context_settings=this.context_settings)
    @click.option(
        "-t",
        "--timeout",
        type=click.INT,
        help="Provider's response generation timeout",
        default=20,
    )
    @click.option(
        "-r",
        "--thread",
        type=click.INT,
        help="Test n amount of providers at once",
        default=5,
    )
    @click.option("-q", "--quiet", is_flag=True, help="Suppress progress bar")
    @click.option(
        "-j", "--json", is_flag=True, help="Stdout test results in json format"
    )
    @click.option("-d", "--dry-test", is_flag=True, help="Return previous test results")
    @click.option(
        "-b", "--best", is_flag=True, help="Stdout the fastest provider <name only>"
    )
    @click.option(
        "-se",
        "--selenium",
        help="Test even selenium dependent providers",
        is_flag=True,
    )
    @click.option(
        "-dl",
        "--disable-logging",
        is_flag=True,
        help="Disable logging",
    )
    @click.option("-y", "--yes", is_flag=True, help="Okay to all confirmations")
    @click.help_option("-h", "--help")
    def test(
        timeout, thread, quiet, json, dry_test, best, selenium, disable_logging, yes
    ):
        """Test and save working providers"""
        from pytgpt.gpt4free import utils

        test = utils.TestProviders(
            test_at_once=thread,
            quiet=quiet,
            timeout=timeout,
            selenium=selenium,
            do_log=disable_logging == False,
        )
        if best:
            click.secho(test.best)
            return
        elif dry_test:
            results = test.get_results(
                run=False,
            )
        else:
            if (
                yes
                or os.path.isfile(utils.results_path)
                and click.confirm("Are you sure to run new test")
            ):
                results = test.get_results(run=True)
            else:
                results = test.get_results(
                    run=False,
                )
        if json:
            rich.print_json(data=dict(results=results))
        else:
            table = Table(
                title="G4f Providers Test Results",
                show_lines=True,
            )
            table.add_column("No.", style="white", justify="center")
            table.add_column("Provider", style="yellow", justify="left")
            table.add_column("Response Time(s)", style="cyan")

            for no, provider in enumerate(results, start=1):
                table.add_row(
                    str(no), provider["name"], str(round(provider["time"], 2))
                )
            rich.print(table)


class ImageGen:

    @staticmethod
    @click.command(context_settings=this.context_settings)
    @click.argument("prompt")
    @click.option(
        "-p",
        "--provider",
        help="Provider name for image generation",
        type=click.Choice(
            list(this.image_providers_map.keys()),
        ),
        default="default",
    )
    @click.option(
        "-d",
        "--directory",
        type=click.Path(exists=True),
        help="Folder for saving the images",
        default=os.getcwd(),
    )
    @click.option(
        "-a",
        "--amount",
        type=click.IntRange(1, 100),
        help="Total images to be generated",
        default=1,
    )
    @click.option("-n", "--name", help="Name for the generated images")
    @click.option(
        "-t",
        "--timeout",
        type=click.IntRange(5, 300),
        help="Http request timeout in seconds",
    )
    @click.option("-pr", "--proxy", help="Http request proxy")
    @click.option(
        "-nd",
        "--no-additives",
        is_flag=True,
        help="Disable prompt altering for effective image generation",
    )
    @click.option("-q", "--quiet", is_flag=True, help="Suppress progress bar")
    @click.option(
        "-s",
        "--stream",
        help="Stream the image download process.",
        is_flag=True,
    )
    @click.help_option("-h", "--help")
    def generate_image(
        prompt,
        provider,
        directory,
        amount,
        name,
        timeout,
        proxy,
        no_additives,
        quiet,
        stream,
    ):
        """Generate images with pollinations.ai"""
        provider_obj = this.image_providers_map.get(provider)
        with Progress() as progress:
            task = progress.add_task(
                f"[cyan]Generating ...[{amount}]",
                total=amount,
                visible=quiet == False,
            )
            imager: Prodia | Imager = provider_obj(
                timeout=timeout, proxies=proxy if proxy else {}
            )
            for image in imager.generate(
                prompt=prompt,
                amount=amount,
                additives=no_additives == False,
                stream=stream,  # Just a hack for temporary save. Raises "'async_generator' object is not iterable"
            ):
                imager.save([image], name=name, dir=directory)
                progress.update(task, advance=1)


class Utils:
    """Utilities command"""

    @staticmethod
    @click.command(context_settings=this.context_settings)
    @click.argument("source", required=False)
    @click.option(
        "-d", "--dev", is_flag=True, help="Update from version control (development)"
    )
    @click.option(
        "-s",
        "--sudo",
        is_flag=True,
        flag_value="sudo ",
        help="Install with sudo privileges",
    )
    @click.help_option("-h", "--help")
    @busy_bar.run(index=1, immediate=True)
    def update(source, dev, sudo):
        """Install latest version of pytgpt"""
        if dev:
            source = "git+" + pytgpt.__repo__ + ".git"
        source = "python-tgpt" if source is None else source
        assert (
            "tgpt" in source or source == "."
        ), f"Cannot update pytgpt from the source '{source}'"
        click.secho(
            f"[*] Updating from '{'pip' if source=='python-tgpt' else source}'",
            fg="yellow",
        )
        this.run_system_command(f"{sudo or ''}pip install --upgrade {source}")
        response = this.run_system_command("pip show python-tgpt")[1]
        click.secho(response.stdout)
        click.secho("Congratulations! Pytgpt updated successfully.", fg="cyan")

    @staticmethod
    @click.command(context_settings=this.context_settings)
    @click.option("-w", "--whole", is_flag=True, help="Stdout whole json info")
    @click.option(
        "-v", "--version", is_flag=True, help="Stdout latest version name only"
    )
    @click.option("-b", "--body", is_flag=True, help="Stdout changelog info only")
    @click.option(
        "-e", "--executable", is_flag=True, help="Stdout url to binary for your system"
    )
    @click.help_option("-h", "--help")
    def latest(whole, version, body, executable):
        """Check pytgpt latest version info"""
        from pytgpt.utils import Updates

        update = Updates()
        if whole:
            rich.print_json(data=update.latest(whole=True))

        elif version:
            rich.print(update.latest_version)
        elif body:
            rich.print(Markdown(update.latest()["body"]))
        elif executable:
            rich.print(update.executable())
        else:
            rich.print_json(data=update.latest())


class API:
    """API control endpoint"""

    @staticmethod
    @click.command(context_settings=this.context_settings)
    @click.option(
        "-p",
        "--port",
        type=click.INT,
        default=8000,
        help="Port for listening requests",
    )
    @click.option(
        "-b",
        "--bind",
        default="127.0.0.1",
        help="Address to serve from",
    )
    @click.option(
        "-l",
        "--log-level",
        type=click.Choice(
            ["debug", "info", "warning", "errror", "critical"],
        ),
        default="info",
    )
    @click.help_option("-h", "--help")
    def run(port, bind, log_level):
        """Launch FastAPI"""
        import uvicorn
        from pytgpt.api import app

        uvicorn.run(app, host=bind, port=port, log_level=log_level)

    @staticmethod
    @click.command(context_settings=this.context_settings)
    @click.argument(
        "content", required=True, type=click.Choice(["images", "audios", "all"])
    )
    @click.option("-y", "--yes", is_flag=True, help="Okay to all confirmation prompts")
    @click.help_option("-h", "--help")
    def clear(content: str, yes: bool):
        """Delete api's static contents"""
        from pytgpt.utils import (
            api_static_image_dir,
            api_static_audio_dir,
            api_static_dir,
        )
        from pathlib import Path
        import shutil

        static_contents_map: dict[str, Path] = {
            "images": api_static_image_dir,
            "all": api_static_dir,
            "audios": api_static_audio_dir,
        }
        content_path: Path = static_contents_map[content]
        if not yes:
            yess: bool = click.confirm(
                f"Are you sure to clear {content} '{content_path.as_posix()}'"
            )
            if not yess:
                return
        else:
            pass
        total_entries = len(os.listdir(content_path))
        shutil.rmtree(content_path)
        click.secho(f"{content.title()} cleared ({total_entries})", fg="yellow")


def make_commands():
    """Make pytgpt chained commands"""
    # generate
    EntryGroup.tgpt2_.add_command(ChatGenerate.generate)

    # interactive
    EntryGroup.tgpt2_.add_command(ChatInteractive.interactive)

    # utils
    EntryGroup.utils.add_command(Utils.update)
    EntryGroup.utils.add_command(Utils.latest)

    # gpt4free
    EntryGroup.gpt4free.add_command(Gpt4free.version)
    EntryGroup.gpt4free.add_command(Gpt4free.update)
    EntryGroup.gpt4free.add_command(Gpt4free.show)
    EntryGroup.gpt4free.add_command(Gpt4free.gui)
    EntryGroup.gpt4free.add_command(Gpt4free.test)

    # Awesome
    EntryGroup.awesome.add_command(Awesome.add)
    EntryGroup.awesome.add_command(Awesome.delete)
    EntryGroup.awesome.add_command(Awesome.search)
    EntryGroup.awesome.add_command(Awesome.update)
    EntryGroup.awesome.add_command(Awesome.whole)

    # Image generator
    EntryGroup.tgpt2_.add_command(ImageGen.generate_image, "imager")

    # FastAPI
    EntryGroup.api.add_command(API.run)
    EntryGroup.api.add_command(API.clear)
    try:
        import pytgpt_bot.cli as bot

        EntryGroup.bot.add_command(bot.run)
        EntryGroup.bot.add_command(bot.clear)
    except ImportError:
        pass


# @this.handle_exception
def main(*args):
    """Fireup console programmically"""
    sys.argv += list(args)
    args = sys.argv
    if len(args) == 1:
        sys.argv.insert(1, "interactive")  # Just a hack to make default command
    try:
        make_commands()
        return EntryGroup.tgpt2_()
    except Exception as e:
        logging.error(this.getExc(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
