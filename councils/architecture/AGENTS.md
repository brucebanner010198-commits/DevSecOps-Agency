# councils/architecture — boundaries

## Output contract

- Lead: `engineering-lead` (CTO hat). Specialists: system-architect, api-designer, data-architect, infra-architect.
- Artifacts: `<slug>/architecture.md`, `<slug>/architecture/data-model.md`, `<slug>/architecture/infra.md`.
- Every data-model column has a **PII classification** (public / internal / confidential / restricted).

## Must

- Choose a stack that matches the spec and the user's stated tech preference (from `brief.md`).
- Draw trust boundaries explicitly. Every cross-boundary call is a threat-model input.
- Data model has: primary keys, indexes, constraints, PII columns flagged, retention rule per PII column.
- API shapes include: auth posture, rate-limit posture, idempotency keys where mutations are external.
- Every non-trivial choice has a one-sentence rationale citing spec or prior pattern.

## Must not

- Pick a stack because it's trendy. Spec justifies, patterns inform.
- Leave a mutation endpoint without an idempotency story.
- Ship an architecture without an infra sketch (even if "host on Vercel" is the whole sketch).
- Skip the data-model PII classification. CISO will bounce it.

## Gate heuristic

- `green`: all three artifacts present, PII classified, trust boundaries named, rationale per choice.
- `yellow`: infra sketch missing or one choice unexplained.
- `red`: data model without PII classification, or APIs without auth/rate-limit posture.

## Added v0.6.1 — Architecture skills

CTO owns two new skills in v0.6.1:

- [`skills/zoom-out`](../../skills/zoom-out/SKILL.md) — short, sharp request pattern for orienting an agent in unfamiliar code. One-prompt skill (no procedure), routes the response through `<slug>/CONTEXT.md` vocabulary and surfaces ADR constraints in the area being explored. Any specialist drops into this mid-task; `disable-model-invocation: true` in the frontmatter prevents auto-trigger noise.

- [`skills/improve-codebase-architecture`](../../skills/improve-codebase-architecture/SKILL.md) — periodic deepening review (recommended every two weeks per active project) that surfaces shallow modules and proposes refactors that turn them into deep ones (Ousterhout). Step 1 explores using a Worker subagent; Step 2 presents a numbered list of deepening candidates; Step 3 drops into a `grill-with-docs`-style conversation on the chosen candidate; Step 4 produces a refactor brief and either hands off to `tdd` or queues at `<slug>/architecture-backlog.md`. Heavily informed by `<slug>/CONTEXT.md` (domain language) and `_decisions/<slug>/adrs/` (decisions the skill MUST NOT re-litigate). Skipping multiple consecutive runs without a written reason routes the project to compliance-drift in the monthly heartbeat (`RHYTHM.md`).

Architectural vocabulary used in both skills: **Module / Interface / Implementation / Depth / Seam / Adapter / Leverage / Locality** — defined in `skills/improve-codebase-architecture/SKILL.md`. CTO MUST use these terms exactly; drift into "component / service / API / boundary" defeats the precision the skills depend on.
