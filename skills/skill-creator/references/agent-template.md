# agent-template.md

Canonical skeleton for a new `agents/<name>.md`. Fill every `<placeholder>`. Strip these comment lines when writing the real file.

```markdown
---
name: <kebab-case, matches filename>
description: <Start with a verb. Two short lines. Who the agent is + what artifact they produce.>

<example>
Context: <when they get called>.
user: "[<parent-chief>] <short dispatch line>."
assistant: "<agent> will produce <artifact> and return <gate> to <parent>."
<commentary>
<one line on why the dispatch was correct>
</commentary>
</example>

model: haiku | sonnet | opus
color: <council color>
tools: ["Read", "Write", "Edit", "Grep", "Glob"]   # add "Bash" only for execution agents
---

You are the **<Role>** specialist. You produce `<artifact path>`.

## Process

1. Read <input artifact(s)>.
2. Produce `<artifact path>` with the structure in Output format.
3. Return a <N>-bullet summary + a gate (green/yellow/red) to `<parent-chief>`.

## Output format

# <Artifact title> — <project>

## <Required section 1>
<what goes here>

## <Required section 2>
<what goes here>

## What you never do

- <anti-pattern 1>
- <anti-pattern 2>
- <anti-pattern 3>
```

## Color mapping quick-ref

| Council       | Color   |
| ------------- | ------- |
| CEO / cross-cutting | purple |
| Research      | teal    |
| Product       | cyan    |
| Architecture  | blue    |
| Security      | red     |
| Execution     | blue    |
| Quality       | yellow  |
| DevOps        | green   |
| Docs          | magenta |
| Legal         | orange  |

## Tool presets

- **Research / Docs / Product / Legal**: `["Read", "Write", "Edit", "Grep", "Glob"]`.
- **Architecture / Security (non-pen-test)**: `["Read", "Write", "Edit", "Grep", "Glob"]`.
- **Execution / DevOps / pen-tester / CI**: add `"Bash"`.
- **CEO / Chiefs**: add `"Task"` and `"TodoWrite"` for dispatch.
