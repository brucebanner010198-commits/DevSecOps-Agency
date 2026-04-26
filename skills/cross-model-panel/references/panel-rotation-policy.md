# Panel rotation policy

The `panel-chair` cycles model combinations across consecutive panels to mitigate **judge drift** — the documented effect that models used as judges over time develop systematic biases in their evaluations.

## Why rotation matters

Per the LLM-as-Judge survey, judge drift is a real effect even within a model's training-data lifetime. Two consecutive panels with identical composition that produce divergent verdicts on similar questions are more likely to reflect drift than to reflect a real change in the underlying truth. By rotating composition, we (a) get cross-composition data points, (b) prevent any single model's quirks from dominating the receipts, (c) make `judge-drift-detected` an empirically-detectable finding instead of an excuse.

## The rotation log

Lives at `_vision/cross-model-panel/panel-rotation.md`. Append-only per Constitution §5.2. One row per panel run.

Format:

```
| Date       | Panel-ID | Convening reason                  | Panel composition                                         | Chairman      | Notes |
|------------|----------|-----------------------------------|-----------------------------------------------------------|---------------|-------|
| 2026-04-25 | P-001    | first-ever panel; smoke test     | Opus-4 / Sonnet-4.5 / Haiku-4.5 / Opus-4-thinking         | CEO persona   | baseline |
| 2026-05-12 | P-002    | ASI-class finding determination  | Opus-4 / Sonnet-4.5 / Haiku-4.5 / Opus-4-thinking         | Sonnet-4.5    | same-comp; drift baseline |
| 2026-05-30 | P-003    | Constitution amendment proposal  | Sonnet-4.5 / Opus-4 / Haiku-4.5 / Opus-4-thinking         | CEO persona   | rotated panelist 1 from Opus to Sonnet to break monotony |
```

## Rotation rules (v1.0)

1. **Standard panel slot composition:** four panelists across three Claude tiers (Opus + Sonnet + Haiku + Opus-with-thinking). The slot composition itself rarely changes — what rotates is which slot is "active" in the synthesis-influencing weight.
2. **Chairman rotation:** the Chairman role MUST cycle across at least 3 distinct configurations within any 5 consecutive panels. Configurations:
   - CEO persona (Sonnet 4.5)
   - Opus 4
   - Opus 4 with thinking
   - Sonnet 4.5 (non-CEO-persona)
   No more than 2 consecutive panels with the same Chairman config.
3. **Same-question re-panel cooldown:** if a panel has been run on a substantively-similar question, the next panel on that question MUST use a different Chairman config AND at least one different panelist tier-mix. This catches drift specifically on repeat questions.
4. **Constitutional amendment exception:** for Constitution amendment proposals, the Chairman MUST be a separate model from any panelist (no self-chairing on amendment work — matches the no-self-dealing principle in Constitution §8). Rotation rules above remain in force.

## When rotation breaks

If `panel-rotation.md` shows the same composition for ≥ 3 consecutive panels (rule 2 violation) or the same Chairman + panelist set for repeat-question runs (rule 3 violation), the panel-chair files a `panel-rotation-violation` ADR. Repeat violations escalate to CRT for review (the bias-mitigation co-owner).

## Drift detection signal

The panel-chair compares ranking patterns across panels of identical composition. If the same panelist's #1 ranking position drifts by ≥ 1 position over a calendar quarter (controlling for question difficulty), file a `judge-drift-detected` row in `_vision/cross-model-panel/<YYYY-QN>.md`. This is not a red — it's a signal worth the User's attention. Repeated drift across multiple quarters routes through CEVO's regression-detector.

## Future enhancements (v0.6.0+)

- Cross-vendor rotation: once OpenRouter is wired in, the rotation includes vendor-mix not just tier-mix. Vendor-diversity is the strongest signal against single-vendor blind spots.
- Drift-detection automation: a regression-detector specialist could compare panel-rotation outputs across quarters and surface drift signal automatically rather than relying on panel-chair manual inspection.
- Adversarial-pair mode: when adversarial mode is enabled (deferred to v0.6.0), the rotation log records which pair was assigned affirmative/negative and rotates those assignments too.
