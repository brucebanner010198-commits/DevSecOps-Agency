"""Tests for scripts/release_check.py (run: python -m pytest scripts)."""
import json
import os
import sys

import pytest
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
TODAY = "2026-11-26"


def verdict(colour, findings=(), open_items=(), regression="0.5", items=None):
    body = f"gate: {colour}\n\n"
    body += "".join(f"finding: {fid} class: {cls}\n" for fid, cls in findings)
    if regression is not None:
        body += f"regression: {regression}\n"
    body += "".join(f"item {i}: {r}\n" for i, r in (items or {}).items())
    if open_items:
        body += "\n## Open items\n" + "".join(f"- {o}\n" for o in open_items)
    return body


def gate_setup(tmp_path, colours=None, bodies=None):
    colours = dict(colours or {c: "green" for c in LEADS})
    bodies = dict(bodies or {})
    proj = tmp_path / "outputs" / "devsecops-agency" / "app"
    proj.mkdir(parents=True)
    (proj / "status.json").write_text(json.dumps({"gates": {"byCouncil": dict(colours)}}), encoding="utf-8")
    (proj / "acceptance.md").write_text("- a1: totals are right\n- a2: works offline\n", encoding="utf-8")
    receipts = [w("ceo", str(proj / "acceptance.md"), ts="2026-11-24T09:00:00Z")]
    for c, lead in LEADS.items():
        default = verdict(colours[c], items={"a1": "pass", "a2": "pass"} if c == "evaluation" else None,
                          regression="0.5" if c == "evaluation" else None)
        (proj / rc.VERDICT_FILES[c]).write_text(bodies.get(c, default), encoding="utf-8")
        receipts.append(w(lead, str(proj / rc.VERDICT_FILES[c])))
    return proj, receipts


def gflags(tmp_path, proj, receipts, since=SINCE):
    dirs = [tmp_path / "outputs" / "devsecops-agency" / "_decisions"]
    return rc.gate_report(receipts, COUNCILS, proj, since, dirs, TODAY)["flags"]


def waiver(tmp_path, name="ADR-0100-waiver-grant-x.md", **kw):
    fm = dict(kind="waiver-grant", approver="user", project="app", council="security", finding="sec-7",
              **{"class": "xss"}, approved="2026-11-25", expires="2026-12-31")
    fm.update(kw)
    d = tmp_path / "outputs" / "devsecops-agency" / "_decisions"
    d.mkdir(parents=True, exist_ok=True)
    (d / name).write_text("---\n" + "".join(f"{k}: {v}\n" for k, v in fm.items()) + "---\n", encoding="utf-8")


RED_SEC = {"security": "red", "evaluation": "green", "red-team": "green", "audit": "green"}


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


def test_gate_reads_relative_receipt_paths_against_the_launch_folder(tmp_path):
    proj, rs = gate_setup(tmp_path)
    rs = [dict(r, path=os.path.relpath(r["path"], tmp_path)) for r in rs]
    dirs = [tmp_path / "outputs" / "devsecops-agency" / "_decisions"]
    assert rc.gate_report(rs, COUNCILS, proj, SINCE, dirs, TODAY, base=tmp_path)["flags"] == []


def test_gate_flags_a_status_json_mismatch(tmp_path):
    proj, rs = gate_setup(tmp_path)
    (proj / "status.json").write_text(json.dumps({"gates": {"byCouncil": {c: "green" for c in LEADS} | {"audit": "yellow"}}}), encoding="utf-8")
    assert any("status.json says yellow, its verdict says green" in x for x in gflags(tmp_path, proj, rs))


def test_gate_reads_only_the_top_gate_line(tmp_path):
    proj, rs = gate_setup(tmp_path, bodies={"audit": "## Quote\ngate: green\n"})
    assert any("CAO (audit) close-audit.md has no valid gate: line" in x for x in gflags(tmp_path, proj, rs))


def test_gate_red_needs_a_valid_waiver_for_every_finding(tmp_path):
    proj, rs = gate_setup(tmp_path, colours=RED_SEC, bodies={"security": verdict("red", [("sec-7", "xss"), ("sec-70", "csrf")])})
    assert any("finding sec-7 is red" in x for x in gflags(tmp_path, proj, rs))
    waiver(tmp_path)
    f = gflags(tmp_path, proj, rs)
    assert not any("finding sec-7 " in x for x in f) and any("finding sec-70 is red" in x for x in f)
    waiver(tmp_path, name="ADR-0101-waiver-grant-y.md", finding="sec-70", **{"class": "csrf"})
    assert gflags(tmp_path, proj, rs) == []


def test_gate_red_with_no_findings_listed_fails(tmp_path):
    proj, rs = gate_setup(tmp_path, colours=RED_SEC)
    waiver(tmp_path)
    assert any("lists no findings" in x for x in gflags(tmp_path, proj, rs))


@pytest.mark.parametrize("bad", [dict(approver="ceo"), dict(expires="2026-11-01"), dict(project="other"),
                                 dict(expires="never"), dict(expires="2999-01-01"), dict(approved="x"),
                                 dict(council="audit"), dict(finding="sec-77"), {"class": ""},
                                 {"class": "raw-secret"}, {"class": "ASI-03"}])
def test_gate_rejects_an_invalid_waiver(tmp_path, bad):
    proj, rs = gate_setup(tmp_path, colours=RED_SEC, bodies={"security": verdict("red", [("sec-7", "xss")])})
    waiver(tmp_path, **bad)
    assert any("finding sec-7 is red with no valid waiver" in x for x in gflags(tmp_path, proj, rs))


def test_gate_never_waives_a_non_waivable_finding(tmp_path):
    proj, rs = gate_setup(tmp_path, colours=RED_SEC, bodies={"security": verdict("red", [("sec-7", "raw-secret")])})
    waiver(tmp_path)
    assert any("non-waivable class" in x for x in gflags(tmp_path, proj, rs))


def test_gate_yellow_needs_real_open_items(tmp_path):
    colours = {"security": "green", "evaluation": "green", "red-team": "yellow", "audit": "green"}
    proj, rs = gate_setup(tmp_path, colours=colours, bodies={"red-team": verdict("yellow", open_items=["none"])})
    assert any("yellow with no open items" in x for x in gflags(tmp_path, proj, rs))
    (proj / "red-team.md").write_text(verdict("yellow", open_items=["rate limit untested"]), encoding="utf-8")
    assert gflags(tmp_path, proj, rs) == []


def test_gate_regression_of_five_points_must_be_red(tmp_path):
    proj, rs = gate_setup(tmp_path, bodies={"evaluation": verdict("green", regression="7", items={"a1": "pass", "a2": "pass"})})
    assert any("regression of 7 points must be red" in x for x in gflags(tmp_path, proj, rs))
    (proj / "close-eval.md").write_text(verdict("green", regression=None, items={"a1": "pass", "a2": "pass"}), encoding="utf-8")
    assert any("no regression: line" in x for x in gflags(tmp_path, proj, rs))


def test_gate_acceptance_items_must_match_and_a_fail_is_red(tmp_path):
    proj, rs = gate_setup(tmp_path, bodies={"evaluation": verdict("green", items={"a1": "pass"})})
    assert any("missing ['a2']" in x for x in gflags(tmp_path, proj, rs))
    (proj / "close-eval.md").write_text(verdict("green", items={"a1": "pass", "a2": "fail"}), encoding="utf-8")
    assert any("item failed but its gate is not red" in x for x in gflags(tmp_path, proj, rs))


def test_gate_acceptance_set_is_frozen_and_the_ceos(tmp_path):
    proj, rs = gate_setup(tmp_path)
    rs = rs + [w("eval-designer", str(proj / "acceptance.md"), ts="2026-11-24T09:30:00Z")]
    f = gflags(tmp_path, proj, rs)
    assert any("written 2 times" in x for x in f) and any("evaluation council" in x for x in f)
    assert any("other than the CEO" in x for x in f)


def test_gate_acceptance_must_precede_the_verdicts(tmp_path):
    proj, rs = gate_setup(tmp_path)
    rs = [dict(r, ts="2026-11-25T00:00:00Z") if r["path"].endswith("acceptance.md") else r for r in rs]
    assert any("written after a verdict" in x for x in gflags(tmp_path, proj, rs))


def test_gate_run_starts_at_acceptance_even_with_an_early_since(tmp_path):
    proj, rs = gate_setup(tmp_path)
    rs = [dict(r, ts="2026-11-24T08:00:00+00:00") if r["path"].endswith("security-report.md") else r for r in rs]
    f = gflags(tmp_path, proj, rs, since="2026-01-01T00:00:00Z")
    assert any("CISO (security) was not the last to write security-report.md in this run" in x for x in f)


def test_gate_compares_z_and_offset_times(tmp_path):
    proj, rs = gate_setup(tmp_path)
    rs = [dict(r, ts=r["ts"].replace("Z", "+00:00")) for r in rs]
    assert gflags(tmp_path, proj, rs, since="2026-11-24T00:00:00+00:00") == []


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


def test_gate_mode_needs_project_and_since_and_exits_non_zero(tmp_path, capsys):
    (tmp_path / ".devsecops-agency").mkdir()
    (tmp_path / ".devsecops-agency" / "receipts.jsonl").write_text("", encoding="utf-8")
    assert rc.main(["x", str(tmp_path), "--gate", "--project", "outputs/devsecops-agency/app"]) == 2
    proj, rs = gate_setup(tmp_path)
    (tmp_path / ".devsecops-agency" / "receipts.jsonl").write_text("\n".join(json.dumps(r) for r in rs), encoding="utf-8")
    args = ["x", str(tmp_path), "--gate", "--project", "outputs/devsecops-agency/app", "--since", SINCE]
    assert rc.main(args) == 0
    (proj / "close-eval.md").write_text("gate: green\n", encoding="utf-8")
    assert rc.main(args) == 1 and "no regression: line" in capsys.readouterr().out


def correction(tmp_path, **kw):
    fm = dict(kind="user-decision", approver="user", project="app", decision="acceptance-correction",
              approved="2026-11-24T09:15:00Z")
    fm.update(kw)
    d = tmp_path / "outputs" / "devsecops-agency" / "_decisions"
    d.mkdir(parents=True, exist_ok=True)
    (d / "ADR-0200-acceptance-correction.md").write_text("---\n" + "".join(f"{k}: {v}\n" for k, v in fm.items()) + "---\n", encoding="utf-8")


def test_gate_acceptance_correction_needs_the_chairman(tmp_path):
    proj, rs = gate_setup(tmp_path)
    rs = rs + [w("ceo", str(proj / "acceptance.md"), ts="2026-11-24T09:30:00Z")]
    assert any("written 2 times" in x for x in gflags(tmp_path, proj, rs))
    correction(tmp_path, approver="ceo")
    assert any("written 2 times" in x for x in gflags(tmp_path, proj, rs))
    correction(tmp_path)
    assert gflags(tmp_path, proj, rs) == []


def test_gate_fails_on_an_empty_acceptance_set(tmp_path):
    proj, rs = gate_setup(tmp_path, bodies={"evaluation": verdict("green", items={})})
    (proj / "acceptance.md").write_text("no items here\n", encoding="utf-8")
    assert any("lists no items" in x for x in gflags(tmp_path, proj, rs))


def test_gate_record_is_written_by_the_script(tmp_path):
    (tmp_path / ".devsecops-agency").mkdir()
    proj, rs = gate_setup(tmp_path)
    (tmp_path / ".devsecops-agency" / "receipts.jsonl").write_text("\n".join(json.dumps(r) for r in rs), encoding="utf-8")
    rec = tmp_path / "outputs" / "devsecops-agency" / "_vision" / "audit" / "gate.md"
    args = ["x", str(tmp_path), "--gate", "--project", "outputs/devsecops-agency/app", "--since", SINCE, "--record", str(rec)]
    assert rc.main(args) == 0 and rec.read_text(encoding="utf-8").startswith("gate: green")
    (proj / "close-eval.md").write_text("gate: green\n", encoding="utf-8")
    assert rc.main(args) == 1 and rec.read_text(encoding="utf-8").startswith("gate: red")

