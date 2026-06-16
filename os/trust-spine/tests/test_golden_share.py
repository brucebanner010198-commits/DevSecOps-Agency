from trust_spine.golden_share import GoldenShare, action_intent
from trust_spine.kernel import ActionRequest, TrustKernel
from trust_spine.ledger import Ledger
from trust_spine.policy import Policy
from trust_spine.verifier import Verifier


def test_approve_verify_roundtrip():
    gs = GoldenShare()
    intent = action_intent("ceo", "spend", {"amount": 49}, {})
    sig = gs.approve(intent)
    assert gs.verify(intent, sig) is True


def test_signature_does_not_transfer_to_other_intent():
    gs = GoldenShare()
    sig = gs.approve(action_intent("ceo", "spend", {"amount": 49}, {}))
    other = action_intent("ceo", "spend", {"amount": 4900}, {})
    assert gs.verify(other, sig) is False


def test_nonce_changes_the_signed_bytes():
    gs = GoldenShare()
    sig = gs.approve(action_intent("ceo", "spend", {"amount": 49}, {}, nonce="n1"))
    # the same content with a different (or absent) nonce is a different intent
    assert gs.verify(action_intent("ceo", "spend", {"amount": 49}, {}, nonce="n2"), sig) is False
    assert gs.verify(action_intent("ceo", "spend", {"amount": 49}, {}), sig) is False


def _kernel(tmp_path, gs, on_spend=None):
    led = Ledger(str(tmp_path / "led"))
    k = TrustKernel(led, Verifier(Policy()), golden_share=gs)
    # A reserved 'spend' is executed from the SIGNED intent via this trusted
    # handler — never an agent's opaque callable.
    charged = []

    def handler(signed):
        charged.append(signed.inputs)
        if on_spend:
            on_spend(signed)
        return {"charged": signed.inputs.get("amount")}

    k.register_effect("spend", handler)
    return k, led, charged


def test_reserved_action_pending_without_golden_share(tmp_path):
    gs = GoldenShare()
    k, _, charged = _kernel(tmp_path, gs)
    res = k.submit(ActionRequest(actor="ceo", action="spend", inputs={"amount": 49}))
    assert res.pending is True and res.allowed is False
    assert charged == []


def test_golden_share_elevates_pending_to_allowed(tmp_path):
    gs = GoldenShare()
    k, led, charged = _kernel(tmp_path, gs)
    inputs, context, nonce = {"amount": 49}, {"to": "vendor"}, "nonce-1"
    sig = gs.approve(action_intent("ceo", "spend", inputs, context, nonce=nonce))
    res = k.submit(
        ActionRequest(
            actor="ceo", action="spend", inputs=inputs, context=context,
            golden_share=sig, nonce=nonce,
        )
    )
    assert res.allowed is True and "golden-share approved" in res.reason
    assert charged == [{"amount": 49}]
    assert led.verify_receipt(res.receipt_id)["ok"] is True


def test_replayed_signature_for_different_amount_stays_pending(tmp_path):
    gs = GoldenShare()
    k, _, charged = _kernel(tmp_path, gs)
    sig = gs.approve(action_intent("ceo", "spend", {"amount": 49}, {"to": "vendor"}, nonce="n"))
    res = k.submit(
        ActionRequest(
            actor="ceo", action="spend", inputs={"amount": 4900}, context={"to": "vendor"},
            golden_share=sig, nonce="n",
        )
    )
    assert res.pending is True and res.allowed is False
    assert charged == []


def test_same_approval_cannot_be_replayed_twice(tmp_path):
    """Red-team fix: one approval = one execution. The single-use nonce is burned
    on first use, so the identical signed request is refused the second time."""
    gs = GoldenShare()
    k, _, charged = _kernel(tmp_path, gs)
    inputs, context, nonce = {"amount": 49}, {"to": "vendor"}, "once"
    sig = gs.approve(action_intent("ceo", "spend", inputs, context, nonce=nonce))

    first = k.submit(ActionRequest(actor="ceo", action="spend", inputs=inputs,
                                   context=context, golden_share=sig, nonce=nonce))
    second = k.submit(ActionRequest(actor="ceo", action="spend", inputs=inputs,
                                    context=context, golden_share=sig, nonce=nonce))
    assert first.allowed is True
    assert second.allowed is False and "already used" in second.reason
    assert charged == [{"amount": 49}]  # executed exactly once


def test_effect_substitution_is_impossible(tmp_path):
    """Red-team CRITICAL fix: the Owner signs the inputs; the kernel runs the
    registered handler over those SIGNED inputs — NOT the agent's opaque
    callable. An attacker who attaches a malicious effect to the approved request
    cannot make it run."""
    gs = GoldenShare()
    k, _, charged = _kernel(tmp_path, gs)
    inputs, context, nonce = {"amount": 49}, {"to": "vendor"}, "n1"
    sig = gs.approve(action_intent("ceo", "spend", inputs, context, nonce=nonce))

    evil_ran = []
    res = k.submit(
        ActionRequest(
            actor="ceo", action="spend", inputs=inputs, context=context,
            golden_share=sig, nonce=nonce,
            effect=lambda: evil_ran.append("PAID ATTACKER $4900"),  # must be ignored
        )
    )
    assert res.allowed is True
    assert evil_ran == []  # the opaque callable never ran
    assert charged == [{"amount": 49}]  # only the signed $49 effect ran


def test_reserved_action_without_registered_handler_is_vetoed(tmp_path):
    """A golden-gated action with no trusted handler fails closed — opaque
    effects are not permitted for reserved actions."""
    gs = GoldenShare()
    led = Ledger(str(tmp_path / "led"))
    k = TrustKernel(led, Verifier(Policy()), golden_share=gs)  # no handler registered
    inputs, nonce = {"amount": 49}, "n1"
    sig = gs.approve(action_intent("ceo", "spend", inputs, {}, nonce=nonce))
    res = k.submit(ActionRequest(actor="ceo", action="spend", inputs=inputs,
                                 golden_share=sig, nonce=nonce))
    assert res.allowed is False and "no registered effect handler" in res.reason
