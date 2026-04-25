# councils/security — REVIEW-KIT

A structured assessment kit for the Security Council. Use it to interview an existing system, audit a finished build, or pre-flight a design proposal. The kit is **prompts you ask**, not answers you assert — every question expects a documented answer in a specific Agency artifact.

Imported from the Google Cloud Well-Architected Framework — Security pillar (Apache-2.0; see [`LICENSES/APACHE-2.0-google-skills.txt`](../../LICENSES/APACHE-2.0-google-skills.txt)). Adapted for the Agency: each question is mapped to the artifact where the answer must live, the council that owns the answer, and the Agency invariant that backs it. Original Google text rephrased and reorganized; structure is original to this Agency.

Ratified **2026-04-25** alongside plugin **v0.5.6**. Owned by **CISO**; convened during Phase 2 (Design) and Phase 6 (Deploy). 71 questions across 7 principles. Every question carries a severity bias (`critical` / `high` / `medium`) so a triage can short-cycle when time is tight.

---

## How to use this kit

1. **At Phase 2 (Design):** the security-lead picks the 12-15 questions from sections §1, §2, §6 most relevant to the project's surface area, fills the answers into `<slug>/security/review-design.md`, and brings unanswered ones to the threat-model session.
2. **At Phase 6 (Deploy):** the security-lead runs the full 71-question pass, fills `<slug>/security/review-pre-deploy.md`, and refuses sign-off on any unanswered `critical` row.
3. **Quarterly portfolio sweep:** CAO spot-checks 3 random shipped projects' review files against this kit and publishes coverage in the trust scorecard.

Answers MUST cite a file path or a specific control. Answers like "we follow best practices" or "TBD" are reds.

---

## §1. Security by design (10 questions)

Backed by Constitution §5.5 (security baseline on every shipped project), `THREAT-MODEL.md` (plugin-level), and `councils/security/AGENTS.md` "STRIDE every trust boundary" rule.

| # | Question | Severity | Answer lives in |
|---|---|---|---|
| 1.1 | How does this project incorporate security into the initial planning and design phase, before any code is written? | critical | `<slug>/architecture.md` §Security-from-day-zero |
| 1.2 | What documented security requirements does this project carry, and where are they versioned? | critical | `<slug>/security/requirements.md` |
| 1.3 | How is security integrated into the development lifecycle (Phase 3 Build → Phase 4 QA → Phase 5 Security → Phase 6 Deploy)? | high | `<slug>/handoff-protocol.md` |
| 1.4 | What threat-modeling technique was applied (STRIDE / PASTA / LINDDUN), and where is the output? | critical | `<slug>/threat-model.md` |
| 1.5 | How are security vulnerabilities discovered during design and development prioritized and tracked? | high | `<slug>/security/findings.md` + ADR refs |
| 1.6 | What is the patch cadence for application dependencies and infrastructure components? | high | `<slug>/security/patch-policy.md` |
| 1.7 | How are security design decisions documented and communicated to other councils? | medium | ADRs of kind `security-design-decision` |
| 1.8 | How are security configurations applied consistently across environments (dev / staging / prod)? | high | `<slug>/infra/` Terraform or equivalent IaC |
| 1.9 | How is the effectiveness of security controls validated (pen-test, automated scan, drill)? | critical | `<slug>/security/pentest-report.md` + drill ADRs |
| 1.10 | How are security exceptions and deviations handled, and where is each exception's expiry recorded? | critical | `_vision/waivers/active.md` (waivers MUST expire ≤ 90d) |

---

## §2. Zero trust (10 questions)

Backed by `SECURITY.md` defense-in-depth, `gcp-auth` skill ("never download service account keys"), and Constitution §8.5 non-waivable raw-secret class.

| # | Question | Severity | Answer lives in |
|---|---|---|---|
| 2.1 | How are users and devices authenticated and verified for every resource access (continuous, not session-once)? | critical | `<slug>/security/auth.md` |
| 2.2 | How is the principle of least privilege enforced for human IAM, service-account IAM, and Kubernetes RBAC? | critical | `<slug>/infra/iam-bindings.tf` + IAM matrix |
| 2.3 | How is internal network traffic monitored, restricted, and inspected (firewall rules, VPC SC perimeters)? | high | `<slug>/infra/network.tf` |
| 2.4 | How is data secured in transit (TLS version, cipher suites) and at rest (KMS, CMEK, envelope encryption)? | critical | `<slug>/security/encryption.md` |
| 2.5 | How is user-and-device activity continuously monitored and logged, and where do those logs go? | high | `<slug>/observability/audit-log-config.md` |
| 2.6 | How are security incidents handled and contained without breaking the zero-trust model? | high | `<slug>/security/incident-response.md` (links DISASTER-RECOVERY.md) |
| 2.7 | How are zero-trust policies updated and rolled out without dropping legitimate traffic? | medium | `<slug>/security/policy-rollout.md` |
| 2.8 | How are third-party services (vendors, MCPs, OSS dependencies) integrated under zero-trust? | high | `<slug>/security/vendor-isolation.md` + tool-scout ADRs |
| 2.9 | How is remote access (BYOD, contractor laptops, on-call from coffee shops) handled? | medium | `<slug>/security/remote-access.md` |
| 2.10 | How is the team trained on zero-trust principles so the human layer doesn't become the weak link? | medium | `<slug>/security/training-log.md` |

---

## §3. Shift-left security (10 questions)

Backed by `runtime-hooks/secrets-scanner/`, `runtime-hooks/dependency-license-checker/`, `runtime-hooks/commit-gate.sh`, and the Agency's "second-pass code-audit after VP-Eng build" rule from `councils/security/AGENTS.md`.

| # | Question | Severity | Answer lives in |
|---|---|---|---|
| 3.1 | How is security testing integrated into the development pipeline (pre-commit hook, CI step, pre-deploy gate)? | critical | `.github/workflows/*.yml` + `runtime-hooks/*/hooks.json` |
| 3.2 | What kinds of security testing run during development (SAST, DAST, dependency scan, IaC scan, secret scan)? | critical | `<slug>/security/test-matrix.md` |
| 3.3 | How do developers receive feedback on security vulnerabilities — turn-around time and signal-to-noise ratio? | high | CI pipeline configuration + sample PR comments |
| 3.4 | How are developers empowered to take ownership of security — what access do they have to fix things themselves? | medium | `councils/execution/AGENTS.md` + IAM doc |
| 3.5 | How are security requirements communicated to developers in language they can act on (not "be secure")? | high | `<slug>/security/requirements.md` (must include positive examples) |
| 3.6 | How is the effectiveness of shift-left initiatives measured (mean time to fix, leak escape rate)? | medium | `_vision/security/metrics-<YYYY-QN>.md` |
| 3.7 | How are security dependencies and third-party libraries handled (pinning, SBOM, vulnerability subscription)? | critical | `<slug>/sbom.spdx.json` + `dependency-license-checker` hook config |
| 3.8 | How are security configurations managed across dev / staging / prod environments? | high | `<slug>/infra/` IaC + GitOps repo |
| 3.9 | How are security exceptions handled in the development environment (dev-only tokens, mock data, etc.)? | medium | `<slug>/security/dev-exceptions.md` |
| 3.10 | How is a culture of security awareness fostered among developers — what's the actual ritual? | medium | `_vision/security/awareness-ritual.md` |

---

## §4. Preemptive cyber defense (10 questions)

Backed by `THREAT-MODEL.md` (STRIDE + OWASP ASI Top 10 + NIST AI RMF + MITRE ATLAS five-lens overlay), `councils/red-team/AGENTS.md`, and the four blocking-council vetoes (CISO/CRT/CEVO/CAO).

| # | Question | Severity | Answer lives in |
|---|---|---|---|
| 4.1 | How are potential security threats proactively identified and mitigated before they impact production? | critical | Quarterly threat-modeling refresh ADR |
| 4.2 | What tools and techniques are used for continuous security monitoring (SIEM, Security Command Center, Cloud Audit Logs)? | high | `<slug>/observability/security-monitoring.md` |
| 4.3 | How are security alerts and incidents responded to and remediated — what's the runbook chain? | critical | `<slug>/security/runbooks/` |
| 4.4 | How are incident-response plans simulated and tested (game days, tabletop exercises, drills)? | high | `_vision/drills/` ADRs (per `RESILIENCE.md` drills section + chaos engineering §) |
| 4.5 | How does the team stay current with the latest security threats and CVE disclosures relevant to its stack? | medium | `_vision/security/threat-intel-cadence.md` |
| 4.6 | How are DDoS attacks against applications and services handled (rate limiting, WAF, CDN)? | high | `<slug>/infra/ddos-defense.md` |
| 4.7 | How is sensitive data protected from insider threats (separation of duties, audit log immutability, key escrow)? | high | `<slug>/security/insider-threat-controls.md` |
| 4.8 | How are advanced persistent threats (APTs) detected, given they evade single-event detection? | medium | `<slug>/observability/anomaly-detection.md` |
| 4.9 | How are supply-chain vulnerabilities handled — and what's the SLSA attestation level for shipped artifacts? | critical | `<slug>/slsa.provenance.json` (per Constitution §5.7) |
| 4.10 | How does the security posture adapt to evolving threats — what's the cadence for threat-model refresh? | high | `THREAT-MODEL.md` refresh ADRs (quarterly) |

---

## §5. AI security (10 questions — for any project that ships an AI/LLM component)

Backed by `THREAT-MODEL.md` AI lens, OWASP ASI Top 10 2025 (per Red-Team Council), and `runtime-hooks/governance-audit/`.

| # | Question | Severity | Answer lives in |
|---|---|---|---|
| 5.1 | How is the integrity of AI models and training data protected (provenance, signing, access control)? | critical | `<slug>/ai/model-provenance.md` |
| 5.2 | How are bias and fairness concerns addressed in the AI model — what evaluation suite catches drift? | high | `<slug>/ai/fairness-eval.md` (per `skills/fairness/`) |
| 5.3 | How are AI models protected from adversarial attacks and data poisoning? | critical | `<slug>/ai/adversarial-defense.md` |
| 5.4 | How is the privacy of data used in AI models ensured (differential privacy, PII redaction, data minimization)? | critical | `<slug>/ai/privacy-controls.md` (per `skills/privacy/`) |
| 5.5 | How are AI model decisions explained or interpreted, especially for high-stakes outputs? | medium | `<slug>/ai/explainability.md` |
| 5.6 | How is access to AI models and their training data controlled (RBAC, API keys, vault refs)? | critical | `<slug>/ai/access-control.md` |
| 5.7 | How is compliance with AI-relevant regulations ensured (EU AI Act, NIST AI RMF)? | high | `<slug>/security/compliance.md` AI section |
| 5.8 | How are anomalies in AI model behavior monitored — what are the canary tests in production? | high | `<slug>/observability/ai-canaries.md` |
| 5.9 | How are security incidents involving AI models handled — what's the rollback path? | high | `<slug>/security/ai-incident-runbook.md` |
| 5.10 | How is the team trained on the secure and responsible use of AI/ML? | medium | `_vision/security/ai-training-log.md` |

---

## §6. AI for security (10 questions — for any project that uses AI to defend itself)

Backed by `councils/red-team/AGENTS.md` (uses LLM-based red-team scans), `runtime-hooks/secrets-scanner/`, and the Agency's general posture that AI augments — never replaces — human security judgment.

| # | Question | Severity | Answer lives in |
|---|---|---|---|
| 6.1 | How is AI/ML used to enhance the security posture beyond what manual review can catch? | medium | `<slug>/security/ai-augmentation.md` |
| 6.2 | What AI models are used for security purposes, and what's the model-card on each (capabilities, limits, failure modes)? | high | `<slug>/security/security-ai-cards.md` |
| 6.3 | How are security-purpose AI models trained, validated, and updated — how often is the validation set refreshed? | high | `<slug>/security/security-ai-lifecycle.md` |
| 6.4 | How is the accuracy and reliability of AI-based security systems measured (precision, recall, F1, drift)? | high | `_vision/security/ai-metrics-<YYYY-QN>.md` |
| 6.5 | How are false positives and false negatives from AI-based security systems handled — what's the fall-back? | critical | `<slug>/security/ai-fallback.md` (manual review path MUST exist) |
| 6.6 | How are AI-based security systems integrated with the existing SIEM, alert pipeline, and incident-response workflow? | high | `<slug>/observability/ai-security-integration.md` |
| 6.7 | How are AI security systems updated, and what's the change-control process? | medium | `<slug>/security/ai-change-control.md` |
| 6.8 | How are decisions made by AI security systems explained or audited (especially when they block traffic)? | high | `<slug>/security/ai-decision-log.md` |
| 6.9 | How is the ethical use of AI for security ensured (no surveillance overreach, no profiling without consent)? | high | `<slug>/security/ai-ethics-statement.md` |
| 6.10 | How is the effectiveness of AI for security measured against the baseline of manual review alone? | medium | Quarterly AI-security retrospective |

---

## §7. Regulatory compliance and privacy (11 questions)

Backed by `skills/privacy/` (DPIA + GDPR/CCPA/DPDP/LGPD/PIPL), `SECURITY.md` §11 reference frameworks, and `councils/legal/AGENTS.md` ownership.

| # | Question | Severity | Answer lives in |
|---|---|---|---|
| 7.1 | What regulatory compliance frameworks and privacy standards apply to this project? | critical | `<slug>/security/compliance.md` (open with the matrix) |
| 7.2 | How are compliance risks assessed, prioritized, and tracked — what's the residual-risk register? | high | `<slug>/security/compliance.md` §residual-risk |
| 7.3 | How is the privacy of sensitive data ensured at every stage (collection, processing, storage, transmission, deletion)? | critical | `<slug>/security/privacy-controls.md` |
| 7.4 | How are data-subject requests (DSRs — access, deletion, portability) handled, and what's the SLA? | high | `<slug>/security/dsr-runbook.md` |
| 7.5 | How are compliance activities and evidence documented and retained for the regulator-mandated retention period? | high | `<slug>/security/compliance-evidence/` |
| 7.6 | How are third-party vendors and partners verified for compliance with the same regulations? | high | `<slug>/security/vendor-compliance.md` |
| 7.7 | How are data breaches and security incidents involving regulated data handled, including notification timelines? | critical | `<slug>/security/breach-notification-runbook.md` (72h GDPR, 60d HIPAA, etc.) |
| 7.8 | How does the team stay current with changes in regulatory frameworks the project is subject to? | medium | `_vision/legal/reg-monitoring-cadence.md` |
| 7.9 | How is the team trained on regulatory compliance and privacy — what's the actual cadence? | medium | `<slug>/security/compliance-training-log.md` |
| 7.10 | How is compliance demonstrated to auditors and regulators — what's the audit-pack? | high | `<slug>/security/audit-pack/` (must be assembleable in < 1 day) |
| 7.11 | How are records-of-processing-activities (Art. 30 GDPR equivalent) maintained and kept current? | high | `<slug>/security/ropa.md` |

---

## Cross-cutting validation checklist

After §1-§7 are answered, run this quick checklist for any obvious gaps. Reds here block deploy regardless of individual question scores.

- [ ] **Defense in depth** at network + host + application + data layers.
- [ ] **Least privilege** enforced — no service running as root, no IAM role with `*` on `*`.
- [ ] **Encryption** at rest (CMEK or provider default) and in transit (TLS 1.2 minimum, 1.3 preferred).
- [ ] **Logging** centralized, immutable retention period set, no PII in logs.
- [ ] **Secrets** in vault refs only — `runtime-hooks/secrets-scanner/` has zero findings.
- [ ] **Default-deny** — every unmatched IAM call, network packet, and API request is denied.
- [ ] **Backup & recovery** tested — `RESILIENCE.md` per-RPO/RTO drills have run within the last quarter.
- [ ] **Incident response** runbook exists and has been rehearsed in the last 6 months.
- [ ] **Threat model** refreshed in the last quarter or since the last material architecture change.
- [ ] **Compliance matrix** filled in (even if to say "no regulated data, regulation X N/A").
- [ ] **Waivers** all carry a calendar-date expiry ≤ 90 days; ASI-class and raw-secret findings have **zero** waivers (non-waivable per Constitution §8.5).
- [ ] **Penetration test** results reviewed; every Critical/High has a mitigation plan with an owner and date.

---

## Sources & influences

- **Google Cloud Well-Architected Framework — Security pillar** (Apache-2.0). Source of the seven-principle structure (security-by-design, zero-trust, shift-left, preemptive cyber defense, AI security, AI for security, compliance + privacy) and the underlying ten-question template per principle. See [`LICENSES/APACHE-2.0-google-skills.txt`](../../LICENSES/APACHE-2.0-google-skills.txt). Original: <https://docs.cloud.google.com/architecture/framework/security>.
- **OWASP Top 10 (2021)** and **OWASP ASI Top 10 (2025)** — referenced as the named threat catalogs in §1.4, §4.1, §4.10 (per `SECURITY.md`).
- **NIST Cybersecurity Framework** and **NIST AI RMF** — frame §5 (AI security) and the §4 monitoring questions.
- **MITRE ATLAS** — frames the AI-attack lens in §5.3 (adversarial defense) per `THREAT-MODEL.md`.
- **EU AI Act** + **GDPR Art. 30** (Records of Processing) — referenced in §5.7 and §7.11.
- **`THREAT-MODEL.md` (this repo, v0.5.0)** and **`SECURITY.md` (this repo, v1.0)** — Agency-specific anchors that every question in this kit ties back to.

End of `councils/security/REVIEW-KIT.md` v1.0 — ratified 2026-04-25 with plugin v0.5.6.
