<!-- Shared shape for every player doc in this pack. Doc 01 (matrix) and 43 (scorecard) parse by these headers — headers are normative, not suggestive. -->

# Warmwind (eva AG)

**One-liner:** A German/EU "AI operating system" — a streamed cloud Linux desktop that a vision-language agent ("Cloud Employee") operates with mouse/keyboard like a human, trained by demonstration ("teaching mode") rather than API integrations. [1][2]
**Axis:** A = AI-OS experience (foreground) — secondarily B (a single-tier "digital employee" workforce). [2][6]
**Category (3-meanings-of-OS):** Mostly **#2 AI-agent experience layer** (a browser-streamed desktop framed as an "OS"), with a real **#1 device-OS** substrate (custom Linux distro) that is an implementation detail, not a user device. [1][9]
**Stage / availability:** Closed beta (invite-only, ~8% approval), public waitlist; free during beta. · **As-of:** 2026-06 [3][7]

---

## What it does best · What it lacks · What we take

- **Best:**
  - **Vision-first universality** — the agent "sees" any GUI and drives it with simulated mouse/keyboard, so it works on legacy and no-API apps: "if a human can use it, Warmwind can use it." This is the hard-to-copy moat versus MCP/API-only agents. [4][8]
  - **Teaching mode as the onboarding primitive** — click one button, demonstrate a task 2–3 times, and the agent generalizes the *intent* (not just clicks), so it adapts when the screen shifts. This is a genuinely consumer-grade way to "program" an agent. [5][12]
  - **EU/GDPR trust posture by construction** — full-stack owned model + interface, German cloud, no third-party APIs, marketed as GDPR-compliant and sovereign; optional on-prem deployment. [6][10][2]
  - **"Close your laptop, they keep working"** — server-side execution streamed to the browser makes always-on autonomy tangible and explains the "OS" metaphor well. [11][1]

- **Lacks (vs. full vision):**
  - **No recursion / no Chairman model** — it is a flat pool of peer "Cloud Employees" managed like an IT admin oversees staff; there is no executive→team→leaf hierarchy and no human-atop-an-org framing. [11] [synthesised]
  - **No dedicated verifier / anti-hallucination layer** — transparency is *visual* (you watch the cursor) plus human-in-the-loop monitoring, not a separate fact-checking/verifier agent. Critics flag reliability/"glorified screen-scraping" risk. [13] [synthesised]
  - **Trust = perimeter + per-agent container, not per-agent least-privilege capabilities** — each agent runs in its own container with data isolation, but there is no published capability/permission model, signed receipts, or reversibility ("undo") trail. [11] [synthesised]
  - **No post-quantum crypto claim** — "end-to-end encryption" only; nothing PQC. [10] [synthesised]
  - **Enterprise/SMB-office framing, not personal AI-OS** — pitched at SMB office-workflow automation, not a personal life OS. [6][2]

- **We take:**
  - **Teaching-mode demonstration loop** as the UX north star for low-friction agent authoring; map to our foreground onboarding (`os/foreground/`). [5][12] [user-knowledge]
  - **The visible AI cursor + task list** as our transparency baseline — then *exceed* it with a real verifier + receipts (our wedge). Anchor against `councils/audit/`, `verifier/`. [synthesised]
  - **Vision+API hybrid stance** ("APIs optional, packaged as apps") informs our connector strategy — prefer APIs for speed, fall back to vision for the long tail. [4] [synthesised]

## Deep dive

**Who's behind it.** Warmwind is built by **eva AG**, a startup based in Jena, Germany, founded in 2022 that has focused on a "secure, European AI stack" since 2023 [3][6]. It exited stealth on **3 July 2025** with a **closed beta** and a public waitlist of **12,000+** at launch [3][7]; later coverage cites a waitlist of ~42,000 companies with an ~8% approval rate [7]. The company raised a **€1.5M seed** round (closed early 2025) from **bm-t Beteiligungsmanagement Thüringen, BRT Ventures, and a private/angel investor** [3][6]. Team is ~10 people [1]. No later/larger round is reported as of 2026-06 [synthesised — absence of newer press].

**What it is.** Warmwind markets itself as "the world's first AI-native operating system" and as an **autonomous Cloud Employee** that automates repetitive office workflows through a visual interface, "without API integrations or deep IT expertise" [2][6]. The "OS" label is admittedly a **deliberate metaphor**: the company concedes that "an AI-powered automation suite for cloud-based interaction orchestration" would lose readers, whereas "an operating system for AI workers" communicates the idea [13].

**How it works (architecture).** Under the hood it is a **custom Linux distribution** optimized for automation, rendered headlessly and streamed to the user's browser via **Wayland + VNC**; logic runs server-side and the user sees a streamed desktop [1][9]. The "brain" is a proprietary **VTAM (Vision-and-Text Action Model) combined with a VLLM (vision LLM)** that perceives the screen in real time and executes via **simulated mouse and keyboard** — no code-based integration required [9]. Each agent runs in **its own container** with data isolation; agents can **share memory/context** (e.g., a support bot sees an issue flagged by a social agent) [11]. The architecture is modular and can also be deployed **on-premise** [6][10].

**Agent / org model.** The unit is a **Cloud Employee** you "hire" inside a browser workspace; you can create/manage **multiple workspaces** and manage "roles, permissions, and workflows like an IT admin overseeing a human team" [11]. This is a **flat, single-tier workforce** — peer agents under one human admin — not a recursive executive hierarchy [11] [synthesised].

**Teaching mode.** The defining authoring loop: click one button to enter teaching mode; the OS "watches everything you do"; you perform the full workflow manually (log in, navigate, fill fields, save, capture confirmation) and **repeat 2–3 times with varied data**; the model learns the **intention** behind clicks so it can re-execute even when the UI shifts [5][12]. This positions Warmwind as demonstrate-once-then-delegate rather than prompt-engineering or scripting.

**Vision vs. MCP stance.** Warmwind's own blog frames an "architecture war": MCP/API agents are efficient in structured environments, but **vision agents** expand reach to legacy/GUI-only tools — "Warmwind needs only a screen and a cursor." Crucially it does **not reject APIs**; it makes them **optional**, packaging external tools as "apps" for speed where available [4][8].

**Trust / security posture.** The trust story is **jurisdictional + isolation-based**: German/EU cloud, GDPR-compliant, full-stack owned (model→interface) with no third-party API dependency, end-to-end encryption, per-agent containers with data isolation, and human-in-the-loop monitoring via a real-time dashboard [6][10][11]. There is **no published per-agent capability/least-privilege model, no dedicated verifier/anti-hallucination component, no signed receipts/reversibility trail, and no post-quantum crypto** — transparency is delivered visually (you watch the AI's cursor and a task list) [11] [synthesised]. Skeptics specifically question reliability ("glorified screen-scraping with ChatGPT") and whether vision-driving-a-GUI is needlessly slow versus back-end APIs [13].

### UX teardown

This is the section most relevant to us as a UX north star [user-knowledge].

- **Surface:** A **browser-streamed desktop** (Chrome/Edge), no local install; the experience is "an always-accessible AI-enhanced desktop environment in your browser." Because execution is server-side, **closing your laptop doesn't stop the work** — a strong, legible mental model for "autonomy that persists." [11][1]
- **Layout / mental model:** The UI splits into **two regions** — a *user-focused* area (settings, profile/workspace management) and an *assistant-focused* area (task execution + monitoring). The assistant is explicitly **not a sidebar chatbot** — it *controls the whole desktop*: opens apps, clicks, fills forms, writes, sends, follows up. This is the key UX inversion: the agent is the primary actor, the human supervises. [5][11]
- **Transparency primitives:** (1) a **visible AI cursor** that shows exactly what the agent is doing in real time; (2) a **task list** tracking ongoing/completed tasks; (3) a **real-time dashboard** to monitor and intervene across agents. Trust is conveyed by *watchability*, not by receipts or proofs — a gap we can exploit. [5][11]
- **Authoring:** **Teaching mode** is the headline interaction — one button, demonstrate, repeat 2–3×, done. No scripting. Aimed deliberately at non-technical users (marketing copy claims it's usable "including children and seniors"). [5][12]
- **App model:** An **integrated app store** with one-click install gives the desktop metaphor real teeth and packages API tools as "apps." [4][9]
- **Onboarding friction:** Access is **invite-gated** (manual approval, ~8% of a large waitlist), browser-only — high scarcity, which builds hype but limits real-world validation. [7]
- **North-star takeaways for us:** the *demonstrate-once* authoring loop, the *agent-as-desktop-driver* (not sidebar) inversion, and the *visible cursor + task list* transparency are all adoptable. Our differentiation is to keep this UX while adding the **recursive org / Chairman framing**, a **dedicated verifier**, and **receipts/reversibility** on top of the watchable surface. [synthesised]

## SWOT (with so-what-for-us)

- **Strengths:** Vision-driven universality + dead-simple teaching mode + EU sovereignty story is a coherent, defensible package. — *So-what:* validates that "demonstrate, don't integrate" + a streamed desktop is a winning consumer UX; we should match the loop and beat the trust layer. [4][5][6]
- **Weaknesses:** Flat single-tier workforce; trust is perimeter/isolation + *visual* transparency, with no verifier, receipts, capability model, or PQC; reliability skepticism unproven at scale. — *So-what:* this is exactly our wedge — recursion + verifier + receipts + PQC are all open lanes. [11][13] [synthesised]
- **Opportunities:** Strong EU-data-sovereignty demand; legacy/no-API long tail is huge; could add hierarchy/governance later. — *So-what:* they could move toward our space; we must own the trust/recursion narrative first. [6] [synthesised]
- **Threats:** Already shipping a polished UX with funding, press, and a 40k+ waitlist; "first AI OS" mindshare in EU. — *So-what:* they set UX expectations and the "AI OS" vocabulary; we differentiate on trust + Chairman model, not on the desktop metaphor alone. [3][7]

## Facts table

Each cell cited `[n]` or `unknown`. Confidence L/M/H.

| Dimension | Value | Conf | Source |
|---|---|---|---|
| Recursion / org depth (flat · 2-tier · deep/recursive) | Flat — pool of peer "Cloud Employees" under one human admin; no executive hierarchy | M | [11] [synthesised] |
| User-as-Chairman fit (does the human sit atop an org?) | Partial — human is an "IT admin" supervising peers, not a Chairman atop a recursive org | M | [11] [synthesised] |
| Interactive-OS surface (none · chat · desktop/OS · streamed) | Streamed desktop (custom Linux via Wayland+VNC) in browser; agent drives the whole desktop | H | [1][9][11] |
| Per-agent security (none · perimeter · per-agent least-priv) | Per-agent container + data isolation (isolation, not published least-priv capability model); EU/GDPR perimeter | M | [11][6] |
| Verifier / anti-hallucination (none · gestures · dedicated) | None dedicated — visual transparency (AI cursor, task list) + human-in-the-loop monitoring only | M | [5][11] [synthesised] |
| Receipts / reversibility (none · logs · auditable trail) | Logs/task list + real-time dashboard; no signed receipts or reversibility/undo published | L | [11] [synthesised] |
| Post-quantum (PQC) (none · stated · shipped) | None — only "end-to-end encryption" stated | M | [10] [synthesised] |
| Local / cloud / hybrid | Cloud (German cloud); modular, on-prem deployment also offered | M | [6][10] |
| Hardware (cloud-only · existing HW · own device) | Cloud-only; accessed via browser on any device (no own device) | H | [9][11] |
| Availability | Closed beta, invite-only (~8% approval), public waitlist (~42k companies cited) | M | [3][7] |
| Pricing | Free during beta; future = subscription tiers by agent count/usage (no per-task fee); exact tiers unknown | L | [7] |
| Funding / stage | €1.5M seed (closed early 2025) from bm-t, BRT Ventures, + angel; eva AG (Jena, founded 2022); ~10 staff | H | [3][6][1] |
| UX notes | Browser-streamed desktop; agent-as-driver (not sidebar); teaching mode (demonstrate 2–3×); visible AI cursor + task list; app store; works after laptop closed | H | [5][11][12][4] |

## Sources

1. BGR — "Warmwind AI OS: How It Works, And Do You Need It?" — https://www.bgr.com/tech/the-worlds-first-ai-operating-system-wants-to-automate-your-workflow/ — accessed 2026-06 (custom Linux, Wayland+VNC streaming, ~10-person team).
2. Warmwind / eva AG — "Warmwind OS: Building the AI Operating System for Everyone" (official blog) — https://about.warmwind.space/warmwind-os-building-the-ai-operating-system-for-everyone/ — accessed 2026-06 (positioning, SMB framing, no-API/no-IT-expertise).
3. Warmwind / eva AG — "Autonomous Cloud Employees Enter Closed Beta" (official blog, exit-stealth announcement, 3 Jul 2025) — https://about.warmwind.space/warmwind-closed-beta/ — accessed 2026-06 (closed beta, 12,000+ waitlist, €1.5M seed, eva AG Jena founded 2022).
4. Warmwind / eva AG — "Vision vs. MCP: The Architecture War Shaping Autonomous AI Agents" (official blog) — https://about.warmwind.space/vision-vs-mcp-the-architecture-war-shaping-autonomous-ai-agents/ — accessed 2026-06 (vision-vs-API stance, "only a screen and a cursor," APIs optional/packaged as apps).
5. Geeky Gadgets — "How warmwind OS Works: Architecture, AI Model and Design" — https://www.geeky-gadgets.com/warmwind-os-ai-operating-system/ — accessed 2026-06 (two-region UI, visible AI cursor, task list, app store, teaching mode, VTAM/VLLM).
6. bm|t — "warmwind Exits Stealth Mode: Autonomous Cloud Employees Enter Closed Beta" (investor press, 2025) — https://www.bm-t.de/en/2025-en/warmwind-exits-stealth-mode/ — accessed 2026-06 (€1.5M seed, investors, German full-stack/GDPR, eva AG).
7. bestaitools — "Warmwind — Is This The Best AI Productivity Tool in 2026?" — https://www.bestaitools.com/tool/warmwind/ — accessed 2026-06 (access model: manual approval ~8%, browser-only Chrome/Edge, ~42k waitlist, free-beta→subscription).
8. Warmwind — "Vision vs. MCP" (Medium mirror) — https://medium.com/@warmwind/vision-vs-mcp-the-architecture-war-shaping-autonomous-ai-agents-3ed4701314a4 — accessed 2026-06 (vision agents reach legacy/GUI-only tools).
9. Informative Picks — "Warmwind-OS: Custom Linux Powering AI's Cloud Workforce" — https://www.informativepicks.com/warmwind-os-architecture-explained/ — accessed 2026-06 (VTAM+VLLM brain, simulated mouse/keyboard, VM/cloud backend, browser frontend).
10. Startbase — "warmwind exits stealth mode with €1.5 million seed" (2025) — https://www.startbase.com/news/warmwind-verlaesst-stealth-modus-mit-15-mio-euro-seed/ — accessed 2026-06 (German domestic cloud, proprietary model, on-prem option, encryption).
11. Googlu AI — "Warmwind OS Review: The AI Operating System with Digital Employees Is Here" — https://googluai.com/warmwind-os-review/ — accessed 2026-06 (per-agent containers + data isolation, shared memory, admin dashboard, hire/manage workspaces, agent-as-driver, "close laptop / keeps working").
12. Geeky Gadgets — "How warmwind OS Automates Your Workflows with AI Agents" — https://www.geeky-gadgets.com/warmwind-os-autonomous-cloud-employees/ — accessed 2026-06 (teaching-mode demonstrate-2-3×, learns intention, generalizes across UI changes).
13. Warmwind — "We Built an Operating System for AI…But Is It Really One?" (official blog) — https://about.warmwind.com/we-built-an-operating-system-for-ai-but-is-it-really-one/ — accessed 2026-06 ("OS" as deliberate metaphor; acknowledges screen-scraping/efficiency skepticism).
