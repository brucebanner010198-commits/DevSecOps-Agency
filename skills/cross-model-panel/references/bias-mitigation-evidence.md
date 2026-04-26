# Bias-mitigation evidence — research backing

This file records the empirical evidence behind each bias-mitigation step in `SKILL.md`. Cite this file when the panel-chair files an ADR; cite specific rows when defending a design choice in an amendment proposal.

## Why we ensemble at all

| Finding | Source | Magnitude |
|---|---|---|
| Council-mode (3-stage parallel + peer review + chairman) reduces hallucination on HaluEval | Council Mode paper, arxiv 2604.02923 | **35.9% relative reduction** |
| Same approach improves TruthfulQA | same paper | **+7.8 points** |
| Multi-Agent Debate improves factual accuracy on biography facts | composable-models.github.io | **30%+ reduction in factual errors** |
| Anthropic ensembling over principles → more robust preference model behavior | Collective Constitutional AI (Anthropic) | qualitative; cited as basis for Constitution-amendment auto-trigger |

These results justify the ~13× cost-multiplier (vs single-model answer) for the highest-stakes decision class.

## Position bias

| Finding | Source | Mitigation in our skill |
|---|---|---|
| GPT-4 shows ~40% inconsistency depending on response order alone | A Systematic Study of Position Bias in LLM-as-a-Judge, ACL 2025 | Stage 2 runs **twice per panelist** — once with order [A,B,C,D], once with [D,C,B,A]. Average the rankings. |
| Pairs of (A,B) vs (B,A) often produce different verdicts | Survey on LLM-as-a-Judge (arxiv 2411.15594) | Same dual-ordering mitigation; flag `position-bias-detected` if avg-position differs by ≥ 1.5 between orderings |

## Verbosity bias

| Finding | Source | Mitigation |
|---|---|---|
| Longer responses get inflated scores on 1-10 scales (~15%) | Survey on LLM-as-a-Judge | Use **rank (1st-4th)**, not score (1-10). Rank-based evaluation does not reward length per token. |
| Boilerplate ("As an AI language model...") adds tokens without information | observed in Karpathy llm-council Stage 1 outputs | Stage 1 prompt explicitly forbids the boilerplate opener |

## Self-enhancement bias

| Finding | Source | Mitigation |
|---|---|---|
| Models slightly favor responses stylistically similar to their own (5-7% even when anonymized) | Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge (arxiv 2410.02736) | Compare each panelist's Stage 1 style fingerprint against its #1-ranked Stage 2 response. Flag `self-enhancement-detected` if simple n-gram overlap > 0.7. We do NOT reject the ranking on this signal alone — the bias is small enough we record and watch. |

## Funneling effect

| Finding | Source | Mitigation |
|---|---|---|
| Semantic diversity peaks in round 1; multi-round debates converge and may suppress legitimate dissent | Multi-Agent Debate Strategies survey (Springer Nature 2025) | Preserve Stage 1 raw responses verbatim in the ADR as the "diversity record". Stage 3 Chairman explicitly instructed: "Do not paper over genuine divergence." Multi-round mode is deferred to v0.6.0 specifically because of this risk. |

## Judge drift

| Finding | Source | Mitigation |
|---|---|---|
| Models used as judges over time develop systematic drift in their evaluations | Survey on LLM-as-a-Judge | `panel-chair` maintains `_vision/cross-model-panel/panel-rotation.md` — cycles model combinations across consecutive panels, versions the panel set, notes when active panel changes. Cross-panel comparisons are explicitly invalidated in `SKILL.md > Anti-patterns`. |

## Authority bias

| Finding | Source | Mitigation |
|---|---|---|
| Judges over-weight responses that cite authorities, even fictional ones | Survey on LLM-as-a-Judge | Stage 1 prompt: "Cite reasoning, not authority." Stage 2 prompt: "Evaluate strictly on factual correctness, completeness, and reasoning quality." (No instruction is bullet-proof here — flag for v0.6.0 multi-round mode where adversarial fact-checking can catch this.) |

## Cost-vs-bias trade-off

| Finding | Source | Implication |
|---|---|---|
| Running 3-5 models with majority vote reduces biases 30-40% but costs 3-5x | Survey on LLM-as-a-Judge | Our default-trigger set is calibrated to keep panels rare and high-value (ASI-class, Constitution amendments, USER-ONLY decisions above COST §2.4 threshold). For routine decisions, single-model is fine. |

## Sources (full)

- **Council Mode: Multi-Agent Consensus** — arxiv 2604.02923 — empirical baseline for the 3-stage pattern
- **A Survey on LLM-as-a-Judge** — arxiv 2411.15594 — comprehensive bias enumeration + mitigation patterns
- **Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge** — arxiv 2410.02736 — quantification of self-enhancement, position, verbosity biases
- **A Systematic Study of Position Bias in LLM-as-a-Judge** — ACL 2025 — the 40% inconsistency finding
- **Multi-Agent Debate Strategies survey** — Springer Nature 2025 — funneling-effect documentation
- **Improving Factuality and Reasoning with Multiagent Debate** — composable-models.github.io — biography-facts result
- **Collective Constitutional AI (Anthropic)** — basis for Constitution-amendment auto-trigger
- **llm-council** — the user's own repo (no LICENSE, Saturday hack by Karpathy-style prototyping) — original 3-stage pattern + strict `FINAL RANKING:` format

When new research appears that updates or contradicts any row above, file a `cross-model-panel-amend` ADR with the new evidence; do not silently update this file — append a new row with date.
