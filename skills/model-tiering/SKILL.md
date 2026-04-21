---
name: model-tiering
description: >
  This skill should be used when the CEO or skill-creator needs to assign a
  model tier to an agent — Haiku for specialists, Sonnet for Chiefs and
  cross-cutting authors, Opus for the CEO. It fixes the `model:` frontmatter
  field on every `agents/*.md` file and defines the override rules for
  upgrading or downgrading a specific agent. Trigger phrases: "pick a model
  for this agent", "which tier", "upgrade this agent to Sonnet",
  "downgrade to Haiku", "apply tiering". Also trigger when the CEO dispatches
  a new agent and the `model:` field is missing or set to `inherit`.
metadata:
  version: "0.1.0"
---

# model-tiering — one tier per role

Assign the cheapest model that reliably does the work. The default tiering below is the hard floor; agents can be upgraded one tier up with a cited reason, never downgraded below the floor.

## Default tier map

| Tier    | Who                                                                                  | Why                                                                                      |
| ------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| Opus    | `ceo`                                                                                 | Cross-phase orchestration, irreducible-decision detection, negotiation with the user.     |
| Sonnet  | All 9 Chiefs: `cro`, `pm-lead`, `engineering-lead` (CTO+VP-Eng), `security-lead`, `qa-lead`, `devops-lead`, `docs-lead`, `gc`. Plus `skill-creator`. | Council orchestration, gate judgement, report synthesis, authoring new personas.          |
| Haiku   | All ~28 specialists                                                                   | Narrow artifact production with clear template + one-pass verification by their Chief.    |

See `references/tier-rules.md` for the exhaustive agent→tier table.

## When to override

### Upgrade one tier

Allowed when all of:

- The agent has a **cross-cutting** output (touches ≥ 2 councils' artifacts).
- The agent's Chief has invoked a fix-loop on the same phase ≥ once.
- The override is logged in the task row's `note` with the cited reason.

Example: `threat-modeler` upgraded Haiku → Sonnet for a crypto-heavy project where STRIDE analysis crosses backend + infra.

### Downgrade one tier

**Never.** Haiku is the floor. If Haiku can't do the work, upgrade — don't ship a worse result.

## Frontmatter contract

Every `agents/<name>.md` carries exactly one of:

```yaml
model: haiku
model: sonnet
model: opus
```

No `inherit`, no blank, no unknown values. `skill-creator` refuses to author an agent without this field.

## Dispatch enforcement

The CEO's dispatch step (in `skills/ceo/SKILL.md > ## 3. Board meetings`) reads the target agent's frontmatter before calling the Task tool. If `model:` is missing or unknown, the CEO:

1. Logs an `error` entry to its session log with `"missing model tier for <agent>"`.
2. Invokes `skill-creator` to add the tier per `references/tier-rules.md`.
3. Then proceeds with the dispatch.

## Cost + latency rationale

Short version (full math in `references/cost-model.md`):

- Specialists produce one artifact with a tight template. Haiku is sufficient and the Chief catches errors on report.
- Chiefs must synthesise 3–5 specialist reports and emit a gate. This requires Sonnet-class reasoning.
- CEO sequences 9 Chiefs across 7 phases, detects irreducible decisions, and never touches code. Opus earns its keep once per project.

Optimising this trio tends to dominate both cost and wall time for a full project run; tune only when evidence warrants.

## Progressive disclosure

- `references/tier-rules.md` — per-agent tier assignment with one-line rationale.
- `references/cost-model.md` — cost and latency math behind the default tiering.
- `references/override-log.md` — append-only log of runtime overrides (per project + reason).
