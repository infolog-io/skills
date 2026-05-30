# component-composer — Tests & End Conditions

## Profile

**Full-shape skill.** Consumes `generator-critic` for loop machinery.
Provides HTML-specific drafter, validator, mechanical checks, and theme
resolution. See `REGRESSION.md` for mechanical-layer defect classification.

## End conditions (skill ships when all are true)

1. Plugin installs cleanly via:
   ```
   /plugin install generator-critic@infolog-io
   /plugin install component-composer@infolog-io
   ```
2. Skill activates on every trigger phrase in SKILL.md (`/compose`,
   `compose with <theme>`, `render this chart with the design system`).
3. All reference files in SKILL.md exist at their stated paths (both
   composer-specific and inherited from `generator-critic`).
4. `scripts/mechanical-checks.js` exports 9 pure check functions.
   Each function is callable without a live browser (per `REGRESSION.md`).
5. A composition run with `infolog-io` theme completes the full loop:
   resolve → draft → render → HUD inject → validate → aggregate → emit.
6. Three-viewport validation runs at 375px, 768px, and 1280px without error.
7. Final emit produces HTML + PNG + PDF + audit summary.
8. README is ≤200 words.

## Test cases — compose→render loop

### TC1 — Theme resolves from themespec.json

Given: user invokes `compose with infolog-io`.
When: composer reads `skills/infolog-io/themespec.json`.
Then: tokens, criteria, patterns, and palette load without error. Drafter
receives theme context before writing the first draft.

### TC2 — Mechanical checks run at all three viewports

Given: a draft artifact is written to the session dir.
When: `preview_eval` dispatches mechanical checks.
Then: the validator runs all 9 checks at 375px, 768px, and 1280px.
Any failure at any viewport is included in the failure list passed to
the drafter.

### TC3 — text_collision detection (from REGRESSION.md)

Given: a draft with two `<text>` labels at coordinates `(50,100)` and
`(52,103)` with font-size 14 (bounding boxes overlap).
When: `mechanical-checks.js` runs `text_collision`.
Then: `FAIL` — `'Jan 2024' overlaps 'Jan 2024'`. Matches regression
fixture verdict in `REGRESSION.md`.

### TC4 — token_compliance detection (from REGRESSION.md)

Given: a draft where `.foo { color: #ff0000; }` appears outside `:root`.
When: `mechanical-checks.js` runs `token_compliance`.
Then: `FAIL` — literal hex outside `:root`. The drafter moves the value
into a CSS custom property on the next iteration.

### TC5 — LLM-judge runs on remaining criteria after mechanical pass

Given: mechanical checks all return `PASS` on a draft.
When: the validator dispatches LLM-as-judge for subjective criteria.
Then: judge evaluates the non-mechanical criteria from the active theme's
`criteria.md`. Failures feed back to the drafter identically to mechanical
failures (per `generator-critic/references/loop-protocol.md`).

### TC6 — Stuck detection surfaces to user

Given: two consecutive iterations produce identical failure sets.
When: the loop evaluates stuck state.
Then: HUD shows a "stuck" banner. The composer prompts the user via
`AskUserQuestion` (continue / abort / give guidance). The loop does not
iterate a third time without user input.

### TC7 — Clean run emits all four output artifacts

Given: a draft passes all active-theme criteria after N iterations.
When: the composer emits.
Then: four artifacts are present — HTML file, PNG (via `scripts/export-png.js`),
PDF (via `scripts/export-pdf.js`), and audit summary matching
`generator-critic/references/audit-summary-format.md`.

### TC8 — Skill does NOT activate on casual HTML requests

Given: user says "make me a throwaway editor for these tickets."
When: the composer evaluates whether to activate.
Then: the skill does not invoke `/compose`. The user receives guidance to
ask Claude directly or use `html-sketch`. (Per SKILL.md "When NOT to use.")

## Relationship to REGRESSION.md

`REGRESSION.md` documents three specific mechanical-layer defect types
(`text_collision`, `hidden_mark`, `token_compliance`) and their regression
fixtures. TC3–TC4 above reference those verdicts directly. Run the regression
suite before any change to `scripts/mechanical-checks.js`:

```
node skills/component-composer/scripts/regression-test.js
```

All 6 assertions must pass before shipping.
