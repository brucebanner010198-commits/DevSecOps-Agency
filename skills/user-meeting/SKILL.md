---
name: user-meeting
description: >
  This skill should be used when the CEO convenes the Chairman of the Board
  for a direct 1:1 selection meeting — most commonly the top-5 idea pipeline
  handoff, but also ETA commits, pivot approvals, and mid-project
  escalations. The skill provides a deterministic 4-phase flow (brief →
  present → capture → commit) that ends with a durable
  `_meetings/<date>-user.md` entry, an ADR for any material decision, and
  taskflow tasks for every action item. Exactly one of these meetings per
  top-5 cycle. Also renders a live Cowork artifact so the Chairman can read
  the top-5 side-by-side with chat. Trigger phrases: "user meeting", "take
  it to the Chairman", "present top-5", "Chairman picks", "commit ETA",
  "escalate to the Chairman". **Group decisions use `skills/board-meeting`
  instead** — this skill is the direct 1:1 Chairman ↔ CEO channel only.
metadata:
  version: "0.3.0-alpha.2"
---

# user-meeting — the direct Chairman ↔ CEO channel

The direct 1:1 agency ↔ Chairman convening. Everything else is a chat message. Used when the decision at hand requires the Chairman's signature but does not need the full Board. See `skills/board-meeting` for the group convening.

## When to invoke

| Trigger | Typical payload | Meeting kind |
| --- | --- | --- |
| Top-5 pipeline handoff | `_vision/strategy/_pipeline/top-5.md` | `user` |
| ETA commit for a picked idea | Scoped spec + effort estimate | `user` |
| Pivot mid-project | Pivot rationale + options | `user` |
| Gate-red waiver request (a blocking council: security, evaluation, red-team, audit; legal per `skills/gates`) | Blocking council's report | `user` |
| Top-5 override proposal by CEO | Alternative ranking + ADR draft | `user` |

Never invoked automatically — CEO invokes on decision-readiness. If prerequisites are not met (e.g., top-5 not written), the skill refuses and returns a missing-prereq list.

## Four phases

### Phase 1 — Brief (CEO-solo)

- Read the primary payload artifact.
- Read `_vision/VISION.md > ## Active OKRs` + `_memory/MEMORY.md > ## Preferences (from user)`.
- Build a 3-section pre-read:
  - **Decision requested** (one sentence)
  - **Options** (≤ 5)
  - **CEO's recommendation** (optional, with reason)
- Write `_meetings/<date>-user-<slug>.md` in `status: scheduled` state with the pre-read pinned.

### Phase 2 — Present (CEO ↔ user)

- Render the live Cowork artifact via `create_artifact`:
  - Header: decision requested
  - Body: one card per option (for top-5 that's 5 cards)
  - Footer: CEO's recommendation + "pick" radio-style control
- Chat narration: CEO speaks, one option at a time, under 60s per card.
- User may pause, ask, swap order. All utterances captured verbatim into minutes.
- Do not advance until the user has responded to every card or explicitly skipped.

### Phase 3 — Capture (user picks + constraints)

- User selects 1–2 options (for top-5) OR picks one path (for pivot/ETA).
- Capture constraints: ETA, budget, must-not-haves, hard deadlines.
- If the user's pick contradicts `opportunity-ranker`'s recommendation → ADR (category: pivot-class) before Phase 4.
- If the user rejects all options → ADR (rejection rationale) + loop back to `idea-pipeline` with captured constraints.

### Phase 4 — Commit (CEO → agency)

- Update `_meetings/<date>-user-<slug>.md` with:
  - Decision verbatim
  - Constraints
  - Action items (each paired with a `taskflow` task ID — 1:1)
  - Committed ETA (range, with explicit assumptions)
- Mark meeting `status: closed`.
- For each picked idea: `vision-doc` writes a stub `_vision/projects/<slug>.md` with derived project-OKRs.
- For each action item: `taskflow` creates the task; ID back-filled into minutes.
- Notify channel: `user-meeting-closed` (rate-limited by `notify` skill).

## Prerequisites

- Top-5 pipeline: `_vision/strategy/_pipeline/top-5.md` exists and is ≤ 24h old.
- ETA commit: picked idea has `spec.md` with scope section.
- Pivot: project status.json has a `needs-decision` task referencing the pivot trigger.
- Waiver: blocking council has filed a `gate-red` report with a waiver ask.

If any prerequisite fails, the skill returns `blocked` with a follow-up list — no user time wasted.

## ADR triggers (v0.3.0)

All material meeting decisions file an ADR. Mandatory:

- User picks an idea not in CEO's preferred order → pivot-class ADR
- User commits an ETA shorter than opportunity-ranker's effort estimate → risk-acceptance ADR
- User rejects all top-5 → thesis-review ADR
- User waives a gate-red → waiver ADR (required by `gates` + `legal-risk-assessment`)

Body of the ADR cites the meeting minutes by `_meetings/<date>-user-<slug>.md:<line>`.

## Outputs

```
_meetings/<date>-user-<slug>.md   # minutes (meeting-minutes skill owns format)
_decisions/ADR-NNNN-<slug>.md      # 0 or more — one per material decision
_vision/projects/<slug>.md         # 1 or 2 — one per picked idea (okr skill writes)
status.json > tasks[]              # N — one per action item
artifact: user-meeting-<date>      # live Cowork artifact (transient; persists in UI)
```

## Cap

- Max 5 options presented per meeting. If more, split into sequential meetings (rare — idea-pipeline already caps at 5).
- Max 45 minutes user-facing. If decision not reached, mark minutes `deferred` and re-schedule.

## Progressive disclosure

- `references/meeting-flow.md` — phase-by-phase checklist, artifact prompts, user-voice capture rules
- `references/top5-script.md` — the exact CEO narration script for top-5 meetings
- `references/decision-capture.md` — how to phrase captured constraints unambiguously
