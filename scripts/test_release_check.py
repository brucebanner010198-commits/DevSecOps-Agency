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


# --- gate mode (draft ADR-0010, CONSTITUTION §8.6) ----------------------------------------

LEADS = {"security": "security-lead", "evaluation": "evaluation-lead", "red-team": "red-team-lead", "audit": "cao"}
SINCE = "2026-11-24T00:00:00Z"


def gate_setup(tmp_path, colours=None, acceptance="pass", extra=""):
    colours = colours or {c: "green" for c in LEADS}
    proj = tmp_path / "outputs" / "devsecops-agency" / "app"
    proj.mkdir(parents=True)
    (proj / "status.json").write_text(json.dumps({"gates": {"byCouncil": dict(colours)}}), encoding="utf-8")
    (proj / "acceptance.md").write_text("- a1\n", encoding="utf-8")
    receipts = [w("ceo", str(proj / "acceptance.md"), ts="2026-11-24T09:00:00Z")]
    for c, lead in LEADS.items():
        body = f"gate: {colours[c]}\n" + ("acceptance: " + acceptance + "\n" if c == "evaluation" else "") + extra
        (proj / rc.VERDICT_FILES[c]).write_text(body, encoding="utf-8")
        receipts.append(w(lead, str(proj / rc.VERDICT_FILES[c])))
    return proj, receipts


def gflags(tmp_path, proj, receipts, today="2026-11-26"):
    dirs = [tmp_path / "outputs" / "devsecops-agency" / "_decisions"]
    return rc.gate_report(receipts, COUNCILS, proj, SINCE, dirs, today)["flags"]


def waiver(tmp_path, **kw):
    fm = dict(kind="waiver-grant", approver="user", project="app", council="security", finding="sec-7", expires="2026-12-31")
    fm.update(kw)
    d = tmp_path / "outputs" / "devsecops-agency" / "_decisions"
    d.mkdir(parents=True, exist_ok=True)
    (d / "ADR-0100-waiver-grant-x.md").write_text("---\n" + "".join(f"{k}: {v}\n" for k, v in fm.items()) + "---\n", encoding="utf-8")


def test_gate_passes_with_every_verdict_green(tmp_path):
    proj, rs = gate_setup(tmp_path)
    assert gflags(tmp_path, proj, rs) == []


def test_gate_fails_closed_without_status_json(tmp_path):
    proj, rs = gate_setup(tmp_path)
    (proj / "status.json").write_text("{not json", encoding="utf-8")
    assert any("status.json is missing" in f for f in gflags(tmp_path, proj, rs))


def test_gate_needs_the_councils_own_verdict_file(tmp_path):
    proj, rs = gate_setup(tmp_path)
    (proj / "red-team.md").unlink()
    rs = rs + [w("frontend-dev", str(proj / "close-audit.md"), ts="2026-11-24T11:00:00Z")]
    f = gflags(tmp_path, proj, rs)
    assert any("CRT (red-team) has no verdict file" in x for x in f)
    assert any("CAO (audit) was not the last to write close-audit.md" in x for x in f)


def test_gate_flags_a_status_json_mismatch(tmp_path):
    proj, rs = gate_setup(tmp_path)
    (proj / "status.json").write_text(json.dumps({"gates": {"byCouncil": {c: "green" for c in LEADS} | {"audit": "yellow"}}}), encoding="utf-8")
    assert any("status.json says yellow, its verdict says green" in x for x in gflags(tmp_path, proj, rs))


def test_gate_red_needs_a_valid_waiver_adr(tmp_path):
    proj, rs = gate_setup(tmp_path, colours={"security": "red", "evaluation": "green", "red-team": "green", "audit": "green"},
                          extra="finding sec-7: XSS in export\n")
    assert any("no valid waiver-grant ADR" in x for x in gflags(tmp_path, proj, rs))
    waiver(tmp_path, finding="sec-9")
    assert any("no valid waiver-grant ADR" in x for x in gflags(tmp_path, proj, rs))
    waiver(tmp_path, approver="ceo")
    assert any("no valid waiver-grant ADR" in x for x in gflags(tmp_path, proj, rs))
    waiver(tmp_path, expires="2026-11-01")
    assert any("no valid waiver-grant ADR" in x for x in gflags(tmp_path, proj, rs))
    waiver(tmp_path, **{"class": "raw-secret"})
    assert any("no valid waiver-grant ADR" in x for x in gflags(tmp_path, proj, rs))
    waiver(tmp_path)
    assert gflags(tmp_path, proj, rs) == []


def test_gate_yellow_needs_open_items(tmp_path):
    proj, rs = gate_setup(tmp_path, colours={"security": "green", "evaluation": "green", "red-team": "yellow", "audit": "green"})
    assert any("yellow with no open items" in x for x in gflags(tmp_path, proj, rs))
    (proj / "red-team.md").write_text("gate: yellow\n\n## Open items\n- rate limit untested\n", encoding="utf-8")
    assert gflags(tmp_path, proj, rs) == []


def test_gate_failed_acceptance_must_be_a_cevo_red(tmp_path):
    proj, rs = gate_setup(tmp_path, acceptance="fail")
    assert any("acceptance failed but its gate is not red" in x for x in gflags(tmp_path, proj, rs))


def test_gate_acceptance_set_is_frozen_and_not_cevos(tmp_path):
    proj, rs = gate_setup(tmp_path)
    rs = rs + [w("eval-designer", str(proj / "acceptance.md"))]
    f = gflags(tmp_path, proj, rs)
    assert any("written 2 times" in x for x in f) and any("evaluation council" in x for x in f)
    assert any("other than the CEO" in x for x in f)


def test_gate_acceptance_must_precede_the_verdicts(tmp_path):
    proj, rs = gate_setup(tmp_path)
    rs = [dict(r, ts="2026-11-25T00:00:00Z") if r["path"].endswith("acceptance.md") else r for r in rs]
    assert any("written after a verdict" in x for x in gflags(tmp_path, proj, rs))


def test_gate_blocking_council_cannot_return_n_a(tmp_path):
    proj, rs = gate_setup(tmp_path, colours={"security": "n/a", "evaluation": "green", "red-team": "green", "audit": "green"})
    assert any("CISO (security) security-report.md has no valid gate: line" in x for x in gflags(tmp_path, proj, rs))


def test_gate_informing_red_needs_a_user_waiver(tmp_path):
    proj, rs = gate_setup(tmp_path)
    st = json.loads((proj / "status.json").read_text(encoding="utf-8"))
    st["gates"]["byCouncil"]["quality"] = "red"
    (proj / "status.json").write_text(json.dumps(st), encoding="utf-8")
    assert any("informing council quality is red" in x for x in gflags(tmp_path, proj, rs))
    waiver(tmp_path, council="quality", finding="qa-3")
    assert gflags(tmp_path, proj, rs) == []


def test_gate_ignores_verdicts_written_before_since(tmp_path):
    proj, rs = gate_setup(tmp_path)
    rs = [dict(r, ts="2026-01-01T00:00:00Z") if r["path"].endswith("security-report.md") else r for r in rs]
    assert any("CISO (security) was not the last to write security-report.md" in x for x in gflags(tmp_path, proj, rs))


def test_gate_mode_needs_project_and_since_and_exits_non_zero(tmp_path, capsys):
    (tmp_path / ".devsecops-agency").mkdir()
    (tmp_path / ".devsecops-agency" / "receipts.jsonl").write_text("", encoding="utf-8")
    assert rc.main(["x", str(tmp_path), "--gate", "--project", "outputs/devsecops-agency/app"]) == 2
    proj, rs = gate_setup(tmp_path)
    (tmp_path / ".devsecops-agency" / "receipts.jsonl").write_text("\n".join(json.dumps(r) for r in rs), encoding="utf-8")
    args = ["x", str(tmp_path), "--gate", "--project", "outputs/devsecops-agency/app", "--since", SINCE, "--today", "2026-11-26"]
    assert rc.main(args) == 0
    (proj / "close-eval.md").write_text("gate: green\n", encoding="utf-8")
    assert rc.main(args) == 1 and "no acceptance: line" in capsys.readouterr().out

