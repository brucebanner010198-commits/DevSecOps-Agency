"""The golden-share — the sovereign master key.

Reserved actions (spend, identity export, granting new powers, irreversible ops)
are never delegated. The verifier returns them as "pending"; they execute only
when the Owner signs the exact action intent with the golden-share key. This is
the human-stays-sovereign guarantee: the AI can prepare a reserved action, but
only the human's signature lets it run.

v0 holds the key in memory. M4+ seals it in hardware (TPM2 / secure element);
the golden-share is the single key that signs every reserved action.
"""

from __future__ import annotations

import json
from typing import Any, Optional

from .signing import Signer, default_signer, verify_signature


def action_intent(
    actor: str, action: str, inputs: Any, context: Any, *, nonce: Optional[str] = None
) -> bytes:
    """Canonical bytes the Owner signs to approve a specific reserved action.

    Binding actor+action+inputs+context means a signature for 'spend $49 to
    vendor X' cannot be replayed to authorise 'spend $4900 to vendor Y'.

    Binding a single-use ``nonce`` additionally stops *same-action* replay: one
    approval authorises exactly one execution. The kernel issues the nonce, the
    Owner signs over it, and the kernel burns it on first use (see TrustKernel).
    When ``nonce`` is None the field is omitted, so older 4-argument intents
    remain byte-identical (back-compat for non-reserved uses)."""
    payload = {"actor": actor, "action": action, "inputs": inputs, "context": context}
    if nonce is not None:
        payload["nonce"] = nonce
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


class GoldenShare:
    def __init__(self, signer: Optional[Signer] = None) -> None:
        self._signer = signer or default_signer()
        self.algorithm = self._signer.algorithm
        self.public_key = self._signer.public_key_bytes()

    def approve(self, intent: bytes) -> bytes:
        """Owner signs an action intent (the human-in-the-loop step)."""
        return self._signer.sign(intent)

    def verify(self, intent: bytes, signature: bytes) -> bool:
        return verify_signature(self.algorithm, self.public_key, intent, signature)
