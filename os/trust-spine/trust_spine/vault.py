"""The Vault — act without reveal.

The Vault holds secrets and *uses* them (pastes a card number / password into a
field) without ever handing the plaintext to the AI agent. Three checks run
before any paste, defeating the confused-deputy autofill-phishing attack
(regression stress-test Scenario B):

  * trusted destination — the secret is written into a destination *registered
                       by the OS/compositor for that origin*, NOT a sink the
                       agent supplied. (Red-team: a caller-supplied sink let the
                       agent receive the plaintext directly — "act without
                       reveal" was theatre. The destination must be resolved by
                       trusted code keyed to the verified origin.)
  * origin-binding   — the destination's origin (and, when set, its certificate
                       fingerprint) must match the origin the secret is bound to.
                       A spoofed domain or an injected proxy fails this.
  * visibility audit — the target field must be actually visible. Fields hidden
                       with opacity:0 (or near-zero), display:none, off-screen
                       positioning (either direction), zero/near-zero size,
                       clip/clip-path collapse, transform:scale(0), aria-hidden,
                       or a buried z-index are refused (that is how malicious
                       pages harvest autofilled secrets invisibly). v0 inspects a
                       self-reported style dict; a production compositor measures
                       the real rendered box (allow-list a positive on-screen
                       bounding box) — see field_anomaly's note.

On success the Vault writes the secret into the registered destination; the
caller gets back only a masked reference and a hash — never the secret.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional


@dataclass
class FieldDescriptor:
    """What the OS compositor knows about the target input field."""

    origin: str  # e.g. "pay.utility.com"
    cert_fingerprint: str = ""  # bound TLS cert / public-key fingerprint, if known
    visible: bool = True
    style: Dict[str, Any] = field(default_factory=dict)  # css-ish attributes


def _to_px(value: Any) -> Optional[float]:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        v = value.strip().lower().removesuffix("px").strip()
        try:
            return float(v)
        except ValueError:
            return None
    return None


def field_anomaly(fd: FieldDescriptor) -> Optional[str]:
    """Return a reason string if the field looks hidden/suspicious, else None.

    v0 is a deny-list over a self-reported style dict, broadened to cover the
    common invisible-field techniques the red-team flagged. A production
    compositor should instead *allow-list* a measured on-screen bounding box
    (positive width/height within the viewport, effective opacity above a
    threshold, not clipped, no hidden ancestor) computed from the real rendered
    layout — never trust style claims from the page."""
    if not fd.visible:
        return "field marked not visible"
    s = {str(k).lower(): v for k, v in fd.style.items()}

    if str(s.get("aria-hidden", s.get("aria_hidden", ""))).lower() == "true":
        return "aria-hidden:true"

    # Near-zero opacity (0, "0", 0.004) — visually invisible but still fillable.
    opacity = _to_px(s.get("opacity", "1"))
    if opacity is not None and opacity < 0.1:
        return f"opacity:{opacity:g} (effectively invisible)"

    if str(s.get("display", "")).lower() == "none":
        return "display:none"
    if str(s.get("visibility", "")).lower() in ("hidden", "collapse"):
        return "visibility:hidden"

    # Off-screen in EITHER direction (left:-9999px or left:99999px both hide it).
    for edge in ("left", "right", "top", "bottom"):
        px = _to_px(s.get(edge))
        if px is not None and abs(px) >= 9999:
            return f"{edge}:{px:g}px (positioned off-screen)"

    # Zero / near-zero size.
    for dim in ("width", "height"):
        px = _to_px(s.get(dim))
        if px is not None and px <= 1:
            return f"{dim}:{px:g}px (zero/near-zero size)"

    # Collapsed clip — rect(0,0,0,0), inset(100%), circle(0), polygon to a point.
    clip = str(s.get("clip-path", s.get("clip", ""))).lower().replace(" ", "")
    if clip and (
        clip in ("inset(100%)", "circle(0)", "circle(0px)")
        or clip.startswith("rect(0,0,0,0")
        or clip.startswith("rect(0px,0px,0px,0px")
    ):
        return f"clip/clip-path:{clip} (collapsed to nothing)"

    # transform: scale(0) / scale3d(0,…) collapses the box.
    transform = str(s.get("transform", "")).lower().replace(" ", "")
    if "scale(0)" in transform or "scale(0," in transform or "scale3d(0," in transform:
        return f"transform:{transform} (scaled to zero)"

    z = _to_px(s.get("z-index", s.get("z_index")))
    if z is not None and z <= -100:
        return f"z-index:{z:g} (buried behind the page)"

    return None


@dataclass
class StoredSecret:
    value: bytes
    bound_origin: str
    bound_fingerprint: str = ""


@dataclass
class UseResult:
    ok: bool
    reason: str
    masked: str = ""  # e.g. "****4242" — never the full secret
    secret_sha256: str = ""


class Vault:
    def __init__(self) -> None:
        self._secrets: Dict[str, StoredSecret] = {}
        # Destinations the secret may be written into, keyed by origin. These are
        # registered by TRUSTED code (the OS/compositor), never by an agent, so
        # the agent can neither supply nor capture the write target.
        self._destinations: Dict[str, Callable[[bytes], None]] = {}

    def store(
        self,
        name: str,
        secret: "str | bytes",
        *,
        bound_origin: str,
        bound_fingerprint: str = "",
    ) -> None:
        value = secret.encode("utf-8") if isinstance(secret, str) else secret
        self._secrets[name] = StoredSecret(value, bound_origin, bound_fingerprint)

    def register_destination(self, origin: str, writer: Callable[[bytes], None]) -> None:
        """Trusted code registers where a secret bound to `origin` may be written
        (e.g. the real, visible field on that origin). The agent never sees or
        supplies this writer — that is what makes 'act without reveal' real."""
        self._destinations[origin] = writer

    def has(self, name: str) -> bool:
        return name in self._secrets

    def use(self, name: str, target: FieldDescriptor) -> UseResult:
        """Write secret `name` into the trusted destination registered for the
        target's origin — only if a destination exists and origin-binding +
        visibility checks pass. The secret never returns to the caller, and the
        caller cannot influence where it goes."""
        secret = self._secrets.get(name)
        if secret is None:
            return UseResult(False, f"no secret named {name!r}")

        if target.origin != secret.bound_origin:
            return UseResult(
                False,
                f"origin mismatch: field {target.origin!r} != bound "
                f"{secret.bound_origin!r} (possible spoof)",
            )
        if secret.bound_fingerprint and target.cert_fingerprint != secret.bound_fingerprint:
            return UseResult(
                False, "certificate fingerprint mismatch (possible proxy/MITM)"
            )

        writer = self._destinations.get(target.origin)
        if writer is None:
            # Fail closed: with no trusted destination there is nowhere safe to
            # write, and we will NOT hand the plaintext back to the caller.
            return UseResult(
                False,
                f"no trusted destination registered for origin {target.origin!r}",
            )

        anomaly = field_anomaly(target)
        if anomaly:
            return UseResult(False, f"refused: target field is hidden — {anomaly}")

        # Act without reveal: the Vault writes the secret into the trusted,
        # origin-bound destination; the agent process never receives the plaintext.
        writer(secret.value)
        tail = secret.value.decode("utf-8", errors="replace")[-4:]
        return UseResult(
            ok=True,
            reason="pasted into a verified, visible, origin-bound field",
            masked="****" + tail,
            secret_sha256=hashlib.sha256(secret.value).hexdigest(),
        )
