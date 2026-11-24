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
| `_agency/baseline/dependencies.md` | `sbom-slsa`, through `security-lead` |
| `_agency/baseline/licenses.md` | `license-checker`, through `gc` |
| `_agency/baseline/environments.md` | `deployment-engineer`, through `devops-lead` |
| `_agency/spec-as-is.md` | `spec-writer`, through `pm-lead` |
| `_agency/adoption-report.md` | `ceo` |

## Steps

### 1. Receive (CEO)

1. Read the Chairman's instruction. Record the repository and the instruction in `_agency/project.md`. Read the commit id from `.git/HEAD` (and the ref it points to) and record it as the **adoption commit**.
2. Ask the Chairman for only the access the work needs, in one message:
   - **Running the repository's code on this machine.** This covers the existing tests (step 3) and installing their dependencies. Running someone else's code needs the Chairman's yes, because there is no OS sandbox on this machine yet.
   - Nothing else. Adoption needs no network access beyond package installs, and no secrets, deploys or pushes.
3. Record the answer in `_agency/project.md`. If the answer is no, step 3's test run is recorded as "not run: not authorised" and everything else proceeds.

### 2. Map (CTO)

Dispatch `devsecops-agency:engineering-lead` with the adoption commit. It dispatches `devsecops-agency:legacy-code-specialist` for `_agency/system-map.md`, then checks the map against the repository with `devsecops-agency:system-architect`. The map must cite a path for every claim.

### 3. Baseline (in parallel, after the map)

- `devsecops-agency:qa-lead` dispatches `devsecops-agency:test-runner` to run the existing tests exactly as the repository's CI runs them, only if step 1 authorised it. Record the command, the pass, fail and skip counts, and the failing test names. **This baseline must hold:** a later change that breaks a test that passed here is a red.
- `devsecops-agency:security-lead` dispatches `devsecops-agency:threat-modeler` for an as-built threat model, and `devsecops-agency:sbom-slsa` for a dependency inventory and known-vulnerability list. It dispatches `devsecops-agency:dlp-scanner` to search the repository for committed secrets, recorded in `_agency/baseline/threat-model.md` by file and line, never by value.
- `devsecops-agency:gc` dispatches `devsecops-agency:license-checker` for the repository's own license and its dependencies' licenses.
- `devsecops-agency:devops-lead` dispatches `devsecops-agency:deployment-engineer` to document the environments the configuration names. It reads only, and deploys nothing.

### 4. Reconstruct intent (CPO)

Dispatch `devsecops-agency:pm-lead`, which dispatches `devsecops-agency:spec-writer` for `_agency/spec-as-is.md`: what the product does today, from the code and its documents. Everything that could not be determined is listed as a question, not guessed.

### 5. Report (CEO)

Write `_agency/adoption-report.md`:

```markdown
# Adoption report — <repository>

Adoption commit: <id>

## What it is
<two or three sentences, from spec-as-is.md and system-map.md>

## Health
- Tests: <passed / failed / skipped, or "not run: not authorised">
- Dependencies: <count; known vulnerabilities by severity>
- Licenses: <the repository's license; any dependency conflicts>

## Risks
<from the as-built threat model and the dependency list, highest first>

## Open questions
<from every record's "could not determine" list, de-duplicated>

## Recommended first steps
<numbered; the first is always "git-ignore `.devsecops-agency/`" unless already ignored, and whether `_agency/` should be committed>

## Evidence
<a link to each record above>
```

Then tell the Chairman the report is ready, summarise it in three lines, and stop. The project is owned only when the Chairman answers the questions and approves.

## Re-entry

If `_agency/project.md` exists, read the adoption commit and compare it with the repository's current commit. If they differ, the repository changed outside the agency. Re-run step 2 for the changed files before anything else, and record the new commit.

## Rules for someone else's repository

- The repository is the source of truth. Follow its branching, style, test and CI conventions.
- During adoption, nothing outside `_agency/` is written. No branch, commit or push is made.
- A department that has nothing to report writes `n/a` with a reason. Skipping silently is not allowed.
