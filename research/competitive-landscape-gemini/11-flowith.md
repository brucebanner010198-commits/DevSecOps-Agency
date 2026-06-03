<!-- Shared shape for every player doc in this pack. Doc 01 (matrix) and 43 (scorecard) parse by these headers — headers are normative, not suggestive. -->

# Flowith / FlowithOS

**One-liner:** An infinite-canvas agentic workspace whose "Infinite Agent" Neo runs long-horizon (1,000+ step) cloud tasks against a personal "Knowledge Garden," now extended into FlowithOS — a desktop/browser-controlling "operating system for AI agents." [1][6][9]
**Axis:** A = AI-OS experience (foreground) — a visual canvas + agent surface, with a nascent OS-control layer; not an AI company/workforce. [synthesised]
**Category (3-meanings-of-OS):** 2 AI-agent experience layer (markets itself as "OS for agents," but it is an app/agent layer, not a real device OS or a kernel-for-agents). [synthesised]
**Stage / availability:** Shipping — web app, iOS app, and a public FlowithOS desktop app (macOS + Windows); seed/seed+ funded. [12][13] · **As-of:** 2026-06

---

## What it does best · What it lacks · What we take

- **Best:** Long-horizon autonomous execution — Neo is marketed as the "world's first infinite agent," a 10M-token-context, 1,000+ inference-step cloud agent that self-corrects via a "Dynamic Recipe" loop rather than a rigid upfront plan. [1][6][9]
- **Best:** Spatial, multi-threaded UX — an infinite 2D canvas where the same prompt fans out across GPT-4o/Claude/Gemini side-by-side, beyond linear chat. [3][6]
- **Best:** Personal grounding via the Knowledge Garden — uploaded docs become semantically linked "Seeds" the agent retrieves from, framed as reducing hallucination on the user's own corpus. [3][6]
- **Best:** Aggressive web-agent benchmark marketing (self-reported 92.8% on the "hardest level" of Online-Mind2Web vs. ChatGPT Atlas's 75.7%), which has driven attention. [4][7] — but see "Lacks" re: independent verification.
- **Lacks:** No recursive AI-company / org model — there is no Chairman-atop-executives-atop-teams structure; Neo is a single powerful agent (plus an "Oracle" scheduler/sub-task splitter), i.e. flat-to-shallow, not a deep org. [6][synthesised]
- **Lacks:** Trust layer is essentially absent vs. our wedge — no dedicated verifier, no per-agent least-privilege security, no published receipts/reversibility model, and no post-quantum-crypto claim found anywhere. [synthesised][hypothesis]
- **Lacks:** Cloud-only / consumer-creator posture — built for solo creators and small agencies, not personal-sovereign or enterprise-grade isolation; benchmark claims are self-published and not reproduced on independent leaderboards (HAL/Princeton, osunlp HF, Steel.dev), which show different leaders. [8][11][synthesised]
- **We take:** The "Knowledge Garden as anti-hallucination grounding" framing maps to our memory/verifier story — personal corpus retrieval as a trust primitive (cf. `councils/audit/`). [synthesised]
- **We take:** The "Dynamic Recipe" self-correcting loop is a useful pattern for a leaf one-task employee that retries with a different approach on tool failure. [synthesised]
- **We take:** Their benchmark-as-marketing move is a cautionary lesson — a dedicated verifier + reproducible receipts is exactly the differentiator they lack. [synthesised]

## Deep dive

**What it is.** Flowith began as an infinite-canvas AI workspace ("Flow mode") for visual, non-linear ideation where a user can run one prompt through multiple models simultaneously and branch threads spatially. [3][6] It layers three named systems on top: **Agent Neo** (the autonomous executor), the **Knowledge Garden** (a personal RAG store of "Seeds"), and **Oracle** (a scheduler that decomposes complex goals into subtasks and selects tools). [6] In October 2025 the company introduced **FlowithOS**, marketed as "the world's first operating system natively built for AI Agents," which extends Neo to control browsers and desktop software for end-to-end task completion; a public FlowithOS desktop app for macOS and Windows followed. [9][12][13]

**Agent model / "recursion."** The architecture is best described as flat-to-shallow, not recursive-org. Neo is a single long-horizon agent with a 10M-token context window claimed to support 1,000+ inference steps, working for "hours, days, or weeks." [1][6][9] Oracle adds one layer of task decomposition/tool routing above Neo, and TechPilot/marketing describe "multiple AI agents that run 24/7," implying parallel Neo instances — but there is no Chairman→executives→teams→leaf-employee hierarchy, no notion of the human sitting atop a recursive company of AI managers. [2][6][synthesised] The user remains an operator of an agent, not a board chairman over an org. [synthesised]

**UX / foreground.** The interactive surface is the infinite 2D canvas plus an agent panel — visual, multi-threaded, model-comparison-friendly. [3][6] FlowithOS adds a desktop/browser-control surface (a streamed/automated environment that drives real software). [9] This is genuinely a "foreground AI experience," but it is an app layer, not a device OS. [synthesised]

**Trust / security posture.** This is the thinnest area relative to our wedge. I found a privacy policy at try.flowith.io/privacy (not fetchable — 403) but no public, specific claims of per-agent least-privilege security, a dedicated verifier/anti-hallucination component, auditable receipts/reversibility, SOC2, or post-quantum cryptography. [synthesised] The Knowledge Garden is positioned as an anti-hallucination *grounding* mechanism (retrieve real snippets vs. generate generic text), which is a verification-adjacent idea but not a dedicated verifier agent. [3][6] FlowithOS's desktop/browser control implies a cloud-sandbox/VM execution model typical of web agents, but I found no published isolation/attestation architecture — treat security as **unknown/weak**. [hypothesis]

**Benchmarks — handle with care.** Flowith's headline marketing claim is that FlowithOS scored **92.8% on the "hardest level" of Online-Mind2Web vs. ChatGPT Atlas's 75.7%**, with some secondary write-ups also citing a **97.7%** figure (conflicting numbers across sources suggest different subsets/judges). [4][7] Agent Neo is separately claimed to "lead the GAIA benchmark." [1] Critically, these are **self-reported**: independent Online-Mind2Web leaderboards (HAL/Princeton, osunlp HuggingFace, Steel.dev, last updated Apr 2026) do **not** list FlowithOS among ranked entries and show different leaders (e.g., Browser Use Cloud ~97%, with explicit caveats that several vendor scores can't be independently verified because judges/harnesses aren't published). [8][11][synthesised] Confidence in the *claim existing* is High; confidence in the *number being independently true* is Low.

**Who's behind it / funding.** Founded 2023 by Derek Nee (CEO) and Yichen Wu (co-founder/COO), reportedly a small team (~10) out of China, now associated with a San Francisco presence. [6][10] Flowith closed combined **Seed and Seed+ rounds totaling "tens of millions" of USD**, announced ~March (2026 per most sources), with the Seed round led by Vertex Ventures and the Seed+ co-led by Sequoia China Seed Fund and LongRiver Investments (Miracleplus also listed). [10][14] Agent Neo launched May 2025 and the product is reported to have grown to over half a million users. [9][6] (A Crunchbase-style ~$5.8M "estimated valuation" appears in one aggregator but conflicts with the "tens of millions raised" figure and is likely an algorithmic estimate — treat as unreliable.) [10][synthesised]

**Pricing.** Sources disagree on exact numbers and tier names (consistent with rapid iteration / annual-vs-monthly framing). The consistent shape is a four-tier consumer ladder plus enterprise: a free **Starter** (~300–1,000 one-time credits, basic models, Composer + Neo); **Professional** (~$15.32–$19.90/mo, ~20–22k monthly credits); **Ultimate** (~$34.93–$49.90/mo, ~50–85k credits); and **Infinite** (~$249.95–$499.90/mo, ~500k–1M credits, founder access); Enterprise is custom. [6][16] Credit-metered, monthly refresh, unused credits expire. [16]

## SWOT (with so-what-for-us)

- **Strengths:** Polished foreground UX (infinite canvas) + a genuinely long-horizon agent and personal RAG, all shipping with VC backing. — *So-what:* they have a credible foreground experience and personal-grounding story we must match or beat; our edge has to be the trust layer they skip.
- **Weaknesses:** No org/company model, no trust/verifier/receipts layer, security posture undisclosed, and benchmark claims are self-reported and not independently reproduced. — *So-what:* our entire wedge (verifier, per-agent security, receipts, PQC, recursive org) is open territory against them.
- **Opportunities:** Their "OS for agents" branding is grabbing the "AI OS" mindshare we want; their Knowledge Garden normalizes personal-corpus grounding for users. — *So-what:* market is being educated for us; we can position as "the *trustable* agent OS" against their unverifiable claims.
- **Threats:** Fast iteration, strong-tier VC (Sequoia/Vertex), big user growth, aggressive benchmark PR, and a desktop app already controlling real software. — *So-what:* they could add light auditing/security and partially close the gap; we need the trust story to be deep and demonstrable, not bolt-on.

## Facts table

Each cell cited `[n]` or `unknown`. Confidence L/M/H.

| Dimension | Value | Conf | Source |
|---|---|---|---|
| Recursion / org depth (flat · 2-tier · deep/recursive) | Flat-to-2-tier (Oracle decomposes → Neo executes; parallel Neo instances). Not recursive. | M | [6][2] |
| User-as-Chairman fit (does the human sit atop an org?) | No — user operates a single powerful agent, not a board over an AI org. | M | [6][synthesised] |
| Interactive-OS surface (none · chat · desktop/OS · streamed) | Desktop/OS-style: infinite 2D canvas + FlowithOS desktop app controlling browser/desktop software. | H | [3][9][12] |
| Per-agent security (none · perimeter · per-agent least-priv) | None published / unknown. | L | unknown [synthesised] |
| Verifier / anti-hallucination (none · gestures · dedicated) | Gestures — Knowledge Garden grounding reduces hallucination on user corpus; no dedicated verifier. | M | [3][6] |
| Receipts / reversibility (none · logs · auditable trail) | None published / unknown. | L | unknown [synthesised] |
| Post-quantum (PQC) (none · stated · shipped) | None found. | L | unknown [synthesised] |
| Local / cloud / hybrid | Cloud (agents run 24/7 in the cloud); desktop app is a control client, not local inference. | M | [1][9][12] |
| Hardware (cloud-only · existing HW · own device) | Cloud-only; runs on existing HW (web, iOS, macOS/Windows app). No own device. | H | [9][12][15] |
| Availability | Shipping: web, iOS app, public FlowithOS desktop (macOS + Windows). | H | [12][13][15] |
| Pricing | Free Starter; Pro ~$15.32–$19.90/mo; Ultimate ~$34.93–$49.90/mo; Infinite ~$249.95–$499.90/mo; Enterprise custom. Credit-metered. (Sources vary.) | M | [6][16] |
| Funding / stage | Seed + Seed+ totaling "tens of millions" USD; Vertex Ventures (Seed), Sequoia China Seed + LongRiver (Seed+); founded 2023, Derek Nee + Yichen Wu. | M | [10][14] |
| UX notes | Infinite canvas, multi-model side-by-side, branchable threads; Knowledge Garden "Seeds"; "Dynamic Recipe" self-correcting agent loop. | H | [3][6] |

## Sources

1. Agent Neo — Flowith (official tool page) — https://flowith.io/tools/agent-neo/ — accessed 2026-06 (via search excerpts; site returns 403 to fetcher).
2. Flowith NEO: Multiple AI Agents that run 24/7 — Tech Pilot — https://techpilot.ai/tools/flowith-neo-ai-agent/ — accessed 2026-06.
3. Flowith Canvas / Knowledge Garden overview — completeaitraining.com & search excerpts — https://completeaitraining.com/ai-tools/flowith-canvas/ — accessed 2026-06.
4. FlowithOS vs ChatGPT Atlas (Online-Mind2Web 92.8% vs 75.7% claim) — Skywork — https://skywork.ai/blog/ai-agent/function/flowith-os-vs-chatgpt-atlas/ — accessed 2026-06.
5. Online-Mind2Web Benchmark (definition: 300 tasks / 136 sites) — arXiv 2504.01382 "An Illusion of Progress? Assessing the Current State of Web Agents" — https://arxiv.org/html/2504.01382v4 — accessed 2026-06.
6. Flowith review (features, pricing, founders, Dynamic Recipe, 10M ctx, 1,000+ steps) — GitHub mirror "lphwrdz/flowith" + fahimai/max-productive excerpts — https://github.com/lphwrdz/flowith — accessed 2026-06.
7. Introducing FlowithOS: A Visual, Agent-Powered OS for Real Work (and 97.7% figure) — Skywork — https://skywork.ai/blog/ai-agent/function/introducing-flowithos-a-visual-agentpowered-os-for-real-work/ — accessed 2026-06.
8. Online-Mind2Web Leaderboard (independent; updated Apr 16 2026; Browser Use ~97%; FlowithOS not listed) — Steel.dev — https://leaderboard.steel.dev/leaderboards/online-mind2web/ — accessed 2026-06.
9. FlowithOS launch (Oct 2025), "world's first OS for agents," controls browser/desktop, >500k users — Skywork deep dive — https://skywork.ai/skypage/en/flowithos-agentic-os-ai-workflows/1983347044656451584 — accessed 2026-06.
10. Flowith funding: Seed + Seed+ "tens of millions," Vertex/Sequoia China/LongRiver; founders; SF — AI Market Watch + Tracxn/PitchBook excerpts — https://www.ai-market-watch.com/news/ai-creation-platform-flowith-raises-tens-of-millions-in-seed-funding-yd27si — accessed 2026-06.
11. Online-Mind2Web independent leaderboards (HAL/Princeton; osunlp HuggingFace) — https://hal.cs.princeton.edu/online_mind2web ; https://huggingface.co/spaces/osunlp/Online_Mind2Web_Leaderboard — accessed 2026-06.
12. FlowithOS public desktop app for macOS & Windows — TestingCatalog (Threads) — https://www.threads.com/@testingcatalog/post/DQW6MWhDSfq/ — accessed 2026-06.
13. Enter FlowithOS — the world's first operating system for AI agents (changelog) — https://updates.flo.ing/changelog/enter-flowithos-the-worlds-first-operating-system-for-ai-agents — accessed 2026-06 (403 to fetcher; title/claim via search).
14. Flowith completes tens of millions in seed funding (announced ~March) — iNEWS — https://inf.news/en/economy/9abab70f5041e6d8815e38593fde4741.html — accessed 2026-06.
15. Flowith — AI Agent Assistant App (iOS) — Apple App Store — https://apps.apple.com/us/app/flowith/id6742640078 — accessed 2026-06.
16. Pricing — Flowith (official) + linktly/dupple review excerpts — https://flowith.io/pricing/ — accessed 2026-06 (official site 403 to fetcher; tiers via review excerpts).
