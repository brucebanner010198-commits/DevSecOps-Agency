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
