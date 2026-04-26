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

## v0.6.0 additions — vendor and role rotation

### Cross-vendor rotation (added v0.6.0)

When a panel runs in `cross-vendor` mode (per [`cross-vendor-panel.md`](cross-vendor-panel.md)), the rotation log captures vendor mix in addition to model mix:

```
| Date       | Panel-ID | Mode          | Vendor mix                         | Notes |
|------------|----------|---------------|------------------------------------|-------|
| 2026-05-15 | P-014    | cross-vendor  | anthropic + openai + google + xai  | first ever cross-vendor; baseline |
| 2026-06-02 | P-019    | cross-vendor  | anthropic + openai + google + xai  | 2nd consecutive same vendor mix; rotate next |
| 2026-06-18 | P-024    | cross-vendor  | anthropic + openai + google + mistral | rotated xai → mistral per rule below |
```

**Vendor-rotation rules:**
- No more than **2 consecutive** cross-vendor panels with identical vendor mix.
- At least **one vendor change per quarter** for any given trigger category (ASI-class, Constitution amendment, etc.).
- Minimum 3 distinct vendors for the cross-vendor label to apply (per `cross-vendor-panel.md`).

**Vendor-rotation enforcement:** if a request would violate the consecutive-mix cap, the panel-chair substitutes the longest-serving vendor in the mix with a different supported vendor and logs `vendor-rotation-substitute` in the ADR.

### Adversarial-role rotation (added v0.6.0)

When a panel runs in `adversarial-pair` mode (per [`adversarial-pair.md`](adversarial-pair.md)), the rotation log captures role assignment per panel:

```
| Date       | Panel-ID | Mode             | Role assignment                                              | Notes |
|------------|----------|------------------|--------------------------------------------------------------|-------|
| 2026-05-20 | P-016    | adversarial-pair | Slot1=AFF, Slot2=NEG, Slot3=PARALLEL, Slot4=PARALLEL         | first; default rotation |
| 2026-06-05 | P-021    | adversarial-pair | Slot2=AFF, Slot1=NEG, Slot3=PARALLEL, Slot4=PARALLEL         | swapped AFF/NEG to break monotony |
```

**Role-rotation rule:** no panelist may be AFFIRMATIVE more than **60% of the trailing 10** `adversarial-pair` panels. Same cap applies to NEGATIVE. The panel-chair computes `role_history_check.{slot_id}_affirmative_pct_last_10` before each adversarial panel and fires `role-rotation-violation` ADR if the cap would be breached.

**Why 60%:** documented threshold from the Multi-Agent Debate Strategies survey for adversarial settings — high enough to allow meaningful rotation, low enough to prevent stable "this model always argues yes" patterns that the Chairman could systematically discount.

## Future enhancements (v0.6.1+)

- **Drift-detection automation:** a regression-detector specialist could compare panel-rotation outputs across quarters and surface drift signal automatically rather than relying on panel-chair manual inspection.
- **Tier-mix experimentation:** explore whether 2-Opus + 2-Haiku panels (extreme tiers) produce different deliberation patterns than the default tier mix.
- **Multi-round + adversarial composition:** once the funneling+polarization compounding literature is characterized, add the composed mode and its rotation rules.
