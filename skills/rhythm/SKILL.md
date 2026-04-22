---
name: rhythm
description: Agency cadence orchestrator. Invoked by CEO at session start to check which daily/weekly/monthly/quarterly heartbeats are due and run them in order. Also callable on-demand via /devsecops-agency:rhythm. Reads _vision/rhythm/state.json, compares against today, writes heartbeat-<date>.md / weekly-<week>.md / monthly-<month>.md / quarterly-<quarter>.md, updates state on pass, increments degradedCount on fail. Pairs with RHYTHM.md (spec) and skills/career-ladder (quarterly promotion step). Bootstrap on first run — null state.json means run daily, plus any cadence whose natural trigger has already passed.
metadata:
  version: "0.1.0"
---

# rhythm

## When to trigger

- CEO session start (every turn that opens a new session — read RHYTHM.md identity step, then invoke this skill).
- `/devsecops-agency:rhythm` on-demand.
- Manual by COO or CAO when a heartbeat is suspected missed.

## Inputs

- `_vision/rhythm/state.json` — last-run timestamps + degradedCount. If missing, bootstrap.
- Current UTC date/time (from `date` or session metadata).
- `RHYTHM.md` — the spec. Canonical source of trigger rules and pass criteria.

## Outputs

- One file per due heartbeat, in the paths listed in `RHYTHM.md`.
- Updated `_vision/rhythm/state.json` (pass) OR incremented degradedCount (fail).
- `notify` event per completed heartbeat (`heartbeat-daily` / `heartbeat-weekly` / `heartbeat-monthly` / `heartbeat-quarterly`).
- Optional ADR if the heartbeat escalates (e.g., missed-quarterly auto-ADR).

## Process

1. **Read state.** Load `_vision/rhythm/state.json`. If missing, go to bootstrap (step 7).
2. **Compute due set.** Compare today against `lastDaily`/`lastWeekly`/`lastMonthly`/`lastQuarterly`. Apply RHYTHM.md trigger rules (first CEO turn of day / Monday / first Monday of month / first Monday of quarter, plus window overrides). Produce an ordered due list.
3. **Sort due set.** Always run in order: daily → weekly → monthly → quarterly. A quarterly run does not replace the day's daily — run both.
4. **Run each heartbeat.** See `references/cadences.md` for the input-read + output-write contract per cadence. Each heartbeat returns `{status: pass | degraded, artifactPath, summary}`.
5. **Update state.** On `pass`, update the corresponding `last*` field and reset its degradedCount. On `degraded`, leave `last*` alone and increment degradedCount.
6. **Escalate on repeated degrade.** If any cadence's degradedCount hits 2, file ADR `kind: rhythm-degraded` and add a `Rung 2` ladder entry. If degradedCount hits 3, escalate to Rung 3 (blocking-council red).
7. **Bootstrap branch.** Create `_vision/rhythm/state.json` with all `last*` = null. Run daily. Then run any cadence whose "natural trigger has already passed" — e.g., install on a Wednesday means weekly is due immediately; install on day > 1 of the month means monthly is due; install in mid-quarter means quarterly is due with `status: bootstrap`.
8. **Return.** Write a 1-line summary per heartbeat run, in order, to session log. Pass back to CEO for its session-start handoff.

## Cadence details

See `references/cadences.md` for the input-read + output-write contract per cadence. See `references/missed-heartbeat.md` for the escalation tree when a heartbeat misses its window.

## Pairings

- **`skills/ceo`** — invokes this skill at session start, immediately after the MISSION+VALUES+LESSONS identity read.
- **`skills/career-ladder`** — invoked by the quarterly heartbeat as one of its sub-steps.
- **`skills/keeper-test`** — invoked by the quarterly heartbeat as its primary sub-step.
- **`skills/eval`** — invoked by the quarterly heartbeat to freeze the regression baseline.
- **`skills/compliance-drift`** — invoked by the monthly heartbeat.
- **`skills/notify`** — event surface on every heartbeat.

## Anti-patterns

- Don't run a heartbeat out of order (e.g., weekly before daily on the same turn).
- Don't skip a heartbeat just because the day's workload looks light. The empty heartbeat file is itself the receipt.
- Don't backfill a missed heartbeat by dating the file in the past. `closedAt` = now; the miss is a separate row.
- Don't merge two cadences into one file (weekly+monthly same day → separate files).
- Don't edit `MISSION.md` / `VALUES.md` / `KEEPER-TEST.md` from a heartbeat. Those are quarterly-and-user-gated.
- Don't run this skill inside a non-CEO session. Other agents read heartbeat files; they don't write them.
