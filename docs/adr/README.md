# docs/adr/ — Agency-level Architecture Decision Records

The Agency's central ADR home, established **2026-04-26** with plugin v0.6.1. Closes the v0.5.0 Schedule B outstanding note (the Constitution had referenced ADRs since v0.4.1 but no central directory existed).

## What lives here

ADRs that span the Agency itself — conventions, founding-document amendments, plugin-wide patterns. Per-project ADRs live at `_decisions/<slug>/adrs/` (per Constitution Schedule B).

The split:

- `docs/adr/` — **Agency-level**: conventions adopted across all projects, founding-document amendments, plugin-wide patterns
- `_decisions/<slug>/adrs/` — **per-project**: Phase transitions, blocking-council verdicts, waivers, cross-model-panel runs scoped to one project

## Format

Each ADR is one markdown file named `ADR-NNNN-<kebab-topic>.md` where `NNNN` is a zero-padded sequence starting at 0001. Numbers are append-only — never reused even if an ADR is superseded. Superseding works by writing a new ADR that links the prior one (per Constitution §5.2 append-only invariant).

Recommended frontmatter:

```yaml
---
adr: 0001
title: <short title>
status: proposed | accepted | superseded | deprecated
date: 2026-MM-DD
deciders: <list of councils or chiefs>
supersedes: <ADR-NNNN, if applicable>
superseded-by: <ADR-NNNN, if applicable>
---
```

## What an ADR is for

Per the convention adopted from Michael Nygard's 2011 essay *Documenting Architecture Decisions*, an ADR is filed when ALL THREE are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **Result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. ADRs are receipts (per Constitution §5.1 receipts ratio = 100%) — they're not a place for trivia.

## Index (auto-maintained best-effort; check the directory listing for ground truth)

| ADR | Title | Status | Date |
|---|---|---|---|
| 0001 | CONTEXT.md per-project convention | Accepted | 2026-04-26 |
| 0002 | docs/adr/ central directory | Accepted | 2026-04-26 |
| 0003 | Skills For Real Engineers wave 1 — concept-port provenance | Accepted | 2026-04-26 |

## Provenance

- **Michael Nygard**, *Documenting Architecture Decisions* (2011) — the original ADR essay; source of the "hard-to-reverse + surprising + real trade-off" three-way test.
- **Constitution §5.1 + §5.2** (this repo) — receipts-ratio invariant + append-only invariant that govern how ADRs are filed and superseded.
- **Constitution Schedule B** (this repo, v0.5.5 amendment row) — explicitly noted the central `docs/adr/` directory as outstanding; this README closes that gap.
