"""Regression tests for the red-team hardening pass (2026-06-16).

Each test pins a specific confirmed finding so a regression re-opens it loudly.
"""

import json
import os

import pytest

from trust_spine.capabilities import (
    NETWORK_EGRESS,
    SECRET_ACCESS,
    UNTRUSTED_INPUT,
    CapabilityBroker,
    required_capabilities,
)
from trust_spine.golden_share import GoldenShare, action_intent
from trust_spine.kernel import ActionRequest, TrustKernel
from trust_spine.ledger import Ledger, LedgerCorruptionError
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


# =============================================================================
# Second red-team pass (2026-06-16) — findings F1, F4, F5
# =============================================================================

# --- F1: golden-share nonce replay across a kernel restart --------------------

def test_golden_share_nonce_is_durable_across_restart(tmp_path):
    """F1: a single-use approval must not be replayable after a restart. The
    earlier fix burned the nonce only IN MEMORY, so a new kernel over the same
    ledger re-opened the approval. The redeemed nonce is now persisted durably."""
    path = str(tmp_path / "led")
    gs = GoldenShare()  # persistent key (sealed in hardware in production)
    spent = []

    def build_kernel():
        kr = KeyRing(strict=True)
        kr.register("owner")
        k = TrustKernel(Ledger(path), Verifier(Policy()), keyring=kr, golden_share=gs)
        k.register_effect("spend", lambda s: spent.append(s.inputs["amount"]))
        return k

    inputs = {"amount": 49, "vendor": "X"}
    nonce = "nonce-1"
    sig = gs.approve(action_intent("owner", "spend", inputs, {}, nonce=nonce))

    r1 = build_kernel().submit(ActionRequest(
        actor="owner", action="spend", inputs=inputs, risk_tier=3,
        golden_share=sig, nonce=nonce))
    assert r1.allowed is True

    # "restart": a fresh kernel over the SAME ledger must reject the replay.
    r2 = build_kernel().submit(ActionRequest(
        actor="owner", action="spend", inputs=inputs, risk_tier=3,
        golden_share=sig, nonce=nonce))
    assert r2.allowed is False and "replay" in r2.reason
    assert spent == [49]  # the approved effect executed exactly once
    assert os.path.exists(os.path.join(path, "redeemed_nonces.txt"))


# --- F4: receipt verification binds actor -> registered key -------------------

def test_verify_log_binds_actor_to_registered_key(tmp_path):
    """F4: a forged receipt attributing an action to a victim actor but signed
    with the attacker's own key must fail verification when a known-keys registry
    is supplied (a valid signature alone proves only that *some* key signed)."""
    path = str(tmp_path / "led")
    kr = KeyRing(strict=True)
    kr.register("owner")

    led = Ledger(path)
    led.append(Ed25519Signer(), actor="owner", action="spend", risk_tier=3,
               decision="allow", inputs={"amount": 1_000_000},
               outputs={"charged": 1_000_000})  # attacker's own key, "owner" actor

    audit = Ledger(path)
    assert audit.verify_log()["ok"] is True  # back-compat: no registry → no binding
    res = audit.verify_log(known_keys=kr.public_keys())
    assert res["ok"] is False
    assert any("forged attribution" in p.get("error", "") for p in res["problems"])

    # A receipt signed with the registered owner key passes the binding.
    good_path = str(tmp_path / "led2")
    Ledger(good_path).append(kr.signer_for("owner"), actor="owner", action="fs.read",
                             risk_tier=1, decision="allow", inputs={}, outputs={})
    assert Ledger(good_path).verify_log(known_keys=kr.public_keys())["ok"] is True


# --- F5: torn trailing write recovered; interior corruption raises ------------

def test_torn_trailing_line_is_recovered(tmp_path):
    """F5: a torn trailing write (crash mid-append, no terminating newline) is
    recovered like a WAL partial record — the ledger still loads."""
    path = str(tmp_path / "led")
    led = Ledger(path)
    s = Ed25519Signer()
    for i in range(2):
        led.append(s, actor="a", action="fs.read", risk_tier=1, decision="allow",
                   inputs={"i": i}, outputs={})
    with open(os.path.join(path, "receipts.jsonl"), "a", encoding="utf-8") as f:
        f.write('{"version": "trust-spine/0.1", "receipt_id": "torn')  # partial, no \n

    reloaded = Ledger(path)  # must NOT raise
    assert reloaded.recovered_torn_tail is True
    assert len(reloaded) == 2
    assert reloaded.verify_log()["ok"] is True  # recovered to the last consistent state


def test_interior_corruption_raises_loudly(tmp_path):
    """F5: a complete (newline-terminated) corrupt line that is NOT the last line
    is a tamper signal, not a torn write, and must raise rather than be skipped."""
    path = str(tmp_path / "led")
    led = Ledger(path)
    led.append(Ed25519Signer(), actor="a", action="fs.read", risk_tier=1,
               decision="allow", inputs={}, outputs={})
    rf = os.path.join(path, "receipts.jsonl")
    with open(rf, encoding="utf-8") as f:
        lines = f.readlines()
    lines.insert(0, "NOT-VALID-JSON\n")  # interior, newline-terminated
    with open(rf, "w", encoding="utf-8") as f:
        f.writelines(lines)
    with pytest.raises(LedgerCorruptionError):
        Ledger(path)
