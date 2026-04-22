# `docs` council — TEAM

> Living team card. Updated whenever the roster changes. Paired with [`AGENTS.md`](./AGENTS.md) which declares the council's contract.

## Remit

README, API docs, ≤ 10-minute tutorial, runbook; no placeholders, no fictional features.

## Convened when

Every project before release.

## Lead

- **`docs-lead`** — sonnet — Use this agent for the Documentation phase of a DevSecOps Agency project.

## Specialists

| Agent | Tier | Purpose |
| --- | --- | --- |
| `api-documenter` | `haiku` | Docs Lead needs API reference documentation generated from the architecture and the actual implemented code. |
| `readme-writer` | `haiku` | Docs Lead needs a polished top-level README for the generated project — overview, quick start, configuration, test, deploy, troubleshooting, and a security note. |
| `tutorial-writer` | `haiku` | CKO (docs-lead) needs a "getting started" tutorial — a step-by-step walkthrough that takes a new user from zero to a working example. |

## Worker tier

Specialists may, when a task decomposes cleanly along a dimension (per-file, per-table, per-endpoint, per-dependency), spawn **workers** — a third tier below specialist. Workers inherit the parent specialist's tool set and model tier unless overridden. Default depth cap is three levels (Chief → Specialist → Worker); deeper fanout requires an ADR from the lead.

Worker declaration lives in the parent specialist's frontmatter:

```yaml
workers:
  - name: <slug>
    split: <dimension>    # e.g. per-file, per-endpoint, per-dep
    max_parallel: 8       # per-council cap, overrides optional
```

Fanout + aggregation is handled by `skills/fanout/` (see root README).

This council declares no worker patterns in v0.3.7. Extend here when one emerges.

## Council norms

The council's must / must-not contract is authoritative in [`AGENTS.md`](./AGENTS.md). This file only records who currently staffs the council.
