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
    "outputs/devsecops-agency/_memory/patterns/tip-splitter.md", "_memory/patterns/a.md",
])
def test_append_only_globs_match_root_and_nested_layout(relpath):
    assert guard.is_append_only(relpath)


# memory/<date>.md is newest-at-top and MEMORY.md takes bullets under its sections, so neither is an
# end-append; B2's lines-kept mode covers them instead (below). index.json is rewritten as a structure.
@pytest.mark.parametrize("relpath", [OUT + "status.json", OUT + "src/app.js", OUT + "red-team/notes.md", OUT + "src/history/list.js",
                                     "outputs/devsecops-agency/_memory/MEMORY.md", "outputs/devsecops-agency/_memory/index.json",
                                     "outputs/devsecops-agency/_memory/memory/2026-11-25.md"])
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
    # It reads hooks/role-cards.json, so the scope rule (B5) must still fire and no L0 note may appear.
    stub = tmp_path_factory.mktemp("noyaml")
    (stub / "yaml.py").write_text('raise ImportError("PyYAML hidden for this test")\n', encoding="utf-8")
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project), PYTHONPATH=str(stub))
    d = call("Write", {"file_path": str(project / "src" / "x.js"), "content": ""}, "devsecops-agency:qa-lead")
    p = subprocess.run([sys.executable, GUARD], input=json.dumps(d).encode(), env=env, capture_output=True)
    assert p.returncode == 2
    rules = json.loads((project / ".devsecops-agency" / "receipts.jsonl").read_text().splitlines()[-1])["rules"]
    assert any(r.startswith("B5") for r in rules) and not any(r.startswith("L0") for r in rules)


def test_bare_agency_name_is_refused_with_the_qualified_form(project):
    cards = {"frontend-dev": {"file": "agents/engineering/frontend-dev.md", "descriptive": {"write_scope_note": "src/"}}}
    b, _ = guard.check(call("Agent", {"subagent_type": "frontend-dev"}, "devsecops-agency:engineering-lead"), cards)
    assert len(b) == 1 and b[0].startswith("B3") and "devsecops-agency:frontend-dev" in b[0] and "cro" not in b[0]


# --- B5 write scope -----------------------------------------------------------------------

SCOPED = {
    "security-lead": {"file": "agents/security/security-lead.md",
                      "write_scope": ["security/", "threat-model.md", "_agency/baseline/*.md"]},
    "frontend-dev": {"file": "agents/execution/frontend-dev.md", "write_scope": ["*"]},
    "qa-lead": {"file": "agents/quality/qa-lead.md", "descriptive": {"write_scope_note": "qa/"}},
}


def scoped(project, agent, rel):
    return guard.check(call("Write", {"file_path": str(project / rel), "content": ""}, "devsecops-agency:" + agent), SCOPED)


@pytest.mark.parametrize("rel", [
    "threat-model.md",
    "outputs/devsecops-agency/app/threat-model.md",
    "security/audit.md",
    "outputs/devsecops-agency/app/security/x/y.md",
    "_agency/baseline/threat-model.md",
    "outputs/devsecops-agency/app/chat.jsonl",
    "_sessions/security-lead/s1.jsonl",
    "inbox.json",
])
def test_in_scope_writes_pass(project, rel):
    assert scoped(project, "security-lead", rel)[0] == []


@pytest.mark.parametrize("rel", [
    "outputs/devsecops-agency/app/app/app.js",
    "src/main.py",
    "security.md",
    "my-security/x.md",
    "_agency/system-map.md",
])
def test_out_of_scope_writes_block_and_name_the_scope(project, rel):
    b = scoped(project, "security-lead", rel)[0]
    assert len(b) == 1 and b[0].startswith("B5") and "threat-model.md" in b[0]


def test_star_scope_allows_any_project_path_but_not_outside(project, tmp_path_factory):
    assert scoped(project, "frontend-dev", "anything/at/all.js")[0] == []
    outside = tmp_path_factory.mktemp("elsewhere") / "x.js"
    b, _ = guard.check(call("Write", {"file_path": str(outside), "content": ""}, "devsecops-agency:frontend-dev"), SCOPED)
    assert any(x.startswith("B1") for x in b)


def test_card_without_write_scope_falls_back_to_log_only(project):
    b, n = scoped(project, "qa-lead", "src/x.js")
    assert b == [] and any(x.startswith("L1") for x in n)


def test_scope_applies_to_edit_too(project):
    (project / "src").mkdir()
    (project / "src" / "a.js").write_text("x", encoding="utf-8")
    d = call("Edit", {"file_path": str(project / "src" / "a.js"), "old_string": "x", "new_string": "y"}, "devsecops-agency:security-lead")
    assert any(x.startswith("B5") for x in guard.check(d, SCOPED)[0])


def test_every_real_card_has_a_scope_and_orchestrators_cannot_write_code():
    cards = guard.load_cards()
    assert all(c.get("write_scope") for c in cards.values())
    for chief in ("ceo", "engineering-lead", "security-lead", "qa-lead", "pm-lead"):
        assert not guard.in_scope("outputs/devsecops-agency/x/src/app.js", cards[chief]["write_scope"])


def test_star_scope_excludes_the_agencys_records(project):
    for rel in ("_agency/baseline/tests.md", "outputs/devsecops-agency/app/_vision/x.md", "_decisions/a.md", "_memory/m.md"):
        assert any(x.startswith("B5") for x in scoped(project, "frontend-dev", rel)[0]), rel
    assert scoped(project, "frontend-dev", "outputs/devsecops-agency/app/src/vision.js")[0] == []


def test_refusal_names_the_owning_agent(project):
    b = scoped(project, "frontend-dev", "_agency/baseline/threat-model.md")[0]
    assert "security-lead" in b[0]


def test_agency_agent_without_a_card_may_not_write(project):
    b, _ = guard.check(call("Write", {"file_path": str(project / "x.md"), "content": ""}, "devsecops-agency:ghost"), SCOPED)
    assert any(x.startswith("B5") and "no role card" in x for x in b)


def test_yaml_fallback_keeps_write_scope(monkeypatch, tmp_path):
    # With hooks/role-cards.json unreadable, the guard must still enforce B5 from the YAML cards.
    import shutil
    root = tmp_path / "plug"
    (root / "hooks").mkdir(parents=True)
    (root / "agents").mkdir()
    shutil.copy(Path(GUARD).parent.parent / "agents" / "role-cards.yaml", root / "agents" / "role-cards.yaml")
    monkeypatch.setattr(guard, "PLUGIN_ROOT", root)
    cards = guard.load_cards()
    assert cards["security-lead"]["write_scope"] and "threat-model.md" in cards["security-lead"]["write_scope"]


def test_refusal_for_code_names_the_builders():
    cards = guard.load_cards()
    b, _ = guard.check(call("Write", {"file_path": os.path.join(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()), "src", "app.js"), "content": ""},
                            "devsecops-agency:engineering-lead"), cards)
    assert len(b) == 1 and b[0].startswith("B5") and "frontend-dev" in b[0] and "backend-dev" in b[0]


@pytest.mark.parametrize("rel", [
    "_vision/VISION.md", "_vision/projects/app.md", "_vision/history/2026-11-25.md",
    "_vision/rhythm/state.json", "_vision/rhythm/heartbeat-2026-11-25.md",
    "_memory/MEMORY.md", "_memory/memory/2026-11-25.md", "_memory/patterns/app.md", "_memory/index.json",
])
def test_ceo_owns_its_vision_and_memory_records(rel):
    scope = guard.load_cards()["ceo"]["write_scope"]
    assert guard.in_scope(rel, scope) and guard.in_scope("outputs/devsecops-agency/" + rel, scope), rel


@pytest.mark.parametrize("rel", [
    "_vision/audit/x.md", "_vision/eval/x.md", "_vision/cost/x.md", "_vision/traces/t.jsonl", "_vision/notes.md",
])
def test_ceo_does_not_get_the_other_vision_records(rel):
    assert not guard.in_scope(rel, guard.load_cards()["ceo"]["write_scope"]), rel




@pytest.mark.parametrize("rel", [
    "app/_worktrees/cto-0/worktree.json", "app/_worktrees/engineering-lead-1/src/worktree.json",
    "app/_worktrees/red-team-fuzzer-1/worktree.json", "app/_worktrees/_merged/cto-0-x/worktree.json",
    "app/_worktrees/cto-0/architecture.md", "app/_worktrees/engineering-lead-1/src/app.js",
])
def test_ceo_has_no_worktree_grant(rel):
    scope = guard.load_cards()["ceo"]["write_scope"]
    assert not guard.in_scope(rel, scope) and not guard.in_scope("outputs/devsecops-agency/" + rel, scope), rel


MEM = "outputs/devsecops-agency/_memory/"
MEMORY_MD = "# Memory\n\n## Recurring risks\n- r1\n\n## Proven stacks\n- s1\n"


@pytest.mark.parametrize("rel", [MEM + "MEMORY.md", MEM + "memory/2026-11-25.md", "_memory/MEMORY.md"])
def test_memory_files_keep_their_lines(rel):
    assert guard.is_lines_kept(rel) and not guard.is_append_only(rel)


@pytest.mark.parametrize("new", [
    "# Memory\n\n## Recurring risks\n- r1\n- r2\n\n## Proven stacks\n- s1\n",   # insert under a section
    "## 2026-11-25\n- new\n\n" + MEMORY_MD,                                     # prepend (newest-at-top)
    MEMORY_MD + "- s2\n",                                                       # append
    MEMORY_MD.rstrip("\n") + "\n- s2",                                          # append, no final newline
])
def test_lines_kept_allows_new_lines_anywhere(project, new):
    f = project / MEM / "MEMORY.md"
    f.parent.mkdir(parents=True)
    f.write_text(MEMORY_MD, encoding="utf-8")
    assert blocks(call("Write", {"file_path": str(f), "content": new})) == []


@pytest.mark.parametrize("new", [
    MEMORY_MD.replace("- r1", "- r1 (edited)"),                                 # changed line
    MEMORY_MD.replace("- r1\n", ""),                                            # deleted line
    "# Memory\n\n## Proven stacks\n- s1\n\n## Recurring risks\n- r1\n",          # reordered
])
def test_lines_kept_refuses_changed_removed_or_reordered_lines(project, new):
    f = project / MEM / "MEMORY.md"
    f.parent.mkdir(parents=True)
    f.write_text(MEMORY_MD, encoding="utf-8")
    assert any(b.startswith("B2 lines kept") for b in blocks(call("Write", {"file_path": str(f), "content": new})))


def test_lines_kept_checks_edits_too(project):
    f = project / MEM / "memory" / "2026-11-25.md"
    f.parent.mkdir(parents=True)
    f.write_text("- a\n- b\n", encoding="utf-8")
    ok = call("Edit", {"file_path": str(f), "old_string": "- a\n", "new_string": "- a\n- a2\n"})
    bad = call("Edit", {"file_path": str(f), "old_string": "- b", "new_string": "- B"})
    assert blocks(ok) == [] and any(b.startswith("B2 lines kept") for b in blocks(bad))


def test_adoption_session_log_is_allowed_and_append_only(project):
    rel = "_agency/_sessions/ceo/s1.jsonl"
    assert guard.is_append_only(rel)
    assert guard.check(call("Write", {"file_path": str(project / rel), "content": "{}\n"}), guard.load_cards())[0] == []


def test_lines_kept_ignores_line_endings(project):
    f = project / MEM / "MEMORY.md"
    f.parent.mkdir(parents=True)
    f.write_bytes(MEMORY_MD.replace("\n", "\r\n").encode("utf-8"))
    new = MEMORY_MD.replace("- r1\n", "- r1\n- r2\n")
    assert blocks(call("Write", {"file_path": str(f), "content": new})) == []


@pytest.mark.parametrize("rel", ["chat.jsonl", "outputs/devsecops-agency/_memory/MEMORY.md"])
def test_b2_refuses_when_the_current_file_is_not_utf8(project, rel):
    f = project / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_bytes(b"\xff\xfe old\n")
    assert any(b.startswith("B2") for b in blocks(call("Write", {"file_path": str(f), "content": "new\n"})))


IDX = {"lastRem": None, "xref": {"a": "LESSONS.md > a"}, "knobHistory": [{"knob": "dedupe", "to": 0.85}]}


def _index(project, data):
    f = project / MEM / "index.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(data), encoding="utf-8")
    return f


@pytest.mark.parametrize("new", [
    dict(IDX, lastRem="2026-11-25T00:00:00Z", xref={}),                                     # structure rewritten
    dict(IDX, knobHistory=IDX["knobHistory"] + [{"knob": "dedupe", "to": 0.9}]),             # knob appended
])
def test_memory_index_may_be_rewritten_but_keeps_knob_history(project, new):
    f = _index(project, IDX)
    assert blocks(call("Write", {"file_path": str(f), "content": json.dumps(new)})) == []


@pytest.mark.parametrize("new", [
    json.dumps(dict(IDX, knobHistory=[])),                                                    # history dropped
    json.dumps(dict(IDX, knobHistory=[{"knob": "dedupe", "to": 0.5}])),                      # history edited
    json.dumps({k: v for k, v in IDX.items() if k != "knobHistory"}),                         # key removed
    "not json",
])
def test_memory_index_refuses_a_lost_or_edited_knob_history(project, new):
    f = _index(project, IDX)
    assert any(b.startswith("B2 knob history") for b in blocks(call("Write", {"file_path": str(f), "content": new})))


def test_memory_index_first_write_passes(project):
    f = project / MEM / "index.json"
    assert blocks(call("Write", {"file_path": str(f), "content": json.dumps(IDX)})) == []
    assert guard.is_memory_index("_memory/index.json") and not guard.is_append_only(MEM + "index.json")
