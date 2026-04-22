# skills/ — rules for every skill

Telegraph. Read before authoring or editing a skill.

## File shape

- `skills/<name>/SKILL.md` with YAML frontmatter: `name`, `description`, `metadata.version`.
- `name` in frontmatter == directory name.
- `description` ≥ 2 sentences. Start: "This skill should be used when...". List trigger phrases.
- SKILL.md ≤ 200 lines. Move detail to `references/`.

## Progressive disclosure

- SKILL.md: what the skill does, when to trigger, top-level steps. No tables of knob defaults.
- `references/*.md`: exact knob values, schemas, recipes, edge cases.
- Link references explicitly from SKILL.md (`See references/foo.md`).

## Content rules

- Rules > prose. Bullets > paragraphs.
- Every instruction is either an imperative or an assertion.
- No "might", "could", "consider". Use "must", "does", "never".
- Frontmatter `description` is the router — it must contain enough keywords to trigger on the right user utterances.

## Versioning

- `metadata.version` follows semver. Bump on contract changes (schema, artifact paths, trigger phrases).
- Plugin root `plugin.json.version` bumps when ≥ 1 skill bumps.

## Skill index (v0.4.0)

| Skill              | Trigger                                                 |
| ------------------ | ------------------------------------------------------- |
| `ceo`              | Main entry point. `/devsecops-agency:ceo`.              |
| `ship-it`          | Legacy v0.1 pipeline.                                   |
| `command-center`   | Dashboard artifact.                                     |
| `board-meeting`    | Power-user re-run of a board phase.                     |
| `council-meeting`  | Power-user re-run of a council.                         |
| `intake`           | Q&A only, no engineering.                               |
| `status`           | Text summary.                                           |
| `escalate`         | Process parked questions.                               |
| `retro`            | Post-deploy retro + REM dreaming trigger.               |
| `memory`           | Read/write durable memory (Light/Deep/REM) with novelty gate. v0.3.0 extends read path to ADRs + meetings. |
| `session-log`      | Per-agent append-only JSONL.                            |
| `gates` (internal) | Gate vocabulary + aggregation. CEO invokes on report.   |
| `taskflow` (internal) | Task state machine + fix-loop cap. CEO invokes on dispatch/report. |
| `worktree` (internal) | Isolated scratch dirs for parallel + fix-loop dispatches. CEO invokes on dispatch/report. |
| `skill-creator`    | Runtime roster extension — author new agents + skills. CEO invokes on domain gap. |
| `model-tiering`    | Per-agent tier assignment (Haiku/Sonnet/Opus). CEO reads on every dispatch. |
| `notify`           | Push-notify surface on close/block/REM. Rate-limited.   |
| **`vision-doc`** (v0.3.0) | Workspace VISION.md — mission + ≤ 5 OKRs + ≤ 5 non-goals. 3-bullet slice prepended to every dispatch. |
| **`okr`** (v0.3.0) | Per-project OKR derivation, per-report scoring, quarter roll-up. CEO invokes on every report. |
| **`adr`** (v0.3.0) | Decision receipts (`_decisions/ADR-NNNN-*.md`). CEO invokes on every material decision trigger. |
| **`meeting-minutes`** (v0.3.0) | Durable minutes for user / board / blocking-council / red-team / audit / retro convenings. |
| **`idea-pipeline`** (v0.3.0 Wave 2) | 4-stage portfolio ideation: raw → screened → ranked → top-5. CEO invokes on "what next" / quarter / REM / empty-backlog. |
| **`user-meeting`** (v0.3.0 Wave 2) | 4-phase CEO ↔ user selection flow (brief → present → capture → commit). Only structured convening with user. |
| **`market-intel`** (v0.3.0 Wave 2) | Canonical shapes for market artifacts. Parsed by section header; readers fail-fast on schema drift. |
| **`positioning`** (v0.3.0 Wave 2) | Messaging canvas + narrative-score rubric. Consumed by opportunity-ranker, top-5 one-pager, comms-writer. |
| **`roster`** (v0.3.0 Wave 3) | Living agent registry + hire/fire/tier-change/repurpose lifecycle. COO-owned. Every mutation files an ADR. |
| **`audit`** (v0.3.0 Wave 3) | Independent paper-trail integrity — close-audit (every ship) + portfolio-audit (per quarter) + incident / pre-release audits. |
| **`capacity`** (v0.3.0 Wave 3) | Per-agent + per-council utilization bands + KR coverage gaps. Feeds roster-manager and idea-pipeline pre-flight. |
| **`ladder`** (v0.3.0 Wave 4) | 8-rung never-give-up resilience ladder. Fix-loop = Rung 1; every rung transition files an ADR; Rung 7 parking lot preserves artifacts for later revival. |
| **`eval`** (v0.3.0 Wave 5) | Close-eval + portfolio regression + benchmark-sweep + compaction. Derives eval items from PKRs (never from shipped artifacts). 5 pp regression threshold. Regression baseline freezes per quarter. |
| **`budget`** (v0.3.0 Wave 5) | Per-project token + $ budget with per-phase allocation, burn tracking on every Chief report, and Rung 6 escalation on cumulative > 110 %. 4 size classes (small / medium / large / custom). |
| **`red-team`** (v0.3.0 Wave 6) | Adversarial testing on every close + prompt-upgrade + integration + quarterly portfolio sweep. OWASP ASI Top 10 mapping; severity → gate → ladder Rung 3. CRT never on delivery path. |
| **`playbook`** (v0.3.0 Wave 6) | DGM-style stepping-stone archive. Immutable stones derived from remediated `high`+ red-team findings. Prompt-diff review runs against archive before `agents/*.md` edits land. |
| **`tool-scout`** (v0.3.0 Wave 7) | Scouts new MCPs, skills, or third-party tools before adoption. CEO invokes on any add-a-tool request. |
| **`a2a`** (v0.3.0 Wave 7) | Agent-to-agent adapter builder. Default-deny allowlists; wildcard allowlists are an automatic critical finding. |
| **`sandbox`** (v0.3.0 Wave 7) | Run untrusted input in an isolated environment. "Just this once" is an ASI-class finding — use the sandbox. |
| **`model-routing`** (v0.3.0 Wave 7) | Model-vendor outage routing. Same-tier lateral moves only; opening + closing ADRs on every override. |
| **`sbom-slsa`** (v0.3.0 Wave 7) | CycloneDX SBOM + SLSA provenance on every published artifact. No exceptions. |
| **`secrets-vault`** (v0.3.0 Wave 7) | Vault refs only — never raw secrets. Weekly + every-close scans. 30-day rotation default. |
| **`ip-lineage`** (v0.3.0 Wave 7) | IP-lineage statement on every close; creative outputs pass perceptual-hash similarity ≥ 85 %. |
| **`compliance-drift`** (v0.3.0 Wave 7) | Monthly + on-demand sweeps. Drift (yellow) vs breach (red) — suppressed drift converts to breach on auditor schedule. |
| **`fanout`** (v0.3.7) | Chief → Specialist → Worker worker-tier convention. 3-level depth cap; parallelism caps 8/specialist, 24/council, 64/agency. |
| **`retrospective`** (v0.3.8) | Post-close / wave / incident / portfolio retro. Feeds `LESSONS.md` via `lessons-ledger`. |
| **`lessons-ledger`** (v0.3.8) | Append-only cross-project learning log `LESSONS.md`. CEO invokes on every close after retrospective. |
| **`keeper-test`** (v0.3.8) | Quarterly + on-demand fire-readily review. Cites `KEEPER-TEST.md`. User has final vote on fires. |
| **`rhythm`** (v0.3.9) | Daily / weekly / monthly / quarterly heartbeat orchestrator. Reads `_vision/rhythm/state.json`; writes `heartbeat-<date>.md` / `weekly-<YYYY-WW>.md` / `monthly-<YYYY-MM>.md` / `quarterly-<YYYY-Q>.md`. Missed heartbeats escalate via `compliance-drift` → Rung 2 → Rung 3. |
| **`career-ladder`** (v0.3.9) | Per-agent L1 (trial) → L2 (steady) → L3 (principal) within-tier level engine. Quarterly sub-step of `rhythm` + ad-hoc on stepping-stone / mentor events. Inter-tier mobility is USER-ONLY. Reserved names (CEO + 16 Chiefs + `skill-creator`) always L3. |
| **`waivers`** (v0.4.0) | Formal time-boxed waiver flow for clearing a blocking-council red without fixing the underlying finding. Proposer = council lead; reviewer = blocking chief + CEO; approver = user-only. Every waiver has a calendar expiration ≤ 90 days; paired `waiver-expiry` ADR files on expiry day. One-finding-one-artifact-one-project scope. ASI-class + raw-secret findings are not waivable. |
| **`drill`** (v0.4.0) | Scheduled + on-demand resilience drills across 5 drill kinds (chief-unavailable, heartbeat-miss, model-outage, waiver-expiry, compaction-loss) on 4 cadences (monthly, quarterly, annual, on-demand). Every drill files a `drill-report` ADR with outcome (pass / pass-with-gaps / fail) + gaps + remediation. Missed drills are CAO reds. Drills never run during a live incident affecting the same subsystem. |
