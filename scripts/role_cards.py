#!/usr/bin/env python3
"""Keep each agent's enforced frontmatter in step with agents/role-cards.yaml.

agents/role-cards.yaml is the single source for the fields Claude Code
enforces: `tools`, `effort` and `maxTurns`. This script writes those three
fields into each agent file's frontmatter and leaves every other byte alone.
`model` is recorded in the cards but never written, because changing a tier
is a Chairman-only decision. `shell` and `write_scope` are enforced by hooks
(Phase 2a), not by Claude Code.

`write` also writes hooks/role-cards.json, the slice of the cards the Phase 2a
guard reads (file and scope note), so the guard needs only the standard
library. `check` fails if that file is stale.

    python scripts/role_cards.py check                 # exit 1 on any drift or rule breach
    python scripts/role_cards.py write                 # write tools, effort and maxTurns
    python scripts/role_cards.py write --only remove   # only remove tools the card no longer grants
    python scripts/role_cards.py write --only add      # only add tools the card grants
    python scripts/role_cards.py write --only limits   # only effort and maxTurns

The `--only` stages exist so that removals, additions and limits can be
reviewed as separate commits.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CARDS = ROOT / "agents" / "role-cards.yaml"
GUARD_CARDS = ROOT / "hooks" / "role-cards.json"
FM = re.compile(r"\A---(\r?\n)(.*?)\r?\n---\r?\n", re.S)
EFFORTS = {"low", "medium", "high", "xhigh", "max"}
# Tools a role card may grant. Anything else is a typo or an unreviewed widening.
KNOWN_TOOLS = {"Read", "Write", "Edit", "Grep", "Glob", "Bash", "Agent", "WebSearch", "WebFetch"}
SHELLS = {None, "full", "sandboxed", "read-only"}


def load_cards() -> dict:
    data = yaml.safe_load(CARDS.read_text(encoding="utf-8"))
    return data["agents"]


def guard_json(cards: dict) -> str:
    """The guard's slice of the cards, as LF-only JSON with sorted keys."""
    slim = {name: {"file": c["file"],
                   "descriptive": {"write_scope_note": (c.get("descriptive") or {}).get("write_scope_note", "")}}
            for name, c in cards.items()}
    doc = {"_generated": "from agents/role-cards.yaml by scripts/role_cards.py write; do not edit", "agents": slim}
    return json.dumps(doc, indent=1, sort_keys=True, ensure_ascii=False) + "\n"


def split(path: Path) -> tuple[str, str, str, str]:
    """Return (newline, frontmatter text, whole frontmatter block, body)."""
    raw = path.read_bytes().decode("utf-8")
    m = FM.match(raw)
    if not m:
        raise ValueError(f"{path}: no frontmatter")
    return m.group(1), m.group(2), m.group(0), raw[m.end():]


def current(path: Path) -> dict:
    _, fm, _, _ = split(path)
    return yaml.safe_load(fm)


def target_tools(cur: list[str], card_tools: list[str], only: str | None) -> list[str]:
    cur = ["Agent" if t == "Task" else t for t in cur]
    if only == "remove":
        return [t for t in cur if t in card_tools]
    if only == "add":
        return cur + [t for t in card_tools if t not in cur]
    return list(card_tools)


def set_key(lines: list[str], key: str, value: str | None, after: str) -> list[str]:
    """Set `key: value` in frontmatter lines; drop it if value is None; insert after `after:` if absent."""
    idx = next((i for i, l in enumerate(lines) if l.startswith(f"{key}:")), None)
    if value is None:
        return [l for i, l in enumerate(lines) if i != idx]
    new = f"{key}: {value}"
    if idx is not None:
        lines[idx] = new
        return lines
    pos = next((i for i, l in enumerate(lines) if l.startswith(f"{after}:")), len(lines) - 1)
    return lines[: pos + 1] + [new] + lines[pos + 1:]


def render(path: Path, card: dict, only: str | None) -> str:
    nl, fm, block, body = split(path)
    lines = fm.split(nl)
    data = yaml.safe_load(fm)
    enf = card["enforced"]
    if only in (None, "remove", "add"):
        tools = target_tools(list(data.get("tools") or []), enf["tools"], only)
        lines = set_key(lines, "tools", json.dumps(tools), "model")
    if only in (None, "limits"):
        lines = set_key(lines, "effort", enf.get("effort"), "model")
        lines = set_key(lines, "maxTurns", None if enf.get("maxTurns") is None else str(enf["maxTurns"]), "effort" if enf.get("effort") else "model")
    new_fm = nl.join(lines)
    out = f"---{nl}{new_fm}{nl}---{nl}{body}"
    # Safety: everything except the three managed keys must parse to the same mapping.
    before = {k: v for k, v in data.items() if k not in ("tools", "effort", "maxTurns")}
    after = yaml.safe_load(new_fm)
    if {k: v for k, v in after.items() if k not in ("tools", "effort", "maxTurns")} != before:
        raise ValueError(f"{path}: an unmanaged frontmatter key changed")
    return out


def rule_errors(name: str, card: dict) -> list[str]:
    e = card["enforced"]
    tools = e["tools"]
    errs = []
    unknown = sorted(set(tools) - KNOWN_TOOLS)
    if unknown:
        errs.append(f"unknown tool(s) {unknown}")
    if e.get("effort") is not None and e["effort"] not in EFFORTS:
        errs.append(f"effort {e['effort']!r} is not one of {sorted(EFFORTS)}")
    if e.get("maxTurns") is not None and (not isinstance(e["maxTurns"], int) or e["maxTurns"] < 1):
        errs.append("maxTurns must be a positive integer")
    if e.get("shell") not in SHELLS:
        errs.append(f"shell {e.get('shell')!r} is not one of {sorted(map(str, SHELLS))}")
    if ("Bash" in tools) != (e.get("shell") is not None):
        errs.append("shell must be set exactly when Bash is granted")
    # Part 4 rule 5: agents that can dispatch hold no shell.
    if "Agent" in tools and "Bash" in tools:
        errs.append("orchestrator holds Bash (Part 4 rule 5)")
    # Part 4 rule 2 (partial): web access and a full shell never together.
    if {"WebFetch", "WebSearch"} & set(tools) and "Bash" in tools:
        errs.append("web access with a shell (Part 4 rule 2)")
    if name == "ceo" and ({"Edit", "Bash"} & set(tools)):
        errs.append("ceo holds Edit or Bash")
    return errs


def main(argv: list[str]) -> int:
    mode = argv[1] if len(argv) > 1 else "check"
    only = None
    if "--only" in argv:
        only = argv[argv.index("--only") + 1]
        if only not in ("remove", "add", "limits"):
            print(__doc__)
            return 2
    if mode not in ("check", "write"):
        print(__doc__)
        return 2
    cards = load_cards()
    files = {p.relative_to(ROOT).as_posix(): p for p in (ROOT / "agents").rglob("*.md") if p.name != "AGENTS.md"}
    problems: list[str] = []
    seen = set()
    for name, card in sorted(cards.items()):
        rel = card["file"]
        seen.add(rel)
        path = files.get(rel)
        if path is None:
            problems.append(f"{name}: card points at missing file {rel}")
            continue
        data = current(path)
        if data.get("name") != name:
            problems.append(f"{rel}: frontmatter name {data.get('name')!r} != card {name!r}")
        if data.get("model") != card["enforced"].get("model"):
            problems.append(f"{rel}: model {data.get('model')!r} != card {card['enforced'].get('model')!r} (tier changes are Chairman-only)")
        problems += [f"{name}: {e}" for e in rule_errors(name, card)]
        held = (card.get("held") or {}).get("add") or []
        if set(held) & set(card["enforced"]["tools"]):
            problems.append(f"{name}: a held tool {sorted(set(held) & set(card['enforced']['tools']))} is granted; settle the hold first")
        # Plan Part 2B stage 1.1: descriptions load into every session, so examples live in the body.
        if "<example>" in (data.get("description") or ""):
            problems.append(f"{rel}: description contains an <example>; move it to the body")
        want = render(path, card, only if mode == "write" else None)
        have = path.read_bytes().decode("utf-8")
        if want != have:
            if mode == "write":
                path.write_bytes(want.encode("utf-8"))
                print(f"wrote {rel}")
            else:
                problems.append(f"{rel}: frontmatter drifts from its role card")
    for rel in sorted(set(files) - seen):
        problems.append(f"{rel}: agent has no role card")
    want_json = guard_json(cards)
    have_json = GUARD_CARDS.read_bytes().decode("utf-8").replace("\r\n", "\n") if GUARD_CARDS.exists() else None
    if want_json != have_json:
        if mode == "write":
            GUARD_CARDS.write_bytes(want_json.encode("utf-8"))
            print(f"wrote {GUARD_CARDS.relative_to(ROOT).as_posix()}")
        else:
            problems.append("hooks/role-cards.json: drifts from agents/role-cards.yaml")
    if problems:
        for p in problems:
            print(p)
        if mode == "check":
            print(f"{len(problems)} problem(s): fix agents/role-cards.yaml, then run python scripts/role_cards.py write")
            return 1
        return 1 if any("drifts" not in p for p in problems) else 0
    print(f"role cards current ({len(cards)} agents)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
