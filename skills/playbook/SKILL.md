---
name: playbook
description: This skill should be used whenever a red-team finding has been remediated and needs to become a durable stepping stone, or whenever a prompt-upgrade to `agents/*.md` or a high-leverage `skills/*/SKILL.md` needs to be reviewed against the archived stones, or whenever the archive needs a roll-up review. The playbook skill owns `_vision/playbooks/ARCHIVE.md` (index) and `_vision/playbooks/stones/*.md` (individual stepping stones). Every stone is derived from one remediated finding, links to an ADR, and encodes both the attack pattern and the defense. Stones are immutable once archived; improvements supersede by linking. Trigger phrases include "archive this stone", "stepping stone for X", "review the prompt diff", "playbook update", "roll up the playbook archive".
metadata:
  version: "0.3.0-alpha.6"
---

# playbook — durable archive of what stopped working

The DGM (Darwin Gödel Machine) pattern, applied to an agency: every successful defense becomes a permanent stepping stone. Future iterations inherit the hardening without needing to rediscover it. The archive is append-only; stones are immutable; supersession links preserve history.

## Invariants

1. Every stone is derived from a remediated `high`+ red-team finding.
2. Every stone links to an ADR (the remediation ADR, at minimum).
3. Every stone has a paired regression eval item (in `skills/eval`).
4. Stones are immutable once archived. Rewriting = memory poisoning candidate.
5. Improvements are new stones that link back to the one they supersede.
6. Every prompt-upgrade to `agents/*.md` or high-leverage skills runs the stone review (via `skills/red-team/references/prompt-diff-review.md`).
7. `_vision/playbooks/ARCHIVE.md` is alphabetical by slug + always current.

## Artifacts

```
_vision/playbooks/
  ARCHIVE.md                  ← alphabetical index
  stones/
    stone-NNNN-<slug>.md      ← individual stones
```

## Stone shape

```yaml
---
id: stone-NNNN
created: <yyyy-mm-dd>
adr: ADR-NNNN-<slug>
source:
  finding: <slug>/red-team/findings.md#rt-NNNN
  session: _sessions/<agent>/<sid>.jsonl
asi_categories: [ASI06, ASI07]
severity_original: high
owners:
  found_by: <specialist>
  remediated_by: <chief-or-specialist>
  hardened_skill: skills/<slug>/SKILL.md    # or agents/<name>.md or a council slug
superseded_by: null                          # if and when a new stone replaces this
supersedes: null                             # link back if this one supersedes a prior
review_cadence: quarterly | pre-release | on-prompt-upgrade
---

## Pattern
<3-5 bullets describing the attack class, abstract — not instance-specific>

## Defense
<3-5 bullets describing what was changed + why>

## Regression test
<pointer to eval item id + file, e.g. `<slug>/eval/eval-set.md#eval-rt-NNNN`>

## Review cadence
<one line: when to re-evaluate>
```

## Processes

### Author a new stone

1. Triggered when CRT marks a finding `remediated: true` in `<slug>/red-team/findings.md`.
2. `playbook-author` reads the finding, the reproduction, the ADR, the remediation diff.
3. Draft the stone. `## Pattern` must be attack-class level, not instance-specific. If a future attacker would need only cosmetic variation to evade the stone, the pattern is too narrow — widen it.
4. Link to the regression eval item. If none exists, file a taskflow task on CEVO (`eval-designer`) to add one before archiving.
5. Append a row to `_vision/playbooks/ARCHIVE.md` (alphabetical by slug).
6. File the supersession-link ADR if this stone replaces an earlier one.

### Review a prompt diff

See `skills/red-team/references/prompt-diff-review.md`. Summary:

1. Playbook-author pulls the diff.
2. Greps ARCHIVE.md for applicable stones.
3. For each stone, verifies the diff doesn't remove `## Defense` language or re-enable `## Pattern` behavior.
4. REJECT if any stone regressed. APPROVE silently otherwise.
5. Appends to `_sessions/playbook-author/<sid>.jsonl`.

### Roll up the archive (quarterly)

1. Triggered with the quarter roll-up (`skills/okr` rollup + portfolio audit + portfolio regression).
2. Playbook-author reads every stone.
3. For each stone, check: does the regression eval item still exist? Has it been run in the last quarter's sweep? Did the paired CAO audit find the linked ADR intact?
4. Stones failing any check get a taskflow task: re-link, re-run, or supersede.
5. Produce `_vision/playbooks/<quarter>-review.md` with counts + failures + next-quarter watchlist.

### Supersession

- New stone cites the old in `supersedes:`.
- Old stone gets `superseded_by:` updated — this is the only allowed edit to a prior stone, and it's a single-field pointer, not a content edit.
- Both the supersedes entry and the superseded_by edit file ADRs.

## Integration

- **`skills/red-team`** — findings → stone pipeline.
- **`skills/adr`** — every stone links to an ADR; every stone authored or superseded files an ADR.
- **`skills/eval`** — every stone has a paired regression eval item derived from the stone's `## Regression test`.
- **`skills/audit`** — CAO cross-checks stone ↔ ADR linkage; stones without a linked ADR = audit red.
- **`skills/roster`** + **`skills/skill-creator`** — every prompt upgrade runs stone review BEFORE the change lands.
- **`skills/memory`** — `model-poisoning-scout` watches for stone rewrites (they're never legitimate).

## Progressive disclosure

- `references/stone-authoring.md` — detailed rules for writing `## Pattern` and `## Defense` at the right abstraction.
- `references/supersession-rules.md` — when to supersede vs augment vs deprecate.
- `references/archive-format.md` — ARCHIVE.md table format + sort rules.

## Anti-patterns

- Writing an instance-specific stone ("block the exact string 'ignore previous'"). Abstract to the class.
- Authoring a stone without a linked ADR.
- Editing an archived stone's body content. Always supersede.
- Skipping the prompt-diff review because "the change is small".
- Using the archive as a generic playbook library. Stones are adversarial-defense specific; general playbooks live elsewhere.
- Letting a stone live without a regression eval item for > 1 quarter.
