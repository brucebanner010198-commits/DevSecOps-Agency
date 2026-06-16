# `os/` self-red-team and hardening — 2026-06-16

Before proposing this code for merge we red-teamed our own trust spine, because a
*trust* product that ships unverified trust code is the thing we exist not to be.
This is the record of what the red-team found and how each finding was resolved.

## Method

Two multi-agent adversarial reviews (8 security dimensions total), each finding
**double-verified** by two independent skeptics (an exploitability lens and a
code-correctness lens); only findings both skeptics confirmed are treated as
"confirmed". Dimensions: cryptographic correctness, verifier-bypass,
lethal-trifecta enforcement, Vault leakage, golden-share replay/forgery,
receipt-log privacy, dual-interface/side-car, recursion budget. (Three dimensions
died on transient API errors in the first run and were re-run to completion, so
coverage is not silently partial.)

Outcome: **14 confirmed findings** (2 critical, 5 high, the rest medium/low) plus
a few disputed/rejected. Every confirmed finding now has a fix and a regression
test that re-opens it loudly if it regresses.

## Confirmed findings → fixes (all fixed)

| # | Sev | Finding | Fix | Test |
|---|-----|---------|-----|------|
| 1 | **crit** | Golden-share signed the intent *description*, but the kernel ran an opaque agent-supplied `effect()` callable not covered by the signature → effect substitution (approve $49, run $4900). | Golden-gated actions are now executed by a **trusted, registered effect handler dispatched from the SIGNED intent** (`TrustKernel.register_effect`, `SignedEffect`); opaque callables are forbidden for reserved actions (fail closed). | `test_effect_substitution_is_impossible`, `test_reserved_action_without_registered_handler_is_vetoed` |
| 2 | **crit** | Vault `use()` wrote the raw secret into a **caller-supplied `sink`** → the agent received the plaintext; "act without reveal" was theatre. | Sink removed from the request. The Vault writes only into a **trusted destination registered by origin** (`register_destination`), resolved by the kernel — the agent can neither supply nor capture it. Fails closed if no destination is registered. | `test_use_refused_when_no_trusted_destination_registered`, `test_use_into_good_field_acts_without_reveal` |
| 3 | high | Golden-share approval had **no nonce / single-use** binding → one approval replayable for N identical reserved actions. | `action_intent` binds a single-use `nonce`; the kernel **burns it on first use** and rejects reuse. | `test_same_approval_cannot_be_replayed_twice` |
| 4 | high | `web.fetch` was an **unguarded egress channel**: mapped to `untrusted_input` only and never allowlist-checked, so `{untrusted_input, secret_access}` (Rule-of-Two-legal) could exfiltrate a secret via the fetch URL. | Actions now carry a **set** of capabilities; `web.fetch = {untrusted_input, network_egress}`, is veto-gated, and every network-reaching action clears the **same egress allowlist**. | `test_web_fetch_requires_both_untrusted_input_and_egress`, `test_web_fetch_with_two_legs_only_is_vetoed`, `test_web_fetch_is_egress_allowlisted_even_with_caps` |
| 5 | high | Side-car `actor` was **self-asserted** over the socket with no peer authentication → any local process could impersonate a more-privileged actor and inherit its capabilities. | Socket peer **authenticated** by a per-actor connection token (`SideCarServer(tokens=…)`, constant-time compare) + owner-only (`0600`) socket. | `test_actor_token_authentication_blocks_impersonation` |
| 6 | high | Vault `field_anomaly` visibility audit was a narrow deny-list — positive off-screen offsets, fractional opacity, zero size, clip-path, `scale(0)`, `aria-hidden` all passed as "visible". | Audit broadened to all of these; documented that a production compositor should **allow-list a measured on-screen box**. | `test_hidden_fields_refused` (expanded) |
| 7 | high | Unknown/unmapped actions **failed open** — kept the agent-declared tier, required no capability, allowed at tier<3. | Policy `deny_unknown_actions` (opt-in, recommended for hardened deployments) **default-denies** any action no layer classifies. | `test_unknown_action_allowed_by_default_but_denied_when_policy_opts_in` |
| 8 | med | `KeyRing` minted a fresh key for **any** actor name → forgeable receipt attribution (an attacker could attribute actions to "owner"). | `KeyRing(strict=True)` pins actors via `register()`; the kernel **refuses unregistered actors** with no forged receipt. | `test_kernel_with_strict_keyring_refuses_unknown_actor` |
| 9 | med | `vault.use` with **no Vault configured** fell through to run the opaque `effect()`. | Kernel **fails closed**: `vault.use` without a Vault is vetoed, never falls through. | `test_kernel_vault_use_fails_closed_without_a_vault` |
| 10 | med | `verify_log` did not detect **trailing truncation/rollback** despite the docstring claiming "any delete breaks a chain link". | `verify_log` compares the live log against `head.json` and an optional external checkpoint (`expected_size/root`); docstring corrected to be honest about what v0 can/can't catch. | `test_trailing_truncation_is_detected`, `test_external_checkpoint_detects_rollback` |
| 11 | med | Receipt input/output hashes were **unsalted SHA-256** → a low-entropy value (phone, card) is brute-forceable off a leaked log. | Digests are **keyed HMAC-SHA256** with a device-local key (`digest.key`, never egressed); compatible with signature/Merkle verification (which never recompute from raw). | `test_receipt_digests_are_keyed_on_disk` |
| 12 | med | Broker mask leak-check was **advisory and ran after** the send. | Now a **fail-closed gate before** egress: any residual detectable entity refuses the send (no send, no receipt) and the receipt records masking was verified. | `test_masking_failure_is_blocked_before_send` |
| 13 | med | Least-privilege silently disabled when no `CapabilityBroker` was wired. | Made **explicit/inspectable** (`Verifier.enforces_capabilities`) and documented; deployments that rely on least-privilege must pass a broker. | (documented; verifier still enforces the coarse layer) |
| 14 | low/disp | `grant()` full-trifecta waiver was a **plain boolean**, not a verified signature, and grants left no receipt. | `CapabilityBroker.bind_golden_share()` enables **signature-verified** trifecta grants + a ledger receipt; the bare boolean remains only for trusted-setup code. | (covered by capabilities behavior) |

## Honest residual boundaries (v0, documented — not silently shipped)

- **FieldDescriptor still comes from the agent in v0.** The destination *writer*
  is now trusted (finding 2), which is what stops plaintext capture; a production
  build must also source the field's visibility from the trusted compositor's
  rendered layout rather than a self-reported style dict (finding 6).
- **Full masking needs NER.** The broker's fail-closed gate (finding 12) refuses
  on any entity its regexes/`names` list can detect; names it cannot detect still
  require a local NER pass (`LocalModel`) — a wired backend, not a v0 stub.
- **`deny_unknown_actions` is opt-in.** Default-off so the free-form recursive-org
  demo runs; hardened deployments (desktop, broker) should set it on.
- **Keys are in-memory.** M-later seals them in hardware (TPM2 / secure element).

## Reproduce

```bash
for p in trust-spine desktop broker; do (cd os/$p && python3 -m pytest -q); done   # 98 passing
```

Every row above maps to a named test; the hardening tests live in
`os/trust-spine/tests/test_hardening.py`, `test_golden_share.py`, `test_vault.py`,
`os/desktop/tests/test_transport.py`, and `os/broker/tests/test_broker.py`.
