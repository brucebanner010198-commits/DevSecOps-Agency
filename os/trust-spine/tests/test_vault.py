from trust_spine.capabilities import SECRET_ACCESS, CapabilityBroker
from trust_spine.kernel import ActionRequest, TrustKernel
from trust_spine.ledger import Ledger
from trust_spine.policy import Policy
from trust_spine.vault import FieldDescriptor, Vault, field_anomaly
from trust_spine.verifier import Verifier

ORIGIN = "pay.utility.com"


def _vault(dest=None):
    """A Vault holding the card, with a TRUSTED destination registered for the
    bound origin. `dest` is that trusted writer (stand-in for the compositor's
    real field) — note the agent never supplies it."""
    v = Vault()
    v.store("card", "4242424242424242", bound_origin=ORIGIN, bound_fingerprint="AA:BB")
    if dest is not None:
        v.register_destination(ORIGIN, dest)
    return v


def test_use_into_good_field_acts_without_reveal():
    pasted = []  # the TRUSTED destination, registered by us (not the agent)
    v = _vault(dest=pasted.append)
    fd = FieldDescriptor(origin=ORIGIN, cert_fingerprint="AA:BB", visible=True)
    res = v.use("card", fd)
    assert res.ok is True
    assert pasted == [b"4242424242424242"]  # the secret reached the trusted field
    assert res.masked == "****4242"
    # the caller learns only a masked ref + a hash; UseResult carries no plaintext
    assert not hasattr(res, "value")
    assert "4242424242424242" not in (res.masked + res.reason + res.secret_sha256)


def test_use_refused_when_no_trusted_destination_registered():
    """Red-team fix: the agent cannot supply the sink. With no trusted
    destination for the origin, the Vault fails closed — it will NOT hand the
    plaintext back to anyone."""
    v = _vault(dest=None)  # nothing registered
    fd = FieldDescriptor(origin=ORIGIN, cert_fingerprint="AA:BB", visible=True)
    res = v.use("card", fd)
    assert res.ok is False and "no trusted destination" in res.reason


def test_origin_mismatch_refused():
    pasted = []
    v = _vault(dest=pasted.append)
    fd = FieldDescriptor(origin="pay.attacker.com", cert_fingerprint="AA:BB")
    res = v.use("card", fd)
    assert res.ok is False and "origin mismatch" in res.reason
    assert pasted == []  # nothing pasted


def test_cert_fingerprint_mismatch_refused():
    pasted = []
    v = _vault(dest=pasted.append)
    fd = FieldDescriptor(origin=ORIGIN, cert_fingerprint="EVIL")
    res = v.use("card", fd)
    assert res.ok is False and "fingerprint" in res.reason
    assert pasted == []


def test_hidden_fields_refused():
    pasted = []
    v = _vault(dest=pasted.append)
    for style in (
        {"opacity": 0},
        {"opacity": "0"},
        {"opacity": 0.004},  # fractional but invisible (red-team bypass)
        {"display": "none"},
        {"visibility": "hidden"},
        {"left": "-9999px"},
        {"left": -9999},
        {"left": "99999px"},  # off-screen the OTHER direction (red-team bypass)
        {"top": "12000px"},
        {"width": 0},  # zero size (red-team bypass)
        {"height": "0px"},
        {"width": "1px"},
        {"clip-path": "inset(100%)"},  # collapsed clip (red-team bypass)
        {"clip": "rect(0,0,0,0)"},
        {"transform": "scale(0)"},  # scaled to nothing (red-team bypass)
        {"aria-hidden": "true"},
        {"z-index": -999},
    ):
        fd = FieldDescriptor(origin=ORIGIN, cert_fingerprint="AA:BB", style=style)
        res = v.use("card", fd)
        assert res.ok is False, f"should refuse style {style}"
        assert pasted == []


def test_field_anomaly_passes_clean_field():
    assert field_anomaly(FieldDescriptor(origin="x", visible=True, style={"opacity": 1})) is None
    # a visible field with benign size is fine
    assert field_anomaly(
        FieldDescriptor(origin="x", visible=True, style={"width": "200px", "height": "32px"})
    ) is None


def test_kernel_vault_use_blocks_confused_deputy(tmp_path):
    """End-to-end: an agent with secret_access tries to autofill into a hidden
    field — the kernel records a veto and nothing is pasted."""
    broker = CapabilityBroker()
    broker.grant("pay-leaf", {SECRET_ACCESS})
    led = Ledger(str(tmp_path / "led"))
    pasted = []
    kernel = TrustKernel(
        led,
        Verifier(Policy(), capability_broker=broker),
        vault=_vault(dest=pasted.append),
    )
    hidden = FieldDescriptor(
        origin=ORIGIN, cert_fingerprint="AA:BB", style={"opacity": 0, "left": "-9999px"}
    )
    res = kernel.submit(
        ActionRequest(actor="pay-leaf", action="vault.use", secret_name="card", field=hidden)
    )
    assert res.allowed is False and "vault refused" in res.reason
    assert pasted == []
    assert led.verify_log()["ok"] is True


def test_kernel_vault_use_allows_good_field(tmp_path):
    broker = CapabilityBroker()
    broker.grant("pay-leaf", {SECRET_ACCESS})
    led = Ledger(str(tmp_path / "led"))
    pasted = []
    kernel = TrustKernel(
        led, Verifier(Policy(), capability_broker=broker), vault=_vault(dest=pasted.append)
    )
    good = FieldDescriptor(origin=ORIGIN, cert_fingerprint="AA:BB", visible=True)
    res = kernel.submit(
        ActionRequest(actor="pay-leaf", action="vault.use", secret_name="card", field=good)
    )
    assert res.allowed is True
    assert pasted == [b"4242424242424242"]
    # the receipt records the masked ref + hash, never the secret
    r = led.get(res.receipt_id)
    assert "4242424242424242" not in r.to_json()


def test_kernel_vault_use_fails_closed_without_a_vault(tmp_path):
    """Red-team fix: a vault.use action must never fall through to a generic
    effect when no Vault is configured — it fails closed."""
    led = Ledger(str(tmp_path / "led"))
    kernel = TrustKernel(led, Verifier(Policy()))  # no vault
    ran = []
    res = kernel.submit(
        ActionRequest(
            actor="x",
            action="vault.use",
            secret_name="card",
            field=FieldDescriptor(origin=ORIGIN, visible=True),
            effect=lambda: ran.append(True),  # must NOT run
        )
    )
    assert res.allowed is False and "no Vault configured" in res.reason
    assert ran == []
