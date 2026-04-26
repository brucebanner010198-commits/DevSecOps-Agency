# Cross-vendor opt-in panel via OpenRouter (v0.6.0)

The v0.5.7 baseline runs a Claude-only panel (Opus 4 + Sonnet 4.5 + Haiku 4.5 + Opus 4 with thinking). This is safe (single vendor relationship, no new API key, predictable behavior) but it loses the **genuine model-diversity benefit** — Claude-specific blind spots are not caught by other Claude tiers, because they share architecture, training data composition, and RLHF lineage. v0.6.0 adds an **opt-in cross-vendor mode** via OpenRouter (single API gateway to ~300 frontier models including OpenAI, Google, xAI, Mistral, Meta, etc.).

This mode is **opt-in per panel**, requires the User to provision an OpenRouter API key, and adds a documented line item to `<slug>/cost-estimate.md`. It is not a default for any trigger event.

## When to use cross-vendor

Strong fit:

- **Constitution amendment proposals** — Anthropic's Collective Constitutional AI research finds ensembling principles produces more robust preference models, and cross-vendor ensembling is the strongest version of that principle. Cross-vendor is the recommended mode for amendment work, IF the User has provisioned the OpenRouter key.
- **ASI-class finding determination** — single-vendor blind spots are exactly the failure mode ASI-class is supposed to catch. Cross-vendor materially raises confidence on close calls.
- **High-stakes architectural decisions where Anthropic-specific framing might bias the answer** (e.g., questions about agent governance, tool-use, or safety norms — where Claude's RLHF directly shapes the response).

Weak fit:

- **Routine convening** — the cost increase and key-management overhead aren't justified.
- **Time-pressured decisions** — OpenRouter latency is higher (single-digit seconds extra per panelist) than direct Anthropic API.
- **When the OpenRouter key isn't provisioned** — fall back to Claude-only, document the fallback in the ADR.

## Setup

The User provisions:

1. **OpenRouter account** at <https://openrouter.ai/>.
2. **API key** with credit balance or auto-top-up enabled.
3. **Environment variable** `OPENROUTER_API_KEY` set in the deploy environment for whichever surface invokes the panel-chair.
4. **Per-project budget cap** in OpenRouter's dashboard (recommend $50/month default; raise on need).

The panel-chair detects key presence at convening time:

```
if OPENROUTER_API_KEY is set:
    cross_vendor mode is AVAILABLE (still opt-in per panel)
else:
    cross_vendor mode is UNAVAILABLE — log "openrouter-key-not-provisioned" in ADR if requested
```

## Cross-vendor panel composition

The v0.6.0 standard cross-vendor panel:

| Slot | Model (OpenRouter ID) | Why |
|---|---|---|
| Panelist 1 | `anthropic/claude-opus-4-6` | Anchor — keeps Claude in the panel for continuity with v0.5.7 |
| Panelist 2 | `openai/gpt-5.1` | Different architecture, different RLHF lineage |
| Panelist 3 | `google/gemini-3-pro-preview` | Different architecture, different training-data composition |
| Panelist 4 | `x-ai/grok-4` OR `mistralai/mistral-large-2` | Fourth vendor for genuine diversity |

The Chairman defaults to the active CEO persona (Claude Sonnet 4.5 via direct Anthropic API, NOT via OpenRouter — Chairman synthesis stays inside the existing vendor relationship for predictable cost + behavior).

**Why Claude is in the panel:** removing Claude entirely would lose the continuity of evaluation behavior we've calibrated against. Keeping one Claude slot anchors the panel to known baselines.

## Procedure

Identical to v0.5.7 single-round (or v0.6.0 multi-round / adversarial-pair) — only the panelist API endpoint changes:

- Panelists invoked via OpenRouter: HTTP POST to `https://openrouter.ai/api/v1/chat/completions` with `Authorization: Bearer ${OPENROUTER_API_KEY}` and the model's OpenRouter ID
- Chairman invoked via direct Anthropic API as usual
- Stage 1 / Stage 2 / Stage 3 prompts unchanged
- Bias-mitigation procedures unchanged (dual-ordering, self-enhancement check, etc.)

## Vendor diversity in panel-rotation

`panel-rotation.md` adds a **vendor-rotation rule** for cross-vendor panels:

- No more than 2 consecutive cross-vendor panels with identical vendor mix.
- At least one vendor change per quarter for any given trigger category.
- Vendor mix is logged in the rotation entry alongside model mix.

Rationale: vendor-specific blind spots can drift just as model-specific blind spots can. Rotating vendors hardens against the cross-vendor analogue of judge drift.

## ADR fields added by cross-vendor mode

```yaml
mode: cross-vendor  # or cross-vendor-multi-round, cross-vendor-adversarial-pair
panel:
  - panelist: 1
    model: anthropic/claude-opus-4-6
    vendor: anthropic
    api_route: openrouter
  - panelist: 2
    model: openai/gpt-5.1
    vendor: openai
    api_route: openrouter
  - panelist: 3
    model: google/gemini-3-pro-preview
    vendor: google
    api_route: openrouter
  - panelist: 4
    model: x-ai/grok-4
    vendor: xai
    api_route: openrouter
chairman:
  model: claude-sonnet-4-6
  vendor: anthropic
  api_route: anthropic-direct  # not openrouter
openrouter_key_status: provisioned  # or fallback-to-claude-only
vendor_diversity:
  unique_vendors: 4
  rotation_compliant: true  # last 2 panels had different vendor mix
```

## Cost

OpenRouter pricing varies by model. Rough estimates per panel run (single-round, ~13 model-call equivalents):

- Claude-only panel (v0.5.7 baseline): ~$0.30-$0.60 per panel
- Cross-vendor panel: ~$0.80-$2.00 per panel (depends on vendor mix; GPT-5.1 and Gemini-3-Pro are pricier than Sonnet/Haiku)
- Multi-round cross-vendor 2-round: ~$1.20-$3.00
- Multi-round cross-vendor 3-round: ~$1.80-$4.50

Per `COST-AWARENESS.md` §2.4, cross-vendor panels MUST be line-itemed in `<slug>/cost-estimate.md` with the OpenRouter spend separated from direct-Anthropic spend (the spike-detector treats them as different cost categories).

## Failure modes & graceful degradation

| Failure | Detection | Response |
|---|---|---|
| OpenRouter API down | HTTP 5xx on convening | Log `cross-vendor-unavailable` in ADR; fall back to Claude-only panel; complete the ADR with mode = `claude-only-fallback` |
| One vendor down (e.g., OpenAI outage) | Per-panelist HTTP error | Log `panelist-N-vendor-outage` in ADR; substitute that slot with a Claude tier (Sonnet 4.5 is the default substitute); complete with mode = `cross-vendor-degraded` |
| OpenRouter rate-limit hit | HTTP 429 | Log + retry once with 30s backoff; if still 429, fall back as above |
| OpenRouter budget exhausted | HTTP 402 / explicit error | Log `openrouter-budget-exhausted` and notify User via `inbox.json` priority `cost-spike` (per COST §2.11); fall back to Claude-only |
| Cross-vendor disabled mid-panel by User | inbox.json control flag | Complete in-flight panelists; fall back to Claude-only for remainder; ADR notes mid-panel mode change |

## Security considerations

- **OpenRouter key is a raw secret** per Constitution §8.5 (non-waivable raw-secret class). MUST live in vault refs only — never in committed config, never in shell history, never logged.
- **Cross-vendor data flow** — the panel question is sent to multiple vendors. For projects that handle regulated or proprietary data, the security-lead MUST file a `cross-vendor-data-flow-authorized` ADR before convening with that data, per `councils/security/REVIEW-KIT.md` §2.8 (third-party isolation) and §7.6 (vendor compliance).
- **Provider TOS check** — each vendor's terms of service govern data-handling for sent prompts. The compliance-officer specialist tracks the per-vendor TOS in `_vision/legal/vendor-tos-tracker.md`; convening cross-vendor with regulated data MUST cite the current TOS row.

## Anti-patterns (in addition to v0.5.7's anti-patterns)

- **Don't convene cross-vendor on regulated data without the security-lead ADR.** TOS and data-handling vary by vendor.
- **Don't bypass the OpenRouter budget cap.** Set the cap in OpenRouter's dashboard; if you hit it, accept the fallback.
- **Don't substitute a missing vendor with a Claude tier silently.** Log the substitution as `panelist-N-vendor-outage` in the ADR.
- **Don't run cross-vendor every panel by default.** Single-vendor Claude-only is the default; cross-vendor is opt-in per panel for the documented strong-fit cases.
- **Don't claim cross-vendor diversity if 3 of 4 slots are the same vendor.** That's not diversity; it's a single-vendor panel with a token outsider. Minimum 3 distinct vendors for the cross-vendor mode label to apply.
