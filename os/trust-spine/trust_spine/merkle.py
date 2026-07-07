"""RFC 6962-style append-only Merkle tree.

We use the Certificate-Transparency hashing rules so receipt inclusion proofs
are interoperable with well-understood, audited definitions:

    leaf_hash(d)      = SHA-256(0x00 || d)
    node_hash(l, r)   = SHA-256(0x01 || l || r)
    MTH({})           = SHA-256("")

`d` (the leaf data) here is a receipt's content hash (32 bytes). The tree gives
us an O(log n) inclusion proof per receipt and a single root that can be
anchored/published so the whole log is tamper-evident, not just each receipt's
own signature.

Reference: RFC 6962 §2.1 (Merkle Tree Hash) and §2.1.1 (inclusion proof verify).
"""

from __future__ import annotations

import hashlib
from typing import List


def _sha256(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()


def leaf_hash(data: bytes) -> bytes:
    return _sha256(b"\x00" + data)


def node_hash(left: bytes, right: bytes) -> bytes:
    return _sha256(b"\x01" + left + right)


def _largest_power_of_two_less_than(n: int) -> int:
    """Largest k = 2**x with k < n (n >= 2)."""
    k = 1
    while k * 2 < n:
        k *= 2
    return k


def merkle_tree_hash(leaves: List[bytes]) -> bytes:
    """MTH over a list of raw leaf data (not pre-hashed)."""
    n = len(leaves)
    if n == 0:
        return _sha256(b"")
    if n == 1:
        return leaf_hash(leaves[0])
    k = _largest_power_of_two_less_than(n)
    return node_hash(merkle_tree_hash(leaves[:k]), merkle_tree_hash(leaves[k:]))


def inclusion_proof(leaves: List[bytes], m: int) -> List[bytes]:
    """Audit path for leaf index m (RFC 6962 PATH)."""
    n = len(leaves)
    if not 0 <= m < n:
        raise IndexError("leaf index out of range")
    return _subproof(m, leaves)


def _subproof(m: int, leaves: List[bytes]) -> List[bytes]:
    n = len(leaves)
    if n == 1:
        return []
    k = _largest_power_of_two_less_than(n)
    if m < k:
        return _subproof(m, leaves[:k]) + [merkle_tree_hash(leaves[k:])]
    return _subproof(m - k, leaves[k:]) + [merkle_tree_hash(leaves[:k])]


def verify_inclusion(
    leaf_data: bytes, m: int, n: int, proof: List[bytes], root: bytes
) -> bool:
    """Verify an inclusion proof exactly per RFC 6962 §2.1.1."""
    if not 0 <= m < n:
        return False
    fn, sn = m, n - 1
    r = leaf_hash(leaf_data)
    for p in proof:
        if sn == 0:
            return False
        if (fn & 1) or (fn == sn):
            r = node_hash(p, r)
            if not (fn & 1):
                while fn != 0 and not (fn & 1):
                    fn >>= 1
                    sn >>= 1
        else:
            r = node_hash(r, p)
        fn >>= 1
        sn >>= 1
    return sn == 0 and r == root
