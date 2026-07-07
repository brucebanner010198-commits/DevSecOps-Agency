"""Per-agent least-privilege and lethal-trifecta separation.

Simon Willison's "lethal trifecta": an agent becomes dangerous when it can
simultaneously (1) read private/sensitive data, (2) ingest untrusted content,
and (3) communicate externally — that combination is what turns a prompt
injection into data exfiltration. Meta's "Agents Rule of Two" hardens it: an
unsupervised agent may hold at most TWO of the three; all three requires a human
(our golden-share).

We enforce this at two layers:

  * grant-time  — the broker REFUSES to mint a grant holding all three legs
                  (unless the Owner's golden-share approves it). Structural.
  * run-time    — the verifier vetoes any action whose required capability the
                  acting agent was never granted. Least-privilege.

So the email-parsing agent that ingests untrusted mail simply never holds
secret-access or egress; when a prompt injection makes it try, the action is
vetoed for lack of capability — the attack is blocked by construction, not by
detection.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, FrozenSet, Iterable, Optional, Set

# The three legs of the lethal trifecta.
UNTRUSTED_INPUT = "untrusted_input"
SECRET_ACCESS = "secret_access"
NETWORK_EGRESS = "network_egress"

# Other, non-trifecta capabilities.
FS_READ = "fs_read"
FS_WRITE = "fs_write"
SPEND = "spend"

TRIFECTA: Set[str] = {UNTRUSTED_INPUT, SECRET_ACCESS, NETWORK_EGRESS}

# Which capabilities each action requires (a *set* — an action can be more than
# one trifecta leg at once). Actions not listed require none.
#
# `web.fetch` is the load-bearing fix from the red-team: an outbound fetch both
# ingests attacker-controllable content AND is a network-egress channel (the URL
# itself carries data out). Counting it as untrusted_input *only* let an agent
# holding {untrusted_input, secret_access} (two legs, Rule-of-Two-legal)
# exfiltrate a secret via the fetch URL without ever holding network_egress. So
# it carries BOTH legs and is routed through the egress allowlist like net.egress.
ACTION_CAPS: Dict[str, FrozenSet[str]] = {
    "net.egress": frozenset({NETWORK_EGRESS}),
    "web.fetch": frozenset({UNTRUSTED_INPUT, NETWORK_EGRESS}),
    "mail.read": frozenset({UNTRUSTED_INPUT}),
    "comms.read": frozenset({UNTRUSTED_INPUT}),  # message bodies are attacker-controllable
    "comms.send": frozenset({NETWORK_EGRESS}),  # sending leaves the device → egress leg
    "vault.use": frozenset({SECRET_ACCESS}),
    "secret.read": frozenset({SECRET_ACCESS}),
    "fs.read": frozenset({FS_READ}),
    "fs.write": frozenset({FS_WRITE}),
    "spend": frozenset({SPEND}),
}


def required_capabilities(action: str) -> FrozenSet[str]:
    """All capabilities an action requires (empty if unmapped)."""
    return ACTION_CAPS.get(action, frozenset())


def required_capability(action: str) -> Optional[str]:
    """Back-compat single-capability lookup: the sole required capability, or
    None if the action is unmapped or requires more than one (use
    :func:`required_capabilities` for the multi-leg actions)."""
    caps = ACTION_CAPS.get(action)
    if not caps or len(caps) != 1:
        return None
    return next(iter(caps))


def is_trifecta_complete(caps: Iterable[str]) -> bool:
    return TRIFECTA.issubset(set(caps))


class LethalTrifectaError(Exception):
    """Raised when a grant would hold all three trifecta legs without approval."""


@dataclass
class CapabilityBroker:
    """Maps each agent to the capability set it was granted. Fail-closed: an
    agent with no grant holds nothing.

    Granting all three trifecta legs requires the Owner's approval. v0 accepts a
    trusted-setup ``human_approved`` boolean (the broker is only ever populated
    by trusted bootstrap code, never by an agent); when a :class:`GoldenShare`
    verifier is wired via :meth:`bind_golden_share`, a full-trifecta grant
    additionally requires a real signature over the grant intent (and emits a
    receipt if a ledger is bound). (Red-team: the bare boolean was a latent
    over-grant path; cryptographic binding closes it.)"""

    _grants: Dict[str, Set[str]] = field(default_factory=dict)
    _gs: object = None  # optional GoldenShare verifier
    _ledger: object = None  # optional Ledger for grant receipts

    def bind_golden_share(self, golden_share: object, ledger: object = None) -> None:
        self._gs = golden_share
        self._ledger = ledger

    def grant(
        self,
        actor: str,
        caps: Iterable[str],
        *,
        human_approved: bool = False,
        golden_share: Optional[bytes] = None,
    ) -> Set[str]:
        caps = set(caps)
        if is_trifecta_complete(caps):
            self._authorize_full_trifecta(actor, caps, human_approved, golden_share)
        self._grants[actor] = caps
        return caps

    def _authorize_full_trifecta(
        self, actor: str, caps: Set[str], human_approved: bool, golden_share: Optional[bytes]
    ) -> None:
        if self._gs is not None:
            # Crypto-bound mode: require a real signature over the grant intent.
            from .golden_share import action_intent  # local import avoids a cycle

            intent = action_intent(actor, "grant.capability", {"caps": sorted(caps)}, {})
            if golden_share is None or not self._gs.verify(intent, golden_share):
                raise LethalTrifectaError(
                    f"refusing to grant all three lethal-trifecta capabilities to "
                    f"'{actor}' without a valid golden-share signature: {sorted(caps)}"
                )
            if self._ledger is not None:  # auditable over-grant
                self._ledger.append(
                    self._ledger_signer(actor),
                    actor=actor,
                    action="grant.capability",
                    risk_tier=3,
                    decision="allow",
                    inputs={"caps": sorted(caps)},
                    outputs={"golden_gated": True},
                )
        elif not human_approved:
            raise LethalTrifectaError(
                f"refusing to grant all three lethal-trifecta capabilities to "
                f"'{actor}' without the golden-share (Meta 'Rule of Two'): {sorted(caps)}"
            )

    def _ledger_signer(self, actor: str):
        from .signing import KeyRing  # local import avoids a cycle

        if not hasattr(self, "_grant_keyring"):
            self._grant_keyring = KeyRing()
        return self._grant_keyring.signer_for("capability-broker")

    def add(
        self,
        actor: str,
        cap: str,
        *,
        human_approved: bool = False,
        golden_share: Optional[bytes] = None,
    ) -> Set[str]:
        caps = self.capabilities(actor) | {cap}
        return self.grant(
            actor, caps, human_approved=human_approved, golden_share=golden_share
        )

    def revoke(self, actor: str, cap: str) -> None:
        self._grants.get(actor, set()).discard(cap)

    def capabilities(self, actor: str) -> Set[str]:
        return set(self._grants.get(actor, set()))

    def has(self, actor: str, cap: str) -> bool:
        return cap in self._grants.get(actor, set())

    def holds_full_trifecta(self, actor: str) -> bool:
        return is_trifecta_complete(self.capabilities(actor))
