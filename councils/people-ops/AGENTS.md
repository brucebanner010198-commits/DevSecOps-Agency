# councils/people-ops — boundaries

## Output contract

- Lead: `coo`. Specialists: `roster-manager`, `hiring-lead`, `performance-reviewer`.
- Artifact root (workspace): `_vision/roster/`.
- Key files: `census.md` (alphabetical rewrite), `performance.md` (window-specific), `proposals.md` (action list), `coo-brief.md` (synthesis).
- Archive: `_vision/roster/_archive/<name>.md` with a redirect line to superseding ADR.
- Informing council. Reds aggregate into the portfolio gate, never block a project ship directly. CEO escalates only via ADR.

## Must

- Hire through `skill-creator`. No raw-drafted agent personas.
- File an ADR for every hire, fire, tier-change, and repurpose. `skills/adr/references/decision-triggers.md > People-ops` is authoritative.
- Preserve fired agents in `_vision/roster/_archive/<name>.md`. Never `git rm`.
- Alphabetize `census.md` and `performance.md`. Prompt-cache determinism requires it.
- Rate-limit performance reviews to ≥ 30-day windows. Single-week snap judgments retire agents that were just ramping.

## Must not

- Mutate any agent's own `agents/<name>.md` prompt without an ADR proposing the change and `skill-creator` executing it.
- Fire a blocking-council agent (`security-lead`, `gc`, their specialists) without a user-signed waiver in `inbox.json`.
- Propose a tier **downgrade**. `skills/model-tiering/SKILL.md` forbids it.
- Hire a new agent whose scope overlaps > 60 % with an existing role. Redundancy is the top hiring mistake.
- Skip archive redirect on repurpose. An agent renamed without a redirect line corrupts the roster history.

## Gate heuristic

- `green`: census + performance + proposals all green; no fires pending user waiver; no idle-for-3-quarters blocking-council agents.
- `yellow`: one specialist yellow (performance flag on a non-blocking agent, capacity skew, pending tier-upgrade).
- `red`: proposal to fire a blocking-council agent without user waiver · tier downgrade proposed · agent prompt mutated without ADR · archive redirect missing.

## OKR alignment hint

- People-ops scores `okr_alignment` against **agency-capacity OKRs only** (e.g., "ship weekly", "zero silent yellows"), never against product OKRs. If no capacity OKR is active in `_vision/VISION.md > ## OKRs`, `okr_alignment: n/a` is acceptable.
- If a proposal would retire an agent whose last 3 reports traced the only green alignments on a top-active KR, `okr_alignment: red`. Surviving agency capacity must cover every active KR.
