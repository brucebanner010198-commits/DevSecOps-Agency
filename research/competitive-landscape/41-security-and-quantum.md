# Security & Quantum — the two hypotheses, fact-checked

**Purpose:** test the Sovereign's two starting hypotheses with current sources, and locate exactly where our trust wedge is defensible.

- **(a)** "Rivals' LLMs handle tasks but not security."
- **(b)** "Their OSes are not quantum-ready."

---

## Hypothesis (a): "tasks, not security" → **VALIDATED, with precision**

The right claim is narrow and defensible: **no rival ships per-agent, least-privilege security with a standing red-team and tool/secret vetting for a *personal* user.** The market is moving on *enterprise governance specs*, not on a per-employee security discipline baked into a personal AI company.

### What rivals actually have
- **Perimeter / jurisdiction, not per-agent:** Warmwind = EU/GDPR hosting + per-agent containers (isolation, no published least-privilege capability model) — doc 10. Brain Natural OS = on-device + Japan-only cloud, one broadly-privileged agent reading across apps — doc 13. Aluminium = per-**app** Android sandboxing, not per-**agent** — doc 12.
- **Enterprise governance frameworks exist** (this is the real state of the art, and it is *not* consumer):
  - **CSA Agentic Trust Framework (ATF)** — Zero-Trust governance spec for agents. [1]
  - **Microsoft Agent Governance Toolkit** — open-source runtime governance; claims coverage of all **10 OWASP agentic-AI risks** with sub-ms policy enforcement. [2]
  - **NVIDIA verified agent skills** — capability governance via signed skill cards. [3]
  - **TAIP** (Trustworthy AI Posture) — continuous-assurance framework (arXiv). [4]
- **The identity gap is industry-admitted:** only ~18% of security leaders are confident their identity systems can handle agent identities; teams share human credentials with agents because no alternative exists. [5]

### Why this is our wedge (repo already centered on it)
The repo seats security as a **blocking executive** (CISO veto), with a standing **red-team** (CRT veto), **independent audit** (CAO veto), plus tool-vetting and secrets-vaulting as first-class disciplines:
- Blocking vetoes CISO/CRT/CEVO/CAO — `AGENTS.md:13,32`.
- Per-agent disciplines — `SECURITY.md`, `THREAT-MODEL.md`, `agents/security/`, `skills/tool-scout/`, `skills/secrets-vault/`, `skills/sandbox/`, `skills/injection-defense/`.
- STRIDE + OWASP + ASI + AI-RMF coverage and vault-refs-only — `SWOT.md` §1 (S8–S9).

**Gap we own:** *per-employee* least-privilege + standing red-team + tool/secret vetting, delivered to a **personal** Chairman — not an enterprise admin. The frameworks above are the bar to clear and to cite; none is a chaired personal AI company.

## Hypothesis (b): "not quantum-ready" → **VALIDATED, with an important nuance**

The standards are final; the **real device OSes (Category 1) are mid-migration; the AI-agent experience layers (Category 2 — our category) say nothing about PQC at all.**

### Where PQC stands (2026)
- **NIST finalized three standards on 2024-08-13:** **ML-KEM / FIPS 203** (key exchange), **ML-DSA / FIPS 204** and **SLH-DSA / FIPS 205** (signatures). [6]
- **Transport is already shipping hybrid:** **X25519MLKEM768** is default in Chrome (since Chrome 131, Nov 2024; non-disableable by Chrome 138) and adopted by Cloudflare/Apple; Cloudflare reported **>50% of human web traffic** PQC-protected by late Oct 2025. [7][8]
- **Migration horizon:** NIST/CISA estimate **2–5 years** for enterprise; NSA CNSA 2.0 mandates PQC for new national-security systems from **2027**, full transition **2033–2035**. [9]
- **A real device OS already inherits PQC:** Aluminium/Android 17 carries **ML-DSA in Keystore, ML-KEM key exchange, PQC for Verified Boot/Attestation/Play signing** (~2029 full migration) — doc 12. This is *platform* PQC we should **consume**, not rebuild.

### The nuance that makes this a wedge
- **Zero AI-OS / AI-workforce rivals (Category 2) mention PQC** in their product/trust messaging (Warmwind states only "end-to-end encryption" — doc 10; Flowith/Rabbit/Genspark/Manus: none found — docs 11, 15; enterprise workforce + startups: none found — docs 21, 22).
- PQC for us lives in **crypto / transport / identity / data-at-rest / inter-agent comms** — all in the experience layer, deliverable **without writing a kernel** (doc 40 §5).
- **Driver:** *harvest-now-decrypt-later* — an adversary records today's encrypted traffic and decrypts it once a quantum computer exists. A personal AI OS holds a user's **entire digital life**, making it a prime HNDL target. That reframes PQC from "compliance checkbox" to "the reason a paranoid user trusts us with everything."

## What we build (deliverable in Category 2)

| Layer | Mechanism | Standard / tool |
|---|---|---|
| Per-agent security | namespaces + seccomp + cgroups; capability-scoped, audited tools; default-deny A2A; standing red-team | repo: CISO/CRT, tool-scout, sandbox, secrets-vault |
| Verifier | dedicated fact-checking employee: citations + "say unknown" | repo: CAO/CEVO/CRT councils |
| Receipts / reversibility | append-only action log + FS snapshots; replay/undo | repo: `docs/adr/`, session logs |
| PQC — transport | hybrid X25519MLKEM768 TLS | FIPS 203 |
| PQC — identity & signing | ML-DSA / SLH-DSA agent identities + signed receipts | FIPS 204 / 205 |
| PQC — at rest | ML-KEM-wrapped keys for user data | FIPS 203 |

## Verdict

- (a) **VALIDATED** — narrow it to *per-employee* security for a *personal* user; enterprise governance specs are the bar, not a competitor product.
- (b) **VALIDATED with nuance** — Category-1 OSes are migrating; **our category is silent**; PQC is deliverable above a reused kernel and is a genuine trust differentiator.

## Sources

1. CSA — The Agentic Trust Framework — https://cloudsecurityalliance.org/blog/2026/02/02/the-agentic-trust-framework-zero-trust-governance-for-ai-agents — 2026-02.
2. Microsoft Open Source — Agent Governance Toolkit (10 OWASP agentic risks) — https://opensource.microsoft.com/blog/2026/04/02/introducing-the-agent-governance-toolkit-open-source-runtime-security-for-ai-agents/ — 2026-04.
3. NVIDIA — Verified Agent Skills / capability governance — https://developer.nvidia.com/blog/nvidia-verified-agent-skills-provide-capability-governance-for-ai-agents/ — 2026.
4. TAIP: Trustworthy AI Posture (arXiv) — https://arxiv.org/pdf/2603.03340 — 2026.
5. Strata — The AI Agent Identity Crisis (governance gap; ~18% confidence) — https://www.strata.io/blog/agentic-identity/ — 2026.
6. NIST — FIPS 203/204/205 finalized 2024-08-13 — https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards — 2024-08.
7. Chrome / hybrid ML-KEM rollout (X25519MLKEM768, Chrome 131→138) — https://blog.chromium.org/ — accessed 2026-06.
8. Cloudflare — PQC traffic share (>50% by late Oct 2025) — https://blog.cloudflare.com/pq-2024/ — accessed 2026-06.
9. ISACA — PQC 12-month playbook (NIST/CISA 2–5yr; CNSA 2.0 2027→2033/35) — https://www.isaca.org/resources/news-and-trends/isaca-now-blog/2026/post-quantum-cryptography-a-12-month-playbook-for-digital-trust-professionals — 2026.
