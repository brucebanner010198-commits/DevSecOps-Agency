"""B3 demo — the de-identification trust broker ("identity stays home").

Run from os/broker/:

    python demos/b3_broker_demo.py

Voice becomes text locally; real entities are masked to synthetic surrogates and
the writing style normalized; only the masked text is eligible to leave; egress is
default-deny + receipted; the cloud reply is re-identified locally. The on-disk
receipt holds no real identity, and a sensitive send needs the golden-share.
"""

from __future__ import annotations

import os
import shutil
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_BROKER = os.path.dirname(_HERE)
sys.path.insert(0, _BROKER)
sys.path.insert(0, os.path.join(os.path.dirname(_BROKER), "trust-spine"))

from broker.broker import TrustBroker  # noqa: E402
from broker.voice import transcribe  # noqa: E402
from trust_spine.golden_share import GoldenShare, action_intent  # noqa: E402
from trust_spine.kernel import TrustKernel  # noqa: E402
from trust_spine.ledger import Ledger  # noqa: E402
from trust_spine.policy import Policy  # noqa: E402
from trust_spine.verifier import Verifier  # noqa: E402

LEDGER_DIR = os.path.join(_HERE, ".b3-demo-ledger")
SECRETS = ["Solomon Joseph", "solomon@acme.com", "4242 4242 4242 4242", "/Users/sj1136/secret.txt"]


def main() -> int:
    if os.path.exists(LEDGER_DIR):
        shutil.rmtree(LEDGER_DIR)
    led = Ledger(LEDGER_DIR)
    gs = GoldenShare()
    kernel = TrustKernel(led, Verifier(Policy(egress_allowlist={"api.anthropic.com"})), golden_share=gs)
    broker = TrustBroker(kernel)

    print("─" * 84)
    print("Trust Spine v0 · B3 de-identification broker (identity stays home)")
    print("─" * 84)

    spoken = transcribe(b"\x00" * 1024, transcript=(
        "Hey there, I'm Solomon Joseph (solomon@acme.com). Charge card "
        "4242 4242 4242 4242 and save the note to /Users/sj1136/secret.txt — Cheers, Sol"
    ))
    names = ["Solomon Joseph", "Sol"]
    print("\n[voice→text, local] the cloud never receives audio:")
    print(f'    "{spoken}"')

    res = broker.egress("assistant", spoken, host="api.anthropic.com", names=names)
    print("\n[mask + normalize] real (stays home) vs sent (leaves the device):")
    print(f"    REAL: {res.real_text}")
    print(f"    SENT: {res.sent_text}")
    print(f"    leaked real entities in SENT: {res.leaked}")
    print(f"\n[egress → api.anthropic.com] decision={res.decision}; receipt={res.receipt_id[:12]}…")
    print(f"    cloud saw only surrogates; reply re-identified locally:")
    print(f"    \"{res.cloud_reply}\"")

    bad = broker.egress("assistant", spoken, host="paste.attacker.net", names=names)
    print(f"\n[egress → paste.attacker.net] decision={bad.decision} (default-deny); sent={bad.cloud_reply}")

    with open(os.path.join(LEDGER_DIR, "receipts.jsonl"), encoding="utf-8") as f:
        blob = f.read()
    survived = [s for s in SECRETS if s in blob]
    print(f"\n[audit] real identity strings present in the on-disk receipt log: {survived}  (none)")

    print("\n[sensitive send] requires the golden-share over the exact masked payload:")
    sk = TrustKernel(
        Ledger(LEDGER_DIR + "-s"),
        Verifier(Policy(egress_allowlist={"api.anthropic.com"}, reserved_actions={"net.egress"})),
        golden_share=gs,
    )
    sbroker = TrustBroker(sk)
    p = sbroker.egress("assistant", spoken, host="api.anthropic.com", names=names)
    print(f"    no signature → {p.decision}")
    nonce = "egress-1"  # single-use: one approval authorises exactly one send
    intent = action_intent(
        "assistant", "net.egress", {"sent_text": p.sent_text}, {"host": "api.anthropic.com"}, nonce=nonce
    )
    ok = sbroker.egress(
        "assistant", spoken, host="api.anthropic.com", names=names, golden_share=gs.approve(intent), nonce=nonce
    )
    print(f"    owner signed → {'allow' if ok.allowed else ok.decision}")
    shutil.rmtree(LEDGER_DIR + "-s", ignore_errors=True)

    print("\n" + "─" * 84)
    print(f"    whole-log verify: ok={led.verify_log()['ok']}  receipts={len(led)}")
    print("    Only masked surrogates ever leave; the surrogate map and real text stay on device.")
    print("─" * 84)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
