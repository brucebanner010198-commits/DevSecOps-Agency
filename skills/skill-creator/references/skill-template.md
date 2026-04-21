# skill-template.md

Canonical skeleton for a new `skills/<name>/SKILL.md`. Fill every `<placeholder>`. Strip comment lines.

```markdown
---
name: <kebab-case, matches dir>
description: >
  This skill should be used when <specific condition>. <Follow-up sentence on
  scope or inputs.> Trigger phrases: "<phrase 1>", "<phrase 2>", "<phrase 3>".
  Also trigger when the CEO invokes the <name> skill.
metadata:
  version: "0.1.0"
---

# <name> — <one-line mission>

<1–3 line mission statement. Imperative. No prose paragraphs after this.>

## When to trigger

- <condition 1>
- <condition 2>
- <condition 3>

## Inputs

- <input 1 with path>
- <input 2 with path>

## Outputs

| Output     | Path                       | Shape                  |
| ---------- | -------------------------- | ---------------------- |
| <name>     | `<path>`                   | <markdown / json>      |

## Process

1. <Imperative step>
2. <Imperative step>
3. <Imperative step>

## Rules

- <must>
- <must not>
- <gate heuristic>

## Progressive disclosure

- `references/<name>.md` — <what's in it>
- `references/<name>.md` — <what's in it>
```

## Versioning

- `metadata.version: "0.1.0"` on first write.
- Bump minor on contract change (frontmatter, artifact paths, trigger phrases).
- Bump patch on rule additions that don't break compatibility.

## Progressive-disclosure policy

- SKILL.md ≤ 200 lines.
- Knob defaults, long checklists, schema, recipes → `references/*.md`.
- Every reference must be linked from the SKILL.md body (`See references/foo.md`).

## Skill index registration

After writing the skill, add a row to `skills/AGENTS.md > ## Skill index`:

```
| `<name>` | <one-line trigger> |
```

Keep the table alphabetical after the core skills (ceo, ship-it, command-center, board-meeting, council-meeting, intake, status, escalate, retro, memory, session-log, gates, taskflow, worktree).
