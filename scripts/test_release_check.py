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


def w(agent, path="out/report.md", decision="allow", ts="2026-11-24T10:00:00Z"):
    return {"agent": P + agent, "tool": "Write", "path": path, "decision": decision, "ts": ts}


ALL = [w("security-lead"), w("evaluation-lead"), w("red-team-lead"), w("cao")]


def flags(receipts, gates=None, **kw):
    return rc.report(receipts, COUNCILS, gates or {}, **kw)["flags"]


def test_all_four_blocking_councils_recording_a_verdict_passes():
    assert flags(ALL) == []


def test_missing_councils_are_flagged():
    f = flags([d("ceo", "security-lead"), w("security-lead")])
    assert sorted(x.split()[0] for x in f) == ["CAO", "CEVO", "CRT"]


def test_a_specialist_of_the_council_counts():
    assert flags([w("threat-modeler"), w("benchmark-runner"), w("adversarial-prompter"), w("gate-auditor")]) == []


def test_denied_writes_and_log_lines_do_not_count():
    rs = [w("security-lead", decision="deny"), w("evaluation-lead", "p/chat.jsonl"),
          w("red-team-lead", "p/_sessions/rt/s.jsonl"), w("cao", "inbox.json")]
    assert sorted(x.split()[0] for x in flags(rs)) == ["CAO", "CEVO", "CISO", "CRT"]


def test_status_json_cannot_stand_in_for_a_missing_council():
    gates = {"byCouncil": {"security": "green", "evaluation": "green", "red-team": "green", "audit": "green"}}
    f = flags([w("security-lead")], gates)
    assert sorted(x.split()[0] for x in f) == ["CAO", "CEVO", "CRT"] and all("not the council's own record" in x for x in f)


def test_red_clears_only_with_a_user_signed_waiver():
    red = {"byCouncil": {"security": "red (two Highs open)"}}
    assert any("no user-signed waiver" in x for x in flags(ALL, red))
    ceo_waiver = dict(red, waivers=[{"council": "security", "waivedBy": "ceo"}])
    assert any("no user-signed waiver" in x for x in flags(ALL, ceo_waiver))
    user_waiver = dict(red, waivers=[{"council": "security", "waivedBy": "user"}])
    assert flags(ALL, user_waiver) == []


def test_project_and_since_narrow_the_evidence(tmp_path):
    other = [w(a, str(tmp_path / "other" / "x.md")) for a in ("security-lead", "evaluation-lead", "red-team-lead", "cao")]
    assert len(flags(other, project=str(tmp_path / "mine"))) == 4
    old = [w(a, ts="2026-01-01T00:00:00Z") for a in ("security-lead", "evaluation-lead", "red-team-lead", "cao")]
    assert len(flags(old, since="2026-11-01")) == 4


def test_main_reads_receipts_and_the_projects_status(tmp_path, capsys):
    (tmp_path / ".devsecops-agency").mkdir()
    proj = tmp_path / "outputs" / "devsecops-agency" / "app"
    proj.mkdir(parents=True)
    (proj / "status.json").write_text(json.dumps({"gates": {"byCouncil": {"audit": "red"}, "waivers": []}}), encoding="utf-8")
    lines = [json.dumps(w(a, str(proj / "r.md"))) for a in ("security-lead", "evaluation-lead", "red-team-lead", "cao")]
    (tmp_path / ".devsecops-agency" / "receipts.jsonl").write_text("\n".join(lines) + "\nbad\n", encoding="utf-8")
    assert rc.main(["x", str(tmp_path), "--project", "outputs/devsecops-agency/app"]) == 0
    out = capsys.readouterr().out
    assert "FLAG CAO (audit) is red with no user-signed waiver" in out and "CEVO" not in out.split("FLAG", 1)[1]
