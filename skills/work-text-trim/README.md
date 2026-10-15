# work-text-trim — Work message trim

[中文](README.zh-CN.md)

For work messages between colleagues, managers and friends: trims each point to what is new, drops the reasoning and keeps the conclusions, keeps one name for each subject, stays friendly rather than formal and leaves proper nouns untouched. Outputs only the revised plain text, followed by any typos and punctuation problems found.

The skill and the prompt are written in Chinese and answer in Chinese; the trigger phrases are Chinese too.

## Contents

| File | What it is |
| --- | --- |
| `SKILL.md` | The skill: when it applies and the rules it follows |
| `prompt.md` | The same rules as a prompt to paste into any AI chat |

## Usage

As a skill (claude.ai, the Claude app, or another assistant that supports Agent Skills):

1. Download the latest `work-text-trim-vYYYY.MM.DD.zip` from [Releases](https://github.com/walkwithedi/prompt-kit/releases) (it holds a `work-text-trim/` folder with `SKILL.md`).
2. Upload the zip on the Skills page of claude.ai settings and turn it on.
3. In a chat, say one of 「精简一下」「职场文本优化」「帮我改这段工作消息」「去掉推导只留结论」 and give the material to work on.

As a prompt: open [`prompt.md`](prompt.md), copy everything in the code block and paste it into any AI chat.

Both versions follow the same rules and are changed together.

## Changes

- First open-source release.
