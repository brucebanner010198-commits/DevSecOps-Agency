# rhythm/references/cadences.md

Per-cadence input-read + output-write contract. Parsed by `skills/rhythm/SKILL.md` step 4.

## 1. Daily

**Trigger.** `lastDaily` is null OR `lastDaily < today (UTC)`.

**Inputs.**

| Read | Purpose |
| --- | --- |
| `inbox.json` (per active project) | Parked questions needing next-turn |
| `_tasks/*.jsonl` | Stale-task filter: `updatedAt < now - 72 h` AND `status ∈ {pending, in_progress, blocked}` |
| `_sessions/**/latest.jsonl` | Last entry per agent; silent-agent filter |

**Output file:** `_vision/rhythm/heartbeat-<YYYY-MM-DD>.md`.

**Format:**

```markdown
# heartbeat-<YYYY-MM-DD>.md

- **Kind:** daily
- **Opened:** <ISO-8601 timestamp>
- **Status:** pass | degraded

## Inbox (<N>)

- [ ] <project> / <inbox-id> — <1-line summary> → next-turn: <agent>
- ...

## Stale tasks (<N>)

| Task | Project | Owner | Last update | Age |

## Silent agents (<N>)

| Agent | Council | Last entry | Project status |

## Due-today heartbeats

- weekly: yes / no
- monthly: yes / no
- quarterly: yes / no

## Notes

<free-form 1–3 bullets>
```

**Pass criteria.** Inbox empty OR every row has a next-turn assignment; no stale task > 7 d; no silent agent on `active` project > 48 h.

**Degraded.** If `inbox.json` can't be read or `_sessions` scan errors, write heartbeat with `Status: degraded` and the error verbatim in Notes.

---

## 2. Weekly

**Trigger.** `lastWeekly` is null OR `today` is Monday (UTC) OR `today - lastWeekly >= 7 d`.

**Inputs.**

| Read | Purpose |
| --- | --- |
| `_vision/roster/performance-<latest>.md` | Rolling agent health |
| `skills/capacity/state.json` | Utilization bands |
| `_vision/idea-pipeline/top-5.md` | Top-of-backlog |
| Every project where `status.project.state ∈ {active, blocked, parked}` | Portfolio roll-up |

**Output file:** `_vision/rhythm/weekly-<YYYY-WW>.md` (ISO-8601 week).

**Format:**

```markdown
# weekly-<YYYY-WW>.md

- **Kind:** weekly
- **Week:** <YYYY-WW>
- **Opened:** <ISO-8601>
- **Status:** pass | degraded

## Portfolio status

| Project | Phase | Gate | Blocked? | Age |

## Capacity heatmap

| Council | Util % | Band | Flag |

## Top-of-backlog

1. <idea> — <1-line>
2. ...
3. ...

## Escalations

- Parked > 7 d: <project> — <ladder rung>

## Audit flags

- Open CAO finding: <count> (<high/med/low breakdown>)

## Decisions needed

- [ ] <decision> — owner: <agent> — by: <date>
```

**Pass criteria.** No project blocked > 14 d without Rung-3+ ADR; no council > 100 % for 2 consecutive weeks; top-5 refreshed ≤ 30 d ago.

**Degraded.** Missed > 3 d → CAO compliance-drift (yellow). Missed > 7 d → breach (red).

---

## 3. Monthly

**Trigger.** `lastMonthly` is null OR `today` is first Monday of month OR `today - lastMonthly >= 32 d`.

**Inputs.**

| Read | Purpose |
| --- | --- |
| `skills/compliance-drift/state.json` | Last sweep |
| `_vision/audit/portfolio-<latest>.md` | CAO portfolio audit |
| `_vision/idea-pipeline/{raw,screened,ranked,top-5}.md` | Funnel throughput |
| `_memory/MEMORY.md` | Light memory additions this month |
| `_budgets/*.json` | Budget burn |
| `_vision/red-team/findings.md` | Open red-team findings |

**Output file:** `_vision/rhythm/monthly-<YYYY-MM>.md`.

**Format:**

```markdown
# monthly-<YYYY-MM>.md

- **Kind:** monthly
- **Month:** <YYYY-MM>
- **Opened:** <ISO-8601>
- **Status:** pass | degraded

## Compliance drift

| Framework | Yellow | Red | Last sweep |

## Portfolio audit rollup

<1–3 bullets from CAO portfolio audit; cite file>

## Idea-pipeline throughput

| Stage | In | Out | Conversion % |

## Light memory additions

<count + 3 highest-novelty pattern titles with paths>

## Budget burn

| Size class | Cumulative % | Flag |

## Red-team findings

| Severity | Open | Closed this month | Oldest open age |

## Actions for next month

- [ ] ...
```

**Pass criteria.** Compliance-drift sweep ran in-month; no red-team high+ open > 30 d; budget cumulative ≤ 110 %.

**Degraded.** Missed monthly = automatic CAO red + `inbox.json` entry `kind: missed-monthly-heartbeat`.

---

## 4. Quarterly

**Trigger.** `lastQuarterly` is null OR `today` is first Monday of Q (Jan/Apr/Jul/Oct) OR `today - lastQuarterly >= 95 d`.

**Sub-skill invocations (run in order).**

1. `skills/keeper-test` — full review of all non-reserved agents. Produces `_vision/roster/performance-<date>.md`.
2. `skills/career-ladder` — reads latest + last-3 performance files; writes `_vision/roster/levels-<date>.md`.
3. `skills/eval` — freeze regression baseline: snapshot SHA → `_baselines/<YYYY-Q>.md`.
4. Mission/values alignment read — scan this-quarter projects for non-goal violations (file ADR `kind: non-goal-drift` per hit).
5. Lessons-ledger mining — group rows by pattern; surface top 3 cross-project lessons.

**Inputs.**

| Read | Purpose |
| --- | --- |
| All `performance-<date>.md` in quarter | Rollup |
| `_vision/roster/levels-<latest>.md` | Promotion moves |
| `skills/eval/baseline-<prev>.md` | Regression comparison |
| `MISSION.md` + `VALUES.md` | Drift indicators (read-only) |
| `LESSONS.md` | Quarter's rows only |

**Output file:** `_vision/rhythm/quarterly-<YYYY-Q>.md` (plus sub-skill outputs).

**Format:**

```markdown
# quarterly-<YYYY-Q>.md

- **Kind:** quarterly
- **Quarter:** <YYYY-Q>
- **Opened:** <ISO-8601>
- **Status:** pass | degraded | bootstrap

## Keeper Test rollup

| Agent | Rating | Δ from last quarter |

## Career-ladder moves

| Agent | L prior → L now | ADR |

## Eval regression baseline

- **Frozen SHA:** <git-sha>
- **Frozen at:** <ISO-8601>
- **Baseline file:** `_baselines/<YYYY-Q>.md`

## Mission alignment

- Non-goal violations found: <count> + list (each with ADR ref)

## Values compliance

| Principle | Citations this quarter | Violations |

## Lessons mining

1. <cross-project pattern> — cited in <rows>
2. ...
3. ...

## Portfolio health

<1–3 bullets>

## OKR rollup

| OKR | Target | Actual | Status |

## Next-quarter thesis

<1 paragraph>
```

**Pass criteria.** All 5 sub-skills ran; every red agent has a disposition (upgrade / repurpose / fire-proposal-to-user); ≥ 1 cross-project lesson surfaced when `LESSONS.md` has ≥ 3 rows for the quarter.

**Degraded.** Missed quarterly = CAO red + blocks new-project acceptance until it lands.
