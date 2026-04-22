# `legal` council — TEAM

> Living team card. Updated whenever the roster changes. Paired with [`AGENTS.md`](./AGENTS.md) which declares the council's contract.

## Remit

License compatibility, privacy posture, IP lineage, compliance-drift detection. Red blocks public release.

## Convened when

Every project pre-release; quarterly drift sweep; any close-phase that ships an external artifact.

## Lead

- **`gc`** — sonnet — General Counsel — the Chief who runs the Legal Council at the end of the pipeline.

## Specialists

| Agent | Tier | Purpose |
| --- | --- | --- |
| `license-checker` | `haiku` | GC (General Counsel) needs a license compatibility check across every dependency — a software bill of materials (SBOM) plus a go / fix / no-go call for public release. |
| `privacy-counsel` | `haiku` | GC (General Counsel) needs a privacy posture review — what personal data is collected, how it flows, what notice + choice the product provides — and a draft privacy notice if th... |
| `compliance-drift` | `sonnet` | Legal Council specialist (Wave 7). |
| `ip-lineage` | `haiku` | Legal Council specialist (Wave 7). |

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
