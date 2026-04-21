# supersession-rules — when to supersede vs augment vs deprecate

Stones are immutable. Change happens via supersession.

## Supersede

**Use when:** the new stone covers the same attack class but with stronger / broader / more-specific defense, and the old stone's defense is no longer accurate.

**Process.**

1. Author the new stone. `supersedes: stone-NNNN`.
2. The new stone's `## Pattern` must cover everything the old one covered (plus any expansion).
3. Edit the single field `superseded_by:` on the old stone — this is the only allowed mutation to an archived stone.
4. File an ADR for both the new authoring + the supersession pointer edit.
5. ARCHIVE.md keeps both rows; the old one is marked `superseded`.

**Example triggers:**

- A newer ASI category covers the same attack class more precisely.
- The defense mechanism moved from one skill to another (stone's `hardened_skill` is now stale).
- The eval item covering this stone was rewritten and the old stone's pointer is dead.

## Augment (do not supersede)

**Use when:** the new stone covers a *different* attack class that happens to share a defense.

**Process.** Author the new stone independently. Cross-reference in `## Defense` but do not set `supersedes`.

**Example triggers:**

- The same `councils/security/AGENTS.md > ## Must not` line defends against two different attacks. Two stones, same quoted line.

## Deprecate

**Use when:** the attack class is obsolete (e.g., a framework deprecated the attack surface, a protocol was replaced).

**Process.**

1. File a deprecation ADR.
2. Author a new stone whose body explicitly marks the old stone `superseded` with justification "attack class obsolete: <reason>".
3. The deprecation stone has empty `## Regression test` + `review_cadence: annual (obsolescence-check)`.
4. Remove the old stone's eval item via taskflow task to CEVO.

Deprecation does **not** mean deleting the old stone. It stays in the archive, `superseded_by: <deprecation-stone>`.

## Rewrite (forbidden)

Never edit an archived stone's body. The only allowed mutation is the single `superseded_by:` pointer field.

Violations are caught by `model-poisoning-scout` (ASI01). Any `## Pattern` or `## Defense` change to an archived stone = poisoning finding + rollback.

## Roll-up review (quarterly)

Playbook-author checks each stone for:

- **Regression test liveness:** does the paired eval item exist + run in the last sweep?
- **ADR liveness:** does the cited ADR still exist and is it still in force?
- **Defense liveness:** does the cited file + section still exist? Has the line been weakened since the last review (patterns in `skills/red-team/references/prompt-diff-review.md > Weakening phrasing patterns`)?
- **Applicability:** does the stone still apply to any active surface?

**Failures:**

- Dead eval item → file taskflow task to CEVO.
- Weakened defense → file ADR + roll red-team prompt-diff review retroactively. If the weakening landed without review, this is a **critical** audit finding.
- Inapplicable → deprecate.
- Everything current → mark `last_verified: <quarter>` via a supersession stone (rare — most stones don't need this).

## Archive hygiene

- Keep ARCHIVE.md under 500 rows per quarter. If it grows beyond that, the roll-up spawns a portfolio-wide audit of superseded vs active stones; superseded ones more than 1 year old can be moved to `_vision/playbooks/_archive/<year>/stones/`.
- Move operations preserve the stone path in ARCHIVE.md; readers follow the redirect.
