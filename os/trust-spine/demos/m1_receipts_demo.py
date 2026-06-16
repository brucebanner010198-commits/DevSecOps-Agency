"""M1 demo — signed, replayable receipts with tamper detection.

Run from os/trust-spine/:

    python demos/m1_receipts_demo.py

It simulates a small Owner -> CEO -> leaf action sequence, prints the live
receipt log, offline-verifies a receipt, then TAMPERS the log on disk and shows
verification flip to FAIL. This is the visible, felt trust loop in miniature.
"""

from __future__ import annotations

import json
import os
import shutil
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))  # make `trust_spine` importable

from trust_spine.ledger import Ledger  # noqa: E402
from trust_spine.signing import Ed25519Signer, pqc_available  # noqa: E402

LEDGER_DIR = os.path.join(_HERE, ".m1-demo-ledger")

# A small, realistic action sequence: the human directs the CEO, the CEO
# delegates, the leaf acts, and one Tier-3 egress is attempted.
ACTIONS = [
    ("ceo", "plan.decompose", 1, "allow", {"goal": "summarise inbox"}, {"subtasks": 3}),
    ("comms-leaf", "mail.read", 1, "allow", {"folder": "inbox", "n": 12}, {"read": 12}),
    ("research-leaf", "fs.write", 1, "allow", {"path": "summary.md"}, {"bytes": 840}),
    ("research-leaf", "net.egress", 3, "veto", {"host": "paste.example.net"}, {"blocked": True}),
    ("ceo", "report.deliver", 2, "allow", {"channel": "owner"}, {"ok": True}),
]


def rule(title: str = "") -> None:
    print("\n" + "─" * 72)
    if title:
        print(title)
        print("─" * 72)


def main() -> int:
    if os.path.exists(LEDGER_DIR):
        shutil.rmtree(LEDGER_DIR)
    led = Ledger(LEDGER_DIR)
    signer = Ed25519Signer()  # one agent key for the demo

    alg = "ML-DSA-65 (post-quantum)" if pqc_available() else "Ed25519 (PQC pluggable)"
    rule(f"Trust Spine v0 · M1 receipts demo   signing: {alg}")

    ids = []
    for actor, action, tier, decision, inp, out in ACTIONS:
        r = led.append(
            signer,
            actor=actor,
            action=action,
            risk_tier=tier,
            decision=decision,
            inputs=inp,
            outputs=out,
        )
        ids.append(r.receipt_id)
        flag = "⛔ VETO" if decision == "veto" else "✓"
        print(f"  {flag:<7} [{actor}] {action}  (tier {tier})  id={r.receipt_id[:12]}…")

    print(f"\n  Merkle root: {led.root()}")
    print(f"  {len(led)} receipts written to {os.path.relpath(LEDGER_DIR, os.getcwd())}/receipts.jsonl")

    rule("Offline verification of a single receipt (the Tier-3 veto)")
    veto_id = ids[3]
    res = led.verify_receipt(veto_id)
    print(json.dumps(res, indent=2))
    print("  → PASS: signature valid, included in the Merkle log, chain link intact.")

    rule("Now an attacker edits the log on disk (rewrites the vetoed egress to 'allow')")
    receipts_file = os.path.join(LEDGER_DIR, "receipts.jsonl")
    with open(receipts_file, encoding="utf-8") as f:
        lines = f.readlines()
    obj = json.loads(lines[3])
    obj["decision"] = "allow"
    obj["outputs_hash"] = "0" * 64
    lines[3] = json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n"
    with open(receipts_file, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("  tampered receipts.jsonl line 4: decision veto → allow")

    tampered = Ledger(LEDGER_DIR)
    res2 = tampered.verify_receipt(veto_id)
    print(json.dumps(res2, indent=2))
    assert res2["ok"] is False and res2["signature"] is False
    print("  → FAIL: the signature no longer matches the edited receipt. Tamper detected.")

    log = tampered.verify_log()
    print(f"\n  whole-log verify: ok={log['ok']}  problems={log['problems']}")
    rule("M1 demo complete — receipts are signed, replayable, and tamper-evident.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
