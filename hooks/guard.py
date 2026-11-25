#!/usr/bin/env python3
"""PreToolUse guard for the agency's own agents (plan Phase 2a).

Runs on every tool call while the plugin is enabled. Calls whose `agent_type`
is not a `devsecops-agency:` agent pass through untouched, so ordinary
sessions are not affected.

Blocking rules (exit 2 with a reason):
  B1 boundary     Write, Edit, MultiEdit and NotebookEdit stay inside the project
                  directory (CLAUDE_PROJECT_DIR, else the call's cwd).
  B2 append-only  On paths the repo's own documents call append-only, the
                  resulting file must start with the current file, byte for
                  byte (line endings normalised).
  B4 receipts     Agents may not write the guard's own receipts folder
                  (.devsecops-agency/); only the hook appends there.
  B3 dispatch     A dispatch target must be a `devsecops-agency:` agent, and the
                  call may not override the target's model.

  B5 scope        Write, Edit, MultiEdit and NotebookEdit must land on a path in the
                  caller's role-card `write_scope` (or the shared logs every agent
                  keeps: chat.jsonl, inbox.json, _sessions/). An entry ending in "/"
                  is a folder; other entries are file names or globs. Both match at
                  any depth, so `brief.md` covers outputs/devsecops-agency/<slug>/brief.md.
                  "*" (the builders) is the whole project except the agency's records
                  (_agency/, _vision/, _decisions/, _memory/). A refusal names the
                  agents whose scope covers the path. A card with no write_scope falls
                  back to L1; an agency agent with no card at all may not write.

Log-only rules (recorded in the receipt, never block):
  L1 scope        the write path is outside the caller's role-card scope note (only for a
                  card with no write_scope).
  L2 own-council  a chief dispatches an agent outside its own council.

Every decision is appended to <project>/.devsecops-agency/receipts.jsonl.

Limits, stated plainly: shell commands are not inspected, so a shell can write
anywhere. Only an OS sandbox (WSL2, a container) contains a shell. A hook runs
as the same OS user as the agent, so an agent with a shell can edit this file.

DEVSECOPS_GUARD_MODE=log turns the blocking rules into log-only ones.
"""
from __future__ import annotations

import fnmatch
import json
import os
import sys
import time
from pathlib import Path

PLUGIN_ROOT = Path(os.environ.get("CLAUDE_PLUGIN_ROOT") or Path(__file__).resolve().parent.parent)
PREFIX = "devsecops-agency:"
WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
DISPATCH_TOOLS = {"Agent", "Task"}

# Paths the repo's documents call append-only (CONSTITUTION §5.2, LESSONS.md, skills,
# agent bodies). Matched against the path relative to the project, with "/" separators.
APPEND_ONLY = [
    "chat.jsonl", "*/chat.jsonl",
    "LESSONS.md", "*/LESSONS.md",
    "_sessions/*",
    "_vision/traces/*",
    "_vision/dlp/*.jsonl",
    "_vision/mcp-registry/*/hashes.jsonl",
    "_vision/sre/*.log",
    "_vision/cost/manual-billing.csv",
    "_vision/cross-model-panel/panel-rotation.md",
    "_vision/history/*",
    "_memory/patterns/*",
    "red-team/findings.md",
]
# The same files under a project output folder (outputs/devsecops-agency/<slug>/...).
# fnmatch's * also matches "/", so "*/" covers any depth.
APPEND_ONLY += ["*/" + g for g in APPEND_ONLY if not g.startswith("*/")]
APPEND_ONLY = sorted(set(APPEND_ONLY))
RECEIPTS_DIR = ".devsecops-agency"
# Logs every agent may write, whatever its scope (chat.jsonl and _sessions/ are also append-only under B2).
SHARED_WRITES = ["chat.jsonl", "inbox.json", "_sessions/"]
# The agency's own records. A "*" scope (the builders) covers the whole project except these.
RECORD_DIRS = ["_agency/", "_vision/", "_decisions/", "_memory/"]


def _norm(p: str) -> str:
    return os.path.normcase(os.path.abspath(p))


def inside(path: str, root: str) -> bool:
    p, r = _norm(path), _norm(root)
    return p == r or p.startswith(r.rstrip(os.sep) + os.sep)


def rel(path: str, root: str) -> str:
    return os.path.relpath(_norm(path), _norm(root)).replace(os.sep, "/")


def is_append_only(relpath: str) -> bool:
    # rel() case-folds on Windows (normcase), so fold the globs the same way there.
    fold = str.lower if os.name == "nt" else (lambda s: s)
    return any(fnmatch.fnmatchcase(fold(relpath), fold(g)) for g in APPEND_ONLY)


def _lf(s: str) -> str:
    return s.replace("\r\n", "\n")


def resulting_content(tool: str, ti: dict, current: str) -> str | None:
    """The file content after the call, or None if it cannot be computed."""
    if tool == "Write":
        return ti.get("content", "")
    edits = ti.get("edits") if tool == "MultiEdit" else [ti] if tool == "Edit" else None
    if edits is None:
        return None
    out = _lf(current)  # Edit matches across line endings, so compare in LF form
    for e in edits:
        old, new = _lf(e.get("old_string", "")), _lf(e.get("new_string", ""))
        if old not in out:
            return None
        out = out.replace(old, new) if e.get("replace_all") else out.replace(old, new, 1)
    return out


def in_scope(relpath: str, scope: list[str]) -> bool:
    """True if relpath matches an entry of scope at any depth. "x/" is a folder, "*" is anything."""
    fold = str.lower if os.name == "nt" else (lambda s: s)
    r = fold(relpath)
    for e in (fold(s) for s in scope):
        if e == "*":
            if not any(("/" + r).find("/" + d) != -1 for d in RECORD_DIRS):
                return True
            continue
        if e.endswith("/"):
            if ("/" + r).find("/" + e) != -1:
                return True
        elif fnmatch.fnmatchcase(r, e) or fnmatch.fnmatchcase(r, "*/" + e):
            return True
    return False


def load_cards() -> dict:
    """Role cards for L1 and L2. hooks/role-cards.json is generated from agents/role-cards.yaml
    (scripts/role_cards.py write) so that the guard needs only the standard library; the YAML
    is a fallback for a checkout where the JSON is missing."""
    try:
        return json.loads((PLUGIN_ROOT / "hooks" / "role-cards.json").read_bytes().decode("utf-8"))["agents"]
    except Exception:
        pass
    try:
        import yaml
        cards = yaml.safe_load((PLUGIN_ROOT / "agents" / "role-cards.yaml").read_text(encoding="utf-8"))["agents"]
        # Same shape as the JSON slice: write_scope sits at the card's top level.
        return {n: dict(c, write_scope=(c.get("enforced") or {}).get("write_scope")) for n, c in cards.items()}
    except Exception:
        return {}


def owners(relpath: str, cards: dict) -> list[str]:
    """Agents whose write_scope covers relpath. Named entries come first; the builders' catch-all
    ("*") is listed only when no named entry covers the path."""
    named = sorted(n for n, c in cards.items() if c.get("write_scope") and "*" not in c["write_scope"]
                   and in_scope(relpath, c["write_scope"]))
    if named:
        return named
    return sorted(n for n, c in cards.items() if c.get("write_scope") and "*" in c["write_scope"]
                  and in_scope(relpath, c["write_scope"]))


def council(card: dict | None) -> str | None:
    if not card:
        return None
    parts = card["file"].split("/")
    return parts[1] if len(parts) > 2 else "root"


def scope_prefixes(note: str) -> list[str]:
    out = []
    for tok in note.replace(" and ", ",").split(","):
        tok = tok.strip().split(" (")[0].strip().strip("`")
        if tok and tok.lower() not in ("none", "none (reports to lead)") and " " not in tok:
            out.append(tok)
    return out


def check(d: dict, cards: dict | None = None) -> tuple[list[str], list[str]]:
    """Return (blocking reasons, log-only notes) for one PreToolUse input."""
    agent = d.get("agent_type") or ""
    if not agent.startswith(PREFIX):
        return [], []
    tool = d.get("tool_name") or ""
    ti = d.get("tool_input") or {}
    project = os.environ.get("CLAUDE_PROJECT_DIR") or d.get("cwd") or os.getcwd()
    block: list[str] = []
    note: list[str] = []
    name = agent[len(PREFIX):]

    if tool in WRITE_TOOLS:
        path = ti.get("file_path") or ti.get("notebook_path") or ""
        if path and not os.path.isabs(path):
            path = os.path.join(project, path)
        if path and not inside(path, project):
            block.append(f"B1 boundary: {name} may not write outside the project ({path}). "
                         f"Write under {project} instead, for example in the project's output folder.")
        elif path:
            r = rel(path, project)
            if r == RECEIPTS_DIR or r.lower().startswith(RECEIPTS_DIR + "/"):
                block.append(f"B4 receipts: {r} is the guard's receipt log; agents may not write it")
            if is_append_only(r) and os.path.exists(path):
                try:
                    current = Path(path).read_bytes().decode("utf-8")
                except Exception:
                    current = None
                new = None if current is None else resulting_content(tool, ti, current)
                if current is not None and (new is None or not _lf(new).startswith(_lf(current))):
                    block.append(f"B2 append-only: {r} is append-only; the new content must start with the current content")
            cards = load_cards() if cards is None else cards
            card = cards.get(name)
            scope = (card or {}).get("write_scope")
            if cards and not card:
                block.append(f"B5 scope: {name} has no role card, so it may not write (default deny, Part 4 rule 1)")
            elif card and scope:
                if not in_scope(r, scope + SHARED_WRITES):
                    own = owners(r, cards)
                    who = f"It belongs to {', '.join(own)}: dispatch that agent, or return the content to the agent that dispatched you." if own                         else "No agent's scope covers it: return the content to the agent that dispatched you."
                    block.append(f"B5 scope: {name} may write only {', '.join(scope)} (plus {', '.join(SHARED_WRITES)}), not {r}. {who}")
            elif card:
                pre = scope_prefixes(card.get("descriptive", {}).get("write_scope_note", ""))
                if pre and not any(r == p.rstrip("/") or r.startswith(p if p.endswith("/") else p + "/") or r.endswith("/" + p) or r == p for p in pre):
                    note.append(f"L1 scope: {r} is outside {name}'s scope note {pre}")

    if tool in DISPATCH_TOOLS:
        target = ti.get("subagent_type") or ""
        cards = load_cards() if cards is None else cards
        if not target.startswith(PREFIX) and target in cards:
            block.append(f"B3 dispatch: {target} is an agency agent, but the bare name does not resolve. "
                         f"Dispatch it as {PREFIX}{target}.")
        elif not target.startswith(PREFIX):
            block.append(f"B3 dispatch: {name} may dispatch only {PREFIX} agents, not {target or 'the default agent'}. "
                         f"For web research dispatch {PREFIX}cro (its researchers hold WebSearch and WebFetch); "
                         f"for other work dispatch the chief that owns it.")
        if ti.get("model"):
            block.append(f"B3 dispatch: {name} may not override the model of {target} (tier changes are the Chairman's)")
        mine, theirs = council(cards.get(name)), council(cards.get(target[len(PREFIX):]))
        if name not in ("ceo", "board-director") and mine and theirs and mine != theirs:
            note.append(f"L2 own-council: {name} ({mine}) dispatched {target} ({theirs})")
    return block, note


def receipt(d: dict, block: list[str], note: list[str], decision: str) -> None:
    project = os.environ.get("CLAUDE_PROJECT_DIR") or d.get("cwd") or os.getcwd()
    ti = d.get("tool_input") or {}
    rec = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "agent": d.get("agent_type"), "agent_id": d.get("agent_id"), "tool": d.get("tool_name"),
        "path": ti.get("file_path") or ti.get("notebook_path"), "target": ti.get("subagent_type"),
        "decision": decision, "rules": block + note,
    }
    try:
        out = Path(project) / ".devsecops-agency"
        out.mkdir(exist_ok=True)
        with open(out / "receipts.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
    except OSError:
        pass


def main() -> int:
    d = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    if not (d.get("agent_type") or "").startswith(PREFIX):
        return 0
    cards = load_cards()
    block, note = check(d, cards)
    if not cards:
        note.append("L0 cards: role cards unavailable (hooks/role-cards.json and agents/role-cards.yaml unreadable); L1 and L2 not checked")
    enforce = os.environ.get("DEVSECOPS_GUARD_MODE", "block") != "log"
    decision = "deny" if block and enforce else ("would-deny" if block else "allow")
    receipt(d, block, note, decision)
    if block and enforce:
        sys.stderr.write("; ".join(block))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
