# `people-ops` council — TEAM

> Living team card. Updated whenever the roster changes. Paired with [`AGENTS.md`](./AGENTS.md) which declares the council's contract.

## Remit

Roster stewardship, hiring via skill-creator, performance reviews, repurposing, ADR-tracked retirements.

## Convened when

Quarterly; whenever CEO needs a role the current roster doesn't cover.

## Lead

- **`coo`** — sonnet — Chief Operating Officer — the Chief who runs the People-ops Council.

## Specialists

| Agent | Tier | Purpose |
| --- | --- | --- |
| `roster-manager` | `haiku` | COO needs the living agent census — who exists, tier, last-used, utilization band. |
| `hiring-lead` | `haiku` | COO needs hire / fire / repurpose / tier-change proposals. |
| `performance-reviewer` | `haiku` | COO needs per-agent performance ratings for the current roster checkpoint. |
| `skill-creator` | `sonnet` | CEO hits a domain the current 16 councils don't cover (cryptography, game-dev, mobile, embedded, ML, compliance regime) and needs to extend the roster at runtime. |

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
