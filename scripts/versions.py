#!/usr/bin/env python3
"""Version numbers of the skills and of the whole kit: release plan and checks.

Version source: the newest entry of the "## Version notes" section of a skill's README.md, written
"- vX.Y (YYYY-MM-DD): ...", and of the "## 版本说明" section of its README.zh-CN.md, written
"- vX.Y（YYYY-MM-DD）：……". Both must name the same newest version. The whole kit (prompt-kit) takes
its version from the same sections of the root README.md and README.zh-CN.md. Pages show vX.Y;
tags are "<skill>-vX.Y.Z" and "prompt-kit-vX.Y.Z".

Previous release: among the old date tags "<name>-vYYYY.MM.DD[.N]" and the new tags, the one whose
commit is an ancestor of the released commit and comes last in history; on one commit a new tag
wins over a date tag. Tag names are never compared as text.

When the folder (for the kit: skills/, the root READMEs and LICENSE) changed since that release:
  - never released, or last released under a date tag: vX.Y.0
  - X.Y went up: vX.Y.0
  - X.Y unchanged and only README files changed: vX.Y.(Z+1)
  - anything else (SKILL.md, prompt.md or LICENSE changed without a higher X.Y, a lower X.Y, or
    a tag that already exists): no release, an error.

Usage:
  python3 scripts/versions.py plan [--head REV] [--force] [--kit] [skill ...]
      one tab-separated line per skill, and with --kit one for prompt-kit: name, action
      (release / skip / error), new tag, previous tag, reason; empty fields are "-".
  python3 scripts/versions.py check
      the version notes of every skill and of the root READMEs parse and agree between English
      and Chinese, and the working tree's changes since each last release follow the rules above.
      Exit code 1 on any problem.
"""
import argparse
import logging
import os
import re
import subprocess
import sys

log = logging.getLogger("versions")
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s.%(funcName)s:%(lineno)d - %(message)s"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KIT = "prompt-kit"
KIT_PATHS = ["skills", "README.md", "README.zh-CN.md", "LICENSE"]
SECTIONS = {"README.md": ("Version notes", re.compile(r"^- v(\d+(?:\.\d+)*) \((\d{4}-\d{2}-\d{2})\): ")),
            "README.zh-CN.md": ("版本说明", re.compile(r"^- v(\d+(?:\.\d+)*)（(\d{4}-\d{2}-\d{2})）："))}
DATE_TAG = re.compile(r"^v(\d{4})\.(\d{2})\.(\d{2})(?:\.(\d+))?$")
NEW_TAG = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")


class VersionError(Exception):
    pass


def git(*args):
    p = subprocess.run(("git",) + args, cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), p.stderr.strip()))
    return p.stdout


def git_ok(*args):
    return subprocess.run(("git",) + args, cwd=ROOT, capture_output=True).returncode == 0


def vstr(parts):
    return ".".join(str(p) for p in parts)


def read(rel, head):
    """A file from the working tree (head None) or from a commit."""
    if head is None:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
            return fh.read()
    return git("show", "%s:%s" % (head, rel))


def newest(text, file_name, where):
    """The highest version of a README's version notes, as a tuple (X, Y)."""
    title, entry = SECTIONS[file_name]
    found, section = [], None
    for line in text.splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        m = entry.match(line) if section == title else None
        if m:
            parts = tuple(int(p) for p in m.group(1).split("."))
            if len(parts) != 2:
                raise VersionError("%s: version note %r must name vX.Y (the release adds .Z)" % (where, line[:40]))
            found.append(parts)
    if not found:
        sample = "- vX.Y (YYYY-MM-DD): ..." if file_name == "README.md" else "- vX.Y（YYYY-MM-DD）：……"
        raise VersionError('%s: no "## %s" entry written "%s"' % (where, title, sample))
    return max(found)


def version_of(name, head):
    """The version of a skill (or the kit) from both READMEs; they must agree."""
    base = "" if name == KIT else "skills/%s/" % name
    versions = {}
    for file_name in SECTIONS:
        rel = base + file_name
        versions[file_name] = newest(read(rel, head), file_name, rel)
    en, zh = versions["README.md"], versions["README.zh-CN.md"]
    if en != zh:
        raise VersionError("%s: README.md names v%s but README.zh-CN.md names v%s" % (name, vstr(en), vstr(zh)))
    return en


def parse_tag(name, tag):
    if not tag.startswith(name + "-v"):
        return None
    rest = tag[len(name) + 1:]
    m = DATE_TAG.match(rest)
    if m and int(m.group(1)) >= 2000:
        return "date", None
    m = NEW_TAG.match(rest)
    if m:
        return "new", tuple(int(p) for p in m.groups())
    return None


def last_release(name, head):
    """The previous release of a skill or the kit, as a dict, or None."""
    rev = head or "HEAD"
    best = None
    for tag in git("tag", "-l", name + "-v*").split():
        info = parse_tag(name, tag)
        if not info:
            continue
        commit = git("rev-parse", tag + "^{commit}").strip()
        if not git_ok("merge-base", "--is-ancestor", commit, rev):
            continue
        key = (int(git("rev-list", "--count", commit).strip()), info[0] == "new", info[1] or ())
        if best is None or key > best[0]:
            best = (key, {"tag": tag, "commit": commit, "kind": info[0], "version": info[1]})
    return best[1] if best else None


def paths_of(name):
    return KIT_PATHS if name == KIT else ["skills/%s/" % name]


def changed(name, since, head):
    args = ["diff", "--name-only", since] + ([head] if head else []) + ["--"] + paths_of(name)
    files = [f for f in git(*args).splitlines() if f]
    if head is None:   # working tree: untracked files count as changes too
        files += [f for f in git("ls-files", "--others", "--exclude-standard", "--", *paths_of(name)).splitlines() if f]
    return files


def readme_only(path):
    return os.path.basename(path) in SECTIONS


def plan(name, head="HEAD", force=False):
    out = {"name": name, "action": "error", "tag": "", "last": "", "msg": ""}
    try:
        cur = version_of(name, head)
    except (VersionError, RuntimeError, OSError) as e:
        out["msg"] = str(e)
        return out
    last = last_release(name, head)
    files = []
    if last:
        out["last"] = last["tag"]
        files = changed(name, last["commit"], head)
        if not files and not force:
            out.update(action="skip", msg="unchanged since %s" % last["tag"])
            return out
    if not last or last["kind"] == "date":
        tag, reason = "%s-v%s.0" % (name, vstr(cur)), "first release" if not last else "first versioned release"
    else:
        prev = last["version"][:2]
        other = [f for f in files if not readme_only(f)]
        if cur > prev:
            tag, reason = "%s-v%s.0" % (name, vstr(cur)), "v%s is higher than v%s" % (vstr(cur), vstr(prev))
        elif cur < prev:
            out["msg"] = "%s: the READMEs name v%s, lower than the last release %s" % (name, vstr(cur), last["tag"])
            return out
        elif other:
            more = " and %d more" % (len(other) - 5) if len(other) > 5 else ""
            out["msg"] = ("%s: %s%s changed since %s but the version notes still name v%s; raise X.Y and add "
                          "a version note to both READMEs" % (name, ", ".join(other[:5]), more, last["tag"], vstr(cur)))
            return out
        else:
            tag, reason = "%s-v%s.%d" % (name, vstr(cur), last["version"][2] + 1), "only READMEs changed"
    if git_ok("rev-parse", "-q", "--verify", "refs/tags/" + tag):
        out["msg"] = "%s: tag %s already exists; raise X.Y" % (name, tag)
        return out
    out.update(action="release", tag=tag, msg=reason)
    return out


def all_skills():
    folder = os.path.join(ROOT, "skills")
    return sorted(d for d in os.listdir(folder) if os.path.isfile(os.path.join(folder, d, "SKILL.md")))


def check():
    problems = []
    for name in all_skills() + [KIT]:
        p = plan(name, head=None)
        if p["action"] == "error" and "already exists" not in p["msg"]:
            problems.append(p["msg"])
        log.debug("%s: %s %s", name, p["action"], p["tag"] or p["msg"])
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--log-level", default=os.environ.get("LOG_LEVEL", "WARNING").upper(),
                    choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    sub = ap.add_subparsers(dest="cmd")
    sub.required = True
    p = sub.add_parser("plan", help="print the release plan")
    p.add_argument("--head", default="HEAD")
    p.add_argument("--force", action="store_true", help="release unchanged skills too")
    p.add_argument("--kit", action="store_true", help="add a line for the whole kit")
    p.add_argument("skills", nargs="*")
    sub.add_parser("check", help="check the version notes and the changes since the last releases")
    a = ap.parse_args(argv)
    logging.basicConfig(level=a.log_level, format=LOG_FORMAT, stream=sys.stderr)
    if a.cmd == "plan":
        names = list(a.skills or all_skills()) + ([KIT] if a.kit else [])
        for name in names:
            if name != KIT and not os.path.isfile(os.path.join(ROOT, "skills", name, "SKILL.md")):
                r = {"name": name, "action": "error", "tag": "", "last": "",
                     "msg": "%s is not a skill folder (no skills/%s/SKILL.md)" % (name, name)}
            else:
                r = plan(name, head=a.head, force=a.force)
            # "-" for empty fields: bash read treats a run of tabs as one separator
            print("\t".join((r[k].replace("\t", " ").replace("\n", " ") or "-")
                            for k in ("name", "action", "tag", "last", "msg")))
        return 0
    problems = check()
    for msg in problems:
        print(msg, file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
