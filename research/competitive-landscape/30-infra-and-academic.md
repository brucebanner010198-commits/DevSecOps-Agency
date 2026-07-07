<!-- Doc 30: AI-infra / kernel-for-agents layer. These are ARCHITECTURE REFERENCES (Infra axis), NOT personal-OS rivals. Headers follow _TEMPLATE.md so docs 01/43 can parse. -->

# AI-Infra / Kernel-for-Agents Layer (VAST · AIOS · Agno · Letta)

**One-liner:** The infrastructure/kernel substrates that run LLM agents at scale — scheduling, memory, storage, tool, and access-control services for agents — studied here for the patterns we should borrow into our "kernel-for-employees" layer, not as competitors. [synthesised]
**Axis:** Infra = architecture reference (none of these is a foreground AI-OS experience or a recursive AI-company for an individual). [synthesised]
**Category (3-meanings-of-OS):** 3 — AI infra / kernel-for-agents. [synthesised]
**Stage / availability:** VAST AI OS shipping (announced 2025-05-21, PolicyEngine/TuningEngine slated end-2026) [1][6]; AIOS research+OSS (COLM 2025) [4][7]; Agno OSS + commercial runtime, shipping [9][10]; Letta OSS + cloud, shipping (v0.16.8, 2026-05-14) [11]. · **As-of:** 2026-06

> **Framing for this pack:** All four are *infra*, not *rivals*. None of them gives an individual user a Chairman-over-a-recursive-org experience, and none is a personal (not enterprise) trust-first AI-OS. They are the plumbing layer beneath what we are building. We mine them for **scheduling, memory, and access-control** patterns. [synthesised]

---

## What it does best · What it lacks · What we take

- **Best (across the group):**
  - VAST: a single physical substrate (DASE) unifying storage + database + event + messaging + agent runtime, with an explicit closed agentic loop (observe → reason → act → evaluate → improve) and pre-execution policy enforcement + tamper-proof logs as a planned trust layer. [1][6][2]
  - AIOS: the cleanest *OS-theoretic* decomposition — kernel/SDK split, LLM-as-syscall, agent scheduler (FIFO/RR), context snapshot/restore, privilege-group access manager — with a measured 2.1× throughput win. [4][7]
  - Agno: production-grade runtime ergonomics — stateless horizontally-scalable runtime, per-session isolation, JWT-based RBAC, multi-tenancy, OpenTelemetry tracing + audit logs, cron scheduling, human-approval gates, "run in your own cloud." [9][10]
  - Letta: memory-as-OS done concretely — core/recall/archival tiers, editable shared memory blocks, asynchronous sleep-time memory agents, MCP-native tools, sandboxed server-side tool execution. [11][12][13][14]
- **Lacks (vs. our full vision):**
  - No recursive AI *company* / Chairman-of-the-Board model — these are flat agent runtimes or 2-tier (agent ↔ sub-agent) at most. [synthesised]
  - No interactive personal AI-OS *foreground*; surfaces are APIs, control-plane UIs, or chat/CLI, all enterprise/developer-facing, not a sovereign personal OS. [9][11][synthesised]
  - Trust is perimeter/RBAC/policy-engine flavored; no per-employee least-privilege *recursive* model, no verifier/anti-hallucination council, no post-quantum posture surfaced. [unknown / synthesised]
- **We take:**
  - AIOS kernel/SDK split + LLM-as-syscall + agent scheduler with context snapshot/restore → our `kernel-for-employees` scheduling & interruptibility design. [4][7]
  - Letta's tiered + *shared, editable* memory blocks and async sleep-time memory maintainer → durable memory for leaf employees + org-shared context. [12][13][14]
  - VAST PolicyEngine's *pre-execution* fine-grained policy enforcement + tamper-proof logs → our trust wedge (receipts/reversibility), mapping to `councils/audit/`. [6][synthesised]

## Deep dive

### VAST Data — "Operating System for the Thinking Machine"

VAST Data announced the **VAST AI Operating System** on **2025-05-21**, framed as the first platform built to manage the complete AI lifecycle on one foundation for storage, database, and compute runtime. [1][6] It sits on VAST's **DASE (Disaggregated Shared-Everything)** architecture — described as the first true parallel distributed-system architecture, letting workloads parallelize, federate clusters into one data cloud, and feed AI from one storage tier; VAST states DASE clusters support over 1 million GPUs in production. [1] The AI OS is described as comprising "every aspect of a distributed system to run AI at global scale": a **kernel** to run platform services (private→public cloud), a **runtime** to deploy AI agents, **eventing infrastructure** for real-time event processing, **messaging infrastructure**, and a **distributed file + database storage system** for real-time capture and analytics. [1]

Named engines: **VAST InsightEngine** extracts context from unstructured data via AI embedding tools (prepares data for AI consumption). [1] **VAST AgentEngine** is the serverless/auto-scaling agentic runtime — a low-code environment to build workflows, select reasoning models, define agent tools, and operationalize reasoning; it includes an "AI agent tool server" letting agents invoke data, metadata, functions, web search, or *other agents* as **MCP-compatible tools**. [1][6] The platform introduces "a closed operational loop that **observes, reasons, acts, evaluates, and improves**." [6][user-knowledge confirms framing]

Trust/security: the planned **VAST PolicyEngine** does **inline policy enforcement** — regulating agents' access to shared resources by explicit, fine-grained permissions and context, **before actions execute**, complemented by **tamper-proof logs**; positioned with zero-trust, multi-tenant isolation, policy-driven access. The companion **TuningEngine** manages model tuning to power automatic learning loops. [6] PolicyEngine + TuningEngine are slated for release by end-2026; the core AI OS is available now. [6] Hardware/deployment: cloud + on-prem hybrid on VAST's storage substrate. [1] Pricing: unknown (enterprise, not published). [unknown]

### AIOS (Rutgers, agiresearch/AIOS) — the LLM-Agent OS kernel

Academic paper **"AIOS: LLM Agent Operating System,"** arXiv **2403.16971**, released **2024-03-25**, authors incl. Kai Mei, Zelong Li, Shuyuan Xu, Ruosong Ye, Yingqiang Ge, Yongfeng Zhang (Rutgers University); **accepted to COLM 2025** (per repo news, 2025-07-08). [4][7] A precursor perspective paper, "LLM as OS, Agents as Apps," is arXiv 2312.03815 (2023-12-06). [7]

Core idea: isolate resources and LLM-specific services from agent applications into an **AIOS kernel** providing scheduling, context management, memory management, storage management, and access control for runtime agents. [4] The system splits into **AIOS kernel** (abstraction layer over the OS kernel, managing LLM/memory/storage/tool) and the **AIOS SDK = Cerebrum** (agiresearch/Cerebrum) for building/running agents against the kernel. [7] Agent queries are decomposed into categorized **system calls (syscalls)** — LLM processing, memory access, storage operations, tool usage — mediated by the kernel and run on categorized threads for parallel execution + central scheduling. [7] Modules:
- **Agent Scheduler** — dispatch/prioritization via classic algorithms **FIFO** and **Round Robin (RR)**. [7]
- **Context Manager** — context-interrupt mechanism with **snapshot and restoration**, pausing/resuming LLM generation to boost throughput. [7]
- **Memory Manager** (short-term, per agent during lifecycle) vs **Storage Manager** (long-term, persistent). [4][7]
- **Tool Manager** — tool calls; in the computer-use variant (LiteCUA) redesigned with a **VM Controller + MCP Server** for a sandboxed environment. [7]
- **Access Manager** — privilege-based access control; each agent assigned to a **privilege group**, enforced via a hashmap of agent-ID → privilege group, regulating cross-agent read/write. [7]
- **LLM Core(s)** — each LLM deployment encapsulated as a "core," akin to a CPU core. [7]

Measured result: **up to 2.1× faster execution / throughput** for agents across frameworks (e.g., Reflexion on Llama-3.1-8B), attributed to kernel scheduling avoiding wasted trial-and-error. [4][7] Deployment modes: local-kernel (Mode 1) and remote-kernel (Mode 2) shipping; remote-dev (Mode 2.5) ongoing; supports onboarding ReAct/Reflexion/AutoGen/MetaGPT/Open Interpreter agents. [7] License: open source (repo). Pricing: free/OSS, Rutgers-sponsored. [7]

### Agno — AgentOS (agno-agi/agno)

Agno is an open-source (Python) SDK for building **agent platforms**, with three layers: a **Python SDK** (agents, teams, workflows), a **runtime = AgentOS** serving the system as a production API, and a **control-plane UI** for testing/monitoring/managing in production. [9][10] Stated philosophy: "own your agent stack" — keep control of data, context, tools, permissions, memory, human-review loops; "run your platform in your cloud." [10] Features (from repo, as of pushed state 2026): Production API with 50+ endpoints (SSE + websockets); **Storage** (sessions, memory, knowledge, traces in your own DB); 100+ tool integrations; **Context Providers** (live data from Slack/Drive/wikis/MCP/custom); **Human approval** (pause runs, block admin-approval tools); **Observability** via OpenTelemetry tracing + run history + audit logs; **Security** = JWT-based RBAC + multi-user/multi-tenant isolation; interfaces over Slack/Telegram/WhatsApp/Discord/AG-UI/**A2A**; **cron-based scheduling** + background jobs with no external infra; deploy on any container host. [10] Architecture described as stateless, horizontally scalable, per-session isolation. [9] v2.5.13 (Mar 2026) added ReliabilityEval + enhanced AgentOS session-management APIs. [9] Org model: 2-tier (agents + teams + workflows), not recursive. [9][10] Pricing: OSS core; commercial offering details unknown. [unknown]

### Letta / MemGPT — memory-as-OS, MCP-native

Letta (the productized successor to the **MemGPT** research) is "the platform for building **stateful agents**: AI with advanced memory that can learn and self-improve over time," Apache-2.0, ~23k GitHub stars, latest release **v0.16.8 (2026-05-14)**, 177 releases; Python SDK + TypeScript SDK + Letta Code CLI + cloud (app.letta.com) + Docker self-host. [11] It explicitly frames an **LLM-as-Operating-System** paradigm where the model manages its own memory/context/reasoning loops like an OS manages RAM/disk. [synthesised from 11/search]

Memory model (OS-inspired three tiers): **Core memory** (always in-context, like RAM), **Recall memory** (full searchable conversation history outside context), **Archival memory** (external searchable vector store, like disk/cold storage); agents move data between tiers via tool calls for an "illusion of unlimited memory." [12][13] **Memory blocks** are editable strings attachable/detachable from agents (in-context = pinned to system prompt) and can be **shared across multiple agents** ("shared blocks"). [13] **Sleep-time agents** manage memory **asynchronously** (triggered every N steps, default 5; `sleeptime_agent_frequency` configurable), separating memory maintenance from the response path — an improvement over MemGPT's single bundled agent. [14] Tools: **server-side tools** run sandboxed on the server; **MCP tools** carry only the schema (executed externally); client-side tools schema-only. [12][synthesised] Multi-agent: agents can call sub-agents and pass state (2-tier coordination). [synthesised from search] Access control: per-agent, block-level sharing; enterprise per-employee least-privilege model unknown. [unknown]

## SWOT (with so-what-for-us)

- **Strengths:** These substrates have already solved the hard kernel problems (scheduling, interruptible generation, tiered memory, policy-before-action). So-what: we can adopt proven primitives rather than reinvent the kernel — focus our novelty budget on the recursive-company + trust foreground. [synthesised]
- **Weaknesses:** All are flat/2-tier and enterprise/developer-facing; trust is RBAC/policy-engine, not recursive least-privilege; no verifier council, no PQC surfaced. So-what: our recursive-org + trust wedge is genuinely open whitespace above this layer. [synthesised]
- **Opportunities:** VAST's pre-execution PolicyEngine + tamper-proof logs and AIOS's privilege groups are exactly the receipts/reversibility primitives our `councils/audit/` needs. So-what: borrow the enforcement-before-action + immutable-log pattern wholesale. [6][7]
- **Threats:** If VAST/Agno extend upward into orchestration UX, or Letta's "self-improving stateful agents" grow org structure, the gap to a personal recursive AI-company could narrow. So-what: keep the Chairman foreground + personal-trust posture as the moat, not the kernel. [hypothesis]

## Facts table

Each cell cited `[n]` or `unknown`. Confidence L/M/H. (Combined; one row-block per project.)

| Dimension | VAST AI OS | AIOS (Rutgers) | Agno AgentOS | Letta / MemGPT |
|---|---|---|---|---|
| Recursion / org depth | flat runtime; agents call agents as MCP tools [1] (M) | flat; kernel mediates agents [4] (H) | 2-tier: agents + teams + workflows [9][10] (H) | 2-tier: agents + sub-agents [search] (M) |
| User-as-Chairman fit | no — enterprise infra [synthesised] (H) | no — research kernel [synthesised] (H) | no — dev platform [synthesised] (H) | no — dev/agent platform [synthesised] (H) |
| Interactive-OS surface | none for end-user; runtime + engines/API [1] (M) | Web UI + Terminal UI for agents [7] (M) | control-plane UI + chat interfaces (Slack/etc) [10] (H) | CLI (Letta Code) + cloud app + ADE UI [11] (H) |
| Per-agent security | planned PolicyEngine: pre-exec fine-grained policy, zero-trust, multi-tenant [6] (M) | Access Manager: per-agent privilege groups (hashmap) [7] (H) | JWT RBAC + multi-tenant per-session isolation [10] (H) | per-agent + block-level sharing; least-priv model unknown [13] (M) |
| Verifier / anti-hallucination | none stated (TuningEngine = tuning, not verify) [6] (L) | none stated [4] (M) | ReliabilityEval (eval, not runtime verifier) [9] (L) | none stated [11] (L) |
| Receipts / reversibility | tamper-proof logs (planned, w/ PolicyEngine) [6] (M) | logs implicit; not emphasized [unknown] (L) | audit logs + run history + OTel tracing [10] (H) | run/message history; reversibility unknown [11] (L) |
| Post-quantum (PQC) | unknown (M) | unknown (H) | unknown (H) | unknown (H) |
| Local / cloud / hybrid | hybrid (private→public cloud + on-prem) [1] (M) | local + remote kernel modes [7] (H) | run-in-your-cloud, any container host [10] (H) | cloud (app.letta.com) + Docker self-host [11] (H) |
| Hardware | own storage substrate (DASE), 1M+ GPUs [1] (M) | commodity / cloud [7] (H) | cloud-only (containers) [10] (H) | cloud / self-host [11] (H) |
| Availability | core shipping 2025-05-21; Policy/Tuning end-2026 [1][6] (H) | OSS; COLM 2025 [4][7] (H) | OSS + runtime, shipping; v2.5.13 Mar 2026 [9][10] (M) | OSS + cloud; v0.16.8 2026-05-14 [11] (H) |
| Pricing | enterprise, unpublished [unknown] (M) | free / OSS / Rutgers-sponsored [7] (H) | OSS core; commercial unknown [unknown] (M) | OSS (Apache-2.0) + paid cloud [11] (M) |
| Funding / stage | VAST Data (well-funded storage co.); shipping [1] (M) | Rutgers academic + community [7] (H) | venture-backed startup; OSS+commercial [9][10] (L) | venture-backed (ex-MemGPT/UC Berkeley) [11] (M) |
| UX notes | low-code AgentEngine; engine-centric, API-first [1] (M) | OS-theoretic; Web+Terminal UI; dev-facing [7] (H) | "beautiful UI" control plane; coding-agent friendly [10] (M) | memory-block ADE; CLI; stateful-agent focus [11] (H) |

## Architecture lessons we take

1. **Kernel/SDK split with LLM-as-syscall + central scheduler + context snapshot/restore (from AIOS).** Decompose every employee action into categorized syscalls (LLM / memory / storage / tool), mediate them in a kernel, schedule with FIFO/RR, and make LLM generation *interruptible* via snapshot/restore. This is the cleanest blueprint for our `kernel-for-employees` scheduling layer and the only one with a measured win (2.1×). [4][7] [synthesised]
2. **Tiered + shared, editable memory with an async maintainer (from Letta).** Core/recall/archival tiers give bounded context with unbounded recall; *shared, editable memory blocks* are the right primitive for org-level shared context (a team's brief pinned across its leaf employees); the *sleep-time agent* pattern keeps memory maintenance off the response path. Maps to durable per-employee + per-team memory. [12][13][14] [synthesised]
3. **Policy-enforced-before-action + tamper-proof logs as the trust substrate (from VAST PolicyEngine; reinforced by AIOS privilege groups + Agno RBAC/audit).** Enforce fine-grained per-employee permissions *before* an action executes, and emit immutable receipts — exactly our trust wedge and the receipts/reversibility our `councils/audit/` needs. We extend it from flat policy to *recursive* least-privilege down the org tree (a lesson the infra layer does not yet implement). [6][7][10] [synthesised]

> **Explicit non-rival note:** Re-confirming for docs 01/43 — VAST, AIOS, Agno, and Letta are scored on the **Infra** axis only. They are architecture references for the kernel layer; none competes for the personal-AI-OS foreground or the recursive AI-company-for-an-individual that is our product. [synthesised]

## Sources

1. VAST Data — "VAST Data Unveils the Operating System for the Thinking Machine" (press release / GlobeNewswire) — https://www.globenewswire.com/news-release/2025/05/21/3085795/0/en/VAST-Data-Unveils-the-Operating-System-for-the-Thinking-Machine.html — dated 2025-05-21, accessed 2026-06.
2. VAST Data — "Unveils the Operating System for the Thinking Machine" (vendor press page) — https://www.vastdata.com/press-releases/vast-data-unveils-ai-os-for-thinking-machines — 2025-05, accessed 2026-06.
3. Blocks & Files — "VAST Data launches AI operating system" — https://blocksandfiles.com/2025/05/21/vast-ai-operating-system/ — 2025-05-21, accessed 2026-06.
4. Mei, Li, Xu, Ye, Ge, Zhang (Rutgers) — "AIOS: LLM Agent Operating System," arXiv 2403.16971 — https://arxiv.org/abs/2403.16971 — released 2024-03-25 (COLM 2025), accessed 2026-06.
5. arXiv HTML v5 of 2403.16971 (kernel internals: scheduler/context/access/syscall, 2.1×) — https://arxiv.org/html/2403.16971v5 — accessed 2026-06.
6. StorageReview — "VAST Data Unveils Agentic AI OS and Advances Its Thinking Machine Vision" (observe→reason→act→evaluate→improve loop; PolicyEngine pre-exec enforcement + tamper-proof logs; TuningEngine; end-2026) — https://www.storagereview.com/news/vast-data-unveils-agentic-ai-os-and-advances-its-thinking-machine-vision — 2025-05, accessed 2026-06.
7. agiresearch/AIOS — GitHub README (kernel/SDK split, Cerebrum, modules, deployment modes, COLM 2025 acceptance 2025-07-08, LiteCUA VM+MCP sandbox) — https://github.com/agiresearch/AIOS — accessed 2026-06.
8. agno-agi/agno — GitHub README (SDK/runtime/control-plane, 50+ endpoints, JWT RBAC, OTel, scheduling, human approval, A2A, run-in-your-cloud) — https://github.com/agno-agi/agno — accessed 2026-06.
9. Agno — AgentOS product page + decisioncrafters coverage (stateless runtime, per-session isolation, v2.5.13 Mar 2026, ReliabilityEval) — https://www.agno.com/agentos — 2026, accessed 2026-06.
10. agno README (features list, as cited inline as [10]) — https://github.com/agno-agi/agno — accessed 2026-06.
11. letta-ai/letta — GitHub README (stateful agents, Apache-2.0, v0.16.8 2026-05-14, SDKs/CLI/cloud/Docker) — https://github.com/letta-ai/letta — accessed 2026-06.
12. Letta Docs — "Introduction to Stateful Agents" / memory tiers + tool sandbox — https://docs.letta.com/guides/agents/memory/ — 2026, accessed 2026-06.
13. Letta Docs — "Memory blocks (core memory)" (editable, attach/detach, shared blocks) — https://docs.letta.com/guides/agents/memory-blocks/ — 2026, accessed 2026-06.
14. Letta Docs — "Sleep-time agents" (async memory maintenance, every-N-steps) — https://docs.letta.com/guides/agents/architectures/sleeptime/ — 2026, accessed 2026-06.
