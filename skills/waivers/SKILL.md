---
name: waivers
description: Formal waiver request/approval flow for clearing a blocking-council red without fixing the underlying finding. Invoked when CISO/CEVO/CRT/CAO hold a red and ship-pressure warrants a time-boxed exception. Proposed by the responsible council lead, reviewed by the blocking Chief + CEO, approved by the user (per GOVERNANCE.md row 7). Every waiver has a calendar expiration — no permanent waivers. Files `waiver-grant` ADR + paired `waiver-expiry` ADR scheduled for the expiry date. On expiry, the original red re-fires unless a closing remediation ADR has landed. Composes with gates, ladder (Rung 3 typical), user-meeting, inbox.json.
metadata:
  version: "0.1.0"
---

# waivers

## When to trigger

- A blocking-council red (CISO / CEVO / CRT / CAO) stands on a ship-path artifact and council-lead judges that the underlying fix would slip the project past an acceptable window.
- A red-team `high` or `critical` finding on a live artifact where rollback is more dangerous than the finding (rare; requires CRT + CEO agreement).
- An eval regression > 5 pp where the regression is known-expected (e.g., quarterly baseline shift) — waiver here amounts to a baseline ADR, but still files via this skill.
- NOT triggered for informing-only chiefs. Informing chiefs don't gate; their concerns become ADRs, not waivers.

## Inputs

- `GOVERNANCE.md` — decision matrix, USER-ONLY list.
- `VALUES.md` — §1 receipts, §4 append-only, §3 independence.
- The originating finding: `_vision/red-team/findings.md` row, CAO close-audit entry, CEVO regression report, or CISO gate row.
- `inbox.json` — for queuing the user decision.

## Outputs

- `_decisions/ADR-NNNN-waiver-grant-<slug>.md` — on user approval.
- `_decisions/ADR-NNNN-waiver-deny-<slug>.md` — on user denial.
- `_decisions/ADR-NNNN-waiver-expiry-<slug>.md` — scheduled for expiry date; files automatically via rhythm heartbeat.
- Append entry to `_vision/waivers/active.md` (or create if absent) — at-a-glance list of open waivers.
- Append entry to `_vision/waivers/history.md` — every grant + deny + expiry + remediation landing.
- `notify` event `waiver-<grant|deny|expiry>` — rate-limited.

## Process

1. **Verify preconditions.** The red must be on file (red-team finding row OR CAO close-audit entry OR CEVO regression report OR CISO gate row). If not, fail fast — waivers don't cover undocumented reds.
2. **Draft the request.** Responsible council lead writes:
   - `finding:` exact id.
   - `impact:` what the blocking chief said would break.
   - `reason to waive:` what slips if we fix first.
   - `remediation plan:` step-by-step how we'll close the red during the waiver window.
   - `expiration:` exact calendar date (YYYY-MM-DD), not relative ("until ship").
   - `owner:` agent accountable for remediation.
3. **Blocking-chief review.** The chief whose council raised the red signs off or sends back. They cannot approve — only the user can approve.
4. **CEO review.** CEO signs off or sends back on procedural grounds (is the expiration reasonable? is the remediation plan concrete? is the owner right?). CEO also cannot approve.
5. **User decision via `user-meeting` + `inbox.json`.** The request is presented to the user in the 4-phase user-meeting flow: brief → present → capture → commit. The commit step yields either APPROVE or DENY.
6. **On APPROVE.** File `ADR-NNNN-waiver-grant-<slug>.md` citing finding id, approver (user), expiration, remediation plan. Append to `_vision/waivers/active.md`. Schedule the `waiver-expiry` ADR via rhythm heartbeat on the expiration date.
7. **On DENY.** File `ADR-NNNN-waiver-deny-<slug>.md` citing finding id, user response, next step (typically: fix the finding, re-run the gate). Append to `_vision/waivers/history.md` only (not active).
8. **On expiry day (rhythm heartbeat).** Check `_vision/waivers/active.md` for rows with `expiration: <today>`. For each:
   - If a remediation ADR has landed closing the finding → file `waiver-expiry` ADR `outcome: remediated`; move row from active.md to history.md.
   - Else → file `waiver-expiry` ADR `outcome: re-fired`; re-open the original finding; notify user; escalate via ladder Rung 3.
9. **Notify.** Emit `waiver-grant` / `waiver-deny` / `waiver-expiry` event with finding id + summary.

## Waiver scope

A single waiver covers **one finding on one artifact on one project**. If the same finding surfaces on a different project, that project needs its own waiver. This is intentional — it prevents one user approval from cascading across the portfolio.

If a systemic fix is in flight (e.g., a stepping-stone that would close this finding class broadly), note it in the `remediation plan:` field, but the waiver is still project-scoped until the stone lands.

## Interaction with other skills

| Skill | How waivers compose |
| --- | --- |
| `gates` | Waiver-grant ADR is the only non-fix path to clear a blocking gate. Gate vocabulary: `waived: <ADR-id>`. |
| `ladder` | Grant typically at Rung 3 (material decision); deny returns to Rung 2 (fix-loop) or Rung 4 (replan). |
| `user-meeting` | Step 5 above runs through the 4-phase flow. |
| `inbox.json` | Queues the user decision when user is async. |
| `rhythm` | Daily heartbeat reads `_vision/waivers/active.md`; on any row with `expiration: <today>`, invokes step 8. |
| `audit` | Close-audit checks every shipped artifact for waived gates. If a waiver was active and no remediation ADR exists, flag CAO red. |
| `red-team` | CRT findings that were waived and re-fired on expiry count toward L3 demotion for the owning agent (via `career-ladder`). |

## Anti-patterns

- Don't grant a waiver without a calendar expiration. Permanent waivers violate `VALUES.md §4` (append-only — a waiver must have a closing row).
- Don't let the blocking chief approve the waiver on their own red. The approver is always the user.
- Don't re-waive an expired waiver without remediation progress. If the first waiver window closed with no fix, the second request must cite the progress that makes the new window credible.
- Don't collapse multiple findings into one waiver. One finding per waiver; the paper trail depends on 1:1 mapping.
- Don't backdate a waiver. The grant covers from the ADR landing forward; pre-ADR work under the red is a separate CAO finding.
- Don't waive an ASI-class red-team finding. Those require fix-or-park; no waiver path.
- Don't grant a waiver through a side channel (Slack DM, call, email). `user-meeting` + `inbox.json` only.
- Don't let a waiver cover a USER-ONLY action itself (e.g., don't waive the requirement that publishing needs user consent). USER-ONLY actions are not waivable.

See `references/request-template.md` for the request format and `references/expiry-protocol.md` for the expiry-day flow.
