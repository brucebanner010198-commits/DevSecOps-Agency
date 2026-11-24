#!/usr/bin/env python3
"""Advisory release check: did every blocking council render a verdict?

CONSTITUTION.md §3.3 names four blocking councils: CISO (security), CEVO
(evaluation), CRT (red-team) and CAO (audit). A ship needs each one's verdict,
and a red from any of them is cleared only by a fix and a re-run, or by a
user-signed waiver.

This script reads <project>/.devsecops-agency/receipts.jsonl (the guard's log)
and, when present, the project's status.json files. It reports, for each
blocking council:
  convened  an agent of that council was dispatched during the run
  recorded  an agent of that council wrote a file
  gate      the colour recorded for it in status.json > gates, if any
It flags a council that never recorded a verdict, and a red with no user
waiver. It is read-only and advisory: it blocks nothing, and making it a gate
is the Chairman's E4 decision.

    python scripts/release_check.py <project-dir>          # print the report
    python scripts/release_check.py <project-dir> --json   # machine-readable
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PREFIX = "devsecops-agency:"
BLOCKING = {"security": "CISO", "evaluation": "CEVO", "red-team": "CRT", "audit": "CAO"}
WRITES = ("Write", "Edit", "MultiEdit", "NotebookEdit")


def load_councils() -> dict[str, str]:
    cards = yaml.safe_load((ROOT / "agents" / "role-cards.yaml").read_text(encoding="utf-8"))["agents"]
    out = {}
    for name, c in cards.items():
        parts = c["file"].split("/")
        out[name] = parts[1] if len(parts) > 2 else "root"
    return out


def read_jsonl(path: Path) -> list[dict]:
    out = []
    for line in path.read_bytes().decode("utf-8").splitlines():
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def gates_from_status(project: Path) -> dict[str, dict]:
    """Merge status.json > gates from every status.json under the project (agency layout)."""
    gates: dict[str, dict] = {}
    for p in project.rglob("status.json"):
        if ".devsecops-agency" in p.parts:
            continue
        try:
            g = json.loads(p.read_bytes().decode("utf-8")).get("gates") or {}
        except (json.JSONDecodeError, AttributeError, UnicodeDecodeError):
            continue
        if isinstance(g, dict):
            for k, v in g.items():
                gates[str(k).lower()] = v if isinstance(v, dict) else {"gate": v}
    return gates


def report(receipts: list[dict], councils: dict[str, str], gates: dict[str, dict]) -> dict:
    convened = {c: False for c in BLOCKING}
    recorded = {c: False for c in BLOCKING}
    for r in receipts:
        if r.get("decision") == "deny":
            continue
        agent = (r.get("agent") or "")[len(PREFIX):] if (r.get("agent") or "").startswith(PREFIX) else None
        target = r.get("target") or ""
        target = target[len(PREFIX):] if target.startswith(PREFIX) else target
        if r.get("tool") in ("Agent", "Task") and councils.get(target) in BLOCKING:
            convened[councils[target]] = True
        if agent and r.get("tool") in WRITES and councils.get(agent) in BLOCKING:
            recorded[councils[agent]] = True
    rows, flags = [], []
    for council, title in BLOCKING.items():
        g = None
        for key in (council, title.lower()):
            if key in gates:
                g = gates[key]
        raw = (g or {}).get("gate")
        colour = str(raw).split()[0].lower().strip(",.;:") if raw else None  # "yellow (no High)" -> "yellow"
        waived = bool((g or {}).get("waivedBy") == "user" or (g or {}).get("waiver"))
        rows.append({"council": council, "title": title, "convened": convened[council],
                     "recorded": recorded[council], "gate": colour, "waived": waived})
        if not recorded[council] and colour is None:
            flags.append(f"{title} ({council}) recorded no verdict")
        if colour == "red" and not waived:
            flags.append(f"{title} ({council}) is red with no user waiver")
    return {"councils": rows, "flags": flags}


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    project = Path(argv[1])
    path = project / ".devsecops-agency" / "receipts.jsonl"
    if not path.exists():
        print(f"no receipts at {path}")
        return 2
    rep = report(read_jsonl(path), load_councils(), gates_from_status(project))
    if "--json" in argv:
        print(json.dumps(rep, indent=1))
        return 0
    for r in rep["councils"]:
        print(f"{r['title']:5} convened={'yes' if r['convened'] else 'no':3} recorded={'yes' if r['recorded'] else 'no':3} "
              f"gate={r['gate'] or '-'}{' (user waiver)' if r['waived'] else ''}")
    for f in rep["flags"]:
        print("FLAG", f)
    if not rep["flags"]:
        print("every blocking council recorded a verdict")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
