# payload-shapes.md — notify payload per event

All payloads share the four required fields: `ts`, `event`, `severity`, `slug`, `note`, `refs`. Additional fields per event below.

## closed-shipped

```json
{
  "ts": "<iso>",
  "event": "closed-shipped",
  "severity": "info",
  "slug": "invoice-splitter",
  "note": "Shipped. 12 artifacts, 1 yellow gate (perf), 0 reds.",
  "refs": ["README.md", "deploy/deploy.md"],
  "metrics": {"phases": 7, "fixLoops": 1, "escalations": 0, "tokens": 184321}
}
```

## closed-blocked

```json
{
  "ts": "<iso>",
  "event": "closed-blocked",
  "severity": "warn",
  "slug": "invoice-splitter",
  "note": "Blocked at verify. CISO red: hardcoded secret in settings.py:12.",
  "refs": ["security/code-audit.md:7", "src/settings.py:12"],
  "inboxItem": "ib-003"
}
```

## task-blocked

```json
{
  "ts": "<iso>",
  "event": "task-blocked",
  "severity": "warn",
  "slug": "invoice-splitter",
  "note": "security · verify blocked after 2 fix-loops. Needs a call on PII scope.",
  "refs": ["security/pentest-report.md:21"],
  "taskId": "t-0014",
  "inboxItem": "ib-004"
}
```

## rem-done

```json
{
  "ts": "<iso>",
  "event": "rem-done",
  "severity": "info",
  "slug": null,
  "note": "REM dreaming: 7 new cross-project patterns, 3 anti-patterns.",
  "refs": ["_memory/MEMORY.md"],
  "delta": {"added": 10, "dropped": 22}
}
```

## gate-red

```json
{
  "ts": "<iso>",
  "event": "gate-red",
  "severity": "warn",
  "slug": "invoice-splitter",
  "note": "Legal · closed-source build contains AGPL dep.",
  "refs": ["legal/licenses.md:§direct-deps"],
  "council": "legal",
  "phase": "document-legal"
}
```

## fix-loop-cap

```json
{
  "ts": "<iso>",
  "event": "fix-loop-cap",
  "severity": "warn",
  "slug": "invoice-splitter",
  "note": "quality · verify hit attempt 3. 3 options waiting in inbox.",
  "refs": ["inbox.json:ib-005"],
  "taskId": "t-0018"
}
```

## worktree-conflict

```json
{
  "ts": "<iso>",
  "event": "worktree-conflict",
  "severity": "warn",
  "slug": "invoice-splitter",
  "note": "Structural conflict on architecture.md between worktrees cto-0 and ciso-0.",
  "refs": ["_worktrees/cto-0/architecture.md", "_worktrees/ciso-0/architecture.md"],
  "worktrees": ["cto-0", "ciso-0"]
}
```

## Validation

- `event` must be one of the seven enumerated values.
- `severity` must be `info` or `warn`.
- `note` ≤ 140 chars.
- `refs` must be non-empty for every `warn` event.
- `slug` may be `null` only for cross-project events (REM, memory consolidation).
