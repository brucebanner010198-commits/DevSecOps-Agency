---
name: cross-model-panel
description: Three-stage cross-model deliberation skill for the Agency's highest-stakes decisions. Concept-port of llm-council (Karpathy, no-LICENSE Saturday hack — pattern only, no code copied). Panel of Claude tiers (Opus 4 + Sonnet 4.5 + Haiku 4.5 + Opus 4 with thinking) answers a hard question independently (Stage 1), evaluates each other's responses anonymized as Response A/B/C/D with dual-order bias mitigation (Stage 2), then a designated Chairman synthesizes (Stage 3). Every panel files an append-only ADR with all raw responses + both Stage-2 orderings + per-panelist rankings + bias-mitigation evidence + Chairman synthesis. Default triggers: ASI-class findings (Constitution §8.5), Constitution amendment proposals (Article X), USER-ONLY decisions above the COST §2.4 threshold. Owned by CEVO with CRT co-ownership. Independence rule per Council file. Cites Council Mode (35.9% HaluEval reduction), Anthropic CCAI ensemble robustness finding, and the broader Multi-Agent Debate literature.
metadata:
  version: "2.0.0"
  ratified: "2026-04-26"
  shipped_with_plugin: "0.6.0"
  baseline_shipped_with_plugin: "0.5.7"
---

# cross-model-panel

## When to trigger

Default-trigger events (auto-invoke):

- **ASI-class finding** per Constitution §8.5 (non-waivable). Cross-model panel review hardens the determination.
- **Constitution amendment proposal** per Article X. Anthropic's Collective Constitutional AI work and the constitutional-ensemble research find that ensembling principles "led to notably more robust preference model behavior."
- **USER-ONLY decision** where COST-AWARENESS.md §2.4 (pre-deploy cost estimate) would apply at material scale (≥ $1k / month projected, or any production data path).

Opt-in invocation by any council on demand. Panel-chair logs the convening reason in the ADR.

Never auto-invoke during a live incident response — incidents use the existing `incident-response` flow, not deliberation.

## Inputs

- A single high-stakes question, one paragraph max.
- Convening reason (default-trigger or council on-demand).
- Optional panel override (default = the standard 4-tier panel below).
- Optional Chairman override (default = the CEO persona for this session).

## Outputs

- `_decisions/ADR-NNNN-cross-model-panel-<topic>-<YYYY-MM-DD>.md` — append-only, contains:
  - Convening reason + question
  - Panel composition (which models, which versions)
  - Stage 1 raw responses (one per panelist)
  - Stage 2 evaluations + rankings — **both order [A,B,C,D] and order [D,C,B,A]** (position-bias mitigation)
  - Aggregate ranking (average position across both orderings, all panelists)
  - Style-fingerprint flag per panelist (self-enhancement bias check)
  - Stage 3 Chairman synthesis
  - Cost summary (tokens + dollars per stage; total)
  - Convening-to-completion wall time
- `_vision/cross-model-panel/<YYYY-QN>.md` — quarterly index of panels run, for the cost scorecard and the trust scorecard.

## The standard panel (Claude-only, v0.5.7)

| Slot | Model | Why |
|---|---|---|
| Panelist 1 | `claude-opus-4-6` | Top-tier reasoning, no thinking mode |
| Panelist 2 | `claude-sonnet-4-6` | Strong general performance, balanced |
| Panelist 3 | `claude-haiku-4-5-20251001` | Fast, different training-data cutoff inflection |
| Panelist 4 | `claude-opus-4-6` (thinking enabled) | Same base as #1 but with extended thinking — gives the panel one "deliberative" voice |

The Claude-only panel keeps the Agency inside the existing vendor relationship and avoids a new API key dependency. **Trade-off acknowledged:** the genuine model-diversity benefit (cross-vendor weighting that catches Claude-specific blind spots) is reduced. v0.6.0+ may add a cross-vendor opt-in panel via OpenRouter once the User decides to take on that billing exposure.

The Chairman defaults to the active CEO persona for the session (so the panel's synthesis is integrated into the Agency's normal voice). The Chairman MAY be a panelist or a separate model; if a panelist also chairs, the ADR notes this and the Chairman's synthesis is fact-checked against the other three panelists' rankings.

## The three-stage procedure

### Stage 1 — Independent first opinions (parallel)

Send the question to each panelist independently. Use identical wording for each. No knowledge of the other panelists. Collect responses. Time-box to 60 seconds per panelist (the slowest panelist sets the wall clock).

Persist each raw response in the ADR under `## Stage 1 — Raw responses`. Each response includes the panelist's identity (real model name) — this is for the audit trail; the panelists themselves never see this metadata.

### Stage 2 — Anonymized peer review with dual-order bias mitigation

For each panelist, prepare a Stage-2 prompt containing:

- A leading instruction: *"You will see four responses to the same question. They are from different language models. They are anonymized as Response A, B, C, D. Disregard any stylistic clues you might use to identify a specific model. Evaluate strictly on factual correctness, completeness, and reasoning quality."*
- The four Stage-1 responses, labeled Response A through D.
- A strict output format: *"Provide your evaluation, then a section header `FINAL RANKING:` followed by a numbered list `1. Response X` through `4. Response Y`, ranking from best to worst. No additional text after the ranking."*

**Position-bias mitigation (added per ACL 2025 position-bias research, GPT-4 shows 40% inconsistency from order alone):** run Stage 2 **twice** for each panelist:

- **Order forward:** A=Panelist 1, B=Panelist 2, C=Panelist 3, D=Panelist 4
- **Order reversed:** A=Panelist 4, B=Panelist 3, C=Panelist 2, D=Panelist 1

The per-panelist ranking is the average of the two orderings (after de-anonymization). If forward and reversed give wildly different rankings (any panelist's average position differs by ≥ 1.5 between the two), flag a `position-bias-detected` row in the ADR — that's a finding worth noting.

**Verbosity-bias mitigation:** the use of rank (1st-4th) instead of score (1-10) is itself the mitigation. Per the LLM-as-Judge survey, rank-based evaluation reduces the ~15% verbosity inflation that score-based evaluation introduces. Do NOT use a 1-10 scale.

**Self-enhancement bias check:** after Stage 2, the panel-chair compares each panelist's Stage 1 response style against its #1-ranked Stage 2 response. If a panelist consistently ranked its own style highly (style-similarity > 0.7 by simple n-gram overlap), file a `self-enhancement-bias-detected` row. The 5-7% bias documented in the LLM-as-Judge survey is small enough we don't reject the ranking, but it's worth recording for the trust scorecard.

### Stage 3 — Chairman synthesis

The Chairman receives:

- The original question.
- All four Stage-1 raw responses (with panelist identity revealed in the prompt).
- The aggregate ranking from Stage 2.
- Any bias flags raised in Stage 2.

The Chairman produces a single integrated answer. The Chairman's prompt explicitly instructs: *"Synthesize the strongest reasoning from each panelist. Where panelists disagree, note the disagreement and choose a position with stated reason. Do not paper over genuine divergence."*

The synthesis is what the Agency presents to the convening council (or to the User, in USER-ONLY cases). The Stage-1 raw responses are preserved in the ADR as the **diversity record** — the funneling-effect research (peak diversity in round 1, narrows on synthesis) means the raw round-1 outputs may carry signal that the synthesis necessarily compresses.

## The receipt — every panel files an ADR

`ADR-NNNN-cross-model-panel-<topic>-<YYYY-MM-DD>.md`. Required fields:

```yaml
kind: cross-model-panel
status: complete
convened_by: <council-or-trigger>
reason: <text>
question: <one paragraph>
panel:
  - model: claude-opus-4-6
  - model: claude-sonnet-4-6
  - model: claude-haiku-4-5-20251001
  - model: claude-opus-4-6
    thinking: true
chairman: <model-id>
stage_1:
  - panelist: 1
    raw: <verbatim response>
  - panelist: 2
    raw: <...>
  # ...
stage_2:
  forward:
    - panelist: 1
      evaluation: <verbatim>
      ranking: ["Response A", "Response C", "Response B", "Response D"]
    # ...
  reversed:
    - panelist: 1
      evaluation: <verbatim>
      ranking: ["Response D", "Response B", "Response C", "Response A"]
    # ...
aggregate_ranking:
  - position: 1
    panelist: <real-model-id>
    avg_position: 1.25
  # ...
bias_flags:
  position_bias_detected: false
  self_enhancement_detected: false
  style_similarity_scores: {...}
stage_3:
  chairman_response: <verbatim>
cost:
  tokens_input: <int>
  tokens_output: <int>
  total_usd: <float>
  per_stage:
    stage_1: <usd>
    stage_2: <usd>  # 2x stage_1 due to dual-ordering
    stage_3: <usd>
wall_time_seconds: <int>
```

The ADR is append-only per Constitution §5.2. Edits = new ADR superseding.

## Independence

`cross-model-panel` is convened by the **`panel-chair` specialist** under CEVO (with CRT co-ownership for the bias-mitigation aspect). Independence rules:

- The panel-chair MUST NOT be a panelist on a panel it chairs (parallels Audit / Eval / Red-Team independence).
- The Chairman role MAY be filled by a panelist OR by a separate model; if a panelist chairs, the ADR records this and the panelist's Stage-2 ranking is excluded from the aggregate (to avoid self-grading the synthesis input).
- For Constitution amendment proposals, the Chairman MUST be a separate model from any panelist (no self-chairing on amendment work — this matches the no-self-dealing principle in Constitution §8).
- The panel-chair maintains `_vision/cross-model-panel/panel-rotation.md` — a rotation log to cycle model combinations across consecutive panels and avoid judge drift (per the LLM-as-Judge survey's documented drift effect).

## Cost discipline (COST-AWARENESS integration)

A four-panelist single-question panel run costs roughly:

- Stage 1: 4 × (Q + R) = ~4 model-call equivalents
- Stage 2: 4 × 2 × (Q + 4R + ranking) = ~8 model-call equivalents (the 2x factor is dual-ordering)
- Stage 3: 1 × (Q + 4R + rankings + synthesis) = ~1 model-call equivalent
- **Total: ~13 model-call equivalents per panel** (vs ~1 for single-model answer)

Per `COST-AWARENESS.md` §2.4 and the LLM-as-Judge survey's "3-5x cost for 30-40% bias reduction" finding, the cost is justified for high-stakes decisions and excessive for routine ones. The default-trigger set above is calibrated to keep panels rare and high-value.

For any project that defaults to panel review in production (rather than just at Agency-internal decision points), `<slug>/cost-estimate.md` MUST line-item the panel costs separately.

## Anti-patterns

- **Don't run a panel during a live incident.** Incidents use `incident-response`. Panels are deliberation, not crisis response.
- **Don't use a panel as a tie-breaker between two equivalent options.** That's overhead theater; use the Chairman directly with both options stated.
- **Don't skip the dual-ordering even if it's faster.** The 40% position-bias finding is real. Cutting Stage 2 in half cuts the bias mitigation in half.
- **Don't aggregate rankings across panels of different model composition.** Judge drift makes inter-panel comparison invalid. Each panel is a self-contained data point.
- **Don't skip the bias-flag step.** Even when the flags don't fire, recording "checked, none triggered" is the receipt that proves the check happened.
- **Don't paraphrase the Stage 1 raw responses in the ADR.** Verbatim or it's not a receipt.
- **Don't treat the Chairman synthesis as authoritative without the panel raw.** A reader who only reads Stage 3 has lost the diversity record; route them back to Stage 1 if they question the synthesis.

## Provenance & inspiration

This skill is a **concept-port**, not a code-port:

- **Inspiration:** [llm-council](https://github.com/brucebanner010198-commits/llm-council) by the user (`brucebanner010198-commits`) — a Saturday hack by Karpathy-style prototyping, FastAPI + React + OpenRouter, no LICENSE declared. The 3-stage pattern (independent → anonymized peer review → Chairman synthesis) and the strict `FINAL RANKING:` format are taken from that repo. Code is NOT imported (no LICENSE, and the FastAPI/React shape doesn't fit a Claude Code plugin).
- **Empirical validation:** Council Mode paper (35.9% relative reduction in hallucination on HaluEval, 7.8-point improvement on TruthfulQA).
- **Bias-mitigation engineering:** A Survey on LLM-as-a-Judge (arxiv 2411.15594), Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge (arxiv 2410.02736), A Systematic Study of Position Bias in LLM-as-a-Judge (ACL 2025).
- **Constitution amendment auto-trigger justification:** Anthropic's Collective Constitutional AI research finding that ensembling over principles produces more robust preference models.
- **Multi-Agent Debate context:** Improving Factuality and Reasoning with Multiagent Debate (composable-models.github.io), Multi-Agent Debate Strategies survey (Springer Nature 2025).

Synthesis is original. No text from any cited source is copied.

## Interaction with other skills

| Skill | How cross-model-panel composes |
|---|---|
| `red-team` | Auto-triggers cross-model-panel on ASI-class finding determination. Panel raw + ranking become inputs to the red-team verdict. |
| `audit` | Panel ADRs are inspected at the quarterly trust-scorecard publish for completeness and bias-flag patterns. |
| `eval` (existing CEVO suite) | Independent of the regression / benchmark / budget specialists. Cross-model-panel is a *deliberation* tool, not an *evaluation* tool — though it's housed in the same council. |
| `model-routing` | Panel-chair queries `model-routing` for current vendor/model availability; if a panelist's model is degraded, falls back to the documented backup model. |
| `waivers` | Constitution amendment ADRs that came out of cross-model-panel deliberation are linked from any related waiver ADR. |
| `rca` | A `chaos-finding` (per `RESILIENCE.md > Chaos engineering`) of severity ≥ high MAY auto-invoke a cross-model-panel for the corrective-action stepping stone. |
| `cost-gate` (runtime hook) | Each panel run logs to `_vision/cost/manual-billing.csv` so the spike-detector can see panel-cost trends. |

## v0.6.0 — research-grade modes (all opt-in, defaults unchanged)

The v0.5.7 baseline (single-round, parallel, Claude-only, average-rank aggregation) remains the default. v0.6.0 adds four opt-in modes documented in their own reference files. Each is opt-in PER PANEL; modes can compose where the literature supports it (multi-round + cross-vendor: yes; adversarial-pair + multi-round: deferred to v0.6.1+).

| Mode | Reference | When to use | Default? |
|---|---|---|---|
| **Multi-round debate** | [`references/multi-round-debate.md`](references/multi-round-debate.md) | Math, factual recall, structured reasoning where revision improves accuracy. INAPPROPRIATE for subjective judgment, time-pressured decisions, or Constitution amendments (funneling effect risks suppressing legitimate dissent). Round-1 raw is preserved verbatim as the inviolable diversity record. | No |
| **Adversarial-pair** | [`references/adversarial-pair.md`](references/adversarial-pair.md) | Binary, comparative, or verdict-frame questions where parallel panels might converge prematurely. Two panelists assigned AFFIRMATIVE / NEGATIVE roles; the other two run parallel. Role-rotation cap: no panelist AFFIRMATIVE > 60% of trailing 10 panels. INAPPROPRIATE for open-ended generative questions or Constitution amendments. | No |
| **Cross-vendor via OpenRouter** | [`references/cross-vendor-panel.md`](references/cross-vendor-panel.md) | High-stakes decisions where Claude-specific blind spots matter — Constitution amendments (RECOMMENDED if key provisioned per Anthropic CCAI ensemble-robustness finding), ASI-class determinations, governance questions where Claude's RLHF could bias the answer. Requires User-provisioned `OPENROUTER_API_KEY`; minimum 3 distinct vendors for the label to apply. | No |
| **Score-aggregation comparison** | [`references/score-aggregation.md`](references/score-aggregation.md) | Always computed, always recorded — average rank (default winner) + Borda count + Condorcet. Discrepancies fire `aggregation-method-discrepancy` flag. Condorcet cycles signal genuinely contested preferences and route to User. | Always-on (recording only; default winner unchanged) |

### Composition rules

- `multi-round` + `cross-vendor`: supported. The cross-vendor cost multiplies with rounds (~$1.20-$3.00 for 2-round cross-vendor).
- `adversarial-pair` + `multi-round`: deferred to v0.6.1+ pending literature on funneling+polarization compounding.
- `adversarial-pair` + `cross-vendor`: supported. Useful for "which-vendor-makes-the-strongest-case" framings on contested governance questions.
- `score-aggregation comparison`: applies to all panel modes; Condorcet cycle detection becomes more likely with cross-vendor (genuine vendor-perspective differences).

## v0.6.1+ deferred

- **Multi-round adversarial.** Funneling-effect compounding with role-induced polarization needs literature characterization first.
- **Multi-round mode for Constitution amendments.** Currently forbidden per `multi-round-debate.md` anti-patterns; revisit if the Anthropic CCAI follow-up research changes the recommendation.
- **More aggregation methods (Schulze, IRV, Approval).** Diminishing returns until we have empirical data on which discrepancies matter most in practice.
- **Automated drift detection across panels** — currently the panel-chair manually inspects `panel-rotation.md` for drift signals; a regression-detector specialist could automate this.

See `references/stage-prompts.md`, `references/bias-mitigation-evidence.md`, `references/panel-rotation-policy.md`, `references/multi-round-debate.md`, `references/adversarial-pair.md`, `references/cross-vendor-panel.md`, and `references/score-aggregation.md` for per-stage and per-mode detail.
