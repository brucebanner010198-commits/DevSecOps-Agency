# Meeting log format

`chat.jsonl` captures every meeting event. Three meeting scopes:

## Executive session (CEO ↔ Chief)

```json
{"ts":"<iso>","scope":"exec","from":"cro","to":"ceo","type":"report","phase":"discovery","gate":"green","artifacts":["research-brief.md"],"note":"wedge: dorms; 3 incumbents; recommend build"}
{"ts":"<iso>","scope":"exec","from":"ceo","to":"engineering-lead","type":"dispatch","phase":"design","note":"architecture + api design"}
{"ts":"<iso>","scope":"exec","from":"ceo","to":"exec","type":"exec-decision","phase":"design","decision":"proceed","note":"CISO gate green"}
{"ts":"<iso>","scope":"exec","from":"ceo","to":"user","type":"escalate","inboxId":"esc-001","note":"Google OAuth credential needed"}
```


## Board of Directors meeting (Chairman ↔ Board ↔ CEO)

```json
{"ts":"<iso>","scope":"board","from":"ceo","to":"board","type":"dispatch","note":"strategy proposal for Q3"}
{"ts":"<iso>","scope":"board","from":"cao","to":"board","type":"report","gate":"green","note":"audit committee: no unaddressed reds"}
{"ts":"<iso>","scope":"board","from":"board-director","to":"chairman","type":"board-decision","decision":"proceed","note":"Chairman approved Q3 strategy"}
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
| `exec-decision`  | CEO-level decision logged                                     |
| `board-decision`  | Board of Directors decision, Chairman's final vote            |
| `fix-loop`        | CEO sent work back to a Chief for another pass                |
| `escalate`        | Item parked in `inbox.json` for user                          |
| `resume`          | User answered; work resuming                                  |
| `handoff`         | Chief handing artifact to another Chief (peer handoff)        |

## Gate vocabulary

`green` · `yellow` · `red` · `n/a`

## Rendering

The command-center artifact reads `chat.jsonl` and renders:
- **Executive-session timeline** (one row per `scope:"exec"` entry) — visible by default; a separate **Board of Directors timeline** renders `scope:"board"` entries when a Board meeting has been convened
- **Council drill-down** (click a Chief's row to expand council chatter)
