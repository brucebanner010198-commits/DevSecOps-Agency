# Trust as the Core Problem — what "trustable" means, and why nobody owns it

**Purpose:** the Sovereign's thesis is that the real problem is a **trustable** AI OS/company — trust is the wedge, not a feature. This doc defines trust operationally, maps how every rival and every trust framework addresses it, and locates the gap.

---

## 1. Five dimensions of "trustable" (operational definition)

"Trust" is not one thing. For a personal AI company that touches a user's whole digital life, it decomposes into five testable properties:

| # | Dimension | The question the user is really asking | Mechanism |
|---|---|---|---|
| T1 | **Competence** | "Did it do the task correctly?" | a **verifier** that checks output against spec + facts, with authority to block |
| T2 | **Containment** | "Can one employee do damage beyond its job?" | **per-agent least-privilege** — scoped, audited tools; default-deny inter-agent |
| T3 | **Accountability** | "Can I see what it did and undo it?" | **receipts / reversibility** — append-only, replayable, signed action trail |
| T4 | **Confidentiality** | "Is my whole digital life safe, now and later?" | encryption + identity, **post-quantum** (harvest-now-decrypt-later) |
| T5 | **Ownership** | "Is this mine, or the platform's — and will it be sold?" | data sovereignty, user-owned keys, no acqui-exit of the trust layer |

A truly trustable product must hit **all five**. The market hits one or two each.

## 2. How every rival scores on the five (from the player docs)

| Player | T1 Verifier | T2 Per-agent security | T3 Receipts/reversibility | T4 PQC | T5 Ownership | Net |
|---|---|---|---|---|---|---|
| Warmwind (`10`) | ✗ (visual monitoring) | ~ (container isolation) | ~ (task list/logs) | ✗ | ~ (cloud-only, EU) | 0.5/5 |
| Flowith (`11`) | ~ (RAG grounding) | ✗ (undisclosed) | ✗ | ✗ | ✗ (cloud) | 0/5 |
| Aluminium/Google (`12`) | ✗ | ~ (per-app sandbox) | ✗ | ✅ (Android PQC) | ✗ (Google-locked) | 1/5 |
| Brain Natural OS (`13`) | ✗ | ~ (perimeter) | ✗ | ✗ | ~ (on-device+JP cloud) | 0.5/5 |
| /dev/agents→Meta (`14`) | ✗ | ~ (consent-based) | ~ (dev logs) | ✗ | ✗ (**sold to Meta**) | 0.5/5 |
| Genspark (`15`) | ~ (MoA cross-check, *in-loop*) | ~ (tenant isolation) | ~ (source attribution) | ✗ | ✗ (cloud) | 1/5 |
| Manus (`15`) | ~ (validation sub-agent, *in-loop*) | ✅ (ephemeral isolated VMs) | ✗ (sandboxes destroyed) | ✗ | ✗ (ownership in flux) | 1/5 |
| Rabbit (`15`) | ✗ | ✗ (**2024 key breach**) | ✗ | ✗ | ~ (own device) | 0/5 |
| MetaGPT/ChatDev (`20`) | ~ (exec feedback) | ✗ | ✗ | ✗ | ✅ (OSS, self-host) | 1/5 |
| CrewAI/AutoGen/LangGraph (`20`) | ~ (guardrails, eval) | ~ (sandbox/RBAC) | ~ (tracing) | ✗ | ✅ (OSS) | 1.5/5 |
| ServiceNow (`21`) | ✗ | ✅ (identity+scoping) | ✅ (audit) | ✗ | ✗ (enterprise) | 2/5 |
| Salesforce Agentforce (`21`) | ~ (Einstein Trust Layer) | ✅ (cert+gateway) | ✅ (Command Center) | ✗ | ✗ (enterprise) | 2.5/5 |
| Microsoft Agent 365 (`21`) | ✅ (**Critique**: Claude audits GPT) | ✅ (Entra CA, least-priv) | ✅ (Defender/audit) | ✗ | ✗ (enterprise) | 3/5 |
| Google Gemini Enterprise (`21`) | ~ (anomaly detection) | ✅ (Agent Identity/Gateway) | ✅ | ✗ | ✗ (enterprise) | 2.5/5 |
| Relevance/Lindy/Artisan/11x (`22`) | ✗ | ~ (SOC2 perimeter) | ✗ | ✗ | ✗ | 0.5/5 |
| Sierra/Cognition (`22`) | ~ (supervisory/guardrails) | ✅ (VPC/SOC2) | ~ | ✗ | ✗ (enterprise) | 2/5 |
| Vertical (Legora/NickAI/Harvey/Imbue) (`31`) | ~ (citation traceability) | ✅ (audited/sandboxed) | ✅ (audit trail) | ✗ | ✗ (enterprise) | 2.5/5 |
| Infra (VAST/AIOS/Agno/Letta) (`30`) | ✗ | ✅ (policy/RBAC) | ✅ (logs) | ✗ | ✅ (self-host) | 2.5/5 |

Legend: ✅ shipped · ~ partial/feature-level · ✗ absent. Scores are directional, not precise — see each player doc for cited detail.

## 3. The three structural truths

1. **The leaders are enterprise, and they trade ownership (T5) for governance.** Microsoft Agent 365 is the single strongest trust story (it even ships **Critique** — Anthropic's Claude auditing OpenAI's GPT, the closest thing to an independent verifier). But it is an *enterprise control plane for an admin*, not a *personal company a user owns*. T5 is structurally impossible for them.
2. **The personal/consumer players are weak on every dimension except, occasionally, ownership.** OSS frameworks (MetaGPT, CrewAI) and infra (AIOS, Letta) give you ownership but no verifier, no receipts product, no PQC. Consumer AI-OS players (Warmwind, Flowith, Brain) give you UX but almost no trust.
3. **Nobody ships T1+T2+T3+T4+T5 together, and nobody ships T4 (PQC) at all in our category.** The verifier exists only as an in-loop ensemble (Genspark, Manus) or an enterprise feature (MS Critique) — never as an *independent employee with veto*. PQC exists only one layer down (the device OS), never in the AI-company layer.

## 4. The trust frameworks (prior art to cite, not products to fear)

Enterprise governance specs are maturing — they define the bar and the vocabulary, but none is a consumer product:
- **CSA Agentic Trust Framework** — Zero-Trust for agents (governance spec).
- **Microsoft Agent Governance Toolkit** — runtime governance, claims all 10 OWASP agentic risks.
- **NVIDIA verified agent skills** — signed skill cards / capability governance.
- **TAIP** (arXiv) — continuous AI-posture assurance.
- Industry-admitted gap: ~18% of security leaders trust their identity systems for agents (`41` [5]).

We **adopt these standards** (OWASP agentic risks, Zero-Trust, signed capabilities) and **productize them for a person** — turning a compliance framework into a felt, visible experience (a verifier you watch, receipts you replay, a Chief Trust Officer who answers to you).

## 5. The cautionary tales (why a user *wants* a trust-first product)

The market itself is generating the demand:
- **/dev/agents → Meta** (the trust-OS team sold; `14`).
- **Manus → Meta deal blocked/unwound by regulators** (`15`).
- **11x ARR/logo scandal**, 75–90% churn (`22`).
- **Cognosys (the one personal player) absorbed, product sunset** (`22`).
- **Rabbit 2024 hardcoded-API-key breach** (`15`).

Each is a story of *misplaced trust*. "Yours, verified, reversible, quantum-safe, and never sold" is the answer the market keeps proving people need.

## 6. The gap (one sentence)

**No product unifies competence (independent verifier) + containment (per-agent least-privilege) + accountability (replayable receipts) + confidentiality (PQC) + ownership (sovereign, unsellable) for a single person — and that union is the trust wedge.**

## Sources

- All per-player scores cite the player docs `10`–`31` (each with its own ≥5 sources). Frameworks + PQC: `41-security-and-quantum.md` and its sources [1]–[9]. Repo trust spine: `AGENTS.md:13,32`, `SECURITY.md`, `THREAT-MODEL.md`, `councils/{audit,evaluation,red-team,security}/`.
