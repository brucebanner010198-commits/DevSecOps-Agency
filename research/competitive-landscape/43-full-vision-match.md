# Full-Vision Match — is anyone already building this?

**Purpose:** the Sovereign's central question. Score **every** player in the pack against the *complete* vision and deliver a verdict. The vision has five non-negotiable pillars; partial matches don't count — the thesis is the **union**.

---

## The five pillars of the full vision

1. **P1 — Recursive company.** A deep org: executives → teams → sub-teams → … → a leaf AI employee that does **exactly one task**. Crucially, **runtime, agent-initiated** depth (an employee can spin up its own sub-team), not a developer's fixed org chart.
2. **P2 — Human as Chairman.** The user sits **atop** the org as Chairman of the Board, holding the sole governing authority — not as an operator, admin, or end-user.
3. **P3 — Interactive OS experience.** A foreground the user sees and touches that *feels like an OS* (not a chat box, not a dev library).
4. **P4 — Trust layer (the union of the 5 Ts, doc 42).** Independent verifier + per-agent least-privilege + replayable receipts + post-quantum crypto.
5. **P5 — Personal & sovereign.** Built for one individual, data-owned, runs on existing hardware, not an enterprise control plane and not sold to a platform.

## Scorecard (✅ full · ◑ partial · ✗ none)

| Player | P1 Recursive | P2 Chairman | P3 OS surface | P4 Trust union | P5 Personal+sovereign | Verdict |
|---|:--:|:--:|:--:|:--:|:--:|---|
| **Warmwind** (`10`) | ✗ | ◑ | ✅ | ✗ | ◑ | Best **UX**; not a company, not trusted |
| **Flowith** (`11`) | ✗ | ✗ | ✅ | ✗ | ✗ | A canvas, not a company |
| **Aluminium/Google** (`12`) | ✗ | ✗ | ✅ (real OS) | ◑ (PQC only) | ✗ | Real OS, single assistant, Google-locked |
| **Brain Natural OS** (`13`) | ✗ | ✗ | ✅ (real OS) | ✗ | ◑ | Shipped AI phone; one agent |
| **/dev/agents** (`14`) | ✗ | ✗ | ✅ | ◑ (trust-as-kernel idea) | ✗ (**→Meta**) | Closest *philosophy*; gone to Meta |
| **Genspark** (`15`) | ✗ | ✗ | ◑ | ◑ (in-loop verifier) | ✗ | Verifier-adjacent only |
| **Manus** (`15`) | ◑ (2-tier/task) | ✗ | ◑ | ◑ (isolation) | ✗ (ownership flux) | Best sandbox; no org/Chairman |
| **Rabbit** (`15`) | ✗ | ✗ | ✅ (device) | ✗ | ◑ | Hardware; trust liability |
| **MetaGPT / ChatDev** (`20`) | ◑ (fixed roles) | ✗ | ◑ (MGX chat) | ✗ | ✅ (OSS) | "AI company" metaphor, shallow+fixed |
| **CrewAI/AutoGen/LangGraph** (`20`) | ◑ (author-time nesting) | ✗ | ✗ (dev libs) | ◑ | ✅ (OSS) | The recursion *primitives* exist here |
| **ServiceNow** (`21`) | ✗ | ✗ | ◑ (console) | ◑ | ✗ (enterprise) | Department fleet, admin seat |
| **Salesforce Agentforce** (`21`) | ◑ (2-tier) | ✗ | ◑ | ◑ | ✗ (enterprise) | Governed fleet, not a company |
| **Microsoft Agent 365** (`21`) | ◑ (2-tier) | ✗ | ◑ | ◑–✅ (**Critique** verifier) | ✗ (enterprise) | **Strongest trust**; enterprise admin |
| **Google Gemini Enterprise** (`21`) | ◑ | ✗ | ◑ | ◑ | ✗ (enterprise) | Governed fleet |
| **Relevance/Lindy/Artisan/11x** (`22`) | ◑ (2-tier max) | ✗ | ◑ | ✗ | ✗ | "AI employees," a department |
| **Sierra / Cognition** (`22`) | ◑ (2-tier) | ✗ | ◑ | ◑ | ✗ (enterprise) | Huge, narrow, enterprise |
| **Legora/NickAI/Harvey/Imbue** (`31`) | ◑ (2-tier) | ✗ | ◑ ("OS" branding) | ◑ (audit/citation) | ✗ (vertical/enterprise) | Vertical aOS; proves the framing |
| **VAST/AIOS/Agno/Letta** (`30`) | ✗ (flat/2-tier) | ✗ | ✗ (infra) | ◑ (policy/logs) | ◑ (self-host) | The plumbing, not the product |

**Nobody has a single ✅ across all five. No player even has four.**

## What the scorecard reveals

- **P1 (recursive company): the deepest anyone goes is author-time-wired nesting** (LangGraph subgraphs, AutoGen SocietyOfMind) or fixed role pipelines (MetaGPT). **No one offers runtime, agent-initiated recursion to a one-task leaf** (`20`). The *primitive* ("a team that looks like one agent") exists in the OSS frameworks — it is buildable — but no product ships it as the org shape.
- **P2 (Chairman): uncontested.** Every single player puts the human in an operator / admin / reviewer / end-user seat. **Not one seats the human as Chairman atop a standing AI org.** This is the most unique and most defensible pillar.
- **P3 (OS surface): crowded and well-executed.** Warmwind is the bar; Aluminium/Brain are real OSes; many have "OS" branding. We do **not** win on novelty here — we adopt Warmwind-class UX (`10`).
- **P4 (trust union): led by enterprise, absent in consumer, PQC missing everywhere in-category.** Microsoft Agent 365 + Critique is the high-water mark but enterprise-only; PQC appears only in the device OS below us (`12`, `41`, `42`).
- **P5 (personal+sovereign): the consumer slot is not just open — it's being *vacated*.** /dev/agents → Meta, Cognosys → Cohere (sunset), Manus deal blocked: the few who aimed personal got absorbed or stalled (`14`, `22`, `15`).

## Closest combinations (who to watch)

- **Most pillars at once: Microsoft Agent 365** (P3◑ + P4✅ + 2-tier P1◑) — but P2✗ and P5✗ are structural; it will never be a personal company you chair.
- **Closest philosophy: /dev/agents** (trust-as-kernel, personal intent) — now inside Meta; assume a Meta personal-agent OS in 12–18 months (`14`). This is the **clock** on the opportunity.
- **Closest org metaphor: MetaGPT/ChatDev** ("AI software company") — but fixed, shallow, no trust, no Chairman.
- **Closest building blocks for P1: CrewAI/AutoGen/LangGraph** — the recursion primitives we'd build on.

## Verdict

**The full vision is unoccupied.** Every rival owns one or two pillars; none owns the **union**, and three of the five pillars are *structurally* hard for the leaders to reach:

- **P2 (Chairman)** contradicts the enterprise admin model every leader is built on.
- **P5 (personal+sovereign)** contradicts the platform-ownership business model (and the market is literally selling these teams to Meta).
- **P1 (runtime recursion)** is technically buildable (primitives exist) but no one has productized it.

The defensible core is therefore **not the agent capability** (that's commoditizing fast) — it's the **org shape (recursive company + Chairman)** fused with the **trust union (verifier + per-agent security + receipts + PQC), delivered personally and sovereignly.** That specific combination has no occupant.

**Caveats (intellectual honesty):**
- "Nobody ships X" is bounded by public sources as of 2026-06; private/unreleased work (esp. Meta, post-/dev/agents) is unknown.
- The build risk is real — runtime recursion + a verifier with veto + reversible receipts + PQC is a *lot* of surface. The repo already has the governance spine (`AGENTS.md`, `councils/`), which de-risks the org+trust pillars more than any rival's starting point.

## Sources

- Every cell cites its player doc (`10`–`31`), which each carry ≥5 dated sources. Cross-refs: `20` (recursion finding), `41` (PQC), `42` (trust union), `46` (roster). Recursion-primitive claim: `20-multi-agent-frameworks.md` §"biggest finding."
