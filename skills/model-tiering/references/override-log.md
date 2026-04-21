# override-log.md — runtime tier overrides

Append-only. One entry per override. Newest at bottom.

## Entry shape

```
<iso-ts> · <project-slug> · <agent> · <from>→<to> · <reason, ≤ 140 chars> · task: <t-NNNN>
```

## When to write an entry

- A Chief upgrades a specialist for a specific project run.
- The CEO downgrades a Chief to Haiku for a trivial project (**forbidden** — document the denial instead).
- `skill-creator` authors a new agent with a non-default tier; record the decision here.

## Example

```
2026-04-20T14:02:11Z · invoice-splitter · threat-modeler · haiku→sonnet · crypto-heavy backend + webhook signing extend STRIDE depth · task: t-0012
```

## Rules

- Never edit a line. Append a correction entry if wrong.
- Cite the task id (`t-NNNN`) so the override is traceable through `status.json > tasks[]` + `_sessions/<agent>/*.jsonl`.
- An override expires with the project. Next project starts at the default tier.
