"""Entity masking → synthetic surrogates, with a local-only reversible map.

Real entities are replaced by stable, non-numeric-heavy surrogates (so a masked
value is never itself re-matched as a different entity). The forward/reverse map
lives only in memory on the device — it is never written into a receipt and never
egressed, so even the surrogate↔real correspondence stays home.

The patterns here are a deterministic v0; a local model can generate richer,
context-preserving surrogates via `LocalModel.make_surrogate` (see local_model.py).
"""

from __future__ import annotations

import re
from typing import Dict, List, Optional

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PATH_RE = re.compile(r"(?:/Users/|/home/|~/)[^\s,;]+")
CARD_RE = re.compile(r"\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b")
PHONE_RE = re.compile(r"\b\+?\d[\d\-\s]{6,}\d\b")


class SurrogateMap:
    def __init__(self) -> None:
        self.forward: Dict[str, str] = {}
        self.reverse: Dict[str, str] = {}
        self._counters: Dict[str, int] = {}

    def _surrogate(self, kind: str, real: str) -> str:
        if real in self.forward:
            return self.forward[real]
        n = self._counters.get(kind, 0) + 1
        self._counters[kind] = n
        surrogate = {
            "email": f"user{n}@example.test",
            "path": f"/redacted/path-{n}",
            "card": f"card-token-{n}",
            "phone": f"phone-token-{n}",
            "name": f"Person-{n}",
        }[kind]
        self.forward[real] = surrogate
        self.reverse[surrogate] = real
        return surrogate

    def mask(self, text: str, names: Optional[List[str]] = None) -> str:
        out = text
        # Named entities first (longest match wins), then structured patterns.
        for name in sorted({n for n in (names or []) if n}, key=len, reverse=True):
            if name in out:
                out = out.replace(name, self._surrogate("name", name))
        out = EMAIL_RE.sub(lambda m: self._surrogate("email", m.group()), out)
        out = PATH_RE.sub(lambda m: self._surrogate("path", m.group()), out)
        out = CARD_RE.sub(lambda m: self._surrogate("card", m.group()), out)
        out = PHONE_RE.sub(lambda m: self._surrogate("phone", m.group()), out)
        return out

    def unmask(self, text: str) -> str:
        out = text
        # Replace longer surrogates first to avoid partial overlaps.
        for surrogate in sorted(self.reverse, key=len, reverse=True):
            out = out.replace(surrogate, self.reverse[surrogate])
        return out


def find_real_entities(text: str, names: Optional[List[str]] = None) -> List[str]:
    """Every real entity we expect to be masked — used for leak checking."""
    found: List[str] = [n for n in (names or []) if n and n in text]
    for rx in (EMAIL_RE, PATH_RE, CARD_RE, PHONE_RE):
        found.extend(rx.findall(text))
    return found
