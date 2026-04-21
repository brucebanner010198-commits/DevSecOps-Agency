# retrieval — grep-first read recipes

No embeddings in v0.1. Pure `rg`/`grep` + deterministic ordering. If this proves too shallow, upgrade to SQLite-vec later (openclaw parity).

## The 4-step read path (project init)

Always run these in order. Budget: ≤ 8 tool calls, ≤ 5k tokens.

### 1. Read MEMORY.md

```
Read _memory/MEMORY.md
```

If it's > 200 lines, read only the `Preferences (from user)` and `Recurring risks` sections first; fetch others on demand.

### 2. Keyword scan for related projects

Pull 3–5 keywords from the user's idea (nouns and domain words, drop filler). Example: idea = `"invoice-splitting web app for roommates"` → keywords = `invoice`, `split`, `roommate`, `expense`.

```
rg -li '<keyword>' _memory/patterns/
```

Take the union of files matching any keyword. Cap at 5 files.

### 3. Headers only

For each matched project file, read only the section headers plus the first line under each:

```
rg -n '^##' _memory/patterns/<match>.md
```

If a section looks directly relevant (e.g., `## Reusable decisions` when the user's idea overlaps), read that section in full. Otherwise skip.

### 4. Inject into brief.md

Add this section to `brief.md` after `## Idea`:

```markdown
## Prior learnings

From `_memory/patterns/<match>.md`:
- <bullet> (source line)
- <bullet> (source line)

From `_memory/MEMORY.md`:
- <bullet>
```

Cap at 6 bullets total. If none apply, write `## Prior learnings\n\n_(no relevant prior projects)_` — the presence of the section tells the Chiefs it was checked.

## Per-Chief targeted reads

Chiefs can read memory directly when needed. Recommended queries by Chief:

| Chief       | Query                                                                          |
| ----------- | ------------------------------------------------------------------------------ |
| CRO         | `rg -li '<domain word>' _memory/patterns/` → `## What shipped` + `## What was gated` sections |
| CPO         | `rg -li 'wedge\|positioning' _memory/patterns/` for positioning precedents   |
| CTO         | `rg -li '<tech stack>' _memory/patterns/` → `## Reusable decisions`          |
| CISO        | `rg -li '<threat vector>\|STRIDE' _memory/patterns/` + `MEMORY.md > ## Recurring risks` |
| VP-Eng      | `rg -li '<framework>' _memory/patterns/` → `## What worked`                  |
| CQO         | `rg -li 'flaky\|perf\|a11y' _memory/patterns/` → `## Recurring risks`        |
| VP-Ops      | `rg -li 'deploy\|rollback' _memory/patterns/` → `## What worked`             |
| CKO         | `rg -li 'tutorial\|readme' _memory/patterns/` for doc patterns               |
| GC          | `rg -li 'license\|privacy\|GDPR\|CCPA' _memory/patterns/ _memory/MEMORY.md`  |

A Chief who reads memory must cite it in their report to the CEO, e.g. `"Prior: patterns/invoice-splitter.md:42 noted Stripe webhook replay risk — mitigation carried forward."`

## What NOT to do

- Do not read every `patterns/*.md` file. Keyword-gate.
- Do not inject full paragraphs into the brief. Bullets only, with citations.
- Do not write from the read path. Reads must not mutate `_memory/`.
- Do not silently import prior decisions as gospel. Prior learnings are inputs; the current project's Chiefs still have to make their own call and may disagree. Log disagreements as `[correction of <date>]` in the next Light dream.

## Index file shape

`_memory/index.json` is a small cache to make keyword scans faster:

```json
{
  "version": "0.1",
  "lastUpdated": "<iso>",
  "lastRem": "<iso or null>",
  "projects": [
    {"slug": "invoice-splitter", "closedAt": "<iso>", "keywords": ["invoice","split","roommate","stripe","expense"], "health": 1.0}
  ],
  "byAgent": {
    "market-researcher": {"projectCount": 4, "sessionCount": 11}
  }
}
```

Refreshed at end of Deep dreaming and end of REM. Do not hand-edit.
