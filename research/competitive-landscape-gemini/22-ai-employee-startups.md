<!-- Follows _TEMPLATE.md shape. Multi-company pack: one sub-section per company, one combined facts table with a row-group per company. Doc 01 (matrix) and 43 (scorecard) parse the headers. -->

# AI-Employee Startup Layer (Relevance AI · Lindy · Artisan · 11x · Cognosys · Sierra · Cognition/Devin)

**One-liner:** The "hire an AI worker" startup layer — vendors that sell digital employees/agents-as-labour (sales, support, research, software) rather than tools, ranging from single task-bots to visual multi-agent "workforces." [synthesised]
**Axis:** B = AI company/workforce (background). These are the closest market analogues to our *recursive org of AI executives → teams → leaf employees*. Sierra/Devin also touch Infra (their "Agent OS" / VPC runtime). [synthesised]
**Category (3-meanings-of-OS):** Mostly **2 = AI-agent experience layer**; Relevance AI and Sierra explicitly brand an "operating system for agents" (meaning 2 + light 3); Devin Enterprise (VPC runtime) edges toward **3 = infra/kernel-for-agents**. [synthesised]
**Stage / availability:** All shipping commercially (Cognosys product sunset post-acquisition). · **As-of:** 2026-06

---

## What it does best · What it lacks · What we take

- **Best:**
  - Crisp "we sell *work*, not software" labour framing — buyers grasp an AI employee far faster than an agent-framework SDK (11x, Artisan, Relevance AI). [1][3][5]
  - Two of them (Relevance AI, Lindy) ship *team / society-of-agents* org models with manager→worker delegation and human-in-the-loop escalation — the nearest thing in-market to our org tree. [6][7]
  - Sierra and Devin show that **trust/reliability can be a paid product surface**: supervisory guardrail layers, encrypted/masked PII, VPC deployment, dedicated Trust Centers. [8][9][14]
  - Vertical depth: Devin writes ~90% of Cognition's own code; Sierra at $150M ARR; real, dog-fooded autonomy at the leaf-task level. [13]
- **Lacks (vs. full vision):**
  - **No Chairman model.** The human is an operator/admin or escalation target, never the apex of a standing AI org chart with executive layers beneath. [synthesised]
  - **Shallow recursion.** Best-in-class is 2-tier (manager→worker, Relevance AI/Lindy) or parallel clones (MultiDevin); none expose a *recursive executives→teams→leaf* hierarchy. [6][7][12]
  - **Perimeter, not per-agent, security.** SOC 2 / ISO 27001 / VPC are org-perimeter controls; no per-agent least-privilege identity, no receipts/reversibility as a first-class trust artefact, **zero post-quantum (PQC)** across all seven. [15][16]
  - **Enterprise-first, not personal.** Pricing ($150k+/yr Sierra; ~$2k–5k/mo Artisan; $500/mo Devin Team) targets companies, not an individual sovereign user. [10][11][17]
  - The 11x scandal shows the category's **trust deficit is real and unsolved** — inflated ARR, fake logos, churn hidden behind "contracted ARR." [4]
- **We take:**
  - The labour/"sell work" narrative + manager→worker delegation UX (maps to our `councils/` org tree and CEO→Chief→specialist→worker depth in `AGENTS.md §Architecture`). [user-knowledge]
  - Sierra's *supervisory guardrail layer* as design precedent for our verifier/anti-hallucination layer (`councils/evaluation/`, `councils/red-team/`). [8]
  - The 11x scandal as the market gap our TRUST wedge fills: receipts + verifier + auditable trail are exactly what would have caught inflated/fabricated claims. [4][user-knowledge]

## Deep dive

### Relevance AI — "AI workforce" / Workforce multi-agent builder
Sydney/SF no-code platform branding itself "the enterprise platform for agents you can trust at scale." Raised a **$24M Series B (≈A$37M) in May 2025, led by Bessemer**, with King River Capital, Insight Partners, Peak XV; total funding ≈$37M. [1][2] Public post-money valuation: unknown. [1] Reported >40,000 agents created on-platform in Jan 2025 alone. [1] The flagship **"Workforce"** is a visual canvas where you drag-and-drop specialist agents, define triggers, handoff rules, routing and escalation paths — explicitly a **multi-agent system (MAS) builder** with manager→worker org structures (e.g., a Team Manager + content-dev + optimisation + editor agents) and agent-to-agent feedback for QC. [6] Human stays "in control" via escalation, i.e. operator/supervisor, **not Chairman**. [6] Security is solid-perimeter: **SOC 2 Type II, GDPR, TLS 1.2+ in transit, AES-256 at rest**, no training on customer data, executive-only data visibility. [15] No PQC, no per-agent least-privilege identity disclosed. [15][16] Pricing: Free / Pro $19/mo / **Team $234/mo** (seat + credits, 84k actions/yr); unlimited agents — usage-metered on Actions + vendor model credits. [17] Cloud SaaS.

### Lindy — no-code "AI employees," societies of Lindies
No-code platform for building "Lindies" (AI employees) that hold cross-session context, make judgment calls, and **coordinate with other Lindies**. Marketed integration count varies by source — vendor materials cite **3,000–4,000+ integrations** (task brief said 1,600+; the higher figure is current). [task-brief][synthesised, from search] The standout org feature is **"Societies of Lindies"**: a manager Lindy (e.g., "Competitive Intel Manager") can *spawn one worker Lindy per item* (per competitor), and Lindies can duplicate themselves and coordinate with duplicates — a genuine **2-tier+ delegation / self-replicating** model, the closest in-market to recursive fan-out. [7] Still no human-as-Chairman atop a standing exec org; the user is the builder/admin. [7][synthesised] Pricing (self-serve, personal-friendly): **Free $0 (400 credits), Pro ~$49.99/mo, higher tiers to ~$199.99/mo** Max; voice billed separately ~$0.19/min. [task-brief][synthesised, from search — exact tier labels vary across third-party pages] Security posture: not surfaced in primary sources reviewed; treat SOC 2 status as **unknown**. Cloud SaaS. Funding: undisclosed/unknown in sources reviewed.

### Artisan — "Ava," the AI BDR
SF startup positioning "AI employees that replace repetitive work," lead product **Ava**, an autonomous AI BDR doing prospecting, messaging, meeting-booking at ~1/5 the cost of a human BDR. [3] Raised **$25M Series A, led by Glade Brook Capital** (HubSpot Ventures, Day One, BOND, Soma, Sequoia Scout). [3] Org model is **single-worker** (Ava) with a B2B data + email-warmup stack around her — not a team or org. [3][synthesised] Human is the operator approving/steering campaigns; **no Chairman**. [synthesised] Pricing is **sales-led, no public self-serve**: third-party estimates ~$2,000–5,000+/mo (annual contracts); also a **success/outcome-based model via Paid.ai** (pay per meeting). [11] Security: **ISO 27001 + PCI DSS** cited on its security page; SOC 2 specifics unknown. [18] No PQC, no per-agent security claims. Cloud SaaS, enterprise-leaning.

### 11x — "Alice" & "Jordan," digital workers ("we sell work")
London/SF, a16z-backed; "Digital workers, Human results." Workers: **Alice** (autonomous SDR, claimed up to 3× response rate) and **Jordan** (multilingual 24/7 phone rep, 30+ languages); 2025 plan to launch up to 20 agents across RevOps/CS/marketing. [5] **$50M Series B led by a16z (Nov 2024), ≈$320M valuation**; ~$74M total across 2024 rounds (a16z, Benchmark). [5][4] Org model: a **roster of single-purpose workers**, not a coordinated team-of-teams; human is operator. [5][synthesised] **Critical trust finding:** a Mar 2025 TechCrunch investigation alleged 11x **inflated ARR** (counting 3-month trials as annual "Contracted ARR"), **displayed customer logos of non-customers** (ZoomInfo publicly denied being a customer), with **75–90% churn at 3 months** and product hallucination/quality issues — dubbed AI's "Theranos moment." [4] 11x claims **SOC 2 Type II**, but compliance does not address the revenue/representation issues. [4] No PQC. Cloud SaaS, enterprise. *This is the category's cautionary tale and the strongest market validation of a TRUST/receipts wedge.* [4]

### Cognosys → Ottogrid → acquired by Cohere
Vancouver autonomous-agent / market-research assistant (founders Omar & Homam Malkawi / "Sully" Omarr). Bootstrapped: ~$660K revenue, **no VC**, ~$2M valuation, ~6 people. [search] **Rebranded Cognosys → Ottogrid in Oct 2024**, then **acquired by Cohere, announced May 16 2025**; standalone product to be **sunset**, smart-table tech folded into Cohere's enterprise "North." [19][search] Org model was **single personal agent** (scheduled research/briefings to email) — personal-productivity, not a team. [search] The most *personal-user-oriented* of the seven, but now effectively absorbed into enterprise infra. Security/PQC: unknown/not applicable post-sunset. Pricing (pre-sunset): from ~$15/mo with a free tier. [search]

### Sierra — Bret Taylor's customer-experience agents + "Agent OS"
Founded ~2023 by **Bret Taylor (OpenAI chair, ex-Salesforce co-CEO) + Clay Bavor**; builds enterprise **customer-experience AI agents**. Funding trajectory is the steepest in the set: **$350M at $10B (Sep 2025)** → **$950M at $15.8B post (May 2026, Tiger Global + GV)**; **$100M ARR at 21 months, ~$150M ARR by early 2026**. [20][21][22] Product is **"Agent OS"** — 7 modules: Agent Studio (no-code), Agent SDK, Insights, Voice, Live Assist (human copilot), Agent Data Platform (memory), and **Trust/Reliability**. [8] Trust is a *first-class product*: LLMs wrapped in **supervisory layers** + **deterministic guardrails** for critical business logic to cut hallucination/abuse; **PII auto-encrypted and masked**; topic/keyword filters; **SOC 2 Type II + GDPR**; dedicated **Trust Center (trust.sierra.ai)**. [8] Org model: a **supervised agent + supervisory agents** (1–2 tier), human as escalation/copilot via Live Assist — **not Chairman**. [8][synthesised] Pricing: **outcome-based per successful resolution, sales-led**; signals ~$150k/yr starting, $200k–350k+ Year-1 all-in; escalations usually not charged. [10] Cloud SaaS, enterprise-only. No PQC disclosed.

### Cognition / Devin — autonomous software engineer
Founded late 2023 (Scott Wu, Steven Hao, Walden Yan); **Devin**, an autonomous AI software engineer (plan→write→test→deploy). Explosive: ARR run-rate **$37M (May 2025) → ~$492M (mid-2026)**; **acquired Windsurf (Jul 2025)**, more than doubling ARR; **>90% of Cognition's own code written by Devin**. [13] Funding: **$400M at $10.2B (Sep 2025)** → **$1B+ Series D at ~$26B (May 2026, Lux/General Catalyst/8VC)**. [13] Org model: **MultiDevin** — multiple parallel Devins under a **coordinating "manager" Devin**, each with its own cloud IDE; Enterprise adds "Managed Devins in parallel," playbooks, knowledge base. [12] This is **2-tier (manager→parallel workers)** but homogeneous clones, not a heterogeneous exec org; human is the delegating eng-manager, **not Chairman**. [12][synthesised] Strongest enterprise security of the set: **SOC 2 Type II (since Sep 2024), VPC deployment (data stays in customer tenant), encryption in transit + at rest, MFA/need-to-know access, SAML SSO, Trust Center (trust.cognition.ai)**. [14] No PQC, no per-agent least-privilege identity beyond tenant isolation. [14][16] Pricing (most personal-accessible of the enterprise set): **Core $20/mo (PAYG, $2.25/ACU), Team $500/mo (250 ACUs, parallel sessions), Enterprise custom (VPC, SSO)**. [9][14] Hybrid: cloud SaaS + VPC.

### Cross-cutting yardstick read [synthesised]
Against the full vision — *recursive AI org with a human Chairman, per-agent security, verifier, receipts, PQC, personal-not-enterprise* — the entire layer clusters at **flat-to-2-tier org depth, operator (not Chairman) human role, perimeter (not per-agent) security, zero PQC, and enterprise (not personal) GTM**. Lindy ("Societies of Lindies," self-replicating, personal pricing) and Relevance AI ("Workforce" MAS canvas) are the closest org-model analogues; Sierra (supervisory guardrails as product) and Devin (VPC + dog-fooded autonomy) are the trust/runtime references. **No competitor occupies the Chairman + recursive-org + per-agent-trust + PQC + personal quadrant — that is open whitespace.**

## SWOT (with so-what-for-us)

- **Strengths:** The category has *proven the "AI employee" buyer narrative* and reached real scale (Sierra $150M ARR, Devin ~$492M run-rate). — *So-what:* validates demand for agents-as-labour; we inherit the framing without re-educating the market. [13][22]
- **Weaknesses:** Org depth caps at manager→worker / parallel clones; trust is perimeter SOC 2, not per-agent; 11x shows the trust deficit can be fraud-adjacent. — *So-what:* our recursive org + receipts/verifier/PQC is a genuine differentiator, not table stakes. [4][6][12]
- **Opportunities:** Nobody is building for the *individual sovereign user as Chairman*; Cognosys (the one personal player) got absorbed into enterprise infra. — *So-what:* personal-AI-OS + Chairman model is uncontested. [19][synthesised]
- **Threats:** Extremely well-capitalised incumbents (Sierra $15.8B, Cognition $26B) can move down-market or add org-depth/trust features fast. — *So-what:* speed + the trust wedge (PQC, receipts) must be defensible before they notice the gap. [13][22]

## Facts table

Each cell cited `[n]` or `unknown`. Confidence L/M/H. One row-group per company.

| Dimension | Value | Conf | Source |
|---|---|---|---|
| **RELEVANCE AI** | | | |
| Recursion / org depth | 2-tier MAS (manager→worker) on visual canvas; not recursive | H | [6] |
| User-as-Chairman fit | No — operator/supervisor via escalation | H | [6] |
| Interactive-OS surface | Chat + visual multi-agent canvas ("Workforce") | H | [6] |
| Per-agent security | Perimeter (SOC2 org-level); no per-agent least-priv disclosed | M | [15][16] |
| Verifier / anti-hallucination | Agent-to-agent feedback for QC; no dedicated verifier | M | [6] |
| Receipts / reversibility | Logs/monitoring on canvas; no auditable receipts product | L | [6] |
| Post-quantum (PQC) | None disclosed | M | [16] |
| Local / cloud / hybrid | Cloud SaaS | H | [15] |
| Hardware | Cloud-only | H | [15] |
| Availability | Shipping | H | [6] |
| Pricing | Free / Pro $19/mo / Team $234/mo (seat + usage credits) | H | [17] |
| Funding / stage | $24M Series B (May 2025, Bessemer); ~$37M total; valuation unknown | H | [1][2] |
| UX notes | Drag-drop agents, triggers, handoff/routing/escalation | H | [6] |
| **LINDY** | | | |
| Recursion / org depth | 2-tier+ "Societies of Lindies"; manager spawns workers; self-duplicating | H | [7] |
| User-as-Chairman fit | No — builder/admin | M | [7] |
| Interactive-OS surface | Chat + no-code agent builder | H | [7] |
| Per-agent security | Unknown (not in primary sources reviewed) | L | unknown |
| Verifier / anti-hallucination | None disclosed | L | unknown |
| Receipts / reversibility | None disclosed | L | unknown |
| Post-quantum (PQC) | None disclosed | M | [16] |
| Local / cloud / hybrid | Cloud SaaS | M | [7] |
| Hardware | Cloud-only | M | [7] |
| Availability | Shipping | H | [7] |
| Pricing | Free $0 / Pro ~$49.99 / up to ~$199.99/mo; voice ~$0.19/min extra | M | [synthesised, from search] |
| Funding / stage | Unknown in sources reviewed | L | unknown |
| UX notes | Cross-session memory; delegation via Agent trigger; 3,000–4,000+ integrations | M | [7] |
| **ARTISAN (Ava)** | | | |
| Recursion / org depth | Flat — single worker (Ava) + data/warmup stack | H | [3] |
| User-as-Chairman fit | No — operator steers campaigns | M | [synthesised] |
| Interactive-OS surface | Chat/dashboard (sales console) | M | [3] |
| Per-agent security | Perimeter (ISO 27001, PCI DSS); no per-agent claims | M | [18] |
| Verifier / anti-hallucination | None disclosed | L | unknown |
| Receipts / reversibility | None disclosed | L | unknown |
| Post-quantum (PQC) | None disclosed | M | [16][18] |
| Local / cloud / hybrid | Cloud SaaS | H | [3] |
| Hardware | Cloud-only | H | [3] |
| Availability | Shipping | H | [3] |
| Pricing | Sales-led; est. ~$2k–5k+/mo (annual); outcome-based option via Paid.ai | M | [11] |
| Funding / stage | $25M Series A (Glade Brook Capital) | H | [3] |
| UX notes | Ava automates prospecting/messaging/booking at ~1/5 human BDR cost | H | [3] |
| **11x (Alice/Jordan)** | | | |
| Recursion / org depth | Flat — roster of single-purpose workers | H | [5] |
| User-as-Chairman fit | No — operator | M | [synthesised] |
| Interactive-OS surface | Chat/dashboard | M | [5] |
| Per-agent security | Claims SOC2 Type II; perimeter only | M | [4] |
| Verifier / anti-hallucination | None; product accused of hallucination | M | [4] |
| Receipts / reversibility | None — trust scandal (inflated ARR, fake logos) | H | [4] |
| Post-quantum (PQC) | None disclosed | M | [16] |
| Local / cloud / hybrid | Cloud SaaS | H | [5] |
| Hardware | Cloud-only | H | [5] |
| Availability | Shipping | H | [5] |
| Pricing | Annual contracts; opt-out at 3 mo; exact list price unknown | L | [4] |
| Funding / stage | $50M Series B (a16z, Nov 2024) ≈$320M val; ~$74M total | H | [5][4] |
| UX notes | Alice (SDR), Jordan (multilingual phone, 30+ langs); 20 agents planned | H | [5] |
| **COGNOSYS → OTTOGRID** | | | |
| Recursion / org depth | Flat — single personal research agent | M | [search] |
| User-as-Chairman fit | No — personal-assistant model | M | [search] |
| Interactive-OS surface | Chat + scheduled email briefings | M | [search] |
| Per-agent security | Unknown | L | unknown |
| Verifier / anti-hallucination | None disclosed | L | unknown |
| Receipts / reversibility | None disclosed | L | unknown |
| Post-quantum (PQC) | None disclosed | L | unknown |
| Local / cloud / hybrid | Cloud SaaS | M | [search] |
| Hardware | Cloud-only | M | [search] |
| Availability | Acquired by Cohere May 2025; standalone product being sunset | H | [19] |
| Pricing | (Pre-sunset) from ~$15/mo + free tier | M | [search] |
| Funding / stage | Bootstrapped (~$660K rev, ~$2M val, ~6 ppl); acquired by Cohere | M | [19][search] |
| UX notes | Rebranded Cognosys→Ottogrid Oct 2024; tech folds into Cohere "North" | H | [19] |
| **SIERRA** | | | |
| Recursion / org depth | 1–2 tier — agent + supervisory agents | H | [8] |
| User-as-Chairman fit | No — escalation/copilot (Live Assist) | M | [8] |
| Interactive-OS surface | "Agent OS" (Studio, Voice, Live Assist) — enterprise console | H | [8] |
| Per-agent security | Supervisory layers + deterministic guardrails; PII encrypt/mask; SOC2 II, GDPR | H | [8] |
| Verifier / anti-hallucination | Dedicated — supervisory layers to cut hallucination | H | [8] |
| Receipts / reversibility | Insights/analytics + Trust Center; not user-facing receipts | M | [8] |
| Post-quantum (PQC) | None disclosed | M | [16] |
| Local / cloud / hybrid | Cloud SaaS | H | [8] |
| Hardware | Cloud-only | H | [8] |
| Availability | Shipping (enterprise) | H | [8] |
| Pricing | Outcome-based per resolution, sales-led; ~$150k/yr start, $200k–350k+ Y1 | M | [10] |
| Funding / stage | $950M at $15.8B (May 2026); prior $350M at $10B (Sep 2025); ~$150M ARR | H | [20][21][22] |
| UX notes | Ghostwriter builds guardrailed multilingual/multichannel agents | H | [8] |
| **COGNITION / DEVIN** | | | |
| Recursion / org depth | 2-tier — MultiDevin: manager Devin → parallel worker Devins (clones) | H | [12] |
| User-as-Chairman fit | No — delegating eng-manager | M | [12] |
| Interactive-OS surface | Per-Devin cloud IDE + sessions; eng console | H | [12] |
| Per-agent security | VPC tenant isolation, SOC2 II, MFA/need-to-know, SAML SSO, encryption | H | [14] |
| Verifier / anti-hallucination | Playbooks + test/CI workflows; no dedicated verifier product | M | [12][9] |
| Receipts / reversibility | PR workflows + session analysis; not user-facing receipts | M | [9][12] |
| Post-quantum (PQC) | None disclosed | M | [16] |
| Local / cloud / hybrid | Hybrid — cloud SaaS + VPC deployment | H | [14] |
| Hardware | Cloud / customer VPC | H | [14] |
| Availability | Shipping | H | [9] |
| Pricing | Core $20/mo (PAYG $2.25/ACU) · Team $500/mo (250 ACUs) · Enterprise custom | H | [9] |
| Funding / stage | $1B+ Series D at ~$26B (May 2026); prior $400M at $10.2B (Sep 2025) | H | [13] |
| UX notes | >90% of Cognition's own code by Devin; acquired Windsurf Jul 2025 | H | [13] |

## Sources

1. Relevance AI — "Raises $24M to Scale the AI Workforce" (blog; HTTP 403 on direct fetch, content via search index) — https://relevanceai.com/blog/the-ai-workforce-revolution-24m-series-b-to-accelerate-our-mission — accessed 2026-06.
2. The SaaS News — "Relevance AI Secures $24 Million in Series B" — https://www.thesaasnews.com/news/relevance-ai-secures-24-million-in-series-b — accessed 2026-06.
3. Artisan — "Artisan raises $25M Series A" — https://www.artisan.co/blog/artisan-series-a — accessed 2026-06.
4. AiSDR — "Lessons in Transparency: Inside the 11x.ai Controversy" (summarising Mar 2025 TechCrunch investigation) — https://aisdr.com/blog/11x-techcrunch/ — accessed 2026-06.
5. Maginative — "11x Raises $50M Series B led by a16z for AI 'Digital Workers'" (Nov 2024) — https://www.maginative.com/article/11x-raises-50m-series-b-led-by-a16z-for-ai-digital-workers/ — accessed 2026-06.
6. Relevance AI — "AI Workforce — Build and Manage Unified AI Agent Teams" / Multi-Agents System builder — https://relevanceai.com/workforce — accessed 2026-06.
7. Lindy — "Announcing a New Way to Create AI Employees" + Delegation 101 (Societies of Lindies) — https://www.lindy.ai/blog/announcing-a-new-way-to-create-ai-employees — accessed 2026-06.
8. Sierra — "Trust your agent" (Agent OS modules, supervisory layers, guardrails, SOC2 II, GDPR, PII masking) — https://sierra.ai/product/trust-and-reliability — accessed 2026-06.
9. Devin — Pricing (Core $20 / Team $500 / Enterprise; ACU model) — https://devin.ai/pricing/ — accessed 2026-06.
10. Sierra — "Outcome-based pricing for AI Agents" — https://sierra.ai/blog/outcome-based-pricing-for-ai-agents — accessed 2026-06.
11. Landbase — "Artisan AI Pricing 2026: Plans and Costs Breakdown" (3rd-party estimate; Paid.ai outcome model) — https://www.landbase.com/blog/artisan-ai-pricing — accessed 2026-06.
12. Devin / Cognition — "Devin 2.0" + Microsoft Azure customer story (MultiDevin, manager + parallel Devins, VPC) — https://cognition.ai/blog/devin-2 — accessed 2026-06.
13. TechCrunch — "AI coding startup Cognition raises $1B at $25B pre-money valuation" (May 2026; ARR, Windsurf, 90% own code) — https://techcrunch.com/2026/05/27/ai-coding-startup-cognition-raises-1b-at-25b-pre-money-valuation/ — accessed 2026-06.
14. Devin Docs — "Enterprise security" (SOC2 II since Sep 2024, VPC, encryption, MFA, SAML SSO, Trust Center) — https://docs.devin.ai/enterprise/security/enterprise-security — accessed 2026-06.
15. Relevance AI Documentation — "Security overview" (SOC2 II, GDPR, TLS 1.2+, AES-256, no training on customer data) — https://relevanceai.com/docs/admin/security — accessed 2026-06.
16. WebSearch (PQC + named vendors) — confirmed *no* PQC/post-quantum claims from Relevance AI, 11x, Sierra, Cognition — query run 2026-06 — accessed 2026-06.
17. Relevance AI — Pricing (Free / Pro $19 / Team $234, usage credits) — https://relevanceai.com/pricing — accessed 2026-06.
18. Artisan — "Security & Compliance" (ISO 27001, PCI DSS) — https://www.artisan.co/features/security — accessed 2026-06.
19. TechCrunch — "AI startup Cohere acquires Ottogrid, a platform for conducting market research" (May 16 2025; Cognosys→Ottogrid→Cohere, product sunset) — https://techcrunch.com/2025/05/16/ai-startup-cohere-acquires-ottogrid-a-platform-for-conducting-market-research/ — accessed 2026-06.
20. TechCrunch — "Bret Taylor's Sierra raises $350M at a $10B valuation" (Sep 2025) — https://techcrunch.com/2025/09/04/bret-taylors-sierra-raises-350m-at-a-10b-valuation/ — accessed 2026-06.
21. Tech Startups — "Sierra raises $950M at $15.8B valuation" (May 2026, Tiger Global + GV) — https://techstartups.com/2026/05/04/bret-taylors-ai-startup-sierra-raises-950m-at-15-8b-valuation/ — accessed 2026-06.
22. TechCrunch — "Bret Taylor's Sierra reaches $100M ARR in under two years" (Nov 2025; ~$150M ARR early 2026) — https://techcrunch.com/2025/11/21/bret-taylors-sierra-reaches-100m-arr-in-under-two-years/ — accessed 2026-06.
