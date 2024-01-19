## v0.0.1

**What's new?**

- Initial release.

## v0.0.2

**What's new?**

- Enhanced response generation
- Prompt optimizers added - *[code, shell_command]*
- Prompt optimizers added - *Console*
- Clear console  - *Console*

## v0.0.3

**What's new?**

- Busy bar index bug **fixed** - *(Console)*
- Other minor fixed.

## v0.0.4

**What's new?**

- Minor fixes 

## v0.0.5

**What's new?**

- Multiple variables renamed.
- First release under `python-tgpt`

## v0.0.6

**What's new?**

- `generate` is the default command. Thanks to @sameedzahoor
- Control response framing `--quiet`
- `generate` based prompt optimizaion - `--code` & `--shell`

## v0.0.7

**What's new?**

- Chat conversationally - *(Experimental)*
- Maintain chat history *.txt*
- Load chat history from file
- Chain request through *proxies*

## v0.0.8

**What's new?**

- Reading piped input as prompt - *(Console)*. Thanks to @sameedzahoor
- Reset conversation - *(Console)*
- View conversation history - *(Console)*
- Other minor fixes

## v0.0.9

**What's new?**

- Chatting conversationally - **Stable**

## v0.1.0

**What's new?**

- Chatting conversationally - **Default Mode**

## v0.1.1

**What's new?**

- Bug fixed - *file not found error*

## v0.1.2

**What's new?**

- Check version - `--version`
- Minor fixes.

## v0.1.3

**What's new?**

- Invalid response - **fixed**

## v0.1.4

**What's new?**

- Incomplete response - **fixed**

## v0.2.0

**What's new?**

- Multiple LLM providers

## v0.2.1

**What's new?**

- Fakeopen rendering issue fixed - [#7](https://github.com/Simatwa/python-tgpt/issues/7)

## v0.2.2

**What's new?**

- Package renamed to **pytgpt** - [#7](https://github.com/Simatwa/python-tgpt/issues/7)
- Visible vertical overflow - [#7](https://github.com/Simatwa/python-tgpt/issues/7)

## v0.2.3

**What's new?**

- Tabulated help info - `h`
- Control response vertical overflow behaviour.

## v0.2.4

**What's new?**

- [WebChatGPT](https://github.com/Simatwa/WebChatGPT/) added as provider
- Awesome-prompts manipulation commands = **CRUD**
- Other minor fixes.

## v0.2.5

**What's new?**

- New provider : [Bard](https://github.com/acheong08/bard) by **Google**.
- Check whole last response
- Other minor fixes.

## v0.2.6

**What's new?**

- Bug fixed - *reset conversation*  - **bard**
- Bug fixed - *low `httpx` logging level*. - **bard** 

## v0.2.7

**What's new?**

- Busy bar disabled when `--quiet` issued in *generate* mode. #12 Thanks to @johnd0e
- `interactive` takes action on `$ pytgpt` otherwise one has to explictly declare the action. #11

## v0.2.8

**What's new?**

- Auto-quiet on output redirection. Thanks to @johnd0e
- Dropped support for sourcing prompt from `stdin stream` in Windows. #12
- Colorized command prompt. <kbd>interactive</kbd>

## v0.2.9

**What's new?**

- Improved command prompt - *icon & color blending*
- Bug fixed - *multiline prompt in `interactive`*

## v0.3.0

**what's new?**

<details>

<summary>

- Improved introductory prompt

</summary>

*You're a Large Language Model for chatting with people.
Assume role of the LLM and give your response.*

</details>

- Combine both of piped and explicitly issued prompt #13
- Support piping input in Windows. #13
- Placeholder for piped input `{{stream}}` and copied text `{{copied}}`. 

## v0.3.1

**What's new?**

<details>

<summary>

41 New models. Thanks to [gpt4free](https://github.com/xtekky/gpt4free).

</summary>

 - AiChatOnline
 - Aura
 - Bard
 - Bing
 - ChatBase
 - ChatForAi
 - Chatgpt4Online
 - ChatgptAi
 - ChatgptDemo
 - ChatgptNext
 - Chatxyz
 - DeepInfra
 - FakeGpt
 - FreeChatgpt
 - GPTalk
 - GeekGpt
 - GeminiProChat
 - Gpt6
 - GptChatly
 - GptForLove
 - GptGo
 - GptTalkRu
 - Hashnode
 - HuggingChat
 - Koala
 - Liaobots
 - Llama2
 - MyShell
 - OnlineGpt
 - OpenaiChat
 - PerplexityAi
 - Phind
 - Pi
 - Poe
 - Raycast
 - TalkAi
 - Theb
 - ThebApi
 - You
 - Yqcloud

</details>

- **Aura** is the default provider
- Other minor fixes.