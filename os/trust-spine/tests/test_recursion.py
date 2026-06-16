from trust_spine.ledger import Ledger
from trust_spine.policy import Policy
from trust_spine.recursion import RecursionBudget, run_recursive_company
from trust_spine.kernel import TrustKernel
from trust_spine.verifier import Verifier


def _kernel(tmp_path):
    led = Ledger(str(tmp_path / "led"))
    return TrustKernel(led, Verifier(Policy(egress_allowlist=set()))), led


def test_run_produces_verifiable_receipts(tmp_path):
    k, led = _kernel(tmp_path)
    summary = run_recursive_company(k, "summarise my inbox", max_depth=3, branching=2)
    assert summary.actions == len(led)
    assert summary.leaves > 0
    assert led.verify_log()["ok"] is True  # the whole run replays + verifies


def test_egress_probe_is_vetoed_mid_recursion(tmp_path):
    k, led = _kernel(tmp_path)
    summary = run_recursive_company(k, "research a vendor", egress_probe=True)
    assert summary.vetoes >= 1
    # the veto is recorded as a receipt
    assert any(r.action == "net.egress" and r.decision == "veto" for r in led.all())


def test_budget_bounds_runaway_recursion(tmp_path):
    k, led = _kernel(tmp_path)
    budget = RecursionBudget(max_actions=5)
    summary = run_recursive_company(
        k, "explode", max_depth=8, branching=4, budget=budget, egress_probe=False
    )
    assert summary.halted_by_budget is True
    assert summary.actions <= 5  # never exceeds the ceiling
    assert len(led) <= 5


def test_replay_is_deterministic(tmp_path):
    k, led = _kernel(tmp_path)
    run_recursive_company(k, "deterministic goal", max_depth=2, branching=2, egress_probe=False)
    actions_first = [(r.actor, r.action, r.decision) for r in led.all()]
    # reload from disk and confirm the exact same sequence verifies
    reloaded = Ledger(led.path)
    actions_again = [(r.actor, r.action, r.decision) for r in reloaded.all()]
    assert actions_first == actions_again
    assert reloaded.verify_log()["ok"] is True
