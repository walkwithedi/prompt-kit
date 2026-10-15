# clarify-needs — Clarify needs

[中文](README.zh-CN.md)

When a request is vague, asks one multiple-choice question at a time before doing the work. The first option of each question is a recommended answer with a one-line reason; anything that can be looked up in the conversation, uploaded files or available sources is looked up rather than asked; questions follow the dependencies between decisions; at most 20 questions, then a summary of the needs to confirm before the task starts.

The skill and the prompt are written in Chinese and answer in Chinese; the trigger phrases are Chinese too.

## Contents

| File | What it is |
| --- | --- |
| `SKILL.md` | The skill: when it applies and the rules it follows |
| `prompt.md` | The same rules as a prompt to paste into any AI chat |

## Usage

As a skill (claude.ai, the Claude app, or another assistant that supports Agent Skills):

1. Download the latest `clarify-needs-vYYYY.MM.DD.zip` from [Releases](https://github.com/walkwithedi/prompt-kit/releases) (it holds a `clarify-needs/` folder with `SKILL.md`).
2. Upload the zip on the Skills page of claude.ai settings and turn it on.
3. In a chat, say one of 「先问我问题」「先澄清需求」「需求澄清」「问清楚再做」 and give the material to work on.

As a prompt: open [`prompt.md`](prompt.md), copy everything in the code block and paste it into any AI chat.

Both versions follow the same rules and are changed together.

## Changes

- First open-source release.
