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
