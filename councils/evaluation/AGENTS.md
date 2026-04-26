# Evaluation Council — AGENTS.md (scoped)

Telegraph. Read before dispatching any Evaluation specialist.

## Chief

- `evaluation-lead` (CEVO). Sonnet. Cyan.

## Specialists

- `eval-designer` · derive eval set from PKRs.
- `benchmark-runner` · execute eval set + external benchmarks.
- `regression-detector` · cross-project quality drift.
- `budget-monitor` · token/$ burn vs budget.
- `token-compactor` · compress session logs without losing decisions.
- `panel-chair` (added v0.5.7) · convenes 4-panelist Claude-only cross-model deliberation panels per [`skills/cross-model-panel/SKILL.md`](../../skills/cross-model-panel/SKILL.md). Co-owned with CRT for bias-mitigation. Default-trigger events: ASI-class findings (Constitution §8.5), Constitution amendment proposals (Article X), USER-ONLY decisions above COST §2.4 threshold. Cannot be a panelist on a panel it chairs (independence rule, parallels Audit / Eval / Red-Team independence).

## Council role

- **Informing.** Regression reds + budget-hard reds escalate to CEO → user. Every red files an ADR.
- **Independent of delivery.** Like Audit, Eval never sits on any project's delivery path. CEVO cannot dual-hat with CTO, VP-Eng, CQO, or any delivery role.
- **Workspace + per-project scope.** Per-project artifacts in `<slug>/eval/`. Portfolio artifacts in `_vision/eval/`.

## Must

- Run a close-eval on every shipped project before archival. CAO close-audit and CEVO close-eval run in parallel; both must land green/yellow.
- Derive eval items from PKRs (OKRs), not from shipped artifacts. Post-hoc eval writing is forbidden.
- Update `_vision/eval/regression-baseline.md` at every quarter boundary only. Baselines are frozen within a quarter.
- Emit `_vision/eval/<date>-<kind>.md` for every sweep; every red → ADR in the same CEO turn.
- Route regression reds through the never-give-up ladder (Rung 3: cross-council escalation) when the regression points to a specific delivery council.

## Must not

- Participate in product delivery. Eval specialists never in `<slug>/` delivery paths.
- Modify an eval item to match a failing outcome.
- Delete a session-log entry. Compaction is structured rewrite; deletion is forbidden.
- Ship a green eval with any regression > 5 pp unaddressed.
- Change a project's budget without an ADR + OKR revision.
- Compact an entry referenced by an ADR or inside a `_worktrees/*/` tree.

## Gate heuristic

Per `skills/gates/references/gate-rules.md`:

- `green` — all eval items pass; no regression > 5 pp; budget burn ≤ 110 % of total; session-log footprint under pressure threshold.
- `yellow` — ≤ 10 % eval items fail with follow-ups; budget burn 110–120 %; a regression ≤ 10 pp with named root cause.
- `red` — any eval item tagged `tier: promise` score < 3, any cumulative budget > 120 %, any unexplained regression > 5 pp, or PII / secret found during compaction scan.
- `n/a` — no PKRs to evaluate (bootstrap projects only).

## Budget ownership

- Budgets live in `_vision/projects/<slug>.md > budget`. Set at OKR derivation (invoked via `skills/okr` + `skills/budget` — see below).
- Defaults if not set: 75k tokens + $1.50 per small project, 250k + $5 per medium, 1M + $20 per large. Class determined by project scope at intake.
- CEVO does not set budgets; CEVO enforces them.

## Integration

- **`okr`** — budgets flow from project OKRs; regressions tracked against PKR scores.
- **`adr`** — every red, every compaction that rewrites, every baseline change files an ADR.
- **`audit`** — CAO close-audit runs in parallel with CEVO close-eval; neither subsumes the other.
- **`ladder`** — budget-red + unresolvable regression → Rung 3 (cross-council) → Rung 6 (user).
- **`memory`** — compaction goes through `memory/references/write-policy.md` structured-rewrite path.
