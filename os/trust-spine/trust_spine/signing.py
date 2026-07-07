"""Signing backends for Trust Spine receipts.

A `Signer` produces detached signatures over the canonical bytes of a receipt.
We ship two backends:

  * Ed25519  — always available via `cryptography`. The v0 default fallback.
  * ML-DSA-65 (FIPS 204) — used automatically when `liboqs` (`oqs`) is installed.

The receipt records its `algorithm` and `public_key`, so verification is
unambiguous regardless of which backend signed it. This is the "PQC is
pluggable, not blocking" rule from the plan made concrete.
"""

from __future__ import annotations

import abc
from typing import Dict

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)

# Optional post-quantum backend. Imported lazily so the package works with or
# without liboqs present. When absent we fall back to Ed25519 (still tamper-
# evident; just not harvest-now-decrypt-later safe).
try:  # pragma: no cover - depends on optional native lib
    import oqs  # type: ignore

    _HAS_OQS = True
except Exception:  # pragma: no cover
    oqs = None  # type: ignore
    _HAS_OQS = False

ED25519 = "ed25519"
ML_DSA = "ML-DSA-65"


class Signer(abc.ABC):
    """A detached-signature producer with a stable public key."""

    algorithm: str

    @abc.abstractmethod
    def sign(self, data: bytes) -> bytes:
        ...

    @abc.abstractmethod
    def public_key_bytes(self) -> bytes:
        ...


class Ed25519Signer(Signer):
    algorithm = ED25519

    def __init__(self, private_key: "Ed25519PrivateKey | None" = None) -> None:
        self._sk = private_key or Ed25519PrivateKey.generate()

    @classmethod
    def from_seed(cls, seed: bytes) -> "Ed25519Signer":
        if len(seed) != 32:
            raise ValueError("ed25519 seed must be exactly 32 bytes")
        return cls(Ed25519PrivateKey.from_private_bytes(seed))

    def seed(self) -> bytes:
        return self._sk.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())

    def sign(self, data: bytes) -> bytes:
        return self._sk.sign(data)

    def public_key_bytes(self) -> bytes:
        return self._sk.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)


class MLDSASigner(Signer):
    """ML-DSA-65 (FIPS 204) signer, available only when liboqs is installed."""

    algorithm = ML_DSA

    def __init__(self) -> None:
        if not _HAS_OQS:
            raise RuntimeError("liboqs (the 'oqs' module) is not installed")
        self._sig = oqs.Signature(ML_DSA)
        self._pub = self._sig.generate_keypair()

    def sign(self, data: bytes) -> bytes:
        return self._sig.sign(data)

    def public_key_bytes(self) -> bytes:
        return self._pub


def verify_signature(
    algorithm: str, public_key: bytes, data: bytes, signature: bytes
) -> bool:
    """Verify a detached signature for the named algorithm. Never raises on a
    bad signature — returns False. Raises only on an unknown algorithm or a
    genuinely unavailable verifier."""
    if algorithm == ED25519:
        try:
            Ed25519PublicKey.from_public_bytes(public_key).verify(signature, data)
            return True
        except InvalidSignature:
            return False
        except Exception:
            return False
    if algorithm == ML_DSA:
        if not _HAS_OQS:
            raise RuntimeError(
                "cannot verify an ML-DSA receipt: liboqs ('oqs') is not installed"
            )
        try:  # pragma: no cover - depends on optional native lib
            with oqs.Signature(ML_DSA) as verifier:
                return bool(verifier.verify(data, signature, public_key))
        except Exception:  # pragma: no cover
            return False
    raise ValueError(f"unknown signature algorithm: {algorithm!r}")


def default_signer(prefer_pqc: bool = True) -> Signer:
    """Prefer ML-DSA when available; otherwise Ed25519."""
    if prefer_pqc and _HAS_OQS:
        return MLDSASigner()
    return Ed25519Signer()


def pqc_available() -> bool:
    return _HAS_OQS


class UnknownActorError(Exception):
    """Raised by a strict KeyRing asked to sign for an unregistered actor."""


class KeyRing:
    """Per-actor signer cache: each agent signs its receipts with a stable key,
    so receipts from the same actor verify against a consistent public key.

    Two modes:

      * lenient (default) — mints a fresh key for any actor on first use. Fine
        for in-process, fully-trusted callers (demos, the recursive org).
      * ``strict=True`` — only actors registered with :meth:`register` may sign;
        an unknown actor raises :class:`UnknownActorError`. Use this at any
        boundary where the actor name is attacker-influenceable (e.g. the
        side-car socket), so an attacker cannot mint an 'owner' key on the fly
        and forge a perfectly-verifying receipt attributing an action to a
        victim. (Red-team finding: lenient minting makes attribution forgeable.)

    v0 keeps keys in memory. M4 seals them in the Vault / hardware (TPM2 /
    secure element) so the keys are sovereign and never leave the device.
    """

    def __init__(self, prefer_pqc: bool = True, strict: bool = False) -> None:
        self._prefer = prefer_pqc
        self.strict = strict
        self._keys: Dict[str, Signer] = {}

    def register(self, actor: str, signer: "Signer | None" = None) -> Signer:
        """Pin an actor to a signing key (its own, or a freshly-minted one)."""
        self._keys[actor] = signer or default_signer(self._prefer)
        return self._keys[actor]

    def knows(self, actor: str) -> bool:
        return actor in self._keys

    def signer_for(self, actor: str) -> Signer:
        if actor not in self._keys:
            if self.strict:
                raise UnknownActorError(actor)
            self._keys[actor] = default_signer(self._prefer)
        return self._keys[actor]

    def public_key_hex(self, actor: str) -> str:
        return self.signer_for(actor).public_key_bytes().hex()

    def public_keys(self) -> Dict[str, str]:
        """actor → public-key hex for every actor with a signing key. Pass this
        to ``Ledger.verify_log(known_keys=…)`` so offline verification can bind a
        receipt's signer key to its claimed actor and reject key-substitution
        forgeries. (Red-team finding F4.)"""
        return {actor: s.public_key_bytes().hex() for actor, s in self._keys.items()}
