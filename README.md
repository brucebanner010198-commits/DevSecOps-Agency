# DevSecOps Agency

A plugin that turns Claude into a fully autonomous AI software-development company. You hand the **CEO** a one-sentence idea; the CEO convenes a board of 16 Chiefs; each Chief runs a council of specialists. Research, Product, Architecture, Security, Execution, Quality, DevOps, Docs, Legal, Marketing, Strategy, People-ops, Audit, Evaluation, Red-Team, SRE. Security-first (STRIDE + OWASP Top 10 for app code; OWASP ASI Top 10 2025 for agent runtime). Ships to GitHub with SBOM + SLSA provenance.

You speak only to the CEO. Everything else is internal.

A live **command center** artifact shows the org chart, every board and council meeting, every handoff, every artifact, and any blocker parked for you.

Durable **memory** (v0.2.1) means the agency learns across projects: the CEO reads prior learnings before intake, rolls up bullets after every phase (*Light dreaming*), consolidates each project on close (*Deep dreaming*), and extracts cross-project patterns on retro (*REM dreaming*). Per-agent **session logs** are append-only JSONL files queryable with `rg` + `jq`.

**Scoped rules** (v0.2.2): every subtree carries an `AGENTS.md` with telegraph-style imperatives that agents read before touching that area. Root, `agents/`, `skills/`, and each of the 9 councils have their own file. Before every Chief dispatch, the CEO quotes the matching `councils/<council>/AGENTS.md` into the Chief's context — Must, Must not, Gate heuristic. Combined with a deterministic-ordering rule for prompt-cache hits, this is the strongest hallucination dampener in the plugin.

**Gates + taskflow** (v0.2.3): two internal skills formalise what used to live in prose. `gates` defines the exact meaning of green/yellow/red/n/a, which councils block ship (security, legal), how to aggregate gates across councils and phases, and when a waiver needs user consent. `taskflow` defines a six-state machine for every dispatched task (`queued → in-progress → needs-decision → blocked → done/cancelled`), enforces a **hard 2-attempt fix-loop cap** per `(council, phase)` so the agency can't thrash, and encodes handoff invariants the CEO checks before advancing any phase. `status.json` gains a `tasks[]` array and a `gates` object the command-center can render directly.

**Worktree parallelism** (v0.2.4): parallel dispatches (CRO+CPO, CQO+CISO², CKO+GC) and every fix-loop (attempt ≥ 1) now run in isolated `<slug>/_worktrees/<chief>-<attempt>/` scratch directories. Each Chief declares `writes[]` and `reads[]` up front; merges into the main tree are atomic (all-or-nothing), scope-checked (out-of-scope writes bounce), and deterministic (alphabetical order for prompt-cache stability). Fix-loops can diff against the previous attempt's worktree, so `corrections[]` maps to visible changes. Structural conflicts escalate to `inbox.json`; non-structural ones merge with a note.

**Runtime extension, model tiering, push-notify, conditional memory** (v0.2.5): four cross-cutting skills that stop the agency from being brittle on edge cases. `skill-creator` authors new AGENTS.md-compliant agent and skill files in-session when the 9 councils don't cover a domain (crypto, game-dev, mobile, embedded, ML). `model-tiering` pins every agent to **Opus CEO / Sonnet Chiefs (+ skill-creator) / Haiku specialists** with declared upgrade rules; the CEO refuses to dispatch agents with a missing tier. `notify` gives the user one rate-limited push surface (5 per run, then digest) for close-shipped, close-blocked, task-blocked, gate-red, fix-loop-cap, worktree-conflict, and REM-done — hook-wired via Cowork `Stop` / `SubagentStop` where available, with a `[notify]` terminal fallback. `memory` now runs a **Jaccard novelty gate** before every Light/Deep/REM write so repeat projects in the same wedge stop bloating `MEMORY.md` with near-duplicates.

---

## The organisation

```
                                              USER
                                                │
                                                ▼
                                    ┌──────────────────────┐
                                    │         CEO          │  ← only one you talk to
                                    └──────────┬───────────┘
    ┌──────┬──────┬──────┬──────┬──────┬──────┼──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
    ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼
   CRO    CPO    CTO   CISO   VP-Eng  CQO   VP-Ops  CKO    GC    CMO    CSO    COO    CAO   CEVO   CRT   CSRE
   Res.  Prod.  Arch.  Sec.   Exec.  Qual.  DevOps Docs  Legal  Mktg  Strat  P-ops Audit   Eval Red-T  SRE
```

| Council       | Chief (agent)              | Specialists                                                                 |
| ------------- | -------------------------- | --------------------------------------------------------------------------- |
| Research      | `cro`                      | market-researcher, tech-scout, literature-reviewer, user-researcher         |
| Product       | `pm-lead` (CPO)            | spec-writer, product-strategist, roadmap-planner                            |
| Architecture  | `engineering-lead` (CTO)   | system-architect, api-designer, data-architect, infra-architect             |
| Security      | `security-lead` (CISO)     | threat-modeler, code-auditor, pen-tester, compliance-officer, **sbom-slsa**, **secrets-vault** |
| Execution     | `engineering-lead` (VP-Eng)| backend-dev, frontend-dev, db-engineer, integrations-engineer               |
| Quality       | `qa-lead` (CQO)            | test-designer, test-runner, performance-tester, a11y-auditor                |
| DevOps        | `devops-lead` (VP-Ops)     | ci-engineer, deployment-engineer, observability-engineer                    |
| Docs          | `docs-lead` (CKO)          | api-documenter, readme-writer, tutorial-writer                              |
| Legal         | `gc`                       | license-checker, privacy-counsel, **ip-lineage**, **compliance-drift**      |
| Marketing     | `cmo`                      | positioning-strategist, comms-writer, brand-guardian, growth-analyst        |
| Strategy      | `cso`                      | trend-scout, competitive-analyst, market-sizer, opportunity-ranker          |
| People-ops    | `coo`                      | roster-manager, hiring-lead, performance-reviewer                           |
| Audit         | `cao` *(independent)*      | adr-auditor, gate-auditor, okr-auditor, memory-auditor                      |
| Evaluation    | `evaluation-lead` (CEVO) *(independent)* | eval-designer, benchmark-runner, regression-detector, budget-monitor, token-compactor |
| Red-Team      | `red-team-lead` (CRT) *(independent)* | adversarial-prompter, tool-abuse-tester, data-exfil-tester, model-poisoning-scout, supply-chain-attacker, social-engineering-tester, playbook-author |
| SRE           | `sre-lead` (CSRE) *(independent)* | mcp-registry-scout, a2a-adapter, sandbox-runner, model-routing-override |

**1 CEO + 16 Chiefs + ~64 specialists.** Each specialist does one thing well and hands their artifact up to the Chief, who consolidates and reports to the CEO. Audit + Evaluation + Red-Team + SRE are **informing + independent** — never on any project's delivery path.

## Skills (slash commands)

| Command                              | What it does                                                                                  |
| ------------------------------------ | --------------------------------------------------------------------------------------------- |
| `/devsecops-agency:ceo`              | **Main entry point (v0.2)**. Adopts the CEO persona. Convenes the board, runs all 7 phases. |
| `/devsecops-agency:ship-it`          | Lean v0.1 pipeline (6-team hierarchy). Still supported.                                       |
| `/devsecops-agency:command-center`   | Opens (or refreshes) the live status artifact.                                                |
| `/devsecops-agency:board-meeting`    | Re-run a specific board phase (power-user).                                                   |
| `/devsecops-agency:council-meeting`  | Re-run a specific council (power-user).                                                       |
| `/devsecops-agency:intake`           | Run intake Q&A only — produces a project brief without kicking off engineering.               |
| `/devsecops-agency:status`           | Quick text summary of the active project.                                                     |
| `/devsecops-agency:escalate`         | Process the human-input queue: surface parked questions, capture answers, resume pipeline.    |
| `/devsecops-agency:retro`            | Post-deploy retrospective — what went well, what to fix, follow-up tickets. Also triggers REM dreaming if ≥ 3 new pattern files since last run. |
| `memory` (internal skill)            | Read/write durable memory. Invoked by the CEO at init, after each phase (Light), at close (Deep), and on retro (REM). |
| `session-log` (internal skill)       | Append-only per-agent JSONL transcripts across projects. Replay via `rg` + `jq`.              |
| `gates` (internal skill)             | Gate vocabulary + aggregation. Invoked by the CEO after every Chief report; single source of truth for blocking-vs-informing councils and waivers. |
| `taskflow` (internal skill)          | Six-state task machine + 2-attempt fix-loop cap + handoff invariants. Invoked by the CEO on every dispatch and report. |
| `worktree` (internal skill)          | Per-dispatch isolated scratch dirs for parallel and fix-loop work. Atomic scope-checked merge into the main tree. |
| `skill-creator` (internal skill)     | Author new `agents/*.md` + `skills/*/SKILL.md` in-session when the 9 councils don't cover a domain. Invoked by the CEO on roster gap. |
| `model-tiering` (internal skill)     | Per-agent tier assignment — Opus CEO / Sonnet Chiefs / Haiku specialists. Read on every dispatch. |
| `notify` (internal skill)            | Single push-notify surface (close / block / REM / fix-loop cap / worktree conflict). 5-per-run cap + digest fallback. |

## Quick start

```
/devsecops-agency:ceo I want a secure invoice-splitting web app for roommates
```

The CEO will ask 3–5 short questions (tech preference, deployment target, constraints), then run everything autonomously. Open `/devsecops-agency:command-center` at any time to watch.

## The 7 phases

```
Phase 1  Discovery       CRO + CPO           (parallel)
Phase 2  Design          CTO → CISO          (sequential; CISO reviews)
Phase 3  Build           VP-Eng
Phase 4  Verify          CQO + CISO²         (parallel)
Phase 5  Ship            VP-Ops
Phase 6  Document+Legal  CKO + GC            (parallel)
Phase 7  Close           CEO
```

Each phase has an **exit criterion** (see `skills/ceo/references/board-phases.md`). No Critical/High unmitigated risk ever gets past CISO.

## Output

Each project gets its own folder under the Cowork outputs directory:

```
outputs/devsecops-agency/<project-slug>/
├── brief.md                    # CEO's intake + decisions + prior learnings
├── research-brief.md           # CRO output
├── research/                   # market, tech-landscape, prior-art, user-needs
├── product/                    # strategy.md, roadmap.md
├── architecture.md             # CTO output
├── architecture/               # data-model.md, infra.md
├── threat-model.md             # CISO output (STRIDE + OWASP)
├── security/                   # compliance.md, code-audit.md, pentest-report.md
├── src/                        # VP-Eng output — the actual code
├── tests/                      # CQO output
├── qa-report.md, qa/           # test results, perf, a11y
├── deploy/                     # VP-Ops output — CI, container, rollback, observability
├── docs/                       # CKO output — README, API, tutorial
├── legal/                      # GC output — licenses.md, privacy.md
├── status.json                 # Pipeline state (read by the command-center)
├── chat.jsonl                  # Board + council meeting log
├── inbox.json                  # Parked human questions
└── _worktrees/                 # Isolated scratch dirs for parallel + fix-loop dispatches (v0.2.4)
    ├── <chief>-<attempt>/      # worktree.json + the Chief's writes[]
    ├── _merged/                # audit archive of cleanly-merged worktrees
    └── _discarded/             # short-lived archive of superseded attempts
```

Shared across projects (v0.2.1):

```
outputs/devsecops-agency/
├── _memory/
│   ├── MEMORY.md              # durable preferences + cross-project patterns (REM output)
│   ├── memory/YYYY-MM-DD.md   # dated facts (Light dreaming, append-only)
│   ├── patterns/<slug>.md     # per-project consolidated learnings (Deep dreaming)
│   └── index.json             # project/agent index + lastRem timestamp
└── _sessions/
    ├── sessions.json          # global index
    └── <agentId>/
        ├── sessions.json      # per-agent index
        └── <sessionId>.jsonl  # append-only transcript per project
```

Opt out of memory for a specific project by setting `brief.md > ## Decisions (CEO) > memory: off`, or globally by creating `_memory/.disabled`.

If a GitHub connector is present, the plugin will offer to push to a fresh repo at the end.

## Security posture

Default gate: **full STRIDE threat model + OWASP Top 10 coverage** before any code is written, plus a second-pass **code audit + pen-test** after build. CISO blocks the pipeline if any Critical/High risk has no mitigation plan. Compliance posture (GDPR / CCPA / PCI / HIPAA as applicable) is scanned by `compliance-officer`. License compatibility and privacy posture are gated by the GC before public release. See `skills/ship-it/references/owasp-checklist.md`.

## Files of interest

- `skills/ceo/SKILL.md` — the v0.2 orchestrator playbook
- `skills/ceo/references/board-phases.md` — exact phase inputs/outputs/exit criteria
- `skills/ceo/references/meeting-log-format.md` — chat.jsonl entry types
- `skills/board-meeting/SKILL.md` — CEO ↔ Chief meeting contract
- `skills/council-meeting/SKILL.md` — Chief ↔ specialist meeting contract
- `skills/command-center/references/artifact-template.html` — live HTML view
- `skills/memory/SKILL.md` — three-tier dreaming (Light / Deep / REM), write policy, retrieval
- `skills/session-log/SKILL.md` — JSONL schema + `rg`/`jq` replay recipes
- `skills/gates/SKILL.md` — gate vocabulary, per-council rules (`references/gate-rules.md`), aggregation worked examples (`references/aggregation.md`)
- `skills/taskflow/SKILL.md` — six-state machine (`references/state-machine.md`), fix-loop cap + escalation template (`references/fix-loop.md`)
- `skills/worktree/SKILL.md` — isolation lifecycle, per-phase parallel matrix (`references/parallel-matrix.md`), merge algorithm + conflict classes (`references/merge-policy.md`)
- `skills/skill-creator/SKILL.md` — runtime roster extension with agent (`references/agent-template.md`) and skill (`references/skill-template.md`) templates, collision policy (`references/collision-policy.md`)
- `skills/model-tiering/SKILL.md` — per-agent tier defaults (`references/tier-rules.md`), cost/latency rationale (`references/cost-model.md`), override log (`references/override-log.md`)
- `skills/notify/SKILL.md` — event catalog, transport priority + hook wiring (`references/hook-wiring.md`), payload shapes (`references/payload-shapes.md`), rate-limit + opt-out (`references/rate-limit.md`)
- `skills/memory/references/novelty.md` — Jaccard novelty gate, thresholds, worked examples
- `skills/ship-it/references/owasp-checklist.md` — security gate rules
- `skills/ship-it/references/status-schema.md` — status.json + chat.jsonl + _sessions + tasks[] + gates schemas
- `skills/ship-it/references/escalation-rules.md` — when a Chief must escalate
- `AGENTS.md` — repo-root conventions: gate vocabulary, deterministic-ordering rule, anti-patterns
- `agents/AGENTS.md`, `skills/AGENTS.md` — subtree rules for persona and skill files
- `councils/<council>/AGENTS.md` — per-council Must / Must not / Gate heuristic (9 files)
- `CLAUDE.md` — thin pointer to root `AGENTS.md` for tools that look there

## Versions

- **0.3.5** — *Audited Apache-2.0 imports from `anthropics/skills`.* Three new skills, two new specialists, zero net new injection surface. `skills/mcp-authoring/` is the **producer side** of the MCP lifecycle, paired with v0.3.4's `mcp-defense` consumer side — four-phase Plan → Implement → Review → Evaluate with a mandatory 10-question XML eval suite and ≥8/10 pass-rate release gate. `skills/webapp-testing/` wraps Playwright with a multi-server lifecycle runner; the upstream `scripts/with_server.py` used `shell=True` + `cd backend && …`, which was **rewritten before import** to `shell=False` + `shlex.split(..., posix=True)` + a new per-server `--cwd` flag to preserve the "injection-resistant, hard to break into" posture (modifications marked per Apache 2.0 §4(b)). `skills/skill-eval/` imports only the eval-harness subset of upstream `skill-creator` (`run_eval.py`, `run_loop.py`, `aggregate_benchmark.py` with σ/μ ≤ 0.15 variance gate, `quick_validate.py` pre-flight, `improve_description.py` for trigger-precision tuning, HTML review viewer) — deliberately does NOT replace the agency's own `skill-creator`; authoring and judging are split roles. New specialists: `mcp-author` (Execution Council, sonnet blue — runs the four-phase MCP process, pairs with `mcp-defender` on the consumer side) and `skill-evaluator` (Evaluation Council, sonnet cyan — runs pass-rate ≥ 0.80 floor + σ/μ ≤ 0.15 variance gate, owns the minor-version sweep that re-evaluates every skill at each v0.x bump). Non-imports: `docx`/`pdf`/`pptx`/`xlsx` (source-available, not redistributable — already Claude defaults in Cowork); `brand-guidelines`, `internal-comms`, `claude-api`, and the creative-skill set (off-mission for a DevSecOps agency). Every imported SKILL.md was grep-audited for jailbreak / Parseltongue / GODMODE / "ignore-previous" patterns (none found); every script was read for dangerous patterns (`shell=True` in `webapp-testing/scripts/with_server.py` was the only finding — hardened before import).
- **0.3.4** — *Injection-resistant hardening + 2026 landscape alignment.* Zero-import wave — every addition is agency-authored, so no new injection surface. Eight new skills: `skills/mcp-defense/` (6-class MCP threat taxonomy: tool poisoning, rug-pull, manifest pre-execution, indirect-injection-via-tool-output, over-permission, response-path exfil; pinned-hash registration, `<tool-description-data>` + `<tool-output-data>` envelopes, quarterly sweep), `skills/observability/` (OpenTelemetry GenAI semantic-conventions instrumentation — trace-id + parentSpanId propagation, per-span `gen_ai.*` attributes, prompts + completions as events not attributes, DLP pre-filter on events, tail-based sampling 100% errors / 10% success), `skills/prompt-cache/` (post-Feb-2026 Anthropic cache strategy — canonical 4-breakpoint assembly, default 5-min TTL, paid 1-hour opt-in only for >6 dispatches per window, workspace-level isolation awareness, ≥ 60% hit-rate target), `skills/dlp/` (outbound DLP on every tool call — 5-channel scan args+URL+query+headers+body, chain-of-tool correlation 20 calls / 5 min for split-secret detection, static-first-NLP-second, block-is-default with waiver ADR TTL ≤ 24 h, redact-at-scanner), `skills/injection-defense/` (4-layer PromptGuard: L1 input gatekeeping with regex + structural-marker + zero-width-unicode strip + homoglyph + optional MiniBERT; L2 `<untrusted-data>` envelope; L3 semantic output validation with instruction-density + tool-call-shape + persona-drift checks; L4 adaptive refinement; 10-class 2026 attack taxonomy; Rebuff explicitly NOT used — archived May 2025), `skills/finops/` (4-column token tracking prompt/tool/memory/response × 3-dim attribution project/council/agent-phase, weekly Monday report, anomaly thresholds span>$1 trace>$10 project>2×7d-mean, cache-creation-cost-pays-creator-not-reader, quarterly roll-up feeds CAO portfolio audit), `skills/chaos/` (14-fault agent-specific library: model-unavailable/slow, partial-response, tool-error-transient/permanent, tool-output-malformed/injected, tool-args-mutated-in-flight, rate-limit-burst, context-overflow, memory-corrupt, clock-skew, audit-log-write-fail, vault-unavailable; sandbox-only; canonical 12-fault pre-release suite with green/yellow/red gate), `skills/self-critique/` (pre-return constitutional check distinct from post-hoc `audit` — 15-principle frozen hash-indexed set, 3-principle sampling per turn seeded by trace-id, separate-completion critique to prevent draft contamination, max 2 revisions then escalate, runtime-hook-enforced). Six new specialists: `agent-telemetry-engineer` (SRE, distinct from existing app-level `observability-engineer`), `prompt-cache-tuner` (SRE), `dlp-scanner` (Security), `finops-analyst` (Evaluation), `chaos-engineer` (Red-Team), `mcp-defender` (Security). Cross-skill wiring: `observability` is the trace source for `finops` / `chaos` / `dlp` / `prompt-cache` / `injection-defense`; `dlp` + `injection-defense` share envelopes with `mcp-defense`; `self-critique` + `audit` cite the same principle set. No new council needed — every addition slots into existing structure.
- **0.3.3** — *Forensics + arxiv + governance reviewer.* Three audited imports from previously-surveyed repos, each filling a real gap. `skills/oss-forensics/` (ported from `NousResearch/hermes-agent` MIT, inspired by RAPTOR's 1800+ line OSS Forensics system): supply-chain investigation toolkit for deleted-commit recovery, force-push detection, IOC extraction, and multi-source evidence collection — consumed by the Security Council (alongside `secrets-vault` + `sbom-slsa`) and the Red-Team Council's `supply-chain-attacker` specialist. `skills/arxiv/` (ported from hermes-agent MIT): thin wrapper over the free arXiv REST API (no key required) for Research Council academic grounding. `agents/agent-governance-reviewer.md` (ported from `github/awesome-copilot` MIT, frontmatter reformatted to agency convention — kebab-case name, sonnet tier, read-only tool grant, council color white): Audit Council specialist that reports to `cao` and runs a 10-point meta-governance review (tool-decorator coverage, intent classification, credential scan, append-only audit trail, rate-limit ceilings, multi-agent trust boundaries, most-restrictive-wins policy composition, fail-closed defaults, allowlist-over-blocklist, HITL on high-impact ops). All three audited clean of `eval` / `exec(open` / `curl … | bash` / `os.system` / `shell=True`. Exclusions (carried over): `godmode` (prompt-injection), `sherlock` (doxxing), `1password` (cred-handling), plus the 200+ awesome-copilot chat modes that duplicate agency roles. No changes to user-facing surface — you still talk only to the CEO.
- **0.3.2** — *SDLC patterns pack.* Adds `skills/sdlc-patterns/` — six operational SDLC skills ported from `NousResearch/hermes-agent` (MIT) after a prompt-injection audit: `plan`, `writing-plans`, `systematic-debugging`, `test-driven-development`, `requesting-code-review`, `subagent-driven-development`. These are specialist-invoked references, not user entry points — the user still talks only to the CEO. The hermes-agent `red-teaming/godmode` skill was **deliberately excluded** (Parseltongue encoding, GODMODE jailbreak templates, `exec(open(...))` dynamic script loader, `auto_jailbreak()` config writer — explicit prompt-injection toolkit that violates the agency's adversarial-defense-first OWASP ASI posture). The GitHub and runtime-framework parts of hermes-agent were skipped as either redundant (gh/git already in use) or non-portable (TUI, gateway, RL training). No new councils, no agent changes.
- **0.3.1** — *Runtime-hooks patch.* Adds `runtime-hooks/` — five read-only defender hooks ported from `github/awesome-copilot` after a prompt-injection audit (`secrets-scanner`, `tool-guardian`, `governance-audit`, `dependency-license-checker`, `session-logger`) plus a locked-down `commit-gate.sh` replacement. The upstream `session-auto-commit` hook was **deliberately excluded** because it uses `git add -A` + `--no-verify` + `git push`, which bypasses every other hook. No new councils, no agent changes, no prompt mutations — only runtime enforcement bolted onto existing skills (`secrets-vault`, `tool-scout`, `audit`, `ip-lineage`, `session-log`). All hooks are read-only regex defenders: no `eval`, no `bash -c`, no network fetch, no remote pattern loading.
- **0.3.0** — *Company release — final cut.* Seven cumulative waves:
  - **Wave 1** (foundations): `vision-doc` + `okr` + `adr` + `meeting-minutes`. Durable mission / OKRs / ADRs / minutes. Every Chief dispatch gets a 3-bullet KR slice; every gate validates after `okr.score`; every material decision files an ADR same-turn; every user / board / blocking-council / red-team / audit / retro convening writes minutes.
  - **Wave 2** (pipeline + user-meeting): Marketing (CMO) + Strategy (CSO) councils. `idea-pipeline` 4-stage funnel → top-5; `user-meeting` 4-phase flow (brief → present → capture → commit); `market-intel` + `positioning` canonical shapes.
  - **Wave 3** (people-ops + audit): People-ops (COO) + Audit (CAO) councils. `roster` (living agent registry + hire / fire / tier-change / repurpose with mandatory ADRs and `_vision/roster/_archive/`); `audit` (4 kinds, independent, every red → ADR); `capacity` (utilization bands + KR coverage gaps). CAO never on any delivery path.
  - **Wave 4** (resilience ladder): `ladder` skill. 8 rungs from `Retry` (0) to `Parking lot` (7). Every rung transition files an ADR. Rung 7 is resumable-terminal; blocking-council reds start the ladder instead of durably blocking.
  - **Wave 5** (evaluation + budget): Evaluation (CEVO) council. `eval` (mandatory close-eval paired with close-audit, 5 pp regression threshold, quarter-frozen baselines); `budget` (4 size classes + per-phase allocation + 110 % triggers Rung 6). Token-compactor performs structured rewrites with a never-compact list.
  - **Wave 6** (red-team + self-modifying playbooks): Red-Team (CRT) council. `red-team` (OWASP ASI Top 10 2025 mapping, 5 kinds, severity × impact × boundary × mitigation rubric); `playbook` (DGM-style immutable stepping-stones, supersession-only, prompt-diff review blocking gate on every `agents/*.md` or `councils/*/AGENTS.md` edit with weakening-phrasing auto-reject).
  - **Wave 7** (SRE + tool-scout + provenance): SRE (CSRE) council. `tool-scout` (7-dimension rubric); `a2a` (cross-agency adapters, default-deny, rate limits, 30 s timeouts, mTLS/JWT); `sandbox` (ephemeral `/tmp/sandbox-<nonce>/`, 2 CPU / 2 GB / 60 s, net default-deny, diff-not-state); `model-routing` (same-tier lateral fallback matrix). Security additions: `sbom-slsa` (CycloneDX + SLSA provenance, keyless sigstore); `secrets-vault` (vault refs only, 30 d rotation, weekly scans). Legal additions: `ip-lineage` (lineage tree + license reconciliation + similarity check); `compliance-drift` (monthly + on-demand, SOC 2 / GDPR / HIPAA, drift ≠ breach).
- **0.2.5** — `skill-creator`, `model-tiering`, `notify` skills + novelty gate on `memory`. Runtime roster extension via AGENTS.md-compliant agent/skill authoring. Per-agent model tiering with Opus CEO / Sonnet Chiefs (+ skill-creator) / Haiku specialists, enforced at dispatch — CEO refuses agents without a tier. Single push-notify surface with 5-per-run rate limit, digest fallback, and Cowork `Stop` / `SubagentStop` hook wiring. Jaccard novelty gate on every Light/Deep/REM write skips trivial duplicates instead of bloating `MEMORY.md`.
- **0.2.4** — `worktree` skill. Parallel dispatches and every fix-loop (attempt ≥ 1) run in isolated `<slug>/_worktrees/<chief>-<attempt>/` directories with declared `writes[]`/`reads[]`, atomic scope-checked alphabetical merge, stale-rebase detection, and structural-vs-non-structural conflict handling.
- **0.2.3** — `gates` + `taskflow` skills. Formal gate vocabulary (green/yellow/red/n/a) with blocking-vs-informing council split, per-rule matrix, and aggregation semantics. Six-state task machine with a hard 2-attempt fix-loop cap and handoff invariants. `status.json` gains `tasks[]` and `gates{}`.
- **0.2.2** — Scoped `AGENTS.md` hierarchy (root + `agents/` + `skills/` + 9 councils = 13 files). Deterministic-ordering rule for prompt-cache hits. CEO now quotes the matching council rules into every Chief dispatch. `CLAUDE.md` pointer at the root.
- **0.2.1** — Durable memory (Light/Deep/REM dreaming) and per-agent session logs, ported from openclaw's memory-host-sdk pattern. Cross-project learnings + grep-addressable transcripts.
- **0.2.0** — CEO + 9 councils + ~28 specialists. 7-phase board. Command center shows meetings by scope.
- **0.1.0** — 6-team hierarchy. 10-stage pipeline. Still runnable via `ship-it`.
