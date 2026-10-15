# clarify-needs — 需求澄清提问

[English](README.md)

任务描述较笼统时，先用选择题逐个提问摸清需求再动手。每题第一个选项是附理由的推荐答案；能从已有材料查到的不问；按决定之间的依赖顺序提问；最多 20 题，最后输出需求摘要，确认后再执行。

## 目录内容

| 文件 | 说明 |
| --- | --- |
| `SKILL.md` | skill 本体：触发条件与执行规则 |
| `prompt.md` | 通用提示词版，可复制到任意 AI 对话框使用 |

## 使用方法

作为 skill（claude.ai、Claude App，或其他支持 Agent Skills 的助手）：

1. 从 [Releases](https://github.com/walkwithedi/prompt-kit/releases) 下载最新的 `clarify-needs-vYYYY.MM.DD.zip`（顶层为 `clarify-needs/` 目录，内含 `SKILL.md`）。
2. 在 claude.ai 设置的 Skills 页面上传该 zip 并启用。
3. 在对话里说「先问我问题」「先澄清需求」「需求澄清」「问清楚再做」等，并给出要处理的内容。

作为提示词：打开 [`prompt.md`](prompt.md)，复制代码块里的全部文字，粘贴到任意 AI 对话框。

两个版本规则相同，修改时须保持一致。

## 版本说明

- 首个开源版本。
