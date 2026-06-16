"""M5 demo — the watchable loop + one recursion (the B1 capstone).

Run from os/trust-spine/:

    python demos/m5_recursion_watch_demo.py

You watch an Owner→CEO→team→one-task-leaf company run live, each step a signed
receipt. A hijacked leaf's exfiltration attempt is vetoed mid-recursion. Then we
replay the entire run from the signed log and re-verify it. Finally we show the
budget ceiling halting a deliberately explosive decomposition.
"""

from __future__ import annotations

import os
import shutil
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))

from trust_spine.kernel import TrustKernel  # noqa: E402
from trust_spine.ledger import Ledger  # noqa: E402
from trust_spine.policy import Policy  # noqa: E402
from trust_spine.recursion import RecursionBudget, run_recursive_company  # noqa: E402
from trust_spine.verifier import Verifier  # noqa: E402

LEDGER_DIR = os.path.join(_HERE, ".m5-demo-ledger")


def main() -> int:
    if os.path.exists(LEDGER_DIR):
        shutil.rmtree(LEDGER_DIR)
    led = Ledger(LEDGER_DIR)
    kernel = TrustKernel(led, Verifier(Policy(egress_allowlist=set())))

    print("─" * 80)
    print("Trust Spine v0 · M5 watchable loop + one recursion (Owner→CEO→leaf)")
    print("─" * 80)
    print("\n[watch] live receipt stream:")

    def on_step(actor, action, res, budget):
        indent = "  " * (actor.count(".") + 1)
        icon = "✓" if res.allowed else ("⛔" if res.decision == "veto" else "✋")
        print(f"    {indent}{icon} {actor:<10} {action:<16} spent={budget.spent}")

    summary = run_recursive_company(
        kernel, "summarise my inbox and draft replies", max_depth=3, branching=2, on_step=on_step
    )
    print(
        f"\n    actions={summary.actions}  leaves={summary.leaves}  "
        f"vetoes={summary.vetoes}  halted_by_budget={summary.halted_by_budget}"
    )

    print("\n[replay] re-open the signed log from disk and re-verify the whole run:")
    reloaded = Ledger(LEDGER_DIR)
    log = reloaded.verify_log()
    print(f"    receipts={log['count']}  verify_ok={log['ok']}  root={log['root'][:16]}…")
    print("    the entire company run is reconstructable and tamper-evident from receipts alone.")

    print("\n[budget] a deliberately explosive decomposition is bounded, not fatal:")
    boom_led = Ledger(LEDGER_DIR + "-boom")
    boom_kernel = TrustKernel(boom_led, Verifier(Policy()))
    boom = run_recursive_company(
        boom_kernel, "explode", max_depth=10, branching=5,
        budget=RecursionBudget(max_actions=8), egress_probe=False,
    )
    print(f"    requested depth=10 branching=5 → capped at {boom.actions} actions; "
          f"halted_by_budget={boom.halted_by_budget}")
    shutil.rmtree(LEDGER_DIR + "-boom", ignore_errors=True)

    print("\n" + "─" * 80)
    print("    B1 Trust Spine v0 complete: receipts · verifier-with-veto · least-")
    print("    privilege · Vault · golden-share · budget-bounded recursion — all signed.")
    print("─" * 80)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
