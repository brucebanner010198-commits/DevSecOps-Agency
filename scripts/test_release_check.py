"""Tests for scripts/release_check.py (run: python -m pytest scripts)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import release_check as rc  # noqa: E402

P = "devsecops-agency:"
COUNCILS = rc.load_councils()


def d(agent, target, decision="allow"):
    return {"agent": P + agent, "tool": "Agent", "target": P + target, "decision": decision}


def w(agent, decision="allow"):
    return {"agent": P + agent, "tool": "Write", "path": "x.md", "decision": decision}


def flags(receipts, gates=None):
    return rc.report(receipts, COUNCILS, gates or {})["flags"]


def test_all_four_blocking_councils_recording_a_verdict_passes():
    rs = [w("security-lead"), w("evaluation-lead"), w("red-team-lead"), w("cao")]
    assert flags(rs) == []


def test_missing_councils_are_flagged():
    f = flags([d("ceo", "security-lead"), w("security-lead")])
    assert sorted(x.split()[0] for x in f) == ["CAO", "CEVO", "CRT"]


def test_a_specialist_of_the_council_counts():
    rs = [w("threat-modeler"), w("benchmark-runner"), w("adversarial-prompter"), w("gate-auditor")]
    assert flags(rs) == []


def test_denied_writes_do_not_count():
    rs = [w("security-lead", "deny"), w("evaluation-lead"), w("red-team-lead"), w("cao")]
    assert any(x.startswith("CISO") for x in flags(rs))


def test_red_without_user_waiver_is_flagged_and_free_text_colour_is_read():
    rs = [w("security-lead"), w("evaluation-lead"), w("red-team-lead"), w("cao")]
    f = flags(rs, {"security": {"gate": "red (two Highs open)"}})
    assert any("red with no user waiver" in x for x in f)
    assert flags(rs, {"security": {"gate": "red", "waivedBy": "user"}}) == []


def test_status_json_gates_count_as_a_verdict(tmp_path):
    proj = tmp_path / "outputs" / "devsecops-agency" / "app"
    proj.mkdir(parents=True)
    (proj / "status.json").write_text(json.dumps({"gates": {"security": "green", "evaluation": "green",
                                                            "red-team": "yellow", "audit": "green"}}), encoding="utf-8")
    assert flags([], rc.gates_from_status(tmp_path)) == []


def test_main_reads_the_receipts(tmp_path, capsys):
    (tmp_path / ".devsecops-agency").mkdir()
    (tmp_path / ".devsecops-agency" / "receipts.jsonl").write_text(json.dumps(w("security-lead")) + "\nbad\n", encoding="utf-8")
    assert rc.main(["x", str(tmp_path)]) == 0
    assert "FLAG CEVO" in capsys.readouterr().out
