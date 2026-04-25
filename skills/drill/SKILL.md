---
name: drill
description: Scheduled + on-demand resilience drills that exercise failure modes from RESILIENCE.md end-to-end. Distinct from skills/chaos (per-service fault injection) — drills cover chief-unavailable, heartbeat-miss, model-outage, waiver-expiry, compaction-loss at the agency level. 5 drill kinds on 4 cadences (monthly / quarterly / annual / on-demand). Every drill files a `drill-report` ADR with outcome + gaps + remediation. Missed drills are CAO reds. Never runs during a live incident affecting the same subsystem.
metadata:
  version: "0.1.0"
---

# drill

## When to trigger

- Monthly: chief-unavailable drill (scheduled by rhythm monthly heartbeat, first business day of the month).
- Quarterly: heartbeat-miss drill + model-outage drill (scheduled by rhythm quarterly heartbeat, in the first two weeks of the quarter).
- Annually: waiver-expiry drill + compaction-loss drill (scheduled by rhythm annual check; typical slot = week 2 of Q1).
- On-demand: by CEO or blocking-council chief in response to a near-miss. ADR `kind: drill-ondemand` must cite the near-miss incident.

Drills never run during a live incident affecting the same subsystem — the real path is the test. Rhythm daily heartbeat checks for active incidents before invoking any scheduled drill.

## Inputs

- `RESILIENCE.md` — failure-mode map. Every drill kind corresponds to one row.
- `_vision/rhythm/state.json` — current degraded-mode set. If ≥ 1 degraded mode overlaps the drill subsystem, reschedule.
- Per-drill config in `references/<kind>.md`.

## Outputs

- `_decisions/ADR-NNNN-drill-report-<kind>-<YYYY-MM-DD>.md` — always, success or fail.
- `_vision/drills/<kind>/<YYYY-MM-DD>.md` — detailed run log with timestamps, observations, gap list.
- `notify` event `drill-<kind>-<outcome>` — rate-limited.

## Process (common)

1. **Pre-flight.** Read `_vision/rhythm/state.json`. If any degraded-mode flag overlaps the drill subsystem (e.g., model-outage drill when model-degraded is active), skip with ADR `kind: drill-skipped` citing reason.
2. **Announce.** Post a drill-start event to notify. The announcement includes a "this is a drill" banner visible to every agent invoked during the drill window.
3. **Execute.** Run the drill kind's specific procedure (see `references/<kind>.md`). Drills are time-boxed — monthly ≤ 30 min, quarterly ≤ 2 h, annual ≤ 1 business day.
4. **Observe.** Record every failure-mode response event, recovery time, ADR landing time, and paper-trail gap.
5. **Classify outcome:**
   - **Pass** — every expected ADR landed, recovery time within window, paper trail complete.
   - **Pass with gaps** — recovery within window but paper trail has gaps or ADRs landed late.
   - **Fail** — recovery exceeded window OR expected ADRs missing OR agency entered an unplanned degraded mode.
6. **Write drill-report ADR.** Cite outcome, recovery time, gap list, remediation commitments. Remediation gaps become `kind: drill-followup` ADRs with owners + due dates.
7. **Notify + archive.** Emit event; archive run log at `_vision/drills/<kind>/<YYYY-MM-DD>.md`.

## The five drill kinds

### 1. Chief-unavailable drill (monthly)

Pick a non-blocking Chief (never CISO, CEVO, CRT, CAO — they're always live). Simulate unavailability: their persona's `model:` tier flipped to `unavailable` for 30 minutes; their council lead takes their role in any scheduled dispatch; measure recovery.

**Pass criteria:**
- Council lead picks up the Chief's responsibilities within 10 minutes.
- Any scheduled dispatch through that Chief routes through the lead or files a `chief-unavailable` ADR citing the drill.
- `heartbeat-<date>.md §Degraded` shows `chief-degraded: <name>` during the drill window.

### 2. Heartbeat-miss drill (quarterly)

Intentionally skip one daily heartbeat. Verify rhythm catch-up mode the next day.

**Pass criteria:**
- The next-day heartbeat contains a `catch-up` entry for the skipped day.
- `state.json` reflects `degradedCount.daily: 1` then back to 0 after catch-up lands.
- No `heartbeat-missed` ADR fires on the first miss (per missed-heartbeat escalation tree); the compliance-drift yellow does fire.

### 3. Model-outage drill (quarterly)

Temporarily block primary model vendor for one specialist (config-level, not real outage). Verify `model-routing` lateral swap.

**Pass criteria:**
- `model-outage-open` ADR files within 5 minutes of detection.
- Specialist's next output is tagged `model: degraded`.
- Primary restored → `model-outage-close` ADR files within 5 minutes.

### 4. Waiver-expiry drill (annually)

Grant a synthetic waiver with a 24-hour expiration on a pre-remediated synthetic finding. Verify the expiry-day flow.

**Pass criteria:**
- Expiry-day rhythm heartbeat detects the row.
- `waiver-expiry` ADR files with `outcome: remediated` (since the finding was pre-remediated).
- Row moves from `_vision/waivers/active.md` to `history.md`.

### 5. Compaction-loss drill (annually)

For one non-reserved specialist, simulate session-log loss: `_sessions/<agent>/<latest>.jsonl` moved aside for 1 hour. Verify the agent can recover from paper trail alone.

**Pass criteria:**
- Agent re-dispatched during the drill window produces output consistent with pre-loss behaviour.
- Paper-trail reads (ADRs, memory, LESSONS, session-log predecessors) are sufficient.
- Post-drill, the moved-aside session-log is restored — the drill is non-destructive.

## Chaos game days (added v0.5.6 wire-through)

Drills above exercise **named failure modes from `RESILIENCE.md > Failure-mode map`** — known unknowns. Chaos game days exercise **failure modes that aren't on the map** — unknown unknowns. They are quarterly, end-to-end, and require a written hypothesis.

**Cadence.** One game day per quarter. Q2's game day is fixed to the slot two weeks before the trust-scorecard publish (so findings can be cited in the scorecard). Game-day participation is mandatory for the chiefs of any council whose subsystem is in the test scope.

**Procedure (per `RESILIENCE.md > Chaos engineering`):**

1. **Hypothesis (written, before any injection).** What do we expect to happen when X breaks? Without a hypothesis we can't tell signal from noise.
2. **Blast radius.** Define `first-to-fail` (the targeted component), `secondary-cone` (collateral that's allowed to fail), and `no-go set` (what MUST NOT fail). The no-go set is non-negotiable.
3. **Steady-state metric.** Pick the one user-facing metric that proves "system healthy now." Read it before, during, after.
4. **Inject.** Smallest perturbation that tests the hypothesis. Network partition between two services, not whole-region failure. Latency at p99 only, not on every request.
5. **Observe + classify.** Reality vs hypothesis. Match → confirmed property documented. Mismatch → file `chaos-finding` ADR with severity.
6. **Recover + blameless post-mortem.** Always recover before the time-box expires. The post-mortem follows the same blameless rules as `RESILIENCE.md > Drills` post-mortems.

**Pass criteria:**

- Written hypothesis filed before injection.
- No-go set was not breached during or after injection.
- Steady-state metric returned to baseline within the documented recovery window.
- Either the property was confirmed (no surprises) or a finding ADR was filed (surprise documented).
- Post-mortem published within 7 days, blameless, with at least one corrective-action stepping stone.

**Independence (same as drills):** the chaos game day for a subsystem CANNOT be run by the council that owns that subsystem. CSRE rotates the lead role across COO / CRT / CAO so no single council is always the disruptor.

**Outputs:**

- `_decisions/ADR-NNNN-chaos-gameday-<YYYY-MM-DD>.md` — always.
- `_decisions/ADR-NNNN-chaos-finding-<slug>.md` — one per finding.
- `_vision/chaos/<YYYY-QN>.md` — full game-day log (hypothesis, blast radius, steady-state metric, injection, observation, recovery, post-mortem links).

## Independence

`drill` cannot be run by the same council as the subsystem being drilled. Model-outage drill is run by CSRE's drill specialist; chief-unavailable drill is run by COO's drill specialist. This parallels red-team independence rules.

## Interaction with other skills

| Skill | How drill composes |
| --- | --- |
| `rhythm` | Schedules + gates drills. Daily/monthly/quarterly/annual triggers live here. |
| `chaos` | Complementary, not overlapping. Chaos = per-service fault injection; drill = end-to-end agency resilience. |
| `ladder` | A failed drill escalates via Rung 3 (material decision → drill-followup ADR). |
| `audit` | CAO spot-checks drill cadence + gap-list coverage quarterly. |
| `waivers` | Waiver-expiry drill exercises `skills/waivers/` directly. |
| `model-routing` | Model-outage drill exercises this skill's swap behaviour. |
| `career-ladder` | Drill gaps attributable to an L3 agent's council count toward L3 demotion if ≥ high severity. |

## Anti-patterns

- Don't skip a scheduled drill. Missed drill = CAO red. Reschedule, don't skip.
- Don't drill during a live incident. Pause the drill schedule; resume after the incident closes.
- Don't drill the same subsystem two months in a row (monthly drill rotation — chief-unavailable cycles through the 12 non-blocking chiefs).
- Don't mark a drill `pass` when paper-trail gaps exist. Use `pass-with-gaps` — each gap files a followup ADR.
- Don't treat a drill as a real incident for postmortem purposes. Drills have their own report format; retrospectives are for real incidents.
- Don't run a drill that has no pass/fail criteria. Every drill kind has explicit pass criteria above; unclear criteria = don't run.
- Don't drill a USER-ONLY path without user consent. If the drill requires the user to respond (e.g., fake user-meeting for waiver-expiry drill), pre-announce and get consent.
- Don't let the same agent drill the same subsystem twice in a calendar year. Fresh eyes catch different gaps.

See `references/chief-unavailable.md`, `references/heartbeat-miss.md`, `references/model-outage.md`, `references/waiver-expiry.md`, `references/compaction-loss.md` for per-kind protocols.
