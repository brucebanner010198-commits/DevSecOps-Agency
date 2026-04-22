# `audit` council — TEAM

> Living team card. Updated whenever the roster changes. Paired with [`AGENTS.md`](./AGENTS.md) which declares the council's contract.

## Remit

Read-only integrity pass over the agency's own paper trail — ADRs, gates, OKRs, memory writes.

## Convened when

Every project close, quarterly roll-up, user-requested integrity check.

## Lead

- **`cao`** — sonnet — Chief Audit Officer — the Chief who runs the Audit Council.

## Specialists

| Agent | Tier | Purpose |
| --- | --- | --- |
| `adr-auditor` | `haiku` | CAO needs the ADR paper trail audited. |
| `gate-auditor` | `haiku` | CAO needs the gate-decision trail audited. |
| `okr-auditor` | `haiku` | CAO needs the OKR scoring trail audited. |
| `memory-auditor` | `haiku` | CAO needs the durable-memory integrity audited. |
| `agent-governance-reviewer` | `sonnet` | CAO needs a meta-governance review of AI-agent code — tool functions without policy decorators, input paths that skip intent classification, hardcoded credentials, missing audit... |

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
