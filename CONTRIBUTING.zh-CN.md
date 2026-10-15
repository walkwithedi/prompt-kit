# 参与贡献

[English](CONTRIBUTING.md)

## 开始

1. 新增 skill 或修改规则前先开 issue，说明要解决的问题。
2. Fork 仓库、建分支，向 main 提 PR。CI 会再跑一遍检查。

## 规则

1. 克隆后执行一次 `git config core.hooksPath .githooks`。之后 pre-commit 运行 scripts/run_checks.py（skill 目录检查与个人信息扫描），commit-msg 扫描提交说明，pre-push 扫描所有待推送的提交。Claude Code 会话通过 .claude/settings.json 获得同样的检查。
2. skills/ 下一个 skill 一个目录，目录名用小写单词加连字符。每个目录含 SKILL.md、prompt.md、README.md、README.zh-CN.md，并在根目录两个 README 里列出。scripts/check_skills.py 检查这些约定。
3. SKILL.md 与 prompt.md 规则相同，须在同一个 PR 里一起修改。prompt.md 的规则放在唯一一个 ```text 代码块里，并有「适用场景：」行。
4. skill 和提示词用中文写；README 分英文（README.md）和中文（README.zh-CN.md）两份，内容一致。每次改动都记入两份 skill README 的版本说明。
5. 脚本只用 Python 标准库，支持 Python 3.8+，日志按其他脚本的格式输出到标准错误，并提供 --log-level 参数。
6. 不得出现个人信息、工作信息和凭据：运行 python3 scripts/sensitive_scan.py。示例用明显虚构的名称（如「某某有限公司」「张三」）、example.com 地址和文档专用 IP 段（192.0.2.0/24）。提交用 GitHub noreply 邮箱。
7. 不写案例和背景：文档、skill 正文、提交说明和 PR 只写规则和行为，不写来历，不写经历，不描述工具服务的环境、单位、人员和项目，不引用真实文档里的数字。确需举例时只给最小的虚构例子。
8. 发版自动进行：合并到 main 后，有改动的 skill 自动发布。不要手动推送发版 tag。
