---
name: command-center-web
description: >
  Maintain the public agency-wide Command Center at `command-center/index.html`.
  This is the hostable web surface (GitHub Pages / Cloudflare Pages / Vercel /
  Netlify / Cowork artifact) that shows the full org chart, rhythm, trust
  commitments, and CEO meeting launcher. Update whenever councils are added or
  removed, rhythm cadence changes, a new Schedule-A founding document is
  incorporated, or a new Trust commitment is added. Distinct from the
  per-project `skills/command-center` which renders a Cowork artifact for the
  active project — this one is the agency-wide public console.
  Trigger phrases include "update the public command center",
  "refresh the web command center", "add a council to the command center",
  "add a doc to the command center", or
  /devsecops-agency:command-center-web.
metadata:
  version: "1.0.0"
---

# command-center-web — maintain the public operations console

Authority: `CONSTITUTION.md` Schedule A · `TRUST.md` §3 · `GOVERNANCE.md` decision matrix
Owner: CEVO · Reviewer: CAO · Called by: `skills/rhythm` (on minor version bump), on demand

## Purpose

The file `command-center/index.html` is the single public surface that shows the Agency running. It renders:

- CEO + 16 councils (blocking vs. informing).
- Vital signs from the repo (councils / skills / agents / hooks — live from the GitHub API).
- Today's rhythm (four heartbeats per RHYTHM.md).
- Trust commitments (twelve per TRUST.md §2; status until first scorecard = "pending").
- Recent commits (last 20 to `main`, relative timestamps, rate-limit displayed).
- Schedule-A founding documents linked to source.
- Five meeting-launcher actions with pre-written prompts.

When any of those source-of-truth facts changes, this file must change with it. A stale command center is a Trust failure (the data is fake) and an Availability failure (the User cannot see the Agency running).

## When to run

- **Required:** Every minor version bump (v0.X.0) — re-measure and reconcile.
- **Required:** Any time a council is added, removed, renamed, promoted to blocking, or demoted to informing.
- **Required:** Any time RHYTHM.md changes cadence or label of any heartbeat.
- **Required:** Any time Schedule A of the Constitution adds or removes a founding document.
- **Required:** Any time a Trust commitment is added, removed, or reworded.
- **Required:** Any time a new user-facing meeting/action becomes common enough to justify a launcher button.
- **On demand:** CEO asks for a refresh; UX / a11y critique comes back; repository is renamed.

## Inputs

1. `command-center/index.html` — the file being edited.
2. `CONSTITUTION.md` Schedule A — authoritative list of founding documents.
3. `GOVERNANCE.md` §blocking-councils — which chiefs hold vetoes.
4. `RHYTHM.md` — cadence table for the four heartbeats.
5. `TRUST.md` §2 — commitments.
6. `councils/` — ground-truth council list.
7. `.github/workflows/pages.yml` — deploy workflow.

## Procedure

### Step 1 — Measure ground truth

```bash
ls councils/ | wc -l          # should equal COUNCILS.length in index.html
ls skills/ | wc -l             # live-fetched at runtime, but sanity-check
ls runtime-hooks/ | wc -l      # live-fetched at runtime
ls *.md CODEOWNERS .well-known/* 2>/dev/null  # Schedule-A surface
```

### Step 2 — Reconcile COUNCILS array

Open `index.html`. In the `<script>` block, find `const COUNCILS = [...]`. Each entry is `{ slug, name, chief, role, tier }`:

- `slug` must match the directory under `councils/`.
- `role: "block"` for CISO, CRT, CEVO, CAO; `role: "inform"` for everyone else.
- `chief` is the short handle; keep to 4 characters where possible.
- If a council was added, append a new entry and update the grid responsive classes (already 2/3/4 columns at breakpoints — usually no change needed).
- If a council was removed, delete the entry and archive the old roster in a LESSONS row.

### Step 3 — Reconcile RHYTHM array

If RHYTHM.md changed: mirror the cadence row here. Keep the same four-tier shape (daily / weekly / monthly / quarterly) — deeper nesting hurts the at-a-glance value of the panel.

### Step 4 — Reconcile TRUST array

If TRUST.md §2 changed: mirror commitment numbers and short labels. Labels ≤ 80 characters for the mono row. If a commitment was retired, do **not** renumber — TRUST commitments are append-only by §2 rules.

### Step 5 — Reconcile DOCS array

If Schedule A changed: add or remove the `{ name, file, tag }` entry. Tags and their color palette:

- `supreme` — CONSTITUTION only. Info chip.
- `identity` — MISSION, VALUES. Info chip.
- `rules` — GOVERNANCE, RESILIENCE, RHYTHM, CAREER, KEEPER-TEST. Muted chip.
- `learning` — LESSONS. Muted chip.
- `security` — SECURITY, THREAT-MODEL, DISASTER-RECOVERY, `.well-known/security.txt`. Crit chip.
- `trust` — TRUST, SWOT, SYSTEM-CARD. Ok chip.
- `community` — CODE_OF_CONDUCT, CONTRIBUTING, CODEOWNERS. Warn chip.

### Step 6 — Add / update an action

Adding an action means adding a button in the hero row and an entry in the `ACTIONS` object with keys `title`, `lede`, `prompt`. Keep prompts:

- Addressed to the relevant chief by code (CEO, CAO, CSRE, etc.).
- Cite the exact skill slash-command when one exists.
- Reference the Constitution / TRUST / relevant doc by file path.
- Explicitly instruct "follow session-start reading path" so the Agency never shortcuts.

### Step 7 — Visual / a11y pass

Before committing:

- Keyboard-only: Tab through every control; every interactive element must have a visible focus ring or border highlight.
- Color contrast: chip text vs. background ≥ 4.5:1 for body text; WCAG 2.2 AA.
- Dialog: `Esc` closes `action-modal`; first focusable element is the Close button.
- Dark-mode only for now — add a light-mode toggle in v0.6.0 only if researched.

### Step 8 — Sanity-check GitHub API quota

A full page load uses ~19 API calls. If you added a new data source that fans out across directories (like the per-council roster fetch), cache aggressively and/or add a manual Refresh gate. The page must stay usable to an unauthenticated viewer with the 60 req/hr cap.

### Step 9 — Deploy verification

After `main` receives a change to `command-center/**`, the GitHub Pages workflow (`.github/workflows/pages.yml`) redeploys automatically. Confirm:

1. Workflow run succeeded under *Actions → Deploy Command Center to GitHub Pages*.
2. Open `https://<owner>.github.io/<repo>/` in a private window (no cached auth).
3. Vital signs populate within 5 seconds.
4. No console errors beyond the Tailwind CDN "production" warning.

If Cloudflare Pages is also configured, verify the `.pages.dev` URL populates within 30 seconds of push.

### Step 10 — Document the update

- Add a CHANGELOG entry line under the current wave.
- If the change materially altered what the User sees (new action, new council, new commitment), note it in SYSTEM-CARD.md §6 (known failure modes → "command center can go stale between X and Y").

## Anti-patterns

- **Silent out-of-sync.** Don't update TRUST.md without updating the `TRUST` array here.
- **Aspirational rendering.** Don't show a council or commitment that isn't real in the repo. The command center shows what IS.
- **Credential in source.** Never paste a PAT into `index.html`; PAT usage is a per-deployer customization documented in the README.
- **Breaking the no-build promise.** If a change tempts you to add a bundler / framework, stop — instead render the dynamic bit via a Worker and keep `index.html` framework-free.
- **Skipping a11y.** The Command Center is the *first* place a researcher or auditor looks; a Low-finding here echoes across every adjacent claim.
- **Rewriting history.** This is a live page, not a ledger — but the repo it describes is append-only. Don't implement UI that implies "undo" of repo actions.

## Outputs

- Updated `command-center/index.html` (one file).
- Optional: CHANGELOG entry, README Identity bullet, SYSTEM-CARD §6 refresh.
- On deploy: GitHub Pages run success; site reachable.

## References

- `CONSTITUTION.md` Schedule A — the source-of-truth list.
- `TRUST.md` §2 and §3 — commitments and scorecard procedure.
- `RHYTHM.md` — cadence definitions.
- `GOVERNANCE.md` — blocking vs. informing chiefs.
- WCAG 2.2 AA — accessibility criteria.
- GitHub REST API v3 — `/repos/{owner}/{repo}`, `/commits`, `/contents/{path}`.
- GitHub Pages: `actions/deploy-pages@v4` workflow pattern.
- Cloudflare Pages static-site deploy pattern.
