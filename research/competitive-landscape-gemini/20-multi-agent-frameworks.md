<!-- Doc 20: Multi-agent frameworks / "AI software company" layer. Six frameworks as sub-sections. Closest prior art to the recursive-company idea. As-of 2026-06. -->

# Multi-Agent Frameworks — the "AI Software Company" Layer

**One-liner:** The cluster of open-source frameworks (MetaGPT, ChatDev, CrewAI, AutoGen/AG2, LangGraph, AgentVerse) that organise LLM agents into role-based "companies" or teams — the closest existing prior art to the recursive AI-company vision.
**Axis:** B = AI company/workforce (background) · Infra = architecture reference
**Category (3-meanings-of-OS):** 3 AI infra/kernel-for-agents (developer frameworks, not end-user OS experiences)
**Stage / availability:** Mostly shipping open-source libraries; MetaGPT has a hosted product (MGX). **As-of:** 2026-06

---

## What it does best · What it lacks · What we take

- **Best:**
  - Validated the "agents-as-an-org-chart" metaphor at scale — role specialisation (PM/architect/engineer/QA), structured comms, and SOP-driven workflows demonstrably beat single-agent baselines [1][6][9].
  - Two-tier hierarchy (supervisor → workers) is now a solved, productised pattern (CrewAI hierarchical process, LangGraph supervisor, AutoGen GroupChat) [3][5][8].
  - LangGraph and AutoGen prove that *nesting* is technically achievable: a sub-team can be wrapped to look like a single agent and embedded in a higher team [5][7][synthesised].
  - Real, shipping trust gestures exist at the edges: AutoGen Docker sandbox + `human_input_mode`, CrewAI Enterprise Hallucination Guardrail + RBAC, MetaGPT executable-feedback self-correction [4][10][12][6].

- **Lacks:**
  - **No genuinely recursive, unbounded org.** Every framework is flat or 2-tier by default; deeper nesting is hand-wired by the developer, not an emergent property an agent can invoke at will (see per-framework recursion verdicts) [synthesised].
  - **No "Chairman" model.** The human is a *user/operator* or an optional `UserProxyAgent` in the loop — never the persistent apex of a standing org that runs autonomously beneath them [synthesised][4].
  - **No interactive AI-OS surface.** These are dev libraries (chat/CLI/notebook); MGX is the only consumer-facing one and it's a chat-to-app builder, not an OS [11][13].
  - **No first-class per-agent least-privilege security, no auditable receipts-as-product, no PQC anywhere** [synthesised].

- **We take:**
  - SOP / structured-comms discipline and the message-pool publish-subscribe pattern → maps to `councils/` orchestration and inter-exec messaging [6].
  - "Wrap a sub-team as one agent" (AutoGen SocietyOfMind / LangGraph subgraph) is the technical primitive our recursion needs — adopt and extend to *agent-initiated* spawning [5][7].
  - Executable-feedback + hallucination-guardrail as the seed of our dedicated verifier layer → `audit/` [6][12].

## Deep dive

This doc treats six frameworks as sub-sections. The throughline: all six are **developer frameworks for assembling agent teams**, and the field has converged on a **2-tier supervisor/worker** pattern. *Recursion* (a sub-agent autonomously spinning up its own sub-team to arbitrary depth) is the dimension where the field is weakest — it is *possible to construct* in the most flexible frameworks but is never the default and is never *agent-initiated*.

### 1. MetaGPT — "First AI Software Company"

Self-described as "The Multi-Agent Framework: First AI Software Company, Towards Natural Language Programming" [1]. Takes a one-line requirement and emits PRD → design → tasks → code via a fixed role pipeline: Product Manager, Architect, Project Manager, Engineer, QA Engineer [1][14]. Core slogan: `Code = SOP(Team)` — it encodes human Standard Operating Procedures into the agent team [1][6]. Two technically notable mechanisms: (a) a **shared message pool with publish-subscribe** structured communication (agents publish structured artifacts to a pool; others subscribe by role rather than calling each other directly) [9]; and (b) **executable feedback** — the Engineer agent iteratively runs and debugs its own code at runtime, giving a measured +4.2% Pass@1 on HumanEval and +5.4% on MBPP in ablations [9]. Paper published at ICLR 2024 [9]. GitHub repo (now `FoundationAgents/MetaGPT`) ~68.5k stars, last tagged release v0.8.1 (Apr 2024) [1]. In Feb 2025 the team launched **MGX (MetaGPT X)** — a hosted "world's first AI agent dev team" with named agents Mike (leader), Emma (PM), Bob (architect), Alex (engineer), plus a data analyst; #1 Product of the Week on ProductHunt Mar 2025 [11][13]. **Recursion:** fixed role pipeline; agents do not spawn sub-teams. **Chairman:** no — human is the requirement-giver. **Trust:** executable-feedback self-correction only; no security/verifier layer described [1][6].

### 2. ChatDev — virtual software company via dialogue

A "virtual, chat-powered software development company" that mirrors the **waterfall model**: designing → coding → testing → documenting [2][15]. Roles include CEO, CPO, CTO, programmer, reviewer, tester, art designer, assigned *per phase* (e.g. CEO/CPO/CTO in design; CTO/programmer/designer in coding; programmer/reviewer/tester in testing) [15]. The key mechanism is the **chat chain** — a directed sequence that decomposes each phase into atomic subtasks, each handled by a **two-agent dyad** (an *instructor* agent that drives and an *assistant* agent that executes), plus a memory stream of cumulative dialogue [2][15]. To curb hallucination it uses **communicative dehallucination**: an agent requests more detail before answering rather than guessing [2]. arXiv 2307.07924 (first submitted Jul 2023; multiple revisions through v5) [2]. **Recursion:** none — the chat chain is a *linear, fixed* pipeline of dyads, not a tree; no agent spawns a sub-company. The CEO/CTO titles are role-play labels, not a live management hierarchy with delegation depth [2][15][synthesised]. **Chairman:** no. **Trust:** communicative dehallucination is an anti-hallucination *gesture*, no security layer [2].

### 3. CrewAI — role-based crews with a manager

A standalone (explicitly *not* built on LangChain) Python framework for "role-playing autonomous agents" [16]. Offers **Crews** (autonomous role-based teams) and **Flows** (event-driven deterministic workflows) [3]. Its **hierarchical process** is the relevant pattern: a manager agent (auto-instantiated from `manager_llm`, or a custom `manager_agent`) receives the goal and delegates tasks to worker agents, validates outcomes, and can request revisions [3]. This is a **2-tier** structure by default. Trust posture is the most enterprise-mature of the open-source set: **Task Guardrails** (function- or LLM-as-judge validators that gate a task's output before completion), an enterprise **Hallucination Guardrail** that grounds output against reference context, and **RBAC** over private vs public tool repositories [12][10]. ~52k GitHub stars (May 2026); $18M raised incl. a Series A led by Insight Partners (round disclosed 2024) [16]. **Recursion:** nominally a worker agent *can* itself wrap another crew (a crew can be invoked as a tool), so multi-level is constructible by the developer, but the native hierarchical process is single-manager/2-tier and manager delegation is documented as unreliable at depth [3][synthesised]. **Chairman:** the manager is an *agent*, not the human; the human configures, not presides. **Trust:** strongest guardrail story here.

### 4. AutoGen / AG2 — conversational multi-agent, nestable

Microsoft's AutoGen (the community fork **AG2** continues the conversational lineage) is a conversation-centric framework. v0.4 (Jan 2025) was a ground-up redesign onto an **actor model** with asynchronous event-driven messaging and a layered Core/AgentChat/Extensions stack [17]. The org primitives: **GroupChat** (a set of agents with a speaker-selection policy), **nested chats**, and most importantly the **SocietyOfMindAgent** — a *group chat that runs as an internal monologue but presents to the outside world as a single agent*, explicitly described as "a clean way of producing a **hierarchy of agents**, hiding complexity as inner monologues" [5]. This is the closest primitive in the field to true recursion: because the wrapped team looks like one agent, you can place it inside another team, and recurse. Human-in-the-loop is first-class via **`UserProxyAgent`** with `human_input_mode` (ALWAYS/NEVER/TERMINATE) [4]. Security: code execution defaults to a **Docker sandbox** so generated code only touches explicitly granted resources [4]. The Magentic-One generalist team is a sibling application [17]. **Recursion:** *deepest technical support* — SocietyOfMind + nested chats make arbitrary nesting constructible, though still developer-wired (an agent does not autonomously decide "I'll hire a sub-team") [5][synthesised]. **Chairman:** the human can sit in the loop as `UserProxyAgent`, the nearest thing to a Chairman, but it's a participant, not a standing apex over an autonomous org [4]. **Trust:** Docker sandbox + human gating; no dedicated verifier.

### 5. LangGraph — graph orchestration with nestable subgraphs

LangChain's low-level orchestration framework (state machine / directed graph over nodes). The **langgraph-supervisor** library (released Mar 2025) productises the supervisor pattern, and the official **Hierarchical Agent Teams** tutorial explicitly shows building **multi-level** systems: a top-level supervisor managing **mid-level supervisors**, each managing their own worker teams, composed via **subgraphs** [5(LG)][8]. Because any compiled graph can be embedded as a node/subgraph in a parent graph, LangGraph offers the **cleanest recursive composition** of the six — supervisor-of-supervisors-of-workers is a documented, supported topology, not a hack [8][synthesised]. Maintainers now also recommend the supervisor-as-tools approach for context control [5(LG)]. Human-in-the-loop is supported via interrupts/checkpoints (LangGraph's persistence) [synthesised]. **Recursion:** *highest among general frameworks* — arbitrary depth via nested subgraphs — but, as everywhere, the topology is **author-time fixed**, not **agent-initiated at runtime** [8][synthesised]. **Chairman:** no persistent human-apex model; human appears as interrupt handler. **Trust:** no built-in verifier/security beyond what the developer adds; relies on LangSmith for tracing/audit [synthesised].

### 6. AgentVerse — dynamic expert recruitment

OpenBMB's research framework (arXiv 2308.10848, Aug 2023; ICLR 2024) providing two modes: **task-solving** and **simulation** [18]. Its task-solving pipeline is a four-stage loop: (1) **Expert Recruitment** — dynamically determine/adjust the agent group's composition for the current problem; (2) **Collaborative Decision-Making**; (3) **Action Execution**; (4) **Evaluation** — compare current vs desired state and feed back to recruitment [18]. The recruitment + evaluation loop is conceptually the closest to "an organiser hires the team it needs," and the framework is notable for studying **emergent social behaviours** among agents [18]. ~5k GitHub stars; last release v0.1.8.1 (Oct 2023) — effectively dormant [18(GH)]. **Recursion:** the recruiter dynamically *composes a flat group*; recruited experts are not documented to recursively recruit their own sub-teams, so it is dynamic-flat rather than recursive [18][synthesised]. **Chairman:** no (the recruiter is an agent). **Trust:** the Evaluation stage is a self-assessment gesture, not a dedicated verifier; no security layer [18].

## SWOT (with so-what-for-us)

- **Strengths:** Mature, battle-tested role/SOP/supervisor patterns and (in CrewAI/AutoGen) shipping trust gestures — so-what: we don't have to reinvent orchestration; we stand on these primitives and differentiate above them.
- **Weaknesses:** All are *developer frameworks* with flat/2-tier defaults, no Chairman model, no OS experience, no PQC, no receipts-as-product — so-what: the recursive-company + Chairman + trust-as-wedge combination is genuinely open whitespace.
- **Opportunities:** "Wrap-a-team-as-an-agent" (SocietyOfMind / subgraph) is exactly the recursion primitive we need; nobody has made it *agent-initiated* or paired it with per-agent least-privilege + auditable receipts — so-what: that pairing is our defensible position.
- **Threats:** Well-funded incumbents (CrewAI/Insight Partners; MetaGPT/MGX with major China financing; Microsoft behind AutoGen) could move "up" toward recursion + trust faster than we expect — so-what: move fast on the trust + Chairman differentiators they're structurally unlikely to prioritise (they're enterprise-dev-tool, not personal-AI-OS).

## Facts table

Each cell cited `[n]` or `unknown`. Confidence L/M/H. Comparison sub-table across the six frameworks.

### Recursion / org-depth verdict (headline dimension)

| Framework | Recursion verdict | Conf | Source |
|---|---|---|---|
| MetaGPT | **Flat fixed pipeline** — fixed PM/architect/PM/engineer/QA roles; no sub-team spawning | H | [1][9] |
| ChatDev | **Flat/linear chat chain of 2-agent dyads** — waterfall phases, no recursion; CEO/CTO are role-play labels | H | [2][15] |
| CrewAI | **2-tier** (manager→workers) default; deeper nesting *constructible* (crew-as-tool) but not native/reliable | M | [3] |
| AutoGen / AG2 | **2-tier default; nesting via SocietyOfMind / nested chats** — closest primitive to true recursion, developer-wired | M | [5] |
| LangGraph | **Arbitrary depth via nested subgraphs** (supervisor-of-supervisors) — cleanest recursive composition, author-time fixed | M-H | [8] |
| AgentVerse | **Dynamic-flat** — recruiter composes a flat expert group; no recursive sub-recruitment documented | M | [18] |
| **Field verdict** | **No framework offers runtime, agent-initiated, unbounded recursion.** Best case = author-wired nested subgraphs (LangGraph) or team-as-agent (AutoGen) | M-H | [synthesised] |

### Template dimensions × framework

| Dimension | MetaGPT | ChatDev | CrewAI | AutoGen/AG2 | LangGraph | AgentVerse |
|---|---|---|---|---|---|---|
| Recursion / org depth | Flat pipeline [1][9] | Flat chat chain [2][15] | 2-tier [3] | 2-tier + nestable [5] | Nested subgraphs (deep) [8] | Dynamic-flat [18] |
| User-as-Chairman fit | No — requirement-giver [1] | No [2] | No — manager is an agent [3] | Partial — `UserProxyAgent` in loop [4] | No — interrupt handler [synth] | No — recruiter is agent [18] |
| Interactive-OS surface | CLI/lib; MGX = chat-to-app [1][11] | CLI/chat [2] | lib/SDK + AMP UI [3] | lib + Studio low-code [17] | lib + LangGraph Studio [synth] | lib/research demo [18] |
| Per-agent security | none [synth] | none [synth] | RBAC on tools (Enterprise) [10] | Docker sandbox (perimeter) [4] | none built-in [synth] | none [synth] |
| Verifier / anti-hallucination | Executable-feedback self-correct [9] | Communicative dehallucination [2] | Hallucination Guardrail + Task Guardrails [12][10] | none dedicated (human gating) [4] | none built-in [synth] | Evaluation stage (self-assess) [18] |
| Receipts / reversibility | logs [synth] | memory stream (logs) [15] | execution logs / traces [synth] | message logs [synth] | LangSmith tracing [synth] | logs [synth] |
| Post-quantum (PQC) | none [synth] | none [synth] | none [synth] | none [synth] | none [synth] | none [synth] |
| Local / cloud / hybrid | both (lib local; MGX cloud) [1][11] | local lib [2] | both (OSS local; Enterprise cloud) [3] | both [17] | both [synth] | local lib [18] |
| Hardware | cloud-only models [synth] | cloud-only [synth] | cloud-only [synth] | cloud-only [synth] | cloud-only [synth] | cloud-only [synth] |
| Availability | OSS + MGX hosted [1][11] | OSS (arXiv 2023) [2] | OSS + Enterprise [3][16] | OSS (MS/AG2) [17] | OSS (LangChain) [8] | OSS (dormant) [18] |
| Pricing | OSS free; MGX paid (unknown tiers) [11] | OSS free [2] | OSS free; Enterprise paid (unknown) [16] | OSS free [17] | OSS free; Platform paid [synth] | OSS free [18] |
| Funding / stage | MGX raised large round (Ant Group et al.) [11] | academic/OSS [2] | ~$18M, Series A Insight [16] | Microsoft-backed; AG2 community [17] | LangChain-backed [synth] | academic (OpenBMB) [18] |
| GitHub stars (approx) | ~68.5k [1] | unknown (large) | ~52k (May 2026) [16] | unknown (large) | unknown (large) | ~5k [18] |
| UX notes | one-line→repo; SOP artifacts [1] | run a "company", get an app [2] | role/crew config in code [3] | conversational/notebook [4] | graph/state-machine code [8] | research demos [18] |

## Sources

1. MetaGPT GitHub (FoundationAgents/MetaGPT) — https://github.com/FoundationAgents/MetaGPT — accessed 2026-06 (tagline, roles, SOP, ~68.5k stars, v0.8.1 Apr 2024).
2. ChatDev: Communicative Agents for Software Development — arXiv:2307.07924 (Jul 2023, rev v5) — https://arxiv.org/abs/2307.07924 — accessed 2026-06 (chat chain, dyads, dehallucination).
3. CrewAI Hierarchical Process docs — https://docs.crewai.com/en/learn/hierarchical-process — accessed 2026-06 (manager/worker, manager_llm vs manager_agent, Crews vs Flows).
4. AutoGen UserProxyAgent + Docker code execution — https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/user_proxy_agent/ and .../blog/2024/01/23/Code-execution-in-docker/ — accessed 2026-06 (human_input_mode, Docker sandbox).
5. AG2 SocietyOfMindAgent / GroupChat docs — https://docs.ag2.ai/latest/docs/use-cases/notebooks/notebooks/agentchat_society_of_mind/ and .../blog/2025/04/28/0.9-Release-Announcement/ — accessed 2026-06 ("hierarchy of agents, hiding complexity as inner monologues").
6. What is MetaGPT? — IBM Think — https://www.ibm.com/think/topics/metagpt — accessed 2026-06 (SOPs, structured comms, executable feedback framing).
7. LangGraph Hierarchical Agent Teams tutorial — https://langchain-ai.github.io/langgraph/tutorials/multi_agent/hierarchical_agent_teams/ — accessed 2026-06 (top + mid-level supervisors via subgraphs).
8. LangGraph Supervisor announcement (Mar 2025) — https://changelog.langchain.com/announcements/langgraph-supervisor-a-library-for-hierarchical-multi-agent-systems — accessed 2026-06 (multi-level supervisor of supervisors).
9. MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework — ICLR 2024 — https://arxiv.org/pdf/2308.00352 — accessed 2026-06 (shared message pool publish-subscribe, executable feedback +4.2%/+5.4%).
10. Hallucination Guardrail / Task Guardrails — CrewAI Enterprise docs — https://docs.crewai.com/en/enterprise/features/hallucination-guardrail — accessed 2026-06 (guardrails, RBAC on tools).
11. MGX (MetaGPT X) launch — MetaGPT on X (Feb 19 2025) + Product Hunt — https://x.com/MetaGPT_/status/1892199535130329356 and https://www.producthunt.com/products/metagpt-x — accessed 2026-06 (Mike/Emma/Bob/Alex; #1 Product of Week Mar 2025; financing incl. Ant Group).
12. Introduction to Task Guardrails in CrewAI — Analytics Vidhya (Nov 2025) — https://www.analyticsvidhya.com/blog/2025/11/introduction-to-task-guardrails-in-crewai/ — accessed 2026-06 (guardrails gate task output).
13. MetaGPT MGX review 2025 — Sider — https://sider.ai/blog/ai-tools/metagpt-review-2025-is-mgx-the-no-code-ai-agent-builder-you-ve-been-waiting-for — accessed 2026-06 (no-code chat-to-app builder).
14. MetaGPT Multi-Agent Framework Explained — AI Innovation Hub — https://aiinovationhub.com/metagpt-multi-agent-framework-explained/ — accessed 2026-06 (default roles PM/architect/PM/engineer/QA).
15. ChatDev framework overview — EmergentMind topic + AI-SCHOLAR — https://www.emergentmind.com/topics/chatdev-framework and https://ai-scholar.tech/en/articles/agent-simulation/chatdev — accessed 2026-06 (waterfall phases, per-phase role assignment, memory stream).
16. CrewAI GitHub + funding — https://github.com/crewAIInc/crewAI and Insight Partners scaleup story — https://www.insightpartners.com/ideas/crewai-scaleup-ai-story/ — accessed 2026-06 (standalone, ~52k stars, ~$18M Series A).
17. AutoGen v0.4 (Jan 2025) — Microsoft Research — https://www.microsoft.com/en-us/research/articles/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/ — accessed 2026-06 (actor model, layered Core/AgentChat/Extensions, Magentic-One).
18. AgentVerse — arXiv:2308.10848 (Aug 2023, ICLR 2024) + GitHub OpenBMB/AgentVerse — https://arxiv.org/abs/2308.10848 and https://github.com/OpenBMB/AgentVerse — accessed 2026-06 (four-stage pipeline, expert recruitment, ~5k stars, v0.1.8.1 Oct 2023).
