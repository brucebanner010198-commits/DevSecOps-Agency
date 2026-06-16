"""Regression tests for the red-team hardening pass (2026-06-16).

Each test pins a specific confirmed finding so a regression re-opens it loudly.
"""

import json
import os

from trust_spine.capabilities import (
    NETWORK_EGRESS,
    SECRET_ACCESS,
    UNTRUSTED_INPUT,
    CapabilityBroker,
    required_capabilities,
)
from trust_spine.kernel import ActionRequest, TrustKernel
from trust_spine.ledger import Ledger
from trust_spine.policy import Policy
from trust_spine.receipts import hash_payload
from trust_spine.signing import Ed25519Signer, KeyRing, UnknownActorError
from trust_spine.verifier import ALLOW, VETO, Verifier


# --- web.fetch egress bypass (lethal-trifecta) --------------------------------

def test_web_fetch_requires_both_untrusted_input_and_egress():
    assert required_capabilities("web.fetch") == frozenset({UNTRUSTED_INPUT, NETWORK_EGRESS})


def test_web_fetch_with_two_legs_only_is_vetoed():
    """Agent holds {untrusted_input, secret_access} (Rule-of-Two legal) but NOT
    network_egress. web.fetch needs egress too → vetoed, so it can't be used to
    exfiltrate a secret via the URL."""
    b = CapabilityBroker()
    b.grant("reader", {UNTRUSTED_INPUT, SECRET_ACCESS})
    v = Verifier(Policy(egress_allowlist={"ok.host"}), capability_broker=b)
    d = v.decide(actor="reader", action="web.fetch", context={"host": "attacker.net"})
    assert d.outcome == VETO and "least-privilege" in d.reason


def test_web_fetch_is_egress_allowlisted_even_with_caps():
    """Even with egress capability, web.fetch clears the egress allowlist (it is
    a network-reaching action), so a non-allowlisted host is vetoed."""
    b = CapabilityBroker()
    b.grant("fetcher", {UNTRUSTED_INPUT, NETWORK_EGRESS})
    v = Verifier(Policy(egress_allowlist={"api.ok"}), capability_broker=b)
    assert v.decide(actor="fetcher", action="web.fetch", context={"host": "attacker.net"}).outcome == VETO
    assert v.decide(actor="fetcher", action="web.fetch", context={"host": "api.ok"}).outcome == ALLOW


# --- unknown-action fail-open -------------------------------------------------

def test_unknown_action_allowed_by_default_but_denied_when_policy_opts_in():
    lenient = Verifier(Policy())
    assert lenient.decide(actor="a", action="os.exec", risk_tier=1).outcome == ALLOW

    strict = Verifier(Policy(deny_unknown_actions=True))
    d = strict.decide(actor="a", action="os.exec", risk_tier=1)
    assert d.outcome == VETO and "unknown action" in d.reason
    # an explicitly-known action still passes under the strict policy
    assert strict.decide(actor="a", action="fs.write", risk_tier=1).outcome == ALLOW


# --- forgeable receipt attribution (strict keyring) ---------------------------

def test_strict_keyring_refuses_unknown_actor():
    kr = KeyRing(strict=True)
    kr.register("known")
    assert kr.knows("known") is True
    assert kr.knows("attacker") is False
    try:
        kr.signer_for("attacker")
        assert False, "expected UnknownActorError"
    except UnknownActorError:
        pass


def test_kernel_with_strict_keyring_refuses_unknown_actor(tmp_path):
    kr = KeyRing(strict=True)
    kr.register("known")
    kernel = TrustKernel(Ledger(str(tmp_path / "led")), Verifier(Policy()), keyring=kr)
    forged = kernel.submit(ActionRequest(actor="owner", action="fs.write"))
    assert forged.allowed is False and "unregistered actor" in forged.reason
    assert forged.receipt_id == ""  # no forged receipt was written
    assert kernel.submit(ActionRequest(actor="known", action="fs.write")).allowed is True


# --- ledger truncation / rollback ---------------------------------------------

def test_trailing_truncation_is_detected(tmp_path):
    path = str(tmp_path / "led")
    led = Ledger(path)
    s = Ed25519Signer()
    for i in range(4):
        led.append(s, actor="a", action="fs.write", risk_tier=1,
                    decision="allow", inputs={"i": i}, outputs={"ok": True})
    assert led.verify_log()["ok"] is True

    # Drop the last receipt line WITHOUT rewriting head.json (naive rollback).
    rf = os.path.join(path, "receipts.jsonl")
    with open(rf, encoding="utf-8") as f:
        lines = f.readlines()
    with open(rf, "w", encoding="utf-8") as f:
        f.writelines(lines[:-1])

    reloaded = Ledger(path)
    res = reloaded.verify_log()
    assert res["ok"] is False
    assert any("truncation" in p.get("error", "") for p in res["problems"])


def test_external_checkpoint_detects_rollback(tmp_path):
    path = str(tmp_path / "led")
    led = Ledger(path)
    s = Ed25519Signer()
    for i in range(3):
        led.append(s, actor="a", action="fs.write", risk_tier=1,
                   decision="allow", inputs={"i": i}, outputs={"ok": True})
    # An external (co-signed) checkpoint remembers there were 3 receipts.
    assert led.verify_log(expected_size=3)["ok"] is True
    # Even a fully-consistent shorter log is caught against the external anchor.
    assert led.verify_log(expected_size=5)["ok"] is False


# --- unsalted-hash oracle (keyed digests) -------------------------------------

def test_receipt_digests_are_keyed_on_disk(tmp_path):
    path = str(tmp_path / "led")
    led = Ledger(path)
    led.append(Ed25519Signer(), actor="a", action="contact.lookup", risk_tier=1,
               decision="allow", inputs={"inputs": "+15551234567", "context": {}},
               outputs={"ok": True})
    with open(os.path.join(path, "receipts.jsonl"), encoding="utf-8") as f:
        stored = json.loads(f.readline())
    # The on-disk digest must NOT be a bare SHA-256 of the input (which a phone
    # number's ~10^10 space would brute-force); the device-local HMAC key blocks it.
    plain = hash_payload({"inputs": "+15551234567", "context": {}})
    assert stored["inputs_hash"] != plain
    assert os.path.exists(os.path.join(path, "digest.key"))


def test_hash_payload_keyed_is_deterministic_and_differs():
    obj = {"a": 1, "b": [2, 3]}
    assert hash_payload(obj, key=b"k") == hash_payload(obj, key=b"k")
    assert hash_payload(obj, key=b"k") != hash_payload(obj)
    assert hash_payload(obj, key=b"k1") != hash_payload(obj, key=b"k2")
