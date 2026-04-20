# Meeting log format

`chat.jsonl` captures every meeting event. Two meeting types:

## Board meeting (CEO ↔ Chief)

```json
{"ts":"<iso>","scope":"board","from":"cro","to":"ceo","type":"report","phase":"discovery","gate":"green","artifacts":["research-brief.md"],"note":"wedge: dorms; 3 incumbents; recommend build"}
{"ts":"<iso>","scope":"board","from":"ceo","to":"engineering-lead","type":"dispatch","phase":"design","note":"architecture + api design"}
{"ts":"<iso>","scope":"board","from":"ceo","to":"board","type":"board-decision","phase":"design","decision":"proceed","note":"CISO gate green"}
{"ts":"<iso>","scope":"board","from":"ceo","to":"user","type":"escalate","inboxId":"esc-001","note":"Google OAuth credential needed"}
```

## Council meeting (Chief ↔ specialist)

```json
{"ts":"<iso>","scope":"council","council":"research","from":"cro","to":"market-researcher","type":"dispatch","artifact":"research/market.md"}
{"ts":"<iso>","scope":"council","council":"research","from":"market-researcher","to":"cro","type":"report","gate":"n/a","artifacts":["research/market.md"],"note":"wedge identified: dorms"}
```

## Type vocabulary

| `type`            | Meaning                                                       |
| ----------------- | ------------------------------------------------------------- |
| `dispatch`        | Sender assigned a task to receiver                            |
| `report`          | Receiver completed and is returning an artifact + gate signal |
| `board-decision`  | CEO-level decision logged                                     |
| `fix-loop`        | CEO sent work back to a Chief for another pass                |
| `escalate`        | Item parked in `inbox.json` for user                          |
| `resume`          | User answered; work resuming                                  |
| `handoff`         | Chief handing artifact to another Chief (peer handoff)        |

## Gate vocabulary

`green` · `yellow` · `red` · `n/a`

## Rendering

The command-center artifact reads `chat.jsonl` and renders:
- **Board timeline** (one row per `scope:"board"` entry) — visible by default
- **Council drill-down** (click a Chief's row to expand council chatter)
