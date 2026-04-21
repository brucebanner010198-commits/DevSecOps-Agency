# okr-writing-rules — OKR vs KPI vs to-do

Distinguish the three. Write OKRs. Never confuse them.

## An **Objective** (O)

- States an **outcome** that changes the world (or the product, or the market).
- Is **qualitative** — describes a state of affairs, not a number.
- Is **inspirational but achievable in one quarter**.
- Is **not** a task ("build the login page" is a to-do, not an O).
- Starts with a verb. "Launch...", "Reduce...", "Become...", "Establish...".

Examples of valid Os:
- `Launch 2 revenue-positive products this quarter`
- `Reduce average time-from-idea-to-launch to under 21 days`
- `Establish the agency as the fastest shipping team on benchmark X`

Examples of **invalid** Os (flag and reject):
- `Build the login page` (that's a task)
- `Have more uptime` (not measurable, not bounded)
- `Win the market` (not achievable in one quarter)

## A **Key Result** (KR)

- States a **measurable** condition that, if true, means the O moved.
- Has a **number and a date** (or is a boolean that must flip to true by a date).
- Is **owned** by a specific Chief (`cro`, `pm-lead`, etc.) or the CEO.
- Is **falsifiable** — at end of quarter you can say true or false.

Examples of valid KRs:
- `Product A reaches $100 MRR within 30 days of launch` (number + date)
- `Red-team council runs on 100% of launches by 2026-06-30` (percent + date)
- `≥ 3 memory/patterns/*.md cited per new project brief by end of quarter` (count + date)

Examples of **invalid** KRs (flag and reject):
- `Improve security` (not measurable)
- `Users love the product` (not falsifiable without a survey instrument)
- `More revenue` (no baseline, no target, no date)

## OKR vs KPI

A **KPI** (key performance indicator) is a metric the agency watches continuously. A **KR** is a KPI **with a target and a date** attached. KPIs live in `status.json > kpis` (a future Wave 5 concern). KRs live in `VISION.md > ## Active OKRs`.

## OKR vs to-do

A **to-do** is in `status.json > tasks[]` (via `taskflow`). A **KR** is in `VISION.md`. A KR may be **decomposed** into many to-dos across many projects. A to-do never becomes a KR.

## Writing checklist (before appending to VISION.md)

For each O:
- [ ] Starts with a verb
- [ ] Describes an outcome, not a task
- [ ] Achievable in one quarter
- [ ] Has ≥ 1 KR, ≤ 3 KRs
- [ ] Each KR has a number and a date
- [ ] Each KR is falsifiable
- [ ] No KR overlaps with another KR's definition

If any box is unchecked, rewrite before writing to `VISION.md`.

## Cadence rules

- OKRs are quarterly. The CEO refreshes `VISION.md` on the first user meeting of a new quarter.
- Mid-quarter amendments require an ADR + a `history/` entry.
- KRs are scored **per phase** by every Chief's report (via the `okr` skill). End-of-quarter score rolls up into the retro.

## Anti-patterns

- Writing 10 OKRs. (Focus dies — cap is 5.)
- Writing an O with 6 KRs. (Cap is 3. Split the O or drop KRs.)
- Copying the previous quarter's OKRs unchanged. (Either this quarter differs or last quarter's OKRs were aspirational trash.)
- Writing "improve X" as a KR. (Not measurable.)
- Writing a KR owned by no one. (Add the owning Chief's slug in parentheses.)
