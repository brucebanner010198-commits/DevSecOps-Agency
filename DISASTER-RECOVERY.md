# Disaster Recovery Plan — DevSecOps-Agency

**Version:** 1.0
**Ratified:** 2026-04-22
**Plugin version:** v0.5.0
**Authority:** [`CONSTITUTION.md`](CONSTITUTION.md) + [`RESILIENCE.md`](RESILIENCE.md)
**Owner:** CSRE + CRes · **Reviewer:** CAO · **Cadence:** tested at every Keeper Test (quarterly)
**Classification:** Public

---

## 0. Purpose

This document answers: **"If something bad happens to the Agency, what do we do, who does what, and how fast?"**

"Something bad" includes: lost repository, corrupted `main` branch, compromised credentials, compromised release artifact, extended User unavailability, hostile fork, and catastrophic data loss.

The plan is written to be executable by the User alone, without the Agency — because in several scenarios the Agency will be offline, read-only, or itself the thing that failed.

---

## 1. Recovery objectives

| Metric | Target |
|---|---|
| **RPO (Recovery Point Objective)** — maximum acceptable data loss | 24 hours |
| **RTO (Recovery Time Objective)** — maximum acceptable downtime before normal ops resume | 72 hours |
| **RTO for USER-ONLY approval pathway** | 4 hours (if the User is reachable) |
| **RTO for read-only mode** | 15 minutes (Agency enters read-only on any trigger) |

RPO is bounded by git push frequency. Any change not pushed to GitHub origin is at risk until it is pushed. Pushes occur at the end of every wave; more frequent pushes are recommended for long sessions.

---

## 2. Backup strategy

### 2.1 Primary backup — GitHub origin

`https://github.com/brucebanner010198-commits/DevSecOps-Agency.git` is the canonical source. All commits on `main` + all tags are the primary backup.

### 2.2 Secondary backup — release archives

Every minor version is shipped as `devsecops-agency-vX.Y.Z.plugin` (a stored zip) and attached to the GitHub Release with that tag. Release archives are a second, immutable snapshot.

### 2.3 Tertiary backup — local working copy

The User's local clone at `/sessions/loving-adoring-maxwell/_ship/repo/` is a third copy. Acceptable for short-term recovery only; not authoritative.

### 2.4 Off-site backup (recommendation to User)

**Recommended:** the User maintains a second clone on a different machine or encrypted external medium, updated at least monthly. The User owns this; the Agency does not.

---

## 3. Detection — how we notice a disaster

| Signal | Source | Escalation |
|---|---|---|
| Force-push detected on `main` | Git audit + GitHub audit log | Critical — treat as Compromise |
| Tag rewritten (non-annotated → annotated, or target changed) | GitHub Release page + git | Critical |
| `.plugin` archive hash mismatch vs. release notes | CSRE hash check | High — possible supply-chain compromise |
| Hook execution disabled or skipped | `runtime-hooks/governance-audit` reports | High |
| Append-only file modified in-place | `runtime-hooks/governance-audit` | Critical |
| User unreachable > 72 hours | CRhy timer | Trigger read-only mode |
| PAT credential exposure detected | secrets-scanner, email alert from GitHub, or vendor notice | Critical — rotate immediately |
| Release archive download mismatch | User-reported or CSRE sample check | High |
| Anthropic platform outage > 48h | Agency cannot run | Trigger read-only advisory to User |

---

## 4. Response playbooks

### 4.1 Playbook A — Corrupted or tampered `main`

**Symptom:** force-push, history rewrite, or an unexpected commit appears on `main`.

**Immediate actions (User, within 1 hour):**

1. Stop all sessions. Open a read-only review terminal.
2. Verify against local reflog:
   ```bash
   cd /sessions/loving-adoring-maxwell/_ship/repo
   git reflog | head -50
   git fsck --full
   ```
3. Identify the last known-good commit. Cross-reference with the latest GitHub Release tag (those are immutable reference points).
4. **Do not** push anything to origin until the known-good state is identified.
5. Create a recovery branch from the known-good commit:
   ```bash
   git checkout -b recovery/<date> <known-good-sha>
   ```
6. Open a private issue on the repo describing what happened. This becomes the incident record.
7. Rotate the PAT token used for pushes (GitHub Settings → Developer settings → Personal access tokens).

**Within 24 hours:**

- The Agency (running read-only) produces an RCA via `skills/rca/SKILL.md`.
- The recovery branch is force-reset to become the new `main` ONLY if the User authorizes (USER-ONLY action: "destructive git operation").
- A Post-Incident Report is committed to the repo and attached to the issue.

**Within 14 days:**

- Threat model §4 is re-walked (per [`THREAT-MODEL.md`](THREAT-MODEL.md) §10).
- Any missing control is closed with a new runtime-hook or council rule.

### 4.2 Playbook B — Lost repository (origin deleted / account lost)

**Symptom:** `github.com/brucebanner010198-commits/DevSecOps-Agency` is unreachable or deleted.

**Recovery path:**

1. Use the local clone as the source of truth.
2. Create a new remote (same or different hoster):
   ```bash
   git remote set-url origin <new-remote-url>
   git push --all
   git push --tags
   ```
3. If the local clone is also gone, reconstruct from the most recent `.plugin` archive the User has:
   ```bash
   cd /tmp && unzip devsecops-agency-vX.Y.Z.plugin -d recovery
   cd recovery && git init && git add . && git commit -m "Recovered from vX.Y.Z archive"
   ```
   *Note:* this loses history. Mark the new repo with an ADR noting the loss and the reconstruction basis. The append-only invariant is **preserved forward** but cannot be proved backward in this case — this is explicitly called out in the recovery ADR.
4. Publish recovery announcement.

### 4.3 Playbook C — Compromised release artifact

**Symptom:** a released `.plugin` archive is discovered to be different from what we shipped, or a user reports a suspicious archive.

**Immediate actions:**

1. **Yank the release.** On GitHub: edit the Release, mark it as a pre-release with a prominent "YANKED — DO NOT INSTALL" note. Do not delete — deletion erases history.
2. Rotate the PAT.
3. Compute hashes of the local artifact (what we actually built) and compare to what GitHub served. If the User can obtain the compromised archive from a reporter, compute its hash too.
4. File a GitHub Security Advisory on the repo.
5. Publish a public notice in the next commit README patch + in the Release notes.
6. Re-release the correct artifact with a patched version bump (vX.Y.Z+1).

**Follow-up:**

- RCA within 48 hours.
- Add a hash-manifest step to the release script (if not already) so every future release ships with `sha256sum *.plugin` in release notes.
- SLSA Level 3 target ([`SWOT.md`](SWOT.md) O / T2) accelerated.

### 4.4 Playbook D — PAT / credential compromise

**Symptom:** secrets-scanner positive, GitHub alert, or anomalous push.

**Immediate actions (User):**

1. Revoke the PAT immediately in GitHub Settings.
2. Audit recent commits and releases for unauthorized changes (applies Playbook A if anything anomalous).
3. Rotate any other credentials that might have touched the same machine.
4. Check GitHub audit log for the compromised window.

**Within 24 hours:**

- Create a new PAT with minimal scope (repo only).
- If possible, switch to SSH key auth for pushes (longer-term safer).
- RCA describing root cause (phishing, leaked machine, etc.) and remediation.

### 4.5 Playbook E — Extended User unavailability (read-only mode)

**Trigger:** User is unreachable for > 72 hours on any in-progress USER-ONLY approval.

**Agency behavior in read-only mode:**

- Continues to analyze, research, and produce draft artifacts under `_ship/` as untracked files.
- **Does not:** commit to `main`, create tags, push to origin, create GitHub Releases, make public posts, or take any USER-ONLY action.
- Writes a `READ-ONLY-MODE.md` at the top of `_ship/repo/` explaining when the mode was entered and what is pending.
- Publishes a brief summary to the session log every 12 hours while in read-only.

**Exiting read-only mode:**

- On User return, the User reads `READ-ONLY-MODE.md`, reviews pending items, and issues approvals.
- Agency resumes full operation; `READ-ONLY-MODE.md` is moved to an `incidents/` folder as a historical record.

### 4.6 Playbook F — Anthropic platform extended outage

**Trigger:** Claude is unavailable for > 48 hours.

- The Agency cannot run. This playbook is for the User only.
- User can continue to push commits manually (outside the Agency) — the repo remains functional as a normal git repo.
- User should **not** amend `main` history or release new versions during the outage unless following a pre-existing ADR. Governance decisions wait.
- On Claude return: the Agency re-boots, reads session logs + ADRs + LESSONS to rehydrate context, and runs the Keeper Test as a consistency check before resuming normal operation.

### 4.7 Playbook G — Hostile fork under similar name

**Symptom:** a fork appears on GitHub or elsewhere that (a) uses the name "DevSecOps-Agency" or a near-miss, (b) strips safety controls or non-waivable classes, (c) claims to be the official version.

**Response:**

1. Post a clarifying notice in our README and our latest Release describing which repo is canonical.
2. File DMCA or trademark claim if applicable.
3. Publish a diff-summary of what the fork changed, so prospective users can make informed choices.
4. Do not silently copy their "improvements" back. Any idea adopted from the fork goes through the normal Constitutional amendment process.

---

## 5. Append-only restoration

The append-only invariant is the single most important property. Here is how it is protected and how it is restored if violated.

**Protection (normal operation):**

- `runtime-hooks/governance-audit` refuses in-place modification of files under `sessions/`, `logs/`, `adrs/` (ADRs), LESSONS.md rows, and stepping-stone trails.
- `runtime-hooks/commit-gate` refuses commits that would modify these paths except by append.
- Branch protection on `main` (v0.6.0 target) will require PR review.

**Restoration (if violated):**

1. Identify the offending commit via `git log --patch <path>`.
2. Revert via a new append-style commit — **never rebase** to hide the violation. The violation itself becomes part of the append-only history.
3. File the incident per Playbook A.
4. The CAO reviews and publishes a public correction in [`LESSONS.md`](LESSONS.md) with tag `APPEND_ONLY_VIOLATION`.

**Key invariant:** even a violation of append-only is recorded append-only. The system does not attempt to erase its own errors.

---

## 6. Restoration verification checklist

After any recovery, before marking the incident closed, the User + Agency runs this checklist:

- [ ] `main` branch HEAD matches the expected known-good SHA or a forward-only recovery commit.
- [ ] All release tags are annotated and signed (where applicable) and point at the expected SHAs.
- [ ] `runtime-hooks/*` run on a test session without error.
- [ ] `.claude-plugin/plugin.json` version matches the latest release tag.
- [ ] [`TRUST.md`](TRUST.md), [`SECURITY.md`](SECURITY.md), [`CONSTITUTION.md`](CONSTITUTION.md) are unchanged from their ratified versions unless the incident itself changed them (in which case the ADR documents the change).
- [ ] Session log for the incident is complete and append-only.
- [ ] Post-Incident Report is committed and linked from the incident issue.
- [ ] [`LESSONS.md`](LESSONS.md) has a row for the incident.

Only then can the incident be marked resolved.

---

## 7. Drill

A disaster-recovery drill is run at every Keeper Test (quarterly). The drill exercises at least one Playbook at random. Drill findings are published to the Keeper Test report in [`TRUST.md`](TRUST.md) §3.

**Minimum drill scenarios on rotation:**

- Simulated force-push on `main` (Playbook A).
- Simulated compromised release (Playbook C).
- Simulated read-only mode trigger (Playbook E).

Findings fold back into this document within 14 days of each drill.

---

## 8. Ownership matrix

| Domain | Primary | Backup |
|---|---|---|
| Recovery coordination | CSRE | CIR |
| Root cause analysis | CIR | CAO |
| Governance / append-only | CAO | CGov |
| Credentials / secrets | CISO | User |
| Release artifact integrity | CSRE | CISO |
| User-facing communication | CEO | CRhy |
| Drill design | CRT | CSRE |

**USER-ONLY actions during recovery:**

- Any `git push --force` or destructive history operation.
- Any PAT / credential rotation.
- Release yank or re-release.
- Public notice or communication.
- Marking the incident resolved.

---

## 9. Document control

- **File:** `DISASTER-RECOVERY.md`
- **Version:** 1.0
- **Owner:** CSRE + CRes (joint)
- **Reviewer:** CAO
- **Append-only:** No (this document is revised; version history in git)
- **Change policy:** Any revision requires CAO concurrence and an ADR.
- **References (original synthesis):**
  - Google SRE Book (Beyer et al.), chapters on disaster testing, DiRT drills, and error budgets.
  - NIST SP 800-34 Rev. 1 — Contingency Planning Guide.
  - NIST SP 800-61 Rev. 2 — Computer Security Incident Handling.
  - ISO 22301 — Business Continuity Management.
  - CNCF Disaster Recovery whitepaper.

---

*The best disaster recovery plan is the one the User has practiced before they need it.*
