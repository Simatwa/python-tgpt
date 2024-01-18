<p align="center">
<img src="https://github.com/Simatwa/python-tgpt/blob/main/assets/py-tgpt.png?raw=true" width='40%'>
</p>

<!-- <h1 align="center"> python-tgpt </h1> -->
<p align="center">
<!--
<a href="https://github.com/Simatwa/python-tgpt/actions/workflows/python-test.yml"><img src="https://github.com/Simatwa/python-tgpt/actions/workflows/python-test.yml/badge.svg" alt="Python Test"/></a>
-->
<a href="https://github.com/Simatwa/python-tgpt/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/static/v1?logo=GPL&color=Blue&message=MIT&label=License"/></a>
<a href="https://pypi.org/project/python-tgpt"><img alt="PyPi" src="https://img.shields.io/static/v1?logo=pypi&label=Pypi&message=0.3.0&color=green"/></a>
<a href="https://github.com/psf/black"><img alt="Black" src="https://img.shields.io/static/v1?logo=Black&label=Code-style&message=Black"/></a>
<a href="#"><img alt="Passing" src="https://img.shields.io/static/v1?logo=Docs&label=Docs&message=Passing&color=green"/></a>
<a href="https://github.com/Simatwa/python-tgpt/actions/workflows/python-package.yml"><img src="https://github.com/Simatwa/python-tgpt/actions/workflows/python-package.yml/badge.svg"/></a>
<a href="#"><img alt="coverage" src="https://img.shields.io/static/v1?logo=Coverage&label=Coverage&message=90%&color=yellowgreen"/></a>
<a href="#" alt="progress"><img alt="Progress" src="https://img.shields.io/static/v1?logo=Progress&label=Progress&message=95%&color=green"/></a>
<a href="https://pepy.tech/project/tgpt2"><img src="https://static.pepy.tech/personalized-badge/tgpt2?period=total&units=international_system&left_color=grey&right_color=green&left_text=Downloads" alt="Downloads"></a>
<a href="https://pepy.tech/project/python-tgpt"><img src="https://static.pepy.tech/personalized-badge/python-tgpt?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads" alt="Downloads"></a>
<!--<a href="https://github.com/Simatwa/python-tgpt/releases"><img src="https://img.shields.io/github/downloads/Simatwa/python-tgpt/total?label=Downloads&color=success" alt="Downloads"></img></a> -->
<a href="https://github.com/Simatwa/python-tgpt/releases"><img src="https://img.shields.io/github/v/release/Simatwa/python-tgpt?color=success&label=Release&logo=github" alt="Latest release"></img></a>
<a href="https://github.com/Simatwa/python-tgpt/releases"><img src="https://img.shields.io/github/release-date/Simatwa/python-tgpt?label=Release date&logo=github" alt="release date"></img></a>
<a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com/Simatwa/python-tgpt"/></a>      
<a href="https://wakatime.com/badge/github/Simatwa/tgpt2"><img src="https://wakatime.com/badge/github/Simatwa/tgpt2.svg" alt="wakatime"></a>
</p>

<h3 align="center">
python-tgpt
</h3> 

<p align="center">
<img src="https://github.com/Simatwa/python-tgpt/blob/main/assets/console-demo.gif?raw=True" width='100%'/>
</p>


```python
>>> from pytgpt.leo import LEO
>>> bot = LEO()
>>> bot.chat('Hello there')
"  Hello! It's nice to meet you. Is there something I can help you with or would you like to chat?"
>>> 
```

This project enables seamless interaction with free LLMs without requiring an API Key.

The name *python-tgpt* draws inspiration from its parent project [tgpt](https://github.com/aandrew-me/tgpt), which operates on [Golang](https://go.dev/). Through this Python adaptation, users can effortlessly engage with a number of free LLMs available as well as OpenAI's Chapytgpt models, fostering a smoother AI interaction experience.

### Features

- 🗨️ Enhanced conversational chat experience
- 💾 Capability to save prompts and responses (Conversation)
- 🔄 Ability to load previous conversations
- ⌨️ Command-line interface
- 🐍 Python package
- 🌊 Stream and non-stream response
- 🚀 Ready to use (No API key required)
- ⛓️ Chained requests via proxy
- 🤖 Pass [awesome-chapytgpt prompts](https://github.com/f/awesome-chapytgpt-prompts) easily
- 🧠 Multiple LLM providers

## Providers

These are simply the hosts of the LLMs, which include:

1. [Leo](https://brave.com/leo/) - **Brave**
2. [FakeOpen](https://chat.geekgpt.org/)
3. Koboldai
4. [OpenGPTs](https://opengpts-example-vz4y4ooboq-uc.a.run.app/)
5. [OpenAI](https://chat.openai.com) *(API key required)*
6. [WebChatGPT](https://github.com/Simatwa/WebChatGPT) - **OpenAI** *(Session ID required)*
7. [Bard](https://github.com/acheong08/bard) - **Google** *(Session ID required)*

## Prerequisites

- [x] [Python>=3.9](https://python.org) *(Optional)*

## Installation and Usage

### Installation

Download binaries for your system from [here.](https://github.com/Simatwa/python-tgpt/releases/latest/)

Alternatively, you can install non-binaries. *(Recommended)*

Choose one of the following methods to get started.

1. From PyPI:

   ```bash
   pip install --upgrade python-tgpt
   ```

2. Directly from the source:

   ```bash
   pip install git+https://github.com/Simatwa/python-tgpt.git
   ```

3. Clone and Install:

   ```bash
   git clone https://github.com/Simatwa/python-tgpt.git
   cd python-tgpt
   pip install .
   ```

## Usage

This package offers a convenient command-line interface.

> **Note** : `leo` is the default *provider*.

- For a quick response:
  ```bash
  python -m pytgpt generate "<Your prompt>"
  ```

- For interactive mode:
  ```bash
  python -m pytgpt interactive "<Kickoff prompt (though not mandatory)>"
  ```

Make use of flag `--provider` postfixed with the provider name of your choice. e.g `--provider koboldai`

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

> **Note** : All providers have got a common class methods.

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

**Note**: Commencing from [v0.1.0](https://github.com/Simatwa/python-tgpt/releases/), the default mode of interaction is conversational. This mode enhances the interactive experience, offering better control over the chat history. By associating previous prompts and responses, it tailors conversations for a more engaging experience.

You can still disable the mode:

```python
bot = koboldai.KOBOLDAI(is_conversation=False)
```

Utilize the `--disable-conversation` flag in the console to achieve the same functionality.

> **Warning** : **Bard** and **WebChatGPT** autohandles context due to the obvious reason; the `is_conversation` parameter is not necessary at all hence not required when initializing the respective classes.

### Advanced Usage of Placeholders

The `generate` functionality has been enhanced starting from *v0.3.0* to enable comprehensive utilization of the `--with-copied` option and support for accepting piped inputs. This improvement introduces placeholders, offering dynamic values for more versatile interactions.

| Placeholder | Represents |
| ------------ | ----------- |
| `{{stream}}` | The piped input |
| `{{copied}}` | The last copied text |

This feature is particularly beneficial for intricate operations. For example:

```bash
$ git diff | pytgpt generate "Here is a diff file: {{stream}} Make a concise commit message from it, aligning with my commit message history: {{copied}}" -p fakeopen --with-copied --shell --new
```
> In this illustration, `{{stream}}` denotes the result of the `$ git diff` operation, while `{{copied}}` signifies the content copied from the output of the `$ git log` command.

For more usage info run `$ pytgpt --help`

## [CHANGELOG](https://github.com/Simatwa/python-tgpt/blob/main/docs/CHANGELOG.md)

## Acknowledgements

1. [x] [tgpt](https://github.com/aandrew-me/tgpt)
2. [x] You