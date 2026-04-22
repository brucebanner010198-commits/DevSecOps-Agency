---
name: retrospective
description: >
  This skill should be used when a project closes (shipped / blocked / parked-rung-7)
  and the CEO needs to run the close retro that feeds `LESSONS.md`. It defines
  the retro format, the mandatory attendance list, the evidence-gathering steps,
  and the output artefact `_meetings/<slug>-retro-<date>.md`. Trigger phrases
  include "run the retro", "close-retro for <slug>", "post-ship retro", "blocked
  project retro", "we're parking this at Rung 7", or any `/devsecops-agency:retro`
  invocation. Also used at quarterly portfolio review.
metadata:
  version: "0.1.0"
---

# retrospective — post-close review

Read `references/format.md` before writing the minutes. Read `references/cadence.md` to know which retro kind applies.

## When to trigger

- **Project close.** Any outcome — shipped, blocked, parked-rung-7. Mandatory. CEO invokes as last step of playbook before `lessons-ledger`.
- **Quarterly portfolio review.** CAO + CEO. Runs across every ledger row in the quarter.
- **Post-incident.** When CSRE declares an incident closed. Kind = `incident`.
- **Post-wave.** When a repo-level wave (v0.3.x) ships. CEO-only. Kind = `wave`.

## Inputs

The skill reads:

1. `outputs/devsecops-agency/<slug>/status.json` — final state.
2. `outputs/devsecops-agency/<slug>/chat.jsonl` — all board decisions.
3. `outputs/devsecops-agency/<slug>/_worktrees/**/worktree.json` — merge outcomes.
4. `_sessions/ceo/<sessionId>.jsonl` + per-chief session logs for the project.
5. `_decisions/ADR-NNNN-*.md` filed during the project.
6. `_vision/audit/<slug>-close-audit.md` (CAO output).
7. `_vision/playbooks/stones/*.md` authored from this project.
8. `_memory/patterns/<slug>.md` (written by Deep dreaming just before the retro).
9. Prior 3 rows of `LESSONS.md` (to check whether any "what we'd change" carried in unchanged).

## Mandatory attendance

Per `references/cadence.md`:

| Kind | Attendees | Written by |
| --- | --- | --- |
| project-close | ceo + cao + cevo + crt | ceo |
| portfolio | ceo + cao + user | ceo + cao |
| incident | ceo + csre + ciso | csre |
| wave | ceo + coo + (optional) user | ceo |

Anyone listed as required who is unavailable produces a **skip note** in the minutes — the retro does not proceed without noting the absence and who covered.

## Output

`_meetings/<slug>-retro-<YYYY-MM-DD>.md`. Written via `meeting-minutes` with kind `retro`. Sections in this order:

1. `## Context` — slug, dates, final outcome, final gate colours.
2. `## Timeline` — phase-by-phase, citing session log lines.
3. `## Worked` — ≤ 5 bullets, cited. What the agency did well.
4. `## Gated` — ≤ 5 bullets, cited. Where gates blocked and why.
5. `## Loops & rungs` — fix-loops per (council, phase), rungs traversed, Rung-7 artifacts if applicable.
6. `## Lessons` — ≤ 3 bullets, each a candidate row for `LESSONS.md` lessons field. Cited.
7. `## Reusable decisions` — ≤ 2 bullets, each citing an ADR worth reusing.
8. `## What we'd change` — ≤ 3 bullets. Behaviour changes, not aspirations.
9. `## Carry-over check` — did any "what we'd change" from the last 3 `LESSONS.md` rows repeat in this project? If yes, flag as CAO red.
10. `## Follow-ups` — paired `taskflow` task IDs for every action item. Orphan actions are forbidden (`AGENTS.md > ## Anti-patterns`).

## Process

1. **Verify preconditions.** CAO close-audit, CEVO close-eval, and CRT pre-release red-team must all have landed. If any is missing, abort and log `blocked — pending <which>`.
2. **Gather evidence.** Read every input file. Build a citation-keyed outline.
3. **Write the minutes.** One section at a time. Every factual claim carries `file:line` per `AGENTS.md > ## Start`.
4. **Carry-over check.** Read prior 3 `LESSONS.md` rows. If any "what we'd change" row repeats verbatim or by paraphrase, emit the carry-over flag and file ADR `kind: repeat-lesson`.
5. **Pair every follow-up with a task ID.** Invoke `taskflow` to create rows under the relevant phase for each action item.
6. **Hand off to `lessons-ledger`.** The retro's `## Lessons`, `## Reusable decisions`, and `## What we'd change` sections feed directly into the ledger row.
7. **Notify.** If the retro produced a CAO red via carry-over flag, invoke `notify` with `event: "gate-red"`.

## Skill index entry

Register in `skills/AGENTS.md > ## Skill index`:

```
| `retrospective` (v0.3.8) | Post-close / post-wave / post-incident retro. Feeds LESSONS.md via `lessons-ledger`. |
```

## Anti-patterns

- **Don't write the retro before CAO + CEVO + CRT land.** Late findings flip the outcome. Wait.
- **Don't skip the retro on a "successful" project.** `MISSION.md > North stars § 5` requires every close to produce a lesson.
- **Don't write a retro longer than 10 minutes of reading.** Detail goes in `_memory/patterns/<slug>.md`.
- **Don't copy-paste last project's retro.** Carry-over check will catch it.
- **Don't create action items without paired `taskflow` task IDs.** Orphan actions rot.
- **Don't let the retro be the first place a finding appears.** If it was a finding, it was a CAO / CEVO / CRT output. The retro consolidates; it does not discover.

## Progressive disclosure

- `references/format.md` — the 10-section template with example fills.
- `references/cadence.md` — the 4 retro kinds, attendance rules, and cadence.
- `references/carry-over-check.md` — the Jaccard comparator used to detect repeat "what we'd change" rows.
