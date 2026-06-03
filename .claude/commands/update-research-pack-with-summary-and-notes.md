---
name: update-research-pack-with-summary-and-notes
description: Workflow command scaffold for update-research-pack-with-summary-and-notes in DevSecOps-Agency.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /update-research-pack-with-summary-and-notes

Use this workflow when working on **update-research-pack-with-summary-and-notes** in `DevSecOps-Agency`.

## Goal

Updates an existing research pack by adding an executive summary, delivery notes, and updating the index to reference new files.

## Common Files

- `research/competitive-landscape/00-README.md`
- `research/competitive-landscape/02-executive-summary.md`
- `research/competitive-landscape/DELIVERY-NOTES.md`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Add an executive summary markdown file (e.g., 02-executive-summary.md) to the research pack folder
- Add DELIVERY-NOTES.md to capture delivery state and caveats
- Update the index file (00-README.md) to link to the new summary and notes

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.