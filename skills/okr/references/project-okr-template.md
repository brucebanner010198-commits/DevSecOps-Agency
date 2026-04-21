# project-okr-template — exact markdown for `_vision/projects/<slug>.md`

```markdown
# <slug> · project OKRs

_Derived from `_vision/VISION.md` on YYYY-MM-DD by ceo. ADR: ADR-NNNN._

## Project OKRs
- [PO1] <project outcome — specific to this project, but traceable to workspace>
  _traces_ ← [KR1.1], [KR1.3]
  - [PKR1.1] <measurable project KR — owner: <chief-slug>> — due YYYY-MM-DD
  - [PKR1.2] <measurable project KR — owner: <chief-slug>> — due YYYY-MM-DD
- [PO2] <project outcome>
  _traces_ ← [KR2.1]
  - [PKR2.1] <measurable project KR — owner: <chief-slug>> — due YYYY-MM-DD

## Non-goals (for this project)
- <optional project-specific non-goals, inherited from workspace unless overridden here>

## Score log
<!-- appended by `okr.score` on every Chief report. Append-only. -->

## Closed
<!-- written by `okr.rollup` or by CEO at close. Final project-KR scores + rationale. -->
```

## Field rules

- `_traces_` line is mandatory. If a PKR does not trace to ≥ 1 workspace KR, reject at write time with `"untraceable KR — either add workspace KR first or drop this PKR"`.
- `owner` is a Chief slug from `agents/*.md` or `ceo`. If the project needs a specialist owner, still route through the Chief who owns that specialist.
- `due` is a date not beyond the current quarter's end. If the project legitimately spans quarters, split the PKR.
- Caps: ≤ 3 POs, ≤ 3 PKRs per PO.

## Score-log entry format

```
YYYY-MM-DD · phase <n> · [PKR<a.b>] <color> — <one-line reason, cite artifact path>
```

Examples:
```
2026-04-22 · phase 1 · [PKR1.1] green — CRO research confirms wedge; cites research/market.md:34
2026-04-23 · phase 3 · [PKR1.1] yellow — build paused on credentials; no regression
2026-04-24 · phase 4 · [PKR1.2] red — QA found coverage gap vs target; cites qa-report.md:78
```

## Closed block format

```markdown
## Closed
Date: YYYY-MM-DD
Outcome: shipped | blocked | cancelled
Final scores:
- [PKR1.1] green — final state at close
- [PKR1.2] yellow — <one-line reason>
- [PKR2.1] n/a — deferred to next project
Retrospective handle: `_memory/patterns/<slug>.md`
```
