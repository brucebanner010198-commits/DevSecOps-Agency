"""Signed, replayable receipts.

Every consequential agent action produces a `Receipt`: who did what, at what
risk tier, with what decision, hashes of the inputs/outputs, a link to the
previous receipt (a hash chain), and a signature over all of that.

The signature covers the *canonical* JSON of every field except the signature
itself, so any later edit to any field invalidates it. The same canonical bytes
are SHA-256'd to give `receipt_hash()` — the leaf that goes into the Merkle log.

This mirrors the pattern now shipping elsewhere (Fetch.ai AEVS; "Notarized
Agents" Ed25519 receipts) but kept *local and sovereign* — no chain, no vendor.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Optional

from .signing import Signer, verify_signature

RECEIPT_VERSION = "trust-spine/0.1"


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _canonical(obj: Any) -> bytes:
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def hash_payload(obj: Any, key: Optional[bytes] = None) -> str:
    """Stable content digest for receipt inputs/outputs.

    With ``key`` it is a keyed HMAC-SHA256; without, a plain SHA-256. The keyed
    form matters for confidentiality: a bare SHA-256 of a *low-entropy* value (a
    phone number, a card, a short email) is brute-forceable by anyone who reads
    the on-disk log, so it is not a safe way to "store only a hash" of identity.
    A device-local HMAC key (never written into the ledger) closes that oracle.
    Verification never recomputes this digest from raw inputs — the signature
    covers the stored digest — so keying is fully compatible with offline
    signature/Merkle verification. (Red-team finding: unsalted-hash oracle.)"""
    canonical = _canonical(obj)
    if key is not None:
        return hmac.new(key, canonical, hashlib.sha256).hexdigest()
    return _sha256_hex(canonical)


@dataclass
class Receipt:
    version: str
    receipt_id: str
    timestamp: str
    actor: str  # the agent / role that performed the action
    action: str  # tool or action name
    risk_tier: int  # 1 = log-only, 2 = async-verified, 3 = veto-gated
    decision: str  # "allow" | "veto" | "pending"
    inputs_hash: str
    outputs_hash: str
    prev_receipt_hash: str  # hash chain link (GENESIS for the first)
    algorithm: str
    public_key: str  # hex
    signature: str = ""  # hex, filled in by create()

    # -- canonical bytes & hashes -------------------------------------------
    def signing_payload(self) -> bytes:
        d = asdict(self)
        d.pop("signature", None)
        return _canonical(d)

    def receipt_hash(self) -> str:
        """SHA-256 of the signing payload — the Merkle leaf and chain link."""
        return _sha256_hex(self.signing_payload())

    # -- construction --------------------------------------------------------
    @classmethod
    def create(
        cls,
        signer: Signer,
        *,
        actor: str,
        action: str,
        risk_tier: int,
        decision: str,
        inputs: Any,
        outputs: Any,
        prev_receipt_hash: str,
        receipt_id: "str | None" = None,
        timestamp: "str | None" = None,
        hash_key: Optional[bytes] = None,
    ) -> "Receipt":
        r = cls(
            version=RECEIPT_VERSION,
            receipt_id=receipt_id or uuid.uuid4().hex,
            timestamp=timestamp or _now_iso(),
            actor=actor,
            action=action,
            risk_tier=int(risk_tier),
            decision=decision,
            inputs_hash=hash_payload(inputs, hash_key),
            outputs_hash=hash_payload(outputs, hash_key),
            prev_receipt_hash=prev_receipt_hash,
            algorithm=signer.algorithm,
            public_key=signer.public_key_bytes().hex(),
        )
        r.signature = signer.sign(r.signing_payload()).hex()
        return r

    # -- verification --------------------------------------------------------
    def verify_signature(self) -> bool:
        if not self.signature:
            return False
        try:
            return verify_signature(
                self.algorithm,
                bytes.fromhex(self.public_key),
                self.signing_payload(),
                bytes.fromhex(self.signature),
            )
        except ValueError:
            return False

    # -- (de)serialisation ---------------------------------------------------
    def to_json(self) -> str:
        return json.dumps(
            asdict(self), sort_keys=True, separators=(",", ":"), ensure_ascii=False
        )

    @classmethod
    def from_json(cls, s: str) -> "Receipt":
        return cls(**json.loads(s))
