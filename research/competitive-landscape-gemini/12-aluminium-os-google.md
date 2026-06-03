<!-- Shared shape for every player doc in this pack. Doc 01 (matrix) and 43 (scorecard) parse by these headers — headers are normative, not suggestive. -->

# Aluminium OS (Google)

**One-liner:** Google's Android-17-based desktop operating system (Chromebook/ChromeOS successor) that converges Android and ChromeOS into a single AI-forward OS with Gemini baked into every layer, on-device NPU inference, and x86 + ARM support. [1][2][4]
**Axis:** Infra = architecture reference (a real device OS we sit *above*) · secondarily Axis A (it ships a foreground AI-OS experience via Gemini + Magic Pointer)
**Category (3-meanings-of-OS):** **1 — real device OS** (kernel + drivers + window manager + verified boot). [synthesised from 1][2]
**Stage / availability:** Announced / pre-release; OEM "Googlebook" devices targeted Q3/Fall 2026. [3][5][6] · **As-of:** 2026-06

---

## What it does best · What it lacks · What we take

- **Best:**
  - Owns the *bottom of the stack* we will never want to own: Linux kernel, drivers, verified boot, secure hardware (Keystore/TEE), monthly security patches, and an x86+ARM hardware ecosystem across Acer/ASUS/Dell/HP/Lenovo. [1][5][6]
  - Real on-device AI: Gemini Nano runs on the laptop NPU so core features (incl. Magic Pointer) work without sending documents to the cloud — a genuine privacy/latency moat that is hard to copy without silicon partnerships. [2][4]
  - Inherits Android 17's **post-quantum** roadmap "for free": ML-DSA in Android Keystore, plus PQC groundwork in Verified Boot, Remote Attestation, and Play signing. [9][10][11] This is exactly the platform-level PQC we want to *build on*, not reinvent.
  - Distribution and trust-by-default at consumer scale: Google brand, OEM channel, education base, and the entire Android app/Play ecosystem.

- **Lacks (vs. full vision):**
  - **No recursive org / no Chairman model.** Gemini is a single assistant ("intelligence system" framing [7]), not a hierarchy of AI executives → teams → leaf one-task employees. There is no "user sits atop an org" abstraction. [synthesised]
  - **No dedicated verifier / anti-hallucination layer.** Magic Pointer + Gemini offer suggestions; there is no independent agent whose job is to check another agent's work. [synthesised]
  - **No receipts / reversibility as a product primitive.** Android has logs and permissions, but nothing surfaced as an auditable, reversible "every action has a receipt" trail for AI actions. [hypothesis — no source describes one]
  - **Per-agent least-privilege is absent.** Security is per-*app* sandboxing + permissions, not per-*agent* least-privilege for a workforce of AIs. [synthesised from 8]
  - **Enterprise/consumer device play, not a personal AI company.** It is an OS for one person's machine, not a personal company you command.

- **We take:**
  - **Sit above it, reuse Linux — do not fight at Category 1.** Treat Aluminium OS (and any Linux device OS) as the host substrate; our trust layer, recursive org, and AI-OS run as a layer on top. Map to `infra/host-adapter/` [hypothesis — anchor to confirm in repo].
  - **Adopt its PQC primitives rather than rolling our own:** target ML-KEM/ML-DSA-backed keys via OS Keystore/TEE where present, falling back to our own PQC otherwise. Anchor: `crypto/pqc/`.
  - **On-device-first inference as a trust signal** — copy the "documents never leave the device for core features" posture for our local verifier path. Anchor: `councils/audit/` + local-model path.

## Deep dive

**What it is and who's behind it.** Aluminium OS (internal codename "ALOS") is a desktop OS developed by Google (with Google DeepMind contributions on the AI layer) to converge Android and ChromeOS. It is described as Android 17 "rebuilt as a genuine desktop platform" — a custom window manager, a real taskbar, virtual desktops integrated into Recents, a built-in Linux environment, and Gemini integrated at the OS layer rather than bolted on. [1][2][4] Because ChromeOS already used the Android Linux kernel and core components, Google frames this as building on shared infrastructure rather than a from-zero kernel. [1]

**Chronology (note: reporting is somewhat inconsistent; treated at M confidence).** Google publicly confirmed in **July 2025** that ChromeOS and Android would converge onto one platform. [synthesised from 7]. At **Qualcomm's Snapdragon Summit in September 2025**, Sameer Samat (President, Android Ecosystem) and Qualcomm's Cristiano Amon announced a partnership to build the common technical foundation, with Snapdragon X cited and first devices in 2026. [3][7] The Aluminium OS name and product framing were surfaced through leaks (late 2025) and then formal reveal events in 2026 — multiple outlets cite **The Android Show on May 12, 2026** ("15 years and one day after the first Chromebook shipped") and the **Google I/O 2026** keynote (mid-May 2026) as the announcement moments. [4][5][7] First "Googlebook" laptops (the rebranded Chromebook) from **Acer, ASUS, Dell, HP, and Lenovo** are targeted for **Q3 / Fall 2026**. [5][6][7] Notably, Samat stated ChromeOS development "will absolutely continue as is" even as Aluminium OS arrives — i.e., a multi-year transition, with engineers calling the old platform "ChromeOS Classic." [1][7]

**Hardware & architecture.** Like ChromeOS, Aluminium OS targets both **ARM and x86**; Google VP John Maletis confirmed chips from **Qualcomm, Intel, and MediaTek**. [2] There is heavy emphasis on **on-device AI via the NPU**: premium devices with a dedicated NPU run Gemini Nano locally, keeping documents on the hardware for "core" features — pitched explicitly at lawyers, doctors, and government contractors who cannot send data to cloud AI. [2][4][8]

**UX / the AI layer.** The headline interaction is **Magic Pointer** (built with Google DeepMind): the cursor becomes a context-aware AI agent — shake/hover over a chart and Gemini offers analysis; select text and it offers rewrite/translate/summarize. [4] Gemini is positioned as the OS-level "intelligence system" (Samat's phrasing: Android moving "from an operating system to an intelligence system"). [7] The broader Google agentic stack (Gemini CLI in the bundled Linux terminal; Gemini 2.5 "Computer Use" / Project Mariner for GUI automation) gives the platform a credible agentic trajectory, though these are Gemini-ecosystem features rather than Aluminium-OS-exclusive. [synthesised from search]

**Trust / security posture.** Inherited from Android: **per-app sandboxing**, granular runtime permissions, **Verified Boot** at every startup, AICore isolating each on-device inference request from other apps, and **monthly security patches**. [8] Crucially, as an Android 17 derivative it inherits the **post-quantum** work landing in Android 17: **ML-DSA support natively in Android Keystore** (quantum-safe signatures inside secure hardware), plus PQC adjustments to **Verified Boot, Remote Attestation, and Google Play signing**, on a roadmap aimed at ~2029 full migration. Google has already moved internal key exchange to **ML-KEM** and ships X25519+ML-KEM-768 hybrid TLS in Chrome by default. [9][10][11] This makes Aluminium OS one of the few real device OSes shipping a credible PQC story — but it is *device/transport/boot* PQC, not *per-agent* application-layer trust.

**Why this matters to us (positioning).** Aluminium OS is a **Category-1 real device OS**: it owns the kernel, drivers, secure boot, and silicon relationships. We deliberately **do not compete here.** We reuse Linux (which Aluminium itself is built on) and run our recursive AI company + trust layer *above* the device OS, treating Aluminium/ChromeOS/Linux as interchangeable hosts. Where Aluminium provides hardware-backed PQC keys and on-device NPU inference, we consume them; where it stops (no recursive org, no Chairman model, no dedicated verifier, no agent-action receipts, no per-agent least-privilege), our wedge begins. [synthesised][user-knowledge]

## SWOT (with so-what-for-us)

- **Strengths:** Owns the full device stack (kernel→silicon→Play ecosystem) with Google distribution and a real PQC + on-device-AI story. [1][2][9] — *So-what:* we should never try to out-OS Google at Category 1; ride on it and differentiate at the trust/org layer.
- **Weaknesses:** Single-assistant model, no recursion/Chairman, no dedicated verifier, no agent-action receipts/reversibility, per-app (not per-agent) security. [synthesised] — *So-what:* every column of our trust + recursive-org thesis is an open gap above Aluminium; that is our defensible space.
- **Opportunities:** Bundled Linux env + Gemini CLI + NPU make it an ideal *host* for a third-party trust/agent layer; hardware PQC keys are exposed via Keystore. [9][10] — *So-what:* build an Aluminium/Linux host-adapter that consumes its PQC + local inference rather than duplicating them.
- **Threats:** Google could extend Gemini from assistant → agentic OS layer and add receipts/verification natively, with unbeatable distribution. [hypothesis] — *So-what:* lead hard on *recursive org + Chairman + per-agent security + receipts* (things Google has no product incentive to ship for a personal AI *company*), and on personal-not-enterprise framing.

## Facts table

Each cell cited `[n]` or `unknown`. Confidence L/M/H.

| Dimension | Value | Conf | Source |
|---|---|---|---|
| Recursion / org depth (flat · 2-tier · deep/recursive) | Flat — single Gemini assistant / "intelligence system," no agent hierarchy | H | [7][synthesised] |
| User-as-Chairman fit (does the human sit atop an org?) | No — user operates a device with one AI assistant, not an org of AIs | H | [synthesised] |
| Interactive-OS surface (none · chat · desktop/OS · streamed) | Desktop/OS — full Android-17 desktop: window manager, taskbar, virtual desktops, Magic Pointer cursor agent | H | [1][2][4] |
| Per-agent security (none · perimeter · per-agent least-priv) | Per-*app* sandboxing + granular permissions (not per-agent least-priv) | M | [8] |
| Verifier / anti-hallucination (none · gestures · dedicated) | None dedicated — Gemini gives suggestions; no independent verifier agent | M | [synthesised] |
| Receipts / reversibility (none · logs · auditable trail) | Logs/permissions only; no surfaced auditable receipt trail for AI actions | M | [hypothesis] |
| Post-quantum (PQC) (none · stated · shipped) | Shipped/landing via Android 17: ML-DSA in Keystore, ML-KEM key exchange, PQC for Verified Boot/Attestation/Play signing (full migration ~2029) | M | [9][10][11] |
| Local / cloud / hybrid | Hybrid — Gemini Nano on-device via NPU for core features; cloud Gemini for heavier tasks | H | [2][4][8] |
| Hardware (cloud-only · existing HW · own device) | Own/OEM devices — "Googlebook" laptops from Acer, ASUS, Dell, HP, Lenovo; Qualcomm/Intel/MediaTek chips; x86 + ARM | H | [2][5][6] |
| Availability | Announced; OEM devices targeted Q3 / Fall 2026; ChromeOS continues in parallel ("Classic") | M | [3][5][7] |
| Pricing | Device tiers reported (unofficial): AL Entry ~$299–499, AL Mass Premium ~$500–799, AL Premium ~$800–1,500+. OS itself bundled/free. Google has not officially confirmed pricing. | L | [unofficial — multiple outlets] |
| Funding / stage | Internal Google/DeepMind product (not separately funded); pre-launch productization | H | [1][7] |
| UX notes | Gemini at OS layer; Magic Pointer (shake cursor → contextual AI); bundled Linux terminal + Gemini CLI; Recents-integrated virtual desktops | H | [4] |

## Sources

[1] "Google's new 'Aluminium OS' project brings Android to PC: Here's what we know" — Android Authority — https://www.androidauthority.com/aluminium-os-android-for-pcs-3619092/ — accessed 2026-06 (via WebSearch summary; direct fetch returned HTTP 403).
[2] "Aluminium OS (ALOS) — The Complete 2026 Guide to Google's Android Desktop OS" — aluminium-os.in — https://www.aluminium-os.in/ — accessed 2026-06 (NPU, x86/ARM, Qualcomm/Intel/MediaTek, John Maletis; via WebSearch summary).
[3] "Google launches Aluminum OS: Unified Android with AI for laptops and desktops in 2026" — Mix Vale (2025-12-01) — https://www.mixvale.com.br/2025/12/01/google-launches-aluminum-os-unified-android-with-ai-for-laptops-and-desktops-in-2026-en/ — accessed 2026-06 (Snapdragon Summit Sept 2025, Osterloh/Amon partnership).
[4] "Google's new 'Aluminium' project is the Android-based future of ChromeOS, and we have the first details" — Chrome Unboxed — https://chromeunboxed.com/googles-new-aluminium-os-is-the-android-based-future-of-chromeos-and-we-have-the-first-details/ — accessed 2026-06 (Android 17, window manager, Magic Pointer, Gemini at OS layer; via WebSearch summary).
[5] "Googlebook Release Date, Specs, and OEMs: What We Know" — The Gadgeteer (2026-05-27) — https://the-gadgeteer.com/2026/05/27/googlebook-release-date-specs-chromebook-successor/ — accessed 2026-06 (OEMs Acer/ASUS/Dell/HP/Lenovo, Q3 2026).
[6] "Inside Google's Aluminium OS: What the future holds for Android on desktops" — Android Central — https://www.androidcentral.com/chromebooks-laptops/googles-aluminium-os-could-be-androids-big-desktop-breakout — accessed 2026-06 (tiers, hardware).
[7] "Google explains its Aluminium OS vision for future Android-powered laptops" — Android Authority, Sameer Samat interview — https://www.androidauthority.com/google-aluminium-os-sameer-samat-interview-3646400/ — accessed 2026-06 ("intelligence system" framing; "ChromeOS development will absolutely continue"; The Android Show 2026-05-12).
[8] "An introduction to privacy and safety for Gemini Nano" — Android Developers Blog (2024-10) — https://android-developers.googleblog.com/2024/10/introduction-to-privacy-and-safety-gemini-nano.html — accessed 2026-06 (AICore request isolation, on-device privacy; underpins Aluminium's Gemini Nano claims).
[9] "Security for the Quantum Era: Implementing Post-Quantum Cryptography in Android" — Google Security Blog — https://blog.google/security/security-for-the-quantum-era-implementing-post-quantum-cryptography-in-android/ — accessed 2026-06 (ML-DSA/ML-KEM in Android).
[10] "Android 17 is Getting a Post Quantum Cryptography Upgrade" — Privacy Guides (2026-03-26) — https://www.privacyguides.org/news/2026/03/26/android-17-is-getting-a-post-quantum-cryptography-upgrade/ — accessed 2026-06 (Keystore ML-DSA, Verified Boot/Attestation/Play signing, ~2029 timeline).
[11] "Android 17 Quantum-Safe Security: What's Protected and What's Not" — Gadget Hacks — https://android.gadgethacks.com/news/android-17-quantum-safe-security-whats-protected-and-whats-not/ — accessed 2026-06 (scope of Android 17 PQC).
[12] "Aluminium OS" — Wikipedia — https://en.wikipedia.org/wiki/Aluminium_OS — accessed 2026-06 (developer Google/DeepMind, Android 17 base, codename ALOS; via WebSearch summary, direct fetch HTTP 403).
