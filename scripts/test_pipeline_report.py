"""Tests for scripts/pipeline_report.py (run: python -m pytest scripts)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import pipeline_report as pr  # noqa: E402

P = "devsecops-agency:"


def w(agent, path="x.md"):
    return {"agent": P + agent, "tool": "Write", "path": path, "decision": "allow"}


def d(agent, target):
    return {"agent": P + agent, "tool": "Agent", "target": P + target, "decision": "allow"}


CARDS = pr.load_cards()


def flagged(receipts):
    return [f["chief"] for f in pr.report(receipts, CARDS)["flagged"]]


def test_chief_that_writes_without_dispatching_is_flagged():
    assert flagged([w("security-lead", "security-report.md")]) == ["security-lead"]


def test_chief_that_dispatches_its_own_council_is_not_flagged():
    assert flagged([d("security-lead", "threat-modeler"), w("security-lead")]) == []


def test_dispatch_outside_own_council_does_not_count():
    assert flagged([d("gc", "threat-modeler"), w("gc")]) == ["gc"]


def test_builders_outside_the_council_do_not_count():
    assert flagged([d("engineering-lead", "frontend-dev"), w("engineering-lead", "architecture.md")]) == ["engineering-lead"]


def test_would_deny_calls_count_and_bare_targets_are_kept():
    rs = [{"agent": P + "qa-lead", "tool": "Agent", "target": "test-runner", "decision": "would-deny"},
          {"agent": P + "qa-lead", "tool": "Write", "path": "qa.md", "decision": "would-deny"}]
    rep = pr.report(rs, CARDS)
    assert rep["chiefs_seen"] == ["qa-lead"]
    assert rep["flagged"] == []  # the bare name still resolves to its own-council card


def test_ceo_and_specialists_are_never_flagged():
    assert flagged([w("ceo"), w("threat-modeler"), w("test-runner")]) == []


def test_denied_calls_and_other_agents_are_ignored():
    rs = [{"agent": P + "gc", "tool": "Write", "path": "x", "decision": "deny"},
          {"agent": "general-purpose", "tool": "Write", "path": "x", "decision": "allow"}]
    assert flagged(rs) == []


def test_main_reads_receipts_and_tolerates_bad_lines(tmp_path, capsys):
    folder = tmp_path / ".devsecops-agency"
    folder.mkdir()
    (folder / "receipts.jsonl").write_text(json.dumps(w("pm-lead")) + "\nnot json\n", encoding="utf-8")
    assert pr.main(["x", str(tmp_path)]) == 0
    assert "FLAG pm-lead" in capsys.readouterr().out
