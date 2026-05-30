# infolog-io — Tests & End Conditions

## Profile

**Full-shape skill.** Theme bundle with 8 reference files. Consumed exclusively
by `component-composer`.

## End conditions (theme ships when all are true)

1. `themespec.json` resolves correctly when `component-composer` reads
   `skills/infolog-io/themespec.json`.
2. All 8 reference files declared in SKILL.md exist at their stated paths.
3. Every one of the 16 criteria in `references/criteria.md` is classified as
   mechanical or LLM-judge (no unclassified entries).
4. `references/tokens.md` names every CSS variable that `references/palette.md`
   assigns a concrete value to. No variable in palette is absent from tokens.
5. A composition run invoking `infolog-io` as theme reaches zero criteria
   failures before emitting the final artifact.
6. README is ≤200 words.

## Test cases

### TC1 — Mechanical checks fire on chartjunk CSS

Given: a draft artifact with `box-shadow: 2px 2px 4px rgba(0,0,0,0.3)` on a
chart element outside `:root`.
When: the mechanical validator runs `chartjunk_decorative_css`.
Then: the check emits `FAIL` with evidence naming the selector and property.
The drafter receives the failure on the next loop iteration.

### TC2 — token_compliance rejects literal hex outside `:root`

Given: a draft artifact where `.axis-label { color: #444444; }` appears in
a rule outside `:root`.
When: `token_compliance` runs.
Then: `FAIL` — literal hex outside `:root`. The corrected draft moves
`#444444` into `:root { --axis-label-color: #444444; }` and uses
`color: var(--axis-label-color)`.

### TC3 — contrast_failure on low-contrast axis text

Given: axis tick labels rendered with computed color `#aaaaaa` on background
`#ffffff` (contrast ratio ≈ 2.3:1, below the 4.5:1 WCAG AA threshold).
When: `contrast_failure` runs.
Then: `FAIL`. The drafter darkens the tick color to meet ≥4.5:1 on the next
iteration.

### TC4 — missing_range_frame flagged by LLM-judge

Given: a line chart whose x-axis runs 0–100 while data spans 14–73.
When: LLM-judge evaluates `missing_range_frame`.
Then: judge flags the criterion. The drafter clips axis extents to the data
range (14 to 73) in the next draft.

### TC5 — hidden_mark rejects sub-2px data mark

Given: a scatter plot with one `<circle r="0.8">` mark.
When: `hidden_mark` runs (requires `width ≥ 2px` and `opacity ≥ 0.3`).
Then: `FAIL`. The drafter enlarges the radius on the next iteration.

### TC6 — insufficient_data_ink flagged on heavy gridlines

Given: a bar chart with `grid-line opacity: 1` and `stroke-width: 2`.
When: LLM-judge evaluates `insufficient_data_ink`.
Then: judge flags the criterion. The drafter reduces gridline opacity to ≤0.2
or removes them.

### TC7 — missing_direct_label on two-series chart

Given: a two-series line chart with a corner legend instead of direct labels.
When: LLM-judge evaluates `missing_direct_label`.
Then: judge flags the criterion. The drafter replaces the legend with inline
labels at line termini.

### TC8 — Full-criteria clean run produces audit summary

Given: a draft that passes all 16 criteria (9 mechanical + 7 LLM-judge).
When: the composer emits.
Then: audit summary contains theme name `infolog-io`, iteration count ≥1,
mechanical runs count, judge calls count, and an empty `resolved-during-loop`
list. Format matches `generator-critic/references/audit-summary-format.md`.

## Out of scope

- Visual regression screenshots comparing renders across theme versions.
- Automated palette-contrast matrix (manual check against `references/palette.md` is sufficient).
