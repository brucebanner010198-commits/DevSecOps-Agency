"""The TrustBroker — the only egress path to a cloud model.

Every send is masked + normalized, routed through the B1 Trust Kernel
(default-deny host allowlist, signed receipt, optional golden-share gate), and
the reply is re-identified locally. The receipt records only the *masked* text
and the surrogate map never leaves memory — so neither the cloud nor the audit
log ever holds real identity data.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, List, Optional

from trust_spine.kernel import ActionRequest, TrustKernel

from .local_model import LocalModel, StubLocalModel
from .stylometry import normalize_style
from .surrogates import SurrogateMap, find_real_entities

CloudFn = Callable[[str], str]


@dataclass
class EgressResult:
    allowed: bool
    decision: str  # allow | veto | pending
    reason: str
    real_text: str  # what the user wrote (stays on device)
    sent_text: str  # masked + normalized — the only thing eligible to leave
    cloud_reply: Optional[str]  # re-identified locally; None if not sent
    receipt_id: str
    leaked: List[str]  # real entities that survived into sent_text (must be empty)


class TrustBroker:
    def __init__(
        self,
        kernel: TrustKernel,
        *,
        local_model: Optional[LocalModel] = None,
        normalizer: Callable[[str], str] = normalize_style,
    ) -> None:
        self.kernel = kernel
        self.local_model = local_model or StubLocalModel()
        self.normalize = normalizer

    def local_infer(self, prompt: str) -> str:
        """Identity-bearing inference — stays entirely on the device."""
        return self.local_model.generate(prompt)

    def egress(
        self,
        actor: str,
        text: str,
        *,
        host: str,
        names: Optional[List[str]] = None,
        golden_share: Optional[bytes] = None,
        nonce: Optional[str] = None,
        cloud: Optional[CloudFn] = None,
    ) -> EgressResult:
        smap = SurrogateMap()
        masked = smap.mask(text, names=names)
        sent = self.normalize(masked)
        cloud_fn = cloud or self._default_cloud

        # FAIL-CLOSED masking gate — runs BEFORE any send/receipt. If any
        # detectable real entity survived into `sent`, refuse: do not send, do
        # not receipt the raw blob. (Red-team: the leak check was advisory and
        # ran *after* submit, so unmasked PII could already have left.)
        residual = [e for e in find_real_entities(text, names) if e in sent]
        if residual:
            return EgressResult(
                allowed=False,
                decision="blocked",
                reason=(
                    f"masking incomplete: {len(residual)} entity(ies) survived into the "
                    "outbound text; egress refused before send"
                ),
                real_text=text,
                sent_text=sent,
                cloud_reply=None,
                receipt_id="",
                leaked=residual,
            )

        captured: dict[str, Any] = {}

        def run_egress(sent_text: str) -> dict[str, Any]:
            # Single source of truth for the actual send, used by both the
            # non-reserved opaque-effect path and the golden-gated registry path.
            captured["reply"] = cloud_fn(sent_text)
            # receipt output carries no real data, and records that masking was
            # verified complete before send.
            return {"sent_chars": len(sent_text), "residual_entities_present": False}

        # For a *reserved* egress (sensitive), the kernel dispatches the effect
        # from the SIGNED intent via this handler — so the Owner's signature
        # binds the exact masked text that leaves, not a description of it.
        self.kernel.register_effect(
            "net.egress", lambda signed: run_egress(signed.inputs["sent_text"])
        )

        res = self.kernel.submit(
            ActionRequest(
                actor=actor,
                action="net.egress",
                inputs={"sent_text": sent},  # masked text only — never the real text
                risk_tier=3,
                context={"host": host},
                golden_share=golden_share,
                nonce=nonce,
                effect=lambda: run_egress(sent),
            )
        )

        cloud_reply = None
        if res.allowed and "reply" in captured:
            cloud_reply = smap.unmask(captured["reply"])  # re-identify locally

        return EgressResult(
            allowed=res.allowed,
            decision=res.decision,
            reason=res.reason,
            real_text=text,
            sent_text=sent,
            cloud_reply=cloud_reply,
            receipt_id=res.receipt_id,
            leaked=[],  # the fail-closed gate above guarantees none survived
        )

    def _default_cloud(self, sent_text: str) -> str:
        # The simulated cloud model can only ever see the masked surrogates.
        return f"Acknowledged: {sent_text}"
