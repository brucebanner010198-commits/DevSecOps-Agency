# Trust Spine v0

The first runnable piece of the sovereign personal AI-OS: the **verifiable trust
loop** that instruments an agent org with the machinery no rival ships for a
*personal* user — an independent verifier-with-veto, signed replayable receipts,
per-agent least-privilege, a Vault that acts without revealing, and a
golden-share gate.

It is built to sit **on top of** the recursive org already in this repo
(`agents/`, `councils/`) and the existing tool-interception in `runtime-hooks/`.
No kernel required — this is the experience-layer trust spine.

> Why this first: post-quantum crypto and basic receipts became table stakes in
> 2026 (Apple/Chrome PQC by default; Fetch.ai AEVS and "Notarized Agents" now
> ship signed receipts). The durable, un-copyable part is an **independent
> verifier-with-veto + sovereign golden-share custody over a recursive company
> you chair** — so we build that, and we build *on* proven primitives (CaMeL,
> Progent, Fides, PunkGo) rather than claiming to invent them.

## Status

| Milestone | What it adds | State |
|---|---|---|
| **M1 — Receipts v0** | signed, replayable receipts over an append-only RFC-6962 Merkle log + `verify-receipt` CLI | ✅ done |
| **M2 — Verifier-with-veto** | independent verifier + risk tiers (1 log-only / 2 async / 3 veto-gated) + Trust Kernel proxy | ✅ done |
| **M3 — Least-privilege** | capability tokens + lethal-trifecta separation (Meta "Rule of Two") | ✅ done |
| **M4 — Vault + golden-share** | act-without-reveal Vault (origin-binding + visibility) + sovereign human-signature gate | ✅ done |
| **M5 — Watchable loop** | live receipt stream + budget-bounded Owner→CEO→leaf recursion, replayable | ✅ done |

**61 tests passing.** Demos: `m1_receipts_demo.py` · `m2_verifier_demo.py` · `m3_least_privilege_demo.py` · `m4_vault_golden_share_demo.py` · `m5_recursion_watch_demo.py`.

## Crypto

Receipts sign with **Ed25519** today (always available via `cryptography`) and
**ML-DSA-65 / FIPS 204** automatically when `liboqs` (the `oqs` module) is
installed. The algorithm is recorded in every receipt, so verification is
unambiguous either way. PQC is hygiene, not a moat — it must never block the
demo.

## Layout

```
trust_spine/
  signing.py    # Ed25519 + ML-DSA backends, pluggable
  merkle.py     # RFC 6962 append-only Merkle tree + inclusion proofs
  receipts.py   # signed, canonical, hash-chained receipts
  ledger.py     # append-only JSONL ledger + offline verification
  cli.py        # verify-receipt / verify-log / show-log
tests/          # 25 tests (signing, merkle, receipts, ledger, tamper)
demos/          # runnable milestone demos
```

## Run it

```bash
cd os/trust-spine
python3 -m pytest -q                 # 25 passing
python3 demos/m1_receipts_demo.py    # the visible trust loop, incl. tamper detection
python3 -m trust_spine.cli --ledger ./demos/.m1-demo-ledger show-log
python3 -m trust_spine.cli --ledger <dir> verify-receipt <id>   # exit 0 PASS / 1 FAIL
```

## Tamper-evidence (what M1 actually guarantees)

1. **Per-receipt:** each receipt is signed over the canonical bytes of all its
   fields except the signature — editing any field breaks its own signature.
2. **Whole-log:** receipts form a hash chain (`prev_receipt_hash`) and an
   RFC-6962 Merkle tree — any insert/delete/reorder breaks a chain link and
   changes the root.

`head.json` anchors the current size + root. In production that checkpoint is
published/co-signed so even a fully rewritten file is caught; in v0 the
**signatures** are the primary detector and the Merkle root provides offline
inclusion proofs.

## Design & standards anchors

- `docs/design/trust-architecture.md`, `docs/design/foundation-architecture.md`
- NIST FIPS 204 (ML-DSA); RFC 6962 (Merkle); OWASP Top-10 for Agentic Apps 2026;
  Meta "Agents Rule of Two"; Simon Willison "lethal trifecta".
