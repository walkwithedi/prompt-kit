# Contributing

[中文](CONTRIBUTING.zh-CN.md)

## How to start

1. Open an issue first for a new skill or a change to a rule, and describe the problem it solves.
2. Fork the repository, make a branch and open a pull request against main. CI runs the checks again.

## Rules

1. Run `git config core.hooksPath .githooks` once after cloning. pre-commit then runs scripts/run_checks.py (skill folder checks and the personal-data scan), commit-msg scans the commit message and pre-push scans every commit about to be pushed. Claude Code sessions get the same through .claude/settings.json.
2. One skill per folder under skills/, named in lower-case words joined by hyphens. Each folder holds SKILL.md, prompt.md, README.md and README.zh-CN.md, and both root READMEs list it. scripts/check_skills.py enforces this.
3. SKILL.md and prompt.md follow the same rules: change both in one pull request. prompt.md keeps its rules in a single ```text code block and has a 「适用场景：」 line.
4. Skills and prompts are written in Chinese; README files come in English (README.md) and Chinese (README.zh-CN.md) with the same content. Record each change under the version notes of both skill READMEs.
5. Scripts use only the Python standard library, run on Python 3.8+, log to stderr in the format used by the other scripts and accept --log-level.
6. No personal data, work details or credentials, ever: run python3 scripts/sensitive_scan.py. Examples use obviously fictional names (Riverside Clinic, Project Atlas), example.com addresses and the documentation IP ranges (192.0.2.0/24). Commit with your GitHub noreply address.
7. No case stories, no background. Documentation, skill text, commit messages and pull requests state rules and behaviour, not where they came from: no anecdotes, no description of the environment, organisation, people or projects something was built for, and no figures taken from real documents. Where an example is needed, keep it minimal and fictional.
8. Releases are automatic: a merge to main releases each changed skill. Do not push release tags by hand.
