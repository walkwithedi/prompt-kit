# fact-check — Fact check

[中文](README.zh-CN.md)

Gives an unemotional verdict on a statement or image and takes it apart: a one-line verdict, the factual claims checked, the reasoning tested for fallacies, the rhetoric and spread pattern, and a short conclusion with the blind spots to watch for. No pleasantries or disclaimers.

The skill and the prompt are written in Chinese and answer in Chinese; the trigger phrases are Chinese too.

## Contents

| File | What it is |
| --- | --- |
| `SKILL.md` | The skill: when it applies and the rules it follows |
| `prompt.md` | The same rules as a prompt to paste into any AI chat |

## Usage

As a skill (claude.ai, the Claude app, or another assistant that supports Agent Skills):

1. Download the latest `fact-check-vYYYY.MM.DD.zip` from [Releases](https://github.com/walkwithedi/prompt-kit/releases) (it holds a `fact-check/` folder with `SKILL.md`).
2. Upload the zip on the Skills page of claude.ai settings and turn it on.
3. In a chat, say one of 「事实核查」「核查这段话」「这话靠谱吗」「分析这段言论」 and give the material to work on.

As a prompt: open [`prompt.md`](prompt.md), copy everything in the code block and paste it into any AI chat.

Both versions follow the same rules and are changed together.

## Changes

- First open-source release.
