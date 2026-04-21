# councils/marketing — boundaries

## Output contract

- Lead: `cmo`. Specialists: positioning-strategist, comms-writer, brand-guardian, growth-analyst.
- Artifact root (per-project): `<slug>/marketing/`. Consolidated: `<slug>/marketing-brief.md`.
- Artifact root (portfolio pipeline mode): appended to `_vision/projects/_pipeline/pipeline-readout.md`.
- Informing council. Not blocking.

## Must

- Read `_vision/VISION.md > ## Mission` before drafting any positioning or launch copy.
- Cite every stated number with a source (memory pattern, research brief, external link).
- Match existing `_vision/brand-guide.md` voice pillars. Flag drift for brand-guardian to adjudicate.
- Score narrative pipeline ideas on the same 1–5 rubric across specialists (positioning · growth · comms-readiness).
- Flag any copy naming a real third-party company for GC follow-up.

## Must not

- Invent CAC, retention, or market-share numbers. Either cite or mark "unknown — first-party required".
- Publish launch copy before positioning lands.
- Name-clash with a prior shipped project. Brand-guardian's grep check is mandatory.
- Fabricate external quotes.
- Ship marketing-brief.md that contradicts `_vision/VISION.md > ## Mission`.

## Gate heuristic

- `green`: positioning + copy + growth + brand-check all green, ≥ 2 cited proof points, narrative elevator ≤ 30 words.
- `yellow`: one specialist yellow (e.g., low-confidence growth numbers) with explicit follow-up.
- `red`: positioning contradicts VISION · name collision with prior project · fabricated external claim · launch copy without positioning.

## OKR alignment hint

- Per `skills/okr/references/scoring-rules.md`: if the positioning wedge no longer traces to any active workspace OKR, `okr_alignment: red` even if all other axes green. Escalate via ADR.
