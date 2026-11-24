"""Tests for hooks/guard.py (run: python -m pytest hooks)."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
import guard  # noqa: E402

GUARD = str(Path(__file__).parent / "guard.py")


@pytest.fixture
def project(tmp_path, monkeypatch):
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path))
    return tmp_path


def call(tool, ti, agent="devsecops-agency:ceo"):
    return {"agent_type": agent, "tool_name": tool, "tool_input": ti}


def blocks(d):
    return guard.check(d, cards={})[0]


# --- pass-through -------------------------------------------------------------------------

def test_other_agents_pass_through(project):
    assert guard.check({"tool_name": "Write", "tool_input": {"file_path": "/etc/x"}}, {}) == ([], [])
    assert guard.check(call("Write", {"file_path": "/etc/x"}, agent="general-purpose"), {}) == ([], [])


# --- B1 boundary --------------------------------------------------------------------------

def test_write_inside_project_passes(project):
    assert blocks(call("Write", {"file_path": str(project / "src" / "a.js"), "content": "x"})) == []


def test_relative_path_resolves_against_project(project):
    assert blocks(call("Write", {"file_path": "src/a.js", "content": "x"})) == []


def test_write_outside_project_blocks(project, tmp_path_factory):
    other = tmp_path_factory.mktemp("elsewhere") / "a.txt"
    assert any(r.startswith("B1") for r in blocks(call("Edit", {"file_path": str(other)})))


def test_sibling_with_shared_prefix_is_outside(project):
    sibling = str(project) + "-evil" + os.sep + "a.txt"
    assert any(r.startswith("B1") for r in blocks(call("Write", {"file_path": sibling, "content": ""})))


def test_dotdot_escape_blocks(project):
    p = str(project / "src" / ".." / ".." / "x.txt")
    assert any(r.startswith("B1") for r in blocks(call("Write", {"file_path": p, "content": ""})))


# --- B2 append-only -----------------------------------------------------------------------

def test_append_by_write_passes_and_rewrite_blocks(project):
    log = project / "outputs" / "p" / "chat.jsonl"
    log.parent.mkdir(parents=True)
    log.write_text('{"a":1}\n', encoding="utf-8")
    assert blocks(call("Write", {"file_path": str(log), "content": '{"a":1}\n{"b":2}\n'})) == []
    assert any(r.startswith("B2") for r in blocks(call("Write", {"file_path": str(log), "content": '{"b":2}\n'})))


def test_append_ignores_line_ending_change(project):
    log = project / "chat.jsonl"
    log.write_bytes(b'{"a":1}\r\n')
    assert blocks(call("Write", {"file_path": str(log), "content": '{"a":1}\n{"b":2}\n'})) == []


def test_edit_that_appends_passes_and_edit_that_changes_blocks(project):
    led = project / "LESSONS.md"
    led.write_text("# L\nrow1\n", encoding="utf-8")
    ok = {"file_path": str(led), "old_string": "row1\n", "new_string": "row1\nrow2\n"}
    bad = {"file_path": str(led), "old_string": "row1", "new_string": "ROW1"}
    assert blocks(call("Edit", ok)) == []
    assert any(r.startswith("B2") for r in blocks(call("Edit", bad)))


def test_edit_that_cannot_apply_blocks_on_append_only(project):
    led = project / "LESSONS.md"
    led.write_text("row1\n", encoding="utf-8")
    assert any(r.startswith("B2") for r in blocks(call("Edit", {"file_path": str(led), "old_string": "nope", "new_string": "x"})))


def test_first_write_of_append_only_file_passes(project):
    assert blocks(call("Write", {"file_path": str(project / "red-team" / "findings.md"), "content": "x"})) == []


def test_ordinary_file_may_be_rewritten(project):
    f = project / "status.json"
    f.write_text("{}", encoding="utf-8")
    assert blocks(call("Write", {"file_path": str(f), "content": '{"phase": 2}'})) == []


# --- B3 dispatch --------------------------------------------------------------------------

def test_dispatch_to_agency_agent_passes(project):
    assert blocks(call("Agent", {"subagent_type": "devsecops-agency:qa-lead", "prompt": "x"})) == []


@pytest.mark.parametrize("target", ["general-purpose", "web-fetch", "", None])
def test_dispatch_outside_agency_blocks(project, target):
    assert any(r.startswith("B3") for r in blocks(call("Agent", {"subagent_type": target})))


def test_model_override_blocks(project):
    r = blocks(call("Task", {"subagent_type": "devsecops-agency:frontend-dev", "model": "opus"}))
    assert any("override" in x for x in r)


# --- log-only rules -----------------------------------------------------------------------

def test_scope_and_council_notes_never_block(project):
    cards = {
        "qa-lead": {"file": "agents/quality/qa-lead.md", "descriptive": {"write_scope_note": "qa/, qa-report.md"}},
        "pen-tester": {"file": "agents/security/pen-tester.md", "descriptive": {"write_scope_note": "security/"}},
    }
    b, n = guard.check(call("Write", {"file_path": str(project / "src" / "x.js"), "content": ""}, "devsecops-agency:qa-lead"), cards)
    assert b == [] and any(x.startswith("L1") for x in n)
    b, n = guard.check(call("Agent", {"subagent_type": "devsecops-agency:pen-tester"}, "devsecops-agency:qa-lead"), cards)
    assert b == [] and any(x.startswith("L2") for x in n)


# --- the hook process ---------------------------------------------------------------------

def run_hook(d, project, mode=None):
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project))
    if mode:
        env["DEVSECOPS_GUARD_MODE"] = mode
    return subprocess.run([sys.executable, GUARD], input=json.dumps(d).encode(), env=env, capture_output=True)


def test_process_blocks_with_exit_2_and_writes_receipt(project):
    p = run_hook(call("Agent", {"subagent_type": "general-purpose"}), project)
    assert p.returncode == 2 and b"B3" in p.stderr
    rec = json.loads((project / ".devsecops-agency" / "receipts.jsonl").read_text().splitlines()[-1])
    assert rec["decision"] == "deny" and rec["target"] == "general-purpose"


def test_log_mode_never_blocks(project):
    p = run_hook(call("Agent", {"subagent_type": "general-purpose"}), project, mode="log")
    assert p.returncode == 0
    rec = json.loads((project / ".devsecops-agency" / "receipts.jsonl").read_text().splitlines()[-1])
    assert rec["decision"] == "would-deny"


def test_process_passes_other_sessions_without_receipt(project):
    p = run_hook({"tool_name": "Write", "tool_input": {"file_path": "/etc/passwd"}}, project)
    assert p.returncode == 0 and not (project / ".devsecops-agency").exists()


def test_hooks_json_registers_guard_fail_closed():
    cfg = json.loads((Path(__file__).parent / "hooks.json").read_text(encoding="utf-8"))
    (entry,) = cfg["hooks"]["PreToolUse"]
    (hook,) = entry["hooks"]
    assert hook["onFailure"] == "block" and "guard.py" in hook["command"]
    for tool in ("Write", "Edit", "Agent", "Task"):
        assert tool in entry["matcher"].split("|")


# --- real layout and the D3a incident -----------------------------------------------------

OUT = "outputs/devsecops-agency/tip-splitter/"


@pytest.mark.parametrize("relpath", [
    OUT + "chat.jsonl", OUT + "LESSONS.md", OUT + "red-team/findings.md", OUT + "_vision/history/2026-11-22.md",
    OUT + "_sessions/ceo/s1.jsonl", OUT + "_vision/traces/2026-11/t.jsonl", OUT + "_vision/dlp/x-custom.jsonl",
    OUT + "_vision/mcp-registry/srv/hashes.jsonl", OUT + "_vision/sre/run.log",
    "_sessions/ceo/s1.jsonl", "_vision/cost/manual-billing.csv", "_vision/cross-model-panel/panel-rotation.md",
])
def test_append_only_globs_match_root_and_nested_layout(relpath):
    assert guard.is_append_only(relpath)


@pytest.mark.parametrize("relpath", [OUT + "status.json", OUT + "src/app.js", OUT + "red-team/notes.md", OUT + "src/history/list.js"])
def test_ordinary_paths_are_not_append_only(relpath):
    assert not guard.is_append_only(relpath)


def test_condensing_findings_is_refused(project):
    # D3a: a red-team record later replaced by a shorter summary (gate kept, detail dropped).
    f = project / OUT / "red-team" / "findings.md"
    f.parent.mkdir(parents=True)
    f.write_text("# findings\ngate: YELLOW\n\n## M1 detail\nrepro steps\n", encoding="utf-8")
    condensed = "# findings\ngate: YELLOW (2 medium)\n"
    assert any(r.startswith("B2") for r in blocks(call("Write", {"file_path": str(f), "content": condensed})))


@pytest.mark.parametrize("name", ["receipts.jsonl", "other.txt"])
def test_agents_may_not_write_the_receipts_folder(project, name):
    p = project / ".devsecops-agency" / name
    assert any(r.startswith("B4") for r in blocks(call("Write", {"file_path": str(p), "content": ""})))


def test_deny_messages_point_to_the_fix(project, tmp_path_factory):
    out = tmp_path_factory.mktemp("elsewhere") / "a.txt"
    assert str(project) in blocks(call("Write", {"file_path": str(out), "content": ""}))[0]
    assert "devsecops-agency:cro" in blocks(call("Agent", {"subagent_type": "web-fetch"}))[0]


def test_missing_cards_are_noted_not_silent(project, monkeypatch):
    monkeypatch.setattr(guard, "load_cards", lambda: {})
    monkeypatch.setattr(sys, "stdin", type("S", (), {"buffer": __import__("io").BytesIO(json.dumps(
        call("Write", {"file_path": str(project / "a.txt"), "content": ""})).encode())})())
    assert guard.main() == 0
    rec = json.loads((project / ".devsecops-agency" / "receipts.jsonl").read_text().splitlines()[-1])
    assert any(r.startswith("L0") for r in rec["rules"])


def test_scope_notes_work_without_pyyaml(project, tmp_path_factory):
    # The guard runs under whatever python3 is on PATH (on Windows, often one without PyYAML).
    # It reads hooks/role-cards.json, so L1 must still fire and no L0 note may appear.
    stub = tmp_path_factory.mktemp("noyaml")
    (stub / "yaml.py").write_text('raise ImportError("PyYAML hidden for this test")\n', encoding="utf-8")
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project), PYTHONPATH=str(stub))
    d = call("Write", {"file_path": str(project / "src" / "x.js"), "content": ""}, "devsecops-agency:qa-lead")
    p = subprocess.run([sys.executable, GUARD], input=json.dumps(d).encode(), env=env, capture_output=True)
    assert p.returncode == 0
    rules = json.loads((project / ".devsecops-agency" / "receipts.jsonl").read_text().splitlines()[-1])["rules"]
    assert any(r.startswith("L1") for r in rules) and not any(r.startswith("L0") for r in rules)


def test_bare_agency_name_is_refused_with_the_qualified_form(project):
    cards = {"frontend-dev": {"file": "agents/engineering/frontend-dev.md", "descriptive": {"write_scope_note": "src/"}}}
    b, _ = guard.check(call("Agent", {"subagent_type": "frontend-dev"}, "devsecops-agency:engineering-lead"), cards)
    assert len(b) == 1 and b[0].startswith("B3") and "devsecops-agency:frontend-dev" in b[0] and "cro" not in b[0]
