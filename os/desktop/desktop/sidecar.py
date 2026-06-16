"""The side-car dispatcher — the agent's structured door into the apps.

An agent calls `SideCar.call(actor, app, method, params)`; the dispatcher routes
it through the B1 Trust Kernel (verifier-gated, capability-checked, receipted) and
applies the app effect only if allowed. The human can `seize()` control at any
instant, which pauses agent calls (the interruptible part of the watchable
desktop).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from trust_spine.kernel import ActionRequest, SignedEffect, TrustKernel

from .apps import App


@dataclass
class SideCarResult:
    ok: bool
    decision: str  # allow | veto | pending | paused | error
    reason: str
    result: Any
    receipt_id: str


class SideCar:
    def __init__(self, kernel: TrustKernel, apps: Dict[str, App]) -> None:
        self.kernel = kernel
        self.apps = apps
        self.human_in_control = False
        # Register a signed-dispatch handler for every app action, so a
        # golden-gated method (e.g. comms.send) is executed by the kernel from
        # the SIGNED params — not from an opaque agent callable. This is what
        # makes the Owner's approval bind the exact send, not just a description.
        for app in apps.values():
            for m in app.methods.values():
                kernel.register_effect(m.action, self._dispatch_signed)

    def _dispatch_signed(self, signed: SignedEffect) -> Any:
        inputs = signed.inputs or {}
        app = self.apps.get(inputs.get("app"))
        method_def = app.method(inputs.get("method")) if app else None
        if method_def is None:
            raise ValueError(f"no method for signed effect {inputs!r}")
        return method_def.handler(inputs.get("params") or {})

    def describe(self) -> Dict[str, Any]:
        """The whole structured surface an agent sees — no pixels."""
        return {name: app.describe() for name, app in self.apps.items()}

    def seize(self) -> None:
        self.human_in_control = True

    def release(self) -> None:
        self.human_in_control = False

    def call(
        self,
        actor: str,
        app: str,
        method: str,
        params: Optional[Dict[str, Any]] = None,
        *,
        golden_share: Optional[bytes] = None,
        nonce: Optional[str] = None,
    ) -> SideCarResult:
        params = params or {}

        if self.human_in_control:
            return SideCarResult(
                False, "paused", "human has seized control; agent calls are paused", None, ""
            )

        target = self.apps.get(app)
        if target is None:
            return SideCarResult(False, "error", f"no app {app!r}", None, "")
        method_def = target.method(method)
        if method_def is None:
            return SideCarResult(False, "error", f"no method {app}.{method}", None, "")

        req = ActionRequest(
            actor=actor,
            action=method_def.action,
            inputs={"app": app, "method": method, "params": params},
            risk_tier=method_def.risk_tier,
            effect=lambda: method_def.handler(params),
            golden_share=golden_share,
            nonce=nonce,
        )
        res = self.kernel.submit(req)
        return SideCarResult(
            ok=res.allowed,
            decision=res.decision,
            reason=res.reason,
            result=res.output,
            receipt_id=res.receipt_id,
        )
