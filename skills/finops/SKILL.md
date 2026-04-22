---
name: finops
description: Cost attribution for the agency — 4-column token tracking (prompt / tool / memory / response) × 3-dimension attribution (project / council / agent-phase). Feeds quarterly roll-ups into portfolio audit. Evaluation Council skill, owned by finops-analyst specialist. Pairs with `budget` (total burn) + `observability` (trace source) + `prompt-cache` (savings).
metadata:
  version: 0.3.4
---

# finops

`budget` tracks total burn. `finops` tells you **where** the burn went. Agents make 3–10× more LLM calls than chatbots; without attribution, a single runaway project consumes the quarter.

## 4-column token tracking

Every LLM call span (via `observability`) emits four token counts:

- **prompt_tokens** — system + AGENTS + SKILL assembly + persona + prior context. Mostly cacheable.
- **tool_tokens** — tool schema definitions consumed on tool-use turns.
- **memory_tokens** — retrieved `_memory/` / `_vision/` / `_sessions/` content injected for this dispatch.
- **response_tokens** — completion, plus thinking-budget tokens on reasoning models.

A single `input_tokens` counter hides where the spend is. This schema lets the tuner target the right surface.

## 3-dimension attribution

Every call tagged with:

- **project** — `<slug>` from the dispatch. Rolls up to `_vision/finops/projects/<slug>.jsonl`.
- **council** — one of `ceo`, `research`, `product`, `architecture`, `security`, `execution`, `quality`, `devops`, `docs`, `legal`, `marketing`, `strategy`, `people-ops`, `audit`, `evaluation`, `red-team`, `sre`. Rolls up to `_vision/finops/councils/<c>.jsonl`.
- **agent-phase** — pair of `{agent:<name>, phase:<plan|build|review|ship|close>}`. Rolls up to `_vision/finops/agent-phase/<name>-<phase>.jsonl`.

Build all three from the start — you cannot re-attribute after the fact.

## Invariants

- **Every LLM call emits 4 columns × 3 dims.** `observability` span attributes are authoritative.
- **FinOps logs are append-only.** Corrections via new line; never mutation.
- **Cost lookup table versioned.** `_vision/finops/rates.jsonl` lists per-model, per-token-type rates effective from a date. Old calls priced at their effective-date rate.
- **Cached tokens priced separately.** Anthropic cache-read is ~10 % of base-input price. Cache-creation is ~125 %. `prompt-cache` savings attributed to the project that triggered the cache creation, not the one reading.
- **Thinking-budget tokens counted as response_tokens.** Reasoning models' extended thinking is real spend.

## Weekly FinOps report

`finops-analyst` runs every Monday, output: `_vision/finops/<yyyy-ww>-weekly.md`.

```markdown
# FinOps Weekly — Week <yyyy-ww>

## Totals
- Tokens (in/cached/out): <n>
- Cost: $<x>
- Week-over-week: <±%>

## Top 5 projects by cost
| Project | Cost | Tokens | Notes |

## Top 5 councils by cost
| Council | Cost | Share | Notes |

## Top 10 agent × phase combos
| Agent | Phase | Cost | Share | Notes |

## Anomalies
- <call-out>

## Prompt-cache savings
- Attributed to: <project> $<x>
- Hit rate: <%>

## Budget burn vs. plan
| Project | Budgeted | Spent | Remaining | Burn rate |

## Rung-6 triggers
- <project> burn > 110 % → ladder transition recommended
```

## Cost runaway detection

Trigger conditions (auto-flag, notify via `notify` skill):

- Single span > $1.
- Single trace > $10.
- Project daily spend > 2× trailing-7-day mean.
- Council daily spend > 3× trailing-14-day mean.
- Single agent-phase daily spend > 5× trailing-30-day mean.

Each flag emits `_vision/finops/anomalies/<ts>-<kind>.md` with root-cause prompt for the analyst.

## Quarterly roll-up

- Feeds `audit` portfolio audit under `_vision/audit/<date>-portfolio-finops.md`.
- Per-project TCO (tokens × rate + infra + human-review if any).
- Per-model distribution (Opus %, Sonnet %, Haiku %, external %).
- Cache-hit % trend.
- Budget-burn accuracy (planned vs. actual).
- CEVO uses this for `eval` cost-efficiency metrics.

## Relationship to `budget`

- `budget` owns: plan-time size-class, per-phase allocation, burn cap, Rung-6 trigger at 110 %.
- `finops` owns: where the burn went, attribution dimensions, anomaly detection, savings accounting.
- They share `_vision/finops/` tree. `budget` writes `plans/`. `finops` writes everything else.

## What never happens

- Attribution that rolls up tokens without the 4-column split. It hides the lever.
- Re-pricing old calls at new rates. Old calls priced at the rate effective on their timestamp.
- Cache-creation costs attributed to the wrong project. Whoever created the cache pays for it.
- Anomaly flags suppressed without an ADR. Anomalies either get explained or logged with a remediation owner.
- Sharing FinOps logs with a non-CSRE / non-CEVO / non-CAO council. Cost data is sensitive.
