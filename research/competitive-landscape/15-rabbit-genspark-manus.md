<!-- Doc 15 in the competitive-landscape pack. Three players, each using the shared _TEMPLATE.md shape, under one shared title. Combined facts tables at the end (one per player). -->

# Rabbit (r1 + LAM) · Genspark (Super Agent + Claw) · Manus (Butterfly Effect)

**Pack note:** Three players researched as of 2026-06. Genspark's Mixture-of-Agents cross-checking and Claw's isolated cloud directly overlap our TRUST/verifier wedge and are analysed closely below. All factual claims carry an inline `[n]` source, or a `[synthesised]`/`[hypothesis]`/`[user-knowledge]` tag; "unknown" where unverified. None of the three is known to ship post-quantum crypto, cryptographic receipts, or per-agent least-privilege security — confirmed absent across all sources searched, which is the core white space for our wedge `[synthesised]`.

---
---

# 1 · Rabbit (rabbit r1 · Large Action Model · rabbitOS 2 · creations · intern)

**One-liner:** A $199 pocket AI companion device whose "Large Action Model" operates apps on your behalf, now reframed around a software agent ("intern") and an on-device vibe-coding "creations" layer. [1][2][8]
**Axis:** A (AI-OS experience, foreground) — a literal handheld device + on-device agent UX; weak on B (workforce). [synthesised]
**Category (3-meanings-of-OS):** 1 real device OS (rabbitOS on r1 hardware) + 2 AI-agent experience layer (LAM/intern). [3][8]
**Stage / availability:** Shipping (hardware since Apr-2024; rabbitOS 2 since Sep-2025; intern since Jun-2025). · **As-of:** 2026-06 [2][8][9]

## What it does best · What it lacks · What we take

- **Best:**
  - Owns a real consumer hardware surface (the r1) at an aggressive $199 price — a tangible foreground device most agent players lack. [1][3]
  - LAM "learns by watching" UIs and then operates them like a human, plus Teach Mode to train your own task-specific "rabbits" — a genuine personalization-of-actions idea. [4][1]
  - rabbitOS 2 "creations" lets non-coders speak tools/games/apps into existence on-device (vibe-coding), powered by the "intern" general agent. [8][9]
- **Lacks:**
  - No recursive org / no Chairman model — it's a single assistant or flat one-off "rabbits," not an executive→team→employee hierarchy. [synthesised]
  - Trust posture is a liability, not a strength: a 2024 disclosure found hardcoded API keys (ElevenLabs/Azure/Yelp/Google Maps/SendGrid) in the codebase. No dedicated verifier, no PQC, no receipts. [5][6]
  - "Device is just an Android app" criticism — thin moat on the experience layer. [5]
- **We take:**
  - Teach Mode → maps to user-taught skills/policies for leaf employees (cf. our skill-teaching loop); adopt the "learn by watching, then replay with guardrails" pattern but gate it behind our verifier (`councils/audit/`). [synthesised]
  - Their security failure is the cautionary tale that justifies our per-agent least-privilege + receipts wedge. [synthesised]

## Deep dive

Rabbit Inc. was founded by Jesse Lyu (ex-Raven Tech, sold to Baidu 2017) in 2021; it raised ~$30M total including a $10M Series A led by Khosla Ventures [1]. The r1 launched at CES Jan-2024, priced $199 with no subscription, and drove ~$10M in preorders on the strength of its Teenage Engineering-designed hardware [1][3]. The pitch: a "Large Action Model" (LAM) that observes how humans use online interfaces and then operates them the same way, driven by natural language — positioned as the action counterpart to LLMs [4][2]. Independent analysis framed LAM as adjacent to RPA, and skeptics (and reverse-engineers) argued early r1 actions were largely scripted/web-automation rather than a novel neuro-symbolic model [4][5].

Trust/security posture is poor on the record: in Jun-2024 community reverse-engineering group "Rabbitude" disclosed hardcoded API keys embedded in the codebase, exposing keys for ElevenLabs (full privileges), Azure, Yelp, Google Maps and SendGrid — theoretically allowing reading of past responses, bricking devices, or altering all devices' responses; Rabbit said it acted on Jun-25 [5][6]. Critics also noted the device was essentially a single Android app [5]. There is no evidence of a dedicated verifier, cryptographic receipts/reversibility, or post-quantum crypto in any Rabbit material [synthesised].

The 2025 strategy pivot is notable: Rabbit launched "intern" (Jun-13-2025), a software-only general AI agent that turns a prompt into websites, reports, presentations, apps, and web actions (e.g., ordering from Amazon, booking reservations) — decoupling Rabbit's agent ambitions from the hardware [9][10]. Then rabbitOS 2 (Sep-8-2025) overhauled the r1 with a card-based UI, gesture/full-touchscreen support, and "creations" — on-device vibe-coding powered by intern, with a free library at rabbit.tech/creations [8][7]. intern pricing is ~$99.99/mo for 30 tasks (promo $69.99/mo annual) [9]. A "2026 edition" hardware refresh (refined scroll wheel, better battery) has been reported [comGateway/howtotechinfo, secondary — lower confidence]. Local/cloud: the device is a thin client; LAM/intern execution is cloud-side [synthesised].

Org/agent model: flat. A user has one assistant plus optionally several taught "rabbits"/creations — no executive hierarchy, no delegation tree, no Chairman seat [synthesised].

## SWOT (with so-what-for-us)

- **Strengths:** Real shipping device + brand recognition at low price — so-what: they own a foreground surface we don't; if we ever want hardware, r1 is the cautionary template. [1][3]
- **Weaknesses:** Headline security failure + "just an Android app" reputation — so-what: trust is their open flank; our entire wedge (per-agent security, receipts) is their gap. [5][6]
- **Opportunities:** "creations"/Teach Mode personalization could become a real skill ecosystem — so-what: validates user-taught leaf agents; we should do it but verified. [8][4]
- **Threats:** If intern matures into a reliable general agent independent of hardware, Rabbit becomes a cheap consumer on-ramp to agentic action — so-what: watch intern, not the device. [9]

---
---

# 2 · Genspark (Super Agent · Mixture-of-Agents · Claw · Call For Me)

**One-liner:** An "all-in-one AI workspace" / Super Agent that orchestrates 30+ models via a Mixture-of-Agents architecture (cross-checking GPT, Claude, Gemini to cut hallucinations), produces real deliverables, makes real phone calls, and now ships "Claw" — an autonomous "AI employee" on a dedicated isolated cloud computer. [genspark.ai][MoA blog][Claw launch] [11][12][13][14]
**Axis:** A + B hybrid — foreground workspace (A) plus an always-on autonomous worker (B); leans toward "one capable employee" rather than a recursive company. [synthesised]
**Category (3-meanings-of-OS):** 2 AI-agent experience layer + edges into 3 (orchestration kernel routing across models). [11][12]
**Stage / availability:** Shipping. Super Agent/workspace GA through 2025; Claw launched Mar-2026; Workspace 3.0 + ~$1.6B valuation Mar-2026. · **As-of:** 2026-06 [13][14][15]

## What it does best · What it lacks · What we take

- **Best:**
  - **Mixture-of-Agents cross-verification** — a central orchestrator routes subtasks to the best model and blends ChatGPT/Claude/Gemini with a reflection step; agents fact-check each other and flag conflicts instead of guessing. This is the closest commercial analog to our verifier wedge. [12][16]
  - Real deliverables + real telephony: produces slides/sheets/docs/video and places real calls ("Call For Me") for bookings/outreach. [11][13]
  - Claw: privacy-by-isolation — each user gets a dedicated cloud computer with its own IP, disk, and domain; data not mixed across accounts; 30+ preinstalled skills; ~$39.99/mo. [13][14]
  - Hyper-growth: $200M ARR, Series B extended to $385M, ~$1.6B valuation by Mar/Apr-2026. [14][15]
- **Lacks:**
  - MoA is **cross-model self-consistency**, NOT a dedicated independent verifier with its own least-privilege boundary or a separate trust authority — it's an ensemble inside the same vendor's loop. [synthesised, contrast 12]
  - No recursive org / no Chairman model — Claw is a single "AI employee," not a company of executives→teams. [synthesised]
  - No evidence of cryptographic receipts/reversibility or post-quantum crypto; "isolation" is perimeter/tenant isolation, not per-agent least-privilege capability tokens. [synthesised]
  - Cloud-only; trust ultimately rests on Genspark + the underlying frontier vendors. [synthesised]
- **We take:**
  - Their MoA cross-check is proof the verifier idea sells — but we differentiate: a *dedicated, independent* verifier agent with its own least-privilege scope + cryptographic receipts, not an in-loop ensemble. Map to `councils/audit/`. [synthesised]
  - "AI employee on an isolated cloud computer" validates per-employee sandboxing; we go further with per-agent capabilities + reversibility. [synthesised]

## Deep dive

Genspark (mainfunc.ai) was founded in 2023 by Jiakai Justin Liu, Eric Jing (CEO), Wen Sang and Ray Zhong [15]. Funding ramped fast: ~$100M Series A (Feb-2025, ~$530M valuation), then a $275M Series B (Nov-2025) at $1.25B making it a unicorn; reporting cites $500M+ ARR by Nov-2025 and a later $200M ARR figure with Series B extended to $385M at ~$1.6B by Mar/Apr-2026 (note: ARR figures vary by source and definition — flagged) [15][14]. 

The core architecture is **Mixture-of-Agents (MoA)**: a central orchestrator decomposes a task and routes each step to the most capable model, then runs a reflection/blend step over ChatGPT, Claude and Gemini, keeping the strongest parts of each [12][16]. The marketed benefit is anti-hallucination by cross-model verification — if Agent A asserts something Agent B can't corroborate from source, the system flags the discrepancy and attaches source attribution + confidence indicators rather than presenting a guess as fact [12][16]. **This directly overlaps our verifier wedge.** The crucial distinction for us: MoA is *self-consistency within one orchestrated loop run by one vendor* — it improves answer quality but is not an *independent* trust authority, has no separate security boundary, no least-privilege scoping, and no cryptographic receipt of what was checked. Our differentiation is a dedicated verifier that is organizationally and cryptographically separate, with reversibility [synthesised, contrast 12].

On the action/autonomy side, Genspark added "Call For Me" (real outbound phone calls via telephony integration) and, in Mar-2026, **Claw** — branded the "first AI employee": an autonomous agent on a dedicated, isolated cloud computer (own IP/disk/domain, no cross-account data mixing), with 30+ preinstalled skills, multi-platform messaging, and phone calls, at ~$39.99–80/mo [13][14]. SiliconANGLE framed Claw as a *secure managed alternative to open agent platforms (OpenClaw)* — i.e., security/managed-isolation is explicitly part of the pitch [siliconangle Claw][13]. However, the security claim is tenant/sandbox isolation; no source evidences per-agent least-privilege capabilities, cryptographic receipts, or PQC [synthesised].

Org/agent model: 2-tier at most — an orchestrator over specialist model-agents, and (with Claw) a single persistent worker. Not recursive; no Chairman-of-an-org framing [synthesised].

## SWOT (with so-what-for-us)

- **Strengths:** MoA cross-check + real deliverables + telephony + fast revenue — so-what: they've productized "trust via cross-checking" and the market is paying; validates our thesis but raises the bar on messaging. [12][14]
- **Weaknesses:** Verification is in-loop ensemble, not an independent verifier; isolation is perimeter not per-agent; no receipts/PQC — so-what: precise white space for us to claim "real, independent, cryptographic trust." [synthesised]
- **Opportunities:** Claw "AI employee" could grow into a small team of workers — so-what: if they add hierarchy, they move toward our turf; monitor for org/recursion features. [13]
- **Threats:** Best-funded, fastest-moving direct overlap on the verifier story; could co-opt "trust" language before we ship — so-what: our defensibility must be the *independent + cryptographic + reversible* parts they don't have. [14][12]

---
---

# 3 · Manus (Butterfly Effect — general autonomous agent)

**One-liner:** A general autonomous AI agent that runs 30–50 step tasks in fully isolated per-task cloud VMs, delegating reasoning to a frontier model (Claude Sonnet) with a planner→specialist-subagent architecture; built by Butterfly Effect (China→Singapore). [Manus blog][zenml][datacamp] [17][18][19]
**Axis:** B (autonomous workforce / one capable general worker) with a chat foreground (A). [synthesised]
**Category (3-meanings-of-OS):** 2 AI-agent experience layer + 3 (per-task cloud-VM execution kernel). [17][18]
**Stage / availability:** Shipping (invite beta Mar-6-2025; GA later 2025). Ownership in flux: Meta acquisition (Dec-2025) blocked/ordered unwound by China's NDRC (Apr-27-2026); founders weighing ~$1B buy-back (May-2026). · **As-of:** 2026-06 [20][21][22][23]

## What it does best · What it lacks · What we take

- **Best:**
  - **Per-task isolated cloud VMs** — every task gets a fully isolated VM (networking, FS, browser, dev tools); network isolation prevents cross-task leakage; sandboxes destroyed after completion (no data residue). Strong execution-isolation primitive. [18][19]
  - Planner-driven multi-agent: a central planner builds a plan tree; a scheduler farms steps to specialist sub-agents (browser/code/file/validation). Closest of the three to a delegated work structure. [18]
  - Pragmatic model strategy: delegate intelligence to the frontier model (Claude Sonnet 3.5→4), tiered model selection (light models for simple steps) cutting tokens. [17][19]
  - Commercial traction: claimed ~$100M ARR in ~8 months; $75M Series B (Benchmark-led, Apr-2025) at ~$500M valuation. [18][22][21]
- **Lacks:**
  - 2-tier delegation, not recursive-to-arbitrary-depth, and no persistent Chairman-of-a-standing-org model — tasks spin up, run, and tear down. [synthesised]
  - Has a "validation" sub-agent but not an *independent* dedicated verifier outside the same loop; no cryptographic receipts/reversibility; no PQC evidenced. [synthesised, vs 18]
  - Ownership/geopolitical risk: the Meta deal was blocked and ordered unwound; future control is uncertain. [20][23]
- **We take:**
  - The **per-task isolated, ephemeral, self-destructing sandbox** is the single best primitive to adopt for leaf one-task employees — pair it with our receipts so teardown still leaves an auditable trail. Map to `councils/audit/` + sandbox layer. [18]
  - Planner→specialist scheduler is a clean reference for executive→team dispatch. [18]

## Deep dive

Manus ("hand" in Latin) is built by Butterfly Effect, founded by Xiao Hong, Ji Yichao (Zhang Tao among founders) in Beijing in 2022, later relocated to Singapore; its earlier product is the Monica AI browser extension [20][22][23]. Manus launched invite-only beta Mar-6-2025 and went viral; the company claimed ~$100M annualized revenue within ~8 months and a >$125M run rate [20][18]. Funding: a $75M round led by Benchmark in Apr-2025 at ~$500M valuation [21][22]. ByteDance had reportedly offered ~$30M in 2024, declined [20].

Architecture (well-documented by the team and analysts): Manus keeps a "very simple but robust" core with zero predefined workflows, delegating intelligence to the foundation model — initially Claude Sonnet 3.5, later Claude 4 — because only sufficiently capable models could sustain its 30–50-step agentic loops [17][19]. It is a planner-driven multi-agent system: a central planning agent produces a plan tree; a scheduler dispatches steps to specialist sub-agents (browser, code, file, validation) [18]. Each task gets a *fully isolated cloud virtual machine* with a full dev environment; network isolation prevents cross-task data leakage; sandboxes are destroyed immediately after completion to eliminate residue; dormant sandboxes recycle after 7 days (free) / 21 days (Pro) [18][19]. Dynamic/tiered model selection routes simple queries to light models (e.g., Llama 3) and reserves Claude for hard reasoning, cutting tokens to ~1/3 of industry averages [19]. Pricing has been credit-based, ~$39–$200/mo [19].

Trust posture: the execution *isolation* is genuinely strong (ephemeral per-task VMs, network isolation, post-task destruction) and is the most security-relevant primitive of the three [18][19]. But there is a "validation" sub-agent inside the same loop rather than an independent verifier; no source evidences cryptographic receipts, reversibility, or post-quantum crypto [synthesised].

Ownership/status (verify — confirmed in flux): Meta announced acquisition of Manus/Butterfly Effect ~Dec-30-2025 for ~$2B (reports range $2–3B; ~4–6x the Apr-2025 valuation) and integrated operations [20][24]. China's NDRC then launched a review (export-control compliance review Jan-2026) and on Apr-27-2026 prohibited foreign investment and ordered the parties to withdraw/unwind the transaction [21][20]. As of May-2026, the three founders were reportedly weighing raising ~$1B from external investors to buy Manus back (at ≥ the $2B Meta price), possibly forming a JV and a Hong Kong IPO — though it's unclear how the agentic tech, already integrated into Meta, would be carved out [22]. **Net: "reportedly acquired" is true but the acquisition was blocked and is being unwound — current ownership is contested/uncertain as of 2026-06.** [20][22][23]

Org/agent model: 2-tier (planner → specialist sub-agents) per task; ephemeral, not a standing recursive company; no Chairman seat [synthesised].

## SWOT (with so-what-for-us)

- **Strengths:** Best-in-class execution isolation + clean planner/scheduler delegation + real revenue — so-what: the sandbox primitive is directly adoptable for our leaf employees. [18][19]
- **Weaknesses:** In-loop validation not independent verifier; no receipts/PQC; ownership uncertainty — so-what: even the most "autonomous" player lacks our trust layer; geopolitics adds product risk. [synthesised][20]
- **Opportunities:** If founders regain independence + raise $1B, Manus could re-accelerate as a neutral player — so-what: a re-independent Manus is a live competitor to watch on the B axis. [22]
- **Threats:** Whoever ends up owning the tech (Meta or re-independent Manus) has the strongest autonomous-agent execution stack — so-what: we must not compete on raw autonomy; compete on trust/verifiability/recursion. [synthesised]

---
---

## Combined Facts tables (one per player)

Each cell cited `[n]` or `unknown`. Confidence L/M/H.

### Rabbit (r1 / LAM / rabbitOS 2 / intern)

| Dimension | Value | Conf | Source |
|---|---|---|---|
| Recursion / org depth | Flat — single assistant + optional taught "rabbits"/creations; no hierarchy | M | [synthesised][8][4] |
| User-as-Chairman fit | Low — user is a device owner, not atop an org | M | [synthesised] |
| Interactive-OS surface | Device OS (rabbitOS on r1) + chat/voice; card UI in OS 2 | H | [3][8] |
| Per-agent security | None evidenced; notable failure (hardcoded API keys, 2024) | H | [5][6] |
| Verifier / anti-hallucination | None dedicated | M | [synthesised] |
| Receipts / reversibility | None evidenced | M | [synthesised] |
| Post-quantum (PQC) | None evidenced | M | [synthesised] |
| Local / cloud / hybrid | Hybrid — thin device client, cloud LAM/intern execution | M | [synthesised][4] |
| Hardware | Own device (r1, $199; "2026 edition" refresh reported) | H | [1][3] |
| Availability | Shipping (HW Apr-2024; OS 2 Sep-8-2025; intern Jun-13-2025) | H | [8][9] |
| Pricing | r1 $199 no-sub; intern ~$99.99/mo (30 tasks), promo $69.99/mo annual | H | [1][9] |
| Funding / stage | ~$30M total ($10M Series A, Khosla); founder Jesse Lyu | M | [1] |
| UX notes | Card-based OS 2, gestures, on-device vibe-coding "creations"; "just an Android app" critique | M | [8][5] |

### Genspark (Super Agent / Mixture-of-Agents / Claw)

| Dimension | Value | Conf | Source |
|---|---|---|---|
| Recursion / org depth | 2-tier — orchestrator over model-agents; Claw = single "AI employee" | M | [synthesised][12][13] |
| User-as-Chairman fit | Low–Med — you delegate to one worker/orchestrator, not an org | M | [synthesised] |
| Interactive-OS surface | Chat/workspace (foreground "AI workspace") + autonomous Claw | H | [11][13] |
| Per-agent security | Perimeter/tenant isolation (Claw: own IP/disk/domain, no data mixing); not per-agent least-priv | M | [13][14] |
| Verifier / anti-hallucination | **Mixture-of-Agents cross-model verification + reflection** (in-loop ensemble, not independent) | H | [12][16] |
| Receipts / reversibility | Source attribution + confidence indicators; no cryptographic receipts/reversibility evidenced | M | [12][synthesised] |
| Post-quantum (PQC) | None evidenced | M | [synthesised] |
| Local / cloud / hybrid | Cloud-only | H | [13] |
| Hardware | Cloud-only (no own device) | H | [13] |
| Availability | Shipping; Claw launched Mar-2026; Workspace 3.0 Mar-2026 | H | [13][14] |
| Pricing | Workspace tiers (~$24.99/mo cited); Claw ~$39.99–80/mo | M | [Scribe review][13][14] |
| Funding / stage | $100M Series A (Feb-2025, ~$530M); $275M Series B (Nov-2025, $1.25B); ext. to $385M, ~$1.6B (Mar/Apr-2026); ARR figures vary ($200M–$500M) | M | [15][14] |
| UX notes | "Describe it, get a finished deliverable" + real phone calls (Call For Me); 30+ skills in Claw | H | [11][13] |

### Manus (Butterfly Effect)

| Dimension | Value | Conf | Source |
|---|---|---|---|
| Recursion / org depth | 2-tier per task — planner → specialist sub-agents (browser/code/file/validation) | H | [18] |
| User-as-Chairman fit | Low–Med — you brief a general agent; ephemeral, no standing org | M | [synthesised][18] |
| Interactive-OS surface | Chat foreground + visible task execution; no device OS | M | [18][19] |
| Per-agent security | Strong execution isolation: per-task isolated cloud VM, network-isolated, destroyed after task | H | [18][19] |
| Verifier / anti-hallucination | In-loop "validation" sub-agent; not an independent verifier | M | [18][synthesised] |
| Receipts / reversibility | None evidenced (sandboxes destroyed; no cryptographic trail) | M | [synthesised][18] |
| Post-quantum (PQC) | None evidenced | M | [synthesised] |
| Local / cloud / hybrid | Cloud (per-task VMs) | H | [18][19] |
| Hardware | Cloud-only | H | [18] |
| Availability | Shipping (invite beta Mar-6-2025; GA later 2025); ownership in flux | H | [20][22] |
| Pricing | Credit-based ~$39–$200/mo | M | [19] |
| Funding / stage | $75M Series B (Benchmark, Apr-2025, ~$500M); ~$100M ARR claimed; Meta deal ~$2B (Dec-2025) **blocked/unwound Apr-2026**; founders weigh ~$1B buy-back (May-2026) | H | [21][20][22] |
| UX notes | General autonomous agent; delegates reasoning to Claude Sonnet/4; tiered model routing; "wide research" | H | [17][19] |

---

## Sources

1. The Rabbit R1 drove $10M in preorders thanks to great design — fastcompany.com/91013196 — accessed 2026-06.
2. introducing r1, a pocket companion that moves AI from words to action — rabbit.tech/newsroom/introducing-r1 — accessed 2026-06 (403 to fetcher; corroborated via search).
3. Rabbit r1 — en.wikipedia.org/wiki/Rabbit_r1 — accessed 2026-06.
4. How Rabbit's Large Action Models tease the future of RPA — diginomica.com/how-rabbits-large-action-models-tease-future-rpa — accessed 2026-06.
5. Critical Rabbit R1 security flaw leaves user data at risk — cybernews.com/security/critical-rabbit-r1-security-flaw — accessed 2026-06.
6. Updates on investigation on r1 SaaS API keys — rabbit.tech/security-investigation-062524 — 2024-06-25, accessed 2026-06.
7. rabbitOS 2.0 Released for R1 with New Card UI and App Creations — androidsage.com (2025-09-09) — accessed 2026-06.
8. rabbit overhauls r1 experience with rabbitOS 2 — businesswire.com/news/home/20250904568217 (2025-09-04) — accessed 2026-06.
9. rabbit officially launches its second product – rabbit intern — rabbit.tech/newsroom/rabbit-intern-launch (2025-06-13) — accessed 2026-06.
10. Rabbit launches "intern," a software AI agent for team-level projects — the-decoder.com (2025-06) — accessed 2026-06.
11. Genspark — Your All-in-One AI Workspace — genspark.ai — accessed 2026-06.
12. Major Upgrade on Genspark Search: Mixture-of-Agents Powered Most Trustworthy AI Search — mainfunc.ai/blog/genspark_moa_powered_search — accessed 2026-06.
13. Genspark launches Claw AI assistant as secure alternative to open agent platforms (OpenClaw) — siliconangle.com (2026-03-12) — accessed 2026-06.
14. Genspark Claw Launches as Genspark's First "AI Employee," Workspace 3.0, $200M ARR, Series B to $385M, ~$1.6B valuation — finance.yahoo.com (2026, Business Wire) — accessed 2026-06.
15. Genspark Secures $275M Series B at $1.25B Valuation — pandaily.com (2025-11) / siliconangle.com (2025-11-20) — accessed 2026-06.
16. Genspark AI features (Mixture-of-Agents cross-verification) — lindy.ai/blog/genspark-ai-features (2026) — accessed 2026-06.
17. Context Engineering for AI Agents: Lessons from Building Manus — manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus — accessed 2026-06 (403 to fetcher; corroborated via search/zenml).
18. Manus: Building an AI Agent Platform with Cloud-Based Virtual Machines — zenml.io/llmops-database/... — accessed 2026-06.
19. Manus AI: Features, Architecture, Access, Early Issues — datacamp.com/blog/manus-ai — accessed 2026-06.
20. Meta acquires Singapore AI agent firm Manus (Butterfly Effect) — cnbc.com/2025/12/30/meta-acquires-singapore-ai-agent-firm-manus... (2025-12-30) — accessed 2026-06.
21. China blocks Meta's $2B Manus deal after months-long probe — techcrunch.com/2026/04/27/china-vetoes-metas-2b-manus-deal... (2026-04-27) — accessed 2026-06.
22. Manus Weighs Raising $1 Billion to Unwind Meta Takeover — bloomberg.com (2026-05-21) — accessed 2026-06.
23. China Unwinds Meta's Acquisition of Manus: Implications — omm.com/insights/... (2026) — accessed 2026-06.
24. Meta buys Manus for $2 billion — techradar.com/pro/meta-buys-manus... (2026) — accessed 2026-06.
