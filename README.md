# DevSecOps Agency

A Claude Code plugin that turns one prompt into a shipped project. You speak only to the **CEO**; the CEO runs a board of 16 Chiefs; each Chief runs a council of specialists; specialists may, when the work shards cleanly, spawn **workers** to run in parallel. Research-first, security-second, receipts-always.

Status: `v0.5.1` · MIT + imports (see `LICENSES/`). Security policy: [`SECURITY.md`](SECURITY.md). Trust commitments: [`TRUST.md`](TRUST.md). Live ops console: [`command-center/`](command-center/) (deploys to GitHub Pages on every push).

## Identity

- **[`CONSTITUTION.md`](CONSTITUTION.md)** — **supreme document.** Ratified 2026-04-22 (Schedule A amended 2026-04-22 for v0.5.0). Preamble + 12 Articles + Bill of Rights + Schedule A (founding docs) + Schedule B (ratification) + Sources & Influences. RFC 2119 grammar. Read FIRST at every session start; cited by every amendment / waiver / drill report / close-audit. User is sovereign; only the User may amend it.
- [`MISSION.md`](MISSION.md) — "Ship software that is secure, receipted, and reversible." North Stars, non-goals, one-sentence tagline.
- [`VALUES.md`](VALUES.md) — 11 operating principles the CEO reads at every session start.
- [`KEEPER-TEST.md`](KEEPER-TEST.md) — quarterly fire-readily review (Netflix-inspired). User has final vote on fires.
- [`LESSONS.md`](LESSONS.md) — append-only cross-project learning ledger, one row per close.
- [`RHYTHM.md`](RHYTHM.md) — daily / weekly / monthly / quarterly heartbeat cadence. The paper trail has a pulse; the CEO reads it at session start.
- [`CAREER.md`](CAREER.md) — L1 (trial) → L2 (steady) → L3 (principal) within-tier level ladder. Inter-tier mobility is USER-ONLY.
- [`GOVERNANCE.md`](GOVERNANCE.md) — decision matrix (Proposer / Reviewer / Approver / Final-vote). Enumerates the 10 USER-ONLY actions and separates blocking chiefs (CISO/CEVO/CRT/CAO) from informing-only chiefs.
- [`RESILIENCE.md`](RESILIENCE.md) — failure-mode map. First response + escalation path + skill + ADR kind for every failure. Four degraded modes (model / heartbeat / chief / budget); five recovery guarantees.
- [`SECURITY.md`](SECURITY.md) — public security policy (v1.0, ratified 2026-04-22 with plugin v0.4.2). Scope + supported versions + reporting channels (GitHub Private Vulnerability Reporting primary, email fallback) + 48h ack / 7d triage / 7d-30d-next-wave fix SLAs / 90d coordinated disclosure / CVSS v3.1 severity rubric / plugin-specific threat model / responsible-testing rules / safe harbor. Non-waivable classes (raw-secret + ASI) inherit from Constitution §8.5.
- **[`TRUST.md`](TRUST.md)** — twelve public trust commitments (v1.0, v0.5.0) each with Claim / Verify-how / If-we-miss; scorecard + incident timeline + push-back channel. First quarterly publish 2026-07-22.
- **[`SWOT.md`](SWOT.md)** — rolling self-audit (v1.0, v0.5.0). 14 Strengths / 18 Weaknesses / 10 Opportunities / 12 Threats with mitigation-by-wave roadmap through v1.0.0. Refreshed at every Keeper Test.
- **[`SYSTEM-CARD.md`](SYSTEM-CARD.md)** — capabilities, limits, tested bounds (v1.0, v0.5.0). Honest "has not been tested" markers. Regenerated at every minor version bump by `skills/system-card`.
- **[`THREAT-MODEL.md`](THREAT-MODEL.md)** — plugin-level STRIDE + OWASP ASI Top 10 + NIST AI RMF + MITRE ATLAS five-lens overlay (v1.0, v0.5.0). Residual-risk table by category.
- **[`DISASTER-RECOVERY.md`](DISASTER-RECOVERY.md)** — RPO 24h / RTO 72h. Seven named playbooks (corrupted main, lost repo, compromised release, PAT compromise, read-only mode on 72h User unreach, Anthropic outage, hostile fork). Append-only restoration procedure.
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) — Contributor Covenant 2.1 + 5 agency-specific expectations.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contribution workflow. Amendment-class gates on founding documents.
- [`CODEOWNERS`](CODEOWNERS) — path-to-council ownership map.
- [`.well-known/security.txt`](.well-known/security.txt) — RFC 9116 disclosure contact.
- **[`command-center/`](command-center/)** — **public operations console (v0.1, v0.5.1).** Single `index.html` — no build step — showing CEO + 16 councils org chart (blocking vs informing chiefs flagged), live vital signs fetched from the GitHub API (councils / skills / agents / hooks), today's rhythm of four heartbeats, twelve Trust commitments panel (shows "pending" until 2026-07-22 scorecard), recent commits feed, Schedule-A founding-documents grid, and five one-click meeting launchers (Call a CEO meeting · Convene a council · Issue a new directive · Schedule a drill · Publish Trust Scorecard). Each launcher copies a pre-written slash-command prompt for Claude. Auto-deploys to GitHub Pages via `.github/workflows/pages.yml`; portable to Cloudflare Pages, Vercel, Netlify, or a Cowork artifact. Maintenance procedure in [`skills/command-center-web`](skills/command-center-web/SKILL.md).

## Install

```bash
# Option 1 — from a local .plugin archive
/plugin install devsecops-agency-0.5.1.plugin

# Option 2 — from this repo (inside a Claude Code workspace)
git clone https://github.com/brucebanner010198-commits/DevSecOps-Agency.git
/plugin install ./DevSecOps-Agency
```

Then, in any Claude Code session:

```text
/devsecops-agency:ceo I want a secure invoice-splitter web app for roommates
```

The CEO asks 3–5 clarifying questions, then runs the 7-phase pipeline autonomously. Open `/devsecops-agency:command-center` any time to watch the board.

## How the agency is organised

```
              USER
                │
                ▼
              CEO ← only agent the user speaks to
                │
   ┌──────┬────┼────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
   ▼      ▼    ▼    ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼
  CRO   CPO   CTO  CISO  VP-Eng  CQO  VP-Ops  CKO   GC   CMO   CSO   COO   CAO   CEVO  CRT  CSRE
 Res.  Prod. Arch. Sec.  Exec.  Qual. DevOps Docs Legal Mktg Strat Peo. Audit  Eval R-T  SRE
   │
   └─► specialists ─► workers (optional, per-task fanout)
```

Three tiers — Chief → Specialist → Worker. Amazon two-pizza recursively; depth capped at three levels, deeper requires an ADR.

| Council | Chief (agent) | Purpose |
| --- | --- | --- |
| research | `cro` | Market + tech + literature + user. Wedge + build/don't-build verdict. |
| product | `pm-lead` (CPO) | Strategy, Now/Next/Later/Never roadmap, testable acceptance criteria. |
| architecture | `engineering-lead` (CTO) | System shape: components, data flow, trust boundaries, stack. |
| security | `security-lead` (CISO) | STRIDE + OWASP Top 10; code audit + pen-test; SBOM+SLSA; secrets; DLP; MCP defense. |
| execution | `engineering-lead` (VP-Eng) | Implementation against approved architecture + threat model. |
| quality | `qa-lead` (CQO) | Unit + integration + e2e; p50/p95/p99; a11y axe-core + WCAG AA. |
| devops | `devops-lead` (VP-Ops) | CI, containers, deploy, health, logs, one-command rollback. |
| docs | `docs-lead` (CKO) | README, API docs, ≤ 10-min tutorial. No placeholders. |
| legal | `gc` | License compatibility, privacy posture, IP lineage, compliance drift. |
| marketing | `cmo` | Positioning, copy, brand voice, growth input. Informing, not blocking. |
| strategy | `cso` | Portfolio-level scanning, competitive, sizing, RICE-ranked shortlist. |
| people-ops | `coo` | Roster, hiring via skill-creator, performance, ADR-tracked retirements. |
| audit | `cao` *(independent)* | Read-only integrity pass over the agency's own paper trail. |
| evaluation | `evaluation-lead` (CEVO) *(independent)* | Eval sets, benchmarks, variance-gated skill evals, FinOps. |
| red-team | `red-team-lead` (CRT) *(independent)* | Adversarial prompting, tool abuse, PII exfil, chaos injection. |
| sre | `sre-lead` (CSRE) *(independent)* | MCP registry, a2a, sandbox, model-routing, telemetry, prompt cache. |

**1 CEO + 16 Chiefs + 75 specialists = 92 agents.** Audit / Evaluation / Red-Team / SRE are informing + independent — never on any project's delivery path. The full roster for each council is in [`councils/<name>/TEAM.md`](councils/).

## Worker tier (optional third level)

When a specialist's task shards cleanly along a dimension — per-file, per-endpoint, per-dep, per-table, per-agent-file, per-preprint, per-probe — the specialist declares workers in its frontmatter and spawns a pool. Workers inherit the specialist's tool set and model tier unless overridden, run in isolation (fresh conversations, sandboxed writes under `_workers/<specialist>/<shard>.md`), and aggregate back deterministically.

```yaml
# in agents/<council>/<specialist>.md frontmatter
workers:
  - name: dep-scanner
    split: per-dep
    max_parallel: 8
    aggregation: union
```

Depth cap: Chief → Specialist → Worker (three levels). Deeper fanout requires a council-lead ADR. See [`skills/fanout/SKILL.md`](skills/fanout/SKILL.md) and [`skills/fanout/references/worker-frontmatter-template.md`](skills/fanout/references/worker-frontmatter-template.md). Workers do not spawn workers by default; the skill explains how to extend depth when a domain truly needs it.

## Slash commands

| Command | What it does |
| --- | --- |
| `/devsecops-agency:ceo` | Main entry point. CEO persona; convenes the board; runs the 7 phases. |
| `/devsecops-agency:command-center` | Open / refresh the live HTML status artifact. |
| `/devsecops-agency:intake` | Run intake Q&A only — produce a brief without kicking off engineering. |
| `/devsecops-agency:board-meeting` | Re-run a specific board phase (power-user). |
| `/devsecops-agency:council-meeting` | Re-run a specific council (power-user). |
| `/devsecops-agency:status` | Quick text summary of the active project. |
| `/devsecops-agency:escalate` | Process parked human-input queue and resume the pipeline. |
| `/devsecops-agency:retro` | Post-deploy retrospective; also triggers REM dreaming on new patterns. |
| `/devsecops-agency:ship-it` | Legacy v0.1 six-team pipeline. Still runnable. |

Internal skills the CEO and Chiefs invoke (not user-facing): `taskflow`, `gates`, `worktree`, `memory`, `session-log`, `notify`, `model-tiering`, `skill-creator`, `fanout`, `ladder`, `audit`, `eval`, `budget`, `red-team`, `playbook`, `tool-scout`, `a2a`, `sandbox`, `model-routing`, `vision-doc`, `okr`, `adr`, `meeting-minutes`, `idea-pipeline`, `user-meeting`, `market-intel`, `positioning`, `roster`, `capacity`, `mcp-defense`, `mcp-authoring`, `observability`, `prompt-cache`, `dlp`, `injection-defense`, `finops`, `chaos`, `self-critique`, `oss-forensics`, `arxiv`, `messaging-formatting`, `container-isolation-posture`, `webapp-testing`, `sdlc-patterns`, `skill-eval`.

## The 7 phases

```
1  Discovery       CRO + CPO           (parallel)
2  Design          CTO → CISO          (sequential; CISO reviews)
3  Build           VP-Eng
4  Verify          CQO + CISO²         (parallel)
5  Ship            VP-Ops
6  Document+Legal  CKO + GC            (parallel)
7  Close           CEO                 (includes CAO + CEVO + CRT)
```

Exit criteria per phase live in [`skills/ceo/references/board-phases.md`](skills/ceo/references/board-phases.md). No Critical/High unmitigated risk ever passes CISO.

## Repo layout

```
agents/                   # 92 agent persona files, grouped by council
  ceo.md                  # root — the only user-facing agent
  <council>/<agent>.md    # e.g. agents/security/threat-modeler.md
councils/                 # per-council contract + team card
  <council>/
    AGENTS.md             # must / must-not / gate heuristic  (contract)
    TEAM.md               # lead + specialists + worker patterns  (roster)
skills/                   # 58 skills — orchestration, defense, memory, eval, ops
runtime-hooks/            # read-only defender hooks (v0.3.1)
LICENSES/                 # import provenance + upstream license text
AGENTS.md                 # repo-root conventions: gates, ordering, anti-patterns
CHANGELOG.md              # wave history (v0.1.0 → current)
CLAUDE.md                 # pointer to AGENTS.md
```

## Output

Each project lands at `outputs/devsecops-agency/<slug>/` with `brief.md`, `research/`, `product/`, `architecture.md`, `threat-model.md`, `src/`, `tests/`, `deploy/`, `docs/`, `legal/`, `status.json`, `chat.jsonl`, `inbox.json`, and `_worktrees/` for parallel + fix-loop work. Across projects: `_memory/` (MEMORY.md + dated Light / per-project Deep / cross-project REM patterns) and `_sessions/` (append-only JSONL per agent). See [`skills/ship-it/references/status-schema.md`](skills/ship-it/references/status-schema.md) for the exact schemas. If a GitHub connector is present, the plugin offers to push to a fresh repo on close.

## Security posture

Full STRIDE + OWASP Top 10 before code is written. Second-pass code audit + pen-test after build. CISO blocks on any Critical/High without mitigation. MCP defense via pinned-hash registration. DLP on every outbound tool call. Secrets only via vault refs. Every shipped artifact gets SBOM + SLSA provenance. OWASP ASI Top 10 2025 covered by the Red-Team council. Session logs are append-only. Memory writes pass a Jaccard novelty gate. Runtime hooks enforce `commit-gate`, `secrets-scanner`, `tool-guardian`, `governance-audit`, `dependency-license-checker`, `session-logger`.

**Reporting a vulnerability in the plugin itself:** see [`SECURITY.md`](SECURITY.md) — GitHub Private Vulnerability Reporting is the preferred channel; 48h ack / 7d triage / 90d coordinated disclosure; CVSS v3.1 severity rubric; raw-secret and ASI-class findings are non-waivable per Constitution §8.5.

## Learn more

- [`AGENTS.md`](AGENTS.md) — repo-root rules (gates, ordering, taskflow, anti-patterns).
- [`CHANGELOG.md`](CHANGELOG.md) — wave-by-wave history.
- [`councils/<name>/AGENTS.md`](councils/) — per-council contracts.
- [`councils/<name>/TEAM.md`](councils/) — per-council rosters.
- [`skills/ceo/SKILL.md`](skills/ceo/SKILL.md) — the orchestrator playbook.
- [`skills/fanout/SKILL.md`](skills/fanout/SKILL.md) — worker tier convention.
