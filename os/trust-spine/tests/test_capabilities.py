import pytest

from trust_spine.capabilities import (
    FS_READ,
    NETWORK_EGRESS,
    SECRET_ACCESS,
    UNTRUSTED_INPUT,
    CapabilityBroker,
    LethalTrifectaError,
    is_trifecta_complete,
    required_capability,
)
from trust_spine.kernel import ActionRequest, TrustKernel
from trust_spine.ledger import Ledger
from trust_spine.policy import Policy
from trust_spine.verifier import VETO, Verifier


def test_required_capability_mapping():
    assert required_capability("net.egress") == NETWORK_EGRESS
    assert required_capability("mail.read") == UNTRUSTED_INPUT
    assert required_capability("vault.use") == SECRET_ACCESS
    assert required_capability("plan.decompose") is None


def test_two_legs_allowed():
    b = CapabilityBroker()
    caps = b.grant("comms-leaf", {UNTRUSTED_INPUT, FS_READ})
    assert caps == {UNTRUSTED_INPUT, FS_READ}


def test_three_legs_refused_without_golden_share():
    b = CapabilityBroker()
    with pytest.raises(LethalTrifectaError):
        b.grant("omni", {UNTRUSTED_INPUT, SECRET_ACCESS, NETWORK_EGRESS})


def test_three_legs_allowed_with_golden_share():
    b = CapabilityBroker()
    caps = b.grant(
        "omni", {UNTRUSTED_INPUT, SECRET_ACCESS, NETWORK_EGRESS}, human_approved=True
    )
    assert is_trifecta_complete(caps)


def test_escalating_to_third_leg_via_add_is_refused():
    b = CapabilityBroker()
    b.grant("leaf", {UNTRUSTED_INPUT, SECRET_ACCESS})
    with pytest.raises(LethalTrifectaError):
        b.add("leaf", NETWORK_EGRESS)
    # the grant is unchanged after the refusal
    assert not b.has("leaf", NETWORK_EGRESS)


def test_verifier_vetoes_when_capability_missing():
    b = CapabilityBroker()
    b.grant("comms-leaf", {UNTRUSTED_INPUT, FS_READ})
    v = Verifier(Policy(egress_allowlist={"api.x"}), capability_broker=b)
    d = v.decide(actor="comms-leaf", action="net.egress", context={"host": "api.x"})
    assert d.outcome == VETO
    assert "least-privilege" in d.reason


def test_verifier_allows_when_capability_present():
    b = CapabilityBroker()
    b.grant("net-leaf", {NETWORK_EGRESS})
    v = Verifier(Policy(egress_allowlist={"api.x"}), capability_broker=b)
    d = v.decide(actor="net-leaf", action="net.egress", context={"host": "api.x"})
    assert d.outcome == "allow"


def test_prompt_injection_email_scenario_is_blocked(tmp_path):
    """Stress-test Scenario A: an injected email tells the parser to read AWS
    creds and POST them out. The parser holds only {untrusted_input, fs_read},
    so both the secret read and the egress are vetoed structurally."""
    broker = CapabilityBroker()
    broker.grant("comms-leaf", {UNTRUSTED_INPUT, FS_READ})  # NOT secret, NOT egress

    led = Ledger(str(tmp_path / "led"))
    verifier = Verifier(Policy(egress_allowlist=set()), capability_broker=broker)
    kernel = TrustKernel(led, verifier)

    # 1. Read the malicious email — allowed (it has untrusted_input).
    r1 = kernel.submit(ActionRequest(actor="comms-leaf", action="mail.read"))
    assert r1.allowed is True

    # 2. Injection makes it try to read secrets — vetoed (no secret_access).
    r2 = kernel.submit(
        ActionRequest(actor="comms-leaf", action="secret.read", inputs={"path": "~/.aws/credentials"})
    )
    assert r2.allowed is False and "least-privilege" in r2.reason

    # 3. Injection makes it try to exfiltrate — vetoed (no network_egress).
    r3 = kernel.submit(
        ActionRequest(actor="comms-leaf", action="net.egress", context={"host": "attacker.com"})
    )
    assert r3.allowed is False and "least-privilege" in r3.reason

    # Every step, including the two refusals, is a verifiable receipt.
    assert led.verify_log()["ok"] is True
