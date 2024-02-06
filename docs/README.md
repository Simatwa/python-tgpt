<p align="center">
<img src="https://github.com/Simatwa/python-tgpt/blob/main/assets/py-tgpt.png?raw=true" width='40%'>
</p>

<!-- <h1 align="center"> python-tgpt </h1> -->
<p align="center">
<!--
<a href="https://github.com/Simatwa/python-tgpt/actions/workflows/python-test.yml"><img src="https://github.com/Simatwa/python-tgpt/actions/workflows/python-test.yml/badge.svg" alt="Python Test"/></a>
-->
<a href="https://github.com/Simatwa/python-tgpt/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/static/v1?logo=GPL&color=Blue&message=MIT&label=License"/></a>
<a href="https://pypi.org/project/python-tgpt"><img alt="PyPi" src="https://img.shields.io/pypi/v/python-tgpt?color=green"/></a>
<a href="https://github.com/psf/black"><img alt="Black" src="https://img.shields.io/static/v1?logo=Black&label=Code-style&message=Black"/></a>
<a href="#"><img alt="Passing" src="https://img.shields.io/static/v1?logo=Docs&label=Docs&message=Passing&color=green"/></a>
<a href="https://github.com/Simatwa/python-tgpt/actions/workflows/python-package.yml"><img alt="Python Package flow" src="https://github.com/Simatwa/python-tgpt/actions/workflows/python-package.yml/badge.svg?branch=master"/></a>
<a href="#"><img alt="coverage" src="https://img.shields.io/static/v1?logo=Coverage&label=Coverage&message=90%&color=yellowgreen"/></a>
<a href="#" alt="progress"><img alt="Progress" src="https://img.shields.io/static/v1?logo=Progress&label=Progress&message=95%&color=green"/></a>
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

This project enables seamless interaction with over **45 free LLM providers** without requiring an API Key.

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

## Providers

These are simply the hosts of the LLMs, which include:

1. [Leo](https://brave.com/leo/) - **Brave**
2. [FakeOpen](https://chat.geekgpt.org/)
3. Koboldai
4. [OpenGPTs](https://opengpts-example-vz4y4ooboq-uc.a.run.app/)
5. [OpenAI](https://chat.openai.com) *(API key required)*
6. [WebChatGPT](https://github.com/Simatwa/WebChatGPT) - **OpenAI** *(Session ID required)*
7. [Bard](https://github.com/acheong08/bard) - **Google** *(Session ID required)*
8. [Phind](https://www.phind.com) - *default*
9. [Llama2](https://www.llama2.ai)
10. [Blackboxai](https://www.blackbox.ai)

<details>

<summary>

41+ Other models proudly offered by [gpt4free](https://github.com/xtekky/gpt4free).

</summary>

 - AiChatOnline
 - [Aura](https://openchat.team)
 - [Bard](https://bard.google.com/)
 - [Bing](https://bing.com)
 - [ChatBase](https://www.chatbase.co/)
 - [ChatForAi](https://chatforai.store/)
 - [Chatgpt4Online](https://chatgpt4online.org)
 - [ChatgptAi](https://chatgpt.ai/)
 - [ChatgptDemo](https://chat.chatgptdemo.net)
 - [ChatgptNext](https://www.chatgpt-free.c)
 - [Chatxyz](https://chat.3211000.xyz)
 - [DeepInfra](https://deepinfra.co)
 - [FakeGpt](https://chat-shared2.zhile.io/)
 - [FreeChatgpt](https://free.chatgpt.org.uk)
 - [GPTalk](https://gptalk.net/)
 - [GeekGpt](https://chat.geekgpt.org)
 - [GeminiProChat](https://geminiprochat.com)
 - Gpt6
 - [GptChatly](https://gptchatly.com)
 - [GptForLove](https://ai18.gptforlove.com/)
 - [GptGo](https://gptgo.ai/)
 - GptTalkRu
 - [Hashnode](https://hashnode.com/)
 - [HuggingChat](https://huggingface.co/chat)
 - Koala
 - [Liaobots](https://liaobots.site)
 - [Llama2](https://www.llama2.ai/)
 - [MyShell](https://app.myshell.ai/chat)
 - OnlineGpt
 - OpenaiChat
 - PerplexityAi
 - [Phind](https://www.phind.com)
 - Pi
 - Poe
 - [Raycast](https://raycast.com)
 - TalkAi
 - [Theb](https://theb.ai/)
 - ThebApi
 - [You](https://you.com/)
 - [Yqcloud](https://chat9.yqcloud.top/)

 <details>

 <summary>
 
All models. *(Include not working)*

 </summary>

1. [AItianhu](https://www.aitianhu.com)
2. [AItianhuSpace](https://chat3.aiyunos.top/)
3. [Acytoo](https://chat.acytoo.com)
4. [AiAsk](https://e.aiask.me)
5. [AiChatOnline](https://aichatonline.org)
6. [AiChatting](https://www.aichatting.net)
7. [AiService](https://aiservice.vercel.app/)
8. [Aibn](https://aibn.cc)
9. [Aichat](https://chat-gpt.org/chat)
10. [Ails](https://ai.ls)
11. [Aivvm](https://chat.aivvm.com)
12. AsyncGeneratorProvider
13. AsyncProvider
14. [Aura](https://openchat.team)
15. [Bard](https://bard.google.com)
16. BaseProvider
17. [Berlin](https://ai.berlin4h.top)
18. [Bestim](https://chatgpt.bestim.org)
19. [Bing](https://bing.com/chat)
20. [ChatAiGpt](https://chataigpt.org)
21. [ChatAnywhere](https://chatanywhere.cn)
22. [ChatBase](https://www.chatbase.co)
23. [ChatForAi](https://chatforai.store)
24. [Chatgpt4Online](https://chatgpt4online.org)
25. [ChatgptAi](https://chatgpt.ai)
26. [ChatgptDemo](https://chat.chatgptdemo.net)
27. [ChatgptDemoAi](https://chat.chatgptdemo.ai)
28. [ChatgptDuo](https://chatgptduo.com)
29. [ChatgptFree](https://chatgptfree.ai)
30. [ChatgptLogin](https://chatgptlogin.ai)
31. [ChatgptNext](https://www.chatgpt-free.cc)
32. [ChatgptX](https://chatgptx.de)
33. [Chatxyz](https://chat.3211000.xyz)
34. [CodeLinkAva](https://ava-ai-ef611.web.app)
35. CreateImagesProvider
36. [Cromicle](https://cromicle.top)
37. [DeepInfra](https://deepinfra.com)
38. [DfeHub](https://chat.dfehub.com/)
39. [EasyChat](https://free.easychat.work)
40. [Equing](https://next.eqing.tech/)
41. [FakeGpt](https://chat-shared2.zhile.io)
42. [FastGpt](https://chat9.fastgpt.me/)
43. [Forefront](https://forefront.com)
44. [FreeChatgpt](https://free.chatgpt.org.uk)
45. [FreeGpt](https://freegpts1.aifree.site/)
46. [GPTalk](https://gptalk.net)
47. [GeekGpt](https://chat.geekgpt.org)
48. [GeminiProChat](https://geminiprochat.com)
49. [GetGpt](https://chat.getgpt.world/)
50. [Gpt6](https://gpt6.ai)
51. [GptChatly](https://gptchatly.com)
52. [GptForLove](https://ai18.gptforlove.com)
53. [GptGo](https://gptgo.ai)
54. [GptGod](https://gptgod.site)
55. [GptTalkRu](https://gpttalk.ru)
56. [H2o](https://gpt-gm.h2o.ai)
57. [Hashnode](https://hashnode.com)
58. [HuggingChat](https://huggingface.co/chat)
59. [Koala](https://koala.sh)
60. [Komo](https://komo.ai/api/ask)
61. [Liaobots](https://liaobots.site)
62. [Llama2](https://www.llama2.ai)
63. [Lockchat](http://supertest.lockchat.app)
64. [MikuChat](https://ai.okmiku.com)
65. [MyShell](https://app.myshell.ai/chat)
66. [Myshell](https://app.myshell.ai/chat)
67. [OnlineGpt](https://onlinegpt.org)
68. [Opchatgpts](https://opchatgpts.net)
69. [OpenAssistant](https://open-assistant.io/chat)
70. [OpenaiChat](https://chat.openai.com)
71. [PerplexityAi](https://www.perplexity.ai)
72. [Phind](https://www.phind.com)
73. [Pi](https://pi.ai/talk)
74. [Poe](https://poe.com)
75. [Raycast](https://raycast.com)
76. RetryProvider
77. [TalkAi](https://talkai.info)
78. [Theb](https://beta.theb.ai)
79. [ThebApi](https://theb.ai)
80. [V50](https://p5.v50.ltd)
81. [Vercel](https://sdk.vercel.ai)
82. [Vitalentum](https://app.vitalentum.io)
83. [Wewordle](https://wewordle.org)
84. [Wuguokai](https://chat.wuguokai.xyz)
85. [Ylokh](https://chat.ylokh.xyz)
86. [You](https://you.com)
87. [Yqcloud](https://chat9.yqcloud.top/)
 
 </details>

</details>

## Prerequisites

- [x] [Python>=3.9](https://python.org) *(Optional)*

## Installation and Usage

### Installation

Download binaries for your system from [here.](https://github.com/Simatwa/python-tgpt/releases/latest/)

Alternatively, you can install non-binaries. *(Recommended)*

1. Developers:

   ```sh
   pip install python-tgpt
   ```

2. Commandline:

   ```sh
   pip install python-tgpt[cli]
   ```

3. Full installation:

   ```sh
   pip install python-tgpt[all]
   ```

## Usage

This package offers a convenient command-line interface.

> **Note** : `phind` is the default *provider*.

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

**Note**: Commencing from [v0.1.0](https://github.com/Simatwa/python-tgpt/releases/), the default mode of interaction is conversational. This mode enhances the interactive experience, offering better control over the chat history. By associating previous prompts and responses, it tailors conversations for a more engaging experience.

You can still disable the mode:

```python
bot = koboldai.KOBOLDAI(is_conversation=False)
```

Utilize the `--disable-conversation` flag in the console to achieve the same functionality.

> **Warning** : **Bard** autohandles context due to the obvious reason; the `is_conversation` parameter is not necessary at all hence not required when initializing the class. Also be informed that majority of providers offered by *gpt4free* requires *Google Chrome* inorder to function.

### Advanced Usage of Placeholders

The `generate` functionality has been enhanced starting from *v0.3.0* to enable comprehensive utilization of the `--with-copied` option and support for accepting piped inputs. This improvement introduces placeholders, offering dynamic values for more versatile interactions.

| Placeholder | Represents |
| ------------ | ----------- |
| `{{stream}}` | The piped input |
| `{{copied}}` | The last copied text |

This feature is particularly beneficial for intricate operations. For example:

```bash
$ git diff | pytgpt generate "Here is a diff file: {{stream}} Make a concise commit message from it, aligning with my commit message history: {{copied}}" -p fakeopen --shell --new
```
> In this illustration, `{{stream}}` denotes the result of the `$ git diff` operation, while `{{copied}}` signifies the content copied from the output of the `$ git log` command.

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
3. [x] You