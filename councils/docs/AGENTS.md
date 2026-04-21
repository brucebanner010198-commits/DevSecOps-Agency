# councils/docs — boundaries

## Output contract

- Lead: `docs-lead` (CKO). Specialists: api-documenter, readme-writer, tutorial-writer.
- Artifacts: `<slug>/docs/README.md`, `<slug>/docs/api/`, `<slug>/docs/tutorial/getting-started.md`.
- Tutorial ends in a visible result within 10 minutes.

## Must

- README answers: what is this, who is it for, how to run it in 60 seconds, where to learn more.
- API docs generated from the code where possible. Handwrite only prose (overview, auth, errors).
- Tutorial has **exact** commands/snippets. Copy-paste must work on a fresh machine.
- Every code snippet is syntax-checked (compiles, lints, or is a known-good shell command).
- Link to PRIVACY, LICENSE, SECURITY from the README.

## Must not

- Use placeholder text ("Lorem ipsum", "TODO", "<your-key-here>" without a note explaining where to get it).
- Document a feature the code doesn't have. Check before writing.
- Ship a tutorial that assumes unstated prerequisites. Declare them in a `## Prerequisites` section.
- Copy the spec into docs verbatim. Docs are for a reader; specs are for a builder.

## Gate heuristic

- `green`: README + API + tutorial all present, tutorial walked end-to-end on a fresh env.
- `yellow`: API section missing one endpoint, or tutorial has one unverified step.
- `red`: tutorial doesn't produce a visible result, or a documented feature is not in code.
