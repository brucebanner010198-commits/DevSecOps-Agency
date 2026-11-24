#!/usr/bin/env python3
"""Advisory release check: did every blocking council render a verdict?

CONSTITUTION.md §3.3 names four blocking councils: CISO (security), CEVO
(evaluation), CRT (red-team) and CAO (audit). A ship needs each one's verdict,
and a red from any of them is cleared only by a fix and a re-run, or by a
user-signed waiver.

Evidence, per blocking council:
  convened  an agent of that council was dispatched (guard receipts)
  recorded  an agent of that council wrote a file other than the shared logs
            (chat.jsonl, inbox.json, _sessions/). This is the verdict.
  gate      status.json > gates.byCouncil.<council>, the shape skills/gates documents
A council with no recorded verdict is flagged, whatever status.json says: the CEO
writes status.json, so a gate entry never stands in for the council's own record.
A red is cleared only by an entry in gates.waivers with "waivedBy": "user" for
that council.

Limits: it is read-only and advisory, and blocks nothing; making it a gate is
the Chairman's E4 decision. Receipts accumulate across runs in the launch folder:
use --project to keep only writes under one project folder (dispatches carry no
path, so they are not narrowed), and --since to drop receipts before a time.
It checks a ship, not an adoption.

    python scripts/release_check.py <launch-dir> [--project <folder>] [--since <ISO time>] [--json]
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PREFIX = "devsecops-agency:"
BLOCKING = {"security": "CISO", "evaluation": "CEVO", "red-team": "CRT", "audit": "CAO"}
WRITES = ("Write", "Edit", "MultiEdit", "NotebookEdit")
LOGS = ("chat.jsonl", "inbox.json")


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


def is_log(path: str) -> bool:
    p = path.replace("\\", "/")
    return p.rsplit("/", 1)[-1] in LOGS or "/_sessions/" in "/" + p


def under(path: str, folder: str | None) -> bool:
    if not folder:
        return True
    a, b = os.path.normcase(os.path.abspath(path)), os.path.normcase(os.path.abspath(folder))
    return a == b or a.startswith(b.rstrip(os.sep) + os.sep)


def read_gates(project: Path | None) -> dict:
    """status.json > gates from the project folder only (not every status.json under the launch folder)."""
    if not project:
        return {}
    p = project / "status.json"
    try:
        g = json.loads(p.read_bytes().decode("utf-8")).get("gates") or {}
        return g if isinstance(g, dict) else {}
    except (OSError, json.JSONDecodeError, UnicodeDecodeError, AttributeError):
        return {}


def colour(value) -> str | None:
    return str(value).split()[0].lower().strip(",.;:") if value else None  # "yellow (no High)" -> "yellow"


def report(receipts: list[dict], councils: dict[str, str], gates: dict,
           project: str | None = None, since: str | None = None) -> dict:
    convened = {c: False for c in BLOCKING}
    recorded = {c: False for c in BLOCKING}
    for r in receipts:
        if r.get("decision") == "deny" or (since and (r.get("ts") or "") < since):
            continue
        agent = r.get("agent") or ""
        agent = agent[len(PREFIX):] if agent.startswith(PREFIX) else None
        target = r.get("target") or ""
        target = target[len(PREFIX):] if target.startswith(PREFIX) else target
        if r.get("tool") in ("Agent", "Task") and councils.get(target) in BLOCKING:
            convened[councils[target]] = True
        path = r.get("path") or ""
        if (agent and r.get("tool") in WRITES and councils.get(agent) in BLOCKING
                and path and not is_log(path) and under(path, project)):
            recorded[councils[agent]] = True
    by_council = gates.get("byCouncil") if isinstance(gates.get("byCouncil"), dict) else {}
    waivers = gates.get("waivers") if isinstance(gates.get("waivers"), list) else []
    rows, flags = [], []
    for council, title in BLOCKING.items():
        c = colour(by_council.get(council))
        waived = any(isinstance(w, dict) and w.get("waivedBy") == "user"
                     and (w.get("council") == council or w.get("to") in (council, title.lower()))
                     for w in waivers)
        rows.append({"council": council, "title": title, "convened": convened[council],
                     "recorded": recorded[council], "gate": c, "user_waiver": waived})
        if not recorded[council]:
            flags.append(f"{title} ({council}) recorded no verdict"
                         + (f"; status.json says {c}, but that is not the council's own record" if c else ""))
        if c == "red" and not waived:
            flags.append(f"{title} ({council}) is red with no user-signed waiver")
    return {"councils": rows, "flags": flags}


def arg(argv: list[str], name: str) -> str | None:
    return argv[argv.index(name) + 1] if name in argv and argv.index(name) + 1 < len(argv) else None


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1].startswith("--"):
        print(__doc__)
        return 2
    launch = Path(argv[1])
    path = launch / ".devsecops-agency" / "receipts.jsonl"
    if not path.exists():
        print(f"no receipts at {path}")
        return 2
    project = arg(argv, "--project")
    proj_path = (launch / project) if project and not os.path.isabs(project) else (Path(project) if project else None)
    rep = report(read_jsonl(path), load_councils(), read_gates(proj_path),
                 str(proj_path) if proj_path else None, arg(argv, "--since"))
    if "--json" in argv:
        print(json.dumps(rep, indent=1))
        return 0
    for r in rep["councils"]:
        print(f"{r['title']:5} convened={'yes' if r['convened'] else 'no':3} recorded={'yes' if r['recorded'] else 'no':3} "
              f"gate={r['gate'] or '-'}{' (user waiver)' if r['user_waiver'] else ''}")
    for f in rep["flags"]:
        print("FLAG", f)
    if not rep["flags"]:
        print("every blocking council recorded a verdict")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
