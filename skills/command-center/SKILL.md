---
name: command-center
description: >
  This skill should be used when the user wants to see the live status of the
  DevSecOps Agency — the full org chart (CEO + 16 councils: Research, Product,
  Architecture, Security, Execution, Quality, DevOps, Docs, Legal, Marketing,
  Strategy, People-ops, Audit, Evaluation, Red-Team, SRE), every board and
  council meeting, queued blockers, and links to every artifact produced.
  Trigger phrases include "open the command center", "show me the agency
  dashboard", "what are the agents doing", "open the project board", "show me
  the board", or /devsecops-agency:command-center. Also called internally by
  the ceo / ship-it / board-meeting / council-meeting skills after every
  handoff so the artifact stays fresh.
metadata:
  version: "0.3.0"
---

# command-center — the live agency view

This skill produces (or refreshes) a persistent Cowork artifact that visualises the active project. It reads `status.json`, `chat.jsonl`, and `inbox.json` and renders them into a single self-contained HTML page.

## Trigger contract

- **Standalone**: user asked to see the dashboard → load active project, render artifact.
- **Internal call**: a phase or meeting just completed → re-render with new state.

## Resolve the active project

1. Look under `/sessions/loving-adoring-maxwell/mnt/outputs/devsecops-agency/` for project subfolders.
2. The active project is the one with `status.json.phase != "delivered"`. If multiple, the most recently updated.
3. If none exists, tell the user: "No active project. Start one with `/devsecops-agency:ceo` or `/devsecops-agency:ship-it`."

## Render

1. Read `status.json`, `chat.jsonl` (last 200 lines), `inbox.json`.
2. Load the template at `references/artifact-template.html`.
3. Substitute `__STATE__` with a single `<script>` block that assigns:
   ```js
   window.__STATE__ = {
     projectFolder: "<absolute path>",
     status: {...},
     chat:   [...],
     inbox:  {...}
   };
   ```
4. Substitute `__PROJECT_TITLE__` with the project slug.
5. Substitute `__GENERATED_AT__` with the current ISO timestamp.

## Publish

- First render for this project → `mcp__cowork__create_artifact` (save artifact ID into `status.json.commandCenterArtifactId`).
- Subsequent renders → `mcp__cowork__update_artifact` with the stored ID.

## What the artifact shows

See `references/panel-spec.md`. Five sections:

1. **Header** — project name, current phase, blocker count, last updated.
2. **Organisation** — CEO at the top; below, 9 council cards (Research, Product, Architecture, Security, Execution, Quality, DevOps, Docs, Legal). Each card shows the Chief title, the lead agent, and their specialists. Active agents pulse green.
3. **Phases** — 7-card timeline (Discovery → Design → Build → Verify → Ship → Document+Legal → Close). Current phase highlighted; completed are green; blocked are red.
4. **Meeting log** — filterable by scope: All / Board / Council. Each entry shows timestamp, type badge, from → to, gate signal (if present), artifacts, note.
5. **Inbox + Artifacts** — open questions (red-bordered) above resolved; linkable list of every file produced.

The artifact is fully self-contained (vanilla HTML/CSS/JS, no external deps, no fetch calls). State is embedded inline so the artifact renders even after the session ends.

## Backward compatibility

If `status.json` uses the v0.1 schema (six `team.pm / team.security / team.engineering / team.qa / team.devops / team.docs` entries), the renderer maps them into the new council layout transparently. v0.1 projects keep rendering.

## Progressive disclosure

- `references/panel-spec.md` — exact per-panel data contract
- `references/artifact-template.html` — the vanilla HTML/CSS/JS template
