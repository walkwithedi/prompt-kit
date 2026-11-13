#!/usr/bin/env python3
"""Install repository routing rules without replacing workspace instructions."""

import argparse
import logging
from pathlib import Path
import tempfile


START = "<!-- BEGIN prompt-kit repository routing -->"
END = "<!-- END prompt-kit repository routing -->"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path("/workspace"))
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()
    logging.basicConfig(level=args.log_level, format="%(levelname)s: %(message)s")
    rules = (Path(__file__).resolve().parent.parent / "AGENTS.md").read_text()
    args.workspace.mkdir(parents=True, exist_ok=True)
    target = args.workspace / "AGENTS.md"
    if target.is_symlink():
        raise ValueError("Refusing to replace a symbolic link")
    existing = target.read_text() if target.exists() else ""
    block = START + "\n" + rules.rstrip() + "\n" + END
    if START in existing or END in existing:
        if existing.count(START) != 1 or existing.count(END) != 1:
            raise ValueError("Invalid routing markers; existing file was preserved")
        start = existing.index(START)
        end = existing.index(END)
        if end < start:
            raise ValueError("Invalid routing marker order")
        content = existing[:start] + block + existing[end + len(END):]
    else:
        content = existing + ("\n\n" if existing else "") + block + "\n"
    mode = target.stat().st_mode & 0o777 if target.exists() else 0o644
    with tempfile.NamedTemporaryFile(mode="w", dir=args.workspace, delete=False) as output:
        temporary = Path(output.name)
        try:
            output.write(content)
            output.flush()
            temporary.chmod(mode)
            temporary.replace(target)
        finally:
            temporary.unlink(missing_ok=True)
    logging.info("Installed repository routing in %s", target)


if __name__ == "__main__":
    main()
