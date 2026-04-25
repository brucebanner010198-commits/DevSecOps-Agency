# Security Policy

DevSecOps-Agency is a Claude Code plugin whose **first job is to stop unsafe software from shipping**. That posture has to start with how we handle security in this repository. This policy is the public contract: what we protect, how you tell us about a finding, and what you can expect back.

Ratified **2026-04-22** alongside `CONSTITUTION.md` v0.4.1. Governed by Article IX (Code of Ethics) and Article XI (Enforcement) of the Constitution. MUST / MUST NOT / SHOULD / SHOULD NOT / MAY in this document are used in the RFC 2119 / RFC 8174 sense.

## 1. Scope of this document

This policy covers the **DevSecOps-Agency plugin** as distributed from `https://github.com/brucebanner010198-commits/DevSecOps-Agency` and the `devsecops-agency-<version>.plugin` archives attached to its GitHub Releases. Concretely: the agent persona files under `agents/`, the skills under `skills/`, the per-council contracts under `councils/`, the runtime hooks under `runtime-hooks/`, the plugin manifest `.claude-plugin/plugin.json`, and every root document listed in Constitution Schedule A (`MISSION.md`, `VALUES.md`, `GOVERNANCE.md`, `RESILIENCE.md`, `KEEPER-TEST.md`, `CAREER.md`, `RHYTHM.md`, `LESSONS.md`, `AGENTS.md`, `CONSTITUTION.md`, and `SECURITY.md` itself).

**Out of scope** for this policy: downstream projects the agency has shipped (each lives at `outputs/devsecops-agency/<slug>/` with its own `threat-model.md` + `security/` directory), user-authored skills under `skills/` that are not part of the published plugin archive, Claude Code itself, the Claude API, and MCP servers bundled in other plugins. Report issues in those components to their respective maintainers.

## 2. Supported versions

| Version | Status | Security updates |
| --- | --- | --- |
| `0.4.x` | **Current.** Latest stable wave (Governance+Resilience + Constitution). | Yes — patch releases within 7 calendar days of triage for Critical, 30 days for High, next scheduled wave for Medium/Low. |
| `0.3.x` | Wave-current for the clarity/identity/learning/rhythm/career waves. | Security fixes only. No feature backports. End-of-support 2026-07-22 (one quarter after v0.4.0 cut). |
| `0.2.x` | Frozen. | **Unsupported.** Upgrade to `0.4.x`. |
| `0.1.x` | Frozen. | **Unsupported.** |
| Any `-alpha.*` or `-rc.*` prerelease | Development only. | **Unsupported.** Prereleases MUST NOT be run against real user data. |

"Supported" means we will issue a patched release, update `CHANGELOG.md`, and publish a new `.plugin` archive on the GitHub Releases page. It does **not** mean we will backport the fix to unsupported lines.

## 3. Reporting a vulnerability

### 3.1 Preferred channel — GitHub Private Vulnerability Reporting

1. Open `https://github.com/brucebanner010198-commits/DevSecOps-Agency/security/advisories/new`.
2. Fill in the advisory with (MUST):
   - A one-sentence summary of the issue.
   - The affected file path and line range, or the affected agent / skill / runtime-hook name.
   - A reproduction — exact prompt, exact input, exact observed output. Synthetic data only (see §6.2).
   - Severity estimate against the rubric in §5.
   - Proposed mitigation, if you have one.
3. Optionally attach a patch as a draft PR linked from the advisory.

### 3.2 Fallback channel — email

If you do not have a GitHub account, or the flaw prevents you from using GitHub, email **brucebanner010198@gmail.com** with subject line `[security] DevSecOps-Agency: <one-line summary>`. Do not put reproduction payloads in the subject line.

Public issue tracker tickets for security findings are closed on sight and recreated as private advisories. Do not file flaws in `github.com/...//issues`.

### 3.3 What we commit to

| Event | Target |
| --- | --- |
| Acknowledge receipt | ≤ 48 hours from submission |
| First triage verdict (accept / reject / need-more-info) | ≤ 7 calendar days |
| Disposition for an accepted Critical/High | Fix target date + temporary mitigation, ≤ 14 calendar days |
| Published fix — Critical | ≤ 7 calendar days after triage |
| Published fix — High | ≤ 30 calendar days after triage |
| Published fix — Medium | Next scheduled wave, ≤ 90 calendar days |
| Published fix — Low | Next scheduled wave, best-effort |
| Public disclosure | 90 calendar days after triage OR on fix publication, whichever is **earlier**, unless coordinated otherwise |

You will get a named point of contact at triage. Silence is not a refusal — escalate to the fallback channel if we go quiet for more than 14 calendar days.

## 4. Coordinated disclosure

We follow a 90-day coordinated-disclosure window consistent with standard industry practice (modeled after Google Project Zero's public norm and CERT/CC's guidance). The window runs from the day we confirm triage.

- Researchers SHOULD keep the finding private until the window closes or a fix ships, whichever is first.
- We MAY request a one-time 14-day extension if a fix is in review. We will not silently roll the window.
- After the fix ships, we publish the advisory with researcher credit (opt-in), a CVE identifier if one has been assigned, and the CVSS v3.1 vector.
- Requests for an embargoed pre-notification of downstream consumers MAY be granted for genuine supply-chain coordination; they will never be granted to delay public disclosure indefinitely.

## 5. Severity rubric

We grade findings on a four-tier rubric aligned with **CVSS v3.1** base scores. Council-level decisions (see §8) use this same rubric so a report filed here lands on the same gate the agency uses internally.

| Severity | CVSS v3.1 | Description | Council response |
| --- | --- | --- | --- |
| **Critical** | 9.0 – 10.0 | Remote, unauthenticated impact. Raw-secret leakage. ASI-class agent-compromise (OWASP ASI Top 10). Constitution violation that bypasses USER-ONLY. | Hard block; drop-everything fix-loop; patch within 7 days; **non-waivable** if raw-secret or ASI-class (Constitution §8.5). |
| **High** | 7.0 – 8.9 | Privileged attacker required but impact wide. Injection that can be chained to tool-abuse. Waiver-bypass. Append-only violation (Constitution §5.2). | Block on ship path; fix within 30 days; waiver permitted only via USER-ONLY approval with ≤ 90-day calendar expiration (Constitution §8.5). |
| **Medium** | 4.0 – 6.9 | Limited impact, requires chaining. Documentation drift that could mislead a future audit. Missing hook enforcement on a non-critical path. | Next-wave fix; filed as `compliance-drift` yellow. |
| **Low** | 0.1 – 3.9 | Informational, hygiene, or defense-in-depth improvement. | Best-effort; may be declined with rationale. |

Non-waivable classes per Constitution §8.5: **any raw-secret exposure** and **any ASI-class finding that breaks agent independence, scope, or identity**. These cannot be cleared by waiver even with user approval — they must be fixed or the artifact does not ship.

## 6. Threat model specific to this plugin

A Claude Code plugin that drives autonomous multi-agent pipelines has a threat surface unlike a traditional web app. Our model names the real attackers and the real surfaces.

### 6.1 In-scope attacker classes

- **External prompt-injection actor.** Delivers payload via a web page fetched by a specialist, an MCP tool response, an email inbox the agency reads, or any content under `<slug>/research/` that originates outside the repo. Goal: hijack an agent's next tool call.
- **Supply-chain attacker.** Targets the dependency graph (npm / PyPI / OS packages), a pinned MCP registry entry, or an upstream OSS skill import. Goal: swap a component and inherit the agent's tool grants.
- **Memory-poisoning actor.** Aims at `_memory/MEMORY.md`, the dated Light / per-project Deep logs, or the cross-project REM pattern store. Goal: survive a single session and corrupt the next one.
- **Persona-tampering actor.** Edits an `agents/*.md` or a high-leverage `skills/*/SKILL.md` off-branch and tries to land it without a prompt-diff review.
- **Waiver-abuse actor.** Tries to clear a blocking-council red via a side channel, a permanent waiver, a re-use of an expired waiver, or an ASI-class / raw-secret finding that is never waivable.
- **Governance-bypass actor.** Attempts a root-doc or Constitution edit without a `constitution-amend` ADR + CAO+CRT review + USER-ONLY approval (Constitution Art X).

### 6.2 In-scope vulnerability classes

MUST be reported:

- Prompt injection, indirect prompt injection, goal hijack, jailbreak — against any persona file, skill, or hook (maps to OWASP ASI Top 10 2025 → `skills/red-team/references/owasp-asi-top-10.md`).
- Tool abuse, permission bypass, tool-chaining outside declared `allowed-tools`, destructive-command evasion of `tool-guardian` (maps to ASI).
- Raw secret in any committed artifact (source, test, fixture, doc, session log, ADR, `inbox.json`, heartbeat file) — vault refs only per Constitution §5.5. **Non-waivable.**
- Data exfiltration — PII, credentials, memory readback, cross-project leakage — by any agent or tool.
- Supply-chain — dependency typosquatting, unpinned MCP registration, missing SBOM, missing SLSA provenance, license violation that slips past `dependency-license-checker`.
- Append-only violation — any write path that mutates a prior session log, ADR, or LESSONS row in place. **Hard invariant per Constitution §5.2.**
- Governance bypass — any path that executes one of the 10 USER-ONLY actions (Constitution §2.2) without user approval captured in `inbox.json` + user-meeting ADR.
- Waiver abuse — permanent waivers, waivers without calendar expiration, self-approved waivers, waivers applied across projects, any waiver on an ASI-class or raw-secret finding.
- Supremacy violation — any agent acting on a subordinate doc when the Constitution is silent or contradictory, rather than filing a §10.1 amendment proposal.
- Prompt-diff bypass — landing a change to `agents/*.md` or a high-leverage `SKILL.md` without a CRT prompt-diff review.
- Runtime-hook bypass — using `git add -A`, `--no-verify`, or any other path that skips `secrets-scanner`, `tool-guardian`, `governance-audit`, `dependency-license-checker`, `session-logger`, or `commit-gate.sh`.
- Memory poisoning — novelty-gate evasion, Jaccard-similarity bypass, silent edit of `_memory/MEMORY.md` outside the `memory` skill.

### 6.3 Out-of-scope

- Denial-of-service against `anthropic.com`, `api.anthropic.com`, or any Anthropic model — report those to Anthropic directly.
- Vulnerabilities in Claude Code, the Claude API, the Claude Agent SDK, the MCP reference servers, or any third-party MCP server we pin but do not author.
- Social-engineering attacks against the User that do not involve a flaw in the plugin's artifacts.
- Findings against prereleases (`-alpha.*`, `-rc.*`).
- Self-XSS or attacks that require an attacker to have already compromised the User's machine.
- Rate-limit or spend-cap bypasses whose only effect is inflating the User's bill without affecting integrity, confidentiality, or availability of shipped work — file these as FinOps concerns, not security.

### 6.4 Responsible testing rules

- Synthesize all test data. MUST NOT exfiltrate real PII, real credentials, or real third-party secrets in a reproduction. Red-Team council follows the same rule internally (`councils/red-team/AGENTS.md`).
- MUST NOT run destructive commands against infrastructure you do not own. The `tool-guardian` hook blocks `rm -rf /`, `git push --force` to `main`, and DB-drop patterns by design — evading it with local bypasses is in-scope; running the bypass against someone else's system is not.
- MUST NOT file a "theoretical" vulnerability without a reproduction. Every accepted finding needs a concrete, runnable repro. This mirrors the internal red-team rule: "Red-team proves; the owning council repairs."
- SHOULD use a dedicated fork or worktree for testing. The agency itself builds in `_worktrees/` precisely to isolate experiments.

## 7. Defense-in-depth already shipped

Before reporting, check whether your finding is already blocked by one of these controls — a genuine bypass is still a finding, but "this attack would work against a plugin without this control" is not.

**Runtime hooks** (`runtime-hooks/`):

- `secrets-scanner/` — 30+ regex patterns for AWS keys, GitHub PATs, Stripe, JWT, Slack, private keys, and similar. Runs read-only on diffs; exits non-zero on match.
- `tool-guardian/` — Block list for destructive invocations (`rm -rf /`, force-push, DB drops) with env-var allowlist for legitimate carve-outs.
- `governance-audit/` — Prompt scan for data-exfil / privesc / system-destruction / prompt-injection / credential-exposure; runs at session-start and session-end.
- `dependency-license-checker/` — License scan on dependency diffs; flags non-compatible licenses before merge.
- `session-logger/` — Append-only JSONL per agent per session. The append-only property is an invariant, not a convention.
- `commit-gate.sh` — Locked-down replacement for auto-commit. No `git add -A`, no `--no-verify`, no auto-push. Explicit file staging only.

**Councils with standing blocking authority** (Constitution §3.3):

- **CISO (`security-lead`)** — STRIDE every trust boundary, OWASP Top 10 coverage A01–A10 with per-item verdict, SBOM + SLSA provenance. Red gate on any unmitigated Critical/High.
- **CRT (`red-team-lead`)** — Pre-release red-team on every shipped project, prompt-diff red-team on every persona or high-leverage skill edit. Every finding maps to OWASP ASI Top 10 (`skills/red-team/references/owasp-asi-top-10.md`) or is invalid.
- **CEVO (`evaluation-lead`)** — Eval-set regression gate; ≥ 5 pp drop is an automatic block.
- **CAO (`cao`)** — Read-only integrity pass across the paper trail; catches append-only violations, missing ADRs, and non-goal drift.

**Skills with security-critical enforcement**:

- `skills/mcp-defense/` — Pinned-hash registration, provenance check on every MCP tool call.
- `skills/mcp-authoring/` — Safe-authorship rules for new MCP servers.
- `skills/dlp/` — Data-loss-prevention scan on every outbound tool call.
- `skills/injection-defense/` — Prompt-injection canaries + response screening.
- `skills/secrets-vault/` — Vault-reference enforcement; raw secrets are a ship-block per Constitution §5.5.
- `skills/red-team/` — Adversarial playbook + OWASP ASI mapping + prompt-diff protocol.
- `skills/waivers/` — USER-ONLY-approved, ≤ 90-day calendar-expiry waiver flow. ASI + raw-secret non-waivable.
- `skills/chaos/` — Per-service fault injection (distinct from agency-level `skills/drill/`).
- `skills/audit/` — CAO integrity sweep.

**Constitutional guarantees** (invoke by § in a vulnerability report):

- §1.1 Supremacy — Constitution overrides any subordinate doc on conflict.
- §2.2 USER-ONLY actions (10 enumerated) — no agent may execute these autonomously.
- §5.1 Receipts — every decision has an ADR + session-log trail.
- §5.2 Append-only — session logs, ADRs, LESSONS rows, archives. Correction rows only.
- §5.5 Vault refs — raw secrets in any artifact are a non-waivable red.
- §5.7 SBOM+SLSA — every shipped artifact.
- §8.5 Waiver bounds — ≤ 90 calendar days, USER-ONLY approval, ASI + raw-secret non-waivable.
- §11.1 Enforcement — routed through CAO + CRT + CEVO + CISO + runtime hooks; no new council, no silent enforcement (§11.6), no enforcement against the User (§11.5).

## 8. Handling of accepted findings

On acceptance, a finding MUST receive (no exceptions):

1. An ADR under `_decisions/` with `kind:` set appropriately (`security-finding` / `waiver-grant` / `red-team-finding` / `append-only-violation` / `constitution-amend`). Constitution Art X applies if the fix requires a Constitution edit.
2. A stepping stone under `_vision/playbooks/` if the finding is High or Critical and has been remediated. Stones are immutable; supersession is via new-stone-with-link-back (Constitution §5.8).
3. A row in the per-project `threat-model.md` — or in the plugin's `SECURITY.md` changelog if the finding is against the plugin itself.
4. A fix commit that cites the advisory ID in its message and passes `commit-gate.sh`.
5. A `CHANGELOG.md` entry in the wave notes of the release that carries the fix.
6. A public advisory republished once the coordinated-disclosure window closes (§4).

Findings that would require clearing a blocking-council red without fixing the underlying issue MUST go through `skills/waivers/` — **proposed** by the responsible council lead, **reviewed** by the blocking chief + CEO (procedural only), **approved** by the User via `user-meeting` + `inbox.json`, with an ISO calendar date expiration ≤ 90 days. No relative dates. No permanent waivers. ASI + raw-secret classes are non-waivable (Constitution §8.5).

## 9. Safe harbor

Security research conducted in good faith against this repository — following this policy, using synthetic data, respecting third parties, and coordinating disclosure per §3 and §4 — will not be met with legal action by the project maintainers. We will:

- Not pursue civil or criminal claims against good-faith research that abides by §6.4.
- Not refer researchers to law enforcement for acts that remained within scope.
- Not terminate GitHub access, strike issues, or block accounts in retaliation for a good-faith advisory.

Safe harbor does **not** cover: accessing data you do not own, running reproductions against third-party infrastructure, exfiltrating real user data, or violating any applicable law.

This clause is a commitment by the project maintainers. It cannot bind Anthropic, GitHub, or any upstream dependency — research against those parties is governed by their own policies.

## 10. Acknowledgments

We credit every researcher whose accepted finding ships in a release, in the advisory and in the relevant `CHANGELOG.md` entry, unless the researcher requests anonymity. Anonymity is honored without question.

No financial bounty is offered at this time. A public hall-of-fame page will be added to the repository at v0.5.0.

## 11. References

Normative:

- **RFC 2119** / **RFC 8174** — Key-word grammar for requirement levels.
- **RFC 9116** — `security.txt` convention for advertising security contact points.
- **Constitution of the Agency** — `CONSTITUTION.md`, supreme over this document on any conflict per §1.1.

Framework influence (original synthesis; see `CONSTITUTION.md > Sources and Influences`):

- **OWASP Top 10 (2021)** — standard web-app coverage for every shipped project.
- **OWASP ASI Top 10 (2025)** — agent-specific attack catalog used by the Red-Team council.
- **CVSS v3.1** — Common Vulnerability Scoring System specification; source of §5 severity rubric.
- **NIST Cybersecurity Framework** — Identify / Protect / Detect / Respond / Recover lifecycle.
- **ISO/IEC 27001** — Information Security Management System control framework.
- **SOC 2 Trust Services Criteria** — Security, Availability, Processing Integrity, Confidentiality, Privacy.
- **SLSA** (Supply-chain Levels for Software Artifacts) — provenance requirement per Constitution §5.7.
- **SPDX / SBOM** — software bill-of-materials format for supply-chain receipts.
- **Anthropic Responsible Scaling Policy (RSP)** — tiered-commitment style reflected in §5 non-waivable classes.
- **Anthropic Usage Policies** — operating constraints for any Claude-driven agent.
- **CERT/CC Vulnerability Disclosure Guidance** — basis for the 90-day window in §4.
- **Google Project Zero Disclosure Policy** — industry reference for coordinated disclosure.
- **ACM Code of Ethics** / **IEEE Code of Ethics** — baseline professional-ethics obligations.

No text above is copied from any cited source; every clause is original to this Agency.

## 13. Design principles (added v0.5.6 wire-through)

The Agency adopts seven design principles from Google Cloud's Well-Architected Framework — Security pillar (Apache-2.0; see [`LICENSES/APACHE-2.0-google-skills.txt`](LICENSES/APACHE-2.0-google-skills.txt)). They are layered over §1–§12, not replacing anything. Each principle MUST be considered at Phase 2 (Design) and verified at Phase 6 (Deploy) using [`councils/security/REVIEW-KIT.md`](councils/security/REVIEW-KIT.md).

### 13.1 Security by design

Security is decided at architecture time, not retrofitted at QA time. Every project's `architecture.md` MUST contain a `§Security-from-day-zero` section before any code is written. Threat-model the trust boundaries, name the attacker classes, decide the controls — then build. The Agency's existing rule "STRIDE every trust boundary" (per `councils/security/AGENTS.md`) is the operational form of this principle. REVIEW-KIT §1.

### 13.2 Zero trust

Never trust, always verify — at every request, not at session start. No implicit trust based on network location, device posture alone, or previously-granted access. Continuous verification, least privilege at IAM and RBAC layers, encryption in transit AND at rest, default-deny perimeters. The `gcp-auth` skill's "never download service account keys" posture is the operational form. REVIEW-KIT §2.

### 13.3 Shift-left security

Security findings are cheaper to fix the earlier they're caught. The Agency's runtime hooks already enforce this: `runtime-hooks/secrets-scanner/` blocks at commit time; `runtime-hooks/dependency-license-checker/` blocks unlicensed dependencies; `runtime-hooks/commit-gate.sh` blocks `--no-verify` bypass attempts. Phase 5 (Security) is a SECOND pass after Phase 3 (Build) — the first pass should already have caught the obvious classes via shift-left. REVIEW-KIT §3.

### 13.4 Preemptive cyber defense

Don't wait to be attacked to find out you're attackable. Proactive measures: threat intelligence ingestion, regular penetration tests, threat-model refresh on every material architecture change (and at least quarterly), tabletop exercises and chaos drills (see `RESILIENCE.md` Drills + Chaos engineering). The Red-Team Council's quarterly red-team scan is the operational form. REVIEW-KIT §4.

### 13.5 AI security (for projects that ship AI/LLM components)

Treat AI/LLM components as a distinct attack surface. Model integrity, training-data provenance, adversarial-input resilience, prompt-injection defense (especially across persona / skill / session-log / MCP / inbox surfaces — already enumerated in §6.2), differential privacy where personal data is involved, explainability for high-stakes outputs. The `THREAT-MODEL.md` AI lens + OWASP ASI Top 10 + NIST AI RMF + MITRE ATLAS five-lens overlay is the operational form. REVIEW-KIT §5.

### 13.6 AI for security (for projects that use AI to defend themselves)

AI augments human security judgment — it never replaces it. Every AI-driven security control MUST have a documented manual fallback path. Precision, recall, and drift metrics MUST be tracked. False-positive and false-negative handling MUST have a runbook. The Red-Team Council's LLM-based scans are the operational form, with the human Chief always in the verdict path. REVIEW-KIT §6.

### 13.7 Regulatory compliance and privacy

Compliance is per-project: every shipped project MUST produce a `<slug>/security/compliance.md` that maps the project's data handling against the regulations that apply (or explicitly says "no regulated data, regulation X N/A"). The `skills/privacy/` skill (DPIA + GDPR/CCPA/DPDP/LGPD/PIPL) and the Legal Council are the operational forms. REVIEW-KIT §7.

### Validation routing

The 71-question assessment kit at [`councils/security/REVIEW-KIT.md`](councils/security/REVIEW-KIT.md) operationalizes §13.1–§13.7. Use it at Phase 2 (focused subset) and Phase 6 (full pass). CAO spot-checks REVIEW-KIT coverage at the quarterly trust-scorecard publish.

---

## 12. Document control

| Field | Value |
| --- | --- |
| Document | `SECURITY.md` |
| Plugin | DevSecOps-Agency |
| Version | 1.0 (shipped with plugin v0.4.1) |
| Ratified | 2026-04-22 |
| Supremacy | `CONSTITUTION.md` overrides this document on any conflict (§1.1). |
| Amendment | Any change to §3 (reporting channels), §4 (disclosure window), §5 (severity rubric), §6 (threat model scope), or §9 (safe harbor) requires a `security-policy-amend` ADR and a CAO + CRT + CISO review. Edits that affect §8 non-waivable classes are a Constitution amendment per Art X and are USER-ONLY. All other edits are standard PR flow. |
| Contact | GitHub Private Vulnerability Reporting (preferred) · `brucebanner010198@gmail.com` (fallback) |
