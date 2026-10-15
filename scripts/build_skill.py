#!/usr/bin/env python3
"""Build the zip of a skill for upload to claude.ai: <name>/SKILL.md and nothing else.

Usage:
  python3 scripts/build_skill.py OUT_DIR NAME [NAME ...]   writes OUT_DIR/<name>-v<version>.zip
  --version VERSION   version in the file name (default: "dev")
"""
import argparse
import logging
import os
import sys
import zipfile

log = logging.getLogger("build_skill")
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s.%(funcName)s:%(lineno)d - %(message)s"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def build(out_dir, name, version):
    src = os.path.join(ROOT, "skills", name, "SKILL.md")
    if not os.path.isfile(src):
        raise SystemExit(f"no skill named {name}")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{name}-v{version}.zip")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        # Fixed timestamp so the same SKILL.md always gives the same zip
        info = zipfile.ZipInfo(f"{name}/SKILL.md", date_time=(2026, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        with open(src, "rb") as fh:
            z.writestr(info, fh.read())
    log.info("built %s", path)
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("out_dir")
    ap.add_argument("names", nargs="+")
    ap.add_argument("--version", default="dev")
    ap.add_argument("--log-level", default=os.environ.get("LOG_LEVEL", "INFO").upper(),
                    choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    a = ap.parse_args()
    logging.basicConfig(level=a.log_level, format=LOG_FORMAT, stream=sys.stderr)
    for n in a.names:
        print(build(a.out_dir, n, a.version))


if __name__ == "__main__":
    main()
