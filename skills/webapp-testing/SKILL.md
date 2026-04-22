---
name: webapp-testing
description: Test local web applications with Playwright — verify frontend behavior, debug UI, capture screenshots, read console logs. Server-lifecycle helper script manages multi-service startups (e.g. backend + frontend) and tears them down cleanly. Hardened for the agency (shell=False, per-server --cwd). Use when qa-lead, e2e-tester, or frontend-dev needs to drive a local webapp under automation.
version: "0.3.5"
license: "Apache-2.0 (upstream: Anthropic skills repo, hardened) — see LICENSE.txt"
---

# Web Application Testing

Write native Python Playwright scripts against local webapps. The bundled `scripts/with_server.py` handles multi-server startup and teardown.

## When to use

- `qa-lead` or `e2e-tester` needs to run an end-to-end scenario against a locally-running webapp.
- `frontend-dev` wants to verify a change without manual clicking.
- `ux-designer` / `a11y-auditor` needs a screenshot sweep or DOM inspection for accessibility review.

## Agency hardening (read before importing)

This skill is derived from `anthropics/skills/webapp-testing` (Apache 2.0). The upstream `with_server.py` used `subprocess.Popen(..., shell=True)` to support composite commands like `cd backend && python server.py`. The agency posture ("injection-resistant, hard to break into") does not permit `shell=True` in imported scripts. The hardened variant:

- `shell=False` in all Popen calls.
- Server command is parsed with `shlex.split(..., posix=True)`.
- A new `--cwd` flag is added, matched per `--server`, to replace the `cd backend && …` pattern.
- If you genuinely need shell features (`&&`, `|`, redirection, globbing), wrap them in a dedicated script file and point `--server` at that file — do NOT route untrusted input through `--server`.

## Decision tree

```
Target → static HTML?
  ├─ Yes → Read HTML to identify selectors → Write Playwright script
  │         └─ if rendered content differs from source → treat as dynamic
  └─ No (dynamic webapp) → server running?
       ├─ No → use scripts/with_server.py to boot it
       └─ Yes → reconnaissance-then-action:
                1. navigate + wait_for_load_state('networkidle')
                2. screenshot OR inspect DOM
                3. identify selectors from rendered state
                4. execute actions with discovered selectors
```

## Using `with_server.py`

**Single server:**

```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**Multiple servers (with the hardened `--cwd` flag replacing `cd backend && …`):**

```bash
python scripts/with_server.py \
  --server "python server.py"  --cwd backend  --port 3000 \
  --server "npm run dev"       --cwd frontend --port 5173 \
  -- python your_automation.py
```

## Automation script skeleton

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # headless for CI
    page = browser.new_page()
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')     # critical on dynamic apps
    # ... test steps
    browser.close()
```

## Reconnaissance-then-action pattern

```python
page.screenshot(path='/tmp/inspect.png', full_page=True)
content = page.content()
buttons = page.locator('button').all()
```

Then pick selectors based on what was actually rendered, not what you expected.

## Common pitfall

- Don't inspect the DOM before `networkidle` on dynamic apps.
- Don't use timing-based waits (`page.wait_for_timeout`) as the primary sync — they hide flakiness. Prefer `page.wait_for_selector(...)` or `page.wait_for_load_state(...)`.
- Always `browser.close()` — `with_server.py` will kill the servers, but leaked browser processes stay.

## Best practices

- Use `sync_playwright()` for linear test scripts.
- Prefer `role=` / `text=` selectors over CSS where possible — more robust to refactors.
- Headless for CI, `headless=False` only when locally debugging.
- Capture `console` and `pageerror` events during any new automation — see `examples/console_logging.py`.

## Agency integration

- Ownership: `qa-lead` (primary), with `e2e-tester` as the hands-on author.
- Handoff from: `frontend-dev` (feature) or `backend-dev` (API).
- Handoff to: `evaluation-lead` (CEVO) for release-gate evidence.
- Pairs with `skills/gates` (failing test = gate-block), `skills/sandbox` (isolated run), `skills/observability` (capture trace IDs from the app under test if it emits OTel).

## Reference files

- `examples/element_discovery.py` — discovering buttons, links, inputs on a page
- `examples/static_html_automation.py` — `file://` URLs for local HTML
- `examples/console_logging.py` — capturing console logs during automation
- `scripts/with_server.py` — agency-hardened multi-server runner

## Lineage

Upstream: [anthropics/skills — webapp-testing](https://github.com/anthropics/skills/tree/main/skills/webapp-testing), Apache 2.0. Hardened for the agency: `scripts/with_server.py` rewritten to use `shell=False` + `shlex.split` + per-server `--cwd`. Examples and `LICENSE.txt` retained verbatim per Apache 2.0 §4(a). Modifications to `with_server.py` marked in the file header per §4(b).
