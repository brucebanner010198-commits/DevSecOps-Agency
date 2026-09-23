"""Request classification and model choice.

Ported from JARVIS-2.0/brain/orchestrator.py, _classify_node (lines 104 to 116)
and the three execute nodes (lines 121 to 147). The prototype's rule:

  1. If tools were offered and the text contains any of the tool keywords,
     route "tool".
  2. Else if the text contains any of the heavy keywords, route
     "heavy_reasoning".
  3. Else route "chat".

  chat            -> local model
  heavy_reasoning -> cloud model
  tool            -> cloud model when a cloud key is set, else local

Two deliberate changes from the prototype:

  * Matching is on whole words, not substrings. The prototype's substring
    test sent "recall" to the tool route (it contains "call"), "zip code" to
    the heavy route ("code") and "reasonable" to the heavy route ("reason").
  * heavy_reasoning goes to the cloud model only when one is configured;
    otherwise it goes local. The prototype always picked the cloud client
    for heavy requests and would fail without a key.

Keyword lists are env-driven through config.py (ROUTER_TOOL_KEYWORDS and
ROUTER_HEAVY_KEYWORDS). No model is involved in classification.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class Route(str, Enum):
    """What kind of request this is."""

    CHAT = "chat"
    HEAVY = "heavy_reasoning"
    TOOL = "tool"


class Target(str, Enum):
    """Which model answers it."""

    LOCAL = "local"
    CLOUD = "cloud"


# Keyword lists exactly as coded in JARVIS-2.0/brain/orchestrator.py lines 108 and 110.
TOOL_KEYWORDS: tuple[str, ...] = ("search", "run", "execute", "tool", "call", "web")
HEAVY_KEYWORDS: tuple[str, ...] = (
    "code",
    "analyze",
    "explain",
    "reason",
    "math",
    "programming",
    "calculate",
)


def _compile(words: Iterable[str]) -> re.Pattern[str]:
    cleaned = [w.strip().lower() for w in words if w and w.strip()]
    if not cleaned:
        return re.compile(r"(?!x)x")  # matches nothing
    alternation = "|".join(re.escape(w) for w in cleaned)
    # Lookarounds rather than \b so a keyword that ends in a symbol ("c++") still
    # matches as a whole word; \b needs a word character on the keyword side.
    return re.compile(rf"(?<!\w)(?:{alternation})(?!\w)", re.IGNORECASE)


@dataclass(frozen=True)
class RouterRules:
    """Keyword lists that drive classification. Whole-word, case-insensitive."""

    tool_keywords: tuple[str, ...] = TOOL_KEYWORDS
    heavy_keywords: tuple[str, ...] = HEAVY_KEYWORDS

    def __post_init__(self) -> None:
        object.__setattr__(self, "_tool_re", _compile(self.tool_keywords))
        object.__setattr__(self, "_heavy_re", _compile(self.heavy_keywords))

    def mentions_tool(self, text: str) -> bool:
        return bool(self._tool_re.search(text))  # type: ignore[attr-defined]

    def mentions_heavy(self, text: str) -> bool:
        return bool(self._heavy_re.search(text))  # type: ignore[attr-defined]


DEFAULT_RULES = RouterRules()


def classify(text: str, *, has_tools: bool = False, rules: RouterRules = DEFAULT_RULES) -> Route:
    """Classify the last user utterance. Precedence: tool, then heavy, then chat."""
    if not text or not text.strip():
        return Route.CHAT
    if has_tools and rules.mentions_tool(text):
        return Route.TOOL
    if rules.mentions_heavy(text):
        return Route.HEAVY
    return Route.CHAT


def choose_target(route: Route, *, cloud_available: bool) -> Target:
    """Pick the model for a route. Chat is always local; the rest prefer cloud when it exists."""
    if route is Route.CHAT:
        return Target.LOCAL
    return Target.CLOUD if cloud_available else Target.LOCAL


@dataclass(frozen=True)
class Decision:
    route: Route
    target: Target


def decide(
    text: str,
    *,
    has_tools: bool = False,
    cloud_available: bool = False,
    rules: RouterRules = DEFAULT_RULES,
) -> Decision:
    """Classify and choose in one call."""
    route = classify(text, has_tools=has_tools, rules=rules)
    return Decision(route=route, target=choose_target(route, cloud_available=cloud_available))
