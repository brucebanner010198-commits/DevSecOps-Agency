---
name: sdlc-patterns
description: |
  A pack of six SDLC operational patterns ported from Nous Research's
  `hermes-agent` (MIT) after a prompt-injection audit. These are NOT agency
  entry points — they are deep-dive operational references that Execution,
  QA, and Architecture Council specialists invoke when they need a canonical
  step-by-step for debugging, TDD, planning, code-review, or subagent-driven
  implementation.
metadata:
  version: "0.3.2"
  sourceProject: "github.com/NousResearch/hermes-agent"
  sourceLicense: "MIT"
  importedAt: "2026-04-21"
---

# sdlc-patterns — canonical SDLC operational patterns

## Why this exists

The agency has the *organizational* layer (councils, CEO dispatch, OKRs, ADRs, audit, ladder) but specialists still need operational playbooks for the common things: how to debug a test failure from first principles, how to run TDD properly, how to write a plan that survives contact with reality, how to review code before committing, how to drive subagents with two-stage review.

Rather than rewriting those from scratch, this pack ports them from `hermes-agent`'s `skills/software-development/` set — MIT licensed, battle-tested, and independent of the agency's orchestration scaffolding.

## Scope boundary — NOT an entry point

These skills are **invoked by specialists mid-task**, not by the user. The user still talks only to the CEO. Execution / QA / Architecture specialists reach into this pack when they hit one of these situations:

| Situation                                     | Skill                               | Invoked by                                  |
| --------------------------------------------- | ----------------------------------- | ------------------------------------------- |
| Before executing a multi-step task            | `writing-plans` or `plan`           | Lead specialists in any council             |
| Encountering a bug / test failure / anomaly   | `systematic-debugging`              | Execution, QA, SRE specialists              |
| Implementing a feature or bugfix              | `test-driven-development`           | Execution specialists                       |
| Before commit / push / PR                     | `requesting-code-review`            | Execution specialists (pre-handoff to QA)   |
| Dispatching multiple parallel delegates       | `subagent-driven-development`       | Chiefs running parallel specialist sprints  |

## Imports — what was and wasn't ported

**Ported (6):** plan, writing-plans, systematic-debugging, test-driven-development, requesting-code-review, subagent-driven-development.

**Excluded:**
- `skills/red-teaming/godmode` — explicit prompt-injection + jailbreak toolkit (Parseltongue encoding, GODMODE templates, `exec(open(...))` dynamic loading, `auto_jailbreak()` config writer). Violates the agency's adversarial-defense-first (OWASP ASI) stance and the user's "no prompt-injection skills" directive. The agency already ships its own defensive Red-Team Council (CRT) under `councils/red-team/`.
- GitHub operational skills (`skills/github/*`) — redundant with the agency's existing `gh`/`git` usage in shipping flows.
- Runtime framework internals (TUI, gateway adapters, RL environments) — not portable to a skill plugin.

## Audit notes

Each ported skill was scanned for:
- `eval` / `exec(open(...))` of external content → none found.
- `curl | bash` or `wget | sh` patterns → none found.
- Remote config / pattern loading → none found.
- `subprocess(..., shell=True)` with user input → none found.
- Credential-fetching logic → none found.

String matches for `os.system`, `subprocess`, `eval`, `exec` in `requesting-code-review/SKILL.md` are all **documentation** — the skill teaches specialists to *scan for* those patterns, not use them.

## Attribution

These skills are derivatives of `hermes-agent` by Nous Research, MIT licensed (Copyright © 2025 Nous Research). The IP-lineage skill records this provenance for every artifact that cites a pattern from this pack.

Each child `SKILL.md` retains its original `author:` field (usually `Hermes Agent (adapted from obra/superpowers)`); the agency's `ip-lineage` specialist files the full lineage statement at ship time.

## Relationship to existing agency skills

- `taskflow` — still owns the six-state machine + 2-attempt fix-loop cap. `requesting-code-review`'s auto-fix loop is *within* a taskflow attempt, not a replacement.
- `ladder` — still owns the never-give-up escalation. When `systematic-debugging` can't isolate a cause after its 4 phases, the specialist escalates via the ladder (Rung 1 → 2 → 3), not by looping forever.
- `meeting-minutes` — still writes the convening record. `writing-plans` writes the *plan artifact*; the minutes capture the decision to plan.
- `adr` — any skill invocation that results in a material methodology choice (e.g., "use TDD for this feature", "skip code review for this hotfix") files an ADR. These skills don't bypass that.

## Versioning

Pack version tracks the agency version at time of import: **v0.3.2**. When agency skills move forward, this pack stays pinned to the imported hermes-agent snapshot unless re-synced. Any local edit to a ported `SKILL.md` is logged in this README's changelog below.

## Changelog

- **2026-04-21** — Initial import of 6 skills from hermes-agent HEAD. Unmodified except for this README wrapper; frontmatter intact.
