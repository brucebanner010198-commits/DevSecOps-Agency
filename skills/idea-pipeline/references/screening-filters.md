# idea-pipeline screening filters (stage 2)

Convergent filter from ~15-40 candidates down to ≤ 10. Applied in order — first failure kills the candidate. Every kill gets a reason line.

## Filter order (first failure kills)

### 1. Legal feasibility (hard kill)

- Requires compliance with jurisdictions the workspace already operates in (check `_vision/VISION.md > ## Constraints`).
- Kill if: explicit regulatory prohibition · requires a license the org does not have · the business model is illegal in any target market.
- No override. These ideas go to a "deferred — legal" list, not into screening.

### 2. Mission fit (soft kill with override)

- Must trace to ≥ 1 bullet in `_vision/VISION.md > ## Mission` OR carry a `[mission-stretch]` flag with CEO approval.
- Kill if: no traceable mission link and no mission-stretch flag.
- Override: CEO can admit a mission-stretch candidate but must file an ADR explaining the admission rationale.

### 3. Incumbent moat (wedge required)

- If a dominant incumbent exists (≥ 30% market share by `_vision/strategy/competitive-map.md`), the candidate needs an explicit wedge: one segment the incumbent ignores, one capability the incumbent can't copy in < 12 months, or a pricing-model flip.
- Kill if: no wedge and the incumbent is healthy.
- Soft retain: explicit `[contrarian-bet]` flag acknowledging the risk.

### 4. Stack adjacency (feasibility)

- Candidate reuses ≥ 1 proven-stack capability from `_memory/MEMORY.md > ## Proven stacks` OR the workspace has budget to onboard a new capability (`skill-creator` invocation acceptable).
- Kill if: candidate requires ≥ 3 new capabilities and no skill-creator budget.
- Soft retain: `[greenfield]` flag with estimated onboarding cost.

### 5. Opportunity-cost shelf-life (timing)

- Candidate is actionable within the horizon. If the trend-radar shows the signal as fading, the window is closing.
- Kill if: signal fading and we're ≥ 6 months from a launch.
- Soft retain: `[window-closing]` flag with target launch ≤ 3 months.

## Kill list format

Every killed candidate goes into `_vision/strategy/_pipeline/screened-<date>.md > ## Deferred` with:

```markdown
- **<slug>** — killed at filter <n> · <one-line reason> · reconsider-if: <condition>
```

No candidate is killed silently. Reconsider-if must be a testable condition (e.g., "reconsider if incumbent raises pricing" not "reconsider if situation changes").

## Stage-2 exit gate

- ≥ 5 and ≤ 10 survivors.
- Every drop has a reason line.
- No `[mission-stretch]`, `[contrarian-bet]`, `[greenfield]`, or `[window-closing]` flag without a paired ADR draft.
