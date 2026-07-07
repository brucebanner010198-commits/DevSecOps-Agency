"""Stylometry defense — normalize away idiosyncratic writing style.

Masking names is not enough: providers (or eavesdroppers) can re-identify a user
from writing style, sign-offs, and punctuation habits (the stress-test's
stylometric-leakage attack). This pass strips the obvious fingerprints and
neutralizes tone before any text leaves the device.

v0 is a deterministic heuristic. A local differential-privacy paraphrase model
plugs in via `paraphraser=` to rewrite more thoroughly; the interface is the same.
"""

from __future__ import annotations

import re
from typing import Callable, Optional

_SIGNOFF_RE = re.compile(
    r"\b(cheers|best|regards|warmly|thanks so much|many thanks|sincerely|xoxo|ttyl)\b[\s,!.]*.*$",
    re.IGNORECASE | re.MULTILINE,
)
_GREETING_RE = re.compile(
    r"^\s*(hey there|hiya|yo|dear team|dear all|hi all|howdy)\b[\s,!:-]*",
    re.IGNORECASE | re.MULTILINE,
)


def normalize_style(text: str, paraphraser: Optional[Callable[[str], str]] = None) -> str:
    if paraphraser is not None:
        return paraphraser(text)
    t = text
    t = _SIGNOFF_RE.sub("", t)
    t = _GREETING_RE.sub("", t)
    # Neutralize idiosyncratic punctuation habits.
    t = t.replace("—", ", ").replace("–", ", ").replace("…", ".")
    t = re.sub(r"!{1,}", ".", t)
    t = re.sub(r"\?{2,}", "?", t)
    # Collapse whitespace.
    t = re.sub(r"\s+", " ", t).strip()
    return t
