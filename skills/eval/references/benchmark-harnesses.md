# benchmark-harnesses — external benchmark registration

Authoritative list for `benchmark-runner`. Harnesses must be declared here before use.

## Canonical harnesses

### SWE-bench-lite (agentic coding)

- Purpose: measure end-to-end agentic coding on a curated GitHub-issues subset.
- Registration: `_vision/eval/harness.md > ## SWE-bench-lite` with `version`, `seed`, `subset`.
- Invocation: benchmark-runner invokes via the harness binary (declared in harness.md). Never re-implements scoring.
- Cost awareness: per-issue run ≈ 30–90 s, $0.05–$0.30 depending on model tier. Budget-monitor pre-flights the run.
- Regression signal: pass-rate delta quarter-over-quarter.

### MLE-bench-lite (ML engineering tasks)

- Purpose: measure ML engineering task completion.
- Registration: `_vision/eval/harness.md > ## MLE-bench-lite` with `version`, `tasks`, `time-budget`.
- Invocation: canonical harness; scoring is the harness's native rubric.
- Cost awareness: per-task 5–30 min of compute. Run only at quarter-roll-up unless the project is ML-focused.

### Custom per-project harness

- Purpose: measure project-specific success not covered by external benchmarks.
- Registration: `<slug>/eval/harness.md` (per-project, not workspace).
- Invocation: declared command + expected-output checker. Checker must be deterministic.
- Promotion: a custom harness that proves useful across ≥ 3 projects is a candidate for workspace-level baseline at the next quarter boundary (via ADR).

## Running rules

- Never modify the harness binary to pass items. Harness is upstream; our fix is in the agent / skill / brief.
- Record exact harness version + seed. Reproducibility is the point.
- If a harness update changes scoring semantics, freeze the old version until the next quarter boundary, then adopt the new version via ADR (same quarter-freeze rule as baseline items).
- If a harness is flaky (non-deterministic on retries), run 3× and report `min / median / max`; flag to CEVO for harness-replacement consideration.

## Cost discipline

- Every harness run is logged against the project's budget via budget-monitor.
- Quarterly portfolio-sweep runs are budgeted separately (`_vision/VISION.md > workspace.budget.quarterly_sweep`).
- Cost overruns on harness runs do NOT invalidate the run's score — the score is recorded; the overrun files an ADR.

## Security

- Harness binaries are pinned by SHA. No running an unpinned harness.
- Harness inputs are sanitised (no secrets, no PII) before submission. `memory-auditor`'s regex scan applies to harness input payloads.
- Any harness that requires internet access is flagged to the SRE council (Wave 7) for egress review.

## Deprecation

- A harness is deprecated via ADR + a `_vision/eval/harness.md` entry with `status: deprecated`. Its results are retained forever in `_vision/eval/`. New runs against a deprecated harness require explicit CEVO override.
