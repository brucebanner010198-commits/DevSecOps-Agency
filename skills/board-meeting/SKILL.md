---
name: board-meeting
description: >
  This skill should be used when the Chairman of the Board convenes the
  Board of Directors — the only *group* meeting the Chairman attends.
  Strategy and project goals are set and approved here: the CEO proposes,
  the Board's standing committees (Audit/CAO, Risk & Security/CISO+CRT,
  Evaluation/CEVO) review and challenge, and the Chairman casts the final
  vote. Also used for USER-ONLY decisions (`CONSTITUTION.md §2.2`) that
  need group review rather than a direct CEO call. Trigger phrases:
  "convene the board of directors", "call a board meeting", "chair the
  board", "set strategy with the board", or /devsecops-agency:board-meeting.
  Distinct from `exec-meeting` (CEO + Chiefs, no Chairman) and from
  `user-meeting` (direct 1:1 Chairman ↔ CEO call).
metadata:
  version: "0.1.0"
---

# board-meeting — the Chairman's Board of Directors convening

The genuine Board of Directors meeting: Chairman (chair) + `board-director` + CEO + the four committee Chiefs. Modeled on `skills/user-meeting`'s deterministic 4-phase flow, but as a *group* convening rather than a 1:1.

## When to invoke

| Trigger | Typical payload | Meeting kind |
| --- | --- | --- |
| Strategy / OKR-cycle approval | CEO's proposed `_vision/VISION.md` updates | `board` |
| Project-goal approval | CEO's proposed project OKRs | `board` |
| CEO oversight review | Close-audit + close-eval + Keeper Test summary | `board` |
| USER-ONLY decision needing group review | Constitution §2.2 action + supporting artifacts | `board` |

Never invoked automatically — only the Chairman convenes the Board (`councils/board/AGENTS.md > ## Must not > Self-convene`). If the CEO believes a Board meeting is warranted, it proposes to the Chairman via a direct call (`skills/user-meeting` or `skills/ceo`); the Chairman decides whether to convene.

## Attendees

- **Chairman of the Board** — chairs, casts the final vote.
- **`board-director`** — represents the Board body; runs the agenda.
- **CEO** — proposes strategy/goals; reports oversight-relevant status.
- **Committee chiefs** — `cao` (Audit), `security-lead` + `red-team-lead` (Risk & Security), `evaluation-lead` (Evaluation) — attend in committee capacity, per `councils/board/TEAM.md`.

## Four phases

### Phase 1 — Present (CEO → Board)

- CEO presents strategy/goals + status pre-read: **decision requested**, **options** (≤ 5), **CEO's recommendation**.
- `board-director` opens `_meetings/<date>-board-<slug>.md` in `status: scheduled` with the pre-read pinned.

### Phase 2 — Review (Board committees ↔ CEO)

- Each committee chief reviews the proposal from its lane (paper-trail integrity / security & risk / evaluation) and challenges it — no rubber-stamping.
- Committee findings recorded verbatim into minutes with `gate: green|yellow|red` per committee.
- Any committee `red` must be resolved or explicitly carried to the Chairman as a flagged risk before Phase 3.

### Phase 3 — Decide (Chairman votes)

- Chairman reviews the CEO's proposal + committee findings.
- Chairman casts the **final vote**: approve, approve-with-conditions, reject, or defer.
- If the Chairman's vote diverges from the committees' recommendation, `board-director` files an ADR (`kind: board-decision`) recording the divergence and rationale.

### Phase 4 — Commit (Board → agency)

- Update `_meetings/<date>-board-<slug>.md` with: decision verbatim, conditions (if any), action items (each paired with a `taskflow` task ID), Chairman's final vote.
- Mark meeting `status: closed`.
- `vision-doc` updates `_vision/VISION.md` / `_vision/projects/<slug>.md` per the approved strategy/goals.
- Append `{"ts":"<iso>","scope":"board","from":"board-director","to":"chairman","type":"board-decision","note":"<one line>"}` to `chat.jsonl`.

## Prerequisites

- CEO has a pre-read ready (strategy proposal, project-goal proposal, or oversight summary).
- For oversight reviews: close-audit (CAO) and/or close-eval (CEVO) and/or Keeper Test output already exist — the Board reads receipts, it does not commission new work.

If a prerequisite fails, the skill returns `blocked` with a missing-prereq list.

## ADR triggers

- Every Board of Directors meeting that lands a material decision files an ADR in the same turn (`kind: board-decision` or `kind: constitution-amend` if it touches a root document).
- Chairman's vote diverges from committee recommendation → ADR recording the divergence.
- Constitution-amend or other USER-ONLY action taken in-meeting → cite `CONSTITUTION.md §2.2` clause + `Article X` per `AGENTS.md > ## Constitution`.

## Outputs

```
_meetings/<date>-board-<slug>.md   # minutes (meeting-minutes skill owns format, kind: board)
_decisions/ADR-NNNN-<slug>.md       # 1+ — every material Board decision
_vision/VISION.md or projects/<slug>.md  # updated per approved strategy/goals
status.json > tasks[]                # N — one per action item
```

## What you never do

- Convene without the Chairman present and chairing.
- Let a committee chief cast the binding vote — only the Chairman's vote is binding.
- Skip minutes — every Board meeting is a receipt.
- Conflate this with `exec-meeting` (CEO + Chiefs, no Chairman, no group vote).
