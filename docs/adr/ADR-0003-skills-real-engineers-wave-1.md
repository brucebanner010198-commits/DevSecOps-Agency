---
adr: 0003
title: Skills For Real Engineers — Wave 1 (concept-port provenance)
status: accepted
date: 2026-04-26
deciders: ceo, cto, cqo, csre
shipped-with-plugin: 0.6.1
---

# ADR-0003: Skills For Real Engineers — Wave 1 (concept-port provenance)

## Context

In the v0.6.1 cycle, the User asked the Agency to evaluate `mattpocock/skills` (MIT, ~54k stars at the time) for adaptation. The repo is a curated collection of slash-command skills built for one developer + one agent. Five skills surfaced as high-value for the Agency: a grilling-style discovery flow tied to a CONTEXT.md convention, a TDD red-green-refactor procedure, a zoom-out-for-context request pattern, an architecture-deepening review skill, and an ultra-compressed agent communication mode. A sixth, a runtime hook that blocks dangerous git commands at the pre-tool stage, was a clean fit for the Agency's existing runtime-hook chain.

The Agency had a choice between three porting strategies (literal port with attribution, concept-only port, or hybrid). The User selected concept-only port.

## Decision

Adopt **concept-only port** for the v0.6.1 wave. Each skill is re-authored from first principles in the Agency's voice and council-dispatch model. No prose, code, or specific examples are copied. Citations attach to the **underlying primary sources** that the broader engineering community draws on, not to any single curator that surfaces them:

| Skill | Primary sources cited |
|---|---|
| `skills/grill-with-docs/` | Eric Evans, *Domain-Driven Design* (2003) |
| `skills/tdd/` | Kent Beck, *Test-Driven Development: By Example* (2002); Beck, *Extreme Programming Explained* (2nd ed. 2004); Hunt & Thomas, *The Pragmatic Programmer* (anniversary ed.) |
| `skills/zoom-out/` | John Ousterhout, *A Philosophy of Software Design* (2nd ed. 2021) |
| `skills/improve-codebase-architecture/` | Ousterhout (deep-modules concept); Beck (XP "design every day" principle); Evans (ubiquitous language for architectural names) |
| `skills/caveman/` | No specific primary source — token-compression as a practice is observable across the LLM-tooling community and the underlying technique (drop articles, fragments OK, abbreviate) is decades-old shorthand from telegraph-era technical communication |
| `runtime-hooks/git-guardrails/` | The dangerous-git-commands enumeration is common engineering knowledge; we author our own list with our own justifications |

Where the Agency's adaptation differs from the broader community pattern (council-dispatch model, ADR-receipt invariant, COST §2.4 cost integration, cross-model-panel composition), the SKILL.md notes this as Agency-specific synthesis.

A single CHANGELOG line acknowledges `mattpocock/skills` as the curator that surfaced these patterns to the Agency in the v0.6.1 cycle, without per-file attribution.

## Consequences

**Positive:**
- No `LICENSES/MIT-mattpocock-skills.txt` file required. Zero per-file attribution overhead. The Agency's footprint stays clean.
- Each skill is shaped from day one for the Agency's council-dispatch model rather than starting from a single-developer slash-command shape and editing.
- Citations to the primary sources (Evans, Beck, Ousterhout, Hunt+Thomas) point future readers at the deep wells, not at any single intermediate.
- The "Chesterton's fence" credit sits in the CHANGELOG once — honest acknowledgment without perpetual burden.

**Negative:**
- The User must trust that the concept-port is a real re-implementation, not a copy with the names filed off. The "Provenance" section in each skill makes the citation chain explicit; CAO can spot-check.
- Future readers who search GitHub for "grill-with-docs" will not find an attribution trail back to the curator. The CHANGELOG provenance line is the only acknowledgment.

**Neutral:**
- Future ports from third-party curators follow the same decision procedure: literal-port (with `LICENSES/` attribution) when prose/code is copied substantively; concept-only-port (with primary-source citations and a CHANGELOG curator line) when the value is in the pattern.

## Alternatives considered

- **Literal port with attribution** (the Agency's posture for `ui-ux-pro-max` v0.5.2 and the `google/skills` import v0.5.5). Rejected for v0.6.1 because the source is short prose-heavy slash-command shape that requires substantial re-shaping anyway; the rewriting is unavoidable; doing it from primary sources is cleaner than starting from text-and-editing.
- **Hybrid: concept-port the prose, literal-port the bash script.** Rejected because the dangerous-git-commands enumeration is common knowledge; no copyright attaches to a list of well-known commands; we can author our own pattern set (overlapping in obvious places) with our own justifications.

## Provenance

- The User's directive in the v0.6.1 conversation cycle: "can matt's skill be repurposed instead of simply copying specific to this agency? This way we don't have to mention his name or get rid of the copyright situation?"
- US copyright doctrine: ideas are not copyrightable; specific expression is. Concept-only port produces no derivative work and triggers no MIT attribution requirement.
- Open-source convention (variable): "credit the field, not the curator." The CHANGELOG line acknowledges `mattpocock/skills` as the curator that pointed the Agency at the patterns in this cycle.
