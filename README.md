# prompt-kit

[中文](README.zh-CN.md)

Chinese-language Claude skills and copy-paste prompts. Each skill comes in two versions that follow the same rules:

- **Skill** (`SKILL.md`): upload it to claude.ai or the Claude app and trigger it with its phrase; it also works with other assistants that support Agent Skills.
- **Prompt** (`prompt.md`): paste it into any AI chat; no platform or script needed.

The skills and prompts are written in Chinese, answer in Chinese and are triggered by Chinese phrases.

## Skills

| Skill | Name | Trigger phrases |
| --- | --- | --- |
| [clarify-needs](skills/clarify-needs/README.md) | Clarify needs | 「先问我问题」「先澄清需求」「需求澄清」「问清楚再做」 |
| [topic-analysis](skills/topic-analysis/README.md) | Topic analysis | 「深度分析」「话题深度分析」「八步分析」「理性拆解一下」 |
| [fact-check](skills/fact-check/README.md) | Fact check | 「事实核查」「核查这段话」「这话靠谱吗」「分析这段言论」 |
| [distill-prompt](skills/distill-prompt/README.md) | Distill a prompt | 「提炼成提示词」「固化成提示词」「把这次做法写成提示词」 |
| [work-text-trim](skills/work-text-trim/README.md) | Work message trim | 「精简一下」「职场文本优化」「帮我改这段工作消息」「去掉推导只留结论」 |

## Usage

**As a skill**

1. Download `<skill>.zip` from the [latest release](https://github.com/walkwithedi/prompt-kit/releases/latest), or `<skill>-vYYYY.MM.DD.zip` from that skill's own release (either holds a `<skill>/` folder with `SKILL.md`).
2. Upload the zip on the Skills page of claude.ai settings and turn it on.
3. Say a trigger phrase in a chat and give the material to work on.

Claude Code and other terminal assistants: copy `skills/<skill>/` into the assistant's skills folder (for example `~/.claude/skills/`).

**Everything at once**

Download `prompt-kit-vYYYY.MM.DD.zip` from [Releases](https://github.com/walkwithedi/prompt-kit/releases): every skill folder (`SKILL.md`, `prompt.md`, READMEs) laid out as in this repository under `prompt-kit/`. For claude.ai, upload the single-skill zips above instead.

**As a prompt**

Open `prompt.md` in the skill's folder, copy everything in the code block and paste it into a chat; put any material after the 「材料」 line.

## Releases

Every merge to main releases each changed skill as `<skill>-vYYYY.MM.DD` with that skill's zip attached, and, when any skill, the root READMEs or LICENSE changed, the whole kit as `prompt-kit-vYYYY.MM.DD` with every skill's `<skill>.zip` attached (marked latest).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security problems: [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE)
