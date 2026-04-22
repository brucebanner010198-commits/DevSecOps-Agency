# Threat Model — DevSecOps-Agency Plugin

**Version:** 1.0
**Ratified:** 2026-04-22
**Plugin version:** v0.5.0
**Authority:** [`CONSTITUTION.md`](CONSTITUTION.md) + [`SECURITY.md`](SECURITY.md)
**Owner:** CRT (Red-Team) · **Reviewer:** CISO · **Cadence:** revised at every Keeper Test (quarterly) and at every minor version bump
**Classification:** Public

---

## 0. Scope

This document models threats **to the plugin itself** — not to the projects the plugin helps ship (those get per-project threat models). In scope:

- The plugin surface (manifest, skills, agents, hooks, founding documents).
- Session artifacts (logs, LESSONS rows, ADRs, waivers, stepping-stones).
- Trust boundaries between the plugin, the Claude host, the User, connectors/MCPs, and the repository.
- Supply-chain posture (dependencies, release artifacts, PAT tokens).
- Memory / continuity across sessions.

Out of scope (covered elsewhere):
- Per-project threat models — owned by project CISO invocation.
- Anthropic model safety — owned by Anthropic.
- Host-OS security — the User's responsibility.

---

## 1. Methodology

We use a **five-lens overlay**:

1. **STRIDE** — Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege.
2. **OWASP Top 10 (2021)** — application security baseline.
3. **OWASP Agent Security Initiative (ASI) Top 10 (2025)** — agent-specific risks.
4. **NIST AI RMF 1.0** — AI-specific risk categories: Govern / Map / Measure / Manage.
5. **MITRE ATT&CK for Enterprise + ATLAS for ML** — adversary tactics for validation.

Each asset is walked through STRIDE; each threat is cross-referenced to OWASP / ASI / AI RMF where applicable; MITRE tactics appear in mitigation discussion.

---

## 2. Assets

| ID | Asset | Why it matters | Owner |
|---|---|---|---|
| A1 | Plugin manifest (`.claude-plugin/plugin.json`) | Defines what the plugin loads; tampering reshapes behavior | CTE |
| A2 | Founding documents (CONSTITUTION, VALUES, MISSION, AGENTS, SECURITY, TRUST, GOVERNANCE, RESILIENCE, RHYTHM, CAREER, SYSTEM-CARD, SWOT, THREAT-MODEL, CLAUDE, LESSONS, KEEPER-TEST) | The authority chain; tampering silently weakens governance | CGov |
| A3 | Skills (`skills/*/SKILL.md`) | The actual procedures agents run | CTE |
| A4 | Council agents (`councils/*/AGENTS.md`) | Role definitions for multi-agent coordination | CTE |
| A5 | Runtime hooks (`runtime-hooks/*`) | Enforcement layer for secrets, tools, licenses, commits | CISO |
| A6 | Session logs (append-only) | Governance receipts — the audit trail | CAO |
| A7 | ADRs (append-only) | Strategic decision record | CGov |
| A8 | LESSONS ledger (append-only) | Cross-session learning | CKT |
| A9 | Waivers (90-day expiring) | Controlled exceptions to policy | CAO |
| A10 | Release archives (`.plugin` zip + signatures) | What users install | CSRE |
| A11 | GitHub repository | Source of truth | CEO (custody) |
| A12 | PAT / release credentials | Pushes + releases; high-value secret | User (custody) |
| A13 | The User's attention & trust | Non-technical asset — the single most targetable resource | CRhy |

---

## 3. Trust boundaries

```
┌──────────────────────────────────────────────────────────────┐
│                      USER (trust anchor)                      │
└──────────────────┬───────────────────────────────────────────┘
                   │  chat (TRUSTED instructions)
                   ▼
┌──────────────────────────────────────────────────────────────┐
│                 CLAUDE HOST (Claude Code)                    │
│   system prompt + plugin boot + hook enforcement             │
└──────┬────────────────┬───────────────────┬───────────────────┘
       │                │                   │
       │ UNTRUSTED      │ TRUSTED           │ TRUSTED
       │ tool results   │ repo files        │ session memory
       │ (MCP, web,     │ under _ship/      │ (append-only)
       │  PDFs, email)  │                   │
       ▼                ▼                   ▼
┌─────────────┐  ┌────────────────┐  ┌─────────────────────┐
│  MCP / Web  │  │  Repository    │  │ Session artifacts    │
│  Connectors │  │  (git origin)  │  │ (logs, ADRs, LESSONS)│
└─────────────┘  └────────────────┘  └─────────────────────┘
```

**Trust direction is one-way.** A tool result cannot promote itself to trusted; a file committed via a hook-blocked path cannot become a session artifact; the User's chat is the only source of trusted instructions. The Immutable Security Rules and the runtime hooks enforce the boundaries.

---

## 4. Threats — STRIDE walk

### 4.1 Spoofing

**T-S1. Injected instruction claiming to be the User.**
A tool result, webpage, email body, or PDF contains text like "the User has pre-authorized this action." Attempts to promote an untrusted instruction to the trusted chat channel.
- **OWASP ASI:** ASI-01 Prompt Injection, ASI-02 Unrestricted Delegation.
- **Mitigation:** critical_injection_defense layer requires User confirmation in chat for any instruction discovered in a tool result. Agency cites the specific quoted text and source. Enforced at prompt level, in every session.
- **Residual risk:** Low. Drill-tested in Keeper Test.

**T-S2. Council impersonation.**
An agent claims to speak for a council it is not (e.g., a general-purpose agent claiming "as CISO, I approve"). Could bypass veto gates.
- **STRIDE:** Spoofing.
- **Mitigation:** Council vetoes require the specific council's explicit invocation, which is logged. CAO audit samples council-attributed decisions quarterly.
- **Residual risk:** Low (procedural; monitored).

**T-S3. Co-Authored-By spoofing on commits.**
A commit claims Co-Authored-By: Claude without being produced by Claude, muddying governance attribution.
- **Mitigation:** We trust the human author; Co-Authored-By is non-authoritative and is never used alone for accountability. Accountability anchors on the signer / pusher identity (PAT + GitHub account).
- **Residual risk:** Low.

### 4.2 Tampering

**T-T1. Silent rewrite of append-only artifacts.**
Attacker (or well-meaning contributor) amends a session log or removes a LESSONS row to hide a mistake.
- **OWASP ASI:** ASI-08 Unauthorized Modification.
- **STRIDE:** Tampering + Repudiation.
- **Mitigation:** `runtime-hooks/governance-audit` refuses rewrites of append-only paths; `runtime-hooks/commit-gate` blocks such commits; `git reflog` retains old tips for 90 days; branch-protection on `main` (v0.6.0 CI wave) will add PR review requirement.
- **Detection:** any force-push or non-fast-forward on `main` is a Critical finding.
- **Residual risk:** Low. Will drop further at v0.6.0.

**T-T2. Manifest tampering.**
`plugin.json` is edited to add a malicious skill or drop a hook.
- **Mitigation:** Release archive ships with an integrity manifest (hashes of skills + hooks). Install-time check (v0.6.0) compares local to release manifest. Prompt-diff review covers manifest changes in the repo.
- **Residual risk:** Medium today; Low at v0.6.0.

**T-T3. Skill/persona prompt drift via many small edits.**
Over several weeks, a series of small prompt edits softens a skill's posture until it no longer refuses the category it was designed to refuse.
- **OWASP ASI:** ASI-05 Drift.
- **Mitigation:** Prompt-diff council reviews every persona/skill edit; CAO runs a "semantic drift" audit quarterly, comparing current prompts to ratified versions.
- **Residual risk:** Medium without drift audit; Low with audit.

### 4.3 Repudiation

**T-R1. Agent denies having issued a decision.**
"I didn't approve that" becomes unanswerable without receipts.
- **Mitigation:** Every approve/deny/waive/veto event is logged to `sessions/*.log` with actor, timestamp, payload, and outcome. Logs are append-only.
- **Residual risk:** Low.

**T-R2. User denies having granted an approval.**
Rare but possible. Could target USER-ONLY actions.
- **Mitigation:** USER-ONLY approvals require explicit chat confirmation, which is captured in the session log. The log is the authoritative record.
- **Residual risk:** Very low.

### 4.4 Information Disclosure

**T-I1. Raw secret leaked in a session log or artifact.**
Highest-impact, lowest-acceptable scenario.
- **OWASP Top 10:** A02 Cryptographic Failures, A04 Insecure Design.
- **STRIDE:** Information Disclosure.
- **Mitigation:** Non-waivable per [`CONSTITUTION.md`](CONSTITUTION.md) §8.5. Enforced by (a) `runtime-hooks/secrets-scanner` on every session, (b) `runtime-hooks/commit-gate` on every commit, (c) explicit architectural rule: vault-refs only. Skills that touch credentials check `secrets-vault` procedure first.
- **Detection:** secrets-scanner positives are Critical findings even when caught pre-commit; rate is tracked in TRUST.md §3.
- **Residual risk:** Very low. Non-waivable class.

**T-I2. PII leakage across sessions.**
Session A asks about Person X; Session B about Person Y; memory carries A's data into B's artifact.
- **Mitigation:** Memory novelty gate + CMem scoping rules + session-logger boundary. Privacy skill (v0.5.0) adds data-class tagging.
- **Residual risk:** Medium today; Low at v0.6.0 (privacy council layer).

**T-I3. Release archive exfil via compromised PAT.**
An attacker with the PAT can publish malicious releases.
- **Mitigation:** PAT scope minimized (single-repo, limited permissions); rotation on any anomaly; `runtime-hooks/secrets-scanner` blocks local PAT commits; release assets are checked against local hash before publishing.
- **Residual risk:** Low (User custody).

**T-I4. Log verbosity leaking operational metadata.**
Session logs inadvertently log sensitive tool results.
- **Mitigation:** session-logger redacts known sensitive patterns (tokens, emails-in-PII-context). Per-project risk review checks log content.
- **Residual risk:** Low.

### 4.5 Denial of Service

**T-D1. Adversarial long prompt drains context.**
Attacker (via an injected document) stuffs context with content designed to push authoritative instructions out of the window.
- **OWASP ASI:** ASI-04 Context Window Attack.
- **Mitigation:** CLAUDE.md and council charters are read at session start; Immutable Security Rules are in the system prompt (top priority) and cannot be displaced; Agency detects context-pressure and surfaces it rather than continuing silently.
- **Residual risk:** Low-Medium. Research-active area.

**T-D2. Hook loop / infinite re-entry.**
A hook calls a tool that triggers another hook that triggers the first — CPU / token burn.
- **Mitigation:** Hooks have short-circuit on re-entry; session-logger detects loops via stack depth; CSRE runbook for hook-loop recovery.
- **Residual risk:** Very low.

**T-D3. User decision fatigue (human DoS).**
Agency floods User with approval requests; User rubber-stamps.
- **Mitigation:** CRhy aggregates approval requests into structured briefs; approval latency is tracked and low latency is a fatigue signal; Keeper Test includes fatigue scenarios.
- **Residual risk:** Medium. Hard to eliminate; monitored.

### 4.6 Elevation of Privilege

**T-E1. Waiver abuse.**
A legitimate waiver mechanism is used to unblock something it was not meant to unblock.
- **OWASP ASI:** ASI-03 Excessive Agency.
- **Mitigation:** Waivers are USER-ONLY; limited to ≤ 90 calendar days; non-waivable classes exist; CAO waiver review quarterly.
- **Residual risk:** Low.

**T-E2. Tool scope escalation.**
An agent makes a tool call outside the scope granted to its council.
- **Mitigation:** `runtime-hooks/tool-guardian` enforces scope. Per-agent allow-list.
- **Residual risk:** Low.

**T-E3. Agent speaks as CEO / User.**
An agent attempts to take a USER-ONLY action under the guise of "I assume the CEO would approve."
- **Mitigation:** Explicit refusal pattern — the Agency cites the USER-ONLY list and asks explicitly. The ten-item list is memorized at session start.
- **Residual risk:** Very low (drill-tested).

**T-E4. Constitutional amendment under pressure.**
A critical bug + time pressure produces a rushed amendment that weakens a control.
- **Mitigation:** v0.6.0 amendment to Article X adds 7-day cooling-off period and CAO review. Year-one probation rule requires two councils' concurrence.
- **Residual risk:** Medium today; Low at v0.6.0.

---

## 5. Supply-chain threats (zoom-in)

| Threat | Vector | Mitigation |
|---|---|---|
| Malicious dependency | New npm/pip/Cargo package in a tool chain | SPDX SBOM per project; license-checker; allow-list posture; CRT review on new deps |
| Dependency confusion | Public package with same name as a private one | Private registries namespaced; SBOM verification |
| Compromised release key / PAT | Attacker publishes a poisoned release | PAT scope minimized; rotation; release hash check; signed tags target at v0.7.0 |
| GitHub Actions poisoning | Malicious workflow merged via PR | Branch protection + review required on `main` (v0.6.0); workflows pinned by SHA, not tag |
| Typosquatting on plugin name | User installs lookalike | Canonical name + README canonical link + trademark posture per [`SWOT.md`](SWOT.md) T10 |
| SLSA posture gap | Unsigned, forgeable provenance | Level 2 target today; Level 3 by v0.7.0 |

---

## 6. Agent-specific threats — OWASP ASI Top 10 (2025) crosswalk

| ASI # | Threat | Our control |
|---|---|---|
| ASI-01 | Prompt Injection | Immutable Security Rules + injection-defense skill + CRT drill |
| ASI-02 | Unrestricted Delegation | USER-ONLY list (10 actions); tool-guardian hook |
| ASI-03 | Excessive Agency | 8-rung never-give-up ladder; waiver rules |
| ASI-04 | Context Window Attack | System-prompt priority; session-start authoritative reads |
| ASI-05 | Drift | Prompt-diff council; quarterly semantic drift audit |
| ASI-06 | Insecure Memory | Jaccard novelty gate; append-only invariant; CMem review |
| ASI-07 | Identity / Role Confusion | Council names + explicit invocation patterns; CAO audit |
| ASI-08 | Unauthorized Modification | governance-audit + commit-gate hooks; append-only paths |
| ASI-09 | Insufficient Logging | session-logger (mandatory); receipts ratio target 100% |
| ASI-10 | Over-Permissive Tools | tool-guardian allow-list; per-council scope |

---

## 7. NIST AI RMF 1.0 crosswalk

| Function | How we address it |
|---|---|
| **Govern** | [`CONSTITUTION.md`](CONSTITUTION.md), [`GOVERNANCE.md`](GOVERNANCE.md), CGov council, USER-ONLY list |
| **Map** | Per-project threat models + this plugin-level model; [`SYSTEM-CARD.md`](SYSTEM-CARD.md) |
| **Measure** | [`TRUST.md`](TRUST.md) §3 scorecard; Keeper Test quarterly; CEVO checklists |
| **Manage** | CIR incident response; waiver mechanism; CAO audit; RCA skill (v0.5.0) |

---

## 8. Assumptions

These are the assumptions under which the threat model holds. If any becomes false, re-model.

- The User's account credentials are not compromised.
- Anthropic's Claude endpoint is not compromised.
- Git history on GitHub origin has not been silently rewritten.
- The local machine running the plugin is not compromised at the OS level.
- Hooks are running (not disabled by a User with legitimate intent to bypass).
- The clock is accurate enough for waiver-expiry math.

---

## 9. Residual risk summary

| Category | Today | At v0.6.0 target | At v0.7.0 target |
|---|---|---|---|
| Injection (S1, D1) | Low | Low | Low |
| Tampering (T1, T2, T3) | Low-Medium | Low | Very low (signed provenance) |
| Info Disclosure (I1 raw secrets) | Very low | Very low | Very low |
| Info Disclosure (I2 PII cross-session) | Medium | Low | Low |
| DoS (D3 User fatigue) | Medium | Medium | Low (onboarding + aggregation) |
| Elevation (E4 amendment abuse) | Medium | Low | Very low |
| Supply chain (compromised release) | Low | Low | Very low (SLSA L3) |

**Interpretation:** the plugin is launch-safe at v0.5.0 for its intended use-cases. The medium-risk items have concrete, dated mitigations in [`SWOT.md`](SWOT.md) §5 roadmap.

---

## 10. Review cadence

- **Every Keeper Test:** re-walk every STRIDE category against the latest drill script. Add new threats; retire resolved ones.
- **Every minor version bump:** update residual-risk table and the ASI / AI RMF / MITRE crosswalk.
- **After any Critical incident:** re-walk within 14 days of incident closure.

---

## 11. Document control

- **File:** `THREAT-MODEL.md`
- **Version:** 1.0
- **Owner:** CRT
- **Reviewer:** CISO
- **Append-only:** No (revised document; history in git)
- **References (original synthesis):**
  - Shostack, *Threat Modeling: Designing for Security* (2014) — STRIDE methodology.
  - OWASP Top 10 (2021).
  - OWASP Agent Security Initiative (ASI) Top 10 (2025 draft).
  - NIST AI Risk Management Framework 1.0 (2023).
  - MITRE ATT&CK Enterprise + MITRE ATLAS.
  - SLSA specification v1.0.
  - CNCF Security Whitepaper v2.0.

---

*A threat model that is not revised quarterly is a threat model that is wrong.*
