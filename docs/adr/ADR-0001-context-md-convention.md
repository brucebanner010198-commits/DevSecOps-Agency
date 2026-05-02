---
adr: 0001
title: CONTEXT.md per-project convention
status: accepted
date: 2026-04-26
deciders: ceo, cto, cko
shipped-with-plugin: 0.6.1
---

# ADR-0001: CONTEXT.md per-project convention

## Context

Through v0.6.0, the Agency had no formal "ubiquitous language" document at either the Agency or per-project level. The result was real cost: agents reading prior session logs had to re-derive what "council," "drill," "panel," "stage," "phase" meant in context every time. Misalignment surfaced repeatedly — a Specialist would talk about "the agent" when a Worker was meant; a Council file would say "team" when a Council was meant. The Constitution's terms were defined; the operational vocabulary that surrounds them was not.

The brownfield-discovery research in v0.5.4 specifically identified the gap: incoming projects with their own jargon (e.g. an invoice-splitter where "split" means something different from a generic engineering "split") forced agents to re-learn vocabulary every session, with cost.

## Decision

Establish **CONTEXT.md** as a first-class founding-document convention at two scopes:

1. **Agency-level**: `CONTEXT.md` at the repo root. Contains the canonical glossary for terms used across all projects (Council, Chief, Specialist, ADR, Receipt, Heartbeat, etc.). Updated lazily — terms added when first resolved, not pre-populated.

2. **Per-project**: `<slug>/CONTEXT.md` at each project folder root. Contains terms specific to that project's domain. Inherits from the Agency-level CONTEXT.md; project-level definitions override Agency-level for that project's scope.

Both files follow a consistent shape:
- One section per entity category
- Each entity gets a 1-2 sentence canonical definition + an `*Avoid*` list of terms NOT to use
- A "Resolved ambiguities" section recording decisions about terms that previously meant multiple things
- A "Provenance" section citing the underlying convention sources

When a term in any artifact (council file, skill, ADR, session log) conflicts with the canonical definition, **CONTEXT.md wins**. Load-bearing conflicts file a `language-conflict` ADR.

The new `grill-with-docs` skill (v0.6.1) updates CONTEXT.md inline as terms get resolved during a grilling session — not in a batch at the end.

## Consequences

**Positive:**
- Variables, functions, files, council files, ADRs all use a single agreed-upon vocabulary.
- Codebases (per-project) and the Agency itself become easier to navigate for future agents.
- Token cost drops because the shared language is more concise than ad-hoc paraphrase.
- New brownfield projects produce their `<slug>/CONTEXT.md` during Phase 1 Intake — the discovery output that v0.5.4 research identified as missing.

**Negative:**
- Adds a maintenance task: when terminology drifts (e.g. a Council renames a concept), CONTEXT.md must be updated in the same commit. Caught by `grill-with-docs` and by CAO spot-checks.
- Per-project CONTEXT.md files multiply across projects. Each is small (~50-200 lines) and project-scoped, so the maintenance is local.

**Neutral:**
- CONTEXT.md is incorporated by reference into Constitution Schedule A (added v0.6.1 amendment).

## Alternatives considered

- **Inline glossary in CONSTITUTION.md.** Rejected — CONSTITUTION.md is supreme law and rarely amended; ubiquitous language drifts more often than constitutional terms; coupling them creates pressure to amend the Constitution for vocabulary changes.
- **Per-skill glossary blocks in each SKILL.md.** Rejected — duplicates the same terms across many files; first one to define a term wins by accident.
- **No formal convention; rely on natural-language consistency.** Rejected — that was the v0.5.x posture; the brownfield-discovery research surfaced the cost.

## Provenance

- **Eric Evans**, *Domain-Driven Design* (Addison-Wesley, 2003) — the "ubiquitous language" concept this convention operationalizes.
- The Agency's own brownfield-discovery research from the v0.5.4 cycle (`mnt/outputs/v0.5.4-research-tri-mode-intake.md` §4.2) identified the missing CONTEXT.md as a discovery-phase gap.
