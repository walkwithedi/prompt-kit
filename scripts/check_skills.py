#!/usr/bin/env python3
"""Check every skill folder under skills/.

  - holds SKILL.md, prompt.md, README.md and README.zh-CN.md
  - SKILL.md starts with front matter whose name equals the folder name and whose
    description is present and at most 1024 characters
  - prompt.md has a "适用场景：" line and exactly one ```text code block
  - the root README.md and README.zh-CN.md link to the skill folder

Exit code 1 when any check fails.
"""
import argparse
import logging
import os
import re
import sys

log = logging.getLogger("check_skills")
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s.%(funcName)s:%(lineno)d - %(message)s"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")
REQUIRED = ("SKILL.md", "prompt.md", "README.md", "README.zh-CN.md")
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def front_matter(text):
    """The key: value pairs of the leading --- block, or None when there is none."""
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    pairs = {}
    for line in m.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep:
            pairs[key.strip()] = value.strip()
    return pairs


def check_skill(name):
    problems = []
    folder = os.path.join(SKILLS, name)
    if not NAME.match(name):
        problems.append(f"{name}: folder name must be lower-case words joined by hyphens")
    for f in REQUIRED:
        if not os.path.isfile(os.path.join(folder, f)):
            problems.append(f"{name}: missing {f}")
    skill = os.path.join(folder, "SKILL.md")
    if os.path.isfile(skill):
        meta = front_matter(read(skill))
        if meta is None:
            problems.append(f"{name}/SKILL.md: no front matter")
        else:
            if meta.get("name") != name:
                problems.append(f"{name}/SKILL.md: name is {meta.get('name')!r}, expected {name!r}")
            desc = meta.get("description", "")
            if not desc:
                problems.append(f"{name}/SKILL.md: empty description")
            elif len(desc) > 1024:
                problems.append(f"{name}/SKILL.md: description longer than 1024 characters")
    prompt = os.path.join(folder, "prompt.md")
    if os.path.isfile(prompt):
        text = read(prompt)
        if not re.search(r"^适用场景：\S", text, re.M):
            problems.append(f"{name}/prompt.md: no 适用场景： line")
        if len(re.findall(r"^```text$", text, re.M)) != 1:
            problems.append(f"{name}/prompt.md: needs exactly one ```text code block")
    for readme in ("README.md", "README.zh-CN.md"):
        if f"skills/{name}/" not in read(os.path.join(ROOT, readme)):
            problems.append(f"{readme}: no link to skills/{name}/")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--log-level", default=os.environ.get("LOG_LEVEL", "INFO").upper(),
                    choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    a = ap.parse_args()
    logging.basicConfig(level=a.log_level, format=LOG_FORMAT, stream=sys.stderr)
    names = sorted(d for d in os.listdir(SKILLS) if os.path.isdir(os.path.join(SKILLS, d)))
    problems = [p for n in names for p in check_skill(n)]
    for p in problems:
        print(p)
    log.info("%d skills checked, %d problems", len(names), len(problems))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
