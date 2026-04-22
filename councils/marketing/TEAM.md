# `marketing` council — TEAM

> Living team card. Updated whenever the roster changes. Paired with [`AGENTS.md`](./AGENTS.md) which declares the council's contract.

## Remit

Positioning, landing copy, brand voice, growth analyst input. Informing only, not blocking.

## Convened when

Every project pre-launch; narrative pipeline mode for portfolio rollups.

## Lead

- **`cmo`** — sonnet — Chief Marketing Officer — the Chief who runs the Marketing Council.

## Specialists

| Agent | Tier | Purpose |
| --- | --- | --- |
| `positioning-strategist` | `haiku` | CMO needs a positioning statement for a project or a narrative score on a shortlisted pipeline idea. |
| `comms-writer` | `haiku` | CMO needs launch copy — press release, landing headline, launch announcement, or week-0-to-week-4 comms sequence. |
| `brand-guardian` | `haiku` | CMO needs a brand consistency check on naming, tone, or visual direction, or when a new project's name/tagline risks collision with prior work. |
| `growth-analyst` | `haiku` | CMO needs activation / retention / monetisation targets for a project, or a growth-loop sketch. |

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
