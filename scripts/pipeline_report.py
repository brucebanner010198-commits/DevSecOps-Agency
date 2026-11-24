#!/usr/bin/env python3
"""Report, from the guard's receipts, which chiefs did their specialists' work.

Log-only and read-only: it reads <project>/.devsecops-agency/receipts.jsonl and
prints a report. It blocks nothing and changes no file. It is the first,
advisory piece of the pipeline enforcement the plan calls 5-lite. Making
the pipeline blocking needs the Chairman's E4 decision.

A chief is any agent whose role card grants `Agent` (it can dispatch), other
than `ceo` and `board-director`. A chief is flagged when it wrote at least one
file and dispatched no agent from its own council during the run. That is
the pattern G1, G2 and adoption run A2 showed: the chief wrote its
specialist's record itself.

    python scripts/pipeline_report.py <project-dir>          # print the report
    python scripts/pipeline_report.py <project-dir> --json   # machine-readable
Exit status is 0 either way; the report is advisory.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PREFIX = "devsecops-agency:"
EXEMPT = {"ceo", "board-director"}
# Recorded cross-council dispatches (2a pack, decision 4; 1a pack, decision 4): the builders
# live in the execution council but work for these chiefs.
ALSO_OWN = {"engineering-lead": {"execution"}, "pm-lead": {"execution"}}


def load_cards() -> dict:
    return yaml.safe_load((ROOT / "agents" / "role-cards.yaml").read_text(encoding="utf-8"))["agents"]


def council(card: dict) -> str:
    parts = card["file"].split("/")
    return parts[1] if len(parts) > 2 else "root"


def read_receipts(path: Path) -> list[dict]:
    out = []
    for line in path.read_bytes().decode("utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def report(receipts: list[dict], cards: dict) -> dict:
    chiefs = {n for n, c in cards.items() if "Agent" in c["enforced"]["tools"] and n not in EXEMPT}
    wrote: dict[str, list[str]] = {}
    dispatched: dict[str, list[str]] = {}
    for r in receipts:
        agent = (r.get("agent") or "")
        if not agent.startswith(PREFIX):
            continue
        name = agent[len(PREFIX):]
        if r.get("tool") in ("Write", "Edit", "MultiEdit", "NotebookEdit") and r.get("decision") == "allow":
            wrote.setdefault(name, []).append(r.get("path") or "")
        if r.get("tool") in ("Agent", "Task") and r.get("decision") == "allow":
            dispatched.setdefault(name, []).append((r.get("target") or "")[len(PREFIX):])
    flagged = []
    for name in sorted(chiefs & (set(wrote) | set(dispatched))):
        mine = {council(cards[name])} | ALSO_OWN.get(name, set())
        own = [t for t in dispatched.get(name, []) if t in cards and council(cards[t]) in mine]
        if wrote.get(name) and not own:
            flagged.append({"chief": name, "files": len(wrote[name]), "dispatched": dispatched.get(name, [])})
    return {
        "chiefs_seen": sorted(chiefs & (set(wrote) | set(dispatched))),
        "flagged": flagged,
    }


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    path = Path(argv[1]) / ".devsecops-agency" / "receipts.jsonl"
    if not path.exists():
        print(f"no receipts at {path}")
        return 2
    rep = report(read_receipts(path), load_cards())
    if "--json" in argv:
        print(json.dumps(rep, indent=1))
        return 0
    print(f"chiefs seen: {', '.join(rep['chiefs_seen']) or 'none'}")
    if not rep["flagged"]:
        print("no chief wrote records without dispatching its own council")
    for f in rep["flagged"]:
        print(f"FLAG {f['chief']}: wrote {f['files']} file(s) and dispatched no agent of its own council"
              + (f" (dispatched: {', '.join(f['dispatched'])})" if f["dispatched"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
