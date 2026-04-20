---
name: board-meeting
description: >
  This skill should be used when the CEO needs to hold a structured board meeting
  with one or more Chiefs — either to brief them on the next phase or to collect
  their reports at the end of a phase. Trigger phrases include "convene the board",
  "run a board meeting", "call in the chiefs", "phase kickoff", "phase close". Also
  trigger when the user invokes /devsecops-agency:board-meeting. Produces a single
  board-decision entry in chat.jsonl and updates status.json. Not a user-facing
  skill — the CEO uses it internally; advanced users may invoke directly to
  re-run a phase or replay a meeting.
metadata:
  version: "0.2.0"
---

# board-meeting — structured Chief orchestration

This skill is a thin wrapper around the Task tool that enforces a board-meeting contract: parallel/sequential dispatch, gate-signal capture, structured logging.

## When to use

Called by the `ceo` skill (internally) at the start and end of each phase. Can also be invoked directly by a power user who wants to re-run a specific phase without going through the full CEO orchestration.

## Contract

Every board meeting has:
- **Phase** (`discovery`, `design`, `build`, `verify`, `ship`, `document-legal`, `close`)
- **Agenda** (one-liner — what needs to be decided or produced)
- **Invitees** (list of Chief agent names)
- **Parallelism** (`sequential` or `parallel`)
- **Expected artifacts** (list of file paths)

## Process

1. **Open the meeting.** Append to `chat.jsonl`:
   ```json
   {"ts":"<iso>","scope":"board","from":"ceo","to":"board","type":"dispatch","phase":"<phase>","note":"<agenda>","invitees":[...]}
   ```

2. **Dispatch Chiefs.** Use the Task tool, one call per Chief (in parallel if permitted). Prompt template:

   ```
   You are {chief-name}, attending a board meeting chaired by the CEO.
   Phase: {phase}
   Agenda: {agenda}
   Project folder: {project-path}

   Read these artifacts before you start:
   - {input-artifact-1}
   - {input-artifact-2}

   Produce:
   - {output-artifact-1}
   - {output-artifact-2}

   Return to the CEO a 3-bullet summary + your gate signal (green/yellow/red) + any ask.
   ```

3. **Collect reports.** For each Chief response, append:
   ```json
   {"ts":"<iso>","scope":"board","from":"<chief>","to":"ceo","type":"report","phase":"<phase>","gate":"<g/y/r>","artifacts":[...],"note":"<summary>"}
   ```

4. **Consolidate.** The CEO reviews:
   - Any `red` gate → fix-loop (max 2) or escalate
   - Any `yellow` gate → CEO decides: accept with note, fix-loop, or escalate
   - All `green` → proceed

5. **Close the meeting.** Append:
   ```json
   {"ts":"<iso>","scope":"board","from":"ceo","to":"board","type":"board-decision","phase":"<phase>","decision":"proceed|fix-loop|escalate","note":"<one line>"}
   ```

6. **Update `status.json`** with phase advancement / blockers.

## Phase spec reference

See the `ceo` skill's `references/board-phases.md` for the canonical phase table (inputs, Chiefs, artifacts, exit criteria).

## What you never do

- Dispatch a Chief without the input artifacts path list — they will hallucinate
- Skip the board-decision entry — the command center needs it to render the phase transition
- Silently advance past a red gate
