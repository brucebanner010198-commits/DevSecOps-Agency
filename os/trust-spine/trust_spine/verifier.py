"""The independent verifier-with-veto.

This is the pillar no rival ships for a *personal* user: a checker that is
structurally separate from the agent it checks, decides **before** the action
runs, and can **block** it. It is risk-tiered so trivial, reversible actions
don't pay veto latency:

    Tier 1  log-only        reversible local actions       → allow, receipt async
    Tier 2  async-verified  non-critical mutations         → allow, flagged
    Tier 3  veto-gated      egress / spend / vault / irreversible → checked, may veto

Reserved actions (the Owner's golden-share set) return "pending" — held until a
human signature (wired in M4), never silently allowed.

Maps to: OWASP Top-10 for Agentic Apps 2026 (ASI mitigations), Meta "Agents Rule
of Two", and the design law in research .../42 and .../47 (the authority that
checks must be independent of, and non-overridable by, the party it checks).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from .capabilities import CapabilityBroker, required_capabilities
from .policy import Policy

ALLOW = "allow"
VETO = "veto"
PENDING = "pending"


@dataclass
class Decision:
    outcome: str  # allow | veto | pending
    tier: int  # effective risk tier (1..3)
    reason: str


class Verifier:
    def __init__(
        self, policy: Policy, capability_broker: Optional[CapabilityBroker] = None
    ) -> None:
        self.policy = policy
        self.caps = capability_broker
        # Explicit, inspectable: per-agent least-privilege is enforced only when
        # a capability broker is wired. Without one the coarse policy layer
        # (tiers, egress allowlist, reserved→pending) still applies, but the
        # trifecta/least-privilege defence-in-depth is OFF — deployments that
        # rely on it (e.g. the watchable desktop) must pass a broker.
        self.enforces_capabilities = capability_broker is not None

    def effective_tier(self, action: str, declared_tier: int) -> int:
        """Escalate to Tier 3 for veto-gated/reserved actions; otherwise clamp
        the agent-declared tier into 1..3. An agent cannot down-declare an
        egress to Tier 1 to dodge the gate."""
        if self.policy.is_veto_gated(action) or self.policy.is_reserved(action):
            return 3
        return max(1, min(3, int(declared_tier)))

    def decide(
        self,
        *,
        actor: str,
        action: str,
        risk_tier: int = 1,
        context: Optional[Dict[str, Any]] = None,
    ) -> Decision:
        context = context or {}
        tier = self.effective_tier(action, risk_tier)

        # Default-deny on unrecognised actions (when the policy opts in): an
        # agent must not be able to smuggle a consequential effect under an
        # action name the policy doesn't classify, at a self-declared low tier.
        if self.policy.deny_unknown_actions and not self.policy.is_known_action(action):
            return Decision(
                VETO, tier, f"unknown action '{action}' refused (default-deny policy)"
            )

        # Least-privilege gate (hard, checked first): the acting agent must hold
        # EVERY capability the action requires. An agent that ingests untrusted
        # input but was never granted egress/secret-access is structurally
        # unable to exfiltrate, even when a prompt injection tells it to. Actions
        # carrying more than one leg (e.g. web.fetch = untrusted_input + egress)
        # must hold all of them — that is what stops the trifecta being completed
        # through a single dual-use action.
        if self.caps is not None:
            for required in required_capabilities(action):
                if not self.caps.has(actor, required):
                    return Decision(
                        VETO,
                        tier,
                        f"least-privilege: '{actor}' lacks capability "
                        f"'{required}' required for '{action}'",
                    )

        # Tiers 1 & 2 — allowed; Tier 2 is flagged for asynchronous verification.
        if tier < 3:
            note = "tier-1 log-only" if tier == 1 else "tier-2 async-verified"
            return Decision(ALLOW, tier, f"{note}: allowed, receipt logged")

        # Tier 3 — veto-gated.
        if self.policy.is_reserved(action):
            return Decision(
                PENDING, tier, f"reserved action '{action}' requires the golden-share"
            )

        # Every network-reaching action (net.egress, web.fetch, …) clears the
        # same egress allowlist — the gate keys on the *property* "reaches the
        # network", not on one literal action name.
        if self.policy.is_network_action(action):
            host = str(context.get("host", ""))
            if self.policy.is_egress_allowed(host):
                return Decision(ALLOW, tier, f"egress to allowlisted host '{host}'")
            return Decision(
                VETO, tier, f"egress to non-allowlisted host '{host or '?'}' blocked"
            )

        if action == "vault.use":
            # The verifier authorises the *attempt* at Tier 3 (already gated by
            # the secret_access capability above). The Vault performs the real
            # origin-binding + visibility audit downstream in the kernel — and
            # the kernel fails closed if no Vault is configured.
            return Decision(
                ALLOW, tier, "vault use authorised at tier 3 (Vault enforces origin/visibility)"
            )

        # Any other Tier-3 action: allowed but recorded at Tier 3.
        return Decision(ALLOW, tier, f"tier-3 action '{action}' allowed by policy")
