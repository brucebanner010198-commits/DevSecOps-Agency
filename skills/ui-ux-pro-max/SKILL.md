---
name: ui-ux-pro-max
description: "Professional UI/UX design system generator for production-grade interfaces on web, mobile, and desktop. Use whenever the user mentions ui, ux, design, design system, landing page, dashboard, website, mobile app, web app, component, layout, color palette, typography, icons, or visual style, even if they only say 'ui' in passing. Also trigger on product requests (SaaS, fintech, healthcare, e-commerce, portfolio, gaming, admin panel), platform mentions (React, Next.js, Vue, SwiftUI, React Native, Flutter, Tailwind, shadcn), or asks to build, design, create, implement, review, fix, improve, or redesign any user-facing interface. Runs an intent-extraction loop; parses the ask, asks targeted follow-ups only when critical slots are missing, confirms, then generates a full design system (pattern, style, colors, typography, effects, anti-patterns, pre-delivery checklist) and hands off to frontend-design for code."
compatibility: "Requires Python 3.8+ on PATH (used by scripts/search.py). Works in any environment with shell/code execution."
---

# UI/UX Pro Max

Design intelligence for building professional UI/UX across platforms. Ported from `nextlevelbuilder/ui-ux-pro-max-skill` (MIT, v2.2.1). Includes 67 UI styles, 96 color palettes, 57 font pairings, 25 chart types, 16 stack guides, 99 UX rules, and a 100-rule reasoning engine. The skill composes these into a complete design system matched to the user's product, industry, audience, and mood.

---

## Mission

Turn a short user request ("build a landing page for a fintech banking app") into a complete, implementation-ready design system in as few exchanges as possible. The skill is **not** a chatbot that collects requirements line by line. It is an intent extractor that infers aggressively, asks only when a critical slot is empty, confirms once, and proceeds.

Output of every run:

1. **Pattern** (landing page structure, section order, CTA strategy)
2. **Style** (one of 67 UI styles, with keywords, performance, accessibility grade)
3. **Colors** (full token set: primary, secondary, accent, bg, fg, muted, border, destructive, ring)
4. **Typography** (heading/body font pairing with Google Fonts URL + CSS import)
5. **Effects** (motion, shadows, transitions)
6. **Anti-patterns** (explicit list of what to avoid for this industry)
7. **Pre-delivery checklist** (tailored to the stack and surface)

---

## Workflow

The skill runs in four phases. Do not skip phases. Do not reorder them.

### Phase 0: Intent extraction (REQUIRED, happens first)

Parse the user's request for six slots:

| Slot        | Critical? | Examples                                                             |
|-------------|-----------|----------------------------------------------------------------------|
| Target      | Yes       | landing page, dashboard, mobile app, web app, component, full app, redesign |
| Domain      | Yes*      | SaaS, fintech, healthcare, e-commerce, portfolio, gaming, crypto, beauty, wellness, admin, media, edtech, legal, real-estate, etc. |
| Audience    | No        | B2B enterprise, C-end consumer, developer, clinician, prosumer       |
| Mood        | No*       | minimal, premium, playful, brutalist, trustworthy, cyberpunk, calm   |
| Stack       | No        | React, Next.js, Vue, SwiftUI, Flutter, React Native, Tailwind, shadcn, HTML |
| Scope       | No        | design-system only, design + implementation, review existing UI, fix |

*One of Domain or Mood must be present. A strong Mood ("brutalist portfolio", "cyberpunk gaming site") can substitute for an unspecified Domain, and vice versa.

**Decision rules:**

- **Both critical slots present** → skip to confirmation. One-line restatement showing what was understood and the defaults applied. Ask "confirm or adjust?" Proceed on any affirmative.
- **One critical slot missing** → ask exactly one targeted question to fill it, then restate + confirm.
- **Both critical slots missing** → ask at most two questions in a single round (never more), then restate + confirm.
- **Never ask more than two questions in one round.** Sir's constraint: few inputs, best output.

**Defaults to apply silently (mention in confirmation so the user can override):**

- Stack → HTML + Tailwind for web, SwiftUI for iOS-only, Jetpack Compose for Android-only, React Native for cross-platform mobile
- Scope → design system + implementation
- Mode support → both light and dark
- Audience → C-end consumer unless Domain implies B2B (SaaS enterprise, admin panels, clinician tools)

**Confirmation format (use verbatim shape):**

```
Understood:
- Target: <target>
- Domain: <domain>
- Audience: <audience>
- Mood: <mood or "defer to domain rules">
- Stack: <stack (default: <x>)>
- Scope: <scope (default: design system + implementation)>

Generating design system now. Reply "adjust" to change any slot.
```

Do not wait for "yes" on unambiguous asks. Proceed unless the user says stop or adjusts.

### Phase 1: Generate the design system

Run the design system generator. This is a Python script that searches five domains in parallel, applies 100 reasoning rules, and produces a structured output.

```bash
python3 scripts/search.py "<domain> <mood> <keywords>" --design-system -p "<project name>" -f markdown
```

- Use `-f markdown` for easier downstream consumption (ASCII default is for terminals).
- `--persist` optionally writes `design-system/MASTER.md` for cross-session retrieval.
- Add `--page <name>` to also create a page-specific override file.

The query string should contain the domain, mood keywords, and any differentiators. Good queries: `"fintech banking dark mode trustworthy"`, `"beauty spa wellness calming premium"`, `"dev tool AI native cyberpunk"`. Weak queries: `"app"`, `"nice site"`.

### Phase 2: Supplement with targeted searches (only if needed)

After the design system is generated, run domain-specific searches for additional detail on any dimension that is unclear or needs deeper specification:

```bash
python3 scripts/search.py "<keyword>" --domain <domain> -n <n>
```

Available domains:

| Domain         | Use For                                                |
|----------------|--------------------------------------------------------|
| `product`      | Product-type pattern matching                          |
| `style`        | UI styles, prompts, CSS keywords                       |
| `color`        | Industry-specific palettes                             |
| `landing`      | Landing page structure + CTA strategy                  |
| `typography`   | Font pairings with Google Fonts imports                |
| `google-fonts` | Individual font metadata                               |
| `chart`        | Chart type recommendations for dashboards              |
| `ux`           | 99 UX guidelines + anti-patterns                       |
| `icons`        | Icon library recommendations                           |
| `react`        | React/Next.js performance patterns                     |
| `web`          | App interface accessibility (iOS/Android/RN)           |

Rule: run Phase 2 only when the Phase 1 output is insufficient for the user's goal. Do not pad the response with searches the user did not ask for.

### Phase 3: Stack-specific guidelines

If the user named a stack (or one was defaulted), pull implementation-specific rules:

```bash
python3 scripts/search.py "<topic>" --stack <stack>
```

Available stacks: `react`, `nextjs`, `vue`, `nuxtjs`, `nuxt-ui`, `svelte`, `astro`, `swiftui`, `react-native`, `flutter`, `html-tailwind`, `shadcn`, `jetpack-compose`, `threejs`, `angular`, `laravel`.

### Phase 4: Handoff to `frontend-design` for implementation (if scope includes code)

This skill produces the **design artifact**. It does not write production component code. When scope includes implementation:

1. Finalize the design system output from Phase 1.
2. Explicitly invoke `frontend-design` with the design system as input. Example framing: "Using this design system [tokens, typography, pattern], build the [component/page] in [stack]."
3. `frontend-design` handles layout, component structure, Tailwind classes, shadcn primitives, and responsive breakpoints.
4. After implementation, return to this skill's **pre-delivery checklist** (see `references/quick-reference.md`) to validate output before delivery.

If scope is design-system only, stop after Phase 1/2/3 and deliver the artifact.

---

## Persistence pattern (optional, for multi-session projects)

For projects spanning multiple sessions, persist the design system as markdown files:

```bash
# Global source of truth
python3 scripts/search.py "<query>" --design-system --persist -p "ProjectName"

# Page-specific override
python3 scripts/search.py "<query>" --design-system --persist -p "ProjectName" --page "checkout"
```

Output structure:

```
design-system/
  projectname/
    MASTER.md              # colors, typography, spacing, components
    pages/
      checkout.md          # overrides to MASTER for this page only
```

Retrieval order: page-specific override → MASTER. If the page file exists, its rules win.

---

## Quick reference (embedded)

A compressed quick-reference is available at `references/quick-reference.md`. Read it when:

- Doing a fast UI review ("is this good?") without running the full generator
- Resolving a specific issue (dark mode contrast, animation timing, touch targets, form UX)
- Running pre-delivery validation on a completed build

The quick-reference is organized by severity (CRITICAL → HIGH → MEDIUM) and by surface (icons, interaction, color, motion, forms, navigation, layout, accessibility).

---

## When NOT to use this skill

Trigger suppression matters as much as trigger expansion. Do **not** engage this skill for:

- Ubuntu/Linux UI scaling bugs or OS-level display issues (OS config, not design)
- CLI/terminal tool UX (different domain; use general engineering judgment)
- Pure backend API design (no user-facing surface)
- Naming variables/functions in code
- "UI tests" in the QA sense (unit/integration/e2e tests)

If the user asks about one of these and the word "UI" appears, acknowledge the linguistic overlap and proceed without loading the full design system engine.

---

## Example: end-to-end in one exchange

**User:** `build a landing page for a fintech banking app, dark theme, Next.js`

**Intent extraction:**
- Target: landing page ✓
- Domain: fintech (banking) ✓
- Mood: dark, trustworthy (inferred)
- Stack: Next.js ✓
- Audience: C-end consumer (default)
- Scope: design + implementation (default)

Both critical slots present. Skip to confirmation.

**Claude:**
```
Understood:
- Target: landing page
- Domain: fintech (banking)
- Audience: C-end consumer
- Mood: dark, trustworthy
- Stack: Next.js
- Scope: design system + implementation

Generating design system now. Reply "adjust" to change any slot.
```

Run:
```bash
python3 scripts/search.py "fintech banking dark trustworthy" --design-system -p "NeoBank" -f markdown
```

Output delivered. Hand off to `frontend-design` with the tokens.

---

## Example: ambiguous ask

**User:** `make me a ui`

**Intent extraction:**
- Target: unknown ✗
- Domain: unknown ✗
- Both critical slots missing → ask up to two questions.

**Claude:**
```
Two quick questions so I can match the right design system:

1. What are you building? (landing page / dashboard / mobile app / component / something else)
2. What's the product or industry? (SaaS, fintech, healthcare, portfolio, gaming, etc.)
```

Wait for reply, then parse, restate, confirm, proceed.

---

## Reference files

- `references/quick-reference.md` — Severity-ordered rule table for fast UI review and pre-delivery validation.
- `scripts/search.py` — CLI entry point. Always invoke from within the skill directory so paths resolve.
- `scripts/core.py` — BM25 search engine + domain/stack config.
- `scripts/design_system.py` — Reasoning engine that composes the design system output.
- `data/*.csv` — 12 domain CSVs.
- `data/stacks/*.csv` — 16 stack-specific CSVs.

## Notes for coordinating with other skills

- **`frontend-design`**: Use after Phase 1 completes. Pass the design system output as context.
- **`canvas-design`**, **`algorithmic-art`**: Not a handoff target. Those skills produce static visual art, not UIs.
- **`pptx` / `docx`**: If the user wants a design-system spec as a document deliverable, invoke after Phase 1 with the markdown output as source.
