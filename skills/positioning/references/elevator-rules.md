# positioning — elevator pitch rules

30 words. Always. No exceptions.

## Format

```
For <audience> who <job-to-be-done>,
<product> is a <category>
that <primary benefit>,
unlike <alternative>.
```

Word count measured by whitespace split. Punctuation doesn't count. Hyphenated compounds count as one word ("zero-setup" = 1).

## Worked passes

- "For US dorm roommates who split shared expenses, dorm-splitter is a zero-setup expense tracker that clears balances in 30 seconds via your existing group chat, unlike Splitwise which needs 4 permissions and a new account." — 34 words · FAIL (over)
- "For dorm roommates splitting shared expenses, dorm-splitter clears balances in 30 seconds via your group chat — unlike Splitwise, which needs 4 permissions." — 24 words · PASS
- "For freelance designers juggling 5+ client invoices, Invoicer auto-sends reminders when invoices age past terms, unlike Bonsai which only surfaces late invoices." — 22 words · PASS

## Worked fails and fixes

### Fail: vague audience

"For people who want to split bills, dorm-splitter is fast and simple."
- No audience (too broad)
- No job-to-be-done
- No category
- No alternative
- FIX: name the segment ("US dorm roommates"), state the job ("split shared expenses"), cite the wedge ("zero-setup").

### Fail: superlative

"For startup founders, OpsBoard is the best operational dashboard, faster than anyone else."
- "Best" without citation
- "Faster than anyone else" without basis
- "Anyone else" is not an alternative
- FIX: "For early-stage SaaS founders tracking ops metrics, OpsBoard consolidates 6 tool dashboards into one view — unlike Notion boards, which require manual sync."

### Fail: feature listing

"FooApp has AI summaries, smart routing, and real-time sync, for teams."
- No audience
- No job
- Features ≠ benefits
- No category
- No alternative
- FIX: "For distributed product teams on Zoom, FooApp summarises 60-min meetings in 90 seconds — unlike Otter.ai, which requires a separate review step."

### Fail: novel category without coinage

"For knowledge workers, ThoughtGraph is a cognitive augmentation system that unifies second brains, PKMs, and note-taking into one paradigm."
- "Cognitive augmentation system" is jargon
- "Unifies second brains, PKMs, and note-taking into one paradigm" is category-soup
- FIX: Either coin a term explicitly ("ThoughtGraph is a new category we call Living Notes...") or map to an existing handle ("ThoughtGraph is an Obsidian-style note graph that auto-links...").

## Edge cases

- Two-audience products: pick the primary audience. If the product genuinely serves two equal audiences, you likely have two products. Flag to `cmo`.
- "Unlike" clause missing: acceptable if the product creates a new category and there is genuinely no alternative. Must be flagged `[new-category]` and justify in messaging hierarchy.
- Elevator requires technical term that is the product's reason-to-exist: allowed, but pair with a 10-word non-technical version for non-target-audience readers.

## Measurement

- Run `wc -w` in your head. Anything 28–32 is fine; 33+ is over; 27 or less may be too terse (double-check audience is specific).
- Count the 5 slots: audience · job · product · benefit · alternative. All 5 present = structurally sound, regardless of length.
