# Baseline 1: the tiered plugin before Phase 1a

Date: 2026-11-22. Plugin: `git archive` of `feat/personal-ai-surface` @ `96fe709`, after Phase W, with the model tiers in effect. Spend: **$3.87** in total, against a $25 cap.

## How it ran

The same three tasks and prompts as Run 1 D1 to D3, each in a fresh directory and a fresh headless session:

- invoked as `/devsecops-agency:ceo <task>`;
- `--model claude-opus-5-5` pinned (see the note on comparability below);
- `--setting-sources project,local` and `--strict-mcp-config`, so the user-level settings, output style and MCP servers were not loaded;
- `--max-budget-usd` caps of $5, $8 and $12, the same as Run 1;
- the same tool allowlist, with `git push` denied;
- a venv with pytest on the PATH, which removes a Run 1 confounder.

**Comparability:** Run 1 billed `claude-fable-5-2` as the main model, and this run billed `claude-opus-5-5`. The dollar figures are therefore not like-for-like. Agent counts and behaviour can be compared.

## Results

| Task | Cost (cap) | Wall time | Agents convened | Model use | Outcome, checked independently |
| --- | --- | --- | --- | --- | --- |
| D1 bug fix | $0.59 ($5) | 22 s | none | Opus 5.5 only | Fixed in one line; 2 of 2 tests pass. The CEO again skipped the pipeline ("one-line fix") |
| D2 feature | $0.70 ($8) | 45 s | none | Opus 5.5 only | `remove()` plus 6 tests; 7 pass and 1 fails. The failure is the pre-existing D1 bug, which the CEO left alone as out of scope and reported. It read the existing code and did not rebuild |
| D3 new app | $1.78 ($12) | 8 min 3 s | `frontend-dev` (1) | Opus 5.5 $1.73; Haiku 5.5 $0.06 | Single-page app with 27 tests; `node --test` passes 27 of 27. Not run in a browser |

### What D3 shows

- **The small tier can build.** `frontend-dev` on Haiku wrote the app, its tests and a smoke check for $0.06. That partly answers review A's F7 question.
- **The CEO does the work around it itself.** The main session:
  - edited `src/calc.js`, the tests and `index.html` itself (it fixed a round-up defect);
  - wrote the security review and the SBOM itself, so the release check was a self-review;
  - wrote the ADRs, `status.json` and the README;
  - **edited the plugin's own `LESSONS.md`** in the install folder.

  No security, QA, legal or audit agent was convened.
- **Output landed in the right place.** Files went to `outputs/devsecops-agency/tip-splitter/`. In Run 1 they went to `<slug>/`.

## Probe: starting the CEO as an agent (review A, F1)

Run with `--agent devsecops-agency:ceo` and a PreToolUse logging hook passed through `--settings`. Cost $0.40 and $0.40.

- **Tools:** the main session's tool list became exactly the CEO's declared set: Read, Write, Edit, Bash, Grep, Glob and Task. In the D runs it had more than 30 tools, including Artifact, Cron and Workflow.
- **Hooks can now see the CEO.** Main-thread calls carried `agent_type: devsecops-agency:ceo` with no `agent_id`; subagent calls carried their own type and id.
- **Dispatch still works.** `engineering-lead` was dispatched and ran on Sonnet 5.5.
- `TodoWrite`, declared in `ceo.md`, does not appear in the tool list.
- **The fix holds:** with `--agent`, the CEO can be bound by its grant and by hooks. Its grant today still includes Edit and Bash, which is gap 2.

## Docs checked (Claude Code 2.1.329)

- **Frontmatter:** `maxTurns` and `effort` (`low` to `max`) are supported subagent frontmatter keys. Unknown keys are ignored silently.
- **Fields plugins ignore:** plugin agents ignore `hooks`, `mcpServers` and `permissionMode` in frontmatter.
- **Default agent:** a plugin cannot set the default main-thread agent. That comes from `--agent` or a project's `.claude/settings.json` `agent` key.
- **Dispatch lists:** `Agent(a, b)` lists restrict only the main-thread agent. In a subagent the list is ignored, so "own specialists only" needs a hook.
- **Plugin hooks:** they live in `hooks/hooks.json` with a top-level `hooks` key. `"onFailure": "block"` makes a hook fail closed; it needs v2.1.295 or later.

## Fixed overhead

D1's first turn wrote about 64,000 tokens to the cache, the session's fixed overhead. The `--agent` probe wrote about 44,000, because it loads fewer tools. These are the "before" numbers for moving the examples out of the agent descriptions in Phase 1a.

## What this changes for Phase 1a

1. **Make the CEO an agent.** The entry point must start the session with `--agent devsecops-agency:ceo`, through a launcher or a project setting. Without it no grant binds the CEO. This is confirmed.
2. **Remove the CEO's Edit and Bash.** In D3 it edited code, reviewed its own work and wrote into the plugin folder.
3. **Make the minimum pipeline enforced, not advisory.** Even with no cap pressure, the CEO convened at most one agent per task and skipped every checker.
