# RESILIENCE.md

One-sentence tagline: **things fail; the agency degrades, recovers, and writes down what it learned — never silently, never without a receipt.**

Unifies the failure-mode map across the agency. Nothing here is new behaviour — it's the map that tells the CEO, on a red day, which existing skill to reach for. Every row cites a concrete skill + ADR kind + expected recovery window.

## Failure-mode map

| Failure mode | Detected by | First response | Escalation path | Skill(s) | ADR kind |
| --- | --- | --- | --- | --- | --- |
| Model vendor outage (primary down) | `model-routing` health probe | Same-tier lateral swap | Opening + closing ADRs per override; CSRE brief in weekly heartbeat | `model-routing` | `model-outage-open` / `model-outage-close` |
| Tool vendor outage (MCP server down) | tool health probe | Disable tool, queue dependent tasks | Tool-scout verdict + CSRE brief; if > 24h, idea-pipeline gates projects that need it | `tool-scout`, `model-routing` | `tool-outage-open` / `tool-outage-close` |
| Fix loop exceeds cap | `taskflow` | Ladder Rung 1 → Rung 2 | Each rung files ADR; max = Rung 7 (parking, user-approved) | `ladder`, `taskflow` | `rung-transition` |
| Blocking-council red on ship | gate aggregation | Stop ship; propose waiver OR fix | Waiver = user-only; fix = re-run gate | `waivers`, `gates` | `waiver-grant` / `waiver-deny` / gate-fix ADR |
| Keeper-Test red at L3 | quarterly keeper-test | Immediate L3 → L2 demotion | `career-demotion` ADR; agent keeps task under L2 privs | `career-ladder`, `keeper-test` | `career-demotion` |
| Missed daily heartbeat | rhythm state check | Catch-up heartbeat with `mode: catch-up` | 1st = yellow `compliance-drift`; 2nd = ADR + Rung 2; 3rd = Rung 3 | `rhythm` | `heartbeat-missed` |
| Missed quarterly heartbeat | rhythm state check | Skip-forward note citing gap | Blocks new project acceptance until caught up | `rhythm` | `heartbeat-missed` |
| Append-only violation (file mutation) | `audit` close-audit + runtime hooks | Immediate CAO red; stop merge | ADR + revert via new file; re-fire on next detection | `audit`, `adr`, `memory` | `integrity-violation` |
| Raw secret in artifact | `secrets-vault` scan, runtime hook | Same-turn rotation + red | CISO red; no ship until rotation confirmed | `secrets-vault` | `secret-leak` |
| Prompt-diff review rejection | `playbook` prompt-diff | Auto-rollback persona edit | Re-propose with a new stepping-stone covering the weakening | `playbook`, `roster` | `prompt-diff-reject` |
| Red-team critical finding on production artifact | `red-team` | Stop-the-line; CRT owns remediation | User-only waiver if ship-pressure; else fix + re-scan | `red-team`, `waivers` | `red-team-finding` |
| Eval regression > 5 pp | `eval` post-close | Root-cause + revert OR new baseline ADR | Baselines freeze at quarter boundary; mid-quarter revisions require CEVO + user | `eval` | `eval-regression` |
| Budget burn > 110 % cumulative | `budget` per-report | Rung 6 escalation | Opening + closing ADRs; project re-scoped or parked | `budget`, `ladder` | `budget-exceeded` |
| Chief-level agent unavailable (prompt-edit failed, ADR-paused) | CEO session start | Council lead acts in Chief's role; if lead also out → escalate | User decides re-hire vs. continue-degraded | `roster`, `keeper-test` | `chief-unavailable` |
| Worker shard stuck | `fanout` aggregation | Worst-of aggregation kicks in | Re-dispatch failed shard; if 3 fails, promote to specialist-serial | `fanout`, `taskflow` | `worker-stuck` |
| User unavailable for USER-ONLY decision | `inbox.json` flag | Queue decision; continue on unblocked work | Daily heartbeat surfaces stale user-pending rows; after 7 days, Rung 5 | `ceo`, `ladder` | `user-pending` |

## Degraded modes

The agency has four explicit "degraded modes" any of which can be in effect at once:

- **Model degraded**: primary model vendor unreachable; same-tier lateral active. All outputs carry `model: degraded` tag. No new projects accepted. Close-eval runs on lateral model only (no cross-tier fallback).
- **Heartbeat degraded**: ≥ 1 cadence is behind its natural trigger. Weekly quick-summary still runs; quarterly heartbeat blocks until caught up.
- **Chief degraded**: one of the 16 chiefs has an open `chief-unavailable` ADR. Council lead acts in Chief's role; delivery paths that require the Chief's sign-off pause.
- **Budget degraded**: one or more projects are > 90 % of budget. Rung 6 triggered at 110 %; projects at 90-110 % get `degraded: budget` tag and run to close under tighter fix-loop cap.

Degraded mode is a property of the agency, not a property of the project. The daily heartbeat publishes the current degraded-mode set in `heartbeat-<date>.md §Degraded`.

## Drills

`skills/drill/` provides scheduled + on-demand resilience drills — different from `skills/chaos/` which does per-service fault injection. Drills exercise failure modes end-to-end:

- **Chief-unavailable drill** (monthly): pick a non-blocking Chief, simulate unavailability, run a planned dispatch through the council; measure recovery window + paper-trail coverage.
- **Heartbeat-miss drill** (quarterly): skip one daily heartbeat intentionally; verify catch-up mode produces correct ADR + state update.
- **Model-outage drill** (quarterly): temporarily block primary model vendor for one specialist; verify lateral swap + opening/closing ADRs.
- **Waiver-expiry drill** (annually): grant a synthetic waiver with short expiration; verify the `waiver-expiry` ADR fires and the red re-fires.
- **Compaction-loss drill** (annually): simulate session-log loss for one agent; verify the agent recovers from paper trail alone with no memory.

Drills file an ADR `kind: drill-report` with outcome + gaps + remediation. Missed drills are CAO reds.

## Recovery guarantees

The agency guarantees:

1. **No silent failure.** Every failure in the map above produces at least one ADR within the turn that detects it.
2. **No lost work.** Rung 7 parking + append-only invariants mean a project can be revived at any later date with full context.
3. **No double-decision.** Every waiver, every gate clear, every tier change files an ADR — re-litigation requires a new row, not an edit.
4. **Recovery window.** Any failure mode has a documented expected recovery window (see per-row cadence). Exceeding the window escalates one rung.
5. **Paper trail survives the agent.** If an agent is fired mid-failure-mode, their in-flight work is preserved via `_vision/roster/_archive/<name>.md` redirect + `_workers/<specialist>/*.md` retained.

## Anti-patterns

- Don't skip the drill because "we've been running fine". Untested resilience is theatre.
- Don't retire a degraded-mode tag without an explicit clear. Degraded stays degraded until closed by ADR.
- Don't "fix" a red-team finding by widening the spec. The finding goes into `_vision/red-team/findings.md` as-is; the fix is a new stepping-stone.
- Don't bypass `skills/ladder` because "this one's simple". Every rung is an ADR — the simple cases are the cheapest receipts.
- Don't let multiple degraded modes compound silently. If ≥ 2 degraded modes are active, the daily heartbeat escalates to weekly-equivalent depth.
- Don't grant a waiver that doesn't expire. Permanent waivers violate `VALUES.md §4` (append-only — a waiver must have a closing row).
- Don't run a drill during a live incident. Drills happen on quiet days; incidents use the real path.

## SLOs and error budgets (added v0.5.6 wire-through)

The Agency's pre-v0.5.6 RESILIENCE posture covered **reactive** resilience — what happens when things break (failure-mode map, degraded modes, drills, recovery guarantees). v0.5.6 layers **proactive** resilience over the top, imported from Google Cloud's Well-Architected Framework — Reliability pillar (Apache-2.0; see `LICENSES/APACHE-2.0-google-skills.txt`).

Every shipped project MUST define:

- **User-focused SLIs** (Service Level Indicators) — measure what the user actually experiences, not what the infrastructure reports. Latency p95 / p99 from the user's edge, not from inside the data center. Error rate as the user's session sees it, not as the load balancer reports.
- **SLOs** (Service Level Objectives) — the target the SLI must meet over a rolling window. Conservative target ≠ best possible; it's the threshold at which user pain begins. Common starting points: 99.5% availability over 30 days for new services; 99.9% for revenue-bearing or trust-critical paths.
- **Error budgets** — `1 - SLO` over the same window. The error budget is **the permission slip for risk-taking**: spend it on velocity (ship faster, accept more breakage), or save it (slow down, harden). When the budget burns at 2× the linear rate, freeze risky deploys; when exhausted, rollback the last risky change.

Live in `<slug>/observability/slo.md` per shipped project. Reviewed at the quarterly retrospective.

Owned by **CSRE** (acceptance criteria) and **CQO** (measurement instrumentation).

## Chaos engineering (added v0.5.6 wire-through)

Drills (above) exercise **named failure modes from the failure-mode map**. Chaos engineering exercises **failure modes that aren't on the map** — the unknowns the map doesn't cover.

The `skills/drill` skill grew a **chaos-engineering procedure** in v0.5.6 (see `skills/drill/SKILL.md` §Chaos game days). The procedure:

1. **Hypothesis.** Write down what you expect to happen when X breaks. Don't run chaos without a written hypothesis — you can't tell signal from noise without one.
2. **Blast radius.** Define what fails first, what is allowed to fail next (the secondary cone), and what MUST NOT fail (the no-go set). The no-go set is non-negotiable; if a chaos injection threatens to breach it, abort.
3. **Steady-state metric.** Pick the one metric that proves "the system is currently healthy." Read it before injection, during, after.
4. **Inject.** Smallest possible perturbation that tests the hypothesis. Network partition between two specific services, not whole-region failure (yet). Latency injection at p99 only, not on every request.
5. **Observe + classify.** Did reality match the hypothesis? If yes — note the confirmed property. If no — that's the finding. File a `chaos-finding` ADR.
6. **Recover + post-mortem.** Always recover before time-boxing expires. Always blameless post-mortem (per Google WAF reliability principle 9 — `conduct postmortems`).

Game days are quarterly (the Q2 game day for the Agency is the 2026-07-15 slot, two weeks before the trust-scorecard publish). Game-day participation is mandatory for the chiefs of any council touched by the test scope.

Owned by **CSRE**. Independence rule (per Drills section above): the chaos game day for a subsystem CANNOT be run by the council that owns that subsystem.

## Interaction with other root docs

- `MISSION.md` non-goal "not a speed demon" — resilience over velocity when they conflict.
- `VALUES.md §5` (never give up below Rung 7) — resilience is the positive form of this value.
- `VALUES.md §4` (append-only) — waivers, drills, recoveries all append; nothing edits the past.
- `KEEPER-TEST.md` — repeated failures by the same agent show up in Axis 1 (gate hit rate) + Axis 4 (values compliance).
- `CAREER.md` — a high+ red-team finding during a drill counts for L3 demotion if attributable.
- `RHYTHM.md` — the daily heartbeat is where degraded-mode status is published.
- `GOVERNANCE.md` — the decision matrix tells you who approves a waiver; this doc tells you when a waiver is the right tool.
