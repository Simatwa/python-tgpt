<p align="center">
<img src="https://github.com/Simatwa/python-tgpt/blob/main/assets/py-tgpt.png?raw=true" width='40%'>
</p>

<!-- <h1 align="center"> python-tgpt </h1> -->
<p align="center">
<!--
<a href="https://github.com/Simatwa/python-tgpt/actions/workflows/python-test.yml"><img src="https://github.com/Simatwa/python-tgpt/actions/workflows/python-test.yml/badge.svg" alt="Python Test"/></a>
-->
<a href="https://github.com/Simatwa/python-tgpt/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/static/v1?logo=GPL&color=Blue&message=MIT&label=License"/></a>
<a href=""><img alt="Python version" src="https://img.shields.io/pypi/pyversions/python-tgpt"/></a>
<a href="https://pypi.org/project/python-tgpt"><img alt="PyPi" src="https://img.shields.io/pypi/v/python-tgpt?color=green"/></a>
<a href="https://github.com/psf/black"><img alt="Black" src="https://img.shields.io/badge/code%20style-black-000000.svg"/></a>
<a href="https://python-tgpt.onrender.com"><img alt="Website status" src="https://img.shields.io/website?url=https://python-tgpt.onrender.com"/></a>
<a href="https://github.com/Simatwa/python-tgpt/actions/workflows/python-package.yml"><img alt="Python Package flow" src="https://github.com/Simatwa/python-tgpt/actions/workflows/python-package.yml/badge.svg?branch=master"/></a>
<a href="https://pepy.tech/project/python-tgpt"><img src="https://static.pepy.tech/personalized-badge/python-tgpt?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads" alt="Downloads"></a>
<a href="https://github.com/Simatwa/python-tgpt/releases/latest"><img src="https://img.shields.io/github/downloads/Simatwa/python-tgpt/total?label=Asset%20Downloads&color=success" alt="Downloads"></img></a>
<a href="https://github.com/Simatwa/python-tgpt/releases"><img src="https://img.shields.io/github/v/release/Simatwa/python-tgpt?color=success&label=Release&logo=github" alt="Latest release"></img></a>
<a href="https://github.com/Simatwa/python-tgpt/releases"><img src="https://img.shields.io/github/release-date/Simatwa/python-tgpt?label=Release date&logo=github" alt="release date"></img></a>
<a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com/Simatwa/python-tgpt"/></a>      
<a href="https://wakatime.com/badge/github/Simatwa/tgpt2"><img src="https://wakatime.com/badge/github/Simatwa/tgpt2.svg" alt="wakatime"></a>
</p>

<h3 align="center">
python-tgpt
</h3> 

<p align="center">
<img src="https://github.com/Simatwa/python-tgpt/blob/main/assets/demo-1.gif?raw=True" width='80%'/>
</p>


```python
>>> import pytgpt.phind as phind
>>> bot = phind.PHIND()
>>> bot.chat('hello there')
'Hello! How can I assist you today?'

```

```python
from pytgpt.imager import Imager
img = Imager()
generated_images = img.generate(prompt="Cyberpunk", amount=3, stream=True)
img.save(generated_images)
```

This project enables seamless interaction with over **45 free LLM providers** without requiring an API Key and generating images as well.

The name *python-tgpt* draws inspiration from its parent project [tgpt](https://github.com/aandrew-me/tgpt), which operates on [Golang](https://go.dev/). Through this Python adaptation, users can effortlessly engage with a number of free LLMs available, fostering a smoother AI interaction experience.

### Features

- 🐍 Python package
- [🌐 FastAPI for web integration](https://python-tgpt.onrender.com)
- ⌨️ Command-line interface
- 🧠 Multiple LLM providers - **45+**
- 🌊 Stream and non-stream response
- 🚀 Ready to use (No API key required)
- 🎯 Customizable script generation and execution
- 🔌 Offline support for Large Language Models
- 🎨 Image generation capabilities
- 🎤 Text-to-audio conversion capabilities
- ⛓️ Chained requests via proxy
- 🗨️ Enhanced conversational chat experience
- 💾 Capability to save prompts and responses (Conversation)
- 🔄 Ability to load previous conversations
- 🚀 Pass [awesome-chatgpt prompts](https://github.com/f/awesome-chatgpt-prompts) easily
- 🤖 [Telegram bot](https://t.me/pytgpt_bot) - interface
- 🔄 Asynchronous support for all major operations.


## Providers

These are simply the hosts of the LLMs, which include:

1. [Leo](https://brave.com/leo/) - **Brave**
2. [Koboldai](https://koboldai-koboldcpp-tiefighter.hf.space)
3. [OpenGPTs](https://opengpts-example-vz4y4ooboq-uc.a.run.app/)
4. [OpenAI](https://chat.openai.com) *(API key required)*
5. [WebChatGPT](https://github.com/Simatwa/WebChatGPT) - **OpenAI** *(Session ID required)*
6. [Gemini](https://github.com/Simatwa/bard) - **Google** *(Session ID required)*
9. [Phind](https://www.phind.com)
10. [Llama2](https://www.llama2.ai)
11. [Blackboxai](https://www.blackbox.ai)
12. [gpt4all](https://gpt4all.io) *(Offline)*
13. [Poe](https://poe.com) - Poe|Quora *(Session ID required)*
14. [Groq](https://console.groq.com/playground) *(API Key required)*
15. [Perplexity](https://www.perplexity.ai)
16. [YepChat](https://yep.com)
17. [Novita](https://novita.ai) *(API key required)*

<details>

<summary>

41+ providers proudly offered by [gpt4free](https://github.com/xtekky/gpt4free).

</summary>

- To list working providers run:
   ```sh
   $ pytgpt gpt4free test -y
   ```
</details>

## Prerequisites

- [x] [Python>=3.10](https://python.org) *(Optional)*

## Installation and Usage

### Installation

Download binaries for your system from [here.](https://github.com/Simatwa/python-tgpt/releases/latest/)

Alternatively, you can install non-binaries. *(Recommended)*

1. Developers:

   ```sh
   pip install --upgrade python-tgpt
   ```

2. Commandline:

   ```sh
   pip install --upgrade "python-tgpt[cli]"
   ```

3. Full installation:

   ```sh
   pip install  --upgrade "python-tgpt[all]"
   ```

> `pip install -U "python-tgt[api]"` will install REST API dependencies.

#### Termux extras

1. Developers:

   ```sh
   pip install --upgrade "python-tgpt[termux]"
   ```

2. Commandline:

   ```sh
   pip install --upgrade "python-tgpt[termux-cli]"
   ```

3. Full installation:

   ```sh
   pip install  --upgrade "python-tgpt[termux-all]"
   ```

> `pip install -U "python-tgt[termux-api]"` will install REST API dependencies


## Usage

This package offers a convenient command-line interface.

> [!NOTE]
> `phind` is the default *provider*.

- For a quick response:
  ```bash
  python -m pytgpt generate "<Your prompt>"
  ```

- For interactive mode:
  ```bash
  python -m pytgpt interactive "<Kickoff prompt (though not mandatory)>"
  ```

Make use of flag `--provider` followed by the provider name of your choice. e.g `--provider koboldai`

> To list all providers offered by gpt4free, use following commands: ```pytgpt gpt4free list providers```

You can also simply use `pytgpt` instead of `python -m pytgpt`.

Starting from version 0.2.7, running `$ pytgpt` without any other command or option will automatically enter the `interactive` mode. Otherwise, you'll need to explicitly declare the desired action, for example, by running `$ pytgpt generate`.


<details>

<summary> 

### Developer Docs

</summary>

1. Generate a quick response

```python
from pytgpt.leo import LEO
bot = LEO()
resp = bot.chat('<Your prompt>')
print(resp)
# Output : How may I help you.
```

2. Get back whole response

```python
from pytgpt.leo import LEO
bot = LEO()
resp = bot.ask('<Your Prompt')
print(resp)
# Output
"""
{'completion': "I'm so excited to share with you the incredible experiences...", 'stop_reason': None, 'truncated': False, 'stop': None, 'model': 'llama-2-13b-chat', 'log_id': 'cmpl-3NmRt5A5Djqo2jXtXLBwJ2', 'exception': None}
"""
```

#### Stream Response 

Just add parameter `stream` with value  `true`.

1. Text Generated only 

```python
from pytgpt.leo import LEO
bot = LEO()
resp = bot.chat('<Your prompt>', stream=True)
for value in resp:
    print(value)
# output
"""
How may
How may I help 
How may I help you
How may I help you today?
"""
```

2. Whole Response

```python
from pytgpt.leo import LEO
bot = LEO()
resp = bot.ask('<Your Prompt>', stream=True)
for value in resp:
    print(value)
# Output
"""
{'completion': "I'm so", 'stop_reason': None, 'truncated': False, 'stop': None, 'model': 'llama-2-13b-chat', 'log_id': 'cmpl-3NmRt5A5Djqo2jXtXLBwxx', 'exception': None}

{'completion': "I'm so excited to share with.", 'stop_reason': None, 'truncated': False, 'stop': None, 'model': 'llama-2-13b-chat', 'log_id': 'cmpl-3NmRt5A5Djqo2jXtXLBwxx', 'exception': None}

{'completion': "I'm so excited to share with you the incredible ", 'stop_reason': None, 'truncated': False, 'stop': None, 'model': 'llama-2-13b-chat', 'log_id': 'cmpl-3NmRt5A5Djqo2jXtXLBwxx', 'exception': None}

{'completion': "I'm so excited to share with you the incredible experiences...", 'stop_reason': None, 'truncated': False, 'stop': None, 'model': 'llama-2-13b-chat', 'log_id': 'cmpl-3NmRt5A5Djqo2jXtXLBwxx', 'exception': None}
"""
```

<details>

<summary>
Auto - *(selects any working provider)*

</summary>

```python
import pytgpt.auto import auto
bot = auto.AUTO()
print(bot.chat("<Your-prompt>"))
```

</details>

<details>

<summary>
Openai

</summary>

```python
import pytgpt.openai as openai
bot = openai.OPENAI("<OPENAI-API-KEY>")
print(bot.chat("<Your-prompt>"))
```

</details>


<details>

<summary>
Koboldai

</summary>

```python
import pytgpt.koboldai as koboldai
bot = koboldai.KOBOLDAI()
print(bot.chat("<Your-prompt>"))
```

</details>


<details>

<summary>
Opengpt

</summary>

```python
import pytgpt.opengpt as opengpt
bot = opengpt.OPENGPT()
print(bot.chat("<Your-prompt>"))
```

</details>

<details>

<summary>
phind

</summary>

```python
import pytgpt.phind as phind
bot = phind.PHIND()
print(bot.chat("<Your-prompt>"))
```

</details>

<details>

<summary>
Gpt4free providers

</summary>

```python
import pytgpt.gpt4free as gpt4free
bot = gpt4free.GPT4FREE(provider="Koala")
print(bot.chat("<Your-prompt>"))
```

</details>

<details>

<summary>
Novita

</summary>

```python
import pytgpt.novita as novita
bot = novita.NOVITA("<NOVITA-API-KEY>")
print(bot.chat("<Your-prompt>"))
```

</details>

### Asynchronous

**Version 0.7.0** introduces asynchronous implementation to almost all providers except a few such as *perplexity & gemini*, which relies on other libraries which lacks such implementation.

To make it easier, you just have to prefix `Async` to the common synchronous class name. For instance `OPENGPT` will be accessed as `AsyncOPENGPT`:

#### Streaming Whole ai response.

```python
import asyncio
from pytgpt.phind import AsyncPHIND

async def main():
    async_ask = await AsyncPHIND(False).ask(
        "Critique that python is cool.",
        stream=True
    )
    async for streaming_response in async_ask:
        print(
            streaming_response
        )

asyncio.run(
    main()
)
```

#### Streaming just the text

```python
import asyncio
from pytgpt.phind import AsyncPHIND

async def main():
    async_ask = await AsyncPHIND(False).chat(
        "Critique that python is cool.",
        stream=True
    )
    async for streaming_text in async_ask:
        print(
            streaming_text
        )

asyncio.run(
    main()
)
```

</details>

<details>

<summary>

To obtain more tailored responses, consider utilizing [optimizers](pytgpt/utils.py) using the `optimizer` parameter. Its values can be set to either `code` or `system_command`.

</summary>

```python
from pytgpt.leo import LEO
bot = LEO()
resp = bot.ask('<Your Prompt>', optimizer='code')
print(resp)
```

</details>

</details>

> [!IMPORTANT]
> Commencing from [v0.1.0](https://github.com/Simatwa/python-tgpt/releases/), the default mode of interaction is conversational. This mode enhances the interactive experience, offering better control over the chat history. By associating previous prompts and responses, it tailors conversations for a more engaging experience.

You can still disable the mode:

```python
bot = koboldai.KOBOLDAI(is_conversation=False)
```

Utilize the `--disable-conversation` flag in the console to achieve the same functionality.

> [!CAUTION]
> **Bard** autohandles context due to the obvious reason; the `is_conversation` parameter is not necessary at all hence not required when initializing the class. Also be informed that majority of providers offered by *gpt4free* requires *Google Chrome* inorder to function.

### Image Generation

This has been made possible by [pollinations.ai](https://pollination.ai).
```sh
$ pytgpt imager "<prompt>"
# e.g pytgpt imager "Coding bot"
```

<details>

<summary>
Developers
</summary>

```python
from pytgpt.imager import Imager

img = Imager()

generated_img = img.generate('Coding bot') # [bytes]

img.save(generated_img)
```

<details>

<summary>
Download Multiple Images
</summary>

```python

from pytgpt.imager import Imager

img = Imager()

img_generator = img.generate('Coding bot', amount=3, stream=True)

img.save(img_generator)

# RAM friendly
```

</details>

#### Using **Prodia** provider

```python
from pytgpt.imager import Prodia

img = Prodia()

img_generator = img.generate('Coding bot', amount=3, stream=True)

img.save(img_generator)
```

</details>

### Advanced Usage of Placeholders

The `generate` functionality has been enhanced starting from *v0.3.0* to enable comprehensive utilization of the `--with-copied` option and support for accepting piped inputs. This improvement introduces placeholders, offering dynamic values for more versatile interactions.

| Placeholder | Represents |
| ------------ | ----------- |
| `{{stream}}` | The piped input |
| `{{copied}}` | The last copied text |

This feature is particularly beneficial for intricate operations. For example:

```bash
$ git diff | pytgpt generate "Here is a diff file: {{stream}} Make a concise commit message from it, aligning with my commit message history: {{copied}}" --new
```
> In this illustration, `{{stream}}` denotes the result of the `$ git diff` operation, while `{{copied}}` signifies the content copied from the output of the `$ git log` command.

### Awesome Prompts

[These prompts](https://github.com/Simatwa/gpt-cli/blob/main/assets/all-acts.pdf?raw=True) are designed to guide the AI's behavior or responses in a particular direction, encouraging it to exhibit certain characteristics or behaviors. The  term "awesome-prompt" is not a formal term in AI or machine learning literature, but it encapsulates the idea of crafting prompts that are effective in achieving desired outcomes. Let's say you want it to behave like a *Linux Terminal*, *PHP Interpreter*, or just to [**JAIL BREAK.**](https://gist.github.com/coolaj86/6f4f7b30129b0251f61fa7baaa881516)

Instances :

```sh
$ pytgpt interactive --awesome-prompt "Linux Terminal"
# Act like a Linux Terminal

$ pytgpt interactive -ap DAN
# Jailbreak
```

> [!NOTE]
> Awesome prompts are alternative to `--intro`.
> Run `$ pytgpt awesome whole` to list available prompts (*200+*).
> Run `$ pytgpt awesome --help` for more info.

### Introducing RawDog

RawDog is a masterpiece feature that exploits the versatile capabilities of Python to command and control your system as per your needs. You can literally do anything with it, since it generates and executes python codes, driven by **your prompts**! To have a bite of *rawdog* simply append the flag `--rawdog` *shortform* `-rd` in *generate/interactive* mode. This introduces a never seen-before feature in the *tgpt ecosystem*. Thanks to [AbanteAI/rawdog](https://github.com/AbanteAI/rawdog) for the idea.

This can be useful in some ways. For instance :

   ```sh
   $ pytgpt generate -n -q "Visualize the disk usage using pie chart" --rawdog
   ```
   
   This will pop up a window showing system disk usage as shown below.
   
   <p align="center">
   <img src="https://github.com/Simatwa/python-tgpt/blob/main/assets/Figure_1.png?raw=true" width='60%'>
   </p>

## Passing Environment Variables

Pytgpt **v0.4.6** introduces a convention way of taking variables from the environment.
To achieve that, set the environment variables in your operating system or script with prefix `PYTGPT_` followed by the option name in uppercase, replacing dashes with underscores.

For example, for the option `--provider`, you would set an environment variable `PYTGPT_PROVIDER` to provide a default value for that option. Same case applies to boolean flags such as `--rawdog` whose environment variable will be `PYTGPT_RAWDOG` with value being either `true/false`. Finally, `--awesome-prompt` will take the environment variable `PYTGPT_AWESOME_PROMPT`.

> [!NOTE]
> This is **NOT** limited to any command

The environment variables can be overridden by explicitly declaring new value.

> [!TIP]
> Save the variables in a `.env` file in your current directory or export them in your `~/.zshrc` file.
> To load previous conversations from a `.txt` file, use the `-fp` or `--filepath` flag. If no flag is passed, the default one will be used. To load context from a file without altering its content, use the `--retain-file` flag.

## Dynamic Provider & Further Interfaces

Version **0.4.6** also introduces dynamic provider called `g4fauto`, which represents the fastest working g4f-based provider.

> [!TIP]
> To launch web interface for g4f-based providers simply run `$ pytgpt gpt4free gui`.
> `$ pytgpt api run` will start the REST-API. Access docs and redoc at */docs* and */redoc* respectively.
To launch the web interface for g4f-based providers, execute the following command in your terminal:

```bash
$ pytgpt gpt4free gui
```

This command initializes the Web-user interface for interacting with g4f-based providers.

To start the REST-API:

```bash
$ pytgpt api run
```

This command starts the RESTful API server, enabling you to interact with the service programmatically.

For accessing the documentation and redoc, navigate to the following paths in your web browser:
- Documentation: `/docs`
- ReDoc: `/redoc`

## Speech Synthesis

To enable speech synthesis of responses, ensure you have either the [VLC player](https://www.videolan.org/vlc/index.html) installed on your system or, if you are a [Termux](https://termux.org) user, the [Termux:API](https://wiki.termux.com/wiki/Termux:API) package.

To activate speech synthesis, use the `--talk-to-me` flag or its shorthand `-ttm` when running your commands. For example:
```bash
$ pytgpt generate "Generate an ogre story" --talk-to-me
```
or
```bash
$ pytgpt interactive -ttm
```
This flag instructs the system to audiolize the ai responses and then play them, enhancing the user experience by providing auditory feedback.

Version **0.6.4** introduces another dynamic provider, `auto`, which denotes the working provider **overall**. This relieves you of the workload of manually checking a working provider each time you fire up pytgpt. However, `auto` as a provider does not work so well with streaming responses, so probably you would need to sacrifice performance for the sake of reliability.

## [Telegram Bot](https://github.com/Simatwa/pytgpt-bot)

If you're not satisfied with the existing interfaces, [pytgpt-bot](https://github.com/Simatwa/pytgpt-bot) could be the solution you're seeking. This bot is designed to enhance your experience by offering a wide range of functionalities. Whether you're interested in engaging in AI-driven conversations, creating images and audio from text, or exploring other innovative features, [pytgpt-bot is equipped to meet your needs.](https://github.com/Simatwa/pytgpt-bot)

The bot is maintained as a separate project so you just have to execute a command to get it installed :

```
$ pip install pytgpt-bot
```

Usage : `pytgpt bot run <bot-api-token>`

Or you can simply interact with the one running now as [@pytgpt-bot](https://t.me/pytgpt_bot)

<details>

<summary>

For more usage info run `$ pytgpt --help`

</summary>

```
Usage: pytgpt [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version  Show the version and exit.
  -h, --help     Show this message and exit.

Commands:
  api          FastAPI control endpoint
  awesome      Perform CRUD operations on awesome-prompts
  bot          Telegram bot interface control
  generate     Generate a quick response with AI
  gpt4free     Discover gpt4free models, providers etc
  imager       Generate images with pollinations.ai
  interactive  Chat with AI interactively (Default)
  utils        Utility endpoint for pytgpt
  webchatgpt   Reverse Engineered ChatGPT Web-Version
```

</details>

### API Health Status

| No. | API | Status |
|--------|-----|--------|
| 1. | [On-render](https://python-tgpt.onrender.com)  | [cron-job](https://pqfzhmvz.status.cron-job.org/) |


## [CHANGELOG](https://github.com/Simatwa/python-tgpt/blob/main/docs/CHANGELOG.md)

## Acknowledgements

1. [x] [tgpt](https://github.com/aandrew-me/tgpt)
2. [x] [gpt4free](https://github.com/xtekky/gpt4free)
