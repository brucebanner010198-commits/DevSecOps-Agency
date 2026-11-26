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
binding. It needs --project and --since, fails closed, and exits 1 on any flag.
"This run" starts at the later of --since and the CEO's write of acceptance.md.
  - status.json must exist and parse;
  - acceptance.md (the set frozen at intake, one "- <id>: <text>" line per
    item) must exist, written exactly once, by the CEO, before any verdict;
  - each blocking council's own verdict file (VERDICT_FILES) must exist in the
    project folder, be last written by an agent of that council in this run,
    and carry a "gate: <green|yellow|red>" line, the first such line at the top
    of the file, that matches status.json. A blocking council never returns n/a;
  - a red verdict lists its findings as "finding: <id> class: <class>" lines.
    It passes only if every finding has its own valid waiver and none is of a
    non-waivable class (CONSTITUTION §8.4). A valid waiver is a waiver-grant ADR
    in _decisions/ with approver: user, this project, council and finding id
    (an exact match), a waivable class, and an expiry not yet passed (today, UTC);
  - a yellow verdict lists at least one real item under "## Open items";
  - CEVO's verdict carries "regression: <max points>" and one
    "item <id>: pass|fail" line for each acceptance.md item, and no others. A
    regression of 5 or more, or a failed item, must be red;
  - an informing council's red in status.json > gates.byCouncil needs a valid
    waiver for that council and project. Informing councils have no verdict
    file, so this rests on status.json, which the CEO writes.
Limits: receipts come from the guard hook, which sees only the file-write
tools, so a write through a shell leaves no receipt; and the waiver ADR is
CEO-written, so only signed receipts (Phase 2b) would prove the User signed it.
Phase colours (byPhase) are derived from the councils' and are not checked.

    python scripts/release_check.py <launch-dir> [--project <folder>] [--since <ISO time>] [--json]
    python scripts/release_check.py <launch-dir> --gate --project <folder> --since <ISO time>
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
COLOURS = ("green", "yellow", "red")
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


def ts(value) -> str:
    """An ISO time normalised to UTC "YYYY-MM-DDTHH:MM:SS", so that Z and +00:00 compare equal; "" if unreadable."""
    try:
        t = datetime.datetime.fromisoformat(str(value).strip().replace("Z", "+00:00"))
    except ValueError:
        return ""
    if t.tzinfo is None:
        t = t.replace(tzinfo=datetime.timezone.utc)
    return t.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def non_waivable(cls: str) -> bool:
    """Fail closed: an empty class, any ASI class and any secret class are never waivable."""
    c = (cls or "").strip().lower()
    return not c or c.startswith("asi") or "secret" in c


EMPTY_ITEM = re.compile(r"^[-*]\s+(none|n/?a|nothing|-)\.?$", re.I)


def parse_verdict(text: str) -> dict:
    """The top gate: line, findings, open items, regression and acceptance items."""
    out = {"gate": None, "findings": {}, "open": [], "regression": None, "items": {}}
    section = None
    for n, line in enumerate(text.splitlines()):
        if line.startswith("#"):
            section = line.lstrip("#").strip().lower()
            continue
        m = re.match(r"\s*gate:\s*(\S+)\s*$", line, re.I)
        if m and out["gate"] is None and section is None:
            out["gate"] = m.group(1).lower().strip(",.;:`*")
        m = re.match(r"\s*finding:\s*(\S+)\s+class:\s*(\S+)", line, re.I)
        if m:
            out["findings"][m.group(1)] = m.group(2)
        m = re.match(r"\s*regression:\s*(-?[0-9.]+)", line, re.I)
        if m and out["regression"] is None:
            try:
                out["regression"] = float(m.group(1))
            except ValueError:
                pass
        m = re.match(r"\s*item\s+(\S+?):\s*(pass|fail)\b", line, re.I)
        if m:
            out["items"][m.group(1)] = m.group(2).lower()
        if section == "open items" and re.match(r"\s*[-*]\s+\S", line) and not EMPTY_ITEM.match(line.strip()):
            out["open"].append(line.strip())
    return out


def acceptance_ids(text: str) -> set[str]:
    return {m.group(1) for m in re.finditer(r"(?m)^\s*[-*]\s+(\S+?):", text)}


def frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    try:
        fm = yaml.safe_load(text[3:end]) if end != -1 else None
    except yaml.YAMLError:
        return {}
    return fm if isinstance(fm, dict) else {}


def valid_waivers(dirs: list[Path], project: str, today: str) -> dict[str, set[str]]:
    """council -> finding ids with a live, user-approved, waivable waiver-grant ADR for this project."""
    out: dict[str, set[str]] = {}
    for d in dirs:
        for f in sorted(d.glob("ADR-*.md")) if d.is_dir() else []:
            fm = frontmatter(read_text(f) or "")
            finding = str(fm.get("finding") or "").strip()
            if (fm.get("kind") == "waiver-grant" and fm.get("approver") == "user"
                    and str(fm.get("project")) == project and fm.get("council") and finding
                    and str(fm.get("expires") or "") >= today
                    and not non_waivable(str(fm.get("class") or ""))):
                out.setdefault(str(fm["council"]), set()).add(finding)
    return out


def gate_report(receipts: list[dict], councils: dict[str, str], project: Path, since: str,
                decision_dirs: list[Path], today: str, base: Path | None = None) -> dict:
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

    def resolve(path: str) -> str:
        q = Path(path)
        return os.path.normcase(os.path.abspath(q if q.is_absolute() or base is None else base / q))

    def writes_to(name: str) -> list[dict]:
        target = os.path.normcase(os.path.abspath(project / name))
        return sorted((r for r in receipts if r.get("decision") != "deny" and r.get("tool") in WRITES
                       and r.get("path") and resolve(r["path"]) == target), key=lambda r: ts(r.get("ts")))

    def council_of(r: dict) -> str | None:
        a = r.get("agent") or ""
        return councils.get(a[len(PREFIX):]) if a.startswith(PREFIX) else None

    def agent_of(r: dict) -> str:
        a = r.get("agent") or ""
        return a[len(PREFIX):] if a.startswith(PREFIX) else a

    acc = writes_to("acceptance.md")
    acc_text = read_text(project / "acceptance.md")
    start = max(ts(since), ts(acc[0].get("ts")) if acc else "")
    if not ts(since):
        flags.append("--since is not a readable ISO time")
    if acc_text is None:
        flags.append("acceptance.md (the set frozen at intake) is missing")
    if len(acc) != 1:
        flags.append(f"acceptance.md was written {len(acc)} times; it is written once, at intake")
    if any(council_of(r) == "evaluation" for r in acc):
        flags.append("acceptance.md was written by the evaluation council (CONSTITUTION §3.5)")
    if any(agent_of(r) != "ceo" for r in acc):
        flags.append("acceptance.md was written by an agent other than the CEO")
    in_run = [r for c in BLOCKING for r in writes_to(VERDICT_FILES[c]) if ts(r.get("ts")) >= ts(since)]
    if acc and in_run and ts(acc[0].get("ts")) > min(ts(r.get("ts")) for r in in_run):
        flags.append("acceptance.md was written after a verdict")

    rows = []
    for council, title in BLOCKING.items():
        name = VERDICT_FILES[council]
        text = read_text(project / name)
        v = parse_verdict(text) if text is not None else parse_verdict("")
        ws = writes_to(name)
        last = ws[-1] if ws else None
        own = bool(last) and council_of(last) == council and ts(last.get("ts")) >= start
        rows.append({"council": council, "title": title, "file": name, "gate": v["gate"],
                     "written_by_council": own, "findings": sorted(v["findings"])})
        if text is None:
            flags.append(f"{title} ({council}) has no verdict file {name}")
            continue
        if not own:
            flags.append(f"{title} ({council}) was not the last to write {name} in this run")
        if v["gate"] not in COLOURS:
            flags.append(f"{title} ({council}) {name} has no valid gate: line (green, yellow or red) at the top")
        sj = colour(by_council.get(council))
        if sj != v["gate"]:
            flags.append(f"{title} ({council}) status.json says {sj or '-'}, its verdict says {v['gate'] or '-'}")
        if v["gate"] == "red":
            if not v["findings"]:
                flags.append(f"{title} ({council}) is red but {name} lists no findings")
            for fid, cls in sorted(v["findings"].items()):
                if non_waivable(cls):
                    flags.append(f"{title} ({council}) finding {fid} is of a non-waivable class ({cls}); it must be fixed")
                elif fid not in waived.get(council, set()):
                    flags.append(f"{title} ({council}) finding {fid} is red with no valid waiver-grant ADR")
        if v["gate"] == "yellow" and not v["open"]:
            flags.append(f"{title} ({council}) is yellow with no open items listed")
        if council == "evaluation":
            if v["regression"] is None:
                flags.append("CEVO (evaluation) verdict has no regression: line")
            elif v["regression"] >= 5 and v["gate"] != "red":
                flags.append(f"CEVO (evaluation) regression of {v['regression']:g} points must be red")
            want = acceptance_ids(acc_text or "")
            if set(v["items"]) != want:
                flags.append("CEVO (evaluation) acceptance items do not match acceptance.md"
                             f" (missing {sorted(want - set(v['items']))}, extra {sorted(set(v['items']) - want)})")
            if "fail" in v["items"].values() and v["gate"] != "red":
                flags.append("CEVO (evaluation) an acceptance item failed but its gate is not red")
    for council, value in sorted(by_council.items()):
        if council not in BLOCKING and colour(value) == "red" and not waived.get(council):
            flags.append(f"informing council {council} is red with no valid waiver-grant ADR (§3.4, §8.6)")
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
        today = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
        dirs = [launch / "outputs" / "devsecops-agency" / "_decisions", proj_path / "_decisions"]
        rep = gate_report(read_jsonl(path), load_councils(), proj_path, since, dirs, today, base=launch)
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
