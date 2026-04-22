# Command Center

A single-file operations console for the DevSecOps-Agency. Live org chart, councils, rhythm, trust commitments, recent commits, and a meeting launcher — all in one `index.html` that reads the repo through the public GitHub API.

## What it does

- **Org chart.** CEO + 16 councils. Tap a council for its roster. Blocking councils (CISO / CRT / CEVO / CAO) are flagged red.
- **Vital signs.** Councils, skills, agents, hooks, trust pledges, USER-ONLY actions — counted live from the repo.
- **Today's rhythm.** Daily / weekly / monthly / quarterly heartbeats with skill pointers.
- **Trust commitments.** The twelve TRUST.md pledges. Until the first scorecard publishes (2026-07-22) they display as "measurement pending."
- **Recent activity.** The last 20 commits to `main`, with rate-limit status.
- **Founding documents.** Every Schedule-A document linked to its source on `main`.
- **Meeting launcher.** Five action buttons — *Call a CEO meeting · Convene a council · Issue a new directive · Schedule a drill · Publish Trust Scorecard*. Each opens a modal with a pre-written prompt you can paste into Claude.

## Why a single file

No build step, no framework, no backend. `index.html` runs anywhere: GitHub Pages, Cloudflare Pages, Vercel, Netlify, `file://`, or a Cowork artifact. Tailwind ships from CDN. Vanilla JS. The GitHub API is the data source — the Agency's repo *is* its state, and the command center is a window onto that state.

## Hosting options

### 1. GitHub Pages (recommended first stop)

Free, tied to the repo, one commit away. The included workflow (`.github/workflows/pages.yml`) auto-deploys `command-center/` on every push to `main`.

**Enable once:**
1. On GitHub → **Settings → Pages**.
2. **Source:** *GitHub Actions*.
3. Push any commit to `main`. The workflow publishes the site.
4. URL: `https://brucebanner010198-commits.github.io/DevSecOps-Agency/`.

Pros: zero config, free forever, versioned with the repo.
Cons: public-only (needs a paid plan to gate), no server-side features.

### 2. Cloudflare Pages (recommended if you outgrow GitHub Pages)

Faster edge, free custom domain, adds Workers for serverless functions if you later want scheduled jobs or authenticated reads.

**One-time setup:**
1. Sign in at [pages.cloudflare.com](https://pages.cloudflare.com).
2. *Create project → Connect to Git* → pick this repo.
3. Build settings:
   - **Framework preset:** *None*
   - **Build command:** *(leave blank)*
   - **Build output directory:** `command-center`
4. Save. Cloudflare publishes to `<project>.pages.dev` and auto-redeploys on every `main` push.
5. (Optional) Attach a custom domain under *Custom domains*.

Pros: faster global CDN, custom domain free, can add Workers.
Cons: another vendor to manage.

### 3. Vercel or Netlify

Nearly identical to Cloudflare Pages. Same steps, different UI:

- **Vercel:** Import Git repo → Framework *Other* → Root directory `command-center` → Deploy.
- **Netlify:** New site from Git → Base directory `command-center` → Build command blank → Publish directory `command-center` → Deploy.

### 4. Cowork artifact (private daily driver)

Open the file directly in the Cowork sidebar via `mcp__cowork__create_artifact` — the Agency's existing `skills/command-center` skill already does this for per-project views. The site detects `window.cowork` and adapts.

### 5. Local file

`open command-center/index.html` in a browser works offline for read-only review. GitHub API calls will fail on `file://` origins that block CORS in some browsers; open it via any of the hosted options for full data.

## How fresh is the data

The page fetches on load and on the **Refresh** button — unauthenticated GitHub API allows **60 requests / hour / IP**. A full page load uses ~19 requests (repo meta + tags + commits + three directory listings + 16 council rosters). That leaves ~3 refreshes per hour per viewer. For higher volume, append a fine-grained PAT to requests (edit `index.html` → `Authorization: token <PAT>` header on each `fetch`) — 5,000 req/hour authenticated. Never commit a token to the repo.

## Customizing

- **Repo pointer.** At the top of the `<script>` block: `REPO_OWNER` and `REPO_NAME`.
- **Councils list.** `COUNCILS` array — slug, display name, chief code, blocking/informing role, introduction wave.
- **Rhythm entries.** `RHYTHM` array — four default heartbeats per RHYTHM.md.
- **Trust pledges.** `TRUST` array — mirrors TRUST.md §2.
- **Founding documents.** `DOCS` array — mirrors Constitution Schedule A.
- **Actions.** `ACTIONS` object — one entry per button; each has `title`, `lede`, and a `prompt` string.

## Accessibility

- WCAG 2.2 AA color contrast on every chip and body text.
- Full keyboard reach for every interactive element (buttons, `<details>` toggles, modal).
- Modal uses native `<dialog>` with `::backdrop` blur.
- No motion-intensive animation beyond a single `pulse` on live indicators; respects `prefers-reduced-motion` implicitly because all transitions are ≤ 500ms.

## Skill wiring

The sibling `skills/command-center-web` skill documents when this surface is updated — every minor version bump, every change to councils / rhythm / trust pledges, and any added Schedule-A document. See that SKILL.md for the procedure.

## Roadmap

- **v0.5.x:** static dashboard (this release).
- **v0.6.0:** council-meeting history feed (reads `_meetings/`), scorecard historical series (reads `_meetings/trust-scorecard-*.md`), waiver ledger panel.
- **v0.7.0:** auth'd mode via Cloudflare Worker — opens the command center to GitHub OIDC, adds write-through "issue a directive" that opens a PR.
- **v1.0.0:** public ship — custom domain, status-page widget, researcher credit hall-of-fame.

## License

Same as the rest of the repo.
