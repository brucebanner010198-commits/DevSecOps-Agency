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

Limits: by default it is read-only and advisory, and blocks nothing. Receipts
accumulate across runs in the launch folder: use --project to keep only writes
under one project folder (dispatches carry no path, so they are not narrowed),
and --since to drop receipts before a time. It checks a ship, not an adoption.

Gate mode (--gate) is the check draft ADR-0010 (CONSTITUTION §8.6) would make
binding. It needs --project and --since, fails closed, and exits 1 on any flag:
  - status.json must exist and parse;
  - each blocking council's own verdict file (VERDICT_FILES) must exist in the
    project folder, be written by an agent of that council after --since, and
    carry a "gate: <green|yellow|red|n/a>" line that matches status.json;
  - a red passes only with a valid waiver: a waiver-grant ADR in _decisions/
    with approver: user, this project and council, an expiry not yet passed,
    and a class that is not non-waivable (CONSTITUTION §8.4);
  - a yellow passes only with a non-empty "## Open items" list in its verdict;
  - CEVO's verdict carries "acceptance: pass|fail"; a fail must be red;
  - acceptance.md (the set frozen at intake) must exist, written once, by no
    evaluation-council agent (CONSTITUTION §3.5).
The waiver ADR is still CEO-written; only signed receipts (Phase 2b) would
prove the User signed it.

    python scripts/release_check.py <launch-dir> [--project <folder>] [--since <ISO time>] [--json]
    python scripts/release_check.py <launch-dir> --gate --project <folder> --since <ISO time> [--today YYYY-MM-DD]
"""
from __future__ import annotations

import datetime
import json
import os
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PREFIX = "devsecops-agency:"
BLOCKING = {"security": "CISO", "evaluation": "CEVO", "red-team": "CRT", "audit": "CAO"}
WRITES = ("Write", "Edit", "MultiEdit", "NotebookEdit")
LOGS = ("chat.jsonl", "inbox.json")
# Each blocking council's own verdict file, in the project folder (a path its role card already grants).
VERDICT_FILES = {"security": "security-report.md", "evaluation": "close-eval.md",
                 "red-team": "red-team.md", "audit": "close-audit.md"}
COLOURS = ("green", "yellow", "red", "n/a")
NON_WAIVABLE = ("asi", "asi-class", "raw-secret")


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


def read_text(path: Path) -> str | None:
    try:
        return path.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def parse_verdict(text: str) -> dict:
    """gate: / acceptance: lines, and the bullets under "## Open items"."""
    out = {"gate": None, "acceptance": None, "open": []}
    section = None
    for line in text.splitlines():
        if line.startswith("#"):
            section = line.lstrip("#").strip().lower()
            continue
        m = re.match(r"\s*gate:\s*(\S+)", line, re.I)
        if m and out["gate"] is None:
            out["gate"] = m.group(1).lower().strip(",.;:`*")
        m = re.match(r"\s*acceptance:\s*(\S+)", line, re.I)
        if m and out["acceptance"] is None:
            out["acceptance"] = m.group(1).lower().strip(",.;:`*")
        if section == "open items" and re.match(r"\s*[-*]\s+\S", line):
            out["open"].append(line.strip())
    return out


def frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    try:
        fm = yaml.safe_load(text[3:end]) if end != -1 else None
    except yaml.YAMLError:
        return {}
    return fm if isinstance(fm, dict) else {}


def valid_waivers(dirs: list[Path], project: str, today: str) -> set[str]:
    """Councils with a live, user-approved waiver-grant ADR for this project."""
    out = set()
    for d in dirs:
        for f in sorted(d.glob("ADR-*.md")) if d.is_dir() else []:
            fm = frontmatter(read_text(f) or "")
            if (fm.get("kind") == "waiver-grant" and fm.get("approver") == "user"
                    and str(fm.get("project")) == project and fm.get("council") in BLOCKING
                    and str(fm.get("expires") or "") >= today
                    and str(fm.get("class") or "").lower() not in NON_WAIVABLE):
                out.add(fm["council"])
    return out


def gate_report(receipts: list[dict], councils: dict[str, str], project: Path, since: str,
                decision_dirs: list[Path], today: str) -> dict:
    flags = []
    raw = read_text(project / "status.json")
    try:
        status = json.loads(raw) if raw is not None else None
    except json.JSONDecodeError:
        status = None
    if not isinstance(status, dict):
        flags.append("status.json is missing or unreadable")
        status = {}
    gates = status.get("gates") if isinstance(status.get("gates"), dict) else {}
    by_council = gates.get("byCouncil") if isinstance(gates.get("byCouncil"), dict) else {}
    waived = valid_waivers(decision_dirs, project.name, today)

    def writes_to(name: str) -> list[dict]:
        target = os.path.normcase(os.path.abspath(project / name))
        return [r for r in receipts if r.get("decision") != "deny" and r.get("tool") in WRITES
                and r.get("path") and os.path.normcase(os.path.abspath(r["path"])) == target]

    def council_of(r: dict) -> str | None:
        a = r.get("agent") or ""
        return councils.get(a[len(PREFIX):]) if a.startswith(PREFIX) else None

    rows = []
    for council, title in BLOCKING.items():
        name = VERDICT_FILES[council]
        text = read_text(project / name)
        v = parse_verdict(text) if text is not None else {"gate": None, "acceptance": None, "open": []}
        own = [r for r in writes_to(name) if council_of(r) == council and (r.get("ts") or "") >= since]
        rows.append({"council": council, "title": title, "file": name, "gate": v["gate"],
                     "written_by_council": bool(own), "waiver": council in waived})
        if text is None:
            flags.append(f"{title} ({council}) has no verdict file {name}")
            continue
        if not own:
            flags.append(f"{title} ({council}) did not write {name} in this run")
        if v["gate"] not in COLOURS:
            flags.append(f"{title} ({council}) {name} has no gate: line")
        sj = colour(by_council.get(council))
        if sj != v["gate"]:
            flags.append(f"{title} ({council}) status.json says {sj or '-'}, its verdict says {v['gate'] or '-'}")
        if v["gate"] == "red" and council not in waived:
            flags.append(f"{title} ({council}) is red with no valid waiver-grant ADR")
        if v["gate"] == "yellow" and not v["open"]:
            flags.append(f"{title} ({council}) is yellow with no open items listed")
        if council == "evaluation":
            if v["acceptance"] not in ("pass", "fail"):
                flags.append("CEVO (evaluation) verdict has no acceptance: line")
            elif v["acceptance"] == "fail" and v["gate"] != "red":
                flags.append("CEVO (evaluation) acceptance failed but its gate is not red")
    acc = writes_to("acceptance.md")
    if read_text(project / "acceptance.md") is None:
        flags.append("acceptance.md (the set frozen at intake) is missing")
    if len(acc) > 1:
        flags.append(f"acceptance.md was written {len(acc)} times; it is frozen at intake")
    if any(council_of(r) == "evaluation" for r in acc):
        flags.append("acceptance.md was written by the evaluation council (CONSTITUTION §3.5)")
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
    if "--gate" in argv:
        since = arg(argv, "--since")
        if not proj_path or not since:
            print("gate mode needs --project and --since")
            return 2
        today = arg(argv, "--today") or datetime.datetime.now(datetime.timezone.utc).date().isoformat()
        dirs = [launch / "outputs" / "devsecops-agency" / "_decisions", proj_path / "_decisions"]
        rep = gate_report(read_jsonl(path), load_councils(), proj_path, since, dirs, today)
        if "--json" in argv:
            print(json.dumps(rep, indent=1))
        for f in rep["flags"]:
            print("FAIL", f)
        if not rep["flags"]:
            print("release gate passes")
        return 1 if rep["flags"] else 0
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
