# CONTEXT.md — DevSecOps-Agency ubiquitous language

The Agency's domain glossary. Read this when terms in ADRs, skills, council files, or session logs feel unfamiliar. **Do not couple this file to implementation details** — only terms meaningful to humans-in-the-loop or to agents reasoning about the Agency.

Established **2026-04-26** with plugin v0.6.1. Convention is documented in [`docs/adr/ADR-0001-context-md-convention.md`](docs/adr/ADR-0001-context-md-convention.md). The "ubiquitous language" pattern this file operationalizes is from Eric Evans, **Domain-Driven Design** (Addison-Wesley, 2003).

## How to use this file

- The `grill-with-docs` skill (v0.6.1) updates this file inline as terms get resolved during a grilling session.
- When a term in a council file or skill conflicts with the canonical definition here, this file wins. File a `language-conflict` ADR if the conflict is load-bearing.
- New terms are added lazily — only when first resolved, not pre-populated.
- Per-project `CONTEXT.md` files live at `<slug>/CONTEXT.md` (per the same convention) and inherit from this Agency-level file. Project-level terms override Agency-level definitions for that project's scope.

## Core entities

### Agency
The 16-council autonomous organization defined by [`CONSTITUTION.md`](CONSTITUTION.md) and the Schedule A founding documents. The agent collective that takes a User directive at Phase 1 and produces shipped artifacts at Phase 7 with full receipts.
*Avoid*: "the system," "the platform," "the bot."

### Council
One of the 16 named decision-making bodies (Strategy, Product, Architecture, Research, Security, Red-Team, Evaluation, Audit, Quality, Execution, DevOps, SRE, Docs, Legal, Marketing, People-Ops). Each has a **Chief**, an **AGENTS.md** scope file, and a **TEAM.md** roster.
*Avoid*: "team," "department," "group" (use "council" everywhere; collapses internal jargon).

### Chief
The lead agent of a Council. Sixteen total. **Blocking chief** = CISO, CRT, CEVO, CAO (hold strict veto over ship). **Informing chief** = the other twelve. See `GOVERNANCE.md`.
*Avoid*: "council head," "lead," "boss" (use "Chief").

### Specialist
An agent reporting to a Chief, owning a specific skill or workflow. E.g. `panel-chair` (under CEVO) owns `cross-model-panel`.
*Avoid*: "expert," "agent" (when a Specialist is meant — "agent" is the broader category).

### Worker
An ephemeral, parallel-dispatched agent spawned by a Specialist when work shards cleanly. See `agents/AGENTS.md` Worker tier.
*Avoid*: "subagent" (Worker is the precise term in the Agency).

### Sovereign / User
The single human directing the Agency. Holds the **ten USER-ONLY actions** per Constitution §2.2. The Agency has exactly one Sovereign per session.
*Avoid*: "owner," "operator," "client."

## Process entities

### Phase
One of the Agency's seven phases: 1 Intake, 2 Design, 3 Build, 4 QA, 5 Security, 6 Deploy, 7 Close. Defined in `AGENTS.md`.
*Avoid*: "stage" (use "stage" only for cross-model panel's Stage 1/2/3 — those are unrelated).

### Project
A single piece of work the Agency takes on, scoped at Phase 1 Intake. Each project has a `<slug>/` folder containing its `brief.md`, `architecture.md`, `<slug>/CONTEXT.md`, ADRs, security artifacts, and shipped output.
*Avoid*: "task," "job," "engagement."

### Slug
The kebab-case identifier for a project (e.g. `dorm-splitter`, `invoice-app`). The folder name and the prefix for all per-project artifacts.
*Avoid*: "name," "id."

### ADR
**Architecture Decision Record.** Markdown file at `_decisions/<slug>/adrs/ADR-NNNN-<kind>-<slug>.md` (per-project) or `docs/adr/ADR-NNNN-<topic>.md` (Agency-level, established v0.6.1). Required for: every phase transition, every blocking-council verdict, every waiver, every Constitution amendment, every cross-model-panel run. Append-only per Constitution §5.2.
*Avoid*: "decision doc," "design doc."

### Receipt
Any artifact that proves a decision happened: an ADR, a session log entry, a LESSONS row, a stepping stone, a drill report. Constitution §5.1 (receipts ratio = 100%) is the load-bearing invariant.
*Avoid*: "log," "audit trail" (unless quoting external systems).

### Waiver
Time-boxed exception (≤ 90 days, calendar date) to a blocking-council red gate. USER-approved. Two classes are non-waivable per Constitution §8.5: **raw-secret** and **ASI-class**.
*Avoid*: "exception," "override," "exemption."

### Heartbeat
A scheduled rhythm event per `RHYTHM.md`: daily, weekly, monthly, quarterly. Each heartbeat produces a markdown file under `_vision/rhythm/`. Trust commitment §2.9 — no missed quarter.
*Avoid*: "checkin," "standup," "sync."

### Drill
End-to-end resilience exercise per `RESILIENCE.md > Drills`. Five named kinds (chief-unavailable, heartbeat-miss, model-outage, waiver-expiry, compaction-loss) on four cadences. Distinct from **chaos game day** (added v0.5.6, exercises unknown failure modes).
*Avoid*: "test," "rehearsal."

### Panel
A run of `cross-model-panel` (added v0.5.7, expanded v0.6.0). Four panelists deliberate on a hard question; Chairman synthesizes; ADR captures the receipt.
*Avoid*: "council" (a Panel is NOT a Council — Council is the long-lived organizational body; Panel is a one-shot deliberation event).

### Trigger event
Any event that auto-invokes a skill or specialist. Cross-model-panel default-triggers: ASI-class findings, Constitution amendments, USER-ONLY decisions over COST §2.4 threshold.
*Avoid*: "event," "hook fire" (use "trigger event").

## Tooling entities

### Runtime hook
A `.sh` script under `runtime-hooks/<name>/` that fires on a Claude Code lifecycle event (preToolUse, sessionEnd, scheduled). Eight in v0.6.1: secrets-scanner, tool-guardian, governance-audit, dependency-license-checker, session-logger, commit-gate, cost-gate (added v0.5.6), git-guardrails (added v0.6.1). Per `TRUST.md` §2.7, hooks are non-optional — bypass files a `runtime-hook-bypass` ADR.
*Avoid*: "guard," "filter."

### Skill
A markdown file under `skills/<name>/SKILL.md` (plus optional `references/`) that prescribes a procedure invokable by an agent. Skills are dispatched by Specialists; they don't dispatch themselves.
*Avoid*: "playbook," "command," "tool."

### Vault ref
A reference to a secret stored outside the repo. Constitution §8.5 requires that secrets only ever appear as vault refs in committed artifacts (raw-secret class is non-waivable).
*Avoid*: "credential," "API key" (when a vault ref is meant — those terms are fine when referring to the underlying secret type).

## Mode entities (cross-model-panel v0.6.0)

### Baseline mode
Single-round, parallel, Claude-only, average-rank — the v0.5.7 default for `cross-model-panel`. Backwards-compatible.

### Multi-round
Successive rounds where panelists see each other's evaluations and revise. Round 1 raw is preserved verbatim as the **diversity record**. INAPPROPRIATE for subjective judgment, time-pressured decisions, or Constitution amendments.
*Avoid*: "iterative debate" (use "multi-round" for the panel mode; "iterative debate" is the broader research category).

### Adversarial-pair
Two of four panelists assigned AFFIRMATIVE / NEGATIVE roles for binary, comparative, or verdict-frame questions. Role-rotation cap: 60% trailing-10. INAPPROPRIATE for open-ended questions or Constitution amendments.

### Cross-vendor
Panel via OpenRouter spanning Anthropic + OpenAI + Google + xAI/Mistral. Chairman stays on direct Anthropic API. Minimum 3 distinct vendors for the label to apply. OpenRouter key is non-waivable raw-secret per Constitution §8.5.

### Diversity record
The verbatim Stage-1 round-1 raw responses preserved in a panel ADR. Mitigates the funneling effect (semantic diversity peaks in round 1 and narrows on synthesis).
*Avoid*: "audit trail" (different concept — diversity record is specifically about preserving disagreement signal pre-synthesis).

## Flagged ambiguities (resolved)

- "council" vs "panel" — resolved: **Council** = long-lived organizational body of 16 named bodies; **Panel** = one-shot deliberation event in `cross-model-panel`. They are not the same thing.
- "stage" vs "phase" — resolved: **Phase** = the seven Agency phases (1-7); **Stage** = the three steps inside a `cross-model-panel` run (Stage 1/2/3). Don't conflate.
- "agent" vs "Specialist" vs "Worker" — resolved: **Agent** is the broad category; **Chief / Specialist / Worker** are the three tiers per `CAREER.md`.
- "secret" vs "vault ref" — resolved: a **secret** is the underlying credential; a **vault ref** is the reference to it that may appear in committed artifacts. Raw secrets in artifacts are non-waivable per Constitution §8.5.

## Provenance

- Eric Evans, **Domain-Driven Design** (Addison-Wesley, 2003) — origin of the "ubiquitous language" concept this file operationalizes.
- Agency-specific synthesis: which entities to enumerate, the "*Avoid*" pattern, the resolved-ambiguities section, the per-mode entities for cross-model-panel, the per-project inheritance rule.
