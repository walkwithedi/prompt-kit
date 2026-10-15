# distill-prompt — 提炼可复用提示词

[English](README.md)

把一次成功的产出逆向提炼成一个或多个可直接复制使用的通用提示词（说明两行，正文分用途、材料、规则、输出格式四部分，纯文本），今后最少交互就能稳定复现同等效果。

## 目录内容

| 文件 | 说明 |
| --- | --- |
| `SKILL.md` | skill 本体：触发条件与执行规则 |
| `prompt.md` | 通用提示词版，可复制到任意 AI 对话框使用 |

## 使用方法

作为 skill（claude.ai、Claude App，或其他支持 Agent Skills 的助手）：

1. 从 [Releases](https://github.com/walkwithedi/prompt-kit/releases) 下载最新的 `distill-prompt-vYYYY.MM.DD.zip`（顶层为 `distill-prompt/` 目录，内含 `SKILL.md`）。
2. 在 claude.ai 设置的 Skills 页面上传该 zip 并启用。
3. 在对话里说「提炼成提示词」「固化成提示词」「把这次做法写成提示词」等，并给出要处理的内容。

作为提示词：打开 [`prompt.md`](prompt.md)，复制代码块里的全部文字，粘贴到任意 AI 对话框。

两个版本规则相同，修改时须保持一致。

## 版本说明

- 首个开源版本。
