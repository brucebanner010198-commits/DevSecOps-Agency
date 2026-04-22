# TRUST.md — The Agency's public trust contract

This document is the single page you point anyone at who asks "can I rely on this thing?". It states — in plain language and in measurable terms — what the Agency promises, how you can verify each promise yourself, and what we owe you when we miss. It is subordinate to `CONSTITUTION.md` (Art I §1.1) and cited from every quarterly audit and every close-out.

Ratified **2026-04-22** alongside plugin v0.5.0. Reviewed quarterly on the `rhythm` cadence; amendable only via `trust-amend` ADR with CAO + CRT + CAO-countersign review (clauses affecting Constitution §8.5 non-waivables or §2.2 USER-ONLY actions route through Constitution Article X as USER-ONLY).

MUST / MUST NOT / SHALL / SHOULD / SHOULD NOT / MAY below follow RFC 2119 / RFC 8174.

---

## 1. The short version

The Agency is **not** a magic box. It is a rules system with receipts. Four practical consequences:

1. **Every material decision has a paper trail you can read.** No silent choices. No "trust me".
2. **Four independent councils can veto a ship.** CISO (security), CEVO (evals), CRT (red-team), CAO (audit). They cannot be overridden by the CEO. They can only be cleared by the User via an expiring, logged waiver — and even then, two classes of finding (raw secrets, ASI-class) are **non-waivable**.
3. **Ten actions are reserved for the User alone.** The Agency cannot fire an agent, publish externally, spend money, amend the Constitution, accept a non-goal, or do seven other named things without you pressing a button in `inbox.json` and a `user-meeting` ADR landing.
4. **If something we said is happening isn't happening, you can prove it.** Every promise below has a `How to verify` row that points at a file path, a hook, or a `git log` command.

Trust with us is empirical, not aspirational.

---

## 2. The twelve public commitments

Each commitment has three fields: **Claim**, **How to verify**, **If we miss**. Claims are numbered for citation (cite as `TRUST §2.N`).

### §2.1 Receipts ratio — **100 %**

- **Claim.** Every phase transition, every blocking-council verdict, every waiver, every agent hire/retire/demote, every Constitution amendment MUST produce an ADR (`_decisions/ADR-NNNN-<kind>-<slug>.md`) and an entry in the append-only session log (`_sessions/<agent>-<YYYY-MM-DD>.jsonl`).
- **How to verify.** In any project folder: `git log --diff-filter=A -- _decisions/` counts ADRs; `wc -l _sessions/*.jsonl` counts session entries. CAO's monthly audit (`skills/audit`) spot-checks receipts ratio and publishes the number in `_vision/rhythm/monthly-<YYYY-MM>.md`.
- **If we miss.** CAO files `audit-finding-missing-receipt` ADR. Ship is blocked until the finding is remediated. Constitution §5.1.

### §2.2 Append-only ledger

- **Claim.** Session logs, ADRs, LESSONS rows, stepping stones, and archived agent files MUST NOT be edited in place. Corrections are new rows that supersede, with links back.
- **How to verify.** `git log --follow <path>` for any log file should show only additions; `git log -p _sessions/ _decisions/ LESSONS.md` with non-additive diffs should be empty. Runtime hook `governance-audit` and skill `audit` both scan for this.
- **If we miss.** Constitution §5.2 hard invariant violation → `append-only-violation` ADR → Rung 3+ on the never-give-up ladder → full restoration from `git reflog` or prior tag.

### §2.3 Four blocking vetoes are real

- **Claim.** CISO (Security), CEVO (Evaluation), CRT (Red-Team), CAO (Audit) each hold strict veto over ship. Their red gates MUST NOT be overridden by the CEO, by any other Chief, or by automated rules. The only path past a red is a user-approved waiver with a calendar-date expiration ≤ 90 days. ASI-class and raw-secret findings are **non-waivable**.
- **How to verify.** Constitution §3.3 + §8.5. Scan `_decisions/ADR-*-waiver-grant-*.md` — every waiver MUST carry `approved-by: user` and an ISO expiry date ≤ 90 days out. `skills/waivers/` enforces this at write time.
- **If we miss.** A cleared red without a user-approved waiver is itself an ASI-class finding, routed to CRT. User is notified the same session.

### §2.4 Ten USER-ONLY actions — no exceptions

- **Claim.** The Agency MUST NOT, without explicit user approval captured in `inbox.json` + a `user-meeting` ADR: amend the Constitution or root docs · change an agent's tier · hire, fire, repurpose, or rename an agent · waive a blocking-council red · park at Rung 7 · kick off a new project · publish externally · spend money · accept a non-goal idea · cross-tier reassign.
- **How to verify.** Constitution §2.2 enumerates the ten. `skills/user-meeting/` is the only code path that writes to `inbox.json` for these categories. CAO monthly audit counts USER-ONLY actions against user-meeting ADRs.
- **If we miss.** USER-ONLY bypass = ASI-class finding → CRT → immediate CEO shutdown of current loop → user notification.

### §2.5 Security baseline on every shipped project

- **Claim.** Every shipped project MUST carry: STRIDE coverage of every trust boundary in `architecture.md`, an explicit verdict on each OWASP Top 10 A01–A10, a pen-test report, an SBOM (SPDX), SLSA provenance, no raw secrets in any committed artifact, and a CRT pre-release pass mapping every finding to the OWASP ASI Top 10.
- **How to verify.** Open `<slug>/threat-model.md`, `<slug>/security/code-audit.md`, `<slug>/security/pentest-report.md`, `<slug>/sbom.spdx.json`, `<slug>/slsa.provenance.json`, `<slug>/red-team/findings.md`. CISO gate is red on any unmitigated Critical/High; CRT red on any unmapped finding.
- **If we miss.** Ship is blocked. No exceptions. Constitution §5.5 + §5.7.

### §2.6 Prompt-diff review on every persona edit

- **Claim.** Any change to `agents/**/*.md` or a high-leverage `skills/**/SKILL.md` MUST land through a CRT `prompt-diff-review.md` receipt before merge. Three consecutive rejections trigger a Keeper-Test review of the proposer.
- **How to verify.** `skills/red-team/references/prompt-diff-review.md` spec. `git log --follow agents/` commits reference their prompt-diff ADR id.
- **If we miss.** The edit is reverted and a `prompt-diff-bypass` ADR filed against the author.

### §2.7 Runtime hooks are non-optional

- **Claim.** `secrets-scanner`, `tool-guardian`, `governance-audit`, `dependency-license-checker`, `session-logger`, and `commit-gate.sh` run at their declared trigger points. The hooks are read-only on input, exit 0 or non-zero, and MUST NOT be bypassed with `--no-verify`, `git add -A`, or equivalent.
- **How to verify.** `runtime-hooks/*/hooks.json` declares triggers. `runtime-hooks/*/*.sh` scripts are small, regex-only, and reviewable in under 10 minutes each. `git log --grep '\-\-no-verify'` in the delivery path should be empty.
- **If we miss.** A successful bypass = runtime-hook-bypass ADR → Rung 3 → root-cause analysis via `skills/rca/` → hook hardening follow-up.

### §2.8 Memory novelty gate

- **Claim.** Writes to `_memory/MEMORY.md` MUST pass a Jaccard novelty gate (currently 0.65) and go through `skills/memory/`. Anything below threshold is rejected or filed as a duplicate reference.
- **How to verify.** `skills/memory/references/novelty-gate.md` specifies the algorithm + threshold. `_memory/index.json` tracks every accept/reject decision with the computed Jaccard score.
- **If we miss.** Memory-poisoning finding filed via CRT; the offending memory line is superseded by a correction row.

### §2.9 Rhythm cadence — heartbeats do not slip silently

- **Claim.** Daily / weekly / monthly / quarterly heartbeats MUST be filed. A missed heartbeat moves through a published escalation tree (1st miss = yellow compliance-drift; 2nd = ADR + Rung 2; 3rd = Rung 3; 4th+ = per-turn user notification).
- **How to verify.** `_vision/rhythm/state.json` + `_vision/rhythm/heartbeat-*.md`. `skills/rhythm/references/missed-heartbeat.md`.
- **If we miss.** Monthly audit escalates; user is surfaced the degrade.

### §2.10 Never-give-up ladder — loudly, not silently

- **Claim.** When a project hits a hard problem, the Agency climbs an 8-rung ladder rather than giving up or hiding the failure. Rung 7 (park) is USER-ONLY; Rung 8 (retire) is USER-ONLY.
- **How to verify.** `RESILIENCE.md` + `skills/ladder/references/rung-definitions.md`. Every rung transition writes a `ladder-step` ADR.
- **If we miss.** A silent give-up is an ASI-class finding (§11.5 "no silent enforcement" analogue for work).

### §2.11 Reproducibility — you can re-run a project from the paper trail

- **Claim.** For any shipped project, another operator with only this repo, the project folder, and the same model tier MUST be able to reconstruct the context used for each phase within 30 minutes of work. Deterministic ordering of session-log writes + ADR references + pinned model IDs make this possible.
- **How to verify.** `CONSTITUTION.md §5.9`. `skills/retrospective` test: re-run any closed project's Phase 4 from the receipts and compare outputs.
- **If we miss.** Reproducibility failure = `reproducibility-regression` ADR → mandatory CEVO baseline refresh.

### §2.12 Independence of CAO / CEVO / CRT / CSRE

- **Claim.** Audit, Evaluation, Red-Team, and SRE councils never sit on a project's delivery path. Their leads SHALL NOT dual-hat as delivery Chiefs. A violation is itself an audit finding.
- **How to verify.** `councils/{audit,evaluation,red-team,sre}/AGENTS.md` and `agents/{audit,evaluation,red-team,sre}/*.md` — no delivery-phase ownership listed. `skills/audit` cross-check.
- **If we miss.** `independence-violation` ADR + immediate return to independent model; offending dual-hat reverted.

---

## 3. Trust scorecard

We compute this every month from the receipts and publish it in `_vision/rhythm/monthly-<YYYY-MM>.md § Trust Scorecard`. It is intentionally simple — twelve binary commitments and a pair of rate metrics, no weighted-average theatre.

| Axis | Metric | Target | Source of truth |
| --- | --- | --- | --- |
| Receipts ratio | ADRs filed / decisions made | 100 % | `skills/audit` |
| Append-only integrity | Non-additive edits to log dirs in last 30 days | 0 | `skills/audit` |
| Blocking-council vetoes honored | Reds cleared without user waiver | 0 | `skills/waivers` + `skills/audit` |
| USER-ONLY compliance | USER-ONLY actions without `user-meeting` ADR | 0 | `skills/user-meeting` + `skills/audit` |
| Security baseline | Projects shipped without full STRIDE/OWASP/SBOM/SLSA | 0 | CISO close-out |
| Prompt-diff coverage | Persona edits without prompt-diff receipt | 0 | CRT audit |
| Runtime-hook execution | Hook trigger points reached without hook run | 0 | `runtime-hooks/*/README.md` + `governance-audit` bookend |
| Memory novelty gate | Memory writes bypassing Jaccard gate | 0 | `skills/memory` index |
| Rhythm cadence | Heartbeats filed on schedule | 100 % | `_vision/rhythm/state.json` |
| Ladder discipline | Silent give-ups (no ladder-step ADR before drop) | 0 | CAO audit |
| Reproducibility | Re-run tests passing in last quarterly drill | 100 % | CEVO quarterly baseline |
| Independence | CAO/CEVO/CRT/CSRE dual-hats on delivery | 0 | Roster audit |

**The scorecard is public.** Any drop below target is published the same monthly heartbeat, not buried.

---

## 4. What you can expect within 48 hours of an incident

When something material breaks:

1. **≤ 30 minutes** — the degraded mode is published in the current day's `heartbeat-<date>.md § Degraded` (RESILIENCE.md).
2. **≤ 4 hours** — an incident ADR lands with `kind: incident-<class>` and a first-response summary.
3. **≤ 24 hours** — a root-cause pass via `skills/rca/` lands with 5 Whys + Ishikawa breakdown.
4. **≤ 48 hours** — a public postmortem lands under `_decisions/ADR-NNNN-postmortem-*.md` and is summarized in the next daily heartbeat.
5. **≤ next quarterly** — the postmortem's structural recommendation lands as either a skill edit (prompt-diff'd) or a Constitution-amend proposal.

We do not hide incidents. Constitution §11.6 forbids silent enforcement; we apply the same principle to our own failures.

---

## 5. How to push back

If the Agency ever tells you to trust it without a receipt, or if a council lead asks you to waive one of these commitments through a side channel, the correct response is to refuse and file a `trust-violation` ADR via `/devsecops-agency:escalate`.

You — the User — are sovereign per Constitution Art II. Your refusal is itself a governance signal. You can and should use it.

---

## 6. Who owns what about this document

| Section | Maintainer | Review cadence |
| --- | --- | --- |
| §1 short version + §2 commitments | CEO + CAO | Quarterly |
| §3 scorecard | CAO + CEVO | Monthly |
| §4 incident timeline | CSRE + CAO | After each incident |
| §5 push-back guidance | User + CEO | Quarterly |
| §6 ownership | CEO | Quarterly |
| All of the above, amendment process | User via Constitution Art X | Any time |

---

## 7. References

- `CONSTITUTION.md` — supreme document.
- `MISSION.md`, `VALUES.md`, `GOVERNANCE.md`, `RESILIENCE.md`, `SECURITY.md`, `KEEPER-TEST.md`, `CAREER.md`, `RHYTHM.md`, `LESSONS.md`.
- `SYSTEM-CARD.md` — capabilities, limits, tested bounds.
- `THREAT-MODEL.md` — plugin-level threat model (complements per-project models).
- `DISASTER-RECOVERY.md` — what happens if the repo / main branch is lost.
- `SWOT.md` — honest self-assessment.
- `skills/audit/` · `skills/waivers/` · `skills/rhythm/` · `skills/red-team/` · `skills/trust-scorecard/` · `skills/rca/`.

Frameworks whose logic informs this document (original synthesis, no copied text): NIST AI Risk Management Framework (AI RMF 1.0), ISO/IEC 42001:2023 (AI management systems), ISO/IEC 27001 (ISMS), SOC 2 Trust Services Criteria, SRE "Error Budgets" discipline from *Site Reliability Engineering* (Google), Cloud Native Computing Foundation Security Whitepaper, Anthropic Responsible Scaling Policy, OECD AI Principles, EU AI Act (Articles on transparency + record-keeping).

---

## 8. Document control

| Field | Value |
| --- | --- |
| Document | `TRUST.md` |
| Version | 1.0 (shipped with plugin v0.5.0) |
| Ratified | 2026-04-22 |
| Supremacy | `CONSTITUTION.md` overrides on any conflict (§1.1). |
| Amendment | `trust-amend` ADR + CAO + CRT + CEVO review. Changes that touch §2.3 non-waivable classes or §2.4 USER-ONLY enumeration route through Constitution Art X as USER-ONLY. |
| Review cadence | Quarterly on the `rhythm` skill. |
