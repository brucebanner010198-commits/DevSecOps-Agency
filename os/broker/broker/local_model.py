"""Pluggable local model — identity-bearing inference stays on the device.

Only de-identified text is ever eligible to leave; anything touching real user
data runs here, locally. v0 ships a stub so the trust flow is runnable without a
model. A real backend (llama.cpp / Ollama / vLLM) implements the same interface.
"""

from __future__ import annotations

from typing import Optional


class LocalModel:
    """Interface for an on-device model."""

    def generate(self, prompt: str) -> str:  # pragma: no cover - interface
        raise NotImplementedError

    def make_surrogate(self, kind: str, real: str) -> Optional[str]:
        """Optionally generate a richer synthetic surrogate. Returning None uses
        the deterministic surrogate from surrogates.py."""
        return None


class StubLocalModel(LocalModel):
    def generate(self, prompt: str) -> str:
        return f"[local-model reply · {len(prompt)} chars processed on-device, identity-bearing]"
