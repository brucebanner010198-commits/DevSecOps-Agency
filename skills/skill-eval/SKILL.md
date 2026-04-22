---
name: skill-eval
description: Evaluate the quality of any agency skill with a structured eval harness. Runs a skill against a benchmark set of prompts, scores responses, and reports aggregate metrics with variance analysis. Supports iterating on a skill's description to improve triggering accuracy. Complements (does NOT replace) the agency's skill-creator — skill-creator authors skills, skill-eval judges them. Use when a new skill lands in the plugin, when a skill's behavior seems to have drifted, or when CEVO needs release-gate evidence that a skill actually works.
version: "0.3.5"
license: "Apache-2.0 (upstream: Anthropic skills repo) — see LICENSE.txt"
---

# Skill Evaluation Harness

The agency's `skill-creator` writes skills. `skill-eval` judges them — does the skill trigger on the right prompts, produce the right outputs, stay consistent across runs.

Think of it as **CI for skills**: every time a skill is added or modified, run the eval; commit the aggregated report as gate evidence.

## When to use

- New skill lands in the plugin — eval it before merge.
- A skill's behavior drifts (regressions reported by agents or users).
- CEVO (`evaluation-lead`) needs evidence that a skill works before a release gate passes.
- Tuning a skill's `description:` frontmatter to improve trigger precision.
- Benchmarking two candidate skill designs head-to-head.

## Four evaluation modes

### 1. Single-run eval — `scripts/run_eval.py`

Run a skill against a single prompt set. Useful for quick sanity checks after a change.

```bash
python scripts/run_eval.py --skill path/to/SKILL.md --prompts path/to/prompts.jsonl
```

Outputs per-prompt pass/fail, summary statistics.

### 2. Benchmark aggregation — `scripts/aggregate_benchmark.py`

Run many trials and aggregate with variance analysis (mean, stdev, CI). Catches flaky skills that pass on average but swing wildly per-run.

```bash
python scripts/aggregate_benchmark.py --skill-dir path/to/skill --n 10 --report out.html
```

Required for every skill before promoting to the plugin. Target: σ / μ ≤ 0.15 on pass-rate (i.e. the skill is reproducible).

### 3. Optimization loop — `scripts/run_loop.py`

Iteratively refine a skill's `description:` to maximize trigger accuracy. Given a labeled dataset (prompts + "should-trigger" flag), the loop:
1. Runs the current description against the dataset.
2. Scores trigger recall / precision.
3. Proposes a rewrite of the description.
4. Repeats until convergence or budget exhaust.

```bash
python scripts/run_loop.py --skill path/to/SKILL.md --dataset trigger-dataset.jsonl --budget 50
```

Output: best-performing description + full trial history.

### 4. Description-only improver — `scripts/improve_description.py`

Lighter-weight than the full loop. Rewrites only the `description:` field, no benchmarking. Use when the skill body is good but the description isn't triggering correctly.

## Quick validation — `scripts/quick_validate.py`

Pre-flight check before running an eval. Confirms the SKILL.md parses, frontmatter is complete, referenced script/reference paths exist.

```bash
python scripts/quick_validate.py path/to/skill
```

**Run this first** on any skill you're about to evaluate — saves time vs. a failed eval run.

## HTML report viewer

`eval-viewer/` contains a static HTML viewer for inspecting eval runs. Generate a report with `scripts/generate_report.py`, then open `eval-viewer/viewer.html` to browse.

```bash
python scripts/generate_report.py --run-dir results/2026-04-21 --out review.html
python eval-viewer/generate_review.py --input review.html --output-html viewer-data.html
```

## Agency integration

- Ownership: **`skill-evaluator`** specialist (Evaluation council, reports to `evaluation-lead`).
- Handoff from: `skill-creator` (agent) — every new skill goes through `skill-eval` before merge.
- Handoff to: `gate-auditor` — eval result becomes a gate artifact in `skills/gates`.
- Release cadence: every skill is re-evaluated at each minor-version bump of the plugin (e.g. v0.3.x → v0.4.0). `skill-evaluator` owns the sweep.

## Relationship to `skills/skill-creator`

- `skill-creator` = authoring (writes a new SKILL.md).
- `skill-eval` (this skill) = judging (scores an existing SKILL.md).

The agency kept its own `skill-creator` because the upstream version's authoring workflow differs from the agency's conventions. The **eval harness is imported** because it's generic and high-quality — works on any SKILL.md regardless of authoring style.

## Schema reference

`references/schemas.md` — JSON schemas for prompt sets, eval results, and benchmark reports.

## Reference files

- `scripts/run_eval.py`, `scripts/run_loop.py`, `scripts/aggregate_benchmark.py`
- `scripts/improve_description.py`, `scripts/quick_validate.py`
- `scripts/generate_report.py`, `scripts/package_skill.py`, `scripts/utils.py`
- `references/schemas.md`
- `eval-viewer/viewer.html`, `eval-viewer/generate_review.py`

## Lineage

Upstream: [anthropics/skills — skill-creator eval harness](https://github.com/anthropics/skills/tree/main/skills/skill-creator), Apache 2.0. **Only the evaluation harness** (scripts/, eval-viewer/, references/schemas.md) is imported — the agency retained its own authoring-side `skill-creator`. Imported files are unmodified per Apache 2.0 §4(a). `LICENSE.txt` retained verbatim.
