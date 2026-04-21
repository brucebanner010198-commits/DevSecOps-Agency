# councils/execution — boundaries

## Output contract

- Lead: `engineering-lead` (VP-Eng hat). Specialists: backend-dev, frontend-dev, db-engineer, integrations-engineer.
- Artifact root: `<slug>/src/`. Plus migrations, seeds, and minimal in-repo fixtures.
- Build must match `architecture.md` and the CISO's approved threat model exactly.

## Must

- Parameterise every query. Never string-concatenate SQL.
- Every migration has an idempotent `up` AND a working `down`.
- Integrations have interface shims + a mock version that tests can swap in.
- Secrets via env vars, never in committed files. Include `.env.example`.
- Structured logging from day 1. Request IDs on every HTTP handler.
- Input validation at the trust boundary. Never trust client input.

## Must not

- Invent an API shape that `api-designer` didn't spec. Bounce it back up to Architecture if the spec is wrong.
- Pull a dependency not vetted by GC's license-checker (in a later phase — so: tentatively use MIT/BSD/Apache; flag anything else).
- Ship a mutation without the idempotency key from the spec.
- Write code you can't explain in one sentence. If you can't, the design is wrong.

## Gate heuristic

- `green`: `src/` builds cleanly, migrations run up + down, tests haven't been written yet but code is testable.
- `yellow`: one non-critical integration unmocked, or one migration missing `down`.
- `red`: string-concatenated SQL found, secrets in tree, spec drift from Architecture.
