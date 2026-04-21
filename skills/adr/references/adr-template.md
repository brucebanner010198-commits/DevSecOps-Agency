# adr-template — paste-and-fill skeleton + worked examples

Use the skeleton verbatim. Fill angle-bracket tokens.

## Skeleton

```markdown
# ADR-NNNN: <title — imperative, ≤ 10 words>

- **Status:** accepted
- **Date:** YYYY-MM-DD
- **Author:** <actor>
- **Related:** <ADR refs, vision section, or project slug, or "none">
- **Project:** <slug> | workspace

## Context

<Paragraph 1: the problem.>

<Paragraph 2: forces at play.>

## Decision

<One paragraph. Active voice. "We will X.">

## Consequences

### Positive
- <one line>
- <one line>

### Negative
- <one line>
- <one line>

### Reversibility
- <one line: "Reversible in N days with M effort" or "One-way door — rollback cost = X">

## Alternatives considered

- **<Alt A>** — <why not, one line>
- **<Alt B>** — <why not, one line>

## Follow-ups

- <concrete task — owner — due date>
- <concrete task — owner — due date>
```

## Worked example 1: technology choice

```markdown
# ADR-0007: Use Supabase for the student-expense-tracker backend

- **Status:** accepted
- **Date:** 2026-04-21
- **Author:** cto (engineering-lead)
- **Related:** _vision/VISION.md § Active OKRs, ADR-0004
- **Project:** student-expense-tracker

## Context

The tracker needs auth, a Postgres-shaped datastore, and row-level security for multi-tenant dorm data. The OKR target is launch in 21 days; build budget is 5 engineering days. Building auth + RLS from scratch in Postgres consumes the budget.

We evaluated Supabase, Firebase, and a hand-rolled Node + Prisma + Postgres stack. The CRO's research (`research/backend-options.md:42`) showed Supabase has the highest Jaccard match against our prior learnings in `_memory/patterns/dorm-logistics.md`.

## Decision

We will use Supabase for auth, database, and RLS. The backend is a thin Node API for webhooks only.

## Consequences

### Positive
- Cuts build time from ~5 days to ~2 days — puts the launch KR back in green.
- RLS + auth are battle-tested; reduces CISO second-pass risk.
- Row-level policies map cleanly to "dorm as tenant boundary."

### Negative
- Vendor lock-in — Supabase schema migrations harder to extract later.
- Realtime pricing becomes material at > 500 concurrent users.
- Introduces a third-party trust boundary for CISO threat model.

### Reversibility
- Reversible in ~3 days of rework (Supabase → plain Postgres) up to first 1000 users. One-way door after that.

## Alternatives considered

- **Firebase** — NoSQL model fights our reporting queries; RLS is weaker.
- **Hand-rolled Node + Prisma + Postgres** — blows the 5-day build budget by ≥ 100%; regresses launch-time KR.

## Follow-ups

- Add Supabase to CISO threat model — ciso — 2026-04-23
- Document RLS policies in `api/security.md` — api-designer — 2026-04-24
- Add a "cost at 500 users" line to `ops/cost-budget.md` — devops-lead — 2026-04-25
```

## Worked example 2: waiver

```markdown
# ADR-0012: Waive a11y gate for internal MVP of finance-dashboard

- **Status:** accepted
- **Date:** 2026-04-22
- **Author:** ceo
- **Related:** skills/gates/references/waiver-rules.md, project: finance-dashboard

## Context

The finance-dashboard is an internal tool with a single user (CFO). QA's a11y audit flagged 3 medium findings (contrast, focus-ring, aria-label). Fixing them extends the launch by ~2 days, which pushes past the KR target. User (Sir) confirmed in 2026-04-22 meeting that internal-only single-user tools can carry a11y debt through v1.

We do not waive a11y for any user-facing product. This waiver is scoped tightly.

## Decision

We will ship finance-dashboard v1 with the 3 medium a11y findings open. Findings are logged as follow-ups for v2.

## Consequences

### Positive
- Hits the launch KR within budget.
- v2 will pick up a11y fixes before any external user sees it.

### Negative
- Debt accumulates; v2 a11y pass cost rises if more UI ships before it.
- Sets a precedent — risk future waivers for similar "internal" tools.

### Reversibility
- Reversible at any time by running the 3 fixes (~2 days).

## Alternatives considered

- **Fix now before launch** — blows the launch KR; no external benefit since no external users.
- **Cancel the a11y gate permanently for internal tools** — rejected; we want the gate to keep running as a warning system.

## Follow-ups

- Add the 3 findings to `finance-dashboard/v2-backlog.md` — cqo — 2026-04-22
- Add a "has-a11y-waiver" flag to `status.json` so command-center shows it — command-center — 2026-04-23
```

## Never

- Skip the Alternatives section. At minimum one alternative.
- Write Decision in passive voice ("It was decided...").
- Cap-break at 120 lines. Split into two ADRs if needed.
- File an ADR that restates an existing ADR. Reference instead.
