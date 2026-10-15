# prompt-kit

[English](README.md)

中文 Claude skill 与可直接复制的通用提示词。每个 skill 同时提供两个版本，规则相同：

- **skill 版**（`SKILL.md`）：上传到 claude.ai 或 Claude App，说口令即可触发；也可用于其他支持 Agent Skills 的助手。
- **提示词版**（`prompt.md`）：复制到任意 AI 对话框直接使用，不依赖任何平台或脚本。

## skill 一览

| skill | 名称 | 口令 |
| --- | --- | --- |
| [clarify-needs](skills/clarify-needs/README.zh-CN.md) | 需求澄清提问 | 「先问我问题」「先澄清需求」「需求澄清」「问清楚再做」 |
| [topic-analysis](skills/topic-analysis/README.zh-CN.md) | 话题深度分析 | 「深度分析」「话题深度分析」「八步分析」「理性拆解一下」 |
| [fact-check](skills/fact-check/README.zh-CN.md) | 言论事实核查 | 「事实核查」「核查这段话」「这话靠谱吗」「分析这段言论」 |
| [distill-prompt](skills/distill-prompt/README.zh-CN.md) | 提炼可复用提示词 | 「提炼成提示词」「固化成提示词」「把这次做法写成提示词」 |
| [work-text-trim](skills/work-text-trim/README.zh-CN.md) | 职场文本精简优化 | 「精简一下」「职场文本优化」「帮我改这段工作消息」「去掉推导只留结论」 |

## 使用方法

**作为 skill**

1. 在[最新版](https://github.com/walkwithedi/prompt-kit/releases/latest)下载 `<skill>.zip`，或在该 skill 自己的 Release 下载 `<skill>-vYYYY.MM.DD.zip`（两者顶层都是 `<skill>/` 目录，内含 `SKILL.md`）。
2. 在 claude.ai 设置的 Skills 页面上传 zip 并启用。
3. 在对话里说出口令，并给出要处理的内容。

Claude Code 等终端助手：把 `skills/<skill>/` 目录复制到助手的 skills 目录（例如 `~/.claude/skills/`）。

**一次取全部**

在 [Releases](https://github.com/walkwithedi/prompt-kit/releases) 下载 `prompt-kit-vYYYY.MM.DD.zip`：内含全部 skill 目录（`SKILL.md`、`prompt.md`、README），按本仓库结构放在 `prompt-kit/` 下。上传 claude.ai 请改用上面的单个 skill zip。

**作为提示词**

打开对应目录的 `prompt.md`，复制代码块里的全部文字，粘贴到对话框；需要材料时贴在「材料」一行后面。

## 发版

合并到 main 后，有改动的 skill 自动发布 Release「<skill>-vYYYY.MM.DD」，附件为该 skill 的 zip；任一 skill、根目录 README 或 LICENSE 有改动时，另发布全量合集「prompt-kit-vYYYY.MM.DD」，并附全部 skill 的 `<skill>.zip`（标为最新）。

## 参与

见 [CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md)。安全问题见 [SECURITY.md](SECURITY.md)。

## 许可证

[MIT](LICENSE)
