---
name: privacy
description: >
  Apply privacy-by-design to any project touching personal data.  Runs a
  screening DPIA, classifies data against GDPR / CCPA / DPDP categories,
  generates a data-flow diagram + retention policy, and produces the
  privacy appendix for the project's ADR.  Trigger phrases include
  "privacy review", "DPIA", "GDPR check", "CCPA", "DPDP", "PII review",
  "is this legal to store", "data minimization", "retention policy",
  "right-to-erasure", "data subject request", or any /devsecops-agency:privacy
  invocation.  Also invoked automatically by the project-start checklist
  when any input data appears to contain personal data.
metadata:
  version: "1.0.0"
---

# privacy — Privacy-by-design review + DPIA

Authority: [`CONSTITUTION.md`](../../CONSTITUTION.md) + [`SECURITY.md`](../../SECURITY.md) + [`VALUES.md`](../../VALUES.md)
Owner: CISO (today) → CPRIV (v0.6.0) · Reviewer: CAO
Called from: `skills/ship-it-kickoff`, `skills/security-review`, `skills/audit`

## When to trigger

REQUIRED when any of the following are true:

- Input data contains or might contain personal identifiers (name, email, phone, address, government ID, device identifier, cookies/IDs, biometric, geolocation, voice).
- Output will be published, shared across orgs, or retained > 30 days.
- Processing is cross-border (data moves across jurisdictions).
- Processing is at scale (> 1000 subjects) OR involves sensitive categories (health, sex, religion, political, union, genetic, biometric, children < 16, criminal).
- Processing includes automated decision-making that affects a person (employment, credit, housing, healthcare, legal).
- A Data Subject Request (DSAR) or right-to-erasure request arrives.

OPTIONAL (but recommended) when handling non-personal but commercially sensitive data that could become personal via re-identification.

## Procedure

### Step 1 — Data classification

Classify every input field against this matrix:

| Class | Definition | Examples |
|---|---|---|
| **P0 — Identifier** | Directly identifies a person | Name, email, phone, government ID, passport |
| **P1 — Quasi-identifier** | Identifies when combined | ZIP + DOB + gender, device ID, cookie ID, precise geolocation |
| **P2 — Sensitive (special category)** | GDPR Art. 9 / CCPA Sensitive / DPDP Sensitive | Health, sex life, religion, political, biometric, genetic, children's data |
| **P3 — Non-personal** | No link to person | Aggregate stats, published research data |

Every P0 or P2 field requires an explicit lawful basis (next step).

### Step 2 — Lawful basis identification (GDPR Art. 6 framing; maps to CCPA/DPDP analogues)

Pick exactly one per processing activity:

- **Consent** — freely given, specific, informed, unambiguous, revocable.
- **Contract** — necessary to perform a contract with the data subject.
- **Legal obligation** — compliance with a law.
- **Vital interests** — protect life.
- **Public task** — exercise of official authority.
- **Legitimate interests** — balanced against data-subject rights (**requires a Legitimate Interests Assessment** documented inline).

If no basis applies, processing does not proceed.

### Step 3 — Screening DPIA (decide whether full DPIA is required)

Run the screening checklist (GDPR Art. 35 + CNIL guidance; works as a conservative baseline across CCPA / DPDP):

- [ ] Large-scale processing of P2 data?
- [ ] Large-scale systematic monitoring of public area?
- [ ] Children's data?
- [ ] Automated decision with legal/significant effect?
- [ ] Cross-border transfer to a country without adequacy?
- [ ] Novel technology used in a way the subject would not reasonably expect?
- [ ] Prevents subject from exercising a right or using a service?

**If ≥ 2 boxes checked → full DPIA.** If 1 or 0 → proceed with the lightweight privacy appendix only.

### Step 4 — Data-flow diagram

Produce a markdown data-flow diagram showing:

- **Sources** (where data enters).
- **Processors** (every agent / tool / hook / council that touches it).
- **Stores** (where it rests, including session logs and LESSONS).
- **Recipients** (where it exits, if at all).
- **Jurisdictions crossed** (annotate edges with the jurisdictions involved).

Any data store with PII must also appear in the retention table (Step 6).

### Step 5 — Minimization & purpose limitation check

For each field ask: **Is this field strictly necessary to achieve the stated purpose?**

- If yes → keep and document why.
- If no → remove it from the flow. Log the minimization decision.

For each purpose ask: **Is processing bounded to this purpose?** Secondary processing for a different purpose requires a new lawful basis.

### Step 6 — Retention policy

For each data class list: field → retention period → deletion trigger → deletion method.

Defaults (can be overridden with justification):

- P0 session-log mentions: 180 days, then redacted from session-logger output.
- P2 fields: NOT stored in session logs at all; redact at capture time.
- Artifacts produced for the User: retained per the User's choice.
- Vault-refs to credentials: non-expiring but rotatable; never raw values.

### Step 7 — Subject rights readiness

Confirm each right can be exercised by our process:

- **Access** — can we produce everything we hold about a subject?
- **Rectification** — can we correct it?
- **Erasure** — can we delete it, and does append-only interfere? **Note:** append-only does not block erasure. We redact in place with a structured `[ERASED YYYY-MM-DD subject: <ref>]` marker; the *metadata of the deletion event* is append-only.
- **Portability** — can we export in a machine-readable format?
- **Objection / restriction** — can we stop processing for this subject?
- **Not subject to automated decision-making** — can we provide human review?

A right we cannot honor is a Critical finding; either add the capability or stop processing the class of data that triggers the right.

### Step 8 — Cross-border transfer check

If data crosses borders:

- Adequacy decision? If yes → document and proceed.
- Standard Contractual Clauses (SCCs)? If yes → attach.
- Binding Corporate Rules? If yes → attach.
- Explicit consent + informed? If yes → attach the consent language.
- None of the above → do not transfer.

For DPDP (India): transfer is permitted unless to a country in the negative list (MeitY notification). Confirm current list.

For CCPA (California): no cross-border restriction, but notice + opt-out obligations apply to "sale" or "sharing".

### Step 9 — Children's data (if applicable)

If subjects may include children < 16 (GDPR) / < 13 (COPPA, US) / as defined locally:

- Parental consent mechanism?
- Age-verification approach?
- Reduced-processing default (no behavioral ads, no profiling)?

If none can be established, do not process.

### Step 10 — Write the Privacy Appendix

The appendix becomes part of the project's ADR. Sections:

1. **Data classification** — from Step 1.
2. **Lawful basis** — from Step 2.
3. **DPIA disposition** — screening result + full DPIA if triggered.
4. **Data-flow diagram** — from Step 4.
5. **Minimization decisions** — from Step 5.
6. **Retention policy** — from Step 6.
7. **Subject-rights readiness** — from Step 7.
8. **Cross-border transfers** — from Step 8.
9. **Children's data** — from Step 9.
10. **Residual privacy risks** — any P2 handling not fully mitigated.
11. **Review date** — next review trigger (annual or on material change).

### Step 11 — Sign-off

Privacy sign-off is recorded in the project ADR. If Critical residual risk remains, USER approval is required before processing begins.

## Anti-patterns

- **"We anonymize after collection."** Anonymization is hard; re-identification is often trivial with quasi-identifiers. Minimize at collection instead.
- **"Consent buried in a ToS."** Consent must be informed and specific. A buried clause is not consent.
- **Vague purpose statements.** "Improve the service" is not a purpose; "train a classifier to detect X" is.
- **Retention = forever.** A retention policy with no deletion trigger is not a policy.
- **Processing sensitive categories "to see what's there".** No lawful basis; no fishing.
- **Treating logs as non-personal.** Session logs with emails or user-specific content are personal data and must appear in the retention table.

## Outputs

- Privacy Appendix attached to the project ADR.
- Data-flow diagram (markdown).
- Retention table (markdown).
- Residual-risk register (if any).
- LESSONS row if a pattern was unusual.

## References (original synthesis)

- GDPR (Regulation (EU) 2016/679) — Articles 5, 6, 9, 25 (by design), 35 (DPIA).
- CCPA / CPRA (California Civil Code §1798.100 et seq.).
- DPDP Act 2023 (India), including Section 8 (Duties) + Schedule categories.
- LGPD (Brazil) — Law 13.709/2018.
- PIPL (China).
- Cavoukian, *Privacy by Design: The 7 Foundational Principles*.
- ENISA, *Data Protection Engineering*.
- NIST Privacy Framework 1.0.
