#!/usr/bin/env python3
"""Keep the `agents` list in .claude-plugin/plugin.json in step with agents/.

Without an explicit list, Claude Code registers every .md file under agents/,
including the scoped working-memory files named AGENTS.md, which then show up
as bogus agents (`devsecops-agency:AGENTS`). The manifest field takes file
paths, not globs, and replaces the default scan, so the list is generated.

    python scripts/plugin_agents.py check   # exit 1 if the list is stale
    python scripts/plugin_agents.py write   # regenerate the list
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / ".claude-plugin" / "plugin.json"


def expected() -> list[str]:
    files = (p for p in (ROOT / "agents").rglob("*.md") if p.name != "AGENTS.md")
    return sorted("./" + p.relative_to(ROOT).as_posix() for p in files)


def main(argv: list[str]) -> int:
    mode = argv[1] if len(argv) > 1 else "check"
    if mode not in ("check", "write"):
        print(__doc__)
        return 2
    raw = MANIFEST.read_bytes().decode("utf-8")
    data = json.loads(raw)
    want = expected()
    if data.get("agents") == want:
        print(f"plugin.json agents list is current ({len(want)} agents)")
        return 0
    if mode == "check":
        have = set(data.get("agents") or [])
        for p in sorted(set(want) - have):
            print(f"MISSING {p}")
        for p in sorted(have - set(want)):
            print(f"EXTRA   {p}")
        print("plugin.json agents list is stale: run python scripts/plugin_agents.py write")
        return 1
    data["agents"] = want
    nl = "\r\n" if "\r\n" in raw else "\n"
    MANIFEST.write_bytes((json.dumps(data, indent=2, ensure_ascii=False) + "\n").replace("\n", nl).encode("utf-8"))
    print(f"wrote {len(want)} agents to plugin.json")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
