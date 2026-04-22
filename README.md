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
