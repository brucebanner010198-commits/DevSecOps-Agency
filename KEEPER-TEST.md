# KEEPER-TEST.md — the fire-readily criterion

Root document. The question the COO asks `performance-reviewer` about every agent at every quarterly checkpoint. Read together with [`VALUES.md`](VALUES.md).

## The question

> *"If this agent walked in tomorrow claiming a similar role from a peer agency, knowing what we now know about their 90-day performance, would we hire them at the same tier?"*

- **Yes** → keep. Annotate strengths in `_vision/roster/performance.md`.
- **Yes, but** → prompt-upgrade. File an ADR; track whether the upgrade moved performance.
- **No** → fire (archive). File an ADR via `roster`; preserve the agent file in `_vision/roster/_archive/<name>.md` with a redirect line. `git rm` is forbidden by `VALUES.md §4 (append-only)`.

The Keeper Test is not a team-fit test. It is an is-this-person-still-our-top-pick test. A high-performing agent whose domain is no longer relevant still passes the test — and gets **repurposed** (a COO roster move) rather than fired.

## Who runs it

- **`performance-reviewer`** (specialist, `people-ops` council) scores each agent against the inputs below and writes `_vision/roster/performance.md`.
- **`hiring-lead`** (specialist, `people-ops`) reads the review and proposes hire / fire / repurpose / tier-change actions.
- **`coo`** (Chief, `people-ops`) convenes the People-ops council, files ADRs for every mutation via the `roster` skill, and reports the roster delta to the CEO.
- **`ceo`** reviews, decides, and — for fires only — escalates to the user via `inbox.json` + `user-meeting`. **The user has the final vote on firing any agent.**

## Cadence

- **Quarterly** (mandatory): every agent scored. Roll-up into `_vision/roster/performance.md`.
- **Per-project** (on-demand): the CAO close-audit may name a specific agent as contributing to a red. That triggers a mid-quarter review for that agent only.
- **On prompt-diff bounceback** (automatic): three consecutive bouncebacks on `red-team` prompt-diff review trigger an immediate mid-quarter review.

## Inputs to the review

`performance-reviewer` reads:

1. **Session logs.** `_sessions/<agent>/*.jsonl` — every dispatch / report / note / error in the review window.
2. **Gate outcomes.** `chat.jsonl` entries across all projects in the window; bucket the agent's reports by gate colour.
3. **Fix-loop attempts.** `status.json > tasks[]` — count `fixAttempts` values ≥ 1 and ≥ 2 for tasks owned by this agent.
4. **Audit findings.** `_vision/audit/*.md` — any CAO findings that cited the agent.
5. **Red-team findings.** `_vision/playbooks/stones/*.md` — any stones authored from findings against this agent's outputs.
6. **Minutes.** `_meetings/*.md` — any meeting where this agent's work was escalated or debated.

## Scoring axes

Four axes per agent. Each scored `green | yellow | red` with one-line evidence (citation required).

| Axis | Green | Yellow | Red |
| --- | --- | --- | --- |
| **Gate hit rate** | ≥ 85 % reports green on first attempt | 65–85 % | < 65 % |
| **Fix-loop rate** | < 10 % of tasks required a fix-loop | 10–25 % | > 25 % or any Rung-3+ | 
| **Audit findings** | zero findings cited this agent | ≥ 1 finding, severity = low | ≥ 1 finding severity ≥ medium |
| **Values compliance** | cited specific values in their reports | inconsistent | violated any value in `VALUES.md` |

Overall rating:

- **Green** (keep) = 4 greens.
- **Yellow** (keep-but-upgrade) = ≥ 1 yellow, 0 reds.
- **Red** (fire-or-repurpose) = ≥ 1 red on any axis.

## Actions by rating

### Green

Keep. No change. Annotate `performance.md` with the strengths.

### Yellow → prompt upgrade

Per `VALUES.md §10`, the COO commissions a prompt-upgrade — never a tier downgrade (tier downgrades are forbidden by `skills/model-tiering/references/tier-rules.md`). The upgrade runs through `red-team` prompt-diff review. Track whether the next 30-day window moves the axis from yellow → green.

If two consecutive prompt upgrades fail to move the yellow → green, escalate to **red** on the next review.

### Red → fire or repurpose

Two options, per `skills/roster/SKILL.md`:

1. **Repurpose.** The agent's domain is still relevant but they are struggling. COO proposes moving them to a different council where their strengths fit better. File an ADR; run the new role for a 30-day window; re-review.
2. **Fire.** The agent's domain is no longer relevant or they have failed a repurpose. **User approval required.** COO proposes via `inbox.json`; user decides at the next `user-meeting`.

If fired:

- Archive `agents/<council>/<name>.md` to `_vision/roster/_archive/<name>.md` with a `## Redirect` header citing the ADR.
- Update `councils/<council>/TEAM.md` roster.
- Update `skills/ship-it/references/status-schema.md > team.<council>.specialists`.
- File the ADR (mandatory, `_decisions/ADR-NNNN-roster-fire-<name>.md`).
- Write a `note` entry on the agent's session log: `"role closed, archived to <archive-path>, ADR-NNNN"`.

## Reserved agents

The 16 chief slugs and `skill-creator` are **not** subject to the Keeper Test in the normal flow — they are structural roles. Firing a Chief or skill-creator requires a **user-only** decision via `user-meeting` + ADR, and triggers a council restructure. See `VALUES.md §3` for why audit / eval / red-team / sre chiefs have an extra independence check.

The user (Sir) is never subject to any review.

## Anti-patterns

- **Don't score on single-project outcomes.** One failed ship is not a red — three failed dispatches in a quarter is.
- **Don't propose a tier downgrade.** Forbidden by `VALUES.md §10`. Propose a prompt upgrade; if two upgrades fail, propose fire-or-repurpose.
- **Don't fire without user consent.** COO alone cannot fire an agent. CEO alone cannot fire an agent. Both must present to the user via `user-meeting`.
- **Don't `git rm` a fired agent.** Archive to `_vision/roster/_archive/` with a redirect. Append-only wins.
- **Don't skip the review because "the agent is obviously fine."** The review is a paper-trail artifact, not a formality. The ledger tells future maintainers *why* we kept this agent.
- **Don't run the review on the same session as the project the agent worked on.** Independence invariant (`VALUES.md §3`) — a mid-project Keeper Test must be run by a performance-reviewer who did not help deliver that project.

## Skill integration

- `skills/keeper-test/SKILL.md` — the invocation contract (how the COO asks `performance-reviewer` to run the test).
- `skills/roster/SKILL.md` — the hire / fire / repurpose / tier-change lifecycle.
- `skills/adr/SKILL.md` — the receipt filed for every mutation.
- `skills/user-meeting/SKILL.md` — the only sanctioned path from "COO proposes fire" to "user approves fire."

See also: [`VALUES.md`](VALUES.md) § 1, 3, 4, 10, 11; [`MISSION.md`](MISSION.md) § non-goals.
