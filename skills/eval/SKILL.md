---
name: eval
description: This skill should be used whenever the CEO needs to measure whether a project actually did what its OKRs promised — on every project close (close-eval), at quarter roll-up (portfolio-regression), before any plugin v-bump (benchmark-sweep), and any time the user asks "is it actually better" or "how does this compare to last quarter". The eval skill owns the per-project eval-set derivation from PKRs, the scoring harness invocation, and the regression-detection pipeline. Trigger phrases include "close-eval", "run the evals", "eval regression sweep", "is it better", "prove it works", "portfolio eval", "quality drift check".
metadata:
  version: "0.3.0-alpha.5"
---

# eval — "did the agency deliver on what it promised"

Paper-trail integrity is the CAO's job (`skills/audit`). Product quality is the CEVO's job — this skill. Evals are derived from PKRs, not from shipped artifacts; post-hoc eval writing is forbidden.

## When to invoke

- Every project close (close-eval), paired with CAO close-audit.
- Quarter roll-up (portfolio-regression sweep).
- Before any plugin v-bump (`plugin.json.version` bump → `benchmark-sweep`).
- User asks "how did we do / is it better / quality drift check".

## Artifacts

```
<slug>/eval/
  eval-set.md         ← derived from PKRs
  results.md          ← per-item pass/fail + aggregate
  budget-ledger.md    ← token + $ burn
_vision/eval/
  <date>-<slug>-close.md
  <date>-regression.md
  regression-baseline.md   ← frozen per quarter
  <date>-benchmark-sweep.md
```

## Process (close-eval)

1. **Convene.** CEO dispatches `evaluation-lead` with the slug, the project's OKR path, and the `budget` block from `_vision/projects/<slug>.md`.
2. **Parallel specialist fan-out** (CEVO invokes):
   - `eval-designer` → `<slug>/eval/eval-set.md` (≥ 1 item / PKR, pass/fail ground-truth).
   - `benchmark-runner` → `<slug>/eval/results.md` (mechanical scoring).
   - `regression-detector` → delta vs `_vision/eval/regression-baseline.md`.
   - `budget-monitor` → `<slug>/eval/budget-ledger.md`.
3. **Synthesise.** CEVO writes `_vision/eval/<date>-<slug>-close.md` with overall gate + findings + regressions + ADR filings required.
4. **Gate + ADRs.** CEO applies `gates` + files ADRs for any red finding. If regression root-cause points to a specific council, open a taskflow task targeting that council + trigger Rung 3 of the ladder.
5. **Minutes.** Every close-eval with ≥ 1 red writes meeting minutes (`kind: audit` — shared with CAO close-audit since both convene at close). Minutes action items are 1:1 taskflow tasks.
6. **Baseline update check.** If this run's eval set adds new canonical items for the regression baseline, propose them for inclusion at the next quarter boundary (not this one — baselines are immutable within a quarter).

## Process (portfolio-regression sweep)

1. At quarter roll-up, CEO dispatches `evaluation-lead` portfolio-wide.
2. `benchmark-runner` re-runs `regression-baseline.md`'s canonical eval set against every closed project's shipped artifacts this quarter.
3. `regression-detector` aggregates and diffs vs prior quarter.
4. CEVO writes `_vision/eval/<date>-portfolio-regression.md`.
5. Any agency-wide regression > 5 pp files an ADR + triggers a paired `roster` review (is this a prompt-rot signature? a model-tier change? a skill edit without ADR?).

## Process (benchmark-sweep)

1. Before any plugin `v-bump`, CEO dispatches `evaluation-lead` with a v-bump scope.
2. `benchmark-runner` runs the standard harness (SWE-bench-lite equivalent + any custom harness declared in `_vision/eval/harness.md`).
3. Regression vs prior version's sweep → CEVO red if any regression > 5 pp.
4. Gate must land green or yellow before the plugin version is cut.

## Process (compaction-check)

1. On any indication of context-window pressure (session-log > 60 % of budget, `chat.jsonl` > 5 000 entries, memory footprint flag), CEO dispatches `evaluation-lead`.
2. `token-compactor` emits structured rewrites per `skills/memory/references/write-policy.md`. Decisions, errors, reports, ADR-referenced lines, rung transitions, meeting lines — never compactable.
3. Report bytes-before → bytes-after to CEVO; flag compactions < 10 % savings for skip.

## Invariants

- No project ships without close-eval. Mandatory, paired with CAO close-audit.
- Eval items derive from PKRs at close time. Retrofitting items to match outcome is forbidden (see `eval-designer` rules).
- Regression baselines are frozen within a quarter. New baseline proposals queue to the next quarter boundary.
- Every red → ADR in same CEO turn. Every yellow → taskflow task.
- Budget overruns > 110 % of total = red; route to Rung 6 (user consult) via the ladder.
- Session-log compaction is structured rewrite, never deletion. Preservation invariant.
- CEVO never in delivery path. Independence invariant — structural, like Audit.

## Integration with existing skills

- **`okr`** — PKRs are the source of eval items; budgets are set at OKR derivation.
- **`audit`** — CAO runs paper-trail integrity checks in parallel with CEVO quality checks.
- **`gates`** — eval findings aggregate into a project-level eval gate, combined with council gates.
- **`adr`** — every red + every compaction rewrite + every baseline change files an ADR.
- **`ladder`** — budget red + unresolvable regression → Rung 3 → Rung 6 per matrix.
- **`memory`** — compaction goes through structured-rewrite path; durable memory writes remain canonical.
- **`notify`** — regression reds trigger a `notify` event on close.

## Progressive disclosure

- `references/eval-set-rubric.md` — per-tier (functional / ux / promise) item shapes, ground-truth patterns, anti-patterns.
- `references/regression-thresholds.md` — the 5 pp + 10 pp + 20 pp thresholds; what each maps to (flag / yellow / red).
- `references/benchmark-harnesses.md` — SWE-bench-lite setup, MLE-bench-lite setup, custom harness registration rules.

## What this skill is not

- Not a replacement for council gates. Eval measures OKR delivery; gates measure per-phase acceptance. Both exist.
- Not a fix-the-regression mechanism. Fix belongs to the delivery council. Eval flags + files + escalates.
- Not a budget-setter. Budgets come from OKR derivation. CEVO enforces.
- Not a compaction-or-nothing. Compaction happens only when pressure thresholds trip AND savings ≥ 10 %.
