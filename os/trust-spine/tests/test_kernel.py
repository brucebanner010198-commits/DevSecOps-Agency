from trust_spine.kernel import ActionRequest, TrustKernel
from trust_spine.ledger import Ledger
from trust_spine.policy import Policy
from trust_spine.verifier import Verifier


def _kernel(tmp_path, allow_hosts=()):
    led = Ledger(str(tmp_path / "led"))
    ver = Verifier(Policy(egress_allowlist=set(allow_hosts)))
    return TrustKernel(led, ver), led


def test_allowed_action_runs_effect_and_receipts(tmp_path):
    k, led = _kernel(tmp_path)
    ran = []
    res = k.submit(
        ActionRequest(
            actor="research-leaf",
            action="fs.write",
            inputs={"path": "summary.md"},
            risk_tier=1,
            effect=lambda: ran.append(True) or {"bytes": 42},
        )
    )
    assert res.allowed is True and res.decision == "allow"
    assert ran == [True]  # effect executed
    assert res.output == {"bytes": 42}
    assert led.verify_receipt(res.receipt_id)["ok"] is True


def test_vetoed_egress_does_not_run_effect(tmp_path):
    k, led = _kernel(tmp_path, allow_hosts={"api.anthropic.com"})
    ran = []
    res = k.submit(
        ActionRequest(
            actor="research-leaf",
            action="net.egress",
            inputs={"payload": "..."},
            risk_tier=3,
            context={"host": "paste.attacker.net"},
            effect=lambda: ran.append(True),
        )
    )
    assert res.allowed is False and res.decision == "veto"
    assert ran == []  # the side effect never ran
    r = led.get(res.receipt_id)
    assert r.decision == "veto" and r.risk_tier == 3


def test_pending_reserved_action_holds(tmp_path):
    k, led = _kernel(tmp_path)
    ran = []
    res = k.submit(
        ActionRequest(
            actor="ceo",
            action="spend",
            inputs={"amount": 100, "to": "vendor"},
            risk_tier=3,
            effect=lambda: ran.append(True),
        )
    )
    assert res.allowed is False and res.pending is True and res.decision == "pending"
    assert ran == []


def test_allowed_egress_to_listed_host_runs(tmp_path):
    k, led = _kernel(tmp_path, allow_hosts={"api.anthropic.com"})
    res = k.submit(
        ActionRequest(
            actor="research-leaf",
            action="net.egress",
            risk_tier=3,
            context={"host": "api.anthropic.com"},
            effect=lambda: {"status": 200},
        )
    )
    assert res.allowed is True and res.output == {"status": 200}


def test_log_stays_verifiable_after_mixed_decisions(tmp_path):
    k, led = _kernel(tmp_path, allow_hosts={"api.anthropic.com"})
    k.submit(ActionRequest(actor="a", action="fs.write", risk_tier=1))
    k.submit(ActionRequest(actor="a", action="net.egress", risk_tier=3, context={"host": "x.evil"}))
    k.submit(ActionRequest(actor="b", action="spend", risk_tier=3))
    log = led.verify_log()
    assert log["ok"] is True and log["count"] == 3


def test_same_actor_uses_stable_key(tmp_path):
    k, led = _kernel(tmp_path)
    r1 = led.get(k.submit(ActionRequest(actor="a", action="fs.write")).receipt_id)
    r2 = led.get(k.submit(ActionRequest(actor="a", action="fs.write")).receipt_id)
    r3 = led.get(k.submit(ActionRequest(actor="b", action="fs.write")).receipt_id)
    assert r1.public_key == r2.public_key  # same actor → same key
    assert r1.public_key != r3.public_key  # different actor → different key
