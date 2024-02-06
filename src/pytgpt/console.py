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
import re
import sys
import datetime
import time
import subprocess
from threading import Thread as thr
from functools import wraps
from rich.panel import Panel
from rich.style import Style
from rich.markdown import Markdown
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.prompt import Prompt
from typing import Iterator
from pytgpt.utils import Optimizers
from pytgpt.utils import default_path
from pytgpt.utils import AwesomePrompts
from WebChatGPT.console import chat as webchatgpt
from colorama import Fore
from colorama import init as init_colorama

init_colorama(autoreset=True)

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

    default_provider = "phind"

    getExc = lambda e: e.args[1] if len(e.args) > 1 else str(e)

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
        url=True, working=True, stream=False, context=False, gpt35=False, gpt4=False
    ):
        from pytgpt import g4f

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

            hunted_providers.append(provider_meta)

        return hunted_providers

    @staticmethod
    def stream_output(
        iterable: Iterator,
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
           iterable (Iterator): Iterator containing contents to be stdout
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


class Main(cmd.Cmd):
    intro = (
        "Welcome to AI Chat in terminal. "
        "Type 'help' or 'h' for usage info.\n"
        f"Submit any bug at {pytgpt.__repo__}/issues/new"
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
            if provider == "leo":
                import pytgpt.leo as leo

                self.bot = leo.LEO(
                    is_conversation=disable_conversation,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_k=top_k,
                    top_p=top_p,
                    model=getOr(model, leo.main.model),
                    brave_key=getOr(auth, leo.main.key),
                    timeout=timeout,
                    intro=intro,
                    filepath=filepath,
                    update_file=update_file,
                    proxies=proxies,
                    history_offset=history_offset,
                    act=awesome_prompt,
                )

            elif provider == "fakeopen":
                from pytgpt.fakeopen import main

                self.bot = main.FAKEOPEN(
                    disable_conversation,
                    max_tokens,
                    temperature,
                    top_p,
                    top_k,
                    top_p,
                    getOr(model, main.model),
                    getOr(auth, main.auth),
                    timeout,
                    intro,
                    filepath,
                    update_file,
                    proxies,
                    history_offset,
                    awesome_prompt,
                )

            elif provider == "openai":
                assert auth, "OpenAI API key is required"
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

            elif provider == "opengpt":
                from pytgpt.opengpt import OPENGPT

                self.bot = OPENGPT(
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

            elif provider == "bard":
                from pytgpt.bard import BARD

                assert (
                    auth
                ), f"Path to bard.google.com.cookie.json file is required. Use the flag `--key` or `-k`"
                self.bot = BARD(
                    cookie_file=auth,
                    proxy=proxies,
                    timeout=timeout,
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
                )

            elif provider == "llama2":
                import pytgpt.llama2.main as llama2

                self.bot = llama2.LLAMA2(
                    is_conversation=disable_conversation,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    presence_penalty=top_p,
                    frequency_penalty=top_k,
                    top_p=top_p,
                    model=getOr(model, llama2.default_model),
                    timeout=timeout,
                    intro=intro,
                    filepath=filepath,
                    update_file=update_file,
                    proxies=proxies,
                    history_offset=history_offset,
                    act=awesome_prompt,
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
        self.__init_time = time.time()
        self.__start_time = time.time()
        self.__end_time = time.time()

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
                f"(`{Fore.MAGENTA}{self.provider})`"
                f"~[`{Fore.LIGHTWHITE_EX}🕒{Fore.BLUE}{current_time}-`"
                f"{Fore.LIGHTWHITE_EX}💻{Fore.RED}{find_range(self.__init_time, time.time(), True)}-`"
                f"{Fore.LIGHTWHITE_EX}⚡{Fore.YELLOW}{find_range(self.__start_time, self.__end_time)}s]`"
                f"\n╰─>"
            )
            whitelist = ["[", "]", "~", "-", "(", ")"]
            for character in whitelist:
                cmd_prompt = cmd_prompt.replace(character + "`", Fore.RESET + character)
            return cmd_prompt

        else:
            return (
                f"╭─[{getpass.getuser().capitalize()}@pyTGPT]({self.provider})"
                f"~[🕒{current_time}"
                f"-💻{find_range(self.__init_time, time.time(), True)}"
                f"-⚡{find_range(self.__start_time, self.__end_time)}s]"
                "\n╰─>"
            )

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
                "Enter path/file-name", default="llama-conversation.txt"
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

    @busy_bar.run()
    def default(self, line, exit_on_error: bool = False):
        """Chat with ChatGPT"""
        if not bool(line):
            return
        if line.startswith("./"):
            os.system(line[2:])
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
            finally:
                self.__end_time = time.time()

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
            click.secho("Okay Goodbye!", fg="yellow")
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


class ChatInteractive:
    """Interactive command"""

    @staticmethod
    @click.command()
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
        default=-1,
    )
    @click.option(
        "-k",
        "--key",
        envvar="auth_key",
        help="LLM API access key or auth value",
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
        envvar="history_offset",
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
        envvar="proxy_path",
        help="Path to .json file containing proxies",
    )
    @click.option(
        "-p",
        "--provider",
        type=click.Choice(pytgpt.available_providers),
        default=this.default_provider,
        help="Name of LLM provider.",
        envvar="llm_provider",
        metavar=(
            f"[{', '.join(pytgpt.tgpt_providers)}] etc, "
            "run 'pytgpt gpt4free list providers -w' to view more providers"
        ),
    )
    @click.option(
        "-vo",
        "--vertical-overflow",
        envvar="vertical_overflow",
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
        help="Flag for controlling response-framing",
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
        vertical_overflow,
        whole,
        quiet,
        new,
        with_copied,
        no_coloring,
        chat_completion,
        ignore_working,
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
        )
        busy_bar.spin_index = busy_bar_index
        bot.code_theme = code_theme
        bot.color = font_color
        bot.disable_coloring = no_coloring
        bot.prettify = prettify
        bot.vertical_overflow = vertical_overflow
        bot.disable_stream = whole
        if prompt:
            if with_copied:
                prompt = prompt + "\n" + clipman.get()
            bot.default(prompt)
        bot.cmdloop()


class ChatGenerate:
    """Generate command"""

    @staticmethod
    @click.command()
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
        default=-1,
    )
    @click.option(
        "-k",
        "--key",
        envvar="auth_key",
        help="LLM API access key or auth value",
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
        envvar="history_offset",
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
        envvar="proxy_path",
        help="Path to .json file containing proxies",
    )
    @click.option(
        "-p",
        "--provider",
        type=click.Choice(pytgpt.available_providers),
        default=this.default_provider,
        help="Name of LLM provider.",
        envvar="llm_provider",
        metavar=(
            f"[{', '.join(pytgpt.tgpt_providers)}] etc, "
            "run 'pytgpt gpt4free list providers -w' to view more providers"
        ),
    )
    @click.option(
        "-vo",
        "--vertical-overflow",
        envvar="vertical_overflow",
        help="Vertical overflow behaviour on content display",
        type=click.Choice(["visible", "crop", "ellipsis"]),
        default="ellipsis",
    )
    @click.option(
        "-q",
        "--quiet",
        is_flag=True,
        help="Flag for controlling response-framing",
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
    ):
        """Generate a quick response with AI"""
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

        elif prompt != prompt.replace(stream_placeholder, ""):
            # {{stream}} without piped input
            raise Exception(f"No piped input detected ~ {stream_placeholder}")

        this.clear_history_file(filepath, new)
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
        bot.default(prompt, True)


class Awesome:
    """Awesome commands"""

    @staticmethod
    @click.command()
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
    @click.command()
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
    @click.command()
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
    @click.command()
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
    @click.command()
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
    @click.command()
    @busy_bar.run(index=1, immediate=True)
    @click.help_option("-h", "--help")
    def version():
        """Check current installed version of gpt4free"""
        version_string = this.run_system_command("pip show g4f")[1].stdout.split("\n")[
            1
        ]
        click.secho(version_string, fg="cyan")

    @staticmethod
    @click.command()
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
    @click.command("list")
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
    @click.option("-j", "--json", is_flag=True, help="Format output in json")
    @click.help_option("-h", "--help")
    def show(target, working, url, stream, context, gpt35, gpt4, json):
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
                        ),
                    )
                )
            )
            hunted_providers = (
                hunted_providers[1:]
                if hunted_providers[0] is None
                else hunted_providers
            )
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
            if json:
                rich.print_json(data=models, indent=4)
            else:
                table = Table(show_lines=True)
                table.add_column("No.", justify="center", style="white")
                table.add_column("Base Provider", style="cyan")
                table.add_column("Model(s)", style="yellow")
                for count, provider_models in enumerate(models.items()):
                    table.add_row(
                        str(count), provider_models[0], "\n".join(provider_models[1])
                    )
                rich.print(table)

    @staticmethod
    @click.command()
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


class Utils:
    """Utilities command"""

    @staticmethod
    @click.command()
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
    @click.command()
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


def make_commands():
    """Make pytgpt chained commands"""
    # webchatgpt
    # Intergration with WebChatGPT https://github.com/Simatwa/WebChatGPT
    EntryGroup.tgpt2_.add_command(webchatgpt, "webchatgpt")

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

    # Awesome
    EntryGroup.awesome.add_command(Awesome.add)
    EntryGroup.awesome.add_command(Awesome.delete)
    EntryGroup.awesome.add_command(Awesome.search)
    EntryGroup.awesome.add_command(Awesome.update)
    EntryGroup.awesome.add_command(Awesome.whole)


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
