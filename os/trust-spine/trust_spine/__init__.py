"""Trust Spine v0 — the verifiable trust loop for a sovereign personal AI OS.

This package instruments an agent org with the trust machinery that no rival
ships for a *personal* user:

  M1  signed, replayable receipts over an append-only Merkle log  (this milestone)
  M2  an independent verifier-with-veto + risk tiers
  M3  per-agent least-privilege + lethal-trifecta separation
  M4  a Vault stub (act-without-reveal) + golden-share gate
  M5  a watchable loop + one recursion demo

Design anchors (see ../../docs/design/): trust-architecture.md, foundation-architecture.md.
Standards anchors: NIST FIPS 204 (ML-DSA), OWASP Top-10 for Agentic Apps 2026,
Meta "Agents Rule of Two", Simon Willison "lethal trifecta".

Crypto note: v0 signs with Ed25519 (always available via `cryptography`) and will
prefer ML-DSA-65 automatically when `liboqs` (the `oqs` module) is installed. PQC is
hygiene, not a moat — it must never block the first runnable demo.
"""

__version__ = "0.1.0"
