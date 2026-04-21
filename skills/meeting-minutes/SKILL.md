---
name: meeting-minutes
description: >
  This skill should be used whenever the agency holds a **meeting** — a
  synchronous decision-making moment with ≥ 2 attendees (humans or agents).
  It writes durable minutes in `_meetings/<date>-<kind>.md` with attendees,
  agenda, discussion, decisions, and action items. The CEO invokes it for:
  (1) board meetings (CEO + Chiefs on phase transitions); (2) council
  meetings (Chief + specialists); (3) user meetings (CEO + user — top-5
  idea pitch, ETA commit, scope review); (4) red-team councils (future Wave 6);
  (5) audit reviews (future Wave 3 CAO); (6) any other formally convened
  discussion. Trigger phrases: "write the minutes", "minutes of", "meeting
  notes", "document this discussion", "convene council — document it", or
  internal invocation by the `ceo`, `board-meeting`, or `council-meeting`
  skills. Part of Wave 1 of v0.3.0 — the company release.
metadata:
  version: "0.1.0"
---

# meeting-minutes — durable record of every convening

Every meeting leaves a trail. The trail is machine-greppable, human-readable, and audit-ready.

## Storage layout

All minutes live under `/sessions/loving-adoring-maxwell/mnt/outputs/devsecops-agency/_meetings/`:

```
_meetings/
├── YYYY-MM-DD-<kind>.md           # one file per meeting
├── YYYY-MM-DD-<kind>-<suffix>.md  # if multiple meetings of same kind same day
└── INDEX.md                        # generated: date, kind, attendees, decisions
```

`<kind>` is one of: `user`, `board`, `council-<council-slug>`, `red-team`, `audit`, `retro`.

Suffixes are `-am`/`-pm` or `-1`/`-2` if multiple meetings of the same kind happen the same day.

## Minutes file format

Exactly this shape, every meeting:

```markdown
# Meeting minutes — <YYYY-MM-DD> — <kind>

- **Kind:** user | board | council-<slug> | red-team | audit | retro
- **Started:** YYYY-MM-DD HH:MM (UTC)
- **Ended:** YYYY-MM-DD HH:MM (UTC)
- **Chair:** <actor>
- **Scribe:** <actor> (same as chair unless specified)
- **Project:** <slug> | workspace
- **Related:** ADR-NNNN, _vision section, prior meeting filename

## Attendees

- <role> · <actor-slug> — present | absent | partial
- ...

## Agenda

1. <topic>
2. <topic>

## Discussion

### <topic 1>
<3–8 bullets. What was raised, by whom. Cite artifacts with file paths.>

### <topic 2>
<...>

## Decisions

- **D1** — <decision, one line> — ADR-NNNN (if ADR filed)
- **D2** — <decision, one line> — no ADR (explain: routine, not a trigger)

## Action items

- **A1** — <action> — owner: <slug> — due: YYYY-MM-DD — task: <task-id in status.json>
- **A2** — ...

## Open questions

- <question carried to next meeting>
```

Cap: **180 lines of markdown per meeting.** Meetings longer than that fracture into topic-specific minutes.

## Six meeting kinds (as of v0.3.0)

### `user`
CEO + the user. Top-5 idea pitch, ETA commit, scope review, retro review, escalations from `inbox.json`. Mandatory minutes for every user meeting regardless of length.

### `board`
CEO + a subset of Chiefs. Phase transitions. Mandatory minutes if ≥ 2 Chiefs convened simultaneously. Single-Chief phase reports go to `chat.jsonl > board-decision` instead and DO NOT need a minutes file.

### `council-<council-slug>`
Chief + their specialists. Scope planning, fix-loop triage, waiver consideration. Mandatory minutes if the council is **blocking** (security, legal) or if a waiver is considered. Informing councils (product, devops, qa, docs, research) log to `chat.jsonl` only unless convened for waiver consideration.

### `red-team` (Wave 6 preview)
CISO + red-team agents. Mandatory minutes.

### `audit` (Wave 3 preview)
CAO + audit specialists. Mandatory minutes.

### `retro`
CEO + user (or CEO alone) at project close. Mandatory minutes.

## Invocation flow

**Before the meeting starts** (if the CEO knows it's about to happen):
1. Allocate the filename: `_meetings/<today>-<kind>[-suffix].md`.
2. Write the header block with `Started:` timestamp, Chair, Project, Attendees list.
3. Write the Agenda block before the meeting opens.

**During the meeting:**
- Append to Discussion as topics resolve.
- Decisions are written immediately as they land (not retrocon'd).
- Action items reference task IDs that will be created via `taskflow`.

**After the meeting ends:**
1. Write `Ended:` timestamp.
2. For each `D<n>` row, if an ADR was required by `adr/references/decision-triggers.md`, file the ADR and put its number next to the decision.
3. For each `A<n>` row, create the task via `taskflow` and write the task ID into the minutes.
4. Update `_meetings/INDEX.md` by appending a new row.
5. If `kind: user`, write a `scope:"memory"` entry to `chat.jsonl` pointing to the minutes file — makes the command-center surface it.

## INDEX.md shape

Generated on every write. Sorted by date descending, then by filename.

```markdown
# Meetings index

| Date       | Kind              | Project           | Attendees | Decisions | ADRs              |
| ---------- | ----------------- | ----------------- | --------- | --------- | ----------------- |
| 2026-04-22 | user              | workspace         | 2         | 3         | ADR-0008, ADR-0009|
| 2026-04-22 | board             | tracker           | 4         | 2         | ADR-0010          |
| 2026-04-21 | council-security  | tracker           | 5         | 1         | ADR-0011 (waiver) |
```

## Contract with other skills

- **`board-meeting`** — invokes `meeting-minutes` on start, updates on progress, finalises on end.
- **`council-meeting`** — same, but only for blocking councils or waiver-considering sessions.
- **`ceo`** — invokes `meeting-minutes` for every user meeting.
- **`adr`** — any decision in a meeting that fires an ADR trigger is cross-linked (ADR's `Related:` ↔ minutes `Decisions` row).
- **`taskflow`** — every action item becomes a task; minutes store the task ID.
- **`retro`** — reads all meetings in the retro window; surfaces meeting frequency, decision count, unfiled-ADR count.

## Write rules

- **Atomic file creation.** Create at meeting start, not at end. Prevents the "we never wrote minutes" failure mode.
- **Append-only for in-flight sections.** Once a topic is closed, its Discussion section is frozen; new thoughts go into the next topic or the next meeting.
- **Never delete.** Even cancelled meetings (kind: `<kind>` + `Status: cancelled` on the header) stay forever.
- **Redact PII, secrets.** Same rule as `memory`.

## Anti-patterns

- Writing minutes after the fact from memory. Write in-the-moment.
- Minutes with a Decisions section but no Action items. Decisions without owners don't happen.
- Minutes with Action items but no task IDs. Un-tracked actions rot.
- Minutes that exceed 180 lines. Split by topic.
- Skipping minutes on "informal" meetings that nonetheless produced a decision.

## Progressive disclosure

- `references/meeting-kinds.md` — full table of kinds, mandatory vs optional minutes, cadence expectations.
- `references/minutes-template.md` — exact skeleton + 2 worked examples (user meeting + council waiver).
- `references/action-tracking.md` — how action items marry to `status.json > tasks[]`.
