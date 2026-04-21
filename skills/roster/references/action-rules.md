# action-rules.md — per-action checklists

Each row in `proposals.md` is one of five actions. Each has a hard checklist. The CEO rejects proposals that don't satisfy the checklist before filing the ADR.

## Hire

- [ ] Council assignment specified and council exists under `councils/<name>/AGENTS.md`.
- [ ] Tier specified: `haiku` or `sonnet`. `opus` is CEO-only unless an ADR supersedes `skills/model-tiering/SKILL.md`.
- [ ] Gap cited with ≥ 2 `file:line` evidence from the last 90 days showing the domain was uncovered.
- [ ] `skill-creator` brief attached: one paragraph persona seed, expected dispatches/quarter, tools list.
- [ ] Redundancy scan: no existing agent within the same council covers > 60 % of proposed scope.
- [ ] ADR trigger: "Hire — new agent".
- [ ] Execution: CEO dispatches `skill-creator` in the same turn. New `agents/<name>.md` + optional `skills/<slug>/` land with the ADR reference in the front matter description's `<example>` block.

## Fire

- [ ] Agent idle ≥ 90 days **or** red on `performance-reviewer` for 2 consecutive audits.
- [ ] Blocking-council check: if agent is `security-lead`, `gc`, or any specialist under those two, a user-signed waiver line exists in `inbox.json`.
- [ ] Archive plan: `_vision/roster/_archive/<name>.md` will carry a redirect line (template in `archive-policy.md`).
- [ ] ADR trigger: "Fire — retire agent".
- [ ] Execution: `agents/<name>.md` moved to `_vision/roster/_archive/<name>.md` (not deleted). All `_sessions/<name>/*.jsonl` retained. Council `AGENTS.md` roster list updated.

## Tier-change (upgrade only)

- [ ] Current tier cited.
- [ ] Failure signal: ≥ 2 `file:line` evidence the agent's outputs consistently miss gate/OKR expectations at current tier.
- [ ] Proposed tier is one step up (haiku → sonnet, sonnet → opus). Skipping tiers requires separate ADR justifying the jump.
- [ ] Downgrade proposed? → **reject immediately**. Propose prompt upgrade instead.
- [ ] Cost impact estimated: token-cost delta per quarter.
- [ ] ADR trigger: "Tier-change — agent upgrade".
- [ ] Execution: `model:` line in `agents/<name>.md` updated. No other changes — prompt stays identical to isolate the variable.

## Repurpose

- [ ] Old scope + new scope each ≤ 1 sentence, cited against current `agents/<name>.md`.
- [ ] Tier preserved. Repurpose is a scope change, not a tier change; stack both if needed.
- [ ] Old name goes to `_archive/<old>.md` with redirect line to new name.
- [ ] Council reassignment? → if yes, update both councils' `AGENTS.md` roster tables.
- [ ] ADR trigger: "Repurpose — scope shift".
- [ ] Execution: `skill-creator` authors new `agents/<new>.md`; old file archived; council files updated.

## Prompt upgrade

- [ ] Target file: `agents/<name>.md` OR `skills/<slug>/SKILL.md`.
- [ ] Specific edits listed (not "rewrite it"). Ideally ≤ 10 diff hunks for reviewability.
- [ ] Expected effect: one testable metric (e.g., "CSRF catch-rate up from current 60 % to ≥ 85 %").
- [ ] Regression plan: if metric not reached in 30 days, revert via new ADR.
- [ ] ADR trigger: "Prompt upgrade — rule change". Only required if the upgrade changes contract (triggers, output shape, gate rules). Formatting/clarification edits skip the ADR but still go through CEO review.
- [ ] Execution: `skill-creator` makes the diff. Version bump in `metadata.version` if contract-changing.

## Universal rules

- No action without a written proposal row. Drive-by tier changes corrupt the roster history.
- No action without a paired ADR in the same CEO turn. Deferred ADRs rot.
- No action that leaves a council without coverage on an active workspace OKR's KR. COO validates coverage before accepting.
- Action bundles (e.g., fire + hire replacement) file one ADR per action, cross-linked in the `## Related` section.
