# 项目 skill

[English](README.md)

Claude Code 在本仓库的会话中自动加载本目录下的 skill。它们只用于开发辅助；对外发布的 skill 在根目录的 skills/ 下，不在这里。

| skill | 用途 | 上游 | 许可 |
|---|---|---|---|
| grill-me | 输入 /grill-me 启动追问，调用 grilling | [mattpocock/skills](https://github.com/mattpocock/skills) @ 49dd158 | MIT（目录内 LICENSE） |
| grilling | 按决策树分轮追问计划或想法，每题附推荐答案 | 同上 | MIT（目录内 LICENSE） |

## 维护

- 内容与上游一致，不在本仓库修改；各目录的 LICENSE 复制自上游仓库根目录。
- 更新时从上游对应提交重新复制整个目录，保留许可文件，并更新上表的提交号。grill-me 只是调用 grilling，两者须从同一提交一起更新。
