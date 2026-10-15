# fact-check — 言论事实核查

[English](README.md)

对一段言论或一张图片做去情绪化的真伪判断与逻辑拆解，按核心定性、事实核查、逻辑推演、话术与传播特征、最终结论输出，不写客套话和免责声明。

## 目录内容

| 文件 | 说明 |
| --- | --- |
| `SKILL.md` | skill 本体：触发条件与执行规则 |
| `prompt.md` | 通用提示词版，可复制到任意 AI 对话框使用 |

## 使用方法

作为 skill（claude.ai、Claude App，或其他支持 Agent Skills 的助手）：

1. 从 [Releases](https://github.com/walkwithedi/prompt-kit/releases) 下载最新的 `fact-check-vYYYY.MM.DD.zip`（顶层为 `fact-check/` 目录，内含 `SKILL.md`）。
2. 在 claude.ai 设置的 Skills 页面上传该 zip 并启用。
3. 在对话里说「事实核查」「核查这段话」「这话靠谱吗」「分析这段言论」等，并给出要处理的内容。

作为提示词：打开 [`prompt.md`](prompt.md)，复制代码块里的全部文字，粘贴到任意 AI 对话框。

两个版本规则相同，修改时须保持一致。

## 版本说明

- 首个开源版本。
