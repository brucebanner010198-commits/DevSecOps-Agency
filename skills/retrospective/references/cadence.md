# retrospective/references/cadence.md

The 4 retro kinds, their triggers, attendance, and output path.

## Kind 1: project-close

**Trigger:** every project close. Outcome is `shipped`, `blocked`, or `parked-rung-7`.

**Attendees (required):** `ceo`, `cao`, `cevo`, `crt`. The three informing-council chiefs are here because their close-audit / close-eval / pre-release-red-team outputs are the primary inputs.

**Optional:** the user (Sir), at the user's request via `user-meeting`.

**Output:** `_meetings/<slug>-retro-<YYYY-MM-DD>.md`.

**Cadence:** on every close, no exceptions. Blocked projects and Rung-7 parked projects still retro — the lesson is why they blocked or parked.

## Kind 2: portfolio

**Trigger:** end of quarter, or explicit user request via `/devsecops-agency:retro portfolio`.

**Attendees (required):** `ceo`, `cao`, `user`.

**Optional:** `cso`, `cmo` (for strategy / messaging carry-over checks).

**Output:** `_meetings/portfolio-retro-<quarter>.md`. Example: `_meetings/portfolio-retro-2026-Q2.md`.

**Cadence:** once per quarter. CAO drives the agenda — reads the quarter's `LESSONS.md` rows, rolls up into themes, escalates any "what we'd change" rows that carried over without resolution for > 1 quarter.

## Kind 3: incident

**Trigger:** CSRE declares an incident closed. Examples — model-vendor outage routed via `model-routing`, prod deploy rolled back by `deployment-engineer`, a red-team finding with severity `critical` that required same-turn vault rotation.

**Attendees (required):** `csre`, `ciso`, `ceo`.

**Optional:** the council lead for the affected delivery path.

**Output:** `_meetings/incident-<id>-retro-<YYYY-MM-DD>.md`. Example: `_meetings/incident-INC-0017-retro-2026-04-21.md`.

**Written by:** `csre` (not `ceo`). CSRE reports the retro to CEO; CEO reviews and files an ADR if the retro produces a playbook stone.

**Cadence:** within 48 hours of incident close.

## Kind 4: wave

**Trigger:** a repo-level version ships (v0.3.x → v0.3.y). Example: v0.3.7 Clarity shipping, v0.3.8 Identity+Learning shipping.

**Attendees (required):** `ceo`, `coo`.

**Optional:** the user, for waves that change the user-facing contract.

**Output:** `_meetings/wave-<version>-retro-<YYYY-MM-DD>.md`. Example: `_meetings/wave-0.3.8-retro-2026-04-22.md`.

**Cadence:** within 48 hours of the GitHub release creation.

## Attendance skip rules

- Any required attendee who is unavailable produces a **skip note** in the minutes `## Attendees` line: `"coo (covered by cao due to roster-review overlap)"`.
- ≥ 2 required attendees skipping = abort the retro and file ADR `kind: retro-blocked` with a reschedule trigger. The CAO close-audit holds on the project close until the retro lands.
- The user is never marked as required for project-close retros; their attendance is opt-in via `user-meeting`.

## Preconditions

Retro cannot start until:

| Kind | Preconditions |
| --- | --- |
| project-close | CAO close-audit + CEVO close-eval + CRT pre-release red-team all landed (i.e., their outputs exist at their declared paths) |
| portfolio | every project-close retro of the quarter is landed; the quarter's `LESSONS.md` rows are appended |
| incident | the `notify` event for the incident is resolved; CSRE has published `_vision/audit/<incident-id>.md` |
| wave | the GitHub release is created and the `.plugin` asset is uploaded |

## Output file naming

Telegraph:

- project-close: `_meetings/<slug>-retro-<YYYY-MM-DD>.md`
- portfolio: `_meetings/portfolio-retro-<YYYY>-Q<n>.md`
- incident: `_meetings/incident-<INC-ID>-retro-<YYYY-MM-DD>.md`
- wave: `_meetings/wave-<version>-retro-<YYYY-MM-DD>.md`

The prefix orders retros alphabetically in the meetings directory: incident-, portfolio-, wave-, `<slug>`-.

## Length budgets

| Kind | Words | Read time |
| --- | --- | --- |
| project-close | 800–1200 | 5–8 min |
| portfolio | 1500–2500 | 10–15 min |
| incident | 600–1000 | 4–6 min (needs to be read quickly) |
| wave | 1000–1500 | 7–10 min |
