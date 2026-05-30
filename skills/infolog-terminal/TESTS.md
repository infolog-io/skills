# infolog-terminal — Tests & End Conditions

## Profile

**Full-shape skill.** Theme bundle for `component-composer`. Sibling of
`infolog-io`. Shares token structure; differs in palette and criteria.

## End conditions (theme ships when all are true)

1. `themespec.json` resolves correctly when `component-composer` reads
   `skills/infolog-terminal/themespec.json`.
2. All 5 references declared in SKILL.md exist: `tokens.md`, `palette.md`,
   `criteria.md`, `patterns.md`, and `themespec.json`.
3. `references/palette.md` specifies a dark background and bright-green
   primary ink with concrete hex or CSS variable values.
4. `references/tokens.md` names every CSS variable that `palette.md`
   assigns a value to. No variable in palette is absent from tokens.
5. `references/criteria.md` includes at least one density-first criterion
   not present in the base `infolog-io` criteria.
6. A composition run invoking `infolog-terminal` as theme renders visually
   distinct output from the same data run under `infolog-io`.
7. README is ≤200 words.

## Test cases

### TC1 — Theme resolves from themespec.json

Given: user invokes `compose with infolog-terminal`.
When: `component-composer` reads `skills/infolog-terminal/themespec.json`.
Then: tokens, criteria, patterns, and palette load without error. Drafter
receives the terminal theme context before writing the first draft.
No `infolog-io` (light-theme) values bleed into this run.

### TC2 — Dark background enforced by token_compliance

Given: a draft artifact where a data container uses `background: #ffffff`
as a literal value outside `:root`.
When: `token_compliance` runs.
Then: `FAIL` — literal outside `:root`. The corrected draft assigns
`#ffffff` to a `:root` variable and references it via `var(--...)`.
On the next draft, the background resolves to the dark value from
`references/palette.md`.

### TC3 — Dense table pattern preferred over bar chart

Given: user asks to compose a tabular data summary under `infolog-terminal`.
When: drafter reads `references/patterns.md`.
Then: the drafter selects a monospace tabular layout over a bar or line chart.
The output contains no serifs, no drop-shadows, and no gradients (per
SKILL.md aesthetic rules).

### TC4 — Multi-theme proof: same data, visually different output

Given: the same dataset rendered once under `infolog-io` and once under
`infolog-terminal`.
When: both artifacts are produced.
Then: the `infolog-io` artifact uses the light Tufte-quiet palette.
The `infolog-terminal` artifact uses the dark green-on-black palette.
Both pass their respective theme's criteria. No criteria bleed across themes.

## Out of scope

- Visual regression screenshots comparing theme renders.
- Automated font-stack validation (manual check against `palette.md` is
  sufficient for v0.x).
