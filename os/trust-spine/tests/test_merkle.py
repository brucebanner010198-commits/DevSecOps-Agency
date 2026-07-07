import hashlib

from trust_spine.merkle import (
    inclusion_proof,
    leaf_hash,
    merkle_tree_hash,
    node_hash,
    verify_inclusion,
)


def _sha(b):
    return hashlib.sha256(b).digest()


def test_empty_tree_is_hash_of_empty_string():
    assert merkle_tree_hash([]) == _sha(b"")


def test_single_leaf_is_leaf_hash():
    assert merkle_tree_hash([b"a"]) == leaf_hash(b"a")


def test_two_leaf_root_known_answer():
    expected = node_hash(leaf_hash(b"a"), leaf_hash(b"b"))
    assert merkle_tree_hash([b"a", b"b"]) == expected


def test_three_leaf_structure():
    # RFC6962: split at largest power of two < 3 => k=2, so (a,b) | c
    left = node_hash(leaf_hash(b"a"), leaf_hash(b"b"))
    right = leaf_hash(b"c")
    assert merkle_tree_hash([b"a", b"b", b"c"]) == node_hash(left, right)


def test_inclusion_proofs_verify_for_all_indices():
    for n in range(1, 18):
        leaves = [f"receipt-{i}".encode() for i in range(n)]
        root = merkle_tree_hash(leaves)
        for m in range(n):
            proof = inclusion_proof(leaves, m)
            assert verify_inclusion(leaves[m], m, n, proof, root) is True


def test_wrong_leaf_fails_inclusion():
    leaves = [f"r{i}".encode() for i in range(7)]
    root = merkle_tree_hash(leaves)
    proof = inclusion_proof(leaves, 3)
    assert verify_inclusion(b"not-the-leaf", 3, 7, proof, root) is False


def test_proof_against_wrong_root_fails():
    leaves = [f"r{i}".encode() for i in range(5)]
    proof = inclusion_proof(leaves, 2)
    assert verify_inclusion(leaves[2], 2, 5, proof, b"\x00" * 32) is False
