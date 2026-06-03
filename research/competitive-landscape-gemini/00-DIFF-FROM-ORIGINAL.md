# Delta Report: Corrections and Upgrades vs. Original Pack

**Date:** 2026-06-02 · **Prepared by:** Gemini Competitive-Intelligence Orchestrator
**Status:** Complete

This document logs every correction, verified fact, confidence upgrade, and structural improvement made to the AI-OS / AI-Company Competitive Landscape research pack compared to the prior version.

---

## 1. Executive Summary of Improvements

1.  **Factual Verification & Primary Sourcing:** Replaced triangulated search-engine snippets with verified primary source fetches for Warmwind, Flowith, Aluminium OS, Brain Natural OS, /dev/agents, Rabbit, Genspark, and Manus.
2.  **Frontier Players Added (Doc 16):** Added comprehensive profiles for OpenAI (Operator, AgentKit), Apple Intelligence (Siri + App Intents), Amazon (Alexa+ / Bedrock AgentCore), and Anthropic (Claude Code / Cowork / SDK / MCP).
3.  **Strict Alphabetization (Doc 01 & 43):** Restructured the Master Capability Matrix and the Crux Scorecard to list all players in strict alphabetical order.
4.  **Self-Red-Team (Doc 47):** Formulated 6 detailed adversarial challenges to our own thesis with honest concessions and rebuttals.
5.  **PQC Reframing (Doc 41 & 44):** Reframed Post-Quantum Cryptography (PQC) as essential first-mover hygiene rather than a permanent technical moat.
6.  **Depth-Cap Ambiguity Flag (Doc 45):** Highlighted the ambiguity in the source repo's depth-cap wording (counting from CEO vs. Chief) to be resolved in the design interview.

---

## 2. Fact Corrections & Verification Log

| File | Claim / Dimension | Original Value | Corrected / Upgraded Value | Source | Confidence Change |
|---|---|---|---|---|---|
| `10` | Warmwind exit stealth & Waitlist | Waitlist ~42k companies, exit stealth 2025 | Verified: Exited stealth July 3, 2025 with 12,000+ waitlist, later growing to ~42,000. Rebranded from eva AG to warmwind AG. | [bm-t.de](https://www.bm-t.de/en/2025-en/warmwind-exits-stealth-mode/), [Startbase](https://www.startbase.com/news/warmwind-verlaesst-stealth-modus-mit-15-mio-euro-seed/) | L/M → **High (H)** |
| `11` | Flowith Funding & Tiers | "tens of millions" | Verified: Seed led by Vertex, Seed+ led by Sequoia China Seed + LongRiver. Users: 500k+. | [iNEWS](https://inf.news/en/economy/9abab70f5041e6d8815e38593fde4741.html) | L/M → **High (H)** |
| `12` | Aluminium OS Announcement | May 12, 2026 | Verified: Codename for Google's Android-based desktop OS to replace ChromeOS; Android 17 desktop integrations. | [Android Authority](https://www.androidauthority.com/google-aluminium-os-sameer-samat-interview-3646400/) | L/M → **High (H)** |
| `13` | Brain Natural OS Launch | 2026-04-24 | Shipped Natural AI Phone with SoftBank Japan on 2026-04-24 for ¥93,600. Jerry Yue founder. | [SoftBank News](https://www.softbank.jp/en/sbnews/entry/20260420_01) | L/M → **High (H)** |
| `14` | /dev/agents Acqui-hire | Mar 23, 2026 | Verified: Exited stealth as Dreamer (Feb 18, 2026); acqui-hired into Meta Superintelligence Labs (MSL) March 23, 2026. | [SiliconANGLE](https://siliconangle.com/2026/03/23/meta-acqui-hires-co-founders-agentic-ai-startup-dreamer/) | L/M → **High (H)** |
| `15` | Manus VM Isolation | Task-isolated VMs | Ephemeral, per-task isolated cloud VMs destroyed after completion. | [ZenML](https://zenml.io/llmops-database/) | L/M → **High (H)** |
| `15` | Manus Meta Deal Block | Blocked by regulators | Verified: Meta's $2B acquisition of Manus (Butterfly Effect) was officially blocked and ordered unwound by China's NDRC on April 27, 2026. | [TechCrunch](https://techcrunch.com/2026/04/27/china-vetoes-metas-2b-manus-deal/) | L/M → **High (H)** |
| `31` | NickAI Launch & Custody | Delaware trading OS | Non-custodial trading OS launched March 12, 2026; backed by Galaxy Digital. | [The Defiant](https://thedefiant.io/) | L/M → **High (H)** |
| `41` | NIST PQC Standards | August 2024 finalization | Verified: FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA) finalized Aug 13, 2024. | [NIST](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) | Medium → **High (H)** |
| `41` | PQC Web Traffic | >50% PQC-protected | Cloudflare reported 57.4% of browser connections use X25519MLKEM768 hybrid key share in early 2026. | [Cloudflare Radar](https://radar.cloudflare.com/post-quantum) | Medium → **High (H)** |
| `41` | Android 17 Keystore | ML-DSA in Android 17 | Verified: Native ML-DSA support inside Secure hardware (TEE) for Verified Boot and Keystore. | [Google Security Blog](https://blog.google/security/security-for-the-quantum-era-implementing-post-quantum-cryptography-in-android/) | Medium → **High (H)** |

---

## 3. Structural Adjustments

*   **PQC Moat Re-evaluation:** In the original pack, PQC was treated as a primary product moat. In the updated pack, it is reframed as **first-mover hygiene** that paranoid users expect. The true moat is user-owned cryptographic custody (keys held on local hardware) rather than the algorithms themselves.
*   **Alphabetical Ordering:** Sorted all matrix rows in `01-overview-and-matrix.md` and scorecard rows in `43-full-vision-match.md` alphabetically.
*   **Ambiguity Flag:** Added a specific warning to `45-open-questions-interview.md` noting that the depth-cap count (3 levels) in the source repository is ambiguous (is it CEO → Chief → Specialist, or starting from Chief?), requiring a design decision.
