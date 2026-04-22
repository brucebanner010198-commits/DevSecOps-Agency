# SWOT Analysis — DevSecOps-Agency

**Ratified:** 2026-04-22
**Plugin version at analysis:** v0.5.0
**Authority:** [`CONSTITUTION.md`](CONSTITUTION.md) Article X (Continuous Improvement)
**Classification:** Public
**Owner:** CEO · **Reviewer:** CAO (Audit) · **Cadence:** Reviewed at every quarterly Keeper Test

---

## 0. Purpose

This document answers, in one place and in writing, four questions about the Agency as it exists at v0.5.0:

1. **Strengths** — what is already working and should be leveraged.
2. **Weaknesses** — what is structurally fragile, incomplete, or unproven, and must be fixed or offset.
3. **Opportunities** — what the Agency could become if it pushes in a direction that is currently open.
4. **Threats** — what could break the Agency from the outside, and how we blunt the blow.

The document does not stop at naming the squares. Each item is paired with a **mitigation / action line** and either (a) a roadmap commitment with a target wave, or (b) a named council that owns the standing response. SWOT-without-action is theatre; we refuse it.

This is a self-audit, not a sales sheet. Items the CAO would flag in an external review are listed here before a critic finds them.

---

## 1. Strengths (S)

The Agency's **structural advantages** — properties that are baked into the design and not easy for competitors or drift to remove.

### S1. Constitutional foundation
A single supreme document ([`CONSTITUTION.md`](CONSTITUTION.md)) that all other founding documents explicitly subordinate themselves to. No silent precedence fights. Amendments require USER approval and an ADR. This alone eliminates an entire class of governance confusion that afflicts most multi-agent systems.
**Leverage:** Cite the Constitution by article and section on every decision. The habit reinforces its authority.

### S2. Four blocking vetoes with real teeth
CISO, CRT, CEVO, CAO can each independently block delivery. The vetoes are **named in the Constitution, logged in session receipts, and tested in the Keeper Test drill.** This is stronger than an advisory review board because the block is architectural, not cultural.
**Leverage:** Publish the list of blocked releases + reason codes in the quarterly trust scorecard ([`TRUST.md`](TRUST.md) §3).

### S3. Independence of CAO, CEVO, CRT, CSRE
Four councils never sit on the delivery path. They cannot be pressured by a deadline because their incentives are de-coupled from shipping. Every SRE outage post-mortem in the industry begins with "the reviewer also owned delivery"; we refuse that setup.
**Leverage:** Expand this model — every new safety-adjacent council added to the Agency inherits the independence property.

### S4. Append-only invariants
Session logs, ADRs, LESSONS rows, and stepping-stone trails are append-only by contract and enforced by `runtime-hooks/governance-audit`. You cannot quietly rewrite history. This is the single most important property for trust: errors are discoverable.
**Leverage:** Publish the append-only invariant as one of the twelve public commitments in [`TRUST.md`](TRUST.md) §2.2.

### S5. Breadth — 16 councils, 92 agents, 66 skills
Coverage spans security (CISO + CRT), quality (CEVO + CAO), reliability (CSRE + CIR), governance (CGov + CEthics), growth (CTE + CKT + CRhy), career (CCar), ops (CPlan + CMem), plus the CEO. Most agent frameworks ship one persona; we ship an institution.
**Leverage:** Market the coverage; don't apologize for the weight.

### S6. Runtime hooks are non-optional
Six hooks (`secrets-scanner`, `tool-guardian`, `governance-audit`, `dependency-license-checker`, `session-logger`, `commit-gate`) run on every session. They are not features the user enables; they are part of the plugin boot sequence. Missing them is a visible failure, not a silent degradation.
**Leverage:** Document the hook contract publicly in [`SECURITY.md`](SECURITY.md) — already done at v0.4.2.

### S7. Prompt-diff discipline
Persona and skill edits go through `councils/prompt-reviewer/AGENTS.md` before merge. This is the discipline that keeps the Agency from drifting into a softer, more agreeable version of itself one PR at a time. Without it, every multi-agent system reverts toward the mean over six months.
**Leverage:** Extend prompt-diff to all founding documents at v0.6.0. Today it covers personas and skills; at v0.6.0 it should also cover [`CONSTITUTION.md`](CONSTITUTION.md), [`VALUES.md`](VALUES.md), [`MISSION.md`](MISSION.md), [`SECURITY.md`](SECURITY.md), [`TRUST.md`](TRUST.md).

### S8. STRIDE + OWASP + ASI + AI RMF coverage
Threat modeling uses STRIDE; application security uses OWASP Top 10 (2021); agent-specific risks use OWASP ASI Top 10 (2025); AI risk is framed against NIST AI RMF 1.0 and ISO/IEC 42001. This is the strongest publicly available synthesis and we use all four lenses, not just one.
**Leverage:** Publish the crosswalk in [`THREAT-MODEL.md`](THREAT-MODEL.md) at v0.5.0 so an auditor can see all four frameworks overlaid.

### S9. Vault-refs only, never raw secrets
Hard-coded in the Constitution as a non-waivable class. Raw secrets cannot enter the repo, cannot enter session logs, cannot enter artifacts. `secrets-scanner` enforces at hook time, `commit-gate` enforces at commit time. This is the single most common reason AI-assisted repositories leak credentials; we made it architecturally impossible.
**Leverage:** Cite the non-waivable class in every security review.

### S10. SBOM + SLSA supply-chain posture
SPDX SBOM generated per project; SLSA provenance is the target for signed artifacts. Most independently-shipped plugins have zero supply-chain telemetry.
**Leverage:** Raise the SLSA target to Level 3 at v0.7.0 (signed, non-forgeable provenance, hardened build).

### S11. Never-give-up ladder
Eight rungs. Rungs 7 (park) and 8 (retire) are USER-ONLY, so the Agency cannot silently abandon a task. Every rung is logged. The ladder replaces the anti-pattern of "assistant gives up politely and the user doesn't notice."
**Leverage:** Surface rung changes in the session header so the User sees escalation events without reading logs.

### S12. Keeper Test quarterly drill
Four-hour adversarial drill ([`KEEPER-TEST.md`](KEEPER-TEST.md)). Simulates injection attacks, waiver abuse, secret exposure, supply-chain compromise, and ASI-class requests. Most agencies discover gaps in production; we force the discovery on a calendar.
**Leverage:** Publish drill results to [`TRUST.md`](TRUST.md) §3 each quarter.

### S13. Ten USER-ONLY actions, enumerated
[`CONSTITUTION.md`](CONSTITUTION.md) §2.2. Financial transactions, production deploys, legal commitments, public posts, talent decisions, security overrides, destructive data ops, vendor contracts, model-scale decisions, ASI-class requests. The list is short, exhaustive, and public. No one has to guess where the line is.
**Leverage:** Keep the list short. Growth of USER-ONLY actions past fifteen would signal creeping paranoia; growth below ten would signal creeping autonomy. Ten is the sweet spot.

### S14. MIT license + public SECURITY.md + public TRUST.md
Transparency is not performative: the source, the policy, and the commitments are all readable. A bad actor cannot hide; a good auditor cannot be blocked.
**Leverage:** Add [`DISASTER-RECOVERY.md`](DISASTER-RECOVERY.md) at v0.5.0 to complete the public-trust triad (policy + commitments + recovery).

---

## 2. Weaknesses (W)

The Agency's **honest failure modes** — what is missing, fragile, or unproven. This section exists so that a critic does not need to discover anything by reading the code.

### W1. Constitution is new and untested in long-horizon practice
Ratified 2026-04-20. A constitution proves itself in crisis, not in calm weather. We have not yet weathered a high-pressure waiver request, a contested CEO override, or a sustained pattern of Critical findings.
**Mitigation:**
- Run the Keeper Test at the end of April 2026 (first scheduled drill).
- Log every constitutional citation in session receipts so amendment patterns become visible.
- Treat the first year as a probation period — any amendment in year one requires two councils' concurrence in addition to USER approval.
**Owner:** CGov. **Target:** Keeper Test #1 (2026-04-30).

### W2. No third-party audit
Self-certification has limits. At some point a neutral observer must verify the claims in [`TRUST.md`](TRUST.md).
**Mitigation:**
- v0.7.0: engage a neutral reviewer (external researcher or security firm) for a point-in-time audit against ISO/IEC 42001 clauses.
- Publish audit report + remediation plan regardless of outcome.
**Owner:** CAO. **Target:** v0.7.0.

### W3. No CI/CD automation of hooks
The hooks are specified and runnable, but there is no GitHub Actions workflow that runs them on every push. A contributor could theoretically merge something that would fail the hooks locally.
**Mitigation:**
- v0.6.0: add `.github/workflows/hooks.yml` running `runtime-hooks/*` on push and PR.
- Branch protection requires the workflow to pass.
**Owner:** CSRE. **Target:** v0.6.0.

### W4. Single-user bottleneck
The Agency is designed around one User (the CEO) who is the source of all USER-ONLY decisions. If the User is unreachable, certain actions cannot proceed.
**Mitigation:**
- [`DISASTER-RECOVERY.md`](DISASTER-RECOVERY.md) at v0.5.0 defines a read-only mode the Agency enters when the User is unreachable >72h. In read-only mode the Agency continues to analyze and log but will not ship.
- v0.8.0: optional "trusted deputy" pattern where the User can pre-designate one other human to authorize a narrow class of emergency-only USER-ONLY actions (e.g., incident containment). The deputy cannot authorize ASI-class or raw-secret actions.
**Owner:** CRes. **Target:** v0.5.0 (read-only mode), v0.8.0 (deputy).

### W5. No privacy specialist council
We handle privacy via the CISO + CAO. That is adequate for secret-handling but not for DPIA work, GDPR Article 35 assessments, CCPA/DPDP compliance, data-minimization, or retention policy.
**Mitigation:**
- v0.5.0 ships `skills/privacy/SKILL.md` — DPIA template, GDPR/CCPA/DPDP checklists, privacy-by-design patterns.
- v0.6.0: elevate to `councils/privacy/AGENTS.md` (CPRIV) with blocking veto on data flows matching PII/sensitive categories.
**Owner:** CISO → CPRIV. **Target:** v0.5.0 → v0.6.0.

### W6. No accessibility standard
WCAG 2.2 / ADA / EN 301 549 coverage is absent. Any UI the Agency ships today could fail accessibility without being caught.
**Mitigation:**
- v0.5.0 ships `skills/accessibility/SKILL.md` — WCAG 2.2 AA checklist + ADA triggers.
- v0.7.0: `councils/accessibility/AGENTS.md` (CA11y) with veto on public-facing UI that fails automated checks.
**Owner:** CEVO → CA11y. **Target:** v0.5.0 → v0.7.0.

### W7. No fairness / bias audit discipline
When the Agency produces analyses across demographics, populations, or segments, there is no standing check for fairness or bias.
**Mitigation:**
- v0.5.0 ships `skills/fairness/SKILL.md` — fairness criteria, group-level error-rate checks, a checklist for when an output could affect people differently.
- Wire the skill into `councils/ethics/AGENTS.md` as the default fairness reviewer.
**Owner:** CEthics. **Target:** v0.5.0.

### W8. No root-cause analysis discipline
Incidents are logged, but there is no explicit RCA skill. Teams that only have "post-mortem" without "5 Whys + Ishikawa + fault tree" produce narrative post-mortems that miss the actual root cause 30-50% of the time.
**Mitigation:**
- v0.5.0 ships `skills/rca/SKILL.md` — 5 Whys, Ishikawa, fault tree, "blameless" framing, action-item ownership.
- CIR (Incident Response) MUST produce an RCA for every Severity ≥ High incident using the skill.
**Owner:** CIR. **Target:** v0.5.0.

### W9. No published trust scorecard data
[`TRUST.md`](TRUST.md) §3 defines the scorecard; scorecard data has not been published yet because we have only just ratified the commitments.
**Mitigation:**
- First scorecard publish: 2026-07-22 (90 days after TRUST.md ratification).
- Every subsequent quarter: scorecard published alongside Keeper Test results.
**Owner:** CAO. **Target:** 2026-07-22.

### W10. No disaster recovery plan
What happens if the repo is wiped, the main branch is rewritten, or the release archives are lost? Today the answer is "git reflog and hope", which is not a plan.
**Mitigation:**
- v0.5.0 ships [`DISASTER-RECOVERY.md`](DISASTER-RECOVERY.md) with RPO/RTO targets, backup cadence, append-only restoration protocol, and signed-tag recovery procedure.
**Owner:** CSRE + CRes. **Target:** v0.5.0.

### W11. No plugin-level threat model
`SECURITY.md` §6 has a condensed threat model, and per-project threat models are produced, but there is no dedicated document that STRIDEs the plugin itself — supply chain, session artifacts, memory leakage between projects, plugin-vs-host trust boundary.
**Mitigation:**
- v0.5.0 ships [`THREAT-MODEL.md`](THREAT-MODEL.md) — full STRIDE on the plugin surface plus the OWASP ASI crosswalk.
**Owner:** CRT. **Target:** v0.5.0.

### W12. No contributing / code-of-conduct docs
The repo has MIT license, README, SECURITY, but a new contributor (or Anthropic partner) has nowhere to find contribution rules, review expectations, or community behavior standards.
**Mitigation:**
- v0.5.0 ships `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1), `CONTRIBUTING.md`, `CODEOWNERS`, `.well-known/security.txt` (RFC 9116).
**Owner:** CGov. **Target:** v0.5.0.

### W13. No system card
Anthropic and other vendors publish system cards describing capabilities and limits. We have not. A system card forces honesty about what the Agency cannot do, and prevents false expectations.
**Mitigation:**
- v0.5.0 ships [`SYSTEM-CARD.md`](SYSTEM-CARD.md) describing capabilities, tested bounds, untested territory, and known failure modes.
**Owner:** CEVO. **Target:** v0.5.0.

### W14. Memory novelty gate is binary
The Jaccard novelty gate is set at 0.65 for memory additions. Binary threshold is easier to reason about than a learned model but can miss subtle duplication or accept near-duplicates.
**Mitigation:**
- Keep 0.65 as baseline.
- v0.8.0: add a second check — if memory growth exceeds a budget (e.g., 500 rows/quarter) trigger a CMem review.
**Owner:** CMem. **Target:** v0.8.0.

### W15. No formal training or onboarding for the User
The Agency is complex. A User who does not read the Constitution may under-use or misuse it.
**Mitigation:**
- v0.6.0: `docs/ONBOARDING.md` — 20-minute tour, 60-minute deep-dive, 1-hour Keeper-Test-as-tutorial.
- Surface "start here" links in the first session after install.
**Owner:** CRhy + CTE. **Target:** v0.6.0.

### W16. Small project / customer base = low real-world exposure
The Agency has not yet survived the adversarial pressure of many concurrent projects, many waiver requests, or many real incidents. Confidence is high, sample size is low.
**Mitigation:**
- Treat the first 20 projects shipped as a learning cohort. Publish lessons to [`LESSONS.md`](LESSONS.md) with the `EARLY_COHORT` tag.
- After 20 projects, run a meta-review and amend the Constitution if patterns demand it.
**Owner:** CKT. **Target:** rolling.

### W17. No formal cost / resource model
The Agency can run expensive workflows (multi-council review, drills, RCA). There is no budget discipline.
**Mitigation:**
- v0.7.0: `skills/cost-model/SKILL.md` and a quarterly cost-vs-value report to the User.
**Owner:** CPlan. **Target:** v0.7.0.

### W18. CONSTITUTION amendment process is USER-ONLY but thin on deliberation
USER approval is necessary and sufficient for amendment. This is correct for ultimate authority but thin on deliberation — no mandatory waiting period, no required council input.
**Mitigation:**
- v0.6.0 amendment to Article X: any Constitutional amendment requires (a) USER approval, (b) a 7-calendar-day cooling-off period between proposal and ratification, (c) a CAO review note attached to the amending ADR. Emergency amendments may bypass (b) only for non-waivable-class issues, and must be re-ratified within 30 days.
**Owner:** CGov. **Target:** v0.6.0.

---

## 3. Opportunities (O)

**External conditions the Agency can capture** if it pushes now.

### O1. Claude Code plugin ecosystem is young
The plugin ecosystem is in its first year. A high-trust, multi-council agency plugin is a differentiated position. Most existing plugins ship a single persona or a skill bundle.
**Push:** Keep shipping. Every wave closes a gap competitors haven't noticed yet. Target: be the reference Claude Code plugin for DevSecOps work by v1.0.0.
**Owner:** CEO + CTE.

### O2. AI-safety research is adopting constitutional patterns
Anthropic's Constitutional AI paper popularized the idea; agent-framework research is following. Our [`CONSTITUTION.md`](CONSTITUTION.md) is an applied instance at the right level of abstraction — neither research-only nor compliance-only.
**Push:** Write a brief public case-study ("What a Constitutional Multi-Agent Agency Looks Like in Practice"). Link from README. Target: v0.7.0.
**Owner:** CKT.

### O3. Self-certification path to SOC 2 / ISO 27001 / ISO 42001
We already align with most controls. A self-attestation followed by independent audit is a credible path.
**Push:** v0.7.0 external audit (see W2). v0.9.0: SOC 2 Type I self-attestation, publicly documented. v1.1.0: ISO/IEC 42001 certification if adoption justifies it.
**Owner:** CAO.

### O4. Privacy + Accessibility + Fairness councils can become differentiators
Most agent frameworks ignore these domains. Shipping [`councils/privacy/AGENTS.md`](councils/privacy/AGENTS.md), [`councils/accessibility/AGENTS.md`](councils/accessibility/AGENTS.md), and expanding [`councils/ethics/AGENTS.md`](councils/ethics/AGENTS.md) to cover fairness lifts the Agency into territory that competitors will find hard to catch up with.
**Push:** v0.5.0 skills → v0.6.0 → v0.7.0 councils. Don't rush the council until the skill has survived two quarters of use.
**Owner:** CISO → CPRIV, CEVO → CA11y, CEthics.

### O5. Community governance pattern
The Agency's governance could scale to a contributor community without collapsing, because the boundaries are explicit. A public CONTRIBUTING + CODEOWNERS + CODE_OF_CONDUCT (shipping v0.5.0) turns the Agency from "one person's repo" into "a community anyone can join."
**Push:** Accept contributions starting v0.6.0. Require contributors to sign the CLA referencing [`VALUES.md`](VALUES.md).
**Owner:** CGov.

### O6. Multi-tenant / team mode
Today the Agency assumes one User. A team mode where multiple users hold different USER-ONLY authorities (CEO for shipping, CFO for spend, CISO-human for security overrides) is a natural extension.
**Push:** v0.9.0 design spike, v1.0.0 implementation. Gate on (a) W18 amendment-deliberation discipline being proven, (b) W4 deputy pattern being proven.
**Owner:** CPlan.

### O7. Plugin federation — DevSecOps-Agency as a reference implementation that other vertical agencies inherit
Someone will build Legal-Agency, Finance-Agency, Healthcare-Agency. If ours is the reference Constitution + councils pattern, they will subclass it. That is a positive-sum outcome.
**Push:** v0.8.0: publish a "fork-friendly skeleton" extracted from the Agency — `agency-skeleton/` minus domain-specific content.
**Owner:** CKT.

### O8. Research contribution — Keeper Test corpus
The Keeper Test drill produces structured adversarial prompts + expected responses. This is a corpus researchers want. We can publish (redacted) quarterly Keeper Test logs as a contribution to AI-safety research.
**Push:** v0.7.0: first public Keeper Test corpus release.
**Owner:** CAO + CKT.

### O9. Sustainability council
Cost-per-session, energy-per-session, model-inference cost, token budgets. Shipping an ops discipline around these would pre-empt the inevitable regulatory focus on AI resource use.
**Push:** v1.0.0: `councils/sustainability/AGENTS.md` (CSUS). Quarterly sustainability report.
**Owner:** CPlan → CSUS.

### O10. Regulatory window — EU AI Act, DPDP (India), evolving US state laws
Being early on documentation (system card, DPIA templates, logs) means the Agency is already aligned when regulation arrives. Late adopters will struggle.
**Push:** Map each emerging regulation to existing Agency artifacts and publish the crosswalk. Target: annually in January.
**Owner:** CGov + CAO.

---

## 4. Threats (T)

**External conditions that could harm the Agency** — things we do not control but must blunt.

### T1. Prompt injection / data-poisoning escalation
Attackers get better. Our defenses (`injection-defense`, `tool-guardian`, Immutable Security Rules at the prompt level) are strong but not invincible.
**Blunt:**
- Keep CRT drills current — every quarter adds new injection patterns from the literature.
- Monitor OWASP ASI Top 10 revisions; adjust runtime hooks within 30 days of any new Top 3 item.
- Maintain an allow-list posture on tool calls that can move data off-system; never an deny-list.
**Owner:** CRT + CISO.

### T2. Supply-chain compromise
A dependency is backdoored; an action workflow is poisoned; a release key is stolen.
**Blunt:**
- SBOM on every project, licenses checked on every hook run.
- SLSA Level 2 now, Level 3 at v0.7.0 (signed + non-forgeable).
- PAT tokens rotated per `runtime-hooks/secrets-scanner` guidance; never store PATs in the repo.
- `DISASTER-RECOVERY.md` (v0.5.0) covers compromise recovery.
**Owner:** CISO + CSRE.

### T3. Model vendor outage or deprecation
Claude becomes unavailable, or a capability we rely on is removed.
**Blunt:**
- Never depend on a capability not documented in the Anthropic public model card.
- Keep a `FALLBACK_CAPABILITIES.md` appendix (v0.6.0) listing degraded modes per critical capability.
- For extended outage (>48h), Agency enters read-only mode per W4 / `DISASTER-RECOVERY.md`.
**Owner:** CSRE.

### T4. Model behavior drift
A model version change silently alters agent behavior. The prompt-diff discipline catches prompt drift, but model drift is harder.
**Blunt:**
- Pin model version in [`CLAUDE.md`](CLAUDE.md) and bump explicitly via ADR.
- Run the Keeper Test on the first production session after any model version change.
- Publish any surprising behavior shift to LESSONS with tag `MODEL_DRIFT`.
**Owner:** CEVO + CSRE.

### T5. Constitutional amendment abuse
A future pressure moment produces a rushed amendment that weakens a control. This is the single most insidious governance failure.
**Blunt:**
- W18 fix (7-day cooling-off period for non-emergency amendments, CAO review required).
- Year-one probation rule (W1).
- Public amendment log required; deletions from the log are cryptographically visible (append-only).
- The non-waivable classes (raw-secret + ASI) cannot be amended at all without a new Constitutional version — baseline at [`CONSTITUTION.md`](CONSTITUTION.md) §8.5.
**Owner:** CGov.

### T6. User fatigue
The User is the single point of approval for USER-ONLY actions. Fatigue could cause rubber-stamping.
**Blunt:**
- Every USER-ONLY approval request must include the minimum decision-critical context. No "please approve X" without the structured brief.
- Track approval latency over time; an approval that takes <10 seconds consistently is a fatigue signal.
- CRhy runs a quarterly "User fatigue check" during the Keeper Test.
**Owner:** CRhy + CEO.

### T7. Reputational harm from a single incident
A single leak, a single bad waiver, a single ASI-adjacent slip-up could undo a year of earned trust.
**Blunt:**
- Incident timeline published within 48h per [`TRUST.md`](TRUST.md) §4, regardless of fault.
- Non-waivable classes make the worst incident categories architecturally rare.
- Post-incident RCA via `skills/rca` + LESSONS entry + (if >= High) a Constitutional amendment proposal if a control gap is found.
**Owner:** CIR + CAO.

### T8. Regulatory change
EU AI Act phases in; DPDP (India) rules evolve; US state laws diverge; export controls shift.
**Blunt:**
- Annual regulatory crosswalk (O10).
- Maintain [`SECURITY.md`](SECURITY.md) in a form acceptable to EU AI Act Article 10 (logging) and Article 15 (transparency).
- Privacy council (O4 → W5) handles the DPDP + GDPR + CCPA triangle.
**Owner:** CGov + CAO.

### T9. Claude Code platform change breaking the plugin
A breaking change in plugin manifest schema, skill loading, or hook execution invalidates our shipping format.
**Blunt:**
- Pin plugin manifest version in `.claude-plugin/plugin.json`.
- Subscribe to Anthropic changelog and run a compatibility check within 7 days of any release affecting `claude.md` / skills / plugins.
- Keep the `agency-skeleton/` pattern (O7) decoupled from the manifest so content survives schema changes.
**Owner:** CSRE + CTE.

### T10. Adversarial fork / bad-actor use
The plugin is MIT-licensed. A bad actor could fork it, strip the safety controls, and ship a dangerous derivative under a similar name.
**Blunt:**
- Trademark and naming: the name "DevSecOps-Agency" is associated with this repository only. Published [`VALUES.md`](VALUES.md) and [`SECURITY.md`](SECURITY.md) make clear what is and is not the original.
- MIT does not restrict fork, but the Constitution requires that forks retain the USER-ONLY list and non-waivable classes if they ship under any name containing "Agency" — enforced socially via [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) (v0.5.0) and legally via the LICENSES/NOTICE pattern.
**Owner:** CEO + CGov.

### T11. Knowledge loss if CEO is unavailable
All tacit knowledge outside the written corpus is lost if the CEO is incapacitated.
**Blunt:**
- All operational decisions are captured in session logs (append-only).
- All strategic decisions are captured in ADRs.
- [`RESILIENCE.md`](RESILIENCE.md) + `DISASTER-RECOVERY.md` (v0.5.0) cover continuity.
- Quarterly "knowledge extraction" pass by CMem — summarize tacit patterns found in session logs into LESSONS rows.
**Owner:** CRes + CMem.

### T12. Drift toward agreeableness
The subtlest threat. Over time, an agent system wants to please the User; pleasing means producing fewer objections. A year from now, the four blocking vetoes could each be used 50% less.
**Blunt:**
- Track veto-invocation rate in [`TRUST.md`](TRUST.md) §3. A veto rate that trends to zero without a corresponding decrease in high-severity findings is a drift signal.
- CAO audits a sample of sessions each quarter for "missed veto opportunities."
- Keeper Test includes scenarios specifically designed to require a veto — a drill that passes with no vetoes invoked is a drill that failed.
**Owner:** CAO + CRhy.

---

## 5. Mitigation Roadmap by Wave

This section rolls the action lines above into a release roadmap so that each mitigation has a target wave and owner.

### v0.5.0 — Trust + Completeness (this wave)

- [`TRUST.md`](TRUST.md) — addresses W9 baseline.
- `SWOT.md` (this file) — addresses the meta-gap of "no written self-audit."
- [`SYSTEM-CARD.md`](SYSTEM-CARD.md) — addresses W13.
- [`THREAT-MODEL.md`](THREAT-MODEL.md) — addresses W11.
- [`DISASTER-RECOVERY.md`](DISASTER-RECOVERY.md) — addresses W10 + W4 (read-only mode) + T3 + T11.
- `CODE_OF_CONDUCT.md` / `CONTRIBUTING.md` / `CODEOWNERS` / `.well-known/security.txt` — addresses W12 + O5 partial.
- `skills/rca/SKILL.md` — addresses W8.
- `skills/privacy/SKILL.md` — addresses W5 (skill layer).
- `skills/accessibility/SKILL.md` — addresses W6 (skill layer).
- `skills/fairness/SKILL.md` — addresses W7.
- `skills/trust-scorecard/SKILL.md` — supports TRUST.md §3 publication cadence.
- `skills/system-card/SKILL.md` — supports SYSTEM-CARD.md regeneration.
- Constitution Schedule A amended to list the new documents.

### v0.6.0 — CI + Privacy council + User onboarding

- `.github/workflows/hooks.yml` — addresses W3.
- `councils/privacy/AGENTS.md` (CPRIV) — addresses W5 (council layer).
- `docs/ONBOARDING.md` — addresses W15.
- Prompt-diff extended to all founding documents — S7 leverage.
- Constitution Article X amended for 7-day cooling-off period — addresses W18 + T5.

### v0.7.0 — External audit + Accessibility council + SLSA L3

- External audit against ISO/IEC 42001 — addresses W2 + O3.
- `councils/accessibility/AGENTS.md` (CA11y) — addresses W6 (council layer).
- SLSA Level 3 artifacts — T2 leverage.
- Public Keeper Test corpus release — O8.
- `skills/cost-model/SKILL.md` — addresses W17.
- Constitutional pattern case-study published — O2.

### v0.8.0 — Trusted deputy + fork-friendly skeleton + memory budget

- Trusted deputy pattern — addresses W4.
- `agency-skeleton/` reference fork — O7.
- Memory growth budget + CMem review trigger — addresses W14.

### v0.9.0 — SOC 2 Type I self-attestation + multi-tenant design spike

- Public SOC 2 Type I — O3.
- Multi-tenant design spike — O6.

### v1.0.0 — Reference plugin status + Sustainability council + multi-tenant

- `councils/sustainability/AGENTS.md` — O9.
- Multi-tenant implementation — O6.

---

## 6. Review Cadence

- **Every Keeper Test (quarterly):** re-score every S/W/O/T item. Add new items; remove items that have been closed out. New version of this document.
- **At every minor version bump (v0.X.0):** update the mitigation roadmap section §5.
- **Annually (January):** full regulatory crosswalk (T8) and append as appendix.

---

## 7. Document Control

- **File:** `SWOT.md`
- **Version:** 1.0 (ratified 2026-04-22 with plugin v0.5.0)
- **Owner:** CEO
- **Reviewer:** CAO
- **Append-only:** No (this file is a rolling analysis; prior versions are preserved via git history)
- **Change policy:** Any change to this document is an ADR-grade decision. Material changes to Strengths/Weaknesses require CAO concurrence; changes to Opportunities/Threats require CTE and CRT concurrence.
- **References (original synthesis, not verbatim):**
  - Weihrich, "The TOWS Matrix — A Tool for Situational Analysis" (Long Range Planning, 1982) — the S/W/O/T framework and its paired-mitigation extension.
  - NIST Cybersecurity Framework 2.0 — risk treatment language.
  - NIST AI Risk Management Framework 1.0 — risk categories and lifecycle stages.
  - ISO/IEC 42001:2023 — AI management system controls.
  - CNCF Security Whitepaper v2.0 — supply-chain and platform-threat categorization.
  - Google SRE Book (Beyer et al.), chapters on error budgets and post-mortems.

---

*The Agency that does not name its own weaknesses cannot be trusted with its strengths.*
