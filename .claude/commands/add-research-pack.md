---
name: add-research-pack
description: Workflow command scaffold for add-research-pack in DevSecOps-Agency.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /add-research-pack

Use this workflow when working on **add-research-pack** in `DevSecOps-Agency`.

## Goal

Adds a new research pack or major research section, consisting of multiple markdown files under a dedicated subfolder, typically for competitive analysis or similar structured research.

## Common Files

- `research/competitive-landscape/00-README.md`
- `research/competitive-landscape/01-overview-and-matrix.md`
- `research/competitive-landscape/*-*.md`
- `research/competitive-landscape/_TEMPLATE.md`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Create a new subfolder under research/ (e.g., research/competitive-landscape/)
- Add multiple structured markdown files (e.g., 00-README.md, 01-overview-and-matrix.md, etc.) covering different aspects of the research topic
- Include a _TEMPLATE.md for future additions

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.