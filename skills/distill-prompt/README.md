# distill-prompt — Distill a prompt

[中文](README.zh-CN.md)

Reverse-engineers a successful result into one or more reusable, copy-paste prompts (a two-line header; a body in four parts: purpose, input, rules, output format; plain text) so the same result can be reproduced later with as little back-and-forth as possible.

The skill and the prompt are written in Chinese and answer in Chinese; the trigger phrases are Chinese too.

## Contents

| File | What it is |
| --- | --- |
| `SKILL.md` | The skill: when it applies and the rules it follows |
| `prompt.md` | The same rules as a prompt to paste into any AI chat |

## Usage

As a skill (claude.ai, the Claude app, or another assistant that supports Agent Skills):

1. Download the latest `distill-prompt-vYYYY.MM.DD.zip` from [Releases](https://github.com/walkwithedi/prompt-kit/releases) (it holds a `distill-prompt/` folder with `SKILL.md`).
2. Upload the zip on the Skills page of claude.ai settings and turn it on.
3. In a chat, say one of 「提炼成提示词」「固化成提示词」「把这次做法写成提示词」 and give the material to work on.

As a prompt: open [`prompt.md`](prompt.md), copy everything in the code block and paste it into any AI chat.

Both versions follow the same rules and are changed together.

## Changes

- First open-source release.
