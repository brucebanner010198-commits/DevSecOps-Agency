---
name: prompt-cache
description: Anthropic prompt-caching strategy tuned for the agency's static-heavy dispatch prompts (root AGENTS.md + council AGENTS.md + skill bundle). Breakpoint placement, TTL planning after the Feb 2026 60min→5min shift, cache-hit telemetry via `observability`. SRE Council skill, owned by prompt-cache-tuner specialist. Pairs with `budget` + `finops`.
metadata:
  version: 0.3.4
---

# prompt-cache

The agency rereads the same static material on every dispatch: root `AGENTS.md`, council-scoped `AGENTS.md`, skill bundle for the active phase, agent persona, VISION.md KR slice. That is ideal cache territory. After Anthropic's Feb 2026 TTL shift (60 min → 5 min by default, 1 h extended-TTL available paid), naive caching leaks 30-60 % of potential savings. This skill makes the agency's cache hygiene explicit.

## Invariants

- **Breakpoints on the last block that stays identical across requests.** Never mid-sentence. Never inside a dynamic block.
- **Maximum 4 breakpoints per request.** Allocate them: (1) after system prompt, (2) after AGENTS.md bundle, (3) after skill bundle, (4) after prior-turn rollup.
- **Static first, dynamic last.** Assembly order: system → root AGENTS → council AGENTS → skill SKILL.md → agent persona → prior context (cache here) → new input (no cache).
- **TTL choice is explicit.** Default TTL = 5 min. Paid 1-hour TTL only for agents with > 6 dispatches per project (verified via telemetry).
- **Cache hit-rate reported on every span.** `gen_ai.usage.cached_tokens` + `gen_ai.usage.cache_creation_input_tokens` recorded by `observability`. Cache-hit ratio < 50 % triggers tuner review.
- **Workspace-level isolation (Feb 2026+) is respected.** Workspaces are scoped per project. Cross-project cache bleed is a red.

## Assembly order (canonical)

```
[system prompt — frozen across all dispatches]             ← cache breakpoint 1
[root AGENTS.md + scoped councils/<c>/AGENTS.md]           ← cache breakpoint 2
[skills/<a>/SKILL.md + skills/<b>/SKILL.md + …]            ← cache breakpoint 3
[agent persona — agents/<name>.md]                         
[prior-turn rollup — if continuing]                        ← cache breakpoint 4
[new user/CEO input]                                       ← never cached
```

## Process — first cache setup for a project

1. At project kickoff, `prompt-cache-tuner` inspects the dispatch path: which AGENTS.md files, which skills, which personas will recur.
2. Declare the four breakpoint positions. Write `_vision/prompt-cache/<slug>.json` with the breakpoints + TTL choice + expected hit rate.
3. First dispatch: cache-creation path. `gen_ai.usage.cache_creation_input_tokens > 0`, `cached_tokens = 0`. Expected.
4. Second dispatch within TTL: `cached_tokens` high, `cache_creation_input_tokens` zero-or-small. Confirm savings.
5. If the second dispatch shows no cache hit, inspect dispatch assembly for off-by-one breakpoint, variable content before the breakpoint, or TTL expiry.

## Process — runtime telemetry

- Every LLM call span attributes: `gen_ai.usage.cached_tokens`, `gen_ai.usage.cache_creation_input_tokens`, `gen_ai.usage.input_tokens`, `prompt_cache.breakpoints`, `prompt_cache.ttl`.
- Weekly: `finops` aggregates cached-tokens × cache-discount to report saved $.
- Monthly: tuner reviews < 50 % hit-rate projects. Root-cause: dynamic content bleed, TTL too short, council rotation between dispatches, skill bundle thrash.

## Gotchas (2026-specific)

- **5-min default TTL** means a project that dispatches once every ~10 min gets zero cache hits. Solve by either (a) batching dispatches, (b) opting into 1-h TTL for that project, (c) reducing dispatch cadence.
- **Workspace-level isolation** (Claude API + Azure AI Foundry) means cross-workspace cache sharing does NOT happen. Multi-project agencies need per-project breakpoint plans; shared system-prompt gets cached per-workspace, not globally.
- **Amazon Bedrock + Google Vertex** retain org-level isolation. Note this in deployment docs.
- **Cache invalidation on AGENTS.md edit.** Any `agents/*.md` or `councils/*/AGENTS.md` or `skills/*/SKILL.md` edit invalidates every downstream breakpoint. Plan prompt-diff review (see `playbook` skill) + cache-rebuild cost into the edit ADR.

## Savings budget

- Target: ≥ 60 % cached tokens on the ≤ breakpoint-3 prefix for any project with > 3 dispatches.
- If a project hits ≥ 80 % cache rate, its `budget` burn gets a 20 % expected-discount applied at plan time (recorded in `finops` as "prompt-cache savings").
- Savings never justify relaxing breakpoint 4 or breakpoint 3 to include dynamic content. Hit rate falls fast when content varies.

## What never happens

- Breakpoints inside dynamic content ("today's date", retrieved context, user input).
- 1-hour TTL opt-in without telemetry showing > 6 dispatches per TTL window.
- Ignoring a cache-creation tokens spike on what should be a cached dispatch. It means breakpoints drifted.
- Caching secrets. The `system` + `AGENTS.md` + `SKILL.md` assembly contains no creds — vault refs only.
