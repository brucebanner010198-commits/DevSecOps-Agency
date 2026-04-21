# user-meeting — phase flow reference

Complete checklist for CEO. No skipping phases. No merging phases.

## Phase 1 — Brief (solo, ≤ 10 min)

- [ ] Payload artifact read in full (top-5, pivot rationale, etc.)
- [ ] `_vision/VISION.md > ## Active OKRs` read
- [ ] `_memory/MEMORY.md > ## Preferences (from user)` read
- [ ] `_memory/patterns/<slug>.md` read if the decision relates to a prior project
- [ ] Pre-read scaffold written to `_meetings/<date>-user-<slug>.md`:
  - Decision requested: 1 sentence
  - Options: ≤ 5 · one line each
  - CEO's recommendation: optional but if present, must cite reason
  - Prerequisites-satisfied checklist: verified
- [ ] Minutes file `status: scheduled`

## Phase 2 — Present (user in room)

Open with: "I have <N> options for <decision>. I'll walk each one in ≤ 60 seconds. Interrupt whenever."

Per option:
- [ ] State option name · elevator pitch (≤ 30 words)
- [ ] State top 2 proof points
- [ ] State top 2 risks
- [ ] Surface the composite score (for top-5) or effort estimate (for ETA)
- [ ] Pause 3 seconds for questions

Close each card with: "Questions on this one?"

After all cards:
- [ ] Summary: "So, <N> options. <brief recap>. Which are you drawn to?"
- [ ] Live artifact rendered with radio-style selection

Do NOT:
- Advance if the user said "wait" or asked a question
- Combine options into the narration (one at a time)
- State CEO's recommendation before all options are presented

## Phase 3 — Capture (user-driven, ≤ 20 min)

- [ ] User selection captured verbatim: "You picked <X> and <Y>" (reflect-back)
- [ ] ETA commit captured (range · assumptions · explicit constraints)
- [ ] Must-not-haves captured as list
- [ ] Hard deadlines captured as dates (or "none")
- [ ] Any disagreement with `opportunity-ranker` noted → ADR draft started
- [ ] User questions not answerable in-meeting captured as `followups[]`

Reflect-back is mandatory. No decision captured without "Is this right?" confirmation.

## Phase 4 — Commit (CEO-solo, ≤ 10 min)

- [ ] Minutes updated with: decision · constraints · action items · committed ETA
- [ ] Each action item paired with a `taskflow` task ID (1:1 invariant)
- [ ] Any ADR triggers filed in same CEO turn
- [ ] For each picked idea: `vision-doc` writes stub `_vision/projects/<slug>.md`
- [ ] `okr` skill invoked to derive per-project OKRs traced from workspace OKRs
- [ ] Minutes `status: closed`
- [ ] `notify` fires `user-meeting-closed` (rate-limited)

## Failure modes

| Failure | Response |
| --- | --- |
| User picks 3+ for top-5 | Gentle push-back: "We commit 1–2 per cycle. Rank them — I'll queue the rest for next pipeline." If user insists → ADR (capacity-override) + attempt commit with risk note. |
| User rejects all options | ADR (rejection rationale) + meeting marked `deferred` + loop back to `idea-pipeline` with captured "what would have worked" constraint. |
| User cannot commit ETA | Meeting marked `deferred` with specific blocker listed. Re-schedule when blocker cleared. |
| User asks for a sixth option | Sixth option always inferior to top-5 by `opportunity-ranker`'s math — narrate that, then offer: "I can re-run the pipeline with <new-constraint>." |
| User overrides CEO recommendation | Default path. Do not argue. ADR captures reason. |

## Voice capture rules

- Every user utterance that affects the decision is quoted verbatim in minutes.
- Paraphrases marked `[paraphrased]`.
- If the meeting is in chat (not voice), no paraphrase distinction needed — the transcript is the minutes source.

## Closing line

"Minutes written to `_meetings/<date>-user-<slug>.md`. ADRs filed: <list or none>. Tasks created: <count>. I'll dispatch chiefs tomorrow unless you want a different sequence."
