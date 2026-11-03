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

Every merge to main releases each changed skill as `<skill>-vX.Y.Z` with that skill's zip attached, and, when any skill, the root READMEs or LICENSE changed, the whole kit as `prompt-kit-vX.Y.Z` with every skill's `<skill>.zip` attached (marked latest).

- The version is the newest entry of the version notes, `- vX.Y (YYYY-MM-DD): ...`, the same in README.md and README.zh-CN.md: a skill's own READMEs for the skill, the root READMEs below for the kit. Pages show vX.Y; tags add .Z.
- A higher X.Y releases vX.Y.0. An unchanged X.Y with only README changes releases vX.Y.(Z+1). A change to SKILL.md, prompt.md (or, for the kit, LICENSE) without a higher X.Y is not released, and the pull request check (`python3 scripts/run_checks.py`) fails, as it does when the English and Chinese READMEs name different versions.
- Earlier releases tagged by date (`<skill>-vYYYY.MM.DD`) stay. The previous release is found by the commit order of old and new tags, never by comparing tag names; the first release after a date tag is vX.Y.0.
- Dry run: `DRY_RUN=1 bash .github/scripts/release_skills.sh` prints the plan and builds the zips without releasing; `python3 scripts/versions.py plan --kit` prints the plan only. Both need the full history and tags.

## Version notes

- v1.0 (2026-11-03): Releases are tagged by version (`<skill>-vX.Y.Z`, `prompt-kit-vX.Y.Z`) instead of by date; every skill starts at v1.0.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security problems: [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE)

## Feedback

Send suggestions and feedback to [hong.xie.me@outlook.com](mailto:hong.xie.me@outlook.com).
