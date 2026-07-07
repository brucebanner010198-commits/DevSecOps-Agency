<!-- Shared shape for every player doc in this pack. Doc 01 (matrix) and 43 (scorecard) parse by these headers — headers are normative, not suggestive. -->

# Enterprise "AI Workforce" Layer — ServiceNow · Salesforce · Microsoft · Google

**One-liner:** The four enterprise platform giants now ship governed fleets of role-specialised AI "workers" (sales, service, IT, HR, security) under a centralized human-run control plane — deep on governance and trust tooling, but enterprise-only and org-shaped as flat fleets, not a recursive company with a Chairman.
**Axis:** B = AI company/workforce (background) — with weak A (foreground) surfaces via chat copilots.
**Category (3-meanings-of-OS):** 2 AI-agent experience layer + 3 AI infra/kernel-for-agents (governance control planes). Not a real device OS.
**Stage / availability:** Shipping (all four GA in 2026) · **As-of:** 2026-06

---

## What it does best · What it lacks · What we take

- **Best:** Production-grade governance control planes — per-agent cryptographic identity, audit trails, least-privilege scoping, policy gateways (ServiceNow AI Control Tower [1][8], Microsoft Agent 365 [4], Google Agent Gateway/Agent Identity [6], Salesforce MuleSoft Agent Gateway [9]). This is the strongest enterprise build-out of the trust wedge we've found.
- **Best:** Real, measured autonomy in deployment — ServiceNow says specialists resolve 91% of cases without reassignment [3]; Agentforce claims 85% query resolution [2]. They have proven that role-specialised agents complete end-to-end work.
- **Best:** Microsoft's "Critique" cross-model verifier (Claude audits GPT output before the user sees it [11][12]) is a shipped, dedicated anti-hallucination mechanism — the closest competitor analogue to our verifier/council concept.
- **Lacks:** No recursive org and no Chairman model. Agents are flat or 2-tier (orchestrator → sub-agents [10][9]) fleets staffed for functional departments (sales/IT/HR/support), not a full C-suite reporting upward to one human principal.
- **Lacks:** Enterprise-only. None is personal/individual-owned. Identity, billing, and governance are all tenant/admin-scoped, not "my agents that I, an individual, own and command" [4][6].
- **Lacks:** No stated post-quantum cryptography in any of the four (searched; none surfaced) [4][6][14]. Receipts/audit exist but PQC does not.
- **We take:** The control-plane primitives validate our trust thesis — per-agent identity + audit + least-priv + policy gateway are exactly our `councils/audit/`-style anchors. The Critique verifier validates a dedicated cross-model checker. We differentiate on: personal ownership, recursive Chairman-topped org, and PQC.

## Deep dive

### ServiceNow — Autonomous Workforce + AI Control Tower (Knowledge 2026)

At Knowledge 2026 (announced 2026-05-05), ServiceNow expanded its **Autonomous Workforce** — a suite of AI "specialists" that "complete entire business processes from start to finish, without human intervention" — to "every major business function": IT operations / site reliability, CRM, HR / employee service, security & risk, plus finance, legal, and procurement [1][3]. President/CPO Amit Zavery framed it as "Enterprises need AI that senses, decides, and securely acts" [synthesised from [3] quote]. Availability: L1 IT Service Desk specialist, CRM specialists, and employee-service specialists available now; broader IT specialists June 2026; security/risk specialists preview June 2026, GA September 2026 [3]. Early metrics: specialists resolve 91% of cases without reassignment; ServiceNow's internal IT specialist resolves cases "99% faster" than humans; Docusign targeting 90% autonomous IT ticket resolution [1][3].

**Org model:** This is a fleet of department-scoped specialists, not a recursive company. There is no AI C-suite and no single human "Chairman" persona; the human role is governance/oversight via the **AI Control Tower** [user-knowledge: maps to our Chairman concept only loosely]. The Control Tower is the trust story: it "finds every AI agent, model, and identity," and "every action runs through AI Control Tower for identity verification, permission scoping, metering, audit trails, session management, OAuth, and role-based tool packages" [14]. At Knowledge 2026 it added 30 new integrations (AWS, Google Cloud, Azure, SAP, Oracle, Workday) and five risk frameworks aligned to NIST and the EU AI Act [14]. It explicitly governs other vendors' agents, and a deepened integration extends Control Tower governance to **Microsoft Agent 365**, Foundry, and Copilot Studio [1][4]. Enterprise-only; no PQC stated.

### Salesforce — Agentforce 360 / Agentforce 3

**Agentforce 360** reached GA 2026-02-23; Salesforce claims deployments in 124 countries resolving 85% of customer queries with escalation rates as low as 5% [2]. Roles are functional: **Service Agent** (chatbot replacement) and **SDR / Sales** agents that engage prospects 24/7 [2 search]. **Agentforce 3** (announced 2025-06-23) added the **Command Center** observability dashboard (latency, error rates, escalation rates) and a **MuleSoft-engineered Agent Gateway** that "centralizes registration, identity management, and policy controls," giving "each digital agent … a secure credential and certificate so that every action can be audited to a specific agent," described as a zero-trust design [9]. Multi-agent support via the **MuleSoft A2A connector** lets agents act as A2A server/client [9].

**Trust posture:** the **Einstein Trust Layer** provides dynamic grounding, zero data retention, and toxicity detection; guardrails are on by default and admin-configurable [2 search]. **Agent Script** is a new scripting language combining AI creativity with "deterministic controls" and conditional logic [2]. **Org model:** orchestrator + sub-agent (2-tier), not recursive; no AI C-suite, no individual-Chairman. **Pricing** is consumption-led: Flex Credits (~$500/100k credits; ~20 credits/action), $2/conversation, or employee per-user add-ons from ~$5 PUPM [pricing search]. Enterprise-only; no PQC stated.

### Microsoft — Copilot agents / Agent 365 / Copilot Studio

**Microsoft Agent 365** went GA 2026-05-01 as a "control plane to observe, govern, and secure agents and their interactions — including agents built with Microsoft AI and ecosystem partners" [4]. Governance components: **Defender** (discovery, runtime blocking), **Intune** (policy, unmanaged-agent detection), **Entra** (Conditional Access for agents, identity), and **Purview** (sensitivity labels propagate to agent output) [4][search]. Least-privilege enforcement and lifecycle (start/stop/delete) included. **Pricing:** $15/user/month standalone, or bundled in **Microsoft 365 E7** [4]. Commercial customers only; "Windows 365 for Agents" preview US-only [4].

**Org model:** **Copilot Studio multi-agent orchestration** (GA April 2026) uses a manager/orchestrator pattern — a main agent routes to domain sub-agents and synthesises responses — plus A2A protocol, Fabric integration, and the M365 Agents SDK [10]. This is 2-tier, not recursive. **Verifier (strongest in class):** "Critique" for the Researcher agent (announced 2026-03-30) has Anthropic's **Claude audit OpenAI's GPT** output for accuracy, completeness, and citation integrity before the user sees it — scoring 57.4 on the DRACO benchmark, ~13.8% above Claude Opus 4.6 alone [11][12]. This is a shipped, dedicated cross-model verifier — directly analogous to our verifier/council. No PQC stated.

### Google — Gemini Enterprise Agent Platform / Agentspace

The **Gemini Enterprise Agent Platform** launched 2026-04-22 (Google Cloud Next), folding Agentspace/Vertex into one platform to "build, scale, govern, and optimize agents" [6]. Governance primitives are notably trust-forward: **Agent Identity** ("every agent receives a unique cryptographic ID … a clear, auditable trail for every action … mapped back to defined authorization policies"); **Agent Registry** (single source of truth, only governed/approved assets); **Agent Gateway** ("air traffic control," enforcing policy + **Model Armor** against prompt injection and data leakage) [6]. Security adds **Agent Anomaly Detection** (statistical + LLM-as-a-judge to flag unusual reasoning), **Agent Threat Detection**, and a **Security Dashboard** on Security Command Center [6]. Multi-agent: agent-to-agent delegation with generative + deterministic orchestration; long-running agents with an Agent Memory Bank [6].

**Org model:** centralized human governance ("keeping human oversight at the center" — L'Oréal [6]); delegation is orchestration, not a recursive company; no AI C-suite, no personal Chairman. Surfaced to employees via the **Gemini Enterprise app**. Pricing not disclosed in the launch [6]. Enterprise-only; no PQC stated.

## SWOT (with so-what-for-us)

- **Strengths:** Mature governance control planes with per-agent identity, audit, least-priv, policy gateways — so-what: validates our trust wedge is real and buyable; we cannot win on "we have governance," only on personal + recursive + PQC.
- **Weaknesses:** Flat/2-tier functional fleets, no Chairman-topped recursive org, enterprise-only — so-what: a genuinely *personal* AI company atop an individual is open white space none of them occupy.
- **Opportunities:** Microsoft's Critique proves enterprises want a dedicated verifier; none ships PQC — so-what: a verifier-by-default + PQC-receipts posture is a credible differentiator with primary-source proof of demand.
- **Threats:** These vendors own distribution, identity (Entra/Okta-class), and data gravity; if any pivots "down-market to individuals," our wedge narrows — so-what: move fast on personal ownership and Chairman UX before they do.

## Facts table

Each cell cited `[n]` or `unknown`. Confidence L/M/H. Row-group per vendor.

| Dimension | Value | Conf | Source |
|---|---|---|---|
| **ServiceNow** — Recursion / org depth | Flat fleet of department specialists (IT/CRM/HR/security/finance/legal/procurement); no recursion | H | [1][3] |
| User-as-Chairman fit | No — human is governance/oversight via AI Control Tower, not a Chairman atop an AI org | M | [14][1] |
| Interactive-OS surface | Chat / Now Assist; no desktop OS | M | [3] |
| Per-agent security | Per-agent identity verification, permission scoping, OAuth, role-based tool packages | H | [14] |
| Verifier / anti-hallucination | Governance/guardrails + risk frameworks (NIST/EU AI Act); no dedicated cross-model verifier surfaced | M | [14] |
| Receipts / reversibility | Audit trails, session mgmt, metering through Control Tower | H | [14] |
| Post-quantum (PQC) | None stated | M | [14] |
| Local / cloud / hybrid | Cloud (Now Platform); multi-cloud governance integrations | H | [14] |
| Hardware | Cloud-only | H | [1] |
| Availability | Now (L1/CRM/employee); IT June 2026; security/risk preview June, GA Sept 2026 | H | [3] |
| Pricing | unknown (enterprise/negotiated) | L | unknown |
| Funding / stage | Public co. (NYSE: NOW); GA shipping | H | [1] |
| UX notes | "Senses, decides, securely acts"; specialists resolve 91% cases w/o reassignment | M | [1][3] |
| **Salesforce** — Recursion / org depth | 2-tier orchestrator → sub-agents (A2A); functional roles (Service, SDR/Sales) | H | [9][2] |
| User-as-Chairman fit | No — admin/leader oversight via Command Center; no Chairman-atop-org model | M | [9][2] |
| Interactive-OS surface | Chat agents + Command Center dashboard; no desktop OS | M | [9] |
| Per-agent security | Per-agent credential + certificate, MuleSoft Agent Gateway, zero-trust, policy controls | H | [9] |
| Verifier / anti-hallucination | Einstein Trust Layer (dynamic grounding, ZDR, toxicity detection); Agent Script deterministic controls | H | [2] |
| Receipts / reversibility | Every action auditable to a specific agent; Command Center observability | H | [9] |
| Post-quantum (PQC) | None stated | M | [2][9] |
| Local / cloud / hybrid | Cloud (Salesforce/Data 360) | H | [2] |
| Hardware | Cloud-only | H | [2] |
| Availability | Agentforce 360 GA 2026-02-23; Agentforce 3 since 2025-06-23 | H | [2][9] |
| Pricing | Flex Credits ~$500/100k (~20/action); $2/conversation; employee add-on ~$5 PUPM | M | [pricing search] |
| Funding / stage | Public co. (NYSE: CRM); GA, 124 countries | H | [2] |
| UX notes | Claims 85% query resolution, ≥5% escalation; 272k certified partners | M | [2][9] |
| **Microsoft** — Recursion / org depth | 2-tier orchestrator → sub-agents (Copilot Studio + A2A); no recursion | H | [10] |
| User-as-Chairman fit | No — admin governance via Agent 365 control plane | M | [4] |
| Interactive-OS surface | Copilot chat; "Cowork"/screen agents; Windows 365 for Agents (US preview) | M | [4][11] |
| Per-agent security | Entra Conditional Access for agents, least-privilege, Defender SPM, Intune policy | H | [4] |
| Verifier / anti-hallucination | "Critique" — Claude audits GPT output pre-delivery (DRACO 57.4, +13.8% vs Claude alone) | H | [11][12] |
| Receipts / reversibility | Purview labels on agent output; audit; lifecycle start/stop/delete | H | [4] |
| Post-quantum (PQC) | None stated | M | [4] |
| Local / cloud / hybrid | Cloud (M365); endpoint/SaaS coverage via Entra/Intune | H | [4] |
| Hardware | Cloud-only (Windows 365 for Agents = cloud PC) | M | [4] |
| Availability | Agent 365 GA 2026-05-01; Copilot Studio multi-agent GA Apr 2026; Critique 2026-03-30 | H | [4][10][11] |
| Pricing | Agent 365 $15/user/mo standalone, or bundled in M365 E7 | H | [4] |
| Funding / stage | Public co. (NASDAQ: MSFT); GA shipping | H | [4] |
| UX notes | Repositioned Copilot from chat to agent deployment/governance platform | M | [11] |
| **Google** — Recursion / org depth | Orchestration (generative + deterministic A2A delegation); no recursion | H | [6] |
| User-as-Chairman fit | No — centralized IT/human oversight ("human oversight at the center") | M | [6] |
| Interactive-OS surface | Gemini Enterprise app (employee delivery); no desktop OS | M | [6] |
| Per-agent security | Agent Identity (unique cryptographic ID), Agent Gateway policy enforcement, least-priv via auth policies | H | [6] |
| Verifier / anti-hallucination | Agent Anomaly Detection (LLM-as-a-judge), Model Armor (prompt-injection/leak), Threat Detection | H | [6] |
| Receipts / reversibility | Auditable trail per action mapped to authorization policies; Security Dashboard | H | [6] |
| Post-quantum (PQC) | None stated in launch | M | [6] |
| Local / cloud / hybrid | Cloud (Google Cloud / Vertex consolidated into Agent Platform) | H | [6] |
| Hardware | Cloud-only | H | [6] |
| Availability | GA 2026-04-22 (Google Cloud Next) | H | [6] |
| Pricing | Not disclosed at launch | L | [6] |
| Funding / stage | Public co. (NASDAQ: GOOGL); GA shipping | H | [6] |
| UX notes | Agent Registry single-source-of-truth; Agent Memory Bank for long-running agents | M | [6] |

### Cross-vendor verdict vs. the full-vision yardstick

| Yardstick axis | ServiceNow | Salesforce | Microsoft | Google | Our edge |
|---|---|---|---|---|---|
| Recursive org of agents | No (flat) | 2-tier | 2-tier | Orchestration | **Recursive exec→team→leaf** |
| Human-as-Chairman atop org | Oversight only | Oversight only | Oversight only | Oversight only | **True Chairman model** |
| Personal (not enterprise) | Enterprise-only | Enterprise-only | Enterprise-only | Enterprise-only | **Personal AI company** |
| Per-agent security | Strong | Strong | Strong | Strong | Parity (must match) |
| Dedicated verifier | Weak | Trust Layer | **Critique (strong)** | Anomaly/judge | **Verifier-by-default** |
| Receipts / audit | Strong | Strong | Strong | Strong | Parity (+ reversibility) |
| PQC | None | None | None | None | **PQC differentiator** |

## Sources

1. ServiceNow — "ServiceNow brings Autonomous Workforce to every major business function" (Newsroom press release) — newsroom.servicenow.com/press-releases/details/2026/ — dated 2026-05-05 — accessed 2026-06 (via search snippet; direct fetch 403).
2. Salesforce — "Agentforce 360 Announcements" / Agentforce platform + "8 Ways AI Agents Are Evolving in 2026" — salesforce.com/agentforce/what-is-new/ ; salesforce.com/blog/ai-agent-trends-2026/ — GA 2026-02-23 — accessed 2026-06 (via search snippet; direct fetch 403).
3. Fortune — "ServiceNow just unveiled an AI workforce that can run your entire company: 'Enterprises need AI that senses, decides, and securely acts'" — fortune.com/2026/05/05/servicenow-knowledge-2026-autonomous-workforce-microsoft-nvidia-ai-announcements/ — 2026-05-05 — accessed 2026-06 (via search snippet; direct fetch 403).
4. Microsoft — "Microsoft Agent 365, now generally available, expands capabilities and integrations" (Microsoft Security Blog) — microsoft.com/en-us/security/blog/2026/05/01/ — GA 2026-05-01, $15/user/mo or M365 E7 — accessed 2026-06 (WebFetch full text).
5. Fortune/diginomica — diginomica.com "ServiceNow Knowledge 2026 — AI Control Tower expands, Autonomous Workforce reaches every function" — 2026-05 — accessed 2026-06 (via search snippet; direct fetch 403).
6. Google Cloud — "Introducing Gemini Enterprise Agent Platform" (Google Cloud Blog) — cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-enterprise-agent-platform — 2026-04-22 — accessed 2026-06 (WebFetch full text).
7. Constellation Research — "ServiceNow Knowledge 2026: AI Control Tower, Action Fabric, Autonomous Workforce and more" — constellationr.com — 2026-05 — accessed 2026-06 (via search snippet; direct fetch 403).
8. ServiceNow — "ServiceNow expands AI Control Tower to discover, observe, govern, secure, and measure AI deployed across any system" (Newsroom) — newsroom.servicenow.com/press-releases/details/2026/ — 2026-05 — accessed 2026-06 (via search snippet).
9. Salesforce Ben / SalesforceDevops — "Salesforce Announces Agentforce 3: Command Center, MCP, and Apps" + Agentforce 3 multi-agent guides — salesforceben.com ; salesforcedevops.net — 2025-06-23 — accessed 2026-06 (via search snippet).
10. Microsoft — "What's new in Copilot Studio: Updates to multi-agent systems" (Copilot Blog) — microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/ — GA April 2026 — accessed 2026-06 (WebFetch full text).
11. Microsoft / TechTimes — "Microsoft Copilot Shifts to Agent Governance: Claude Checks GPT Work, Screen Agents Go Live" — techtimes.com — Critique announced 2026-03-30 — accessed 2026-06 (via search snippet; direct fetch 403).
12. The New Stack / Microsoft Mechanics — "Microsoft's Copilot makes Anthropic's Claude and OpenAI's GPT team up" / "Claude + GPT — Multi-model intelligence in Copilot" — thenewstack.io ; techcommunity.microsoft.com — DRACO 57.4 (+13.8%) — 2026-03/04 — accessed 2026-06 (via search snippet).
13. ServiceNow — "ServiceNow expands AI agent governance through deeper integration with Microsoft" (Newsroom) — newsroom.servicenow.com — 2026-05 — accessed 2026-06 (via search snippet).
14. ServiceNow / Efficiently Connected / ERP Today — AI Control Tower capability detail (identity verification, permission scoping, metering, audit, OAuth, 30 integrations, NIST/EU AI Act frameworks) — servicenow.com/products/ai-control-tower.html ; efficientlyconnected.com ; erp.today — 2026-05 — accessed 2026-06 (via search snippet).
15. Salesforce pricing pages / G2 / eesel — Agentforce Flex Credits (~$500/100k), $2/conversation, ~$5 PUPM add-on — salesforce.com/agentforce/pricing/ ; g2.com — 2026 — accessed 2026-06 (via search snippet).
