# Multi-round debate mode (v0.6.0)

The v0.5.7 baseline runs a single round (Stage 1 → Stage 2 → Stage 3). Multi-round debate adds rounds 2/3 where panelists see each other's evaluations and revise their own positions. The Multi-Agent Debate literature (Du et al. 2023, "Improving Factuality and Reasoning") shows multi-round helps measurably on math, factual recall, and structured reasoning — but introduces the **funneling effect** (Springer Nature 2025 survey on Multi-Agent Debate Strategies): semantic diversity is highest at round 1 and narrows on each subsequent round.

This skill makes multi-round **opt-in**, defaults to single-round, and treats round-1 raw responses as the inviolable **diversity record** preserved verbatim regardless of how many rounds run.

## When to use multi-round

Multi-round is appropriate for:

- **Math / factual recall** where revision after seeing peer reasoning measurably improves accuracy (the Du et al. result).
- **Cross-checking technical claims** where a second look at peer evidence catches errors a first pass missed.
- **High-stakes decisions where time is not the constraint** — multi-round costs ~2× the single-round runtime per added round.

Multi-round is INAPPROPRIATE for:

- **Subjective judgment calls** where convergence-by-pressure is worse than honest divergence (e.g., "is this design good?" — preserve disagreement; don't grind it down).
- **Time-pressured decisions** — multi-round adds 60-180s per round.
- **Constitutional amendment proposals.** The Anthropic CCAI ensemble-robustness finding favors PARALLEL deliberation, not iterative; multi-round risks suppressing legitimate dissent that the User needs to see.

## Procedure

### Round 1 (= Stage 1, identical to single-round)

Send the question to each panelist independently. Collect raw responses. **Preserve verbatim in the ADR as `stage_1_round_1` — this is the diversity record. Never overwrite.**

### Round 2 (new in v0.6.0)

Each panelist receives:
- The original question
- Their own round-1 response (labeled "Your previous response")
- The other panelists' round-1 responses (anonymized as Response B, C, D — your own is always Response A from your perspective)

Prompt:

```
You answered this question in round 1. You now see the other panelists' round-1 responses, anonymized.

Original question:
<QUESTION>

Your round-1 response (Response A):
<YOUR_ROUND_1>

Other panelists' round-1 responses, anonymized:

Response B:
<OTHER_1>

Response C:
<OTHER_2>

Response D:
<OTHER_3>

Considering the other responses, do any of them contain reasoning, evidence, or framing that you find more correct than your own? You may revise your position. You may also reaffirm your position with stronger reasoning. State explicitly:

REVISED POSITION (or REAFFIRMED):
<your updated answer; if reaffirmed, restate the position with any sharpened reasoning>

KEY DISAGREEMENTS (if any):
<bullet list of points where you remain in disagreement with one or more peers, named as "Response X"; this is REQUIRED — do not collapse disagreements>
```

Collect round-2 responses. Preserve verbatim as `stage_1_round_2`.

### Round 3 (optional — only invoke when round-2 disagreements remain on a critical fact)

Same prompt format as round 2, but each panelist sees the round-2 responses (not round-1). Prompt explicitly notes that this is the final round.

### Stage 2 (peer ranking — runs on the FINAL round's responses)

Anonymized peer review per the v0.5.7 procedure (dual-ordering, FINAL RANKING format), but the responses being ranked are from the LAST round (round 2 or 3, not round 1).

### Stage 3 (Chairman synthesis — sees ALL rounds)

The Chairman receives:
- Original question
- All round-1 raw responses (the diversity record) with panelist identity revealed
- All round-2 responses
- (If applicable) all round-3 responses
- Aggregate ranking from Stage 2

Chairman prompt addition:

```
This panel ran multiple rounds. You see round 1 (the diversity record — original divergence) and round N (final positions after deliberation). Your synthesis MUST:

1. Note explicitly which positions converged across rounds and which remained in disagreement.
2. Do NOT treat convergence as automatically "correct" — convergence under deliberation pressure is a known anti-pattern (the funneling effect). If round-1 had a defensible minority position that got abandoned in round 2 without strong rebuttal, surface that.
3. The KEY DISAGREEMENTS captured at each round are part of the receipt — preserve them in your synthesis even if they didn't make it into the final ranking.
```

## Funneling-effect mitigation (the load-bearing reason this is opt-in)

The Multi-Agent Debate Strategies survey (Springer 2025) documents that semantic diversity is highest in round 1 and narrows monotonically. Even "good" convergence loses signal. Three mitigations:

1. **Round-1 is preserved verbatim, always.** The ADR's `stage_1_round_1` field is the diversity record; future audits MUST be able to reconstruct what each panelist thought before deliberation pressure.
2. **KEY DISAGREEMENTS are required at every round.** Panelists are explicitly prompted to list points of remaining disagreement. Empty `KEY DISAGREEMENTS` blocks fire a `funneling-suspicious` flag in the ADR.
3. **Chairman MUST note convergence vs disagreement.** A synthesis that papers over honest dissent gets caught at the CAO trust-scorecard spot-check.

## ADR fields added by multi-round mode

```yaml
mode: multi-round
rounds_run: 2  # or 3
stage_1_round_1:
  - panelist: 1
    raw: <verbatim>
  # ...
stage_1_round_2:
  - panelist: 1
    revised_position: <verbatim>
    reaffirmed: false  # or true
    key_disagreements: ["...", "..."]  # MUST be non-empty unless full convergence is genuine
  # ...
funneling_flags:
  empty_disagreements_count: 0  # > 0 = suspicious
  convergence_without_rebuttal: false
  # ...
```

## Cost

Multi-round multiplies the panel cost roughly:
- Round 1: 4 model-call equivalents (same as single-round Stage 1)
- Each additional round: 4 model-call equivalents (same prompt size as round 1, plus the peer responses)
- Stage 2: still 8 (4 panelists × 2 orderings)
- Stage 3: 1, but the Chairman sees more context (round 1 + round 2 + ranking) → ~1.5x of single-round Stage 3

**Single-round panel:** ~13 model-call equivalents.
**2-round panel:** ~17 model-call equivalents (~30% more).
**3-round panel:** ~21 model-call equivalents (~60% more).

Per `COST-AWARENESS.md` §2.4, multi-round panels MUST be line-itemed separately in the project cost estimate.

## Anti-patterns (in addition to v0.5.7's anti-patterns)

- **Don't run multi-round on subjective judgment calls.** Convergence-by-pressure is the wrong outcome.
- **Don't accept empty KEY DISAGREEMENTS without checking.** Either the question really has full convergence (rare on hard questions) or the prompt failed to elicit honest dissent.
- **Don't overwrite round-1 outputs with round-2 in the ADR.** Each round is its own field; round 1 is the diversity record.
- **Don't run more than 3 rounds.** The funneling-effect literature shows diminishing-then-negative returns past 3 rounds; long debates harm calibration.
- **Don't use multi-round on Constitution amendment proposals.** Use single-round per the v0.5.7 procedure — the User needs to see honest parallel divergence, not deliberated consensus.
