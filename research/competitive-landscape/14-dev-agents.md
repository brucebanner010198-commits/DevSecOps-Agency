<!-- Shared shape for every player doc in this pack. Doc 01 (matrix) and 43 (scorecard) parse by these headers — headers are normative, not suggestive. -->

# /dev/agents → Dreamer (acqui-hired by Meta, Mar 2026)

**One-liner:** A "cloud OS for trusted AI agents across any device" — shipped as the consumer product **Dreamer** (Feb 2026), an app-store-style platform where a personal **Sidekick** ("agent that builds agents") orchestrates user-built agents; the entire founding team was acqui-hired into Meta Superintelligence Labs ~5 weeks after public beta. [1][7][9][12]
**Axis:** A = AI-OS experience (foreground) — explicitly a consumer "Personal Agent OS." Secondary B (agents do background tasks) but NOT an org/workforce model. [7][9]
**Category (3-meanings-of-OS):** Primarily **2 (AI-agent experience layer)**, self-described as **3 (kernel-for-agents)** via its OS metaphor (Sidekick = kernel, agents = userspace, tools = drivers). Cloud OS, not a real device OS. [9][11]
**Stage / availability:** Open beta launched 2026-02-18; team joined Meta 2026-03-23; product's independent future **unclear / likely wound down** (community forum said to stay online through 2026; no team remains). [10][12][13] · **As-of:** 2026-06

---

## What it does best · What it lacks · What we take

- **Best:**
  - **The cleanest articulation anywhere of "OS for agents as a *trust* substrate"** — Sidekick = kernel = "the trusted component that mediates and enables all access," "powerhouse" + "traffic cop ensuring none of your data goes to places you wouldn't expect." This is the closest public competitor to our trust wedge. [11][9]
  - **Permissions UX done as a first-class, inspectable install-time flow:** the OS knows exactly which tools an agent needs; you see, inspect, and explicitly grant tool access when installing someone else's agent. [9][11]
  - **Natural-language agent authoring** ("agent that builds agents"): describe a task, Sidekick drafts blueprint → checks tool access → writes logic+UI → tests → deploys. Genuinely novel consumer UX. [14][9]
  - **Top-tier founders + distribution credibility:** ex-Android/Stripe/Oculus team (Singleton, Barra, Kirkpatrick, Jitkoff), $56M seed at $500M post, Index + CapitalG, angels incl. Karpathy, Alexandr Wang, Nikesh Arora, Andy Rubin. [3][4][1]

- **Lacks (vs. full vision):**
  - **No recursive company / no Chairman-of-the-Board model.** It's flat: one user + a Sidekick + installable agents. No executives→teams→leaf-employee hierarchy. [synthesised from 9][11]
  - **Trust = permissions + "traffic cop," not verification.** No dedicated verifier / anti-hallucination agent, no receipts/reversibility/auditable-trail product, **no post-quantum crypto** — none of these appear in any primary source (search returns only generic PQC research, nothing tied to Dreamer). [synthesised — absence across 1,7,9,11,14]
  - **"Reimagined privacy model" stayed largely a slogan + install-time consent** — concrete mechanism (encryption, data-flow enforcement) never publicly detailed. [9][2]
  - **Now effectively a Meta asset.** Personal-trust positioning is undercut by absorption into Meta Superintelligence Labs; the independent product is leaderless. [12][13]

- **We take:**
  - Adopt the **kernel-as-trusted-mediator metaphor** but harden it into our actual differentiator: a *dedicated verifier* + *receipts/reversibility* + *per-agent least-privilege*, not just an install-time consent dialog → maps to `councils/audit/` and our verifier layer. [hypothesis][synthesised]
  - Steal the **install-time, inspectable tool-permission flow** as table-stakes UX for per-agent security. [9]
  - Lesson: **trust-as-slogan + Big-Tech exit is the failure mode we must avoid** — a personal trust OS that sells into Meta forfeits the wedge. Our PQC + reversibility + "personal-not-enterprise, never-the-platform-owns-you" stance is the counter-position. [user-knowledge][synthesised]

## Deep dive

**Who / funding.** /dev/agents was founded in 2024 by David Singleton (CEO; ex-Stripe CTO ~7 yrs, prior VP Eng Google Android), Hugo Barra (CPO; ex-Google Android product, ex-Meta VP Oculus/VR), Ficus Kirkpatrick (CTO; early Android engineer, ex-Meta VP AR/VR), and Nicholas Jitkoff (ex-principal designer Google Chrome, senior roles at Dropbox/Figma). [1][3][4] It raised a **$56M seed at a ~$500M post-money valuation**, co-led by **Index Ventures and CapitalG** (Alphabet's growth fund), with Conviction; angels included Andrej Karpathy, Alexandr Wang, Nikesh Arora, and Andy Rubin. Round dated **2024-11-26**, reported by TechCrunch 2024-11-28. [1][3][4]

**Original thesis (Nov 2024).** Index framed it as a "cloud OS for trusted agents to work with users across all their devices," resting on three pillars: **"new UI patterns, a reimagined privacy model, and a developer platform that makes it radically simpler to build useful agents."** The pitch was explicitly "the Android of the AI era." [16][5][2]

**What shipped — Dreamer (Feb 2026).** After ~15 months in stealth the company emerged as **Dreamer**, a consumer-first, no-code platform to "discover, build, and remix AI agents." Founder blog post 2026-02-17; **open beta 2026-02-18.** [7][8][14] Architecture is an explicit OS metaphor:
- **dreamer.com = the GUI;**
- **Agents = user space** — "intelligence-native software you can speak into existence," running in isolated environments, buildable by anyone, installable from a **gallery**, and **remixable** in natural language; [9][14]
- **Sidekick = the kernel** — a persistent, personalized agent with memory that "gets to know you over time," is both "powerhouse" (does the hard work) and "traffic cop" (mediates all access so data doesn't leak); it is literally "an agent that builds agents"; [9][11]
- **Tools = device drivers** — abstracted capabilities (printer/camera analogy) that are **part of the permissions model**: any agent/Sidekick may request them, and the OS surfaces exactly which tools an agent needs so you grant/deny at install. [9][11]

**UX surface.** Cross-device: desktop (dreamer.com), iOS (TestFlight; Android forthcoming), Chrome extension, and email. Agents are event-triggered (e.g., "email from sender X," a phone share, a Chrome-extension share). Example flow: "monitor my email for flight confirmations and add the trip to my calendar" → Sidekick produces a blueprint, checks tool access, writes business logic + UI, tests, deploys. [14][9] Includes its own **SDK, logging, database, and prompt management.** [9]

**Business model.** Beta = extended free trial of a **paid product** (promised no surprise charges); GA pricing **never disclosed**. Creator monetization: a share of user subscriptions paid to popular **tool builders**; gallery-featured agents earn creators platform credits. [10][9]

**Trust / security posture (the part most relevant to us).** This is the marquee claim and also the most under-specified. Trust = (a) Sidekick-as-kernel mediating all data access ("traffic cop"), and (b) **install-time, inspectable per-tool permissions**. [9][11] That is real and good, but it is **perimeter/consent-style**, not per-agent least-privilege enforcement, and there is **no dedicated verifier, no receipts/reversibility product, no audit-trail feature, and no post-quantum cryptography** in any primary source. The "reimagined privacy model" was never publicly detailed beyond consent + memory controls. [synthesised — absence across 2,7,9,11,14]

**The twist — Meta acqui-hire (Mar 2026).** ~5 weeks after beta, on **2026-03-23**, Meta absorbed the **entire founding team** into **Meta Superintelligence Labs**. Structured as a **non-exclusive technology license + acqui-hire**, not an acquisition: Dreamer remains a standalone legal entity; investors (Index, CapitalG, Conviction) reportedly get a **premium** on the $56M. The independent product is now **leaderless**; community forum said to remain online through 2026, but Dreamer's future as a standalone is "unclear." [12][13][10]

**Net assessment vs. full-vision yardstick.** Dreamer is our **closest philosophical competitor on "trust + OS for agents"** and validated the category — but it stopped at *consent-grade* trust and a *flat* agent model (user + Sidekick + apps), never reaching recursion, a Chairman org, verification, reversibility, or PQC. Its absorption into Meta is both a threat (Meta now holds the tech + the canonical team) and a strategic gift (the independent, personal-trust position is now vacant, and "we sold our trust OS to Meta" is a cautionary tale we can position against). [synthesised]

## SWOT (with so-what-for-us)

- **Strengths:** Best-in-class founders + the cleanest public "kernel = trusted mediator" framing and install-time permission UX. — *So-what:* they set the bar for how the trust story should be *told*; we must out-execute on substance (verifier/receipts/PQC), not just narrative.
- **Weaknesses:** Trust was consent-deep, not verified; privacy model never specified; no recursion/Chairman; no PQC/receipts; team gone. — *So-what:* every gap is directly a column where our differentiators score and theirs are blank — lean into it.
- **Opportunities:** They proved investor + consumer appetite for a "personal agent OS" and a creator/tool marketplace. — *So-what:* the independent personal-trust slot is now open; their gallery/tool-payout model is a marketplace blueprint we can adapt.
- **Threats:** Meta now has the tech license + the exact team that can rebuild this at Instagram/WhatsApp scale and distribution. — *So-what:* assume a Meta "personal agent OS" within 12–18 months; our moat must be the things Meta structurally *cannot* credibly offer — user-owned trust, reversibility, PQC, "the platform never owns you."

## Facts table

Each cell cited `[n]` or `unknown`. Confidence L/M/H.

| Dimension | Value | Conf | Source |
|---|---|---|---|
| Recursion / org depth (flat · 2-tier · deep/recursive) | **Flat** — user + Sidekick (kernel) + installable agents; no exec/team hierarchy | M | [9][11] synthesised |
| User-as-Chairman fit (does the human sit atop an org?) | **No** — user is an OS owner granting tool permissions, not a Chairman over an AI org | M | [9] synthesised |
| Interactive-OS surface (none · chat · desktop/OS · streamed) | **Desktop/OS-style** (dreamer.com GUI) + iOS + Chrome ext + email; chat-driven Sidekick | H | [9][14] |
| Per-agent security (none · perimeter · per-agent least-priv) | **Perimeter/consent** — install-time inspectable per-tool grants via Sidekick "traffic cop"; not enforced least-privilege | M | [9][11] |
| Verifier / anti-hallucination (none · gestures · dedicated) | **None disclosed** | M | absence in [9][11][14] synthesised |
| Receipts / reversibility (none · logs · auditable trail) | **Logging exists for devs (SDK)**; no user-facing receipts/reversibility/audit-trail product | L–M | [9] synthesised |
| Post-quantum (PQC) (none · stated · shipped) | **None** — no mention anywhere | M | absence across [1][7][9][11][14] |
| Local / cloud / hybrid | **Cloud** ("cloud OS"); cross-device clients | H | [16][1][9] |
| Hardware (cloud-only · existing HW · own device) | **Cloud-only on existing HW** (web/iOS/Chrome); no own device | H | [9][14] |
| Availability | Open beta 2026-02-18; team → Meta 2026-03-23; standalone future unclear/likely wound down | H | [8][12][13] |
| Pricing | Beta = free trial of a paid product; **GA pricing never disclosed** | M | [10] |
| Funding / stage | $56M seed, ~$500M post, 2024-11-26; Index + CapitalG + Conviction; acqui-hired by Meta (non-exclusive license, investor premium) | H | [1][3][12] |
| UX notes | Sidekick "agent that builds agents"; NL authoring → blueprint→tool-check→logic+UI→test→deploy; gallery + remix; event triggers; tool-builder revenue share | H | [9][14][10] |

## Sources

1. New startup named /dev/agents led by Ex-Google, Meta tech leaders raises $56M — SiliconANGLE — https://siliconangle.com/2024/11/26/new-startup-named-dev-agents-led-ex-google-meta-tech-leaders-raises-56m-ai-agents/ — dated 2024-11-26, accessed 2026-06.
2. The Operating System for AI Agents: Our investment in /dev/agents — Index Ventures — https://www.indexventures.com/perspectives/the-operating-system-for-ai-agents-our-investment-in-devagents/ — 2024-11, accessed 2026-06 (via search summary; site 403'd direct fetch).
3. Why AI agent startup /dev/agents commanded a massive $56M seed round at a $500M valuation — TechCrunch — https://techcrunch.com/2024/11/28/ai-agent-startup-dev-agents-has-raised-a-massive-56m-seed-round-at-a-500m-valuation/ — dated 2024-11-28, accessed 2026-06 (via search summary; 403'd direct).
4. David Singleton (@dps) launch announcement — X/Twitter — https://x.com/dps/status/1861413927856546187 — dated 2024-11-26, accessed 2026-06.
5. /dev/agents company page — Index Ventures — https://www.indexventures.com/companies/devagents/ — accessed 2026-06.
6. /dev/agents valuation, funding & news — Sacra — https://sacra.com/c/dev-agents/ — accessed 2026-06.
7. Dreamer – why we built it! — David Singleton blog (singleton.io) — https://blog.singleton.io/posts/2026-02-17-introducing-dreamer/ — dated 2026-02-17, accessed 2026-06 (via search summary; 403'd direct fetch).
8. Dreamer Raised $56M to Build an Agent OS — 5 Weeks After Launch, Meta Hired the Entire Team — topaiproduct.com — https://topaiproduct.com/2026/03/23/dreamer-raised-56m-to-build-an-agent-os-5-weeks-after-launch-meta-hired-the-entire-team/ — dated 2026-03-23, accessed 2026-06.
9. Dreamer: the Personal Agent OS — David Singleton (Latent Space podcast/writeup) — https://www.latent.space/p/dreamer — 2026-02/03, accessed 2026-06.
10. Dreamer lets anyone build AI agents — The Neuron — https://www.theneurondaily.com/p/dreamer-lets-anyone-build-ai-agents — 2026-02, accessed 2026-06.
11. Dreamer: The Agent OS That Treats AI Like Apps — teamday.ai (analysis of Latent Space interview) — https://www.teamday.ai/ai/singleton-dreamer-agent-os-latent-space — 2026, accessed 2026-06.
12. Meta acqui-hires the co-founders of agentic AI startup Dreamer — SiliconANGLE — https://siliconangle.com/2026/03/23/meta-acqui-hires-co-founders-agentic-ai-startup-dreamer/ — dated 2026-03-23, accessed 2026-06.
13. Meta acqui-hires Dreamer's entire team to bolster its lagging AI agent ambitions — The Decoder — https://the-decoder.com/meta-acqui-hires-dreamers-entire-team-to-bolster-its-lagging-ai-agent-ambitions/ — dated 2026-03, accessed 2026-06.
14. Dreamer: Building AI Agents for Everyone — StartupHub.ai — https://www.startuphub.ai/ai-news/artificial-intelligence/2026/dreamer-building-ai-agents-for-everyone — 2026, accessed 2026-06.
15. Meta's Stealthy Acqui-Hire of Dreamer — Buttondown (Verified) — https://buttondown.com/verified/archive/metas-stealthy-acqui-hire-of-dreamer-why-the-tech/ — 2026-03, accessed 2026-06.
16. Former Google execs band together to create OS for AI — Mobile World Live — https://www.mobileworldlive.com/ai-cloud/former-google-execs-band-together-to-create-os-for-ai/ — 2024-11, accessed 2026-06.
