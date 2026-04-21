# councils/quality — boundaries

## Output contract

- Lead: `qa-lead` (CQO). Specialists: test-designer, test-runner, performance-tester, a11y-auditor.
- Artifacts: `<slug>/tests/`, `<slug>/qa-report.md`, `<slug>/qa/perf-report.md`, `<slug>/qa/a11y-report.md`.
- Tests target **both** the spec's acceptance criteria AND the threat model's mitigations.

## Must

- Unit + integration + at least one happy-path e2e. Name every test in plain English.
- Perf report has `p50`, `p95`, `p99` for every user-facing endpoint. Flag N+1 queries.
- A11y: axe-core automated + manual WCAG 2.1 AA checklist. Every form field has a label.
- Flaky tests are bugs. If a test passes 4/5, it's red — fix the test or the code.
- Each qa report cites `src/` paths for coverage evidence.

## Must not

- Ship green with < 70% branch coverage on business logic unless the CEO explicitly waives.
- Write tests that only pass because they assert nothing (`expect(true).toBe(true)` style).
- Skip perf because "it's just a demo". Establish baseline p95.
- Accept an a11y failure of "contrast" or "missing label" without a follow-up ticket.

## Gate heuristic

- `green`: tests pass, coverage acceptable, perf p95 within target, a11y baseline met.
- `yellow`: one known flaky test with a recorded fix plan, or one a11y medium issue with ticket.
- `red`: failing test, missing coverage on a mitigated threat, perf regression > 2x baseline, a11y critical.
