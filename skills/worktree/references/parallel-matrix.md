# Parallel dispatch matrix

Which Chiefs run in parallel per phase, and exactly which paths each writes and reads. The CEO uses this when allocating worktrees so the `writes[]` / `reads[]` fields in `worktree.json` are declared upfront (not inferred).

A Chief that writes paths outside its declared `writes[]` fails the merge check and bounces. A Chief that reads from a sibling's worktree — forbidden. Reads only from the main tree or its own worktree.

## Phase 1 — Discovery (parallel)

Two Chiefs run in parallel. Non-overlapping writes.

| Chief     | writes[]                                                | reads[] (from main tree)         |
| --------- | ------------------------------------------------------- | -------------------------------- |
| `cro`     | `research-brief.md`, `research/market.md`, `research/tech-landscape.md`, `research/prior-art.md`, `research/user-needs.md` | `brief.md` |
| `pm-lead` | `product/strategy.md`, `product/roadmap.md`             | `brief.md`, `research/*` (read after `cro` merges — allocate `pm-lead` worktree only after `cro` merges if `pm-lead` needs research input) |

Allocation note: if the user's idea doesn't require research to draft a strategy, `cro` and `pm-lead` can genuinely run in parallel. If `pm-lead` needs research output, dispatch `cro` first, merge, then `pm-lead` — no worktree needed for `pm-lead`.

## Phase 2 — Design (sequential, no parallel)

One Chief at a time.

| Chief               | writes[]                                                        | reads[]                 |
| ------------------- | --------------------------------------------------------------- | ----------------------- |
| `engineering-lead` (CTO) | `architecture.md`, `architecture/data-model.md`, `architecture/infra.md` | `brief.md`, `research-brief.md`, `product/*` |
| `security-lead` (CISO)   | `threat-model.md`, `security/compliance.md`                    | `architecture.md`, `architecture/data-model.md`, `architecture/infra.md` |

CISO follows CTO sequentially. Worktree only allocated if CTO is on a fix-loop (attempt ≥ 1).

## Phase 3 — Build (sequential)

| Chief                    | writes[]                        | reads[]                                      |
| ------------------------ | ------------------------------- | -------------------------------------------- |
| `engineering-lead` (VP-Eng) | `src/**`, `.env.example`, migration files | `architecture.md`, `architecture/**`, `threat-model.md`, `product/*` |

Worktree on every Build dispatch. Build is the heaviest phase and fix-loops are expected; cheap to have worktrees default-on here.

## Phase 4 — Verify (parallel)

Two Chiefs run in parallel. Non-overlapping writes.

| Chief           | writes[]                                                      | reads[]                                   |
| --------------- | ------------------------------------------------------------- | ----------------------------------------- |
| `qa-lead` (CQO) | `tests/**`, `qa-report.md`, `qa/perf-report.md`, `qa/a11y-report.md` | `src/**`, `architecture.md`, `threat-model.md`, `product/*` |
| `security-lead` (CISO²) | `security/code-audit.md`, `security/pentest-report.md` | `src/**`, `threat-model.md`, `architecture.md`, `security/compliance.md` |

Both read `src/**` concurrently (reads don't conflict). Writes are in disjoint subtrees (`tests/`, `qa/`, `qa-report.md` vs `security/code-audit.md`, `security/pentest-report.md`).

## Phase 5 — Ship (sequential)

| Chief                | writes[]                                                            | reads[]                                                         |
| -------------------- | ------------------------------------------------------------------- | --------------------------------------------------------------- |
| `devops-lead` (VP-Ops) | `deploy/**`, `.github/workflows/*.yml` (when applicable), `deploy/runbook.md`, `deploy/observability.md` | `src/**`, `architecture/infra.md`, `security/code-audit.md`, `qa-report.md` |

## Phase 6 — Document + Legal (parallel)

Two Chiefs run in parallel. Non-overlapping writes.

| Chief             | writes[]                                                         | reads[]                                       |
| ----------------- | ---------------------------------------------------------------- | --------------------------------------------- |
| `docs-lead` (CKO) | `docs/README.md`, `docs/api/**`, `docs/tutorial/getting-started.md` | `src/**`, `architecture.md`, `deploy/**`, `legal/*` (after GC merges, or dispatch CKO after GC) |
| `gc`              | `legal/licenses.md`, `legal/privacy.md`, `PRIVACY.md` (root of project) | `src/**`, `architecture/data-model.md`, `deploy/**`, `package.json`/`requirements.txt`/etc. |

Note: `docs-lead` linking to PRIVACY/LICENSE from README means CKO needs GC's output. Two valid orderings:

1. Dispatch GC first, merge, then CKO (no parallelism but simple).
2. Dispatch both in parallel; CKO uses placeholder links and emits `yellow` with a `followup` to re-run after GC. Merge CKO after GC.

Option 1 is the default. Option 2 only if the user is in a hurry and accepts the yellow.

## Phase 7 — Close (sequential)

| Chief     | writes[]                         | reads[]                     |
| --------- | -------------------------------- | --------------------------- |
| `ceo` (you) | `status.json` final, user summary | `chat.jsonl`, all artifacts |

No worktree. CEO is the merger of last resort.

## Summary of default worktree allocations

| Phase            | Default parallel?  | Worktrees on attempt 0? |
| ---------------- | ------------------ | ----------------------- |
| Discovery        | `cro` + `pm-lead`  | yes (both)              |
| Design           | no                 | no (direct write)       |
| Build            | no                 | yes (heavy phase)       |
| Verify           | `qa-lead` + `security-lead²` | yes (both)    |
| Ship             | no                 | no                      |
| Document + Legal | optional           | yes if parallel, else no |
| Close            | no                 | no                      |

On any fix-loop (attempt ≥ 1), allocate a worktree regardless of phase.
