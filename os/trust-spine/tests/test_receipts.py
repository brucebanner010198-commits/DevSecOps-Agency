from trust_spine.ledger import GENESIS
from trust_spine.receipts import Receipt
from trust_spine.signing import Ed25519Signer


def _make(signer=None, **overrides):
    signer = signer or Ed25519Signer()
    kw = dict(
        actor="leaf-agent-7",
        action="fs.write",
        risk_tier=1,
        decision="allow",
        inputs={"path": "/tmp/notes.md", "bytes": 12},
        outputs={"ok": True},
        prev_receipt_hash=GENESIS,
    )
    kw.update(overrides)
    return Receipt.create(signer, **kw)


def test_receipt_signature_verifies():
    assert _make().verify_signature() is True


def test_tampering_action_breaks_signature():
    r = _make()
    r.action = "fs.delete"  # mutate after signing
    assert r.verify_signature() is False


def test_tampering_inputs_hash_breaks_signature():
    r = _make()
    r.inputs_hash = "0" * 64
    assert r.verify_signature() is False


def test_receipt_hash_excludes_signature():
    r = _make()
    h_before = r.receipt_hash()
    r.signature = "deadbeef"  # signature is not part of the hashed payload
    assert r.receipt_hash() == h_before


def test_json_roundtrip_preserves_verification():
    r = _make()
    r2 = Receipt.from_json(r.to_json())
    assert r2 == r
    assert r2.verify_signature() is True


def test_inputs_hash_is_order_independent():
    s = Ed25519Signer()
    a = _make(s, inputs={"x": 1, "y": 2})
    b = _make(s, inputs={"y": 2, "x": 1})
    assert a.inputs_hash == b.inputs_hash
