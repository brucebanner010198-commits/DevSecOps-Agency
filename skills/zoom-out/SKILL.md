---
name: zoom-out
description: A short, sharp request pattern for an agent that has just dropped into an unfamiliar area of code or an unfamiliar Council surface. Asks the responder to go up one layer of abstraction and provide a map of the relevant modules and their callers, using the project's CONTEXT.md vocabulary. Owned by the Architecture Council (CTO). The whole skill is one short prompt — it doesn't dispatch other agents, doesn't run multi-stage procedures, doesn't file ADRs. It's a vocabulary-aligning lens that any specialist can drop into mid-task to get oriented faster than reading a directory tree top-to-bottom.
metadata:
  version: "1.0.0"
  ratified: "2026-04-26"
  shipped_with_plugin: "0.6.1"
disable-model-invocation: true
---

# zoom-out

## When to invoke

Drop this skill into any conversation when one of these holds:

- An agent has just been dispatched into a code area it hasn't touched before and the directory tree alone isn't telling it the shape of the system.
- A council file or skill references concepts that the convening agent doesn't yet have a mental model for, and reading the file linearly is producing low-yield understanding.
- A debug or diagnose session has narrowed the question to a specific function but the wider call-graph context is missing.
- Cross-council work where the inviting council's vocabulary is unfamiliar and quick orientation is needed before substantive work begins.

If the answer is already obvious from a single file, skip this skill — it's overhead. The skill earns its keep when one layer up genuinely changes the shape of what's being looked at.

## The whole prompt

```
I don't know this area of code well. Go up a layer of abstraction.
Give me a map of all the relevant modules and their callers, using the project's
CONTEXT.md vocabulary. Note any ADRs in _decisions/<slug>/adrs/ that constrain
this area. If a term used in the local file conflicts with the canonical
definition in CONTEXT.md, surface the conflict — don't silently translate.
```

## Why it's this short

Skills in the Agency tend to be procedures. This one is a request pattern. Its value is:

1. **Naming the operation**. "Zoom out" is the convention; once it's a named operation, agents reach for it more readily than they would reach for *"please summarize this section's role in the broader system"*.
2. **Standardizing the vocabulary lens**. The "use CONTEXT.md vocabulary" instruction routes the response through the project's ubiquitous language, not whatever the responder's default phrasing would be.
3. **Surfacing ADR constraints**. The "note any ADRs in this area" instruction means the responder doesn't accidentally reintroduce a previously-rejected pattern.
4. **Catching language drift**. The "surface the conflict" instruction means a local file using outdated terminology is flagged, not silently auto-translated.

The skill is intentionally not a multi-step procedure. Multi-step procedures for orientation-tasks are over-engineering — the request pattern itself does the work.

## Frontmatter note

`disable-model-invocation: true` is set so the skill does not auto-trigger on every "I don't know this area" thought. Specialists invoke it explicitly when they want the framing applied. Auto-invocation would be noise.

## Anti-patterns

- **Using `zoom-out` when the answer is already in a single file.** Read first. This skill is for cases where one file isn't enough.
- **Using `zoom-out` to avoid doing the work of orientation.** It's a lens to apply during real reading, not a substitute for reading.
- **Quoting the responder's `zoom-out` answer in a final artifact.** The map is for the requester's understanding; if it belongs in a final artifact, write it fresh in the artifact's voice.

## Interaction with other skills

| Skill | How `zoom-out` composes |
|---|---|
| `grill-with-docs` | When the grilling session reveals that the convening Specialist doesn't have orientation in the area being grilled, drop into `zoom-out` to get the map, then resume grilling. |
| `improve-codebase-architecture` | The exploration step (Step 1) of that skill effectively does a zoom-out as part of its broader walk; this skill is the lighter-weight, single-question version. |
| `incident-response` | When an incident is narrowed to an unfamiliar subsystem, `zoom-out` orients the responder fast before deep diagnosis. |
| `code-review` | When reviewing a PR that touches an unfamiliar module, `zoom-out` first to know what the change is in the context of. |

## Provenance

- **John Ousterhout**, *A Philosophy of Software Design* (2nd ed., 2021) — the principle that "modules should be deep" (a lot of behavior behind a small interface) means the layer above any specific function carries information the function alone doesn't expose; zooming out is how you find it.
- **Eric Evans**, *Domain-Driven Design* (2003) — the ubiquitous language motivation for routing the response through `CONTEXT.md` vocabulary.
- The `mattpocock/skills` repository (MIT, 2026) is the curator that surfaced the named "zoom-out" request pattern to the Agency in the v0.6.1 cycle. The skill above is Agency-original synthesis with the additional ADR-surfacing and language-conflict instructions specific to the Agency's discipline.
