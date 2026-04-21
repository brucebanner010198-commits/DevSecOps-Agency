# cost-table — per-model $/M-token rates

Authoritative table for `budget` skill's cost conversion. **Update via ADR** when rates change.

## Rates (Apr 2026 baseline)

| Model                | Input $/M tok | Output $/M tok | Cached $/M tok |
| -------------------- | -------------:| --------------:| --------------:|
| claude-opus-4-6      | 15.00         | 75.00          | 1.50           |
| claude-sonnet-4-6    |  3.00         | 15.00          | 0.30           |
| claude-haiku-4-5     |  0.80         |  4.00          | 0.08           |

Rates are approximate. Budget-monitor's $ figures are **indicative only**; actual billing comes from Anthropic's usage reports.

## Per-agent defaults

- CEO (opus): counts at opus rates.
- Chiefs (sonnet): counts at sonnet rates.
- Specialists (haiku): counts at haiku rates.
- Anything that says `model: sonnet` in `agents/<name>.md` uses sonnet rates regardless of role, and so on.

## Conversion formula

```
cost_usd = (input_tokens * input_rate / 1_000_000)
        + (output_tokens * output_rate / 1_000_000)
        + (cached_read_tokens * cached_rate / 1_000_000)
```

Cached tokens come from the prompt-cache (reused system prompt + deterministic ordering). This is why the `prompt-cache rule` in root `AGENTS.md` matters — caching cuts $ by ~10× on repeated reads.

## Update protocol

- Rate changes announced by provider → CEO files ADR — `ADR-NNNN-cost-table-update-<date>`.
- Update takes effect at the next quarter boundary (consistent with regression-baseline quarter-freeze rule).
- Retroactive re-costing of past projects: optional; if done, append a `[correction]` line on each budget-ledger.md noting the re-costing.

## Forecasting

- Budget-monitor's forecast uses a 20-minute trailing token-rate (tokens per minute of CEO wall-clock), multiplied by remaining estimated wall-clock.
- If trend is accelerating (2nd derivative > 0), use worst-case (trend-line × 1.3) for the forecast.
- Chaotic trend → report `trend: chaotic` + use worst-case.

## Token accounting tips

- Worktree dispatches double-count is a smell. Each Chief's tokens count once; re-dispatches count once more. Budget-monitor de-duplicates by task ID.
- Compaction-driven re-reads do not count (read cache) — budget-monitor inspects `cached_read_tokens` and applies cached rate.
- Memory reads (MEMORY.md, patterns/*.md) are cached; their $ impact is negligible after the first read per session.
