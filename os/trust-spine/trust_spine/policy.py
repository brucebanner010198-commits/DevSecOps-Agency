"""Trust policy — the rules the verifier enforces.

Deliberately small and declarative so it is auditable (MISSION forbids
"compliance theatre"). The policy is owned by the *verifier*, not the agent, so
the thing being checked cannot rewrite the thing checking it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Set

# Actions the Owner reserves to themselves — they require the golden-share
# (a human signature). The verifier returns "pending" so the action is held,
# never silently allowed.
DEFAULT_RESERVED: Set[str] = {
    "spend",
    "identity.export",
    "fs.delete.bulk",
    "grant.capability",
    "comms.send",  # sending a message externally on the Owner's behalf is reserved
}

# Actions always treated as Tier 3 (veto-gated) regardless of the tier the
# calling agent declared. Every network-reaching action is here so an agent
# cannot down-declare it to Tier 1 to dodge the egress allowlist (web.fetch was
# the red-team's missing one — an unguarded outbound channel).
DEFAULT_VETO_GATED: Set[str] = {"net.egress", "web.fetch", "vault.use", "spend"}

# Actions that reach the network and must clear the egress allowlist at Tier 3.
# (comms.send is also network-reaching but is *reserved* → it goes to the
# golden-share before any allowlist check.)
DEFAULT_NETWORK_ACTIONS: Set[str] = {"net.egress", "web.fetch"}


@dataclass
class Policy:
    egress_allowlist: Set[str] = field(default_factory=set)
    reserved_actions: Set[str] = field(default_factory=lambda: set(DEFAULT_RESERVED))
    veto_gated_actions: Set[str] = field(default_factory=lambda: set(DEFAULT_VETO_GATED))
    network_actions: Set[str] = field(default_factory=lambda: set(DEFAULT_NETWORK_ACTIONS))
    # Fail-closed posture for actions the policy does not recognise. Off by
    # default (the recursive-org demo uses free-form action names); hardened
    # deployments (desktop, broker) turn it on so an agent cannot smuggle a
    # consequential effect under an unenumerated action name at a self-declared
    # low tier. `known_actions` is the explicit allowlist consulted when on.
    deny_unknown_actions: bool = False
    known_actions: Set[str] = field(default_factory=set)

    def is_reserved(self, action: str) -> bool:
        return action in self.reserved_actions

    def is_veto_gated(self, action: str) -> bool:
        return action in self.veto_gated_actions

    def is_network_action(self, action: str) -> bool:
        return action in self.network_actions

    def is_egress_allowed(self, host: str) -> bool:
        return host in self.egress_allowlist

    def is_known_action(self, action: str) -> bool:
        """An action is 'known' if any layer classifies it: reserved, veto-gated,
        network, capability-mapped, or explicitly allowlisted in known_actions."""
        from .capabilities import ACTION_CAPS  # local import avoids a cycle

        return (
            action in self.reserved_actions
            or action in self.veto_gated_actions
            or action in self.network_actions
            or action in ACTION_CAPS
            or action in self.known_actions
        )
