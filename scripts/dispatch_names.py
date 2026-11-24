#!/usr/bin/env python3
"""Find (or qualify) bare agency agent names in dispatch instructions.

A dispatch to a bare name such as `pm-lead` does not resolve at runtime and the
Phase 2a guard (B3) refuses it; the name must be `devsecops-agency:pm-lead`.
On any body line (frontmatter is skipped) containing the word "dispatch", a
backtick-quoted role-card name that comes after that word is taken to be a
dispatch target. Limit: names without backticks, and dispatches phrased
without the word "dispatch", are not seen; a one-off grep found two such
instructions, fixed by hand.

    python scripts/dispatch_names.py check   # exit 1 and list each bare target
    python scripts/dispatch_names.py write   # qualify them in place
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PREFIX = "devsecops-agency:"
WORD = re.compile(r"(?i)\bdispatch(?:es|ed|ing)?\b")
NAME = re.compile(r"(?<!devsecops-agency:)`([a-z0-9-]+)`")


def names() -> set[str]:
    return set(json.loads((ROOT / "hooks" / "role-cards.json").read_text(encoding="utf-8"))["agents"])


def fix_line(line: str, cards: set[str]) -> str:
    m = WORD.search(line)
    if not m:
        return line
    head, tail = line[: m.end()], line[m.end():]
    return head + NAME.sub(lambda n: f"`{PREFIX}{n.group(1)}`" if n.group(1) in cards else n.group(0), tail)


def files() -> list[Path]:
    return sorted(p for d in ("agents", "skills", "councils") for p in (ROOT / d).rglob("*.md"))


def main(argv: list[str]) -> int:
    mode = argv[1] if len(argv) > 1 else "check"
    cards = names()
    bad = []
    for p in files():
        raw = p.read_bytes().decode("utf-8")
        lines = raw.split("\n")
        # Skip the YAML frontmatter: descriptions mention other agents without dispatching them.
        start = 0
        if lines and lines[0].rstrip(chr(13)) == "---":
            start = next((i + 1 for i in range(1, len(lines)) if lines[i].rstrip(chr(13)) == "---"), 0)
        out = lines[:start] + [fix_line(l, cards) for l in lines[start:]]
        for i, (a, b) in enumerate(zip(lines, out), 1):
            if a != b:
                bad.append(f"{p.relative_to(ROOT).as_posix()}:{i}")
        if mode == "write" and out != lines:
            p.write_bytes("\n".join(out).encode("utf-8"))
    for b in bad:
        print(b)
    if mode == "check" and bad:
        print(f"{len(bad)} line(s) dispatch a bare agency name: run python scripts/dispatch_names.py write")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
