# skills/ — rules for every skill

Telegraph. Read before authoring or editing a skill.

## File shape

- `skills/<name>/SKILL.md` with YAML frontmatter: `name`, `description`, `metadata.version`.
- `name` in frontmatter == directory name.
- `description` ≥ 2 sentences. Start: "This skill should be used when...". List trigger phrases.
- SKILL.md ≤ 200 lines. Move detail to `references/`.

## Progressive disclosure

- SKILL.md: what the skill does, when to trigger, top-level steps. No tables of knob defaults.
- `references/*.md`: exact knob values, schemas, recipes, edge cases.
- Link references explicitly from SKILL.md (`See references/foo.md`).

## Content rules

- Rules > prose. Bullets > paragraphs.
- Every instruction is either an imperative or an assertion.
- No "might", "could", "consider". Use "must", "does", "never".
- Frontmatter `description` is the router — it must contain enough keywords to trigger on the right user utterances.

## Versioning

- `metadata.version` follows semver. Bump on contract changes (schema, artifact paths, trigger phrases).
- Plugin root `plugin.json.version` bumps when ≥ 1 skill bumps.

## Skill index (v0.3.0-alpha.5)

| Skill              | Trigger                                                 |
| ------------------ | ------------------------------------------------------- |
| `ceo`              | Main entry point. `/devsecops-agency:ceo`.              |
| `ship-it`          | Legacy v0.1 pipeline.                                   |
| `command-center`   | Dashboard artifact.                                     |
| `board-meeting`    | Power-user re-run of a board phase.                     |
| `council-meeting`  | Power-user re-run of a council.                         |
| `intake`           | Q&A only, no engineering.                               |
| `status`           | Text summary.                                           |
| `escalate`         | Process parked questions.                               |
| `retro`            | Post-deploy retro + REM dreaming trigger.               |
| `memory`           | Read/write durable memory (Light/Deep/REM) with novelty gate. v0.3.0 extends read path to ADRs + meetings. |
| `session-log`      | Per-agent append-only JSONL.                            |
| `gates` (internal) | Gate vocabulary + aggregation. CEO invokes on report.   |
| `taskflow` (internal) | Task state machine + fix-loop cap. CEO invokes on dispatch/report. |
| `worktree` (internal) | Isolated scratch dirs for parallel + fix-loop dispatches. CEO invokes on dispatch/report. |
| `skill-creator`    | Runtime roster extension — author new agents + skills. CEO invokes on domain gap. |
| `model-tiering`    | Per-agent tier assignment (Haiku/Sonnet/Opus). CEO reads on every dispatch. |
| `notify`           | Push-notify surface on close/block/REM. Rate-limited.   |
| **`vision-doc`** (v0.3.0) | Workspace VISION.md — mission + ≤ 5 OKRs + ≤ 5 non-goals. 3-bullet slice prepended to every dispatch. |
| **`okr`** (v0.3.0) | Per-project OKR derivation, per-report scoring, quarter roll-up. CEO invokes on every report. |
| **`adr`** (v0.3.0) | Decision receipts (`_decisions/ADR-NNNN-*.md`). CEO invokes on every material decision trigger. |
| **`meeting-minutes`** (v0.3.0) | Durable minutes for user / board / blocking-council / red-team / audit / retro convenings. |
| **`idea-pipeline`** (v0.3.0 Wave 2) | 4-stage portfolio ideation: raw → screened → ranked → top-5. CEO invokes on "what next" / quarter / REM / empty-backlog. |
| **`user-meeting`** (v0.3.0 Wave 2) | 4-phase CEO ↔ user selection flow (brief → present → capture → commit). Only structured convening with user. |
| **`market-intel`** (v0.3.0 Wave 2) | Canonical shapes for market artifacts. Parsed by section header; readers fail-fast on schema drift. |
| **`positioning`** (v0.3.0 Wave 2) | Messaging canvas + narrative-score rubric. Consumed by opportunity-ranker, top-5 one-pager, comms-writer. |
| **`roster`** (v0.3.0 Wave 3) | Living agent registry + hire/fire/tier-change/repurpose lifecycle. COO-owned. Every mutation files an ADR. |
| **`audit`** (v0.3.0 Wave 3) | Independent paper-trail integrity — close-audit (every ship) + portfolio-audit (per quarter) + incident / pre-release audits. |
| **`capacity`** (v0.3.0 Wave 3) | Per-agent + per-council utilization bands + KR coverage gaps. Feeds roster-manager and idea-pipeline pre-flight. |
| **`ladder`** (v0.3.0 Wave 4) | 8-rung never-give-up resilience ladder. Fix-loop = Rung 1; every rung transition files an ADR; Rung 7 parking lot preserves artifacts for later revival. |
| **`eval`** (v0.3.0 Wave 5) | Close-eval + portfolio regression + benchmark-sweep + compaction. Derives eval items from PKRs (never from shipped artifacts). 5 pp regression threshold. Regression baseline freezes per quarter. |
| **`budget`** (v0.3.0 Wave 5) | Per-project token + $ budget with per-phase allocation, burn tracking on every Chief report, and Rung 6 escalation on cumulative > 110 %. 4 size classes (small / medium / large / custom). |
