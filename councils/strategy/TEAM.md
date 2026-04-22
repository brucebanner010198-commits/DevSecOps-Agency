# `strategy` council — TEAM

> Living team card. Updated whenever the roster changes. Paired with [`AGENTS.md`](./AGENTS.md) which declares the council's contract.

## Remit

Portfolio-level horizon scanning, competitive analysis, market sizing, RICE-ranked opportunity shortlist.

## Convened when

Quarterly roll-up; user-initiated idea pipeline; REM dreaming trigger.

## Lead

- **`cso`** — sonnet — Chief Strategy Officer — the Chief who runs the Strategy Council.

## Specialists

| Agent | Tier | Purpose |
| --- | --- | --- |
| `trend-scout` | `haiku` | CSO needs a workspace-level emerging-tech + adjacent-market scan — what's rising, what's adjacent to current bets, what's fading. |
| `competitive-analyst` | `haiku` | CSO needs a portfolio-level competitive map — who's moving where across the workspace's current and candidate markets. |
| `market-sizer` | `haiku` | CSO needs TAM/SAM/SOM estimates across candidate markets. |
| `opportunity-ranker` | `haiku` | CSO needs the candidate opportunities ranked against a shared scorecard — RICE + strategic-fit + narrative-score from CMO. |

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
