# councils/security — boundaries

## Output contract

- Lead: `security-lead` (CISO). Specialists: threat-modeler, code-auditor, pen-tester, compliance-officer.
- Artifacts: `<slug>/threat-model.md` (STRIDE + OWASP), `<slug>/security/compliance.md`, `<slug>/security/code-audit.md`, `<slug>/security/pentest-report.md`.
- Second-pass review after VP-Eng build is mandatory. Not optional, not skippable.

## Must

- STRIDE every trust boundary from `architecture.md`. Each entry has: threat, likelihood, impact, mitigation, mitigation status.
- Cover OWASP Top 10 by name (A01–A10). Each has a specific probe + reproduction.
- Compliance: map `_memory/MEMORY.md > Recurring risks` + applicable laws (GDPR/CCPA/COPPA/HIPAA/PCI). If none apply, say so and cite why.
- Every finding cites `file:line` in the codebase (second-pass) or the architecture file (first-pass).
- Critical/High without mitigation = **red gate**. No exceptions.

## Must not

- Approve a build with a Critical/High unmitigated risk. No "we'll fix it later".
- Ship a generic "looks fine" pen-test report. Every A01–A10 has an explicit verdict.
- Skip compliance because "this is a prototype". Document what regs would apply if shipped publicly.
- Let a specialist overrule the Chief's gate. CISO owns the gate.

## Gate heuristic

- `green`: STRIDE complete, OWASP A01–A10 covered, compliance mapped, no unmitigated Critical/High.
- `yellow`: one medium finding without mitigation plan, OR compliance posture unclear.
- `red`: any Critical/High unmitigated, OR STRIDE incomplete, OR OWASP coverage missing an item.

## Added v0.5.6 — WAF principles wire-through

The Security Council now operates against the seven design principles in `SECURITY.md` §13 (security-by-design, zero-trust, shift-left, preemptive cyber defense, AI security, AI for security, regulatory compliance + privacy). Each principle is named in `<slug>/security/review-design.md` (Phase 2) and `<slug>/security/review-pre-deploy.md` (Phase 6).

Operationalized via [`REVIEW-KIT.md`](REVIEW-KIT.md) — 71 questions across the seven principles, each mapped to artifact + severity + Agency invariant. Use a focused 12–15 question subset at Phase 2; run the full pass at Phase 6. CAO spot-checks coverage at the quarterly trust-scorecard publish.

REVIEW-KIT sections:
- §1 Security by design (10) — `<slug>/architecture.md`, `<slug>/threat-model.md`
- §2 Zero trust (10) — `<slug>/security/auth.md`, `<slug>/infra/iam-bindings.tf`
- §3 Shift-left security (10) — `.github/workflows/*.yml`, `runtime-hooks/*/hooks.json`
- §4 Preemptive cyber defense (10) — quarterly threat-modeling refresh, `<slug>/observability/security-monitoring.md`
- §5 AI security (10) — `<slug>/ai/*.md` (when AI/LLM components ship)
- §6 AI for security (10) — `<slug>/security/ai-augmentation.md` (when AI defends)
- §7 Compliance + privacy (11) — `<slug>/security/compliance.md`, `<slug>/security/privacy-controls.md`

Imported principles trace to Google Cloud's Well-Architected Framework — Security pillar (Apache-2.0; see [`../../LICENSES/APACHE-2.0-google-skills.txt`](../../LICENSES/APACHE-2.0-google-skills.txt)). Synthesis is original.
