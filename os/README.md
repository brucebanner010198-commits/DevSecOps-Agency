# os/ — the trustable personal AI-OS (MVP wedge)

The first **runnable** software of the OS in [`VISION.md`](../VISION.md) /
[`MISSION.md`](../MISSION.md). It does not try to out-novel the crowded
agent-desktop field; it builds the one thing no rival ships for a *personal* user
— **an independent verifier-with-veto + signed receipts + sovereign golden-share
over a recursive company you chair** — and builds it *on top of* the recursive org
(`../agents/`, `../councils/`) and tool-interception (`../runtime-hooks/`) already
in this repo. No kernel required.

Grounded in the verified competitive research in
[`../research/competitive-landscape-ai-os/`](../research/competitive-landscape-ai-os/)
(refreshed + fact-checked 2026-06-16) and mapped to published standards
(NIST FIPS 204, OWASP Top-10 for Agentic Apps 2026, Meta "Agents Rule of Two",
Simon Willison's "lethal trifecta").

## The three sub-projects (built in sequence)

| Dir | What it is | Tests | Demo |
|---|---|---|---|
| **[`trust-spine/`](trust-spine/)** | the trust loop: receipts · verifier-with-veto · least-privilege · Vault · golden-share · budget-bounded recursion | 77 | `m1`–`m5` |
| **[`desktop/`](desktop/)** | the dual-interface app model — a typed side-car agent API routed through the trust spine (kills screen-scraping injection) | 9 | `b2_dual_interface` |
| **[`broker/`](broker/)** | the de-identification broker — mask → default-deny → receipt → re-identify; identity stays home | 12 | `b3_broker` |

**98 tests passing.** Each sub-project's README has run instructions.

> **Self-red-teamed.** This code was adversarially reviewed against itself before
> merge: 14 confirmed findings (2 critical) — including golden-share effect
> substitution, a Vault plaintext leak, and a `web.fetch` egress bypass — were
> fixed, each pinned by a regression test. See
> [`SECURITY-REDTEAM.md`](SECURITY-REDTEAM.md).

## Run everything

```bash
for p in trust-spine desktop broker; do (cd os/$p && python3 -m pytest -q); done
```

## What maps to which threat (regression stress-test → code)

| Attack (stress-test) | Defended by |
|---|---|
| Prompt-injection → exfiltration (OWASP ASI / lethal trifecta) | `trust-spine` M3 capabilities (multi-leg, incl. `web.fetch`) + `desktop` side-car |
| Confused-deputy autofill phishing | `trust-spine` M4 Vault (origin-binding + visibility + trusted destination) |
| Approval forgery by effect substitution | golden-gated effects dispatched from the **signed** intent via a trusted registry |
| Replaying one approval N times | single-use **nonce** burned by the kernel on first use |
| Secret captured via an agent-supplied sink | Vault writes only into a **trusted origin-bound destination** |
| Impersonating a more-privileged agent | side-car **peer token** auth + owner-only socket |
| Stylometric leakage | `broker` stylometry normalization |
| Unconsented egress / incomplete masking | `broker` default-deny + **fail-closed mask gate** + golden-share |
| Runaway recursion / budget collapse | `trust-spine` M5 RecursionBudget |
| Log tampering / truncation / harvest-now-decrypt-later | signed Merkle receipts (ML-DSA), truncation check, keyed digests |

A full record of the adversarial review and every fix is in
[`SECURITY-REDTEAM.md`](SECURITY-REDTEAM.md).

## Known v0 boundaries (honest)

- Receipts sign with **ML-DSA-65 (FIPS 204)** when `liboqs` is installed
  (verified working on this machine via `~/_oqs`), and fall back to **Ed25519**
  automatically when it isn't — PQC is pluggable hygiene, never a blocker.
- `desktop` is the trust core, not a native Wayland compositor (later effort).
- `broker` ships a **stub** local model + voice ASR + LDP paraphraser; real
  backends (llama.cpp/Ollama, whisper.cpp) plug in behind the same interfaces.
