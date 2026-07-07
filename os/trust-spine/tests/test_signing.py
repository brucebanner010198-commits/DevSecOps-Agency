from trust_spine.signing import (
    ED25519,
    Ed25519Signer,
    default_signer,
    pqc_available,
    verify_signature,
)


def test_ed25519_sign_verify_roundtrip():
    s = Ed25519Signer()
    msg = b"the AI acted; here is the receipt"
    sig = s.sign(msg)
    assert verify_signature(ED25519, s.public_key_bytes(), msg, sig) is True


def test_ed25519_tampered_message_fails():
    s = Ed25519Signer()
    sig = s.sign(b"pay $10")
    assert verify_signature(ED25519, s.public_key_bytes(), b"pay $1000", sig) is False


def test_ed25519_wrong_key_fails():
    a, b = Ed25519Signer(), Ed25519Signer()
    msg = b"egress to api.example.com"
    sig = a.sign(msg)
    assert verify_signature(ED25519, b.public_key_bytes(), msg, sig) is False


def test_ed25519_seed_is_deterministic():
    seed = b"\x01" * 32
    s1, s2 = Ed25519Signer.from_seed(seed), Ed25519Signer.from_seed(seed)
    assert s1.public_key_bytes() == s2.public_key_bytes()
    assert s1.seed() == seed


def test_unknown_algorithm_raises():
    import pytest

    with pytest.raises(ValueError):
        verify_signature("rot13", b"k", b"m", b"s")


def test_default_signer_present_and_consistent():
    s = default_signer()
    # ML-DSA when liboqs is installed, Ed25519 otherwise — never None.
    assert s.algorithm in {"ed25519", "ML-DSA-65"}
    if not pqc_available():
        assert s.algorithm == "ed25519"
