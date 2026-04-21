---
name: notify
description: >
  This skill should be used when the agency needs to surface a notification
  to the user — project close, blocked-task escalation, REM dreaming
  completion, long-running phase exits, or any event the user would want to
  know about even if they're not watching the command-center. Trigger
  phrases: "notify me when this ships", "ping me on escalations",
  "push-notify done", "send completion", "alert on blocked". Also trigger
  internally from the `ceo` skill at project close, on `inbox.json` writes,
  and on `/devsecops-agency:retro` completion.
metadata:
  version: "0.1.0"
---

# notify — push-surface for the agency

Single, deduplicated surface for "the agency wants your attention". Hooks into Cowork/Claude Code `Stop` and `SubagentStop` event surfaces when available; falls back to a terminal-visible line in the CEO's final reply when not.

## Events that trigger a notify

| Event                              | Source                         | Severity |
| ---------------------------------- | ------------------------------ | -------- |
| Project closed, shipped            | `ceo > ### 5. Close-out`        | info     |
| Project closed, blocked            | `ceo` + `inbox.json` escalate   | warn     |
| Task transitions to `blocked`      | `taskflow` state machine        | warn     |
| REM dreaming completed             | `retro` skill + `memory` REM    | info     |
| Blocking-council red unwaived      | `gates` aggregation             | warn     |
| Fix-loop attempt 3 (forced block)  | `taskflow` fix-loop cap         | warn     |
| Worktree merge conflict (structural) | `worktree` merge algo         | warn     |

## Transport

Probe in order; use the first available:

1. **Cowork `Stop` / `SubagentStop` hook.** If the plugin is running inside Cowork and the `Stop` or `SubagentStop` hook surfaces are configured for notifications, emit there. See `references/hook-wiring.md`.
2. **Desktop push.** If Claude Code desktop push notifications are enabled, emit via the settings surface.
3. **Fallback.** A single line at the top of the CEO's final reply, prefixed with `[notify]`.

The notify skill never writes to `chat.jsonl` or `_sessions/` — those are already captured. It only emits the user-facing surface.

## Payload

Every notify entry is a four-field record:

```json
{
  "ts": "<iso>",
  "event": "closed-shipped | closed-blocked | task-blocked | rem-done | gate-red | fix-loop-cap | worktree-conflict",
  "severity": "info | warn",
  "slug": "<project-slug>",
  "note": "<one line, ≤ 140 chars>",
  "refs": ["<file:line>", "..."]
}
```

- `event` is one of the enumerated values above. No ad-hoc strings.
- `note` is user-facing: plain English, no agent-internal jargon.
- `refs` are clickable repo-relative paths (e.g. `security/pentest-report.md:42`).

## Dedupe

- Never emit the same `(event, slug, note)` twice inside a single session. Track last-sent in memory.
- If the same event fires again for the same slug, append a counter: `"... (2nd time)"`.
- Escalate severity to `warn` on the 2nd occurrence of any `info` event.

## Rate limit

Hard cap: **5 notifies per project run**. Further notifies merge into a single "digest" note at the next phase boundary. This prevents the agency from becoming a pager.

## Opt-out

If the user says "stop pinging me", "quiet mode", or sets `status.json > notifications.optOut: true`, the skill suppresses all transports except the `[notify]` fallback on the final CEO reply at close.

## Integration with CEO

The `ceo` skill calls notify at:

- **Close-out** (any state): emit `closed-shipped` or `closed-blocked`.
- **Escalation** (after `inbox.json` append): emit `task-blocked` or `gate-red` with the inbox item id.
- **Retro** (after REM dreaming): emit `rem-done` with the `_memory/MEMORY.md` change count.

The `taskflow` skill calls notify at:

- Fix-loop attempt 3 → `fix-loop-cap` warn.

The `worktree` skill calls notify at:

- Structural conflict on merge → `worktree-conflict` warn.

## Progressive disclosure

- `references/hook-wiring.md` — Cowork / Claude Code hook surfaces and config snippets.
- `references/payload-shapes.md` — full JSON schema + worked examples for each event.
- `references/rate-limit.md` — dedupe, digest, and opt-out behaviour.
