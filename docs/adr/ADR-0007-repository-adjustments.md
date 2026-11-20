---
adr: 0007
title: Repository adjustments - no license, sensitive data kept out, no file headers
status: accepted
date: 2026-11-20
deciders: user
kind: repository-settings
related: CONTRIBUTING.md section 9, SYSTEM-CARD.md, README.md, .claude-plugin/plugin.json, LICENSES/
---

# ADR-0007: Repository adjustments

## Context

The owner's repo standard (`repo-standard/STANDARD.md` section 12) asks for
each repository's own adjustments to be recorded before the first change.
This repository had none on record. Until now the README, `plugin.json`,
`CONTRIBUTING.md` and `SYSTEM-CARD.md` described the project as MIT licensed,
but there was no `LICENSE` file, so no license had ever actually been
granted.

## Decision

The Chairman decided on 2026-11-20:

| Item | Decision |
| --- | --- |
| Visibility | Public. The command center deploys to GitHub Pages. |
| License | **None.** The project is not open source. All rights are reserved, and no `LICENSE` file is added. |
| Third-party code | Imported components keep their own licenses. The notices in `LICENSES/` stay, because the upstream MIT and Apache-2.0 terms require them. |
| File headers | None. |
| Sensitive data | No real patient or personal health data goes into git, GitHub or the published site. Four local files that may hold such data are kept git-ignored and are not read by AI tools. None of them has ever been in the repository's history. |
| Admin rights | The acting account (`brucebanner010198-commits`) has admin rights. |

## Consequences

- The project's own MIT claim is removed from `README.md`, `CONTRIBUTING.md`
  and `SYSTEM-CARD.md`. In `plugin.json`, `license` becomes
  `LicenseRef-Proprietary`, the SPDX form for "not open source". The field
  stays because `claude plugin validate` refuses a plugin that has neither a
  `LICENSE` file nor a `license` value. A value that grants nothing meets
  that check without adding a license.
- `CONTRIBUTING.md` no longer says contributions are MIT licensed. Terms
  for outside contributions are left for the owner to set before any are
  accepted.
- Public visibility lets people read the code but grants no right to copy,
  modify or redistribute it.
- The agency's own license tooling (`license-checker`, `ip-lineage`) still
  defaults to MIT for the projects it builds. That default is about
  generated projects, not this repository, and is unchanged.
