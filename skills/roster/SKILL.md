---
name: roster
description: This skill should be used when the COO (or the CEO on COO's behalf) is managing the living agent roster — hires, fires, tier changes, repurposes, idle reviews, and agency-capacity census. Trigger phrases include "roster check", "census", "who do we have", "hire a new specialist", "fire agent", "repurpose", "tier upgrade", "agent-performance review", "fix-loop-cap hit twice — is it the role or the prompt", and every REM retro or quarter roll-up. Wired into People-ops Council; also invoked by CEO on 2nd fix-loop-cap hit within a 30-day window.
metadata:
  version: 0.3.0-alpha.3
---

# roster — living agent registry + lifecycle

Roster is the agency's org chart as data. Census is the snapshot; proposals + ADRs are the mutations. Waves 1-2 wrote the process contract; Wave 3 (this skill) gives it a home.

## When to trigger

- Project kick-off / close / quarter roll-up / REM retro (scheduled).
- On 2nd fix-loop-cap hit on the same `(council, phase)` within 30 days (reactive).
- On user request (ad-hoc): "who do we have", "do we need a specialist for X", "why is agent Y still around".
- On CEO observation that a council emitted zero dispatches across two consecutive projects (idle-flag).

## Artifact layout

```
_vision/roster/
  census.md           # rewrite — alphabetized full agent table
  performance.md      # window-specific — usually 30d or 90d
  proposals.md        # action list — hire / fire / repurpose / tier-change / prompt upgrade
  coo-brief.md        # synthesis — 1-page CEO read
  _archive/
    <name>.md         # preserved prompts of fired/repurposed agents
```

## Process

1. **CEO convenes COO.** Roster is a People-ops output. CEO is the only user voice; COO is the only agent voice on roster changes.
2. **COO dispatches three specialists in parallel** (no ordering dependency): `roster-manager` → census, `performance-reviewer` → performance, `hiring-lead` → proposals.
3. **COO synthesises `coo-brief.md`** with the standard 4-section shape: census delta, capacity, performance flags, recommendations.
4. **CEO accepts each recommendation explicitly.** Every accepted recommendation is an ADR in the same CEO turn — never deferred. See `skills/adr/references/decision-triggers.md > People-ops`.
5. **`skill-creator` executes.** Hires and repurposes go through `skill-creator`. Fires file an archive redirect; the agent file moves to `_vision/roster/_archive/<name>.md`.
6. **Meeting minutes capture the board-style discussion** if more than one recommendation is debated. 1:1 taskflow-task mapping for every action item per root AGENTS.md.

## Invariants

- Hires only via `skill-creator`. No raw-drafted agent prompts. See `skills/skill-creator/SKILL.md`.
- Every hire/fire/tier-change/repurpose files an ADR. Mandatory triggers in `skills/adr/references/decision-triggers.md`.
- Fires preserve the prompt in `_vision/roster/_archive/`. Never `git rm` an agent file.
- Blocking-council fires (`security-lead`, `gc`, their specialists) require user-signed waivers in `inbox.json`.
- Tier **downgrades** are forbidden by `skills/model-tiering/SKILL.md`. Propose prompt upgrade instead.
- See `references/action-rules.md` for per-action checklists (hire/fire/tier-change/repurpose/prompt-upgrade).
- See `references/archive-policy.md` for the exact archive file shape + redirect line.

## Contract with adjacent skills

- `okr.score` runs on every COO report. `okr_alignment` is against agency-capacity OKRs only.
- `gates.validate` uses People-ops heuristic in `councils/people-ops/AGENTS.md > Gate heuristic`.
- `meeting-minutes` writes if board discussion involves ≥ 2 recommendations.
- `capacity` skill (sibling) supplies the utilization bands that `roster-manager` reads.
- `audit` skill (sibling) validates the resulting paper trail in the next close-audit.

## Pre-flight checks

- If `_vision/roster/census.md` missing: this is the **first** roster checkpoint. Bootstrap by reading `agents/*.md` and writing the initial census. No performance.md yet (no window data).
- If performance.md window would be < 30 days: return `blocked` with a wait-line. Single-week judgments retire ramping agents.
- If the COO being invoked was just hired (< 30 days active): surface a first-run warning in `coo-brief.md`.
