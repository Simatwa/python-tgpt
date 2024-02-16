<p align="center">
<img src="https://github.com/Simatwa/python-tgpt/blob/main/assets/py-tgpt.png?raw=true" width='40%'>
</p>

<!-- <h1 align="center"> python-tgpt </h1> -->
<p align="center">
<!--
<a href="https://github.com/Simatwa/python-tgpt/actions/workflows/python-test.yml"><img src="https://github.com/Simatwa/python-tgpt/actions/workflows/python-test.yml/badge.svg" alt="Python Test"/></a>
-->
<a href="https://github.com/Simatwa/python-tgpt/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/static/v1?logo=GPL&color=Blue&message=MIT&label=License"/></a>
<a href="#"><img alt="Python version" src="https://img.shields.io/pypi/pyversions/python-tgpt"/></a>
<a href="https://pypi.org/project/python-tgpt"><img alt="PyPi" src="https://img.shields.io/pypi/v/python-tgpt?color=green"/></a>
<a href="https://github.com/psf/black"><img alt="Black" src="https://img.shields.io/static/v1?logo=Black&label=Code-style&message=Black"/></a>
<a href="#"><img alt="Passing" src="https://img.shields.io/static/v1?logo=Docs&label=Docs&message=Passing&color=green"/></a>
<a href="https://github.com/Simatwa/python-tgpt/actions/workflows/python-package.yml"><img alt="Python Package flow" src="https://github.com/Simatwa/python-tgpt/actions/workflows/python-package.yml/badge.svg?branch=master"/></a>
<a href="#"><img alt="coverage" src="https://img.shields.io/static/v1?logo=Coverage&label=Coverage&message=90%&color=yellowgreen"/></a>
<a href="https://pepy.tech/project/tgpt2"><img src="https://static.pepy.tech/personalized-badge/tgpt2?period=total&units=international_system&left_color=grey&right_color=green&left_text=Downloads" alt="Downloads"></a>
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
>>> from pytgpt.console import main
>>> main()
Welcome to AI Chat in terminal. Type 'help' or 'h' for usage info.
Submit any bug at https://github.com/Simatwa/python-tgpt/issues/new
╭─[Smartwa@pyTGPT](phind)~[🕒04:05:55-💻00:00:00-⚡0.0s]
╰─>
"""
```

This project enables seamless interaction with over **45 free LLM providers** without requiring an API Key as well generating images.

The name *python-tgpt* draws inspiration from its parent project [tgpt](https://github.com/aandrew-me/tgpt), which operates on [Golang](https://go.dev/). Through this Python adaptation, users can effortlessly engage with a number of free LLMs available, fostering a smoother AI interaction experience.


### Features

- 🗨️ Enhanced conversational chat experience
- 💾 Capability to save prompts and responses (Conversation)
- 🔄 Ability to load previous conversations
- ⌨️ Command-line interface
- 🐍 Python package
- 🌊 Stream and non-stream response
- 🚀 Ready to use (No API key required)
- ⛓️ Chained requests via proxy
- 🤖 Pass [awesome-chatgpt prompts](https://github.com/f/awesome-chatgpt-prompts) easily
- 🧠 Multiple LLM providers - **45+**
- 🎯 Customizable script generation and execution
- 🔌 Offline support for Large Language Models
- 🎨 Image generation capabilities

## Providers

These are simply the hosts of the LLMs, which include:

1. [Leo](https://brave.com/leo/) - **Brave**
2. [Koboldai](https://koboldai-koboldcpp-tiefighter.hf.space)
3. [OpenGPTs](https://opengpts-example-vz4y4ooboq-uc.a.run.app/)
4. [OpenAI](https://chat.openai.com) *(API key required)*
5. [WebChatGPT](https://github.com/Simatwa/WebChatGPT) - **OpenAI** *(Session ID required)*
6. [Bard](https://github.com/acheong08/bard) - **Google** *(Session ID required)*
9. [Phind](https://www.phind.com) - *default*
10. [Llama2](https://www.llama2.ai)
11. [Blackboxai](https://www.blackbox.ai)
12. [gpt4all](https://gpt4all.io) *(Offline)*
13. [Poe](poe.com) - Poe|Quora *(Session ID required)*


<details>

<summary>

41+ Other models proudly offered by [gpt4free](https://github.com/xtekky/gpt4free).

</summary>

- To list working providers run:
   ```sh
   $ pytgpt gpt4free test -y
   ```
</details>

## Prerequisites

- [x] [Python>=3.9](https://python.org) *(Optional)*

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

> [!NOTE]
> All providers have got a common class methods.

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
Fakeopen

</summary>

```python
import pytgpt.fakeopen as fakeopen
bot = fakeopen.FAKEOPEN()
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
Bard

</summary>

```python
import pytgpt.bard as bard
bot = bard.BARD('<Path-to-bard.google.com.cookies.json>')
print(bot.chat("<Your-prompt>"))
```

</details>

<details>

<summary>
phind

</summary>

```python
import pytgp.phind as phind
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
bot = gpt4free.GPT4FREE(provider="Aura")
print(bot.chat("<Your-prompt>"))
```

</details>

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

This has been made possible by [pollination.ai](https://pollination.ai).
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


</details>

### Advanced Usage of Placeholders

The `generate` functionality has been enhanced starting from *v0.3.0* to enable comprehensive utilization of the `--with-copied` option and support for accepting piped inputs. This improvement introduces placeholders, offering dynamic values for more versatile interactions.

| Placeholder | Represents |
| ------------ | ----------- |
| `{{stream}}` | The piped input |
| `{{copied}}` | The last copied text |

This feature is particularly beneficial for intricate operations. For example:

```bash
$ git diff | pytgpt generate "Here is a diff file: {{stream}} Make a concise commit message from it, aligning with my commit message history: {{copied}}" --shell --new
```
> In this illustration, `{{stream}}` denotes the result of the `$ git diff` operation, while `{{copied}}` signifies the content copied from the output of the `$ git log` command.

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
> Save the variables in a `.env` file in your current directory or export the them in your `.zshrc` file.

## Dynamic Provider

Version **0.4.6** also introduces dynamic provider called `g4fauto`, which represents the fastest working g4f-based provider.

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
  awesome      Perform CRUD operations on awesome-prompts
  generate     Generate a quick response with AI
  gpt4free     Discover gpt4free models, providers etc
  interactive  Chat with AI interactively (Default)
  utils        Utility endpoint for pytgpt
  webchatgpt   Reverse Engineered ChatGPT Web-Version
```

</details>

## [CHANGELOG](https://github.com/Simatwa/python-tgpt/blob/main/docs/CHANGELOG.md)

## Acknowledgements

1. [x] [tgpt](https://github.com/aandrew-me/tgpt)
2. [x] [gpt4free](https://github.com/xtekky/gpt4free)
