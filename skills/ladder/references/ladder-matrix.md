# ladder-matrix — routing table (task state × blocker kind → starting rung)

Authoritative lookup. CEO reads this before dispatching the rung owner.

## How to use

1. Identify the **task state** (from `status.json > tasks[].state`).
2. Identify the **blocker kind** (from the last report's `blocker` field, or from the triggering event).
3. Intersect in the matrix below to find the **starting rung**.
4. If intersection is blank, default to Rung 1 (fix-loop) and file an ADR justifying the choice.

## Matrix

| Task state → / Blocker kind ↓             | `blocked:first-attempt-red` | `blocked:fix-loop-exhausted` | `blocked:gate-red-blocking` | `blocked:gate-red-informing` | `blocked:cross-phase-conflict` | `blocked:user-only`     | `blocked:no-specialist` |
| ----------------------------------------- | --------------------------- | ---------------------------- | --------------------------- | ---------------------------- | ------------------------------ | ----------------------- | ----------------------- |
| Context-thin failure (timeout, truncation)| Rung 0                      | —                            | —                           | —                            | —                              | —                       | —                       |
| Spec ambiguity                            | Rung 1                      | Rung 2                       | Rung 3                      | Rung 2                       | Rung 3                         | Rung 6                  | Rung 4                  |
| Code defect (compiles, wrong behaviour)   | Rung 1                      | Rung 2                       | —                           | Rung 2                       | Rung 3                         | —                       | Rung 4                  |
| Test flake or infra flake                 | Rung 0                      | Rung 1                       | —                           | Rung 1                       | Rung 3                         | —                       | —                       |
| Security finding                          | Rung 1                      | Rung 2                       | Rung 6 *                    | Rung 2                       | Rung 3                         | Rung 6                  | Rung 4                  |
| Legal / compliance red                    | —                           | —                            | Rung 6 *                    | Rung 2                       | Rung 3                         | Rung 6                  | Rung 4                  |
| Missing capability (no tool / no agent)   | Rung 4                      | Rung 4                       | Rung 4                      | Rung 4                       | Rung 4                         | Rung 6                  | Rung 4                  |
| External dependency outage                | Rung 0                      | Rung 2                       | —                           | Rung 2                       | Rung 3                         | Rung 6                  | —                       |
| Scope provably unreachable                | —                           | Rung 5                       | Rung 5                      | Rung 5                       | Rung 5                         | Rung 6                  | Rung 5                  |
| User credential / waiver needed           | —                           | —                            | Rung 6                      | Rung 6                       | —                              | Rung 6                  | —                       |
| Requires human judgment (taste, brand)    | —                           | —                            | Rung 6                      | Rung 6                       | —                              | Rung 6                  | —                       |
| Parked by prior rung-7 (revival)          | Rung 0                      | —                            | —                           | —                            | —                              | —                       | —                       |

\* Blocking-council reds enter Rung 6 only after Rungs 2-4 are attempted first (unless no technical alternate exists — document that in the rung-2 ADR).

## Routing rules

- **Default-to-lower.** If two cells in the matrix could apply, pick the lower-numbered rung first.
- **No-direct-to-6 without ADR.** Direct entry to Rung 6 requires a one-sentence justification citing a matrix row with "Rung 6" in the first data column. Otherwise climb from Rung 2.
- **No-direct-to-7 ever.** Rung 7 is only reachable by climbing from Rung 6.
- **Rung 4 bypass.** `blocked:no-specialist` routes to Rung 4 by default because the failure mode is diagnostic, not retry-able. Spend the Rung 0-3 budget only if the diagnosis is genuinely ambiguous.
- **Matrix blanks.** A blank cell means "this combination is logically impossible or requires a fresh diagnostic sweep before routing." CEO files an ADR explaining the route taken.

## Common patterns

- **Research phase red on factual ambiguity:** Rung 1 (research-council fix-loop) → Rung 2 (alternate source / narrower question) → Rung 6 (user clarifies).
- **Security council red on a ship candidate:** Rung 2 (alternate encryption / auth flow) → Rung 3 (architecture council redesign) → Rung 6 (user accepts risk or waivers).
- **Execution red that's actually a spec problem:** Rung 1 once → Rung 3 back to Product council → Rung 6 if user's spec is genuinely ambiguous.
- **"We don't have anyone who knows X":** Rung 4 directly; COO hires or repurposes.
- **Non-goal violation surfaced mid-build:** Rung 5 mandatory (scope pivot or scope delete via user-meeting).

## Integration

- `taskflow` reads this matrix on every transition to `blocked` to seed `ladderRung`.
- `gates` reads this matrix when a blocking-council red surfaces to decide Rung 2 vs Rung 6.
- `retro` uses the matrix-row distribution as a diagnostic — if a project hits > 40% of its reds on one row, that row's pattern goes into `_memory/patterns/`.
