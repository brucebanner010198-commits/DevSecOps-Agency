"""The append-only receipt ledger.

Receipts are appended as JSON lines to `receipts.jsonl`. The tamper-evidence
mechanisms protect the log to different degrees — stated honestly:

  1. Each receipt is signed → editing any field breaks its own signature.
  2. Receipts form a hash chain (prev_receipt_hash) and a Merkle tree → any
     insert, *interior* delete, or reorder breaks a chain link.
  3. `head.json` stores the current size + Merkle root. `verify_log` compares
     the live log against it, so a naive *trailing truncation/rollback* (which
     breaks no surviving chain link) is caught as a size/root mismatch.

What v0 still cannot catch on its own: an attacker who truncates the log AND
rewrites `head.json` to match. Detecting that needs an *external* anchor — a
co-signed/published checkpoint — which `verify_log(expected_size=, expected_root=)`
accepts. (Red-team finding: trailing-delete was previously undetected and the
old docstring overclaimed "any delete breaks a chain link".)

The `inputs_hash`/`outputs_hash` are keyed with a device-local HMAC key
(`digest.key`, never egressed) so low-entropy inputs can't be brute-forced off
a leaked log.
"""

from __future__ import annotations

import json
import os
import secrets
from typing import Any, Dict, List, Optional

from .merkle import inclusion_proof, merkle_tree_hash, verify_inclusion
from .receipts import Receipt
from .signing import Signer

GENESIS = "0" * 64  # prev_receipt_hash of the first receipt


class LedgerCorruptionError(Exception):
    """An interior receipt line failed to parse — a tamper signal, raised loudly.

    Distinguished from a *torn trailing write* (a crash mid-append leaving a
    partial final line), which is recovered automatically per append-only/WAL
    crash-safety practice (validate-and-discard the partial tail), not raised."""


class Ledger:
    def __init__(self, path: str) -> None:
        self.path = path
        self.receipts_file = os.path.join(path, "receipts.jsonl")
        self.head_file = os.path.join(path, "head.json")
        self.digest_key_file = os.path.join(path, "digest.key")
        # Durable single-use store for redeemed golden-share nonces. The kernel's
        # in-memory burn does not survive a restart, so a captured approval could
        # be replayed after a crash/reboot; persisting the redeemed nonce digests
        # here (reloaded on init) makes "one approval, one execution" hold across
        # restarts. (Red-team 2026-06-16, finding F1.)
        self.nonces_file = os.path.join(path, "redeemed_nonces.txt")
        os.makedirs(path, exist_ok=True)
        self._digest_key = self._load_or_make_digest_key()
        self._receipts: List[Receipt] = []
        self._leaves: List[bytes] = []  # raw leaf data = receipt_hash bytes
        self.recovered_torn_tail = False  # set True if a torn final line was dropped
        self._redeemed_nonces: set[str] = self._load_redeemed_nonces()
        self._load()

    def _load_or_make_digest_key(self) -> bytes:
        """Device-local HMAC key for input/output digests. Stays on device
        (owner-only perms, gitignored); never written into a receipt or egressed
        — so a leaked log can't be brute-forced to recover low-entropy PII."""
        if os.path.exists(self.digest_key_file):
            with open(self.digest_key_file, "rb") as f:
                return f.read()
        key = secrets.token_bytes(32)
        with open(self.digest_key_file, "wb") as f:
            f.write(key)
        try:
            os.chmod(self.digest_key_file, 0o600)
        except OSError:  # pragma: no cover - non-POSIX
            pass
        return key

    def _load(self) -> None:
        if not os.path.exists(self.receipts_file):
            return
        with open(self.receipts_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        last = len(lines) - 1
        for idx, raw in enumerate(lines):
            line = raw.strip()
            if not line:
                continue
            try:
                r = Receipt.from_json(line)
            except (ValueError, TypeError) as e:
                # A torn *trailing* write (no terminating newline) is a crash
                # mid-append: recover by discarding it, like a WAL replay drops a
                # partial final record. Any other parse failure is an interior
                # corruption / tamper and is raised loudly. (Finding F5.)
                if idx == last and not raw.endswith("\n"):
                    self.recovered_torn_tail = True
                    continue
                raise LedgerCorruptionError(
                    f"corrupt receipt at line {idx + 1}: {type(e).__name__}: {e}"
                )
            self._receipts.append(r)
            self._leaves.append(bytes.fromhex(r.receipt_hash()))

    # -- durable single-use nonce store (golden-share anti-replay) -----------
    def _load_redeemed_nonces(self) -> "set[str]":
        s: set[str] = set()
        if os.path.exists(self.nonces_file):
            with open(self.nonces_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        s.add(line)
        return s

    def is_nonce_redeemed(self, nonce_digest: str) -> bool:
        return nonce_digest in self._redeemed_nonces

    def redeem_nonce(self, nonce_digest: str) -> bool:
        """Durable check-and-set: record `nonce_digest` as spent and return True,
        or return False if it was already redeemed. Written (and fsync'd) BEFORE
        the effect runs, so a crash during the effect can never re-open the
        approval — at worst the owner re-approves (the fail-safe direction)."""
        if nonce_digest in self._redeemed_nonces:
            return False
        newfile = not os.path.exists(self.nonces_file)
        with open(self.nonces_file, "a", encoding="utf-8") as f:
            f.write(nonce_digest + "\n")
            f.flush()
            os.fsync(f.fileno())
        if newfile:
            try:
                os.chmod(self.nonces_file, 0o600)
            except OSError:  # pragma: no cover - non-POSIX
                pass
        self._redeemed_nonces.add(nonce_digest)
        return True

    def _write_head(self) -> None:
        head = {
            "size": len(self._receipts),
            "root": self.root(),
            "head_receipt_hash": self.head_hash,
        }
        with open(self.head_file, "w", encoding="utf-8") as f:
            json.dump(head, f, indent=2)

    # -- properties ----------------------------------------------------------
    @property
    def head_hash(self) -> str:
        return self._receipts[-1].receipt_hash() if self._receipts else GENESIS

    def __len__(self) -> int:
        return len(self._receipts)

    def all(self) -> List[Receipt]:
        return list(self._receipts)

    def get(self, receipt_id: str) -> Optional[Receipt]:
        i = self.index_of(receipt_id)
        return self._receipts[i] if i >= 0 else None

    def index_of(self, receipt_id: str) -> int:
        for i, r in enumerate(self._receipts):
            if r.receipt_id == receipt_id:
                return i
        return -1

    def root(self) -> str:
        return merkle_tree_hash(self._leaves).hex()

    def proof(self, m: int) -> List[str]:
        return [p.hex() for p in inclusion_proof(self._leaves, m)]

    # -- append --------------------------------------------------------------
    def append(
        self,
        signer: Signer,
        *,
        actor: str,
        action: str,
        risk_tier: int,
        decision: str,
        inputs: Any,
        outputs: Any,
    ) -> Receipt:
        r = Receipt.create(
            signer,
            actor=actor,
            action=action,
            risk_tier=risk_tier,
            decision=decision,
            inputs=inputs,
            outputs=outputs,
            prev_receipt_hash=self.head_hash,
            hash_key=self._digest_key,
        )
        with open(self.receipts_file, "a", encoding="utf-8") as f:
            f.write(r.to_json() + "\n")
        self._receipts.append(r)
        self._leaves.append(bytes.fromhex(r.receipt_hash()))
        self._write_head()
        return r

    # -- verification --------------------------------------------------------
    def verify_receipt(
        self, receipt_id: str, known_keys: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Offline-verify one receipt: signature + Merkle inclusion + chain link.

        ``known_keys`` (actor → public-key hex) additionally binds the signer key
        to the claimed actor. A bare signature only proves *some* key signed; it
        does not prove the *registered* key signed, so without this an attacker
        who rewrites the log can attribute an action to a victim actor and sign
        it with their own key (a key-substitution forgery). Pass
        ``keyring.public_keys()`` to close that gap. (Finding F4.)"""
        i = self.index_of(receipt_id)
        if i < 0:
            return {"ok": False, "reason": "receipt not found"}
        r = self._receipts[i]
        sig_ok = r.verify_signature()
        leaf = bytes.fromhex(r.receipt_hash())
        proof = inclusion_proof(self._leaves, i)
        root = merkle_tree_hash(self._leaves)
        inc_ok = verify_inclusion(leaf, i, len(self._leaves), proof, root)
        prev = GENESIS if i == 0 else self._receipts[i - 1].receipt_hash()
        chain_ok = r.prev_receipt_hash == prev
        actor_key_ok = self._actor_key_ok(r, known_keys)
        return {
            "ok": bool(sig_ok and inc_ok and chain_ok and actor_key_ok),
            "receipt_id": receipt_id,
            "index": i,
            "algorithm": r.algorithm,
            "signature": sig_ok,
            "merkle_inclusion": inc_ok,
            "chain_link": chain_ok,
            "actor_key_binding": actor_key_ok,
            "root": root.hex(),
            "tree_size": len(self._leaves),
        }

    @staticmethod
    def _actor_key_ok(r: Receipt, known_keys: Optional[Dict[str, str]]) -> bool:
        """True unless a known-keys registry is supplied and the receipt's
        public_key is not the registered key for its actor (or the actor is
        absent from the registry — an unrecognized signer)."""
        if known_keys is None:
            return True
        return known_keys.get(r.actor) == r.public_key

    def verify_log(
        self,
        expected_size: Optional[int] = None,
        expected_root: Optional[str] = None,
        known_keys: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Verify every signature and chain link across the whole log, and check
        the log against its checkpoint so trailing truncation is caught.

        - Always compares the live log against the on-disk ``head.json`` anchor;
          a naive truncation that didn't also rewrite head.json shows up as a
          size/root mismatch.
        - ``expected_size`` / ``expected_root`` accept an *external* (e.g.
          co-signed/published) checkpoint; a current size below it, or a root
          mismatch, is flagged. This is what defeats an attacker who rewrote
          head.json too — v0 cannot detect that without an external anchor.
        - ``known_keys`` (actor → public-key hex) binds each receipt's signer key
          to its claimed actor, so a forged log that attributes actions to a
          victim actor but signs them with the attacker's own key is rejected
          (a valid signature alone does not prove the *right* key signed). Pass
          ``keyring.public_keys()``. (Finding F4.)
        """
        problems: List[Dict[str, Any]] = []
        prev = GENESIS
        for i, r in enumerate(self._receipts):
            if not r.verify_signature():
                problems.append({"index": i, "id": r.receipt_id, "error": "bad signature"})
            if not self._actor_key_ok(r, known_keys):
                problems.append(
                    {"index": i, "id": r.receipt_id,
                     "error": f"public_key not the registered key for actor "
                              f"'{r.actor}' (forged attribution / key substitution)"}
                )
            if r.prev_receipt_hash != prev:
                problems.append(
                    {"index": i, "id": r.receipt_id, "error": "broken chain link"}
                )
            prev = r.receipt_hash()

        size = len(self._receipts)
        root = self.root()

        # On-disk anchor self-consistency: a trailing truncation that left an
        # un-rewritten head.json is detectable as a size/root disagreement.
        anchor = self._read_head()
        if anchor is not None:
            if anchor.get("size", size) > size:
                problems.append(
                    {"error": "log shorter than head.json anchor (possible truncation)",
                     "anchor_size": anchor.get("size"), "actual_size": size}
                )
            elif anchor.get("size") == size and anchor.get("root") not in (None, root):
                problems.append({"error": "root disagrees with head.json anchor"})

        # External checkpoint (defeats a rewritten head.json).
        if expected_size is not None and size < expected_size:
            problems.append(
                {"error": "log shorter than external checkpoint",
                 "expected_size": expected_size, "actual_size": size}
            )
        if expected_root is not None and expected_root != root:
            problems.append({"error": "root disagrees with external checkpoint"})

        return {
            "ok": len(problems) == 0,
            "count": size,
            "root": root,
            "problems": problems,
        }

    def _read_head(self) -> Optional[Dict[str, Any]]:
        if not os.path.exists(self.head_file):
            return None
        try:
            with open(self.head_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError):  # pragma: no cover - corrupt anchor
            return None
