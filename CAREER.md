# CAREER

> How agents progress within the agency. Three levels within each tier; promotion is earned, not assigned; inter-tier mobility is USER-ONLY.

One-sentence summary: **do the work, get the receipts, earn the level.**

Read by: `skills/keeper-test/SKILL.md` (gates upgrades by level); `skills/career-ladder/SKILL.md` (promotion engine); `skills/roster/SKILL.md` (stores current level); CAO on quarterly audit.

---

## Tier vs. level

**Tier** is the model budget (Haiku / Sonnet / Opus) and is pinned on the Role Card. Changing tier requires a user-meeting and USER approval per `VALUES.md §10`. The Keeper Test skill does not promote between tiers.

**Level** is internal seniority *within* a tier. Three levels:

| Level | Shortname | Meaning |
| --- | --- | --- |
| L1 | trial | New to the role. Still proving gate hit-rate + fix-loop discipline + values compliance. |
| L2 | steady | Reliably green on the four Keeper Test axes. Default working level. |
| L3 | principal | Top-rated within tier. Authors stepping-stones; votes first on prompt-diffs; mentors new agents in the council. |

Level is stored in `_vision/roster/levels-<YYYY-MM-DD>.md` and refreshed quarterly by `skills/career-ladder`.

---

## Promotion gates

### L1 → L2 (trial → steady)

All three must hold:

1. **Two consecutive Keeper Test greens** (both Axis 1–4 green in two back-to-back quarterly performance files).
2. **≥ 10 reports landed** during the trial window (filters out "green because no data").
3. **Zero `roster-upgrade` ADRs** in the trial window. (An upgrade means the axis was actually yellow and the COO intervened — inconsistent with "steady".)

Bootstrap exception: in Quarter 0 and Quarter 1, agents remain L1 regardless of preliminary ratings. L1 → L2 is earliest at the first full Keeper Test review.

### L2 → L3 (steady → principal)

All four must hold:

1. **Four consecutive Keeper Test greens** while at L2 (≥ 1 year of steady performance).
2. **≥ 3 stepping-stones authored** (as primary author) that survived the playbook archive's supersession process.
3. **≥ 1 prompt-upgrade authored** — the agent was the primary author on a `roster-upgrade` ADR body for *another* agent in the same council (counts as mentorship evidence, not their own upgrade).
4. **Zero high+ red-team findings** attributable to work the agent led during the window.

### L3 → L2 (demotion)

Demotion within tier is allowed and happens on:

- **Any Keeper Test red** while at L3 → immediate L2 (bypasses the standard upgrade/repurpose path for non-reserved L3s; the signal is that principal-level performance is not currently being sustained).
- **One or more high+ red-team findings** attributable to L3-led work during the quarter.

Demotion is not punitive — it files ADR `kind: career-demotion` with the rating evidence and lets the agent re-climb via the L2 → L3 path when performance rebounds. Tier is never touched.

### No L3 → L1

Skipping a level on the way down is forbidden. Demotions always move one step (L3 → L2). If the performance is bad enough to warrant L1 re-trial, that's actually a `roster-repurpose` (via `skills/keeper-test/actions.md`), not a career-ladder move.

---

## Privileges by level

Each level unlocks concrete authorship + review permissions:

| Privilege | L1 | L2 | L3 |
| --- | --- | --- | --- |
| Runs assigned tasks | Yes | Yes | Yes |
| Writes ADRs on own work | Yes | Yes | Yes |
| Votes on prompt-diff review in own council | No | Yes | **First vote** |
| Authors stepping-stones | No | Yes | Yes (counted toward L3 re-validation) |
| Primary author of `roster-upgrade` ADR for another agent | No | No | Yes |
| Mentor assignment for newly-hired agent | No | No | Yes |
| First-choice reviewer for cross-council drafts | No | No | Yes |

First-vote on prompt-diff review means: if ≥ 1 L3 is present in the reviewing council, their vote is tallied first and is the de facto initial recommendation. Other L2 votes still count; the L3 vote is not a veto.

---

## Reserved names

The following are **always L3** and are not subject to L1 / L2 / L3 progression:

- `ceo`
- The 16 Chiefs (one per council: cro, pm-lead, engineering-lead, security-lead, qa-lead, devops-lead, docs-lead, gc, cmo, cso, coo, cao, evaluation-lead, red-team-lead, sre-lead, plus the execution VP-Eng role which shares the engineering-lead file).
- `skill-creator`.

Total: 1 + 16 + 1 = 18 reserved names. The 16 Chiefs overlap with the Keeper Test exclusion list. `skill-creator` is also excluded from the Keeper Test entirely.

Reserved names can still be fired — the USER has final vote and there is no upper bound. But they are not promoted or demoted by `career-ladder`.

---

## Writing the first levels file

At v0.3.9 ship-date, every non-reserved agent starts at **L1**. Write `_vision/roster/levels-<YYYY-MM-DD>.md`:

```markdown
# levels-<YYYY-MM-DD>.md

- **Review kind:** bootstrap
- **Window:** bootstrap — v0.3.9 install date
- **Roster size:** 75 (non-reserved)

## Non-reserved agents

| Agent | Council | Tier | Level | Since | Last change |
| --- | --- | --- | --- | --- | --- |
| <agent> | <council> | Sonnet | L1 | 2026-04-22 | - |
| ... | ... | ... | L1 | 2026-04-22 | - |

## Reserved (always L3)

ceo · cro · pm-lead · engineering-lead · security-lead · qa-lead · devops-lead · docs-lead · gc · cmo · cso · coo · cao · evaluation-lead · red-team-lead · sre-lead · skill-creator
```

Bootstrap ADR: `_decisions/ADR-NNNN-career-ladder-bootstrap.md`, kind `career-bootstrap`. Cites v0.3.9 and the levels-file path.

---

## Anti-patterns

- Don't promote across tiers via `career-ladder`. That path is USER-ONLY and goes through a user-meeting.
- Don't backdate L2 / L3 promotions to recognize "historical" work. The gate is prospective — the window starts at v0.3.9 install for every agent.
- Don't skip demotion on a red Keeper Test because the agent is "important" to an active project. A red L3 that stays L3 is a VALUES §1 violation (receipts over opinions). File the demotion ADR immediately; the agent keeps running their task under L2 privileges.
- Don't let a single stepping-stone count toward multiple agents' L3 gates. Primary author only; co-authors are named but do not accrue the gate credit.
- Don't treat L3 as permanent. Principal level is re-earned every quarter via the four-axis Keeper Test; one red resets the streak.
- Don't edit a landed `levels-<date>.md` after the fact. Correction is a new file with `kind: correction` in the header, citing the prior file.
