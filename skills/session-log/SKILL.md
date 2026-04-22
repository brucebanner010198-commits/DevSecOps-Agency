---
name: session-log
description: >
  This skill should be used whenever the agency needs a durable, grep-addressable
  record of an agent's work across projects and sessions. Every Chief and
  specialist dispatched by the CEO writes an append-only JSONL entry per
  dispatch and per report; the skill also exposes replay recipes for
  cross-project analysis. Trigger phrases: "show me what market-researcher has
  concluded across projects", "replay the CISO's recent decisions", "what did
  we say about OAuth last time", or internal invocation by the `ceo`,
  `board-meeting`, and `council-meeting` skills after every dispatch.
metadata:
  version: "0.1.0"
---

# session-log — per-agent append-only transcripts

Ported pattern from openclaw's `skills/session-logs/SKILL.md`. JSONL, grep-addressable, no runtime. Complements `chat.jsonl` (which is per-project, meeting-oriented) with a per-agent, cross-project view.

## Storage layout

```
/sessions/loving-adoring-maxwell/mnt/outputs/devsecops-agency/_sessions/
├── sessions.json                  # index across all agents
└── <agentId>/
    ├── sessions.json              # per-agent index
    └── <sessionId>.jsonl          # one JSON object per line, append-only
```

`<agentId>` = the subagent_type name: `ceo`, `cro`, `market-researcher`, `security-lead`, `threat-modeler`, etc.
`<sessionId>` = a random short hex (12 chars). One session ID per *project* per *agent*. An agent reused across two projects has two sessions.

## JSONL entry shape

One JSON object per line:

```json
{
  "ts": "<iso>",
  "agentId": "market-researcher",
  "sessionId": "a4f1c09b22e8",
  "projectSlug": "invoice-splitter",
  "phase": "discovery",
  "type": "dispatch | report | handoff | note | error",
  "from": "cro",
  "to": "market-researcher",
  "artifact": "research/market.md",
  "gate": "green | yellow | red | n/a",
  "tokens": { "in": 1234, "out": 512 },
  "note": "one-line summary"
}
```

Fields:
- `ts` — ISO 8601 with seconds.
- `type` — limited vocabulary: `dispatch` (Chief dispatches specialist), `report` (specialist reports back), `handoff` (artifact crosses council boundaries), `note` (in-flight observation worth keeping), `error` (dispatch or tool failure).
- `gate` — only meaningful on `report` entries; otherwise `n/a`.
- `tokens` — optional, fill when known; empty object otherwise.
- `note` — ≤ 120 chars, one sentence, no ellipsis.

## Index files

### Per-agent `sessions.json`

```json
{
  "agentId": "market-researcher",
  "sessions": [
    {
      "sessionId": "a4f1c09b22e8",
      "projectSlug": "invoice-splitter",
      "startedAt": "<iso>",
      "endedAt": "<iso>",
      "messageCount": 6,
      "gates": {"green": 1, "yellow": 0, "red": 0}
    }
  ]
}
```

### Global `_sessions/sessions.json`

```json
{
  "lastUpdated": "<iso>",
  "totals": {"agents": 29, "sessions": 142, "entries": 1087},
  "byProject": {
    "invoice-splitter": ["ceo","cro","market-researcher","...","gc"]
  }
}
```

Both refreshed at every dispatch + report. Cheap to keep current.

## Write contract (who writes, when)

Written by the dispatching agent **before** and by the reporting agent **after**:

| Trigger                                    | Writer             | Entry type |
| ------------------------------------------ | ------------------ | ---------- |
| CEO dispatches a Chief                     | ceo                | `dispatch` |
| Chief reports back to CEO                  | ceo                | `report`   |
| Chief dispatches a specialist              | chief              | `dispatch` |
| Specialist reports back to Chief           | chief              | `report`   |
| Artifact promoted across council boundary  | receiving Chief    | `handoff`  |
| Tool error during dispatch                 | dispatching agent  | `error`    |
| Mid-run observation worth saving           | any                | `note`     |

Writer responsibility means only one agent writes each entry — no duplicates.

## Read path

See `references/replay-recipes.md`. Three canonical queries:

- **"What has agent X concluded across all projects?"**
- **"Show all Critical/High gates from CISO in the last 30 days."**
- **"Reconstruct the full CEO transcript for project Y."**

All answerable with `rg` + `jq`. No runtime needed.

## Log size + rotation

- Soft cap 2 MB per `<sessionId>.jsonl`. A single specialist session rarely exceeds 200 entries; if you hit the cap, something is wrong (fix-loop gone feral — escalate, don't rotate).
- No rotation in v0.1. Sessions are closed when the project closes; they stay readable forever.
- If `_sessions/` exceeds 100 MB total, notify the CEO; the user may want to archive old projects.

## Integration with the CEO skill

The CEO playbook writes exactly these entries in order:

1. **Project init** → write `note` entry: `"session opened"` on own session.
2. **Each phase dispatch** → write `dispatch` entry on CEO session AND on Chief session (mirror).
3. **Each Chief report** → write `report` entry on CEO session AND on Chief session (mirror).
4. **Project close** → write `note` entry: `"session closed, shipped"` OR `"session closed, blocked"`.

Chief playbooks mirror the same pattern for specialist dispatches.

## Relationship to `chat.jsonl`

- `chat.jsonl` = per-project, for the command-center. Keep rendering from there.
- `_sessions/` = per-agent, cross-project, for replay and memory-feeding. This is new.

Both can be written from a single helper in practice. Overlap is fine — they're authoritative for different questions.

## Relationship to `runtime-hooks/session-logger/`

The runtime hook writes a separate, **minimal** JSONL file (`.github/logs/copilot/session-logger/log.jsonl`) at three events: session-start, each prompt, session-end. It is intentionally small and does not mirror the per-agent schema above.

- `_sessions/*.jsonl` — agency-internal orchestration trail. Written by dispatching + reporting agents inside the CEO / Chief / specialist loop.
- `.github/logs/copilot/session-logger/log.jsonl` — runtime-boundary trail. Written by the shell hook outside the agent.

The two are never merged. Cross-reference is by timestamp if a CAO audit needs to correlate them.

## Progressive disclosure

- `references/replay-recipes.md` — canonical `rg`/`jq` queries
