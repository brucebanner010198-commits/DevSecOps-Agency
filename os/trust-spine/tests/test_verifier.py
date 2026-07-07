from trust_spine.policy import Policy
from trust_spine.verifier import ALLOW, PENDING, VETO, Verifier


def _verifier(allow_hosts=()):
    return Verifier(Policy(egress_allowlist=set(allow_hosts)))


def test_tier1_local_action_allowed():
    d = _verifier().decide(actor="leaf", action="fs.write", risk_tier=1)
    assert d.outcome == ALLOW and d.tier == 1


def test_egress_is_forced_to_tier3_even_if_declared_low():
    d = _verifier(allow_hosts={"api.openai.com"}).decide(
        actor="leaf", action="net.egress", risk_tier=1, context={"host": "evil.example"}
    )
    # declared tier 1, but egress is veto-gated → tier 3, and host not allowed → veto
    assert d.tier == 3
    assert d.outcome == VETO


def test_egress_to_allowlisted_host_allowed():
    d = _verifier(allow_hosts={"api.anthropic.com"}).decide(
        actor="leaf", action="net.egress", risk_tier=3, context={"host": "api.anthropic.com"}
    )
    assert d.outcome == ALLOW and d.tier == 3


def test_egress_to_unlisted_host_vetoed():
    d = _verifier(allow_hosts={"api.anthropic.com"}).decide(
        actor="leaf", action="net.egress", risk_tier=3, context={"host": "paste.attacker.net"}
    )
    assert d.outcome == VETO


def test_reserved_action_is_pending():
    d = _verifier().decide(actor="ceo", action="spend", risk_tier=3, context={"amount": 50})
    assert d.outcome == PENDING and d.tier == 3


def test_vault_use_authorised_at_tier3_by_verifier():
    # The verifier authorises the attempt at Tier 3; the Vault does the real
    # origin/visibility check downstream (see test_vault.py).
    d = _verifier().decide(actor="leaf", action="vault.use", risk_tier=1)
    assert d.outcome == ALLOW and d.tier == 3
