# agent-browser patterns (reference)

Reference doc distilled from the MIT-licensed `agent-browser` skill in `qwibitai/nanoclaw@v1.2.53` (`container/skills/agent-browser/SKILL.md`, © 2026 Gavriel). Content rewritten for DevSecOps-Agency v0.3.6. This is **reference material for `webapp-testing`** — it is not a runnable skill in this plugin because the `agent-browser` CLI is an external binary the agency does not ship. Use these patterns when driving Playwright, the Claude-in-Chrome MCP, or any similar semantic-locator browser surface.

See `LICENSES/MIT-nanoclaw.txt` for attribution.

## Why these patterns matter

`agent-browser` is a CLI wrapper that exposes a browser as an accessibility-tree API. Its design is one of the cleanest examples of how an LLM should drive a browser, and the pattern generalizes:

- **Reconnaissance → action, not action-first.** Never click by coordinates. Always enumerate interactive elements first, then act on *stable references* to them.
- **Re-snapshot on navigation / significant DOM change.** Refs are only valid within a single snapshot.
- **Prefer semantic locators to CSS selectors.** `role=button name="Submit"` is robust across cosmetic changes; `.btn-primary.mt-2` is not.

These are the same principles `webapp-testing` (Playwright) encodes, and the Claude-in-Chrome MCP follows. Write tests and automation to the pattern, not to the library.

## Core workflow

```
1. Navigate                 agent-browser open <url>                | playwright: page.goto(url)
2. Snapshot (interactive)   agent-browser snapshot -i               | playwright: await page.locator('[role]').all()
3. Act on @e-refs           agent-browser click @e1                 | playwright: locator.click()
4. Re-snapshot if DOM moved agent-browser snapshot -i               | playwright: re-query
5. Close / teardown         agent-browser close                     | playwright: page.close()
```

Three mistakes this workflow prevents:

1. **Coordinate-based clicking** — brittle, breaks on any redesign. Always click by ref.
2. **Stale refs** — a ref from before navigation is not valid after. Always re-snapshot after `wait --url "**/…"` or `wait --load networkidle`.
3. **Over-filtering the snapshot** — a full snapshot is noisy; use `-i` (interactive only) plus optional `-s <selector>` scoping to keep context manageable.

## Semantic locator vocabulary

The upstream CLI exposes five stable locator axes. All five map directly to Playwright and to the Chrome MCP:

| Axis        | agent-browser                                     | Playwright                                      |
| ----------- | ------------------------------------------------- | ----------------------------------------------- |
| Role + name | `find role button click --name "Submit"`          | `page.getByRole('button', { name: 'Submit' })`  |
| Visible text | `find text "Sign In" click`                      | `page.getByText('Sign In')`                     |
| Form label  | `find label "Email" fill "a@b.com"`               | `page.getByLabel('Email')`                      |
| Placeholder | `find placeholder "Search" type "query"`          | `page.getByPlaceholder('Search')`               |
| Test id     | (n/a upstream — add `data-testid` + semantic-ref) | `page.getByTestId('submit-button')`             |

**Prefer role-or-label over text or placeholder.** Role/label survive copy-editing ("Sign In" → "Log In"); text/placeholder don't. Placeholder also disappears on focus in some frameworks.

**Avoid CSS selectors** (`.btn-primary`) except as a scoping hint (`snapshot -s "#main"`). They are the coordinate-clicks of locator design.

## Wait primitives

```
agent-browser wait @e1                     # wait for element to appear
agent-browser wait 2000                    # wait N ms (last resort)
agent-browser wait --text "Success"        # wait for text on page
agent-browser wait --url "**/dashboard"    # wait for URL pattern (glob)
agent-browser wait --load networkidle      # wait for network idle
```

Playwright equivalents: `locator.waitFor()`, `page.waitForTimeout()`, `page.waitForSelector(text=…)`, `page.waitForURL(…)`, `page.waitForLoadState('networkidle')`.

Rule: **never sleep** (`wait 2000`) unless you have explicitly ruled out a meaningful signal (URL change, text appearance, network idle). Time-based waits are the other common source of flake.

## Authenticated-state pattern

```
# Step 1 (once): log in and save state
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "username"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
agent-browser state save auth.json

# Step 2 (every run): load saved state, skip login
agent-browser state load auth.json
agent-browser open https://app.example.com/dashboard
```

Playwright equivalent: `context.storageState({ path: 'auth.json' })` → `browser.newContext({ storageState: 'auth.json' })`.

Two gotchas the upstream skill underspecifies:

- **Secrets in `auth.json`.** The saved state contains cookies and localStorage — a valid authentication token. Treat the file like a credential, not a fixture. Per container-isolation-posture rule 9, it should not be mounted into an agent container; load it from a vault path instead.
- **Expiry.** Saved state goes stale. Tests should either refresh on 401, or re-login in a fixture scoped appropriately (typically once per test-file).

## Data-extraction pattern

```
agent-browser open https://example.com/products
agent-browser snapshot -i
agent-browser get text @e1          # product title
agent-browser get attr @e2 href     # link URL
agent-browser get count ".item"     # count of matches
agent-browser screenshot products.png
```

Playwright equivalents: `locator.textContent()`, `locator.getAttribute('href')`, `locator.count()`, `page.screenshot({ path })`.

Rule: capture the screenshot at the end of a recon pass even if you don't need it — it's the cheapest piece of evidence for why an assertion failed later.

## Anti-patterns (from the upstream skill plus agency-specific findings)

1. **Clicking without a snapshot.** There is no stable identity for an element outside of a recent snapshot. Always `snapshot -i` first.
2. **Snapshotting too broadly.** A 500-node tree dumps 20k of tokens. Scope with `-s` or use `-i` + `-d` to limit depth.
3. **Stale refs after navigation.** Refs die on URL change, route change in SPAs, and any DOM mount/unmount. Re-snapshot.
4. **Shell-injection via `--server` / CLI args.** Already addressed in the agency's hardened `with_server.py` (`shlex.split(posix=True)` + `shell=False` + per-server `--cwd`). Don't regress.
5. **Running under a real user account in production.** Always run in a dedicated least-privilege account with its own browser profile.
6. **No network isolation.** A headed test browser with the user's normal network can exfiltrate through a DNS lookup. Run under the same credential-vault pattern as container-isolation-posture rule 9.

## Mapping to the agency's stack

| Want to do this                        | Use in DevSecOps-Agency                          |
| -------------------------------------- | ------------------------------------------------ |
| Drive a web app end-to-end             | `webapp-testing` (Playwright + hardened with_server.py) |
| Drive a web app from this chat         | Claude-in-Chrome MCP (tools `mcp__claude-in-chrome__*`) |
| Write a test plan                      | `engineering:testing-strategy` + `webapp-testing` |
| Audit a flow for injection             | `injection-defense` + `red-team`                 |
| Run browser-driven agents in a sandbox | `sandbox` + `container-isolation-posture`        |

The `agent-browser` binary itself is **not** a dependency of this plugin; these patterns apply regardless of which browser driver you use. If a future wave ever adds `agent-browser` as a dependency, lineage + attribution are already set.
