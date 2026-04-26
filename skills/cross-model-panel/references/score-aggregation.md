# Score-aggregation methods (v0.6.0)

The v0.5.7 baseline aggregates per-panelist rankings via **average rank**: each panelist's #1 = 1, #2 = 2, etc.; aggregate = mean position across panelists across both Stage-2 orderings; lowest mean wins. Average rank is simple, robust to ties, and was llm-council's native method.

But aggregation theory (Arrow's impossibility theorem, social choice literature) tells us **different aggregation methods can produce different winners on the same ranked-ballot data**. v0.6.0 adds two alternative methods — **Borda count** and **Condorcet voting** — and records all three in the ADR. The "winner" is still the average-rank winner (the v0.5.7 default), but discrepancies between methods are surfaced as a `aggregation-method-discrepancy` flag.

## Why this matters

Aggregation method dependence is real. Examples:

- **Borda flips average-rank** when a polarizing response gets one strong endorsement and three middle rankings — average rank looks middling, Borda may look strong.
- **Condorcet may have no winner** when preferences cycle (A > B > C > A across panelists) — the absence of a Condorcet winner is itself signal.
- **Average-rank is biased toward middle-ranking responses** when panelists disagree strongly at the extremes — it converges on the "least-objectionable" rather than the "most-correct" answer.

Documenting all three methods means the convening council can see **whether the choice of aggregation matters for THIS panel's verdict**. If all three agree, confidence is high. If they diverge, the question may be genuinely contested, and the Chairman's synthesis bears more weight than the aggregate.

## The three methods

### 1. Average rank (v0.5.7 baseline, still the default winner)

```
For each response R:
  positions = [rank(R) per panelist per ordering]
  avg_rank(R) = mean(positions)
Winner = min(avg_rank)
```

Example: 4 panelists × 2 orderings = 8 ballots per response.

**Properties:**
- Simple, intuitive
- Robust to single-panelist outliers
- Biased toward middle-of-pack responses (the "compromise" winner)

### 2. Borda count

```
For each ballot (one panelist's ranking under one ordering):
  Each response gets points = (n - position), where n = panel size
  e.g., for 4 panelists: #1 = 3 points, #2 = 2 points, #3 = 1 point, #4 = 0 points
For each response R:
  borda_score(R) = sum of points across all ballots
Winner = max(borda_score)
```

**Properties:**
- Rewards consistently-strong rankings
- Less robust to single-panelist outliers than average-rank (a single #1 vote is worth a lot)
- Surfaces "polarizing-but-strong" responses that average-rank smooths over

### 3. Condorcet voting

```
For each PAIR of responses (R_i, R_j):
  pairwise_wins(R_i, R_j) = count of ballots where R_i is ranked above R_j
A response R is a Condorcet winner iff:
  for every other response R': pairwise_wins(R, R') > pairwise_wins(R', R)

If no response satisfies the above:
  no Condorcet winner exists (a "Condorcet cycle")
```

**Properties:**
- Strongest theoretical guarantee — the Condorcet winner beats every other option in head-to-head
- May not exist (cycles are signal — preferences are genuinely contested)
- Computationally O(n²) but n ≤ 4 in our panel so trivial

## Aggregation-method-discrepancy flag

After all three methods are computed:

```
agreement_check:
  if avg_rank_winner == borda_winner == condorcet_winner:
    full_agreement: true
    aggregation_discrepancy: false
  elif condorcet_winner is None (cycle exists):
    aggregation_discrepancy: true
    discrepancy_type: condorcet_cycle
    note: "preferences are genuinely contested — Chairman synthesis bears more weight"
  elif avg_rank_winner != borda_winner:
    aggregation_discrepancy: true
    discrepancy_type: rank_vs_borda
    note: "polarizing-but-strong vs middle-of-pack distinction matters here"
  else:
    aggregation_discrepancy: true
    discrepancy_type: condorcet_vs_others
    note: "head-to-head comparison favors a different response than aggregate methods"
```

The convening council sees this flag prominently in the Chairman's synthesis prompt. The User sees it in any USER-ONLY decision brief.

## ADR fields added by aggregation-method recording

```yaml
aggregation:
  default_method: average_rank
  results:
    average_rank:
      winner: panelist_2
      scores:
        panelist_1: 2.50
        panelist_2: 1.25
        panelist_3: 2.75
        panelist_4: 3.50
    borda_count:
      winner: panelist_2
      scores:
        panelist_1: 12
        panelist_2: 19
        panelist_3: 11
        panelist_4: 6
    condorcet:
      winner: panelist_2
      pairwise_table: {...}
      cycle_detected: false
  agreement_check:
    full_agreement: true
    aggregation_discrepancy: false
```

## Worked example — the discrepancy case

Suppose 4 panelists × 2 orderings give these rankings (8 ballots total) for responses R1-R4:

| Ballot | 1st | 2nd | 3rd | 4th |
|---|---|---|---|---|
| 1 | R1 | R3 | R2 | R4 |
| 2 | R3 | R1 | R2 | R4 |
| 3 | R1 | R3 | R2 | R4 |
| 4 | R3 | R1 | R4 | R2 |
| 5 | R2 | R1 | R3 | R4 |
| 6 | R2 | R3 | R1 | R4 |
| 7 | R3 | R2 | R1 | R4 |
| 8 | R3 | R1 | R2 | R4 |

- **Average rank:** R3 = 2.0, R1 = 2.0, R2 = 2.5, R4 = 3.875 → **R1 and R3 tie**
- **Borda count:** R3 = 18, R1 = 17, R2 = 13, R4 = 0 → **R3 wins**
- **Condorcet:** R3 beats R1 5-3, R3 beats R2 6-2, R3 beats R4 8-0 → **R3 is Condorcet winner**

In this case, average-rank tie obscures that R3 is the genuine head-to-head winner. The flag fires on `condorcet_vs_others` (Condorcet picks R3 unambiguously, average-rank ties). The Chairman is told this and gives R3 more weight in synthesis.

## When discrepancy matters

- **Single-method dominance:** if all three methods pick the same winner, the panel is well-calibrated; Chairman synthesis can lean confidently on the aggregate.
- **Rank vs Borda discrepancy:** the question is between consensus-builder vs polarizing-but-strong. The Chairman should surface this: "Response R is the consensus pick (average rank #1), but Response R' is the strongest signal (Borda #1, but with one panelist ranking it #4)."
- **Condorcet cycle:** preferences are genuinely contested. The Chairman MUST recommend deferring to the User with all three perspectives attached. No automatic "winner" survives the cycle.

## Cost

Trivial — O(n²) computation in panel-chair on n ≤ 4 panelists. No additional model calls. The aggregation step is computed locally after Stage 2 completes.

## Anti-patterns

- **Don't change the default winner from average-rank without an ADR.** Average-rank is the v0.5.7 baseline; switching default requires a `cross-model-panel-amend` ADR.
- **Don't ignore discrepancy flags.** The whole point is to surface them. A discrepancy that goes unaddressed in the Chairman synthesis is a quality miss.
- **Don't claim a "winner" when a Condorcet cycle exists.** Cycles are honest signal; report them as cycles and defer.
- **Don't add a fourth aggregation method without literature review.** Aggregation methods proliferate fast (Plurality, Approval, IRV, Schulze, etc.) — the three we have cover the major axes of disagreement; adding more is diminishing returns until we have data on which discrepancies matter most in practice.
