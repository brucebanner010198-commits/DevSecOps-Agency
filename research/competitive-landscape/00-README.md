# AI-OS / AI-Company Competitive Landscape — Research Pack

**Prepared for:** the Sovereign (Chairman of the Board) · **By:** CEO + research fan-out · **Date:** 2026-06-02
**Status:** research only — *not* a build, *not* yet the design interview. Read this, then we run the one-at-a-time interview (`45`).

---

## Why this pack exists

The Sovereign is reframing this repo (the DevSecOps-Agency: CEO → 16 Chiefs → ~75 specialists, verifier councils, Constitution, gates, receipts) into a product with **two surfaces handed to one user**:

- **Background — a recursive AI *company*.** The user is **Chairman of the Board**; every other role is an AI executive. Each executive runs a team; each member runs a team; recursion continues until the lowest AI employee does **exactly one task**.
- **Foreground — an interactive AI-OS experience** the user actually sees and touches (Warmwind-class).
- **The thesis:** the problem worth solving is a **trustable** AI OS/company. Trust is the wedge, not a feature.

Before any design, the Sovereign wanted the most detailed, web-sourced competitive picture possible, to answer one question: **is anyone already building this full vision, or is it open?** Plus two sub-hypotheses: rivals handle tasks but **not per-agent security**, and their OSes are **not quantum-ready**.

**The short answer (full argument in `43`):** No one occupies the full vision. Every rival owns one or two of the five pillars; none owns the union, and three pillars (human-as-Chairman, personal+sovereign, runtime recursion) are structurally hard for the leaders to reach. Both sub-hypotheses validate (with nuance) in `41`.

## The three meanings of "OS" (read this first — see `40`)

| Category | Meaning | Examples | Our stance |
|---|---|---|---|
| 1. Real device OS | kernel + scheduler + memory + drivers; boots on metal | Aluminium/Google, Brain Natural OS, Windows | sit *above* it; **reuse Linux** |
| 2. AI-agent experience layer | runtime + UI where AI employees work, atop a real OS | Warmwind, Flowith, Rabbit | **this is us** |
| 3. AI infra / kernel-for-agents | substrate scheduling agents/memory/tools | VAST, AIOS, Letta | borrow architecture |

## How to read this pack

| # | Doc | What's in it |
|---|---|---|
| 00 | [README](00-README.md) | this index + methodology |
| 01 | [Overview & Master Matrix](01-overview-and-matrix.md) | the map of both axes + the capability matrix + white-space |
| — | **Axis A — AI-OS experience** | |
| 10 | [Warmwind ⭐](10-warmwind.md) | UX north star — deep dive + SWOT + UX teardown |
| 11 | [Flowith](11-flowith.md) | infinite-canvas agent OS |
| 12 | [Aluminium OS / Google](12-aluminium-os-google.md) | real desktop OS (Cat-1) |
| 13 | [Brain Natural OS](13-brain-natural-os.md) | shipped AI-native phone OS (Cat-1) |
| 14 | [/dev/agents → Meta](14-dev-agents.md) | trust-first agent OS (team acqui-hired by Meta) |
| 15 | [Rabbit · Genspark · Manus](15-rabbit-genspark-manus.md) | three SWOTs |
| — | **Axis B — AI company / workforce** | |
| 20 | [Multi-agent frameworks](20-multi-agent-frameworks.md) | MetaGPT, ChatDev, CrewAI, AutoGen, LangGraph, AgentVerse |
| 21 | [Enterprise AI workforce](21-enterprise-ai-workforce.md) | ServiceNow, Salesforce, Microsoft, Google |
| 22 | [AI-employee startups](22-ai-employee-startups.md) | Relevance, Lindy, Artisan, 11x, Cognosys, Sierra, Cognition |
| — | **Infra / vertical references** | |
| 30 | [Infra & academic](30-infra-and-academic.md) | VAST, AIOS, Agno, Letta — architecture lessons |
| 31 | [Vertical agent-OS](31-vertical-agent-os.md) | Legora, NickAI, Harvey, Imbue |
| — | **Synthesis** | |
| 40 | [OS fundamentals primer](40-os-fundamentals-primer.md) | kernel/scheduling/memory/OSI + build forms (run on existing HW) |
| 41 | [Security & quantum](41-security-and-quantum.md) | the two hypotheses, fact-checked |
| 42 | [Trust as the core problem](42-trust-as-the-core-problem.md) | the 5 Ts; how every rival scores; the gap |
| 43 | [Full-vision match ⭐](43-full-vision-match.md) | **the crux** — is anyone building this? scorecard + verdict |
| 44 | [Positioning & white-space](44-positioning-and-whitespace.md) | pitch, one-liner, differentiation (positioning canvas) |
| 45 | [Open questions — the interview](45-open-questions-interview.md) | one-at-a-time agenda for AFTER this pack |
| 46 | [Executive roster map](46-executive-roster-map.md) | your C-suite directory → repo's 16 Chiefs → rival staffing |

Read alongside the repo's internal self-audit: [`SWOT.md`](../../SWOT.md).

## Methodology & honesty notes

- **Sourcing:** each player doc carries ≥5 dated, distinct sources (most have 10–24). Built by parallel research agents, one per doc, then synthesized.
- **Citation discipline** (per `AGENTS.md:43-44` + `skills/market-intel`): every factual claim is cited or tagged `[synthesised]` / `[hypothesis]` / `[user-knowledge]`; when a fact couldn't be confirmed it says **unknown** rather than guessing. Confidence is **L/M/H**.
- **Fetch caveat:** in this environment `WebFetch` was broadly HTTP-403-blocked, so many primary-source facts were triangulated from dated search-engine extracts of the *same* primary URLs rather than full-page fetches. Where this lowers confidence, the doc says so. Numbers that couldn't be pinned (funding, pricing, benchmarks) are flagged, not invented. **Self-reported benchmarks (e.g. Flowith's Mind2Web score) are labelled as such and not treated as verified.**
- **As-of date:** 2026-06. Fast-moving market — `14` (→Meta) and `15` (Manus ownership) are explicitly in flux.
- **What this is not:** a design or a build. It is the evidence base for the design conversation in `45`.

## Bottom line

The defensible core is **not** the agent capability (commoditizing fast). It is the **org shape** (recursive company + human-as-Chairman) fused with the **trust union** (independent verifier + per-agent least-privilege + replayable receipts + post-quantum crypto), delivered **personally and sovereignly**. That specific combination has no occupant today — and the repo's existing governance spine is a stronger starting point for it than any rival's. Details in `43`; the pitch in `44`; the questions we owe ourselves in `45`.
