# band-rules.md — capacity bands + edge cases

## Band formulas

**Per-agent, 30-day window:**

```
band = match dispatches_30d:
  0       → idle
  1..2    → low
  3..7    → healthy
  8..14   → hot
  > 14    → overloaded
```

**Per-Chief, 30-day window:**

```
band = match dispatches_30d:
  0..3    → idle
  4..20   → healthy
  21..40  → hot
  > 40    → overloaded
```

A Chief's dispatches = outbound Task tool calls (to specialists or peer Chiefs). Inbound (CEO dispatching the Chief) does not count — that's the CEO's rate.

**CEO** is always `n/a`. The CEO's rate is a derived agency aggregate, not a personal band.

## New-hire probation

Agents active < 30 days are tagged `probation` instead of a band. Probation rules:

- No fire proposal on a probation agent regardless of utilization.
- Probation agents skip the `idle` flag even if 0 dispatches — they may not have been offered work yet.
- Probation is lifted automatically at day 31.

## Specialist vs niche role

Some specialists are legitimately `low` or `idle` by design — e.g., `pen-tester` may run once per project, `license-checker` once per legal review. `hiring-lead` checks scope-expected cadence before flagging idle. Cadence hints:

| Agent pattern                      | Expected band |
| ---------------------------------- | ------------- |
| Per-project, always-called         | healthy       |
| Per-project, optional-called       | low–healthy   |
| Portfolio-only (CSO specialists)   | low           |
| Per-quarter (auditors on close)    | low–healthy   |
| On-incident (red-team, to-be-Wave-6) | idle acceptable |

Idle for 3+ quarters with no on-incident invocation = fire candidate regardless of pattern.

## Council-level parallel utilization

```
parallel_util = parallel_dispatches / total_dispatches
```

Compare to `worktree/references/parallel-matrix.md` allowance:

- If matrix allows ≥ 50 % parallel and actual < 30 % → yellow flag (throughput left on the table).
- If matrix allows 100 % parallel (e.g., Audit Council always parallel) and actual < 80 % → red flag (process bug, not capacity).
- If actual > matrix allows → red flag (invariant violation — report to CAO).

## Coverage gap handling

When a KR is flagged uncovered:

1. Check if any currently-queued project's brief targets the KR. If yes → not a gap.
2. Check if KR is marked `status: paused` in `_vision/VISION.md`. If yes → not a gap.
3. Otherwise → true gap.

True gaps have three remediation paths (CEO chooses, ADR mandatory):

- **Hire**: new specialist covering the domain.
- **Repurpose**: existing agent's scope widens.
- **Retire KR**: if the KR is no longer strategic, supersede it in the next quarter roll-up.

Gap left uncovered for > 60 days escalates to user via CEO.

## Deterministic output

All lists in capacity output (overloaded agents, idle agents, bottleneck flags) sort:

- Alphabetical for names (stable prompt-cache key).
- Descending for numeric bands within a section (overloaded before hot before healthy).
- Bands themselves ordered overloaded → hot → healthy → low → idle → probation (risk-first).
