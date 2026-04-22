# career-ladder/references/levels.md

Exact gate thresholds for each level transition. Parsed by `skills/career-ladder/SKILL.md` step 4 and 5.

## L1 → L2 (trial → steady)

All three must hold simultaneously on the quarterly review turn:

| # | Gate | Exact threshold | Evidence |
| --- | --- | --- | --- |
| 1 | Consecutive Keeper Test greens | ≥ 2 | Latest 2 `performance-<date>.md` both green for this agent across Axis 1–4 |
| 2 | Minimum reports landed in trial window | ≥ 10 | Count of `kind: report` session-log entries by this agent |
| 3 | Zero `roster-upgrade` ADRs for this agent | 0 | `_decisions/` filter by `kind: roster-upgrade` AND `subject: <agent>` |

Trial window = from the later of (v0.3.9 install date, most recent `career-ladder` bootstrap for this agent) to today.

## L2 → L3 (steady → principal)

All four must hold:

| # | Gate | Exact threshold | Evidence |
| --- | --- | --- | --- |
| 1 | Consecutive Keeper Test greens at L2 | ≥ 4 | Latest 4 `performance-<date>.md` while agent was at L2 — all green |
| 2 | Stepping-stones authored as primary | ≥ 3 | `_vision/playbook/index.md` filter by `primaryAuthor: <agent>` AND `survived: true` |
| 3 | Prompt-upgrades authored for others | ≥ 1 | `_decisions/` filter by `kind: roster-upgrade` AND `author: <agent>` AND `subject ≠ <agent>` AND `subject.council = <agent>.council` |
| 4 | Zero high+ red-team findings attributable to L2-led work | 0 | `_vision/red-team/findings.md` filter by `severity ∈ {high, critical}` AND `leadAgent: <agent>` AND `window: current` |

Primary-author on stepping-stones is NOT transferable. If two agents co-authored, the one in the `primaryAuthor` field counts; the other does not get credit toward their L3 gate.

## L3 → L2 (demotion)

Either trigger:

| Trigger | Condition | Immediate action |
| --- | --- | --- |
| Red Keeper Test | This quarter's rating = red on any axis | File ADR `kind: career-demotion`; update levels file; no waiting period |
| Red-team finding | ≥ 1 `severity ∈ {high, critical}` attributable to L3-led work in this quarter | Same |

Demotion is not punitive. The agent keeps running their current task under L2 privileges (loses first-vote on prompt-diff, loses mentor assignments for newly-hired agents) but workload continues. The next quarterly can re-promote if gates are re-met.

## L3 re-validation (no movement)

An L3 with an all-green quarterly stays at L3 but its "L3 streak" counter resets — a fresh 4-quarter clock begins. This isn't about demotion risk; it's about surfacing the cohort of L3s who have been principal for multiple consecutive quarters (used by the quarterly heartbeat's "tenure" analytics).

## L3 → L1 (forbidden)

Skipping a level on the way down is never allowed via career-ladder. If an L3's performance is so bad that L1 trials would be warranted, that is:

- A `roster-repurpose` move via `skills/keeper-test/references/actions.md` (change council), OR
- A fire proposal to USER via `skills/keeper-test/references/actions.md` § Fire.

Neither is handled by career-ladder. Career-ladder only ever moves agents one step at a time (L1 → L2 up, L3 → L2 down, with bidirectional L2 → L3 ↔ L2 movement across quarters).

## Bootstrap

Every non-reserved agent starts at L1 on v0.3.9 install:

- `Review kind: bootstrap` in `levels-<date>.md` header.
- One `career-bootstrap` ADR covers the entire roster — not one per agent.
- No promotions happen in bootstrap, even if a prior rating system (pre-v0.3.9) might have suggested otherwise. The gate is prospective.

## Reserved names (always L3)

Hardcoded in `skills/career-ladder/SKILL.md`:

```
ceo, cro, pm-lead, engineering-lead, security-lead, qa-lead, devops-lead,
docs-lead, gc, cmo, cso, coo, cao, evaluation-lead, red-team-lead, sre-lead,
skill-creator
```

(17 names — `engineering-lead` serves both CTO and VP-Eng roles.)

Reserved names are listed in `levels-<date>.md` under a separate "Reserved (always L3)" section and are NOT processed by the promotion/demotion gates. Firing a reserved name goes through the Keeper Test USER-ONLY path; there is no career-ladder move for them.

## Auditing the gates

Every level change files an ADR with `evidence:` section citing exact file paths + line numbers used to compute the gate. CAO quarterly audit spot-checks ≥ 10 % of promotion ADRs.
