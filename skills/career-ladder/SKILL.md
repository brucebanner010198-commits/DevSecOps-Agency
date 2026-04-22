---
name: career-ladder
description: Per-agent level engine. L1 (trial) → L2 (steady) → L3 (principal) within tier; never promotes between tiers (VALUES §10, USER-ONLY). Invoked quarterly by skills/rhythm as a sub-step, and ad-hoc when an agent authors a stepping-stone or primary-authors a roster-upgrade ADR. Reads _vision/roster/performance-<latest>.md + last 3, computes promotion/demotion per CAREER.md gates, writes _vision/roster/levels-<date>.md, files career-promotion / career-demotion / career-bootstrap ADR per level change. Reserved names (CEO, 16 Chiefs, skill-creator) are always L3 — not processed. Bootstrap: first run writes every non-reserved agent at L1.
metadata:
  version: "0.1.0"
---

# career-ladder

## When to trigger

- Quarterly, as sub-skill of `skills/rhythm`'s quarterly heartbeat (primary path).
- Ad-hoc when an agent authors a stepping-stone that survives playbook supersession (updates L3 re-validation counter).
- Ad-hoc when an agent is primary author on a `roster-upgrade` ADR for another agent in its council (updates L3 mentorship counter).
- Manual by COO when a Keeper Test red lands mid-quarter on an L3 — immediate L3 → L2 demotion.

## Inputs

- `CAREER.md` — canonical gate definitions (L1→L2, L2→L3, L3→L2).
- `_vision/roster/performance-<latest>.md` + last 3 performance files.
- `_vision/roster/levels-<prev>.md` (if any).
- `_vision/playbook/index.md` — stepping-stone authorship ledger.
- `_decisions/*.md` — filter for `kind: roster-upgrade` with author field.
- `_vision/red-team/findings.md` — for L3 demotion trigger on high+ findings attributable to L3-led work.
- Reserved-names list (18 names) — frozen inside this skill.

## Outputs

- `_vision/roster/levels-<YYYY-MM-DD>.md` — per-agent level table.
- ADR per level change: `ADR-NNNN-career-{bootstrap|promotion|demotion}-<agent>.md`.
- Append to `_vision/roster/history.md` per change.
- `notify` event `career-levels-published` on quarterly runs (rate-limited: one notification per file).

## Process

1. **Verify preconditions.** If invoked quarterly, confirm `skills/keeper-test` has already produced `performance-<date>.md` for this quarter — if not, block and return.
2. **Load prior levels.** Read the most recent `levels-<date>.md`. If none exists, go to bootstrap (step 8).
3. **Compute each non-reserved agent.** For each row in the roster (excluding reserved names):
   - Read their rating in the latest + 3 prior performance files.
   - Count stepping-stones authored in the window (primary author only).
   - Count prompt-upgrades authored for others in the window.
   - Count high+ red-team findings attributable to their work in the window.
4. **Apply promotion gates per CAREER.md.**
   - L1 → L2: two consecutive greens + ≥ 10 reports + zero `roster-upgrade` ADRs.
   - L2 → L3: four consecutive greens + ≥ 3 stepping-stones + ≥ 1 prompt-upgrade + zero high+ red-team findings.
5. **Apply demotion gates.**
   - L3 → L2 on any Keeper Test red OR ≥ 1 high+ red-team finding attributable.
   - L3 → L1 is forbidden; a rating bad enough for L1 trials triggers `roster-repurpose` via `skills/keeper-test`, not a career-ladder move.
6. **Emit level diffs.** Produce a `{agent, prior, next, reason}` list for every change.
7. **Write outputs.** Author `levels-<YYYY-MM-DD>.md`. File one ADR per diff row. Append to `history.md`.
8. **Bootstrap branch.** If no prior `levels-<date>.md` exists, write one with every non-reserved agent at L1 and `Review kind: bootstrap`. File one `career-bootstrap` ADR covering the whole roster.
9. **Notify.** Emit `career-levels-published` event. Done.

## Interaction with keeper-test

The Keeper Test action-tree (`skills/keeper-test/references/actions.md`) handles Keep / Upgrade / Repurpose / Fire. Career-ladder handles level within tier. They compose:

| Keeper Test rating | Level change | Action |
| --- | --- | --- |
| Green at L1 | L1 → L2 if 2-streak + threshold met | Promote |
| Green at L2 | L2 → L3 if 4-streak + stones + mentor | Promote |
| Green at L3 | stay L3 | Reset re-validation counter |
| Yellow at L1 | stay L1 | Upgrade (prompt edit via roster) |
| Yellow at L2 | stay L2 | Upgrade |
| Yellow at L3 | stay L3 (first yellow); two-strike → L3 → L2 on second | Upgrade |
| Red at L1 | stay L1 (but flagged for fire/repurpose) | Fire-or-repurpose via keeper-test |
| Red at L2 | stay L2 (but flagged for fire/repurpose) | Fire-or-repurpose |
| Red at L3 | L3 → L2 immediately | Demotion ADR |

A reserved-name agent ignores this table entirely — they are always L3 in `levels-<date>.md`, regardless of Keeper Test rating.

## Anti-patterns

- Don't promote across tiers. That's USER-ONLY (`VALUES.md §10`) and goes through a user-meeting.
- Don't backdate a promotion to recognize "historical" work. Window starts at v0.3.9 install.
- Don't skip demotion on red L3 because they're working on an important project. File the demotion; their task runs under L2 privileges without interruption.
- Don't let a single stepping-stone count toward multiple agents' L3 gates. Primary author only.
- Don't write `levels-<date>.md` with zero changes and no ADR. If nothing moved, still write the file (append-only integrity) but file ADR `kind: career-noop-<YYYY-Q>` once per quarter to prove the skill ran.
- Don't edit a landed `levels-<date>.md`. Correction = new file citing prior, `Review kind: correction`.
- Don't promote in bootstrap. Bootstrap is L1-for-all; first real movement is the next quarterly.

See `references/levels.md` for per-level gate details and `references/privileges.md` for what each level unlocks.
