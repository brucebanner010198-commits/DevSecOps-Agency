"""M4 demo — the Vault (act without reveal) + the golden-share gate.

Run from os/trust-spine/:

    python demos/m4_vault_golden_share_demo.py

Part 1 (regression stress-test Scenario B): a malicious page hides an input
field off-screen to harvest an autofilled card number. The Vault refuses to
paste into the hidden field, and into a spoofed origin — but pastes into the
real, visible field without the agent ever seeing the number.

Part 2: a Tier-3 spend is held pending; only the Owner's golden-share signature
over that exact spend lets it run. A signature for a different amount does not.
"""

from __future__ import annotations

import os
import shutil
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(_HERE))

from trust_spine.capabilities import SECRET_ACCESS, SPEND, CapabilityBroker  # noqa: E402
from trust_spine.golden_share import GoldenShare, action_intent  # noqa: E402
from trust_spine.kernel import ActionRequest, TrustKernel  # noqa: E402
from trust_spine.ledger import Ledger  # noqa: E402
from trust_spine.policy import Policy  # noqa: E402
from trust_spine.vault import FieldDescriptor, Vault  # noqa: E402
from trust_spine.verifier import Verifier  # noqa: E402

LEDGER_DIR = os.path.join(_HERE, ".m4-demo-ledger")


def main() -> int:
    if os.path.exists(LEDGER_DIR):
        shutil.rmtree(LEDGER_DIR)
    led = Ledger(LEDGER_DIR)

    vault = Vault()
    vault.store("card", "4242424242424242", bound_origin="pay.utility.com", bound_fingerprint="AA:BB")

    broker = CapabilityBroker()
    broker.grant("pay-leaf", {SECRET_ACCESS})
    broker.grant("ceo", {SPEND})  # may *initiate* spends; each one still needs the golden-share

    gs = GoldenShare()
    kernel = TrustKernel(
        led, Verifier(Policy(), capability_broker=broker), vault=vault, golden_share=gs
    )

    print("─" * 80)
    print("Trust Spine v0 · M4 Vault (act-without-reveal) + golden-share gate")
    print("─" * 80)

    print("\n[1] Confused-deputy autofill phishing (Vault refuses; agent never sees the card)")
    # `pasted` is the TRUSTED destination field, registered by the OS/compositor
    # for the bound origin — NOT supplied by the agent. The agent only names the
    # secret + field; it can neither supply nor capture where the plaintext goes.
    pasted = []
    vault.register_destination("pay.utility.com", pasted.append)
    fields = [
        ("hidden off-screen trap", FieldDescriptor(
            origin="pay.utility.com", cert_fingerprint="AA:BB",
            style={"opacity": 0, "left": "-9999px"})),
        ("spoofed origin", FieldDescriptor(origin="pay.attacker.com", cert_fingerprint="AA:BB")),
        ("real visible field", FieldDescriptor(
            origin="pay.utility.com", cert_fingerprint="AA:BB", visible=True)),
    ]
    for label, fd in fields:
        res = kernel.submit(ActionRequest(
            actor="pay-leaf", action="vault.use", secret_name="card", field=fd))
        icon = "✓ paste " if res.allowed else "⛔ REFUSE"
        masked = ""
        if res.allowed and pasted:
            tail = pasted[-1].decode("utf-8", errors="replace")[-4:]
            masked = f"  (pasted ****{tail} into the verified field)"
        print(f"    {icon} {label:<22}{masked}")
        if not res.allowed:
            print(f"             ↳ {res.reason}")
    print("    the agent's result carries no plaintext — the paste went Vault → field directly")

    print("\n[2] Golden-share gate on a Tier-3 spend")
    # The spend is executed from the SIGNED intent via a trusted handler — never
    # an opaque agent callable — so the Owner's signature binds *what runs*.
    charged = []
    kernel.register_effect(
        "spend", lambda signed: charged.append(signed.inputs["amount"]) or {"charged": signed.inputs["amount"]}
    )
    inputs, context, nonce = {"amount": 49.0}, {"to": "utility-co"}, "spend-1"
    # 2a — no signature → held
    r1 = kernel.submit(ActionRequest(actor="ceo", action="spend", inputs=inputs, context=context))
    print(f"    ✋ no signature        → {r1.decision}  ({r1.reason})")
    # 2b — signature bound to $49 won't authorise a swapped-in $4900
    bad_sig = gs.approve(action_intent("ceo", "spend", {"amount": 49.0}, context, nonce=nonce))
    r2 = kernel.submit(ActionRequest(actor="ceo", action="spend", inputs={"amount": 4900.0},
                                     context=context, golden_share=bad_sig, nonce=nonce))
    print(f"    ⛔ swapped to $4900     → {r2.decision}  (signature bound to $49 won't authorise $4900)")
    # 2c — correct signature + single-use nonce → runs exactly once
    good_sig = gs.approve(action_intent("ceo", "spend", inputs, context, nonce=nonce))
    r3 = kernel.submit(ActionRequest(actor="ceo", action="spend", inputs=inputs, context=context,
                                     golden_share=good_sig, nonce=nonce))
    print(f"    ✓ owner signed $49     → {r3.decision}  · effect ran={charged == [49.0]}")
    # 2d — the same approval can't be replayed
    r4 = kernel.submit(ActionRequest(actor="ceo", action="spend", inputs=inputs, context=context,
                                     golden_share=good_sig, nonce=nonce))
    print(f"    ⛔ replay same approval → {r4.decision}  (single-use nonce already burned)")

    print("\n" + "─" * 80)
    log = led.verify_log()
    print(f"    whole-log verify: ok={log['ok']}  receipts={log['count']}")
    print("    Secrets act without reveal; reserved spends need the human's key.")
    print("─" * 80)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
