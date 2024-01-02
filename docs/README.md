<h1 align="center"> python-tgpt </h1>

<p align="center">
<!--
<a href="https://github.com/Simatwa/python-tgpt/actions/workflows/python-test.yml"><img src="https://github.com/Simatwa/python-tgpt/actions/workflows/python-test.yml/badge.svg" alt="Python Test"/></a>
-->
<a href="https://github.com/Simatwa/python-tgpt/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/static/v1?logo=GPL&color=Blue&message=MIT&label=License"/></a>
<a href="https://pypi.org/project/python-tgpt"><img alt="PyPi" src="https://img.shields.io/static/v1?logo=pypi&label=Pypi&message=v0.0.7&color=green"/></a>
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

<p align="center">
AI for all
</p> 

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

This project allows you to interact with AI ([LLaMA](https://ai.meta.com/llama/)) without API Key.

The name *python-tgpt* is inherited from it's parent project [tgpt](https://github.com/aandrew-me/tgpt) which runs on [golang](https://go.dev/).

## Prerequisite

- [x] [Python>=3.9](https://python.org)

## Installation and usage

### Installation

Pick either of the following ways to get started.

1. From pypi:

```
pip install python-tgpt
```

2. Direct from source

```
pip install git+https://github.com/Simatwa/python-tgpt.git
```

3. Clone and Install

```
git clone https://github.com/Simatwa/python-tgpt.git
cd python-tgpt
pip install .
```

## Usage

This package features a ready to use commandline interface.

- Quick response
   `python -m tgpt generate "<Your prompt>"`

- Interactive mode 
   `python -m tgpt interactive "<Kickoff prompt though not a must>"`

Instead of `python -m tgpt`, you can as well just use `tgpt`

As from [version 0.0.6](https://github.com/Simatwa/python-tgpt/releases), `generate` is the default command. So something like this will still work. `tgpt "<Your prompt>"`

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

- To get better feedback, you can make use of [optimizers](tgpt/utils.py) using parameter `optimizer` with values *(code or system_command)*

</summary>

```python
from tgpt import TGPT
bot = TGPT()
resp = bot.ask('<Your Prompt>', optimizer='code')
print(resp)
```

</details>


> **Note** : As of [v0.0.7](https://github.com/Simatwa/python-tgpt/releases/), chatting conversationally has been featured *(Experimental)* : `bot = tgpt.TGPT(is_conversation=True)` at console just append flag `--conversation`. NB: *Tends to fail after relative lengthy chat.*

## Acknowledgements

1. [x] [tgpt](https://github.com/aandrew-me/tgpt)
2. [x] You

