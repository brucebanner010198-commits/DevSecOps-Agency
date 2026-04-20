# Handoff Protocol

How work moves between stages, leads, and specialists.

## Lead ↔ specialist

A **lead agent** never does the detail work itself. It:

1. Reads the inbound artifact
2. Decides which specialists are needed and in what order
3. Dispatches each specialist via the Task tool with a narrowly scoped prompt
4. Reviews the specialist's output against the stage exit criteria
5. If needed, dispatches the specialist again with focused feedback (max 2 rounds)
6. Consolidates the specialists' outputs into the stage artifact
7. Logs the handoff to `chat.jsonl` and updates `status.json`

## Specialist prompt shape

Keep specialist prompts short and tool-grounded. Always include:

- **Project folder path** (absolute)
- **Files to read** (by path)
- **File to produce** (by path)
- **One-line success criterion**
- **Back-reference** to the lead — "When done, return a 3-bullet summary; the lead will integrate."

Specialists should NOT re-dispatch other specialists. That's the lead's job.

## Stage ↔ stage

When a stage completes, the Managing Director (the ship-it skill):

1. Reads the final stage artifact to verify exit criteria
2. Appends a `handoff` entry to `chat.jsonl`:
   ```json
   {"ts":"<iso>","from":"<lead>","to":"<next-lead>","type":"handoff","artifact":"<path>","note":"<1-line status>"}
   ```
3. Updates `status.json.phase` and `status.json.completed`
4. Calls the next lead

## chat.jsonl entry types

| Type        | Meaning                                                   |
| ----------- | --------------------------------------------------------- |
| `handoff`   | Artifact passed from one lead to the next                 |
| `dispatch`  | Lead dispatched a specialist                              |
| `report`    | Specialist returned results to its lead                   |
| `decision`  | Lead resolved ambiguity autonomously (document the call)  |
| `escalate`  | A blocker was parked in `inbox.json`                      |
| `resume`    | Human answered a blocker; pipeline resumed                |
| `fix-loop`  | Lead sent work back to a previous stage for rework        |

## Example chat.jsonl sequence

```jsonl
{"ts":"2026-04-20T10:00:00Z","from":"md","to":"pm-lead","type":"handoff","artifact":"brief.md","note":"intake complete"}
{"ts":"2026-04-20T10:00:05Z","from":"pm-lead","to":"user-researcher","type":"dispatch","note":"personas + JTBD"}
{"ts":"2026-04-20T10:00:45Z","from":"user-researcher","to":"pm-lead","type":"report","note":"3 personas, 5 JTBD"}
{"ts":"2026-04-20T10:00:50Z","from":"pm-lead","to":"spec-writer","type":"dispatch","note":"draft functional spec"}
{"ts":"2026-04-20T10:02:10Z","from":"spec-writer","to":"pm-lead","type":"report","note":"8 acceptance criteria"}
{"ts":"2026-04-20T10:02:15Z","from":"pm-lead","to":"md","type":"report","artifact":"brief.md","note":"PM phase complete"}
{"ts":"2026-04-20T10:02:20Z","from":"md","to":"security-lead","type":"handoff","artifact":"brief.md","note":"ready for threat model"}
```
