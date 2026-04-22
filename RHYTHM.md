# RHYTHM

> The agency's operating tempo. What runs daily, weekly, monthly, quarterly; who owns each heartbeat; where the artifact lives; what happens when a heartbeat is missed.

One-sentence summary: **the paper trail has a pulse, and the CEO reads it at session start.**

Read by: `skills/ceo/SKILL.md` session-start step; `skills/rhythm/SKILL.md` orchestrator; CAO close-audit; user on `/devsecops-agency:status`.

---

## The four cadences

| Cadence | Period | Heartbeat | Owner | Artifact path |
| --- | --- | --- | --- | --- |
| **Daily** | 24 h | inbox triage + stale-task sweep | CEO | `_vision/rhythm/heartbeat-<YYYY-MM-DD>.md` |
| **Weekly** | 7 d | portfolio status + capacity check + top-of-backlog review | CEO + COO | `_vision/rhythm/weekly-<YYYY-WW>.md` |
| **Monthly** | 30 d | compliance-drift sweep + portfolio audit read + idea-pipeline refresh | CAO + CPO | `_vision/rhythm/monthly-<YYYY-MM>.md` |
| **Quarterly** | 90 d | Keeper Test + eval regression baseline freeze + values/mission review | COO + CEVO + user | `_vision/rhythm/quarterly-<YYYY-Q>.md` |

Session-level rhythm (open = read MISSION+VALUES+latest 5 LESSONS rows; close = retrospective + lessons-ledger) is already wired in v0.3.8 and is not duplicated here.

---

## 1. Daily heartbeat

**Trigger.** First CEO turn of the calendar day (UTC).

**Inputs read.**

- `inbox.json` — all parked questions across active projects.
- `_tasks/*.jsonl` — every open task, filtered by `updatedAt < now - 72 h` → stale list.
- `_sessions/**/latest.jsonl` — last entry per agent; agents with no entry in the last 24 h while their project is `status: active` are flagged.

**Outputs written.**

- `_vision/rhythm/heartbeat-<YYYY-MM-DD>.md` — 5 sections: Inbox / Stale tasks / Silent agents / Due-today heartbeats (any weekly/monthly/quarterly also due) / Notes.
- `notify` event `heartbeat-daily` with 1-line summary.

**Pass criteria.** Inbox is empty OR every entry has an assigned next-turn; no stale task older than 7 d; no silent agent on an `active` project older than 48 h.

**Failure mode.** If the CEO cannot read `inbox.json` (file missing / malformed), the heartbeat is written with `status: degraded` and the next CEO turn re-tries. Two consecutive degraded heartbeats → CAO red and Rung-2 ladder entry.

---

## 2. Weekly heartbeat

**Trigger.** First CEO turn on or after Monday 00:00 UTC, or when the last weekly heartbeat is ≥ 7 d old.

**Inputs read.**

- `_vision/roster/performance-<latest>.md` — rolling agent health.
- `skills/capacity/state.json` — per-agent + per-council utilization bands.
- `_vision/idea-pipeline/top-5.md` — current shortlist.
- All projects with `status ∈ {active, blocked, parked}`.

**Outputs written.**

- `_vision/rhythm/weekly-<YYYY-WW>.md` — 6 sections: Portfolio status (project → phase → gate) / Capacity heatmap / Top-of-backlog (next 3 ideas) / Escalations (parked > 7 d) / Audit flags (open CAO findings) / Decisions-needed.
- `notify` event `heartbeat-weekly` with the Decisions-needed count.

**Pass criteria.** No project blocked > 14 d without a Rung-3+ ladder entry; no council over 100 % utilization for 2 consecutive weeks; top-5 shortlist has been refreshed in the last 30 d.

**Failure mode.** If the weekly misses its window by > 3 d, CAO files a compliance-drift (yellow); > 7 d is a breach (red).

---

## 3. Monthly heartbeat

**Trigger.** First CEO turn on or after the first Monday of the calendar month, or when the last monthly is ≥ 32 d old.

**Inputs read.**

- `skills/compliance-drift/state.json` — last sweep timestamp.
- `_vision/audit/portfolio-<latest>.md` — CAO portfolio audit findings.
- `_vision/idea-pipeline/raw.md` + `screened.md` — current idea funnel.
- `_memory/MEMORY.md` — light memory patterns added this month.

**Outputs written.**

- `_vision/rhythm/monthly-<YYYY-MM>.md` — 7 sections: Compliance drift (yellow / red count) / Portfolio audit rollup / Idea-pipeline throughput (raw→screened→ranked→top-5 conversion) / Light memory additions / Budget burn (by size class) / Red-team findings (open / closed) / Actions-for-next-month.
- `notify` event `heartbeat-monthly`.

**Pass criteria.** Compliance-drift sweep has been run in-month; no red-team `high+` finding open > 30 d; budget burn ≤ 110 % cumulative (any project above triggers Rung 6).

**Failure mode.** A missed monthly is an automatic CAO red and escalates to user via `inbox.json` with `kind: missed-monthly-heartbeat`.

---

## 4. Quarterly heartbeat

**Trigger.** First CEO turn on or after the first Monday of each calendar quarter (Jan / Apr / Jul / Oct), or when the last quarterly is ≥ 95 d old.

**Inputs read.**

- Every `performance-<date>.md` in the quarter.
- `_vision/roster/levels-<latest>.md` — current career-ladder state.
- `skills/eval/baseline-<prev-quarter>.md` — prior regression baseline.
- `MISSION.md` + `VALUES.md` — checked for drift indicators (not edited).
- `LESSONS.md` — quarter's rows only.

**Outputs written.**

- `_vision/rhythm/quarterly-<YYYY-Q>.md` — 9 sections: Keeper Test rollup (per agent) / Career-ladder moves (promotions this quarter) / Eval regression baseline freeze (SHA + date) / Mission alignment review (any non-goal violations found?) / Values-compliance report / Lessons-ledger mining (top 3 cross-project patterns) / Portfolio health / OKR rollup / Next-quarter thesis.
- `_meetings/keeper-test-<YYYY-Q>.md` (linked from Keeper Test skill).
- `notify` event `heartbeat-quarterly` + user-meeting request in `inbox.json` if promotion-between-tiers is on the table (USER-ONLY per VALUES §10).

**Pass criteria.** Keeper Test ran; baseline froze; every red-rated agent got a disposition (upgrade / repurpose / fire-proposal); ≥ 1 cross-project lesson surfaced if `LESSONS.md` has ≥ 3 rows for the quarter.

**Failure mode.** A missed quarterly is an automatic CAO red AND blocks all new-project starts until the heartbeat lands. CEO cannot accept a new brief under `/devsecops-agency:ceo` while quarterly is > 100 d old — the user is told the heartbeat must land first.

---

## Heartbeat state

Persisted at `_vision/rhythm/state.json`:

```json
{
  "lastDaily":     "2026-04-21",
  "lastWeekly":    "2026-W17",
  "lastMonthly":   "2026-04",
  "lastQuarterly": "2026-Q1",
  "degradedCount": { "daily": 0, "weekly": 0, "monthly": 0, "quarterly": 0 }
}
```

Read by `skills/rhythm` to compute which heartbeats are due on any given CEO turn. Updated only on pass; a degraded heartbeat does not update `last*` but does increment `degradedCount`.

---

## Bootstrap

At v0.3.9 ship-date the agency has no rhythm history. First CEO turn after install:

1. Write `_vision/rhythm/state.json` with all four `last*` set to `null`.
2. Run the daily heartbeat first (cheapest, always due).
3. Run any other heartbeats whose natural trigger has already passed (e.g., if install is on a Wednesday, weekly is due immediately).
4. Monthly and quarterly bootstrap with `status: bootstrap` tags — they do the read-portion but skip the "compare to last quarter" analytics until a second monthly/quarterly exists.

---

## Anti-patterns

- Don't skip a heartbeat because "nothing changed" — the empty heartbeat file is itself the receipt that the cadence is being respected.
- Don't backdate a missed heartbeat to make the window look full. Missed = missed; file a `compliance-drift` row and move on.
- Don't merge two cadences into one file (e.g., weekly+monthly on the same day). Separate files, separate receipts, separate audit trails.
- Don't let a degraded heartbeat silently re-try forever. Two consecutive degrades on the same cadence → escalate.
- Don't edit `MISSION.md` or `VALUES.md` inside a daily/weekly/monthly heartbeat. Those are quarterly-only changes and require a user-meeting.
