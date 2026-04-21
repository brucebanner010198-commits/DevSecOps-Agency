---
name: budget
description: This skill should be used whenever the CEO is deriving a new project's budget (at OKR derivation time), tracking burn against that budget (on every Chief report), or accounting a project's final cost (at close). The budget skill sets per-project token + $ caps, allocates per-phase sub-caps, records burn entries to `metrics.tokens` + `metrics.cost`, and surfaces overruns. Trigger phrases include "set the budget", "budget allocation", "how much have we spent", "over budget", "budget overrun", "token burn", "cost accounting", "cheap project / medium project / large project".
metadata:
  version: "0.3.0-alpha.5"
---

# budget — token + $ discipline

Without this skill, projects spend until they're done and nobody knows why. With this skill, projects carry a declared budget + per-phase allocation; `budget-monitor` is the watchdog; `adr` records overruns; CEO decides the ladder route on red.

## When to invoke

- **Derive** at OKR derivation (`skills/okr` invokes this skill). Default size class is set from project scope at intake; user can override in the top-5 user-meeting.
- **Track** on every Chief report — accumulator updates to `<slug>/status.json > metrics.tokens` and `metrics.cost`.
- **Report** on every close — `<slug>/eval/budget-ledger.md` written by `budget-monitor`.
- **Pre-flight** before every harness run, every worktree merge, and every rung-transition to Rung 4 (hire) — the action's expected cost is compared to remaining budget.

## Size classes

| Class  | Total tokens | Total $ (approx) | Scope                                  |
| ------ | ------------ | ---------------- | -------------------------------------- |
| small  | 75 k         | $1.50            | single-screen app, simple utility      |
| medium | 250 k        | $5.00            | full-stack with auth + DB + deploy     |
| large  | 1 M          | $20              | multi-service, integrations, AI-heavy  |
| custom | user-set     | user-set         | declared via ADR in top-5 commit       |

Defaults are conservative. User can raise via ADR; lowering below the floor (10 % of class minimum) requires a waiver ADR.

## Per-phase allocation

Default split (medium project, 100 % = total):

```
discovery  10 %
design     15 %
build      40 %
verify     15 %
ship       10 %
docs        5 %
close       5 %
```

Projects may re-allocate via ADR (e.g. a docs-heavy project shifts 5 pp from build to docs). Re-allocation happens at OKR-derivation time, not mid-flight.

## Burn tracking

- `metrics.tokens.byPhase.<phase>` accumulates across all Chief reports in that phase.
- `metrics.cost.byPhase.<phase>` tracks $ (computed from token × per-model rate table in `references/cost-table.md`).
- `metrics.tokens.total` + `metrics.cost.total` roll up automatically.

## Thresholds (budget-monitor)

| Condition                                   | Flag     | Action                                                    |
| ------------------------------------------- | -------- | --------------------------------------------------------- |
| Phase burn > 120 % of phase cap             | yellow   | `budget-monitor` surfaces; CEVO reports; CEO decides      |
| Cumulative burn > 90 % of total             | yellow   | notify: approaching cap                                   |
| Cumulative burn > 110 % of total            | red      | Rung 6 (user consult): pivot / expand budget / park       |
| Forecast-at-close > 150 % of total          | red      | Rung 6 immediately; do not wait for overrun to realise    |

## Process (derive)

1. `skills/okr` invokes `budget` during project OKR derivation.
2. CEO infers size class from scope + brief; if ambiguous, ask user in the commit phase of the user-meeting.
3. Write `_vision/projects/<slug>.md > ## Budget` with:
   - Total tokens / Total $
   - Per-phase allocation (defaults or declared override)
   - Size class
   - Any ADR references (for overrides)
4. File ADR for any non-default override.

## Process (track)

1. After every Chief report, append a burn entry to `<slug>/chat.jsonl`:
   ```jsonl
   {"ts":"<iso>","scope":"budget","kind":"burn","phase":"build","taskId":"t-NNNN","tokens":N,"costUSD":X.XX}
   ```
2. Update `<slug>/status.json > metrics`.
3. If threshold tripped, `budget-monitor` emits a flag — CEVO decides yellow-yellow-surface vs red-ladder-climb.

## Process (account-at-close)

1. `budget-monitor` writes `<slug>/eval/budget-ledger.md` with per-phase breakdown + forecast-vs-actual delta.
2. Budget-ledger is part of the close-eval artifact set (CEVO owns), and its findings feed into the CEVO close-eval gate.
3. Any overrun files an ADR in the same CEO close turn.

## Invariants

- Budgets are per-project, not per-agent. Agents consume from the project budget.
- Phase allocation is declared, not inferred. An un-declared phase inherits the default.
- No silent budget change. Every modification files an ADR.
- Overruns surface, never hide. `budget-monitor` cannot normalise away a breach.
- Rung 6 (user consult) is the only rung that can expand a budget. Rungs 0–5 can only operate within declared budget.

## Integration

- **`okr`** — budgets derive at project OKR derivation.
- **`eval`** — close-eval gate factors in overrun severity.
- **`adr`** — every override + every overrun files an ADR.
- **`ladder`** — budget red routes to Rung 6 per `ladder-matrix.md`.
- **`audit`** — CAO cross-checks that every overrun has a matching ADR.
- **`capacity`** — utilization bands factor into budget-class defaults (large = burn-heavy = higher class floor).

## Progressive disclosure

- `references/cost-table.md` — per-model $/M-token rates used to convert token burn to $.
- `references/size-class-calibration.md` — how to classify a project at intake + examples.

## What this skill is not

- Not a real-time meter. Burn is accumulated on Chief reports, not on every model call.
- Not a hard stop. Over-budget is a recommendation + ADR, not a blocker.
- Not a replacement for `capacity`. Capacity tracks agent utilization across the portfolio; budget tracks a project's spend.
- Not applicable pre-Wave 5 projects. Backfill budgets are optional but recommended.
