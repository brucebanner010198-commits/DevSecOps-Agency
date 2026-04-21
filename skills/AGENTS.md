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

## Skill index (v0.2.1)

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
| `memory`           | Read/write durable memory (Light/Deep/REM).             |
| `session-log`      | Per-agent append-only JSONL.                            |
