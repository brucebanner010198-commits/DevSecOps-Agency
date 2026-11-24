---
name: adopt
description: >
  This skill should be used when the Chairman hands the DevSecOps Agency an
  existing repository to take over, rather than a new idea. Trigger phrases
  include "take over this repo", "adopt this project", "here is my existing
  codebase", "map this repository", or /devsecops-agency:adopt. Runs adoption
  gate A from the alignment plan, steps 1 to 5: receive, map, baseline,
  reconstruct intent, report. It changes no code. It ends with an adoption
  report and waits for the Chairman's approval.
metadata:
  version: "0.1.0"
---

# adopt — take over an existing repository (gate A)

An existing repository enters through adoption, not through intake. **No code changes until the Chairman approves the adoption report.** This skill covers steps 1 to 5 of gate A. Step 6, approval, is the Chairman's. Change requests after approval are not part of this skill.

## Where it runs

Launch the agency **inside the repository's own folder** (`--agent devsecops-agency:ceo` with that folder as the working directory). The guard (B1) keeps every write inside the launch folder, so this is the only way the records can sit with the repository.

All records go in one folder inside the repository: `_agency/`. The guard's own receipts go in `.devsecops-agency/`. Neither is committed by this skill.

| Record | Written by |
| --- | --- |
| `_agency/project.md` | `ceo` |
| `_agency/chat.jsonl` | every chief (append-only) |
| `_agency/system-map.md` | `legacy-code-specialist`, through `engineering-lead` |
| `_agency/baseline/tests.md` | `test-runner`, through `qa-lead` |
| `_agency/baseline/threat-model.md` | `threat-modeler`, through `security-lead` |
| `_agency/baseline/security-scan.md` | `code-auditor`, through `security-lead` |
| `_agency/baseline/licenses.md` | `license-checker`, through `gc` |
| `_agency/baseline/environments.md` | `deployment-engineer`, through `devops-lead` |
| `_agency/spec-as-is.md` | `spec-writer`, through `pm-lead` |
| `_agency/baseline/integrity.md` | `test-runner`, through `qa-lead` (step 5) |
| `_agency/adoption-report.md` | `ceo` |

## The adoption brief

Every chief and specialist here has a normal process for building a product from nothing: designing tests, writing CI, writing `deploy/`, writing `threat-model.md` at the project root. **None of that runs during adoption.** Every dispatch in this skill starts with this brief, word for word. Each chief passes it unchanged to every specialist it dispatches.

```
ADOPTION MODE. This is an existing repository the agency did not write.
Do not follow your normal phase process. Do exactly the one task below.
Write only the one output file named below, under _agency/. Create, edit,
move or delete no other file, including tests, CI config, deploy files,
manifests, lockfiles and .gitignore. Make no branch, commit or push.
If a write you need is refused, return the full text of the file instead;
the agent that dispatched you writes it unchanged.
Pass this brief, word for word, to any agent you dispatch.
Task: <task>
Output file: <path>
```

## Steps

### 1. Receive (CEO)

1. Read the Chairman's instruction. Record the repository and the instruction in `_agency/project.md`. Read the commit id from `.git/HEAD` (and the ref file or `.git/packed-refs` entry it points to). Record it as the **adoption commit**.
2. Ask the Chairman for only the access the work needs, in one message:
   - **Running the repository's code on this machine.** This covers the existing tests and their dependency install (step 3), and dependency audit tools. Running someone else's code needs the Chairman's yes, because there is no OS sandbox on this machine yet.
   - Nothing else. Adoption needs no network access beyond package installs, and no secrets, deploys or pushes.
   - If the Chairman's instruction already answers this, do not ask again.
3. Record the answer in `_agency/project.md`. If the answer is no, every step that would run the repository's code records "not run: not authorised", and everything else proceeds.

### 2. Map (CTO)

Dispatch `devsecops-agency:engineering-lead` with the brief and the adoption commit.
- Task: map the repository.
- Output: `_agency/system-map.md`.

It dispatches `devsecops-agency:legacy-code-specialist` for the map. Then it has `devsecops-agency:system-architect` check the map against the repository, returning corrections as text and not writing `architecture.md`.

### 3. Baseline (in parallel, after the map)

Each chief gets the brief, with the task and output below.

- **`devsecops-agency:qa-lead` → `devsecops-agency:test-runner`.**
  - Task: run the existing test suite exactly as the repository's CI or README runs it, only if step 1 authorised it. Write no tests and no test scripts. Record the command, the counts of passed, failed and skipped tests, and the failing test names.
  - Output: `_agency/baseline/tests.md`.
  - **This baseline must hold:** a later change that breaks a test that passed here is a red.
- **`devsecops-agency:security-lead` → `devsecops-agency:threat-modeler`.**
  - Task: an as-built threat model from `_agency/system-map.md` and the code.
  - Output: `_agency/baseline/threat-model.md`.
- **`devsecops-agency:security-lead` → `devsecops-agency:code-auditor`.**
  - Task:
    - search the repository with Grep for committed secrets (keys, tokens, private keys, passwords in config), recorded by file and line and never by value;
    - run the dependency audit the stack offers (`npm audit --json`, `pip-audit`, or the like), only if step 1 authorised it.
  - Output: `_agency/baseline/security-scan.md`.
- **`devsecops-agency:gc` → `devsecops-agency:license-checker`.**
  - Task: the repository's own license, and each dependency's license from the manifests and lockfiles. The project license is whatever the repository states, not a default.
  - Output: `_agency/baseline/licenses.md`.
- **`devsecops-agency:devops-lead` → `devsecops-agency:deployment-engineer`.**
  - Task: document the environments and deploy targets that the repository's configuration names, by reading only. Deploy nothing, and write no `deploy/` files.
  - Output: `_agency/baseline/environments.md`.

### 4. Reconstruct intent (CPO)

Dispatch `devsecops-agency:pm-lead`, which dispatches `devsecops-agency:spec-writer`.
- Task: an as-is specification: what the product does today, from the code and its documents, as features with the evidence path for each. Everything that could not be determined is listed as a question, not guessed. Success metrics are out of scope.
- Output: `_agency/spec-as-is.md`.

### 5. Integrity check, then report (CEO)

1. Dispatch `devsecops-agency:qa-lead` → `devsecops-agency:test-runner`, with the brief.
   - Task: run `git status --porcelain` and `git rev-parse HEAD`, and record both outputs verbatim. These commands are read-only, so this step needs no authorisation.
   - Output: `_agency/baseline/integrity.md`.
2. Compare that with the adoption commit:
   - any changed or new path outside `_agency/` and `.devsecops-agency/` is a **breach**;
   - so is a different HEAD.

   A breach goes at the top of the report.
3. Write `_agency/adoption-report.md`:

```markdown
# Adoption report — <repository>

Adoption commit: <id>
Integrity: <clean / breach: the paths, and the HEAD if it changed>

## What it is
<two or three sentences, from spec-as-is.md and system-map.md>

## Health
- Tests: <passed / failed / skipped, or "not run: not authorised">
- Security scan: <secrets found by file, or none; dependency findings by severity, or "not run">
- Licenses: <the repository's license; any dependency conflicts>

## Risks
<from the as-built threat model and the security scan, highest first>

## Open questions
<from every record's "could not determine" list, de-duplicated>

## Recommended first steps
<numbered; the first is "git-ignore `.devsecops-agency/`" unless it is already ignored, then whether `_agency/` should be committed>

## Evidence
<a link to each record above>
```

4. Tell the Chairman the report is ready, summarise it in three lines, and stop. The project is owned only when the Chairman answers the questions and approves.

## Re-entry

If `_agency/project.md` exists, read the adoption commit and compare it with the repository's current commit. If they differ, the repository changed outside the agency. Re-run step 2 for the changed files before anything else, and record the new commit.

## Rules for someone else's repository

- The repository is the source of truth. Follow its branching, style, test and CI conventions.
- During adoption, nothing outside `_agency/` is written. No branch, commit or push is made. This rests on the brief and the step 5 check, not on the guard: B1 only keeps writes inside the launch folder.
- A department that has nothing to report writes `n/a` with a reason. Skipping silently is not allowed.
