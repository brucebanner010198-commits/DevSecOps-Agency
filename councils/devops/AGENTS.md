# councils/devops — boundaries

## Output contract

- Lead: `devops-lead` (VP-Ops). Specialists: ci-engineer, deployment-engineer, observability-engineer.
- Artifacts: `<slug>/deploy/` — CI config, container/build, deploy manifest, rollback plan, `observability.md`.
- Deploy is repeatable. Rollback is one command.

## Must

- CI runs: build, lint, tests, dependency audit. Every PR. No skip on green branches.
- Containers pin base image versions. No `latest` tags in production config.
- `/healthz` (liveness) and `/readyz` (readiness) endpoints exist.
- Structured logs (JSON) with request IDs. Metrics endpoint or equivalent.
- Rollback plan is ≤ 3 commands AND has been walked through in `deploy/runbook.md`.
- Secrets via the platform's secret store, not env vars in a file.

## Must not

- Ship a deploy without a rollback plan. Ever.
- Use `:latest` in a prod Dockerfile or manifest.
- Log a secret, token, or PII. Redact at the log formatter.
- Skip the dependency audit step in CI.

## Gate heuristic

- `green`: CI green, container pinned, health endpoints work, rollback walk-through recorded.
- `yellow`: one non-critical log field unredacted, or observability thin but functional.
- `red`: no rollback plan, secret in a committed file, `:latest` in prod config, no CI.
