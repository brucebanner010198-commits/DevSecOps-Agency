# prompt-diff-review — stone-matching + reject criteria for prompt upgrades

Every mutation to `agents/*.md` or a high-leverage `skills/*/SKILL.md` runs through this review BEFORE it lands.

## Triggers

- `skill-creator` proposes a change to `agents/<name>.md`.
- Any ADR with trigger `agents/<name>.md prompt edit` or `skills/<slug>/SKILL.md edit` is in flight.
- `skills/roster` hire / repurpose / prompt-upgrade (the new or edited prompt is reviewed).
- CEO dispatches red-team-lead with context "prompt-upgrade red-team".

## Process

1. Read the two versions of the target file: current (on disk) and proposed (from the `skill-creator` output or ADR).
2. Compute the diff — added / removed / changed lines.
3. Grep `_vision/playbooks/ARCHIVE.md` for any stone whose `hardened_skill` field matches the file being edited (or the file's council, for council-level stones).
4. For each matching stone:
   a. Read `## Pattern` — the attack class being defended against.
   b. Read `## Defense` — the specific language / rule / invariant that hardens against it.
   c. Check the diff: does it remove the defense? Does it weaken phrasing (imperative → permissive)? Does it change a `Never` to a `Should not`? Does it remove a citation that grounded the defense?
   d. If the answer to any of these is yes → **REJECT**.
5. Run `adversarial-prompter` against the proposed version in isolation (no other changes applied). If the prompter lands a reproduction that exploits the change → **REJECT**.
6. If neither check rejects → **APPROVE**. Write an `[approve]` entry to `_sessions/playbook-author/<sid>.jsonl` citing the stones reviewed.

## Reject reasons → ADR body

An `[ADR] reject: prompt upgrade` record must include:

- The file being changed + proposed diff (quote the offending change).
- The stone(s) the change regresses (link + line).
- The specific attack the stone defends against.
- Either: `auto-rollback` (the change never lands) OR `override-required` (user must accept the regression via Rung 6).

Overrides are rare — a prompt upgrade that intentionally removes a stone defense must cite a superseding stone or explain the attack class is obsolete. Either way, ADR.

## Stone matching — strict rules

A stone matches a diff if ANY of:

- `hardened_skill: skills/<slug>/SKILL.md` exactly equals the file path.
- `hardened_skill: agents/<name>.md` exactly equals the file path.
- `hardened_skill: <council>` and the file is a Chief / specialist of that council.
- Any `asi_categories:` in the stone covers a surface the file touches.

False positives are preferable to false negatives. A spurious match costs one extra review turn; a missed match regresses a defense.

## Weakening phrasing patterns

Automatic reject candidates if the diff does any of these to a line inside an area a stone protects:

| Before              | After                | Weakening?              |
|---------------------|----------------------|-------------------------|
| Never do X          | Should not do X      | Yes                     |
| Never do X          | Avoid doing X        | Yes                     |
| Must do Y           | Should do Y          | Yes                     |
| Must cite source    | Ideally cite source  | Yes                     |
| Always …            | Typically …          | Yes                     |
| Required            | Recommended          | Yes                     |
| Forbidden           | Discouraged          | Yes                     |
| (imperative removed)| (imperative removed) | Yes                     |

Upgrades in the other direction (Should → Must) are fine and do not need stone review for hardening, but still need an ADR if the change is to `agents/*.md`.

## Scope

Prompt-diff review is scoped to files explicitly on the stone-tracked list. It does not run on:

- Reference files under `skills/<slug>/references/*.md` (unless a stone explicitly pins them).
- Documentation (`README.md`, `docs/*.md`).
- Data files (`_decisions/ADR-*.md` once accepted; those are immutable anyway).

## Output

```
artifact: _sessions/playbook-author/<sid>.jsonl (appended)
gate: n/a (rejects surface as blocking ADR; approves are silent)
note: "<approve | reject>: <N stones reviewed>"
citations: [stone paths, ...]
```
