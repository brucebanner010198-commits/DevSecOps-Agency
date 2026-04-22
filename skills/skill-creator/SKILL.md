---
name: skill-creator
description: >
  This skill should be used when the CEO hits a domain the current 16 councils
  don't cover (cryptography, game-dev, mobile, embedded, ML, niche compliance
  regime) and needs to extend the agency's roster at runtime. It authors new
  agent files and new skill files that comply with `agents/AGENTS.md` and
  `skills/AGENTS.md`. Trigger phrases: "create a new agent", "add a specialist
  for X", "we need a skill for Y", "extend the roster", "author a skill",
  "bootstrap a new agent". Also trigger when the CEO explicitly invokes the
  `skill-creator` subagent.
metadata:
  version: "0.1.0"
---

# skill-creator — runtime roster extension

Author new `agents/<council>/<name>.md` and `skills/<name>/SKILL.md` files so the agency can cover a domain its 16 councils don't. Returns new file paths to the CEO. Does not dispatch the new agents itself.

## When to trigger

- CEO dispatch note: "no existing specialist covers \<domain\>".
- User asks for work that pattern-matches an undefined role (mobile dev, smart-contract auditor, game designer, ADA auditor, SOC2 evidence-pack writer).
- An existing agent needs a new named capability (e.g. `a11y-auditor` needs an `ada-audit` checklist skill).

## Output kinds

| Kind       | When                                                          | Path                                |
| ---------- | ------------------------------------------------------------- | ----------------------------------- |
| agent      | Distinct role the agency will repeatedly dispatch             | `agents/<council>/<name>.md`        |
| skill      | New capability owned by an existing agent                     | `skills/<name>/SKILL.md` (+ refs)   |
| both       | Domain needs both a persona and a repeatable procedure        | both of the above                   |

## Process

1. **Read scope rules first.** In order:
   - `agents/AGENTS.md` — file shape, council color map, dispatch/report contract.
   - `skills/AGENTS.md` — file shape, progressive disclosure, versioning.
   - `councils/<council>/AGENTS.md` if the new agent joins an existing council.
2. **Decide output kind** (agent, skill, or both) per the table above.
3. **Decide council assignment.** Reuse an existing council's color + add the specialist to its `AGENTS.md` and to `skills/ship-it/references/status-schema.md > team.<council>.specialists`. If cross-cutting, use `purple` and report to CEO directly.
4. **Decide model tier** per `skills/model-tiering/SKILL.md`: Opus for CEO-class only; Sonnet for Chiefs and cross-cutting authors (including `skill-creator` itself); Haiku for specialist output.
5. **Author the agent file** following `references/agent-template.md`. Frontmatter fields only: `name`, `description`, `model`, `color`, `tools`. Body: `## Process`, `## Output format`, `## What you never do`.
6. **Author the skill file** (if required) following `references/skill-template.md`. Frontmatter: `name`, `description` (≥ 2 sentences starting with "This skill should be used when..."), `metadata.version: "0.1.0"`. Body ≤ 200 lines; detail in `references/`.
7. **Refuse on collision.** If `agents/<council>/<name>.md` or `skills/<name>/SKILL.md` already exists, abort and return `note: "collision"` with the existing path.
8. **Return to CEO.** One block per new file: `file:`, `kind:`, `summary:`. The CEO reviews and runs the first dispatch.

## Content rules

- Imperatives only. "Must", "does", "never". No "might / could / consider".
- Rules and bullets. No multi-sentence prose paragraphs.
- Every agent gets a `## What you never do` block with ≥ 3 anti-patterns.
- Every skill description starts "This skill should be used when..." and lists ≥ 3 trigger phrases.
- Never grant `Bash` to a non-execution agent.

## Reserved names

Do not create agents with these reserved names: `ceo`, `cro`, `pm-lead`, `engineering-lead`, `security-lead`, `qa-lead`, `devops-lead`, `docs-lead`, `gc`, `cmo`, `cso`, `coo`, `cao`, `evaluation-lead`, `red-team-lead`, `sre-lead`, `skill-creator`.

## Integration with CEO

The CEO playbook invokes skill-creator when:

- A dispatch would require a subagent type not present in `status.json > team.<council>.specialists`.
- The user asks for a domain skill not present in `skills/` (checked by `ls` first).

After skill-creator returns, the CEO:

1. Reads the new file(s) and checks them against `agents/AGENTS.md` / `skills/AGENTS.md` rules.
2. If compliant, commits them (in-session write is enough) and updates `status.json > team.<council>.specialists` for new agents.
3. Updates `skills/AGENTS.md > ## Skill index` if a new skill was authored.
4. Dispatches the new agent or invokes the new skill as normal.

## Progressive disclosure

- `references/agent-template.md` — canonical agent file skeleton.
- `references/skill-template.md` — canonical skill file skeleton + `references/` layout.
- `references/collision-policy.md` — what to do on name collision (refuse vs version bump).
