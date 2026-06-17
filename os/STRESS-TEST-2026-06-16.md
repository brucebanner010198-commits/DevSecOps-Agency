# `os/` second-pass red-team stress test — 2026-06-16

A *fresh*, deeper adversarial stress test of the whole `os/` Trust Spine build
(`trust-spine` B1 · `desktop` B2 · `broker` B3), run **after** the first
self-red-team ([`SECURITY-REDTEAM.md`](SECURITY-REDTEAM.md), 14 findings fixed).
The goal of a second pass is to find what the first pass missed — and to fix each
finding *properly* (root-cause, grounded in published practice), not paper over it.

Every finding below was **reproduced with a working proof-of-concept before it was
claimed**, and is now **closed with a fix and a regression test** that re-opens it
loudly if it regresses. Nothing here is speculative.

- **Baseline before:** 98 tests passing.
- **After this pass:** **105 tests passing** (+7 regression tests), 5 new findings fixed.

---

## 1. Scope & system under test

| In scope | Detail |
|---|---|
| `trust-spine/` | kernel, verifier, policy, capabilities, golden-share, Vault, signing (Ed25519 / ML-DSA-65), receipts, Merkle log, recursion budget |
| `desktop/` | side-car dispatcher + local Unix-domain-socket transport (the agent's typed door into apps) |
| `broker/` | de-identification broker (mask → default-deny → receipt → re-identify), stylometry, surrogates |

**Threat model boundary (unchanged from the build's own design):** a *personal,
single-user, sovereign device*. The adversary is (a) a prompt-injected / hijacked
agent inside the trust loop, and/or (b) a local process on the same machine that
can reach the side-car socket or the on-disk ledger. We do **not** assume a remote
network attacker (the transport is local-only by construction) or a kernel/root
compromise (out of scope for v0; keys move to TPM2 later).

**Access used:** full source + test read/write, ability to run the suite and
author PoCs. No external systems were touched.

---

## 2. Methodology

1. **Read the whole trust path** end-to-end (request → verifier → golden-share →
   effect/Vault → signed receipt → Merkle log), plus the two boundaries that take
   untrusted input: the side-car socket and the broker egress path.
2. **Adversarial hypotheses** along eight dimensions: replay/idempotency,
   resource-exhaustion/DoS, peer authentication, log forgery & non-repudiation,
   crash-safety/recovery, capability over-grant, masking completeness, and
   re-identification integrity.
3. **Reproduce-before-claim.** Each surviving hypothesis was turned into a runnable
   PoC; only PoC-confirmed issues are reported as findings.
4. **Research the *proper* fix** for each, grounded in current published standards
   (CWE, OWASP, OS man pages, WAL/crash-recovery literature) — see §6 Sources.
5. **Fix at root cause + pin with a regression test**, then re-run every PoC to
   confirm closure and the full suite to confirm no regression.
6. **Record what was considered and *rejected*** (§4), so the absence of a finding
   is honest, not silent.

---

## 3. Findings (all confirmed, all fixed)

| # | Sev | Finding | Class | Fix | Regression test |
|---|-----|---------|-------|-----|-----------------|
| **F1** | **High** | Golden-share single-use nonce was burned **only in memory**, so a captured approval re-executes after a kernel **restart** (crash/reboot) — defeating "one approval, one execution" for reserved actions (spend, identity.export, grant.capability). | Replay / idempotency | Redeemed nonces persisted **durably** (`redeemed_nonces.txt`, owner-only, fsync'd **before** the effect runs) and reloaded on init. | `test_golden_share_nonce_is_durable_across_restart` |
| **F2** | **High** (avail.) | Side-car transport: `_read_line` was **unbounded** (memory-exhaustion) and the accept loop served **one connection to completion before the next**, so a single silent client stalls **every** agent indefinitely (slowloris). | DoS (CWE-770 / CWE-400) | Frame **size cap** (64 KiB) + per-connection **recv timeout** (5 s) + **bounded worker pool** (one worker per connection, semaphore-capped) + load-shedding; kernel call serialized under a lock. | `test_slow_client_does_not_block_other_agents`, `test_read_line_refuses_oversized_frame` |
| **F3** | **Medium** | Side-car peer auth was DAC perms (`0600`, silently skipped on non-POSIX) + an *optional* token that **defaults to none**. No kernel-attested peer identity. | Authentication | **Peer-uid check** (Linux `SO_PEERCRED` / macOS·BSD `getpeereid`): a determinable-and-mismatched uid **fails closed**, so owner-only holds even if the socket perm is lost. Token remains the second layer. | `test_peer_uid_is_readable_for_same_uid_connection` |
| **F4** | **Medium** | Offline receipt verification checked only *embedded pubkey vs signature* — nothing bound **`actor` → registered key**. A rewritten log can attribute a $1M "owner" spend signed with the **attacker's own key** and `verify_log()` returns `ok: True`. | Non-repudiation / key substitution | `verify_log`/`verify_receipt` accept a **`known_keys` registry** (`keyring.public_keys()`); a receipt whose `public_key` ≠ the registered key for its `actor` is flagged. | `test_verify_log_binds_actor_to_registered_key` |
| **F5** | **Low** (resil.) | A **torn trailing write** (crash mid-append) or a junk byte made the *entire* ledger unreadable — `Ledger.__init__` raised, so the kernel couldn't even start to run `verify`. | Crash-safety / recovery | WAL-style recovery: a torn **trailing** record is validated-and-discarded (`recovered_torn_tail`); an **interior** corrupt line still **raises loudly** (`LedgerCorruptionError`) as a tamper signal. | `test_torn_trailing_line_is_recovered`, `test_interior_corruption_raises_loudly` |

### Severity rationale
Qualitative scale matched to the personal-device threat model. F1/F2 are **High**
because they break a *core product promise* — human-sovereign approval (F1) and an
always-responsive, interruptible agent door (F2) — even though both require a local
foothold. F3/F4 are **Medium**: defense-in-depth / offline-verification gaps with a
real but narrower precondition (lost socket perms; attacker write-access to the
log file). F5 is **Low**: availability/robustness, no confidentiality or integrity
loss.

---

### F1 — Golden-share nonce replay survives a restart  *(High)*

**Evidence (PoC, before fix).** A persistent golden-share key (as in a real TPM2
deployment) signs one `$49` spend intent bound to nonce `nonce-abc-123`:

```
session-1 submit:    allow   | spent: [49]
same-session replay: veto    | spent: [49]      # in-memory burn works...
post-restart replay: allow   | spent: [49, 49]  # ...but a NEW kernel re-executes
>>> VULNERABLE: the $49 approval executed TWICE across a restart
```

**Root cause.** `TrustKernel._used_nonces` was an in-process `set()`; a restart
reconstructs it empty, and the captured `(intent, signature, nonce)` re-verifies
(the signature is deterministic over the same intent) → re-`ALLOW`.

**Proper fix (research-grounded).** Anti-replay nonces must be **persisted**, not
held in volatile memory, and for charge/order-like operations the durable
**idempotency-key** pattern (store the redeemed key; a repeat returns the prior
result instead of re-executing) is the standard remedy — OWASP / API replay-prevention
guidance ([MDN: Replay attack](https://developer.mozilla.org/docs/Glossary/Replay_attack);
[Protecting API requests using nonce + time validation](https://dev.to/raselmahmuddev/protecting-api-requests-using-nonce-redis-and-time-based-validation-11nd)).
We persist the redeemed **nonce digest** to `redeemed_nonces.txt` (owner-only,
`fsync`'d **before** the effect runs — write-ahead, so a crash mid-effect can only
fail *safe*: the owner re-approves) and reload it on init.

**After fix:** `post-restart replay: veto | spent: [49]` — executed exactly once.

---

### F2 — Side-car transport is a trivial local DoS  *(High, availability)*

**Evidence (PoC, before fix).** One client connects and sends a partial frame with
no newline, then sits idle:

```
>>> VULNERABLE: a single silent client blocked the legitimate agent call for >3s
    (the server is stuck in _read_line on a never-terminated frame; all other
    agents are starved).
```

`_read_line` also had no length cap: a client that never sends `\n` grows the
buffer without bound (memory exhaustion).

**Root cause.** Two CWE-770 / CWE-400 patterns: (1) unbounded read buffer, (2) a
single-flight accept loop that fully reads+handles one connection before
`accept()`-ing the next, with no recv timeout — textbook slowloris
([CWE-770](https://cwe.mitre.org/data/definitions/770.html),
[CWE-400](https://cwe.mitre.org/data/definitions/400.html)).

**Proper fix (research-grounded).** The published remedy combines **a maximum
message size, a recv/read timeout, and bounded concurrency** so neither large nor
slow payloads can exhaust resources (size cap alone does not stop a 1-byte-per-minute
drip — you need the timeout too). We added all three: a 64 KiB frame cap, a 5 s
per-connection recv deadline, and a semaphore-bounded one-worker-per-connection
model with load-shedding at capacity; the single-writer kernel call is serialized
under a lock so concurrency stays safe.

**After fix:** `legit call returned in 0.01s` while the silent client stalls — no
head-of-line blocking; oversized frames are refused.

---

### F3 — No kernel-attested peer authentication  *(Medium)*

**Root cause.** Authentication relied on `chmod 0600` (silently skipped on
non-POSIX, lost if the socket dir is mis-permissioned) plus an **optional** token
that defaults to `None` → no auth. The `actor` string drives every
capability/attribution decision, so the connecting process's identity must be
established, not assumed.

**Proper fix (research-grounded).** `SO_PEERCRED` (Linux) / `getpeereid` via
`LOCAL_PEERCRED` (macOS·BSD) returns the peer's uid **from the kernel** — the
client cannot spoof it
([getpeereid(3)](https://man.freebsd.org/cgi/man.cgi?query=getpeereid);
[PostgreSQL `getpeereid.c`](https://github.com/postgres/postgres/blob/master/src/port/getpeereid.c)).
We read it on each connection and **fail closed** when it is determinable and ≠ the
server uid, so owner-only holds even if the filesystem perm was lost. The per-actor
token remains as the second layer for multi-agent separation.

---

### F4 — Receipt verification doesn't bind `actor` → key  *(Medium)*

**Evidence (PoC, before fix).** Attacker rewrites the ledger, attributing a spend
to `owner` but signing with their own freshly-minted key:

```
forged receipt actor : owner
forged receipt pubkey: 37dbba54f5ab92e6 … (attacker's key)
verify_receipt ok    : True | signature: True | chain: True
verify_log ok        : True | problems: []
>>> VULNERABLE: a $1,000,000 'owner' spend signed with an unknown key verifies
    as authentic; nothing binds actor->key at verify time.
```

**Root cause.** A signature proves *some* key signed — **not that the *registered*
key signed**. This is the classic key-substitution / non-repudiation gap
(Menezes–Smart, 2004:
[Key substitution attacks revisited](https://link.springer.com/article/10.1007/s10207-005-0071-2)).
The strict `KeyRing` (prior finding #8) blocks forged attribution at **write** time,
but **offline verification** of an exported/tampered log had no actor→key ground
truth.

**Proper fix.** `verify_log(known_keys=…)` / `verify_receipt(known_keys=…)` bind
each receipt's `public_key` to its `actor` against a pinned registry
(`keyring.public_keys()`); a mismatch is flagged as *forged attribution / key
substitution*. Default behaviour is unchanged (back-compat) when no registry is
supplied.

**After fix:** with `known_keys`, the forged log → `ok: False` (problem flagged); a
receipt signed with the registered owner key still passes.

---

### F5 — Ledger unreadable after a torn write  *(Low, resilience)*

**Evidence (PoC, before fix).** A partial final line (power loss mid-append):

```
>>> VULNERABLE: ledger load crashed on a torn line:
    JSONDecodeError: Unterminated string starting at: line 1 column 46 (char 45)
```

**Root cause.** `_load` parsed every line with no error handling; one bad byte made
the whole log — and every consumer of it, including `verify` — unloadable.

**Proper fix (research-grounded).** Append-only / WAL crash recovery **validates
each record and discards a torn trailing record** rather than aborting
([Write-Ahead Logging & ARIES recovery](https://sookocheff.com/post/databases/write-ahead-logging/)).
We recover a torn **trailing** line (set `recovered_torn_tail`, reload to the last
consistent state) while an **interior** corrupt line — which a torn write cannot
produce — still raises `LedgerCorruptionError` loudly as a tamper signal.

---

## 4. Considered and **rejected** (no invention)

Honest record of hypotheses that did **not** survive scrutiny, so their absence
from §3 is deliberate, not an oversight:

- **Broker masking-gate bypass via stylometry normalization** — *rejected.* The
  fail-closed gate re-scans for entities the detector can find, and the detector's
  coverage is a **subset** of the masker's (both use the same regex/`names` set,
  masking longest-first), so anything the detector sees was already masked. There
  is no exploitable order-of-operations gap. The *real* residual is the
  already-documented **NER boundary** (entities neither regex nor `names` cover) —
  unchanged, see §5.
- **`unmask` trusts attacker-controlled cloud tokens** — *not a new vuln.* The
  reverse map only contains surrogates actually emitted for *this* request, so a
  malicious cloud can at most reorder the user's *own* entities in a reply it
  generates; it cannot introduce identities it never received. Inherent to any
  reversible-mask broker; logged as a residual boundary, not a fix.
- **Capability grant signatures lack a nonce** — *acknowledged, low.* `grant`
  intents are not nonce-bound, so a grant signature is replayable. But the broker
  is **trusted-setup only** (never populated by an agent), so the attack surface is
  bootstrap code. Recorded as a residual hardening item (§5), not a shipped fix, to
  avoid over-engineering a trusted path.

---

## 5. Residual boundaries (v0, documented — not silently shipped)

- **F3 on exotic platforms.** Where neither `SO_PEERCRED` nor `getpeereid` exists
  (e.g. Windows AF_UNIX), peer-uid is *undeterminable*; the transport falls back to
  the token + filesystem perms there. macOS and Linux (the build targets) enforce.
- **F4 needs a pinned registry.** Binding requires the verifier to *hold* the
  actor→key map. For a log exported to a third party, ship a co-signed key directory
  alongside it; without one, offline verification can still only prove
  self-consistency (same class as the documented external-checkpoint boundary).
- **Masking completeness still needs NER.** The broker refuses on any entity its
  regex/`names` can detect; names it cannot detect need a local NER pass
  (`LocalModel`) — a wired backend, not a v0 stub.
- **Grant-intent replay** (above) — fold a nonce into `grant.capability` intents
  when the broker is exposed beyond trusted bootstrap.
- **Keys are in-memory.** Sealing the golden-share and per-actor keys in hardware
  (TPM2 / secure element) is the M-later effort; the durable nonce store (F1) is the
  software half of "approval survives a restart."

---

## 6. Patch plan — steps, owners, validation

All five fixes are **already implemented and merged into this branch** (this is a
remediation record, not a backlog). Ownership reflects the recursive-org roles in
`agents/` / `councils/`.

| Step | Finding | Action | Responsible (role) | Validation criteria — **status** |
|---|---|---|---|---|
| 1 | F1 | Durable redeemed-nonce store, fsync-before-effect, reload on init | Security reviewer (Opus tier) | `test_golden_share_nonce_is_durable_across_restart` green; PoC-1 post-restart = `veto`; effect runs once — **DONE** |
| 2 | F2 | Frame cap + recv timeout + bounded workers + call lock | Lead developer (Sonnet tier) | `test_slow_client_…` + `test_read_line_refuses_oversized_frame` green; PoC-4 legit call < 3 s under stall — **DONE** |
| 3 | F3 | `SO_PEERCRED`/`getpeereid` peer-uid, fail-closed | Security reviewer | `test_peer_uid_is_readable_…` green; mismatched uid rejected before kernel — **DONE** |
| 4 | F4 | `known_keys` actor→key binding in verify paths | Architect (Opus tier) | `test_verify_log_binds_actor_to_registered_key` green; PoC-2 forged log → `ok:False` with registry; back-compat preserved — **DONE** |
| 5 | F5 | WAL-style torn-tail recovery; interior corruption raises | Lead developer | `test_torn_trailing_line_is_recovered` + `test_interior_corruption_raises_loudly` green; PoC-3 loads OK — **DONE** |
| 6 | all | Full-suite regression gate | Gatekeeper (Opus tier) | **105/105 tests pass** across `trust-spine` (81), `desktop` (12), `broker` (12) — **DONE** |
| 7 | residual | Track §5 boundaries (TPM2 keys, grant nonce, NER, log export key directory) | Chairman (Owner) | Carried to the M-later roadmap; none block this merge — **OPEN** |

### Reproduce

```bash
# Full suite (105 passing):
for p in trust-spine desktop broker; do (cd os/$p && python3 -m pytest -q); done
```

The five PoCs used to confirm the findings are kept out-of-tree (local scratch);
each finding's behaviour is now pinned by the named regression test above, which is
the durable, version-controlled proof.

---

## 7. Sources

Fixes are grounded in these published references (accessed 2026-06-16):

- MDN Web Docs — *Replay attack* (single-use nonce requirement): https://developer.mozilla.org/docs/Glossary/Replay_attack
- *Protecting API requests using nonce + time-based validation* (durable nonce store / idempotency): https://dev.to/raselmahmuddev/protecting-api-requests-using-nonce-redis-and-time-based-validation-11nd
- MITRE **CWE-770** — *Allocation of Resources Without Limits or Throttling*: https://cwe.mitre.org/data/definitions/770.html
- MITRE **CWE-400** — *Uncontrolled Resource Consumption* (slowloris / read-timeout): https://cwe.mitre.org/data/definitions/400.html
- FreeBSD **getpeereid(3)** man page (Unix-socket peer credentials): https://man.freebsd.org/cgi/man.cgi?query=getpeereid
- PostgreSQL **`src/port/getpeereid.c`** (portable peer-uid reference impl): https://github.com/postgres/postgres/blob/master/src/port/getpeereid.c
- Menezes & Smart, *Key substitution attacks revisited* (signature ≠ identity binding / non-repudiation): https://link.springer.com/article/10.1007/s10207-005-0071-2
- Sookocheff, *Write-Ahead Logging and the ARIES crash-recovery algorithm* (torn-record recovery): https://sookocheff.com/post/databases/write-ahead-logging/

Mappings to the standards the build already targets — OWASP Top-10 for Agentic Apps
2026, Meta "Agents Rule of Two", Simon Willison's "lethal trifecta", NIST FIPS 204
(ML-DSA), RFC 6962 (Merkle) — are unchanged from [`README.md`](README.md) and the
first-pass [`SECURITY-REDTEAM.md`](SECURITY-REDTEAM.md).
