"""The Trust Kernel — the proxy every agent action passes through.

This is the integration point that turns the prompt-based recursive org
(`agents/`, `councils/`) and the existing `runtime-hooks/` tool-interception
into a *trust-instrumented* one:

    request → verifier decides → (golden-share may elevate a pending reserved
    action) → effect / vault runs ONLY on allow → signed receipt (always)

A vetoed or pending action never runs its side effect, but it still leaves a
signed receipt, so the refusal itself is auditable and replayable.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field, is_dataclass
from typing import Any, Callable, Dict, Optional

from .golden_share import GoldenShare, action_intent
from .ledger import Ledger
from .signing import KeyRing, UnknownActorError
from .vault import FieldDescriptor, UseResult, Vault
from .verifier import ALLOW, PENDING, VETO, Decision, Verifier


def _json_safe(value: Any) -> Any:
    """Coerce arbitrary inputs/context into JSON before hashing into a receipt,
    so a stray dataclass or callable never crashes receipt creation (and a
    secret/sink is never persisted in clear)."""

    def fallback(o: Any) -> Any:
        if is_dataclass(o) and not isinstance(o, type):
            return asdict(o)
        if callable(o):
            return "<callable>"
        return str(o)

    return json.loads(json.dumps(value, default=fallback))


@dataclass(frozen=True)
class SignedEffect:
    """The signed-only view handed to a registered effect handler for a
    golden-gated action. It carries exactly the fields the Owner's signature
    covers — never the agent's opaque callable — so a handler can act only on
    data the human approved. This is what makes the golden-share bind *what
    runs*, not merely a textual description of it."""

    actor: str
    action: str
    inputs: Any
    context: Dict[str, Any]
    nonce: Optional[str]


@dataclass
class ActionRequest:
    actor: str
    action: str
    inputs: Any = None
    risk_tier: int = 1
    context: Dict[str, Any] = field(default_factory=dict)
    # The real side effect. Run only if the verifier allows. Kept as a callable
    # so the kernel — not the agent — controls whether it ever executes.
    # NOTE: for a *golden-gated* (reserved) action this opaque callable is NOT
    # used; the effect is dispatched from the signed intent via a registered
    # handler (see TrustKernel.register_effect). Opaque effects run only for
    # non-reserved actions, where no human signature is meant to bind them.
    effect: Optional[Callable[[], Any]] = None
    # Reserved-action approval: the Owner's golden-share signature over the
    # action intent (which includes `nonce`). Present only when the human has
    # approved this exact, single-use action.
    golden_share: Optional[bytes] = None
    nonce: Optional[str] = None  # single-use token bound into the signed intent
    # vault.use fields — the secret name + target field. The secret itself lives
    # in the Vault, never in the request; the *destination* is resolved by the
    # Vault from a trusted registry keyed to the field's origin, so the agent
    # can neither supply nor capture where the plaintext goes (no sink here).
    secret_name: Optional[str] = None
    field: Optional[FieldDescriptor] = None


@dataclass
class ActionResult:
    allowed: bool
    decision: str  # allow | veto | pending
    reason: str
    tier: int
    receipt_id: str
    output: Any = None
    pending: bool = False


class TrustKernel:
    def __init__(
        self,
        ledger: Ledger,
        verifier: Verifier,
        keyring: Optional[KeyRing] = None,
        vault: Optional[Vault] = None,
        golden_share: Optional[GoldenShare] = None,
        effect_registry: Optional[Dict[str, Callable[["SignedEffect"], Any]]] = None,
    ) -> None:
        self.ledger = ledger
        self.verifier = verifier
        self.keyring = keyring or KeyRing()
        self.vault = vault
        self.golden_share = golden_share
        # Handlers for golden-gated effects, keyed by action. Registered by
        # *trusted* code (a broker, the side-car, OS bootstrap) — never supplied
        # by an agent per-request — so a reserved effect is reconstructed from
        # the signed intent, not from anything the agent controls out-of-band.
        self._effects: Dict[str, Callable[["SignedEffect"], Any]] = dict(effect_registry or {})
        # Single-use nonces already redeemed — one approval, one execution.
        self._used_nonces: set[str] = set()

    def register_effect(
        self, action: str, handler: Callable[["SignedEffect"], Any]
    ) -> None:
        self._effects[action] = handler

    def submit(self, req: ActionRequest) -> ActionResult:
        # Resolve the signing identity first. A strict KeyRing refuses an
        # unregistered actor, so an attacker who controls the actor string (e.g.
        # over the side-car socket) cannot mint a fresh key to forge a
        # perfectly-verifying receipt attributing the action to a victim.
        try:
            signer = self.keyring.signer_for(req.actor)
        except UnknownActorError:
            return ActionResult(
                allowed=False,
                decision="veto",
                reason=f"unregistered actor {req.actor!r} refused (strict keyring)",
                tier=req.risk_tier,
                receipt_id="",
                output=None,
                pending=False,
            )

        decision = self.verifier.decide(
            actor=req.actor,
            action=req.action,
            risk_tier=req.risk_tier,
            context=req.context,
        )

        # The golden-share (a human signature over this exact, single-use action
        # intent) can elevate a pending reserved action to allowed — and nothing
        # else can. The intent now binds a one-time `nonce`, and a reserved
        # action must have a registered effect handler, so the approval is both
        # single-use and bound to a concrete, signed effect.
        elevated = False
        if (
            decision.outcome == PENDING
            and req.golden_share is not None
            and self.golden_share is not None
        ):
            handler = self._effects.get(req.action)
            if req.nonce is None:
                decision = Decision(
                    PENDING,
                    decision.tier,
                    "reserved action requires a single-use nonce · " + decision.reason,
                )
            elif handler is None:
                decision = Decision(
                    VETO,
                    decision.tier,
                    f"reserved action {req.action!r} has no registered effect "
                    "handler; opaque effects are not permitted for golden-gated "
                    "actions · " + decision.reason,
                )
            elif req.nonce in self._used_nonces:
                decision = Decision(
                    VETO,
                    decision.tier,
                    "golden-share already used (replay) · " + decision.reason,
                )
            else:
                intent = action_intent(
                    req.actor, req.action, req.inputs, req.context, nonce=req.nonce
                )
                if self.golden_share.verify(intent, req.golden_share):
                    self._used_nonces.add(req.nonce)
                    decision = Decision(
                        ALLOW, decision.tier, "golden-share approved · " + decision.reason
                    )
                    elevated = True
                # invalid signature → stays PENDING (no nonce consumed)

        output: Any = None
        extra: Dict[str, Any] = {}
        if decision.outcome == ALLOW:
            if req.action == "vault.use":
                # Fail closed: a secret-use action must never fall through to a
                # generic effect. With no Vault there is no gate, so we veto.
                if self.vault is None:
                    decision = Decision(
                        VETO, decision.tier, "vault.use refused: no Vault configured (fail-closed)"
                    )
                else:
                    ures = self._use_vault(req)
                    if ures.ok:
                        output = {"result": ures.reason}
                        extra = {"masked": ures.masked, "secret_sha256": ures.secret_sha256}
                    else:
                        # The Vault's origin/visibility check is the final gate; a
                        # failure downgrades an otherwise-allowed action to a veto.
                        decision = Decision(VETO, decision.tier, "vault refused · " + ures.reason)
            elif elevated:
                # Golden-gated: dispatch from the SIGNED intent via the trusted
                # handler — never the agent's opaque callable. This is what
                # stops effect substitution (the Owner signed $49 → only the
                # $49 effect can run).
                handler = self._effects[req.action]  # checked present above
                output = handler(
                    SignedEffect(req.actor, req.action, req.inputs, req.context, req.nonce)
                )
                extra["golden_gated"] = {
                    "nonce_sha256": hashlib.sha256(req.nonce.encode("utf-8")).hexdigest()
                }
            elif req.effect is not None:
                output = req.effect()

        label = decision.outcome  # ALLOW/PENDING/VETO are already the labels
        receipt = self.ledger.append(
            signer,
            actor=req.actor,
            action=req.action,
            risk_tier=decision.tier,
            decision=label,
            inputs=_json_safe({"inputs": req.inputs, "context": req.context}),
            outputs=_json_safe({"output": output, "reason": decision.reason, **extra}),
        )

        return ActionResult(
            allowed=(decision.outcome == ALLOW),
            decision=label,
            reason=decision.reason,
            tier=decision.tier,
            receipt_id=receipt.receipt_id,
            output=output,
            pending=(decision.outcome == PENDING),
        )

    def _use_vault(self, req: ActionRequest) -> UseResult:
        if req.secret_name is None or req.field is None:
            return UseResult(False, "vault.use requires secret_name and field")
        # No agent-supplied sink: the Vault resolves the destination from its own
        # trusted, origin-keyed registry.
        return self.vault.use(req.secret_name, req.field)
