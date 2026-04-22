# Contributing to DevSecOps-Agency

**Version:** 1.0
**Ratified:** 2026-04-22
**Plugin version:** v0.5.0
**Authority:** [`CONSTITUTION.md`](CONSTITUTION.md), [`GOVERNANCE.md`](GOVERNANCE.md), [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)

---

## 0. Before you contribute — read this first

DevSecOps-Agency is a **governed** project. That means:

- All founding documents are subordinate to [`CONSTITUTION.md`](CONSTITUTION.md).
- Certain actions are **USER-ONLY** (see Constitution §2.2). Contributors do not take these actions; they propose them via issues or PRs.
- Certain classes are **non-waivable** (raw secrets, ASI-class per Constitution §8.5). Contributions that weaken these are rejected on sight.
- All work produces **receipts** — session logs, ADRs, LESSONS rows. Contributions include their governance trail.

If this seems heavy for your use case, that is working as intended. The project optimizes for trust and traceability, not velocity.

---

## 1. How to contribute

We welcome the following kinds of contributions, roughly in order of the path of least friction:

1. **Bug reports** — file a GitHub issue. Security bugs go through [`SECURITY.md`](SECURITY.md) §3, not public issues.
2. **Documentation improvements** — typo fixes, clarification, examples. Usually merges quickly.
3. **New skills** (additions under `skills/*/`) — follow §4 below.
4. **New council roles or council changes** — follow §5 below. These have higher review gates.
5. **Changes to founding documents** (Constitution, Mission, Values, Security, etc.) — follow §6 below. These are amendment-class and rare.

Please do **not** open large PRs without first opening an issue to discuss scope. We prefer to converge on design before you write code.

---

## 2. Prerequisites

- GitHub account.
- Git ≥ 2.25.
- A working Claude Code installation to test skills and councils.
- Familiarity with [`CONSTITUTION.md`](CONSTITUTION.md), [`VALUES.md`](VALUES.md), and [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

---

## 3. Contribution workflow

1. **Open an issue first** for anything non-trivial. Describe the problem and proposed direction.
2. **Fork the repo**, create a topic branch: `feature/<short-description>` or `fix/<short-description>`.
3. **Make your changes.** Run any hooks locally:
   ```bash
   bash runtime-hooks/secrets-scanner/check.sh
   bash runtime-hooks/commit-gate.sh
   ```
4. **Commit with the Co-Authored-By trailer** if Claude helped:
   ```
   Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
   ```
5. **Open a pull request** against `main`. Link the issue. Describe what changed and why.
6. **Respond to review.** Expect prompt-diff review on any persona/skill edit; CAO review on any governance edit; CISO/CRT review on any security-adjacent edit.
7. **Squash-merge after approval.** The PR author keeps the Co-Authored-By attribution.

---

## 4. Adding a skill

A skill lives at `skills/<name>/SKILL.md` and follows this shape:

```markdown
---
name: <kebab-case-name>
description: <one-sentence trigger + scope>
---

# <Title>

## When to use
...

## Procedure
1. ...
2. ...

## Outputs
...

## References
...
```

**Review gates:**

- Prompt-diff council (councils/prompt-reviewer).
- CEVO checklist — verify the skill has clear inputs, outputs, and a test procedure.
- CTE — verify it fits the existing skill catalog (no redundancy with existing skills).

**Constitutional note:** any skill that touches credentials **must** use vault-refs and cite [`CONSTITUTION.md`](CONSTITUTION.md) §8.5.

---

## 5. Adding or changing a council

A council change is heavier than a skill change because it redefines who can veto, escalate, or advise.

**Required artifacts:**

- `councils/<name>/AGENTS.md` — role definition, responsibilities, scope, invocation pattern.
- An ADR under `adrs/` explaining why this council exists and how it relates to existing councils.
- Update to [`AGENTS.md`](AGENTS.md) (root) listing the new council.
- If the council has a blocking veto, update [`CONSTITUTION.md`](CONSTITUTION.md) §3 (Councils and Vetoes).

**Review gates:** CGov + CAO + CEVO, then USER approval for the Constitution edit.

---

## 6. Amending a founding document

Founding documents include: [`CONSTITUTION.md`](CONSTITUTION.md), [`MISSION.md`](MISSION.md), [`VALUES.md`](VALUES.md), [`GOVERNANCE.md`](GOVERNANCE.md), [`SECURITY.md`](SECURITY.md), [`TRUST.md`](TRUST.md), [`RESILIENCE.md`](RESILIENCE.md), [`RHYTHM.md`](RHYTHM.md), [`CAREER.md`](CAREER.md), [`KEEPER-TEST.md`](KEEPER-TEST.md), [`SYSTEM-CARD.md`](SYSTEM-CARD.md), [`SWOT.md`](SWOT.md), [`THREAT-MODEL.md`](THREAT-MODEL.md), [`DISASTER-RECOVERY.md`](DISASTER-RECOVERY.md).

**Procedure:**

1. Open an issue titled `amendment: <document> — <one-line reason>`.
2. Draft the change as a PR.
3. Attach an ADR under `adrs/` citing the reason, cost, benefit, and affected controls.
4. Receive CAO review (audit), CGov review (governance), and any domain-council review (e.g., CISO for SECURITY.md).
5. **USER approval** is required for ratification. Constitutional amendments additionally require a 7-day cooling-off period (v0.6.0 rule) and CAO concurrence.
6. Update Constitution Schedule A if a new founding document is added.
7. Prepend CHANGELOG.md entry.

**Non-waivable classes cannot be amended without a new Constitutional version.** See Constitution §8.5.

---

## 7. Commit and PR style

- **Subject line:** ≤ 72 characters, imperative mood: "Add privacy skill", not "Added privacy skill" or "Adding privacy skill".
- **Body:** explain *why*, not *what* (the diff shows what).
- **Trailer:** include `Co-Authored-By: Claude ... <noreply@anthropic.com>` when Claude assisted. This is non-authoritative — accountability lives with the PR author.
- **PR title:** same style as commit subject.
- **PR description:** link the issue; describe risk; describe how you tested; list affected councils and reviewers.

---

## 8. Testing

- Every skill should include at least one worked example or test vector in its SKILL.md.
- Runtime hook changes must pass `bash runtime-hooks/<hook-name>/test.sh` if a test exists, otherwise include a sample session where the hook fires as expected.
- Founding-document changes should include a citation trail showing the change preserves or strengthens (never weakens) the non-waivable classes and USER-ONLY list.

CI automation (v0.6.0 target) will run hooks on every PR.

---

## 9. Licensing of contributions

By submitting a contribution, you agree that your contribution is licensed under the [MIT license](LICENSES/README.md) of this repository.

You also agree that your contribution does not violate any third-party license or copyright.

---

## 10. Getting help

- **General questions:** open a GitHub discussion or issue.
- **Security questions:** follow [`SECURITY.md`](SECURITY.md).
- **Code of conduct concerns:** contact brucebanner010198@gmail.com (enforcement contact in [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)).

---

## 11. Credits

Contributors who are merged into `main` are credited in the relevant ADR and in the CHANGELOG entry for the release that includes their change.

---

## 12. Document control

- **File:** `CONTRIBUTING.md`
- **Version:** 1.0
- **Owner:** CGov
- **Reviewer:** CAO
