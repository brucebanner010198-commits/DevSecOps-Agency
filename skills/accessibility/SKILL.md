---
name: accessibility
description: >
  Audit any public-facing UI, document, or deliverable against WCAG 2.2 AA
  + ADA Title III + EN 301 549 + Section 508.  Produces a pass/fail report
  with ranked findings and fix-guidance.  Also applies to markdown, PDFs,
  videos, and API error messages consumed by humans.  Trigger phrases
  include "accessibility review", "WCAG check", "ADA", "a11y", "screen
  reader", "contrast check", "alt text", "keyboard navigation", "508", or
  any /devsecops-agency:accessibility invocation.  Auto-triggered on any
  artifact marked public-facing in the project ADR.
metadata:
  version: "1.0.0"
---

# accessibility — A11y audit (WCAG 2.2 AA + ADA + Section 508 + EN 301 549)

Authority: [`CONSTITUTION.md`](../../CONSTITUTION.md) + [`VALUES.md`](../../VALUES.md) (universal usability)
Owner: CEVO (today) → CA11y (v0.7.0) · Reviewer: CAO
Called from: `skills/ship-it-kickoff`, `skills/eval`

## When to trigger

REQUIRED for:
- Any public-facing UI, web page, or web app.
- Any document delivered to an end user (PDF, DOCX, markdown).
- Any video or audio deliverable.
- Any API error message or on-screen text that the user reads.
- Any UI the User will present to a third party.

## Standards crosswalk

| Region / standard | Level targeted |
|---|---|
| WCAG 2.2 | AA (mandatory) |
| ADA Title III (US) | Court-accepted proxy = WCAG 2.1+ AA |
| Section 508 (US federal) | WCAG 2.0 AA + specific §1194 sections |
| EN 301 549 (EU) | WCAG 2.1 AA + specific clauses |
| ARIA Authoring Practices | Followed for interactive widgets |

We target **WCAG 2.2 AA** as the baseline because it subsumes the stricter parts of most regional requirements.

## Procedure

### Step 1 — Scope the audit

List the artifact + every interactive state (default, hover, focus, pressed, disabled, error) and every responsive breakpoint (mobile, tablet, desktop).

Note content types: text, image, video (with/without captions), audio, form, interactive widget (menu, dialog, carousel, etc.), data table, chart.

### Step 2 — The four principles (POUR)

WCAG is organized under:

- **P — Perceivable** — users can perceive the content.
- **O — Operable** — users can operate the interface.
- **U — Understandable** — users can understand the content and interface.
- **R — Robust** — content works across assistive tech.

Walk each.

### Step 3 — Perceivable checks

| Check | WCAG SC | Method |
|---|---|---|
| Images have meaningful alt text (or alt="" if decorative) | 1.1.1 | Inspect each `<img>`, each SVG with role="img", each CSS background image with meaning |
| Video has captions | 1.2.2 | Confirm captions track exists + is accurate |
| Audio has transcript | 1.2.1 | Confirm linked transcript |
| Text contrast ≥ 4.5:1 (normal), 3:1 (large ≥ 18pt or bold 14pt) | 1.4.3 | Automated contrast checker; spot-check hover/focus states |
| UI component contrast ≥ 3:1 | 1.4.11 | Buttons, inputs, focus indicators vs adjacent background |
| Text is resizable to 200% without loss of content | 1.4.4 | Browser zoom test |
| Content reflows at 320 CSS pixels wide without horizontal scroll | 1.4.10 | Viewport test |
| Content does not rely on color alone | 1.4.1 | Review icons, status indicators, links |
| Spacing can be overridden without loss of content | 1.4.12 | CSS override test |

### Step 4 — Operable checks

| Check | WCAG SC | Method |
|---|---|---|
| All functionality available from keyboard | 2.1.1 | Unplug mouse; navigate fully |
| No keyboard trap | 2.1.2 | Tab through; verify can exit every widget |
| Skip link to main content | 2.4.1 | Tab from page top; expect "Skip to main" |
| Focus order is logical | 2.4.3 | Tab through; order follows visual flow |
| Focus indicator is visible | 2.4.7, 2.4.11 | Each focus state has ≥ 3:1 contrast indicator, not occluded |
| Target size ≥ 24×24 CSS pixels (WCAG 2.2) | 2.5.8 | Measure tap targets |
| No motion traps / no autoplay > 5 sec | 2.2.2 | Check for unstopped carousels, autoplay video |
| No seizure-risk flashing (> 3 Hz red) | 2.3.1 | Review any animation |
| Dragging has non-drag alternative (WCAG 2.2) | 2.5.7 | Click-based alternative for every drag |
| Consistent help location (WCAG 2.2) | 3.2.6 | Help widget is in the same place across pages |

### Step 5 — Understandable checks

| Check | WCAG SC | Method |
|---|---|---|
| Page has `<html lang=...>` | 3.1.1 | Inspect |
| Form inputs have labels | 3.3.2 | Every `<input>` has `<label for="...">` or aria-label |
| Errors are identified and described | 3.3.1, 3.3.3 | Submit invalid form; errors announced to screen readers |
| No unexpected context change on focus | 3.2.1 | Focus events don't navigate away |
| No unexpected context change on input | 3.2.2 | Typing or selecting doesn't auto-submit |
| Consistent navigation | 3.2.3 | Nav order is the same across pages |
| Authentication does not require cognitive test (WCAG 2.2) | 3.3.8 | No CAPTCHA that requires remembering sequences |

### Step 6 — Robust checks

| Check | WCAG SC | Method |
|---|---|---|
| Valid HTML (no duplicate IDs, proper nesting) | 4.1.1 (removed in 2.2 but still best practice) | Validator |
| Name, role, value programmatically determined | 4.1.2 | Inspect ARIA + native semantics |
| Status messages announced (aria-live) | 4.1.3 | Screen reader test on toasts, errors, loading states |

### Step 7 — Screen-reader test

Run the artifact with at least one screen reader:

- **NVDA** + Firefox (Windows) — free, most common baseline.
- **JAWS** + Chrome (Windows) — commercial; test if audience uses it.
- **VoiceOver** + Safari (macOS/iOS) — Apple users.
- **TalkBack** + Chrome (Android) — Android users.

Confirm:
- Page structure (headings in order, regions labeled).
- Every interactive element announces role + name + state.
- Live regions announce dynamic content.

### Step 8 — Document accessibility (PDF / DOCX / MD)

For documents:

- PDFs are tagged (PDF/UA-1 compliant preferred).
- Headings use heading styles, not bold text.
- Tables have header rows marked semantically.
- Alt text on every image.
- Reading order is explicit in the tagged structure.
- Markdown: heading hierarchy is correct (no skipping); images have alt text; link text is meaningful.

### Step 9 — Cognitive-load checks (beyond WCAG baseline)

- Plain-language test: reading grade level ≤ 8th grade for general audience (per Flesch-Kincaid).
- Error messages say what went wrong and how to fix it.
- Forms explain format requirements before submission, not after.
- No jargon without definition on first use.

### Step 10 — Ranked finding list

Report each finding with:

- **ID** (A11Y-YYYY-MM-DD-N)
- **Severity** — Critical (blocks use) / High (makes use much harder) / Medium (friction) / Low (polish)
- **WCAG SC** — the success criterion violated.
- **Evidence** — screenshot / quoted text / reproducer.
- **User impact** — which user group is affected (blind, low-vision, motor, cognitive, deaf).
- **Fix guidance** — concrete remediation.

### Step 11 — Sign-off

- **Critical findings: 0** required for ship.
- **High findings: 0** required for public launch; waiver acceptable (90 days) for internal or beta.
- **Medium / Low: tracked** in the backlog.

## Automated tools (complement, do not replace, manual audit)

- axe-core / axe DevTools.
- Pa11y.
- WAVE.
- Lighthouse (Accessibility section).

**Automated tools catch ~30-40% of WCAG violations.** The remainder is manual: screen reader, keyboard, and cognitive evaluation.

## Anti-patterns

- **"Aria-labels fix everything."** No. Semantics first; aria-labels only when native semantics are insufficient. Over-use of ARIA is worse than none.
- **"Automated scan passed, we're done."** See above.
- **Accessibility overlay widgets.** Don't. They regress usability for screen-reader users and are legally unreliable.
- **Testing only on desktop Chrome.** Most a11y bugs appear on mobile + assistive tech + high zoom.
- **Treating a11y as launch-gate only.** By then it's expensive. Ship checks integrate from design phase.

## Outputs

- Accessibility Audit Report attached to the project ADR.
- Ranked finding list with IDs.
- Remediation PRs (one per High finding).
- LESSONS row if a systemic pattern was discovered.

## References (original synthesis)

- W3C WCAG 2.2 Recommendation (W3C, 2023).
- ARIA Authoring Practices Guide (W3C).
- ADA Title III standards — DOJ NPRM 2024.
- Section 508 standards (Revised 2017).
- EN 301 549 v3.2.1 (2021-03).
- WebAIM, *Screen Reader User Survey #10* — baseline of real-user behavior.
