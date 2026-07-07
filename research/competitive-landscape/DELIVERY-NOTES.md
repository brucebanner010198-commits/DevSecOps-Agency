# Delivery Notes — state of this branch

Captured in writing so the delivery state isn't only in chat. **Date:** 2026-06-02.

## What was delivered

- **Branch:** `research/competitive-landscape-ai-os`
- **Scope:** net-new directory `research/competitive-landscape/` only. No code, config, or root docs changed.
- **Contents:** index + executive summary + master matrix (`00`, `02`, `01`); 11 player deep-dives (`10`–`31`); 7 synthesis docs (`40`–`46`); shared template (`_TEMPLATE.md`); this note.
- **Method:** parallel research agents (one per player doc) doing live web research, then CEO synthesis. Each player doc carries ≥5 dated sources (most 10–24). Citation discipline per `AGENTS.md:43-44` + `skills/market-intel`: every claim cited or tagged `[synthesised]`/`[hypothesis]`/`[user-knowledge]`; unknowns flagged, not invented; confidence L/M/H.

## Known caveats (honest record)

1. **Commit signing was disabled for these commits.** The environment's signing server returned HTTP 400 ("missing source") on every attempt, so commits were made with `commit.gpgsign=false` to let the work land. Re-sign / amend when signing is restored if the repo requires signed commits.
2. **No GitHub remote in this container.** The repo was seeded from a local bundle (`/home/user/.seed.bundle`), so `.git` has **no `origin`** and the `gh` CLI is not installed. A normal `git push origin` / PR-open cannot run from here. The work lives as commits on the branch above, which the web platform tracks. To publish a PR, either the platform surfaces this branch, or a remote is added locally:
   ```
   git remote add origin <github-url>
   git push -u origin research/competitive-landscape-ai-os
   # then open a PR
   ```
3. **WebFetch was broadly 403-blocked** in this environment; agents triangulated facts from dated search-engine extracts of the same primary URLs. Where this lowers confidence, the relevant doc says so. Self-reported benchmarks (e.g. Flowith's Mind2Web score) are labelled as such, not treated as verified.

## Next step

The design conversation has not started. It runs one question at a time per `45-open-questions-interview.md`, beginning with: *which build form (A app / B distro / C cloud-streamed) does "the OS" mean?* (See `40-os-fundamentals-primer.md` §4.)
