---
adr: 0002
title: Central docs/adr/ directory at Agency root
status: accepted
date: 2026-04-26
deciders: ceo, cao
shipped-with-plugin: 0.6.1
supersedes: (none — closes Constitution Schedule B v0.5.5 outstanding note)
---

# ADR-0002: Central docs/adr/ directory at Agency root

## Context

The Constitution has referenced ADRs since v0.4.1, and individual ADRs have been filed under `_decisions/<slug>/adrs/` per-project since the same release. But there has never been an Agency-level home for ADRs that don't belong to a single project — conventions, founding-document amendments, plugin-wide patterns. This gap was explicitly noted in `CONSTITUTION.md` Schedule B as recently as the v0.5.5 amendment row:

> **Schedule B note — ADR backfill (outstanding).** The v0.5.0, v0.5.2, and v0.5.5 amendment ADRs referenced above live under `_decisions/<slug>/adrs/` once a project slug exists; a central `adrs/` directory at the repo root is not yet created.

That note has now been outstanding through three releases (v0.5.5, v0.5.6, v0.5.7) and one minor bump (v0.6.0). The v0.6.1 wave creates the directory and closes the note.

## Decision

Establish `docs/adr/` at the repo root as the home for **Agency-level ADRs**.

The split between Agency-level and per-project ADRs:

- `docs/adr/` — Agency-level: conventions adopted across all projects, founding-document amendments (Constitution Schedule A/B updates), plugin-wide patterns (skill conventions, runtime hook conventions, governance amendments)
- `_decisions/<slug>/adrs/` — per-project: Phase transitions, blocking-council verdicts on a specific project, waivers granted on a specific project, cross-model-panel runs scoped to one project's question

Naming: `ADR-NNNN-<kebab-topic>.md` where `NNNN` is a zero-padded sequence starting at 0001. Numbers are append-only (Constitution §5.2) — never reused even when an ADR is superseded. Superseding works by writing a new ADR that links the prior one via the `supersedes:` / `superseded-by:` frontmatter fields.

The directory ships with a `README.md` that documents the format and the index.

## Consequences

**Positive:**
- The Constitution Schedule B outstanding note is closed in v0.6.1.
- Agency-level conventions now have an obvious home — future readers searching for "why does the Agency do X" land in `docs/adr/`.
- Future Constitution amendments are filed as ADRs in `docs/adr/` first, then summarized in Schedule B with the ADR id linked.

**Negative:**
- Two ADR directories now exist (Agency-level + per-project). Authors must pick the right one. The README clarifies the split.

**Neutral:**
- This ADR is itself filed in `docs/adr/` (the very directory it establishes). The first ADR (`ADR-0001` for CONTEXT.md convention) and this one (`ADR-0002`) are filed simultaneously in the v0.6.1 commit.

## Alternatives considered

- **Single shared `_decisions/` directory** (without per-project subfolder split). Rejected — per-project receipts must be portable when a project's folder is archived or moved; Agency-level receipts should not move with any single project.
- **Wiki / GitHub Issues for Agency-level decisions.** Rejected — append-only invariant per Constitution §5.2 is harder to enforce off-repo; ADRs as files in the repo are auditable via `git log`.

## Provenance

- **Michael Nygard**, *Documenting Architecture Decisions* (2011) — the original ADR essay; influences the format and the "hard-to-reverse + surprising + real trade-off" three-way test documented in `docs/adr/README.md`.
- **CONSTITUTION.md Schedule B** (this repo) — the outstanding note this ADR closes.
