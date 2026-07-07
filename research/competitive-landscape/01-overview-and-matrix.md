# Landscape Overview & Master Matrix

**Scope:** every player researched in this pack, mapped across both axes (AI-OS experience + AI company/workforce) plus infra references, with a master capability matrix and the white-space call-out. Full per-player detail (with ≥5 sources each) lives in docs `10`–`31`; this doc is the map. Synthesis lives in `40`–`46`.

---

## The categorized map

```
AXIS A — AI-OS EXPERIENCE (foreground, what the user sees)
  Consumer "AI OS":   Warmwind(10) · Flowith(11) · Rabbit(15) · /dev/agents→Meta(14) · Genspark(15) · Manus(15)
  Real device OS (Cat-1): Aluminium/Google(12) · Brain Natural OS(13)

AXIS B — AI COMPANY / WORKFORCE (background, the org doing the work)
  "AI software company" frameworks: MetaGPT · ChatDev · CrewAI · AutoGen/AG2 · LangGraph · AgentVerse (20)
  Enterprise AI workforce:          ServiceNow · Salesforce Agentforce · Microsoft Agent 365 · Google Gemini Enterprise (21)
  AI-employee startups:             Relevance AI · Lindy · Artisan · 11x · Cognosys · Sierra · Cognition/Devin (22)

INFRA / ARCHITECTURE (the plumbing, mine for patterns — not rivals)
  VAST · AIOS(Rutgers) · Agno AgentOS · Letta/MemGPT (30)

VERTICAL agentic-OS (proof the framing goes per-domain)
  Legora(legal) · NickAI(trading) · Harvey(legal) · Imbue (31)
```

The three meanings of "OS" (real device OS · AI-agent experience layer · infra/kernel-for-agents) are explained in `40`. **We are the AI-agent experience layer (Cat-2) with consumer ambition, built on a reused Linux kernel.**

## Master capability matrix

Rows alphabetical. Columns use the full-vision yardstick. Legend: ✅ shipped/strong · ◑ partial/feature-level · ✗ none/undisclosed. Every value traces to the cited per-player doc; confidence and sources are in those docs.

| Player (doc) | Axis | Recursion / org depth | Chairman | OS surface | Per-agent security | Verifier | Receipts | PQC | Deploy | Availability | Pricing | Stage / funding |
|---|---|---|:--:|---|:--:|:--:|:--:|:--:|---|---|---|---|
| 11x (`22`) | B | flat worker roster | ✗ | ◑ | ◑ SOC2 | ✗ | ✗ | ✗ | cloud | shipping | annual ~$5k/mo | $50M B, ~$320M val |
| Aluminium/Google (`12`) | A | flat (1 assistant) | ✗ | ✅ real OS | ◑ per-app | ✗ | ✗ | ✅ Android PQC | hybrid | OEM Q3 2026 | ~$299–1,500 device | Google product |
| Agno AgentOS (`30`) | Infra | 2-tier teams | ✗ | ◑ control plane | ✅ RBAC | ✗ | ✅ audit logs | ✗ | self-host | OSS v2.5 | OSS+commercial | VC startup |
| AIOS / Rutgers (`30`) | Infra | flat kernel | ✗ | ◑ web/term | ✅ priv groups | ✗ | ◑ | ✗ | self-host | OSS (COLM'25) | free | academic |
| Artisan (`22`) | B | flat (Ava) | ✗ | ◑ | ◑ ISO27001 | ✗ | ✗ | ✗ | cloud | shipping | ~$2–5k/mo | $25M A |
| Brain Natural OS (`13`) | A | flat (1 agent) | ✗ | ✅ real OS | ◑ perimeter | ✗ | ✗ | ✗ | hybrid | on sale (JP) 2026-04 | ¥93,600 device | ~$51.5M |
| ChatDev (`20`) | B | linear dyad chain | ✗ | ◑ | ✗ | ◑ | ✗ | ✗ | self-host | OSS | free | academic |
| Cognition/Devin (`22`) | B | 2-tier (MultiDevin) | ✗ | ◑ | ✅ VPC/SOC2 | ◑ | ◑ | ✗ | cloud/VPC | shipping | $20–$500+/Ent | $1B D, ~$26B |
| Cognosys→Cohere (`22`) | B | flat personal | ✗ | ◑ | ✗ | ✗ | ✗ | ✗ | cloud | **sunset** | ~$15/mo | acq. Cohere 2025 |
| CrewAI (`20`) | B | 2-tier (+nestable) | ✗ | ✗ dev lib | ◑ RBAC | ◑ guardrail | ◑ trace | ✗ | self-host | OSS, ~52k★ | OSS+Ent | VC |
| AutoGen/AG2 (`20`) | B | 2-tier (SocietyOfMind) | ✗ | ✗ dev lib | ◑ sandbox | ◑ | ◑ | ✗ | self-host | OSS | free | Microsoft/OSS |
| /dev/agents→Meta (`14`) | A | flat | ✗ | ✅ | ◑ consent | ✗ | ◑ dev logs | ✗ | cloud | **team→Meta** | n/a | $56M seed |
| Flowith (`11`) | A | flat–2-tier | ✗ | ✅ canvas/OS | ✗ | ◑ RAG | ✗ | ✗ | cloud | shipping | free–~$500/mo | seed "tens of $M" |
| Genspark (`15`) | A/B | 2-tier (Claw) | ✗ | ◑ | ◑ tenant | ◑ MoA (in-loop) | ◑ attribution | ✗ | cloud | shipping | ~$25–80/mo | ~$1.6B val |
| Google Gemini Ent. (`21`) | B | orchestration | ✗ | ◑ | ✅ Agent Identity | ◑ anomaly | ✅ | ✗ | cloud | GA 2026-04 | undisclosed | Google |
| Harvey (`31`) | B/vert | 2-tier builder | ✗ | ◑ | ◑ enterprise | ✅ citation-trace | ◑ | ✗ | cloud | shipping | ~$200k ACV | $200M @ $11B |
| Imbue (`31`) | B/vert | flat parallel | ◑ | ✅ desktop | ✅ sandbox | ◑ | ◑ merge/discard | ✗ | hybrid | beta | free beta | $200M B, >$1B |
| Legora (`31`) | B/vert | 2-tier | ✗ | ✅ "OS" web | ◑ audited | ◑ review-commit | ✅ audit trail | ✗ | cloud | aOS 2026-05 | enterprise | ~$600M D, $5.6B |
| Letta/MemGPT (`30`) | Infra | 2-tier | ✗ | ◑ ADE/CLI | ◑ block sharing | ✗ | ◑ run history | ✗ | self-host/cloud | OSS v0.16 | OSS+cloud | VC (ex-MemGPT) |
| Lindy (`22`) | B | 2-tier "Societies" | ✗ | ◑ | ✗ | ✗ | ✗ | ✗ | cloud | shipping | free–~$200/mo | undisclosed |
| Manus (`15`) | A/B | 2-tier per task | ✗ | ◑ | ✅ ephemeral VM | ◑ validate (in-loop) | ✗ | ✗ | cloud | shipping; **ownership flux** | ~$39–200/mo | $75M B; Meta deal blocked |
| MetaGPT (`20`) | B | fixed role pipeline | ✗ | ◑ MGX | ✗ | ◑ exec feedback | ✗ | ✗ | self-host | OSS, ~68k★ | OSS+MGX | Ant/Cathay round |
| Microsoft Agent 365 (`21`) | B | 2-tier (A2A) | ✗ | ◑ | ✅ Entra least-priv | ✅ **Critique** | ✅ Defender | ✗ | cloud | GA 2026-05 | $15/user/mo | Microsoft |
| Rabbit (`15`) | A | flat | ✗ | ✅ device OS | ✗ (2024 breach) | ✗ | ✗ | ✗ | hybrid | shipping | $199 + $99/mo | ~$30M |
| Relevance AI (`22`) | B | 2-tier MAS | ✗ | ◑ | ◑ SOC2 | ✗ | ✗ | ✗ | cloud | shipping | free–$234/mo | $24M B, ~$37M total |
| Salesforce Agentforce (`21`) | B | 2-tier (A2A) | ✗ | ◑ | ✅ cert+gateway | ◑ Einstein Trust | ✅ Command Center | ✗ | cloud | GA 2026-02 | ~$2/conv, ~$5 PUPM | Salesforce |
| ServiceNow (`21`) | B | flat fleet | ✗ | ◑ console | ✅ identity+scope | ✗ | ✅ audit | ✗ | cloud | →GA Sep 2026 | enterprise | ServiceNow |
| Sierra (`22`) | B | 1–2 tier | ✗ | ◑ | ✅ SOC2/guardrail | ◑ supervisory | ◑ | ✗ | cloud | shipping | ~$150k+/yr outcome | $950M @ $15.8B |
| VAST (`30`) | Infra | flat (MCP tools) | ✗ | ◑ runtime | ◑ PolicyEngine | ✗ | ◑ tamper-proof (planned) | ✗ | hybrid/on-prem | shipping; Policy end-2026 | enterprise | VAST Data |
| Warmwind (`10`) | A | flat (peer pool) | ◑ | ✅ streamed Linux | ◑ container | ✗ visual-monitor | ◑ task list | ✗ | cloud | closed beta | sub (TBD) | €1.5M seed |
| **Our vision** | A+B | ✅ recursive→1-task | ✅ Chairman | ✅ (Warmwind-class) | ✅ per-employee least-priv | ✅ independent+veto | ✅ replayable | ✅ ML-KEM/DSA | local/cloud/hybrid | — | personal | repo spine `AGENTS.md` |

## White-space call-out

Reading the matrix top to bottom, the empty columns are the story:

1. **Chairman (P2): a column of ✗.** No player seats the human atop the org. *Uncontested.*
2. **Runtime recursion to a one-task leaf (P1): nobody.** Deepest is author-time nesting (LangGraph) or fixed roles (MetaGPT) (`20`).
3. **PQC (P4): a column of ✗ in our category.** Only the device OS below us (Aluminium) has it (`12`, `41`).
4. **Independent verifier with veto (T1): nobody.** Closest are in-loop ensembles (Genspark/Manus) or an enterprise feature (MS Critique) — none is a standing employee with block authority (`42`).
5. **Personal + sovereign + trusted, together (P5): being vacated**, not just empty (/dev/agents→Meta, Cognosys→Cohere) (`14`, `22`).

The union of these five is the wedge. Full argument in `43-full-vision-match.md`; positioning in `44`.

## How to read the rest of the pack

- **Per-player deep dives + SWOT + facts tables:** `10`–`15` (Axis A), `20`–`22` (Axis B), `30`–`31` (infra/vertical).
- **Synthesis:** `40` (OS fundamentals), `41` (security+quantum), `42` (trust), `43` (the crux), `44` (positioning), `46` (executive roster).
- **Next step:** `45` (the one-at-a-time interview, after you read this).
- **Internal self-audit to read alongside:** root [`SWOT.md`](../../SWOT.md).
