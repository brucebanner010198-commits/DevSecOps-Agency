# System Card — DevSecOps-Agency

**Version:** 1.0
**Ratified:** 2026-04-22
**Plugin version at card publish:** v0.5.0
**Authority:** [`CONSTITUTION.md`](CONSTITUTION.md) Article III (Transparency)
**Owner:** CEVO · **Reviewer:** CAO · **Cadence:** regenerated at every minor version bump (v0.X.0)
**Classification:** Public

---

## 0. Purpose

A system card is a single document a reasonable third party (auditor, new User, researcher, regulator) can read in 15 minutes and walk away with an **accurate** picture of what this system **is, can do, cannot do, has been tested against, and is known to fail at.**

This card is written in the pattern of Anthropic, OpenAI, and Google model-card / system-card publications, adapted to a multi-agent agency plugin rather than a base model.

**If any claim here is overstated, a waiver is required per [`CONSTITUTION.md`](CONSTITUTION.md) §8. A false claim is a Critical-severity governance finding.**

---

## 1. What DevSecOps-Agency is

A Claude Code plugin that turns a single Claude session into a multi-council software agency with constitutional governance. It ships:

- **1 CEO** — the single point of coordination and USER-facing communication.
- **16 councils** — Security (CISO), Red-Team (CRT), Evaluation (CEVO), Audit (CAO), Reliability (CSRE), Incident Response (CIR), Governance (CGov), Ethics (CEthics), Technology (CTE), Knowledge Transfer (CKT), Rhythm (CRhy), Career (CCar), Planning (CPlan), Memory (CMem), Resilience (CRes), plus supporting councils.
- **92 agents** — chief, specialist, and worker tiers across the councils.
- **66 skills** — reusable procedures invoked by agents on demand.
- **6 runtime hooks** — `secrets-scanner`, `tool-guardian`, `governance-audit`, `dependency-license-checker`, `session-logger`, `commit-gate`.
- **14 founding documents** — Constitution, Mission, Values, Agents, Governance, Security, Trust, SWOT, System-Card (this file), Rhythm, Career, Keeper-Test, Resilience, Lessons.

The plugin is delivered as `devsecops-agency-v0.5.0.plugin` — a stored zip archive.

---

## 2. Intended use

DevSecOps-Agency is designed for:

- **Security-sensitive software work** — threat modeling, security review, code review with CISO + CRT gates.
- **Governance-demanding work** — projects where waivers, approvals, and append-only audit trails are required.
- **Multi-domain coordination** — tasks spanning development, reliability, compliance, privacy, and ethics.
- **A single primary User** operating as the CEO-equivalent stakeholder.
- **One-shot or long-horizon projects** where the append-only invariant protects the work.

It is **not** designed for:

- Unsupervised autonomous shipping. USER-ONLY actions require the User, not an agent.
- Financial transactions, production deploys, legal commitments, model-scale decisions, or ASI-class requests — all are USER-ONLY.
- Environments that require a different governance pattern (e.g., regulated healthcare with HIPAA officer roles not yet mapped).

---

## 3. Capabilities (what the Agency has been designed and tested to do)

### 3.1 Governance

- Enforce constitutional precedence — all founding docs subordinate to [`CONSTITUTION.md`](CONSTITUTION.md).
- Enumerate the **10 USER-ONLY actions** explicitly; refuse to proceed on any without explicit User approval.
- Maintain append-only session logs, ADRs, LESSONS rows, and stepping-stone trails.
- Invoke the **8-rung never-give-up ladder** with transparent escalation (Rungs 7 & 8 USER-ONLY).
- Hold four independent blocking vetoes (CISO, CRT, CEVO, CAO).
- Run the quarterly **Keeper Test** adversarial drill.

### 3.2 Security

- Per-project threat modeling using STRIDE, OWASP Top 10 (2021), OWASP ASI Top 10 (2025), NIST AI RMF 1.0.
- Runtime hooks: secrets-scanner (blocks raw-secret commits), tool-guardian (blocks out-of-scope tool calls), commit-gate (blocks forbidden commits), dependency-license-checker, governance-audit, session-logger.
- Vault-refs only for credentials; non-waivable per [`CONSTITUTION.md`](CONSTITUTION.md) §8.5.
- Vulnerability disclosure + coordinated 90-day window per [`SECURITY.md`](SECURITY.md).
- Supply-chain posture: SPDX SBOM per project, SLSA Level 2 target.

### 3.3 Quality, Reliability, Audit

- CEVO evaluation checklists on every shipped artifact.
- CAO audit trails with full receipts ratio target 100%.
- CSRE reliability patterns — error budgets, incident response runbooks, blameless post-mortems.
- CIR incident response with 30-min ack, 4-hour containment, 24-hour triage, 48-hour User report for Severity ≥ High.

### 3.4 Ethics & Responsibility

- CEthics ethical review on requests touching people, populations, or power.
- Alignment with Anthropic Responsible Scaling Policy and Anthropic Usage Policies.
- ASI-class requests are non-waivable — refused by the Agency and escalated only to the User for awareness, never for action.

### 3.5 Knowledge & Career

- Append-only LESSONS ledger captures learning across projects.
- CRhy enforces rhythm and cadence (prevents silent slips).
- CCar supports career-ladder work for the User's own development (see [`skills/career-ladder`](skills/career-ladder)).

---

## 4. Limits (what the Agency cannot or will not do)

**Will not** (refuse by design):

- Execute trades, transfer funds, or initiate financial transactions.
- Accept legally binding terms on the User's behalf.
- Publish to public channels without explicit User approval.
- Store, log, or transmit raw secrets (architecturally impossible via hooks + vault-refs).
- Honor an amendment to the non-waivable classes (raw-secrets, ASI) without a new Constitutional version.
- Produce disinformation, targeted harassment, facial recognition of non-consenting subjects, or content that violates Anthropic Usage Policies.

**Cannot** (capability bound):

- Operate without a User — no peer override exists for USER-ONLY actions in v0.5.0 (a deputy pattern is planned for v0.8.0, see [`SWOT.md`](SWOT.md) W4).
- Verify external claims beyond what the User or a connected tool provides — we do not independently re-verify the internet.
- Guarantee against novel model-behavior drift — we mitigate via version pinning and Keeper Test re-runs, but cannot eliminate.
- Reason about physical or real-time systems with sub-second precision.
- Scale to multi-tenant teams in v0.5.0 — single-User model only.

**Has not been tested against** (honest territory markers):

- Sustained pressure of many concurrent projects (>5 at once). See [`SWOT.md`](SWOT.md) W16.
- Adversarial waiver requests under time pressure (first Keeper Test drill: 2026-04-30).
- Post-quantum-cryptography impact on vault-ref patterns.
- Regulatory audit by an external auditor (planned v0.7.0, see [`SWOT.md`](SWOT.md) O3).

---

## 5. Evaluation methodology

The Agency is evaluated on four dimensions.

### 5.1 Governance integrity — CAO

- **Metric:** Receipts ratio (decisions logged / decisions made). **Target: 100%.**
- **Metric:** Append-only invariant (rewrites detected / period). **Target: 0.**
- **Metric:** USER-ONLY bypass attempts (by agent, blocked). **Target: 0 unblocked.**
- **Cadence:** Weekly sampling; quarterly summary in [`TRUST.md`](TRUST.md) §3.

### 5.2 Security posture — CRT + CISO

- **Metric:** Secrets-scanner hits before commit-gate (should be 0 at commit; >0 in dev is fine).
- **Metric:** Dependency-license-checker violations.
- **Metric:** Time-to-acknowledge for reported vulnerabilities. **Target: ≤ 48h.**
- **Metric:** Time-to-patch Critical. **Target: ≤ 7 calendar days.**

### 5.3 Quality — CEVO

- **Metric:** Prompt-diff review compliance rate on persona/skill edits. **Target: 100%.**
- **Metric:** Artifacts shipped without CEVO checklist. **Target: 0.**
- **Metric:** Post-ship defect rate (defects traced to missed checklist items / total ships).

### 5.4 Drill — Keeper Test quarterly

- **Metric:** Injection attacks caught. **Target: 100%.**
- **Metric:** Waiver-abuse attempts refused. **Target: 100%.**
- **Metric:** ASI-class refusals. **Target: 100%.**
- **Metric:** Novel findings generated per drill. **Target: ≥ 3 — a drill producing zero novel findings is itself a finding.**

All metrics are published in [`TRUST.md`](TRUST.md) §3 each quarter.

---

## 6. Known failure modes

Every system fails in known ways. Here are the ones we've anticipated and what we do about them.

### 6.1 Agreeableness drift — T12 in [`SWOT.md`](SWOT.md)

The subtlest failure. Over time, the Agency wants to please. Mitigation: veto-rate tracking and CAO missed-veto audits. If vetoes trend to zero without a corresponding drop in high-severity findings, the system is drifting.

### 6.2 Waiver creep

Waivers are legitimate but can accumulate. Mitigation: 90-day calendar expiry (automatic), USER-ONLY approval, CAO quarterly waiver review.

### 6.3 Memory bloat

Append-only means we never delete, but we can get noisy. Mitigation: Jaccard novelty gate (0.65) blocks duplicate additions; growth budget (v0.8.0) will add a secondary check.

### 6.4 Council staleness

A council defined in markdown but never invoked is theatre. Mitigation: quarterly council-invocation report. A council with <1 invocation in 90 days triggers a review — either it was never needed, or work is routing around it.

### 6.5 Single-User bottleneck — W4 in [`SWOT.md`](SWOT.md)

If the User is unreachable for >72h, the Agency enters read-only mode per [`DISASTER-RECOVERY.md`](DISASTER-RECOVERY.md). Analysis continues, shipping does not.

### 6.6 Knowledge loss in long sessions

Session context windows are bounded. Mitigation: CMem extracts decisions into LESSONS rows; append-only session logs survive restart; ADRs carry the strategic content.

### 6.7 Platform change breaking the plugin — T9 in [`SWOT.md`](SWOT.md)

Claude Code manifest schema changes. Mitigation: schema version pinned in `.claude-plugin/plugin.json`; compatibility check within 7 days of any platform release.

### 6.8 Supply-chain compromise — T2 in [`SWOT.md`](SWOT.md)

A dependency is backdoored. Mitigation: SBOM + license-checker + SLSA target + DISASTER-RECOVERY procedure.

---

## 7. Inputs the Agency accepts

- **Natural-language User instructions** — treated as trusted (source: chat interface).
- **Files under `_ship/`** — treated as trusted (User has curated them).
- **Tool results from MCPs** — treated as **untrusted data** per critical_injection_defense rules.
- **Web content via WebFetch / WebSearch** — **untrusted data.**
- **Emails, messages, PDFs** — **untrusted data by default.**
- **Clipboard contents** — **untrusted data.**

Any instruction discovered in the untrusted categories requires User verification before action, per the Immutable Security Rules baked into the Agency's operational prompt.

---

## 8. Outputs the Agency produces

- **Session responses to the User** — in chat.
- **Files in the workspace folder** `/sessions/loving-adoring-maxwell/mnt/outputs/` — deliverables, artifacts, release archives.
- **Appended rows in LESSONS, session logs, ADRs** — governance receipts.
- **Git commits on `main`** — content changes, signed with Co-Authored-By trailer per repository convention.
- **GitHub Releases + assets** — versioned, tag-pinned release archives with release notes.

Outputs that have legal, financial, or public-visibility consequence pass through USER-ONLY gates before emission.

---

## 9. Dependencies

- **Claude (Anthropic)** — the base model. Model version pinned in [`CLAUDE.md`](CLAUDE.md).
- **Claude Code** — the plugin host. Manifest schema version pinned in `.claude-plugin/plugin.json`.
- **Git + GitHub** — source of truth for the repo, release hosting.
- **No runtime network dependencies** beyond those required by specific tool calls (WebFetch, connector MCPs).

---

## 10. Environmental considerations

Token-per-session cost is non-trivial for long councils. Sustainability council (O9 in [`SWOT.md`](SWOT.md)) planned for v1.0.0. Until then, cost is tracked informally.

---

## 11. Change control

- **Minor version bumps (v0.X.0):** regenerate this card. `skills/system-card/SKILL.md` (v0.5.0) provides the procedure.
- **Patch version bumps (v0.X.Y):** this card does not require regeneration unless capabilities or limits actually changed.
- **Emergency card updates:** if a capability/limit claim here is discovered false, the card is patched within 48h, the correction is logged, and the root cause is surfaced in an RCA via `skills/rca/SKILL.md`.

---

## 12. Disclosures

- **The Agency is self-certified.** No third-party audit has been performed as of v0.5.0. External audit targeted for v0.7.0 (see [`SWOT.md`](SWOT.md) O3).
- **The Constitution is new** — ratified 2026-04-20. Probation period is 12 months.
- **The trust scorecard** ([`TRUST.md`](TRUST.md) §3) is defined but has not yet published its first quarterly scorecard. First publication: 2026-07-22.
- **No SOC 2, ISO 27001, ISO 42001, or FedRAMP certification exists.** Alignment is claimed; certification is not.
- **The plugin is MIT licensed.** Forks may strip safety controls — the name "DevSecOps-Agency" belongs to this repository; forks using similar names without the USER-ONLY list and non-waivable classes are not endorsed.

---

## 13. Document control

- **File:** `SYSTEM-CARD.md`
- **Version:** 1.0
- **Regenerated by:** `skills/system-card/SKILL.md`
- **Owner:** CEVO
- **Reviewer:** CAO
- **References:** Anthropic model cards (pattern); Google model card paper (Mitchell et al., 2019, "Model Cards for Model Reporting"); NIST AI RMF 1.0; ISO/IEC 42001:2023.

---

*A system is what it claims to be only when those claims are both public and falsifiable.*
