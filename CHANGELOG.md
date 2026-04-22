# CHANGELOG

Wave-by-wave history of DevSecOps-Agency. Newest at the top. See `AGENTS.md` for the currently authoritative conventions and `README.md` for the user-facing overview.

## v0.3.9 — Rhythm+Career (2026-04-22)

Third of four staggered waves. Adds the rhythm layer (4-cadence heartbeat) and the career layer (within-tier L1/L2/L3 ladder). Skill-layer and root-doc-layer only — no new agents, no new councils, no new tool grants. Safe upgrade from v0.3.8.

- **`RHYTHM.md`** (new root doc). "The paper trail has a pulse, and the CEO reads it at session start." Declares 4 heartbeat cadences with owners, triggers, inputs, outputs, pass criteria, and failure modes: **daily** (CEO → `_vision/rhythm/heartbeat-<date>.md`: inbox sweep + open-project pulse + yesterday's ADR+session-log scan + today's backlog + rhythm-state check), **weekly** (CEO+COO → `weekly-<YYYY-WW>.md`: Monday morning; board-phase flow, council utilization, rung traversal, fix-loop rate, compliance-drift yellows, LESSONS row since-last-weekly), **monthly** (CAO+CPO → `monthly-<YYYY-MM>.md`: first business day; close-audit roll-up, portfolio OKR movement, non-goal violations, append-only integrity spot-check, model-tier/budget/FinOps roll-up), **quarterly** (COO+CEVO+user → `quarterly-<YYYY-Q>.md`: invokes keeper-test → career-ladder → eval baseline freeze → mission alignment → lessons mining; convened as user-meeting). State schema in `_vision/rhythm/state.json` with `lastDaily`, `lastWeekly`, `lastMonthly`, `lastQuarterly`, and `degradedCount` per cadence. Bootstrap: null state → run daily + any cadence whose natural trigger already passed.
- **`CAREER.md`** (new root doc). Declares within-tier **L1 (trial) → L2 (steady) → L3 (principal)** ladder. Tier vs. level distinction made explicit — tier is USER-ONLY (`VALUES.md §10`), level is per-quarter mechanical. Promotion gates: **L1→L2** needs 2 consecutive Keeper-Test greens + ≥ 10 reports + zero `roster-upgrade` ADRs; **L2→L3** needs 4 consecutive greens + ≥ 3 stepping-stones as primary author + ≥ 1 mentor upgrade + zero high+ red-team findings. Demotion: **L3→L2** on any Keeper-Test red OR any high+ finding attributable to L3-led work; **L3→L1** is forbidden — repurpose via keeper-test instead. Reserved names (CEO + 16 Chiefs + `skill-creator` = 17 agent files) are always L3 and are not processed. Privilege matrix: L3-only privileges = primary-author on `roster-upgrade` ADR for another agent, mentor assignment for newly-hired agents, first-vote on prompt-diff review, single-sign-off on close-out gate within own council. Bootstrap: all non-reserved agents start at L1 on v0.3.9 install.
- **`skills/rhythm/`** (new skill, v0.1.0). Heartbeat orchestrator. Triggers: session start (mandatory), schedule-driven (daily via CEO step 3), explicit `/devsecops-agency:rhythm`. 8-step process (read state → compute due set → sort daily→weekly→monthly→quarterly → run each → update state → escalate on repeated degrade → bootstrap → return). Composes with keeper-test + career-ladder on quarterly. `references/cadences.md` gives per-cadence input-read + output-write contracts with file-format templates. `references/missed-heartbeat.md` defines escalation tree: 1st miss = yellow compliance-drift (no ADR), 2nd miss = ADR + Rung 2, 3rd miss = Rung 3 (quarterly blocks new projects), 4th+ = Rung 4+ with per-turn user notification. Catch-up mode (daily/weekly) writes the backfill heartbeat with `mode: catch-up`; skip-forward mode (monthly/quarterly) writes a single `mode: skip-forward` note citing the gap.
- **`skills/career-ladder/`** (new skill, v0.1.0). Per-agent level engine. Triggers: quarterly sub-step of `rhythm`, ad-hoc on stepping-stone that survives supersession, ad-hoc on primary-author of `roster-upgrade` for another agent, manual by COO on mid-quarter L3 red. 9-step process (verify keeper-test preconditions → load prior levels → compute each non-reserved agent → apply promotion gates → apply demotion gates → emit diffs → write `_vision/roster/levels-<date>.md` + per-change ADRs → bootstrap branch → notify). Interaction matrix with keeper-test covers all 9 rating×level combinations. `references/levels.md` gives exact gate thresholds with file-path evidence for audit. `references/privileges.md` gives the L1/L2/L3 privilege matrix. ADR `kind`s: `career-promotion` / `career-demotion` / `career-bootstrap` / `career-noop-<YYYY-Q>` (files once per quarter even when nothing moved to prove the skill ran).
- **CEO playbook extended.** `skills/ceo/SKILL.md` bumped to v0.3.9. New `## Rhythm + Career (v0.3.9)` section after Identity+Learning. `### 0. Session start` gains a new step 3 "Run the rhythm heartbeat" invoking `skills/rhythm` (which cascades through any due cadence); previous step 3 → step 4, previous step 4 → step 5. Progressive-disclosure bullet added for the two new skills + two new root docs.
- **Root `AGENTS.md` extended.** New `## Rhythm + Career (v0.3.9)` section (4 bullets). Eleven new anti-patterns: don't skip a heartbeat because "nothing changed" · don't backdate a heartbeat file · don't merge cadences · don't run quarterly without keeper-test → career-ladder ordering · don't promote across tiers via career-ladder (USER-ONLY) · don't skip demotion on a red L3 on an "important project" · don't let a single stepping-stone count for multiple agents' L3 gates · don't carry L3 privileges across a demotion · don't edit a landed `levels-<date>.md` · don't backdate a promotion to recognize pre-v0.3.9 work · don't run career-ladder on reserved names.
- **`skills/AGENTS.md` index refresh.** Header bumped v0.3.8 → v0.3.9. Added 2 new rows for `rhythm` and `career-ladder` with cadence + scope summary.
- **README.md identity block extended.** Two new bullets in the `## Identity` section linking `RHYTHM.md` and `CAREER.md`. Version pointers updated 0.3.8 → 0.3.9.

## v0.3.8 — Identity+Learning (2026-04-22)

Second of four staggered waves. Adds the identity layer (MISSION / VALUES / KEEPER-TEST) and the learning layer (append-only LESSONS ledger + post-close retrospective). Skill-layer and root-doc-layer only — no new agents, no new councils, no new tool grants. Safe upgrade from v0.3.7.

- **`MISSION.md`** (new root doc). "Ship software that is secure, receipted, and reversible." One-sentence tagline ("One user voice, sixteen chiefs, one paper trail."), primary / secondary / never-users, 7 non-goals (not a chatbot / not a consensus machine / not no-code / not compliance theatre / not a speed demon / not self-modifying at runtime / not a market research firm), 5 North Stars (receipts ratio = 100 %, blocking-council green on ship, SBOM+SLSA on every artifact, Rung-7 preservation, ≥ 1 LESSONS row per close).
- **`VALUES.md`** (new root doc). 11 operating principles: 1. Receipts over opinions · 2. Security and legal blocking · 3. Audit / Eval / Red-team / SRE independence · 4. Append-only hard invariant · 5. Never give up below Rung 7 · 6. Deterministic ordering for prompt cache · 7. Vault refs only · 8. Default-deny on external adoption · 9. SBOM+SLSA on every artifact · 10. Prompt-diff review on every persona edit · 11. Learn in writing not in memory. Each value carries a "Fails this value" anti-pattern list. Enforced via CEO session-start read, COO Keeper-Test citations, CAO close-audit scoring, CRT prompt-diff review.
- **`KEEPER-TEST.md`** (new root doc). Netflix-inspired quarterly fire-readily review. Core question: "If this agent walked in tomorrow claiming a similar role from a peer agency, knowing what we now know about their 90-day performance, would we hire them at the same tier?" Who runs it: `performance-reviewer` (score) → `hiring-lead` (propose) → COO (convene) → CEO (review) → **user (final vote on fires)**. Cadence: quarterly mandatory, per-project on CAO finding, automatic on 3 consecutive prompt-diff bouncebacks. Four scoring axes (gate hit rate / fix-loop rate / audit findings / values compliance). Reserved names excluded (16 chiefs + skill-creator).
- **`LESSONS.md`** (new root doc, starts empty). Append-only cross-project learning ledger. One row per close. 11-field row schema: outcome / council-lead / ship / OKR alignment / rungs traversed / fix-loops / waivers / stones authored / lessons (≤ 3 cited bullets) / reusable decisions (≤ 2 ADR citations) / what we'd change / next-run trigger. Readers: `idea-pipeline`, `memory`, `retrospective`, `ceo`, `cao`.
- **`skills/retrospective/`** (new skill, v0.1.0). Four kinds — project-close / portfolio / incident / wave. 10-section output format (Header / Context / Timeline / Worked / Gated / Loops & rungs / Lessons / Reusable decisions / What we'd change / Carry-over check / Follow-ups). Jaccard-similarity carry-over check against LESSONS.md with thresholds ≥ 0.80 (hard carry-over → ADR + CAO red) and 0.50–0.79 (weak-positive, portfolio-audit flag). Graceful-degrades: skips carry-over check until LESSONS has ≥ 3 rows.
- **`skills/lessons-ledger/`** (new skill, v0.1.0). Append-only ledger-row writer invoked after every close. 9-step process (verify preconditions → read → compute → collision check → Write → sort → ADR `kind: lessons-append` → update `_memory/index.json` → return). Correction-row rules (slug unchanged, `closedAt > original`, outcome gets `-corrected` suffix, `lessons[0]` starts with `[correction]`). Not idempotent by design — every append is a new truth.
- **`skills/keeper-test/`** (new skill, v0.1.0). Wrapper around `performance-reviewer` + `roster` + `hiring-lead`. Four scoring axes with exact thresholds. Action tree: Keep (no-op + annotate) / Upgrade (prompt edit via `roster` + `red-team` prompt-diff + ADR, two-strike rule) / Repurpose (move council + ADR + 30-day probation, no tier change) / **Fire (USER ONLY)** via `inbox.json` → user-meeting → archive to `_vision/roster/_archive/` with redirect header + ADR `kind: roster-fire`. Bootstrap rules for Quarter 0 (skip review, file bootstrap ADR) and Quarter 1 (Axis 3 + 4 only, `preliminary-*` ratings).
- **CEO playbook extended.** `skills/ceo/SKILL.md` bumped to v0.3.8. New `## Identity + Learning (v0.3.8)` section. New `### 0. Session start` playbook step: read MISSION, read VALUES, read the latest 5 LESSONS rows, check active project against non-goals, open session log. Close-out playbook renumbered 1–9 → 1–10 with step 4 "Run the retrospective" (attendees ceo/cao/cevo/crt, preconditions CAO+CEVO+CRT all landed) and step 5 "Append the lessons-ledger row" (cites MISSION North Stars §5). Final summary now carries a one-line ledger anchor.
- **Root `AGENTS.md` extended.** New `## Identity + Learning (v0.3.8)` section (5 bullets). Ten new anti-patterns: don't start CEO session without reading MISSION+VALUES · don't accept a non-goal without user-meeting + ADR · don't skip the lessons-ledger append at close · don't edit a prior LESSONS row (correction-row only) · don't fire without user approval · don't `git rm` a fired agent (archive, with redirect header) · don't run Keeper Test on reserved names · don't write the retro before CAO+CEVO+CRT land · don't skip the retrospective carry-over check · don't hand-edit `VALUES.md` mid-project (quarterly-only).
- **`skills/AGENTS.md` index refresh.** Header bumped from "v0.3.0-alpha.6" to "v0.3.8". Back-filled 9 missing rows (all 8 Wave 7 skills + v0.3.7 `fanout`) + 3 new v0.3.8 rows (`retrospective`, `lessons-ledger`, `keeper-test`).
- **README.md identity block.** New top-of-README "## Identity" section linking MISSION / VALUES / KEEPER-TEST / LESSONS before the Install section. Version pointers updated 0.3.7 → 0.3.8.

## v0.3.7 — Clarity (2026-04-22)

Pure restructure. No new capabilities. Foundation wave for the Identity / Learning / Rhythm / Career / Governance / Resilience work that follows in v0.3.8 → v0.4.0.

- **Council directory restructure.** 91 agent persona files moved from the flat `agents/` tree into 16 per-council subfolders under `agents/<council>/<agent>.md`. `agents/ceo.md` remains at repo root as the single user-facing agent. `git mv` preserved blame.
- **Role Card v1 on every agent.** All 92 agent files now carry an 8-field role card (Council / Role / Reports to / Team / Model tier / Purpose / Convened by / Must not) immediately after the frontmatter, guarded by `<!-- role-card:v1 -->` for idempotent regeneration. Purpose is derived deterministically from the first sentence of `description:` with `<example>` blocks stripped.
- **Per-council TEAM.md.** 16 new roster cards at `councils/<council>/TEAM.md` — Remit, Convened-when, Lead, Specialists table (Agent / Tier / Purpose), Worker-tier section with the frontmatter YAML template, and a pointer back to the council's `AGENTS.md` contract. AGENTS.md = contract (must / must-not), TEAM.md = roster (who currently staffs it).
- **Worker tier scaffold.** New `skills/fanout/SKILL.md` declares the Chief → Specialist → Worker convention: 3-level depth cap (deeper requires a council-lead ADR), legal split dimensions (per-file, per-endpoint, per-dep, per-table, per-agent-file, per-preprint, per-probe), parallelism caps (8 / specialist, 24 / council, 64 / agency-wide), aggregation contracts (union | majority | worst-of | tally), isolation under `_workers/<specialist>/<shard>.md`, and its relationship to `skills/taskflow/` (workers carry `parent_task_id`). Paired `references/worker-frontmatter-template.md` gives the YAML template, sizing rules, envelope pattern.
- **README.md rewrite.** 201 lines → 143 lines. Sections: Install, How the agency is organised (16-council table, org chart), Worker tier, Slash commands, The 7 phases, Repo layout, Output, Security posture, Learn more. "Workers do not spawn workers by default" stated explicitly.
- **AGENTS.md rewrite.** 288 lines → 170 lines. Wave-accumulation history moved out to this CHANGELOG. New `## Workers (fanout)` section. Council count updated 9 → 16. Paths updated to `agents/<council>/<agent>.md`. Scoped-rules + read-before-write extended to include TEAM.md. Anti-patterns extended with four worker-specific rules: don't declare workers for non-independent dimensions, don't spawn workers from a council lead, don't exceed 3-level depth without an ADR, don't merge worker shards without declared aggregation semantics.
- **No new agents, no new runtime behaviour, no new tool grants.** Safe upgrade from v0.3.6.

## v0.3.6 — Messaging dialects + container isolation posture (MIT imports)

Audited imports from `qwibitai/nanoclaw` v1.2.53 (MIT, © 2026 Gavriel). Zero new injection surface, zero new specialists. Two new skills + one reference doc:

- `skills/messaging-formatting/` — dialect router for Slack mrkdwn vs. Discord vs. Microsoft Teams vs. email vs. CommonMark. Detection rules + construct-by-construct delta tables + length limits + composition pattern. Replaces the paste-CommonMark-into-Slack failure mode. Derived from nanoclaw's container-skill `slack-formatting` and substantially rewritten / extended for four surfaces.
- `skills/container-isolation-posture/` — design-guidance skill. Nine-rule checklist codifying the sandbox posture: container-is-primary-boundary, external allowlist outside the sandbox, fail-closed config loaders, block-by-default sensitive patterns, symlink resolution before policy check, container-path validation (no-absolute / no-dot-dot / no-colon), read-only project root with writable paths listed, per-tenant session isolation, credentials never enter the sandbox. Distilled from `docs/SECURITY.md` + `src/mount-security.ts` with NO TypeScript source ported — design guidance only.
- `skills/webapp-testing/references/agent-browser-patterns.md` — pattern reference distilled from nanoclaw's `container/skills/agent-browser`: reconnaissance-then-action workflow, five semantic-locator axes (role / text / label / placeholder / testid), wait primitives, authenticated-state pattern, six anti-patterns. Mapped to Playwright + Claude-in-Chrome MCP equivalents. Binary itself NOT a dependency.

Audit findings: nanoclaw's `sender-allowlist.ts` defaults to fail-OPEN (`allow: '*', mode: 'trigger'`) on missing config — documented as a tradeoff note in container-isolation-posture rule 3. Dockerfile uses unpinned `npm install -g` — flagged in the nine-rule checklist. Everything else in the TypeScript source (container-runner, ipc, router, scheduler, channels, db, sessions) is host-daemon infrastructure with no home in a plugin and deliberately NOT ported.

License handling: MIT requires preserving copyright + permission text. Full nanoclaw MIT notice and per-file provenance note at `LICENSES/MIT-nanoclaw.txt`; per-skill `LICENSE.txt` markers in each of the two new skill directories.

## v0.3.5 — MCP authoring + skill evaluation + webapp testing (Apache-2.0 imports)

Audited imports from the official `anthropics/skills` repo (Apache 2.0), zero new injection surface. Three new skills:

- `skills/mcp-authoring/` — producer side. Four-phase Plan → Implement → Review → Evaluate process for building MCP servers. TypeScript / Python SDK guidance. 10-question XML eval suite required for release. Pairs with v0.3.4's `skills/mcp-defense/` (consumer side) for end-to-end MCP lifecycle competence.
- `skills/webapp-testing/` — Playwright-based local webapp testing with multi-server lifecycle management. **HARDENED for the agency**: upstream `scripts/with_server.py` rewritten to use `shell=False` + `shlex.split` + per-server `--cwd` flag instead of `shell=True` + `cd backend && …`, preserving the injection-resistant posture. Modifications marked per Apache 2.0 §4(b).
- `skills/skill-eval/` — evaluation harness for any SKILL.md. Single-run eval, multi-trial benchmark with variance analysis (σ/μ ≤ 0.15 gate), description-tuning optimization loop for trigger precision, description-only improver, HTML review viewer. Does NOT replace the existing `skill-creator` — authoring vs. judging split.

Two new specialists:

- `mcp-author` (Execution Council, reports to CTO via engineering-lead) — runs the four-phase MCP authoring process, pairs with `mcp-defender` on the consumer side, blocks release on < 8/10 eval pass-rate.
- `skill-evaluator` (Evaluation Council, reports to evaluation-lead / CEVO) — runs `quick_validate` → benchmark with n=10 trials → pass-rate ≥ 0.80 floor + σ/μ ≤ 0.15 variance gate. Owns the minor-version sweep re-evaluating every skill at each bump.

Each import audited for prompt injection (clean SKILL.md text, no jailbreak / Parseltongue / GODMODE patterns) and dangerous patterns (`shell=True` in webapp-testing was the only finding — hardened before import). Source-available skills from upstream (docx, pdf, pptx, xlsx) were deliberately NOT imported — Anthropic's license blocks redistribution.

## v0.3.4 — Injection-resistant hardening + 2026 landscape alignment

Eight new agency-authored skills (zero upstream imports = zero new injection surface):

- `skills/mcp-defense/` — 6-class MCP threat taxonomy (tool poisoning, rug-pull, manifest pre-execution, indirect-injection-via-tool-output, over-permission, response-path exfil) + pinned-hash registration + `<tool-description-data>` + `<tool-output-data>` envelopes + quarterly sweep.
- `skills/observability/` — OpenTelemetry GenAI semantic-conventions instrumentation. Trace-id propagation, per-span `gen_ai.*` attributes, prompts / completions as events (not attributes), DLP pre-filter on events, tail-based sampling (100% errors / 10% success).
- `skills/prompt-cache/` — post-Feb-2026 Anthropic cache tuning. Canonical 4-breakpoint assembly, default 5-min TTL with paid 1-hour opt-in only for > 6 dispatches per window, workspace-level isolation awareness, ≥ 60% hit-rate target.
- `skills/dlp/` — outbound Data Loss Prevention. 5-channel scan (args + URL + query + headers + body), chain-of-tool correlation (20 calls / 5 min for split-secret detection), static-first-NLP-second, block-is-default (waiver requires ADR).
- `skills/injection-defense/` — 4-layer PromptGuard framework:
  - Layer 1: input gatekeeping (regex + structural-marker scan + zero-width-unicode strip + homoglyph + optional MiniBERT classifier)
  - Layer 2: `<untrusted-data>` envelope with explicit data-not-instruction framing
  - Layer 3: semantic output validation (instruction-density + tool-call-shape + persona-adherence checks)
  - Layer 4: adaptive refinement
  10-class 2026 attack taxonomy. Rebuff explicitly NOT used — archived May 2025.
- `skills/finops/` — cost attribution. 4-column token tracking (prompt / tool / memory / response) × 3-dimension attribution (project / council / agent-phase), weekly report, anomaly thresholds (span > $1, trace > $10), quarterly roll-up feeding CAO portfolio audit. "Cache-creation pays, not cache-reader" invariant.
- `skills/chaos/` — 14-fault agent-specific chaos library (model-unavailable / slow, partial-response, tool-error-transient / permanent, tool-output-malformed / injected, tool-args-mutated-in-flight, rate-limit-burst, context-overflow, memory-corrupt, clock-skew, audit-log-write-fail, vault-unavailable). Sandbox-only. Canonical 12-fault pre-release suite with green / yellow / red gate.
- `skills/self-critique/` — pre-return constitutional check. Every agent samples 3 of 15 principles from a frozen-at-dispatch-start hash-indexed set and revises if any fail. Separate-completion critique to prevent draft contamination. Max 2 revisions then escalate. Runtime-hook-enforced; cannot be disabled by the agent.

Six new specialists across existing councils: `agent-telemetry-engineer` (SRE, distinct from `observability-engineer` which does app-level health endpoints), `prompt-cache-tuner` (SRE), `dlp-scanner` (Security), `finops-analyst` (Evaluation), `chaos-engineer` (Red-Team), `mcp-defender` (Security). All authored in-agency to keep the injection surface zero.

## v0.3.3 — OSS forensics + arXiv + agent-governance-reviewer

Three audited imports:

- `skills/oss-forensics/` — supply-chain investigation, deleted-commit recovery, force-push detection, IOC extraction, multi-source evidence collection. Inspired by RAPTOR's 1800+ line OSS Forensics system, ported from Nous `hermes-agent` MIT after prompt-injection audit.
- `skills/arxiv/` — search + retrieve academic papers via the free arXiv REST API, no key required. Consumed by Research Council specialists.
- `agent-governance-reviewer` specialist (Audit Council, reports to CAO) — 10-point meta-governance review checklist: tool-decorator coverage, intent classification on input paths, hardcoded-credential scan, append-only audit trail, rate-limit ceilings, multi-agent trust boundaries, most-restrictive-wins policy composition, fail-closed defaults, allowlist-over-blocklist, HITL on high-impact ops.

Frontmatter of the imported agent reformatted to agency convention (kebab-case name, sonnet tier, minimum-tools grant, read-only, never edits code under review). Excluded on this pass: hermes-agent godmode (Parseltongue + GODMODE), sherlock-doxxing, 1password-cred-handling.

## v0.3.2 — SDLC patterns pack (MIT imports)

`skills/sdlc-patterns/` — six operational SDLC skills ported from Nous Research's `hermes-agent` (MIT) after a prompt-injection audit: `plan`, `writing-plans`, `systematic-debugging`, `test-driven-development`, `requesting-code-review`, `subagent-driven-development`. Specialist-invoked deep references, not user entry points. User-facing skill surface unchanged.

The hermes-agent `red-teaming/godmode` skill was deliberately excluded: Parseltongue encoding, GODMODE jailbreak templates, `exec(open(...))` dynamic loading, `auto_jailbreak()` config writer — explicit prompt-injection toolkit.

## v0.3.1 — Runtime hooks patch

`runtime-hooks/` — five drop-in shell hooks ported from github/awesome-copilot after a prompt-injection audit: `secrets-scanner`, `tool-guardian`, `governance-audit`, `dependency-license-checker`, `session-logger`. Plus a locked-down `commit-gate.sh` replacement for the upstream auto-commit hook — the upstream `session-auto-commit` was excluded because it uses `git add -A` + `--no-verify` + auto-push, bypassing the very defenses it ships alongside.

Hooks are read-only regex defenders: no eval, no shell-exec of untrusted input, no network fetch, no remote pattern loading. They complement the prompt-level rules in each council's AGENTS.md with runtime enforcement.

## v0.3.0 — Company release (Waves 1–7)

The "company" release. The user speaks only to the CEO; the CEO holds board meetings with Chiefs, each of whom runs a council of specialists. Research → Product → Architecture → Security → Execution → Quality → DevOps → Docs → Legal → Marketing → Strategy → People-ops → Audit → Evaluation → Red-Team → SRE. Security-first (STRIDE + OWASP Top 10) by default; adversarial-defense-first (OWASP ASI Top 10 2025) via the Red-Team Council. 16 Chiefs + ~64 specialists at cut.

### Wave 1 — Foundations (v0.3.0-alpha.1)

Durable corporate paper trail:

- `skills/vision-doc/` — workspace VISION.md + 3-bullet KR slice per dispatch.
- `skills/okr/` — per-project OKR derivation + per-report alignment + quarter roll-up.
- `skills/adr/` — immutable decision receipts.
- `skills/meeting-minutes/` — minutes for every user / board / blocking-council / red-team / audit / retro convening.

### Wave 2 — Marketing + Strategy (v0.3.0-alpha.2)

CMO + CSO councils + 8 specialists. Four new skills:

- `skills/idea-pipeline/` — 4-stage gated ideation → top-5.
- `skills/user-meeting/` — 4-phase CEO ↔ user selection flow with live Cowork artifact.
- `skills/market-intel/` — canonical artifact shapes.
- `skills/positioning/` — messaging canvas + narrative rubric.

### Wave 3 — People-ops + Audit (v0.3.0-alpha.3)

COO + CAO councils + 7 specialists (`roster-manager`, `hiring-lead`, `performance-reviewer`, `adr-auditor`, `gate-auditor`, `okr-auditor`, `memory-auditor`). Three new skills:

- `skills/roster/` — living agent registry + hire / fire / tier-change / repurpose lifecycle with mandatory ADRs and `_vision/roster/_archive/`.
- `skills/audit/` — independent close + portfolio paper-trail integrity, 4 audit kinds, every red → ADR.
- `skills/capacity/` — per-agent + per-council utilization bands + KR coverage gaps.

### Wave 4 — Resilience ladder (v0.3.0-alpha.4)

`skills/ladder/` — never-give-up escalation with 8 rungs (0 Retry → 1 Fix-loop → 2 Alternate approach → 3 Cross-council → 4 Hire / repurpose via COO → 5 Scope pivot → 6 User consult → 7 Parking lot). Per-rung attempt budgets. ADR per transition. Rung 7 is a resumable terminal state that preserves every artifact with a reconsider-trigger. Taskflow extended with `ladderRung` field; gate reds start the ladder instead of durably blocking.

### Wave 5 — Evaluation Council (v0.3.0-alpha.5)

CEVO + 5 specialists (`eval-designer`, `benchmark-runner`, `regression-detector`, `budget-monitor`, `token-compactor`). Two new skills:

- `skills/eval/` — mandatory close-eval paired with close-audit. Portfolio-regression with 5 pp threshold + quarter-frozen baselines. Benchmark-sweep across SWE-bench-lite / MLE-bench-lite / per-project harnesses. Eval items derived from PKRs — never retrofitted.
- `skills/budget/` — four size classes (small 75k / $1.50, medium 250k / $5, large 1M / $20, custom). Per-phase allocation, per-report burn tracking. Cumulative > 110% triggers Rung 6.

Token-compactor performs structured rewrites (rollup + correction pointer, never delete). Never-compact list covers decisions, errors, reports, ADR-refs, meeting lines, rung transitions.

### Wave 6 — Red-Team Council (v0.3.0-alpha.6)

CRT + 7 specialists (`adversarial-prompter`, `tool-abuse-tester`, `data-exfil-tester`, `model-poisoning-scout`, `supply-chain-attacker`, `social-engineering-tester`, `playbook-author`). Two new skills:

- `skills/red-team/` — OWASP ASI Top 10 2025 mapping. Severity rubric (reproducibility × impact × boundary × mitigation). Severity → gate → ladder routing (default Rung 3). Five kinds: pre-release / prompt-upgrade / integration / portfolio-sweep / incident. CRT never on delivery path.
- `skills/playbook/` — DGM-style stepping-stone archive under `_vision/playbooks/`. Immutable stones authored from remediated high+ red-team findings. Supersession-only evolution. Prompt-diff review blocking gate before `agents/*.md` or `councils/*/AGENTS.md` changes land, with weakening-phrasing auto-reject patterns.

### Wave 7 — SRE Council (v0.3.0 final)

CSRE + 4 specialists (`mcp-registry-scout`, `a2a-adapter`, `sandbox-runner`, `model-routing-override`) + four provenance specialists distributed across existing councils: Security (`sbom-slsa`, `secrets-vault`), Legal (`ip-lineage`, `compliance-drift`). Eight new skills:

- `skills/tool-scout/` — 7-dimension rubric (provenance / scope / abuse-surface / reversibility / secret-handling / maintenance / integration-cost) with auto-red trinity.
- `skills/a2a/` — cross-agency agent-to-agent adapters with default-deny allowlists, rate limits, 30s timeouts, mTLS / JWT identity, and mandatory smoke suites.
- `skills/sandbox/` — ephemeral `/tmp/sandbox-<nonce>/` with 2 CPU / 2 GB / 60s / network default-deny caps. Diff-not-state.
- `skills/model-routing/` — same-tier lateral fallback matrix. Opus: claude-opus-4.6 / 4.5 / gpt-5-thinking. Sonnet: claude-sonnet-4.6 / 4.5 / gpt-5 / gemini-2.5-pro. Haiku: claude-haiku-4.5 / 4 / gpt-5-mini / gemini-2.5-flash. Downgrades forbidden. Every override = opening + closing ADR + session-log tag.
- `skills/sbom-slsa/` — CycloneDX JSON + SLSA provenance on every shipped artifact. Keyless sigstore. Level reported, not claimed.
- `skills/secrets-vault/` — agents receive vault refs (`_vault:<project>-<tool>`), never raw creds. 30d rotation default (7d high-privilege). Rotation = overlap + verify. Weekly + every-close gitleaks / trufflehog scans.
- `skills/ip-lineage/` — lineage tree + license reconciliation + perceptual-hash similarity (≥ 85% red, 70–85% yellow). User contributions always credited.
- `skills/compliance-drift/` — monthly + on-demand SOC 2 / GDPR / HIPAA / state-privacy sweeps. Version-pinned rubrics. Drift yellow ≠ breach red.

CSRE council is independent — never on any project's delivery path (same invariant as Audit + Eval + Red-Team).

## v0.2.5 — Runtime roster, model tiering, rate-limited notify, novelty-gated memory

`skills/skill-creator/` runtime roster extension. Per-agent model tiering (Opus CEO / Sonnet Chiefs / Haiku specialists). Rate-limited notify. Novelty-gated memory writes.

## v0.2.4 — Worktree parallelism

`skills/worktree/` — atomic, scope-checked merge for parallel implementation and fix-loop work.

## v0.2.3 — Gates + taskflow

`skills/gates/` — green / yellow / red / n/a with blocking-vs-informing councils. `skills/taskflow/` — six-state machine with 2-attempt fix-loop cap.

## v0.2.2 — Scoped AGENTS.md hierarchy

Scoped `AGENTS.md` hierarchy with deterministic ordering for prompt-cache stability.

## v0.2.1 — Durable memory + session logs

Three-tier Light / Deep / REM dreaming cross-project memory under `_memory/`. Append-only JSONL session logs under `_sessions/`.

## v0.2.0 — Initial release

CEO orchestration, 9 councils, STRIDE + OWASP Top 10 baseline.
