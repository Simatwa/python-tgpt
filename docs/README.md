<p align="center">
<img src="https://github.com/Simatwa/python-tgpt/blob/main/assets/py-tgpt.png?raw=true" width='40%'>
</p>

<!-- <h1 align="center"> python-tgpt </h1> -->
<p align="center">
<!--
<a href="https://github.com/Simatwa/python-tgpt/actions/workflows/python-test.yml"><img src="https://github.com/Simatwa/python-tgpt/actions/workflows/python-test.yml/badge.svg" alt="Python Test"/></a>
-->
<a href="https://github.com/Simatwa/python-tgpt/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/static/v1?logo=GPL&color=Blue&message=MIT&label=License"/></a>
<a href="https://pypi.org/project/python-tgpt"><img alt="PyPi" src="https://img.shields.io/static/v1?logo=pypi&label=Pypi&message=v0.1.4&color=green"/></a>
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
>>> import tgpt
>>> bot = tgpt.TGPT()
>>> bot.chat('Hello there')
"  Hello! It's nice to meet you. Is there something I can help you with or would you like to chat?"
>>> 
```

This project enables seamless interaction with [LLaMA](https://ai.meta.com/llama/) AI without requiring an API Key.

The name *python-tgpt* draws inspiration from its parent project [tgpt](https://github.com/aandrew-me/tgpt), which operates on [Golang](https://go.dev/). Through this Python adaptation, users can effortlessly engage with LLaMA's capabilities *(alias **LEO** by Brave)*, fostering a smoother AI interaction experience.

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

- For a quick response:
  ```bash
  python -m tgpt generate "<Your prompt>"
  ```

- For interactive mode:
  ```bash
  python -m tgpt interactive "<Kickoff prompt (though not mandatory)>"
  ```

You can also simply use `tgpt` instead of `python -m tgpt`.

Starting from version 0.1.2, `generate` is the default command if you issue a prompt, and `interactive` takes action if you don't. Therefore, something like this will generate a response and exit `$ tgpt "<Your prompt>"` while `$ tgpt` will fire up an interactive prompt.

<details>

<summary>

### Developer Docs

</summary>

1. Generate a quick response

```python
from tgpt import TGPT
bot = TGPT()
resp = bot.chat('<Your prompt>')
print(resp)
# Output : How may I help you.
```

2. Get back whole response

```python
from tgpt import TGPT
bot = TGPT()
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
from tgpt import TGPT
bot = TGPT()
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
from tgpt import TGPT
bot = TGPT()
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


</details>

<details>

<summary>

To obtain more tailored responses, consider utilizing [optimizers](tgpt/utils.py) using the `optimizer` parameter. Its values can be set to either `code` or `system_command`.

</summary>

```python
from tgpt import TGPT
bot = TGPT()
resp = bot.ask('<Your Prompt>', optimizer='code')
print(resp)
```

</details>

**Note**: Commencing from [v0.1.0](https://github.com/Simatwa/python-tgpt/releases/), the default mode of interaction is conversational. This mode enhances the interactive experience, offering better control over the chat history. By associating previous prompts and responses, it tailors conversations for a more engaging experience.

You can still disable the mode:

```python
bot = tgpt.TGPT(is_conversation=False)
```

Utilize the `--disable-conversation` flag in the console to achieve the same functionality.


## Acknowledgements

1. [x] [tgpt](https://github.com/aandrew-me/tgpt)
2. [x] You

