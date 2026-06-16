import json
import os

from trust_spine.ledger import GENESIS, Ledger
from trust_spine.signing import Ed25519Signer


def _seed_ledger(path, n=4):
    led = Ledger(path)
    signer = Ed25519Signer()
    ids = []
    for i in range(n):
        r = led.append(
            signer,
            actor=f"leaf-{i}",
            action="fs.write" if i % 2 == 0 else "net.egress",
            risk_tier=1 if i % 2 == 0 else 3,
            decision="allow",
            inputs={"i": i},
            outputs={"ok": True},
        )
        ids.append(r.receipt_id)
    return led, signer, ids


def test_append_builds_hash_chain(tmp_path):
    led, _, _ = _seed_ledger(str(tmp_path / "led"), n=3)
    rs = led.all()
    assert rs[0].prev_receipt_hash == GENESIS
    assert rs[1].prev_receipt_hash == rs[0].receipt_hash()
    assert rs[2].prev_receipt_hash == rs[1].receipt_hash()


def test_verify_receipt_passes_for_each(tmp_path):
    led, _, ids = _seed_ledger(str(tmp_path / "led"), n=5)
    for rid in ids:
        res = led.verify_receipt(rid)
        assert res["ok"] is True
        assert res["signature"] and res["merkle_inclusion"] and res["chain_link"]


def test_verify_log_clean(tmp_path):
    led, _, _ = _seed_ledger(str(tmp_path / "led"), n=6)
    res = led.verify_log()
    assert res["ok"] is True
    assert res["count"] == 6
    assert res["problems"] == []


def test_persistence_reload(tmp_path):
    path = str(tmp_path / "led")
    led, _, ids = _seed_ledger(path, n=4)
    root_before = led.root()
    reloaded = Ledger(path)
    assert len(reloaded) == 4
    assert reloaded.root() == root_before
    assert reloaded.verify_receipt(ids[0])["ok"] is True


def test_head_file_anchor_written(tmp_path):
    path = str(tmp_path / "led")
    led, _, _ = _seed_ledger(path, n=3)
    with open(os.path.join(path, "head.json"), encoding="utf-8") as f:
        head = json.load(f)
    assert head["size"] == 3
    assert head["root"] == led.root()


def test_on_disk_tamper_is_detected(tmp_path):
    """Edit a field in the JSONL on disk → reload → signature verification fails."""
    path = str(tmp_path / "led")
    led, _, ids = _seed_ledger(path, n=4)
    target = ids[1]

    receipts_file = os.path.join(path, "receipts.jsonl")
    with open(receipts_file, encoding="utf-8") as f:
        lines = f.readlines()
    obj = json.loads(lines[1])
    assert obj["receipt_id"] == target
    obj["action"] = "net.egress.attacker"  # tamper
    lines[1] = json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n"
    with open(receipts_file, "w", encoding="utf-8") as f:
        f.writelines(lines)

    tampered = Ledger(path)
    res = tampered.verify_receipt(target)
    assert res["ok"] is False
    assert res["signature"] is False  # the signature no longer matches the edited field
    # and the whole-log check surfaces it too
    log = tampered.verify_log()
    assert log["ok"] is False
    assert any(p["error"] == "bad signature" for p in log["problems"])
