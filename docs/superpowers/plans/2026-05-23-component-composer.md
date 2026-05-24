# Component Composer + atomic-data-viz Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a generator-critic loop that drafts single-file HTML data graphics, validates with hybrid mechanical+LLM-judge checks, and iterates until every active-theme criterion passes — implementing the composer skill, the atomic-data-viz theme (refactored from tufte-love), a second theme to prove multi-theme works, and the supporting components catalog.

**Architecture:** Three skills participate. `component-composer` is the loop orchestrator (drafter LLM + hybrid validator + HUD + iteration history + exports). `atomic-data-viz` is the first theme, supplying tokens/criteria/patterns/palette. `atomic-brand` gains a structural components catalog. `bloomberg-dense` is a scaffolded sibling theme proving the multi-theme architecture. All artifacts are zero-dependency single-file HTML in the `ThariqS/html-effectiveness` style.

**Tech Stack:** Plain HTML/CSS/SVG output (zero npm dependencies in the artifact). Vanilla JS for the in-loop HUD only. Mechanical validator scripts in ES modules executed via Claude Preview's `preview_eval`. Tests via Node.js built-in test runner (`node --test`). LLM orchestration described in markdown skill protocols; no Python or build pipeline.

**Goal doc reference:** [docs/superpowers/specs/2026-05-23-component-composer-goal.md](../specs/2026-05-23-component-composer-goal.md) — read this first if context is missing.

---

## File Structure

### `skills/component-composer/` (new skill)

| Path | Responsibility |
|---|---|
| `.claude-plugin/plugin.json` | Plugin manifest |
| `SKILL.md` | Skill entry; activation triggers + operating mode summary |
| `README.md` | Human-facing description |
| `references/drafter-protocol.md` | Drafter LLM behavior + input/output schema |
| `references/validator-protocol.md` | Hybrid validator behavior; mechanical→LLM-judge dispatch |
| `references/loop-protocol.md` | Loop steps, stuck detection, audit summary format |
| `references/theme-spec.md` | Theme interface contract |
| `references/output-style.md` | Single-file HTML style anchor (html-effectiveness reference) |
| `references/hud-protocol.md` | HUD injection + polling protocol |
| `scripts/mechanical-checks.js` | 9 pure check functions + browser adapter |
| `scripts/mechanical-checks.test.js` | Unit tests using `node --test` |
| `scripts/hud.js` | HUD code injected during iteration |
| `scripts/export-png.js` | PNG export via `preview_screenshot` |
| `scripts/export-pdf.js` | PDF export via `window.print()` trigger |
| `template/base.html` | HTML skeleton with token slots |
| `template/fixtures/` | Synthetic HTML fixtures used by mechanical-check tests |

### `skills/atomic-data-viz/` (rename from `skills/tufte-love/`)

| Path | Responsibility |
|---|---|
| `.claude-plugin/plugin.json` | Updated plugin manifest with new name |
| `SKILL.md` | Theme declaration (much shorter than current tufte-love SKILL.md) |
| `themespec.json` | Theme manifest |
| `references/tokens.md` | CSS variable schema (new) |
| `references/palette.md` | Concrete palette values (new) |
| `references/criteria.md` | Validator rules (new, from audit-rubric.md) |
| `references/patterns.md` | Preferred chart patterns (new) |
| `references/principles.md` | Renamed from `tufte-principles.md` |
| `references/analytical-design.md` | Kept |
| `references/chart-patterns.md` | Kept supplementary |
| `references/chart-rules-extras.md` | Kept supplementary |
| (delete) `references/audit-rubric.md` | Folded into criteria.md + principles.md |
| (delete) `references/color-palette.md` | Folded into palette.md |

### `skills/atomic-brand/` (extend existing)

| Path | Responsibility |
|---|---|
| `references/components.md` | NEW: 9 structural components (axis, legend, annotation, sparkline, data-mark, table-row, small-multiple-cell, slopegraph-line, strip-plot-tick) |

### `skills/bloomberg-dense/` (new sibling theme)

| Path | Responsibility |
|---|---|
| `.claude-plugin/plugin.json` | Plugin manifest |
| `SKILL.md` | Theme declaration |
| `themespec.json` | Theme manifest |
| `references/tokens.md` | CSS variable schema (terminal aesthetic) |
| `references/palette.md` | Green-on-black palette |
| `references/criteria.md` | Density-first validator rules |
| `references/patterns.md` | Dense-table-first patterns |

### Marketplace + repo updates

| Path | Responsibility |
|---|---|
| `marketplace.json` | Register the three new/refactored skills |
| `README.md` (repo root) | Update plugin list |

---

## Phase 1 — component-composer skill scaffold

### Task 1: Create component-composer directory + plugin.json

**Files:**
- Create: `skills/component-composer/.claude-plugin/plugin.json`

- [ ] **Step 1: Create the directory structure**

```bash
mkdir -p skills/component-composer/.claude-plugin \
         skills/component-composer/references \
         skills/component-composer/scripts \
         skills/component-composer/template/fixtures
```

- [ ] **Step 2: Write `plugin.json`**

```json
{
  "name": "component-composer",
  "version": "1.0.0",
  "description": "Generator-critic loop: drafts a single-file HTML artifact, validates with mechanical + LLM-judge checks, iterates until every active-theme criterion passes.",
  "author": {
    "name": "Information Logistics",
    "email": "bdl@infolog.io"
  }
}
```

- [ ] **Step 3: Commit**

```bash
git add skills/component-composer
git commit -m "feat(component-composer): scaffold skill directory + plugin manifest"
```

### Task 2: Write SKILL.md

**Files:**
- Create: `skills/component-composer/SKILL.md`

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: component-composer
description: >
  Generator-critic loop for single-file HTML artifacts. Drafts via theme,
  renders in Claude Preview, validates with hybrid mechanical + LLM-as-judge
  checks at three viewports, iterates until every active-theme criterion
  passes. Activates on "compose with <theme>", "render this chart",
  "/compose", or any data-graphics composition request that names a theme.
---

# component-composer

## Purpose

Build single-file HTML data graphics through a generator-critic loop. The
drafter writes HTML; the validator critiques the rendered output; the
composer feeds failures back to the drafter and iterates until clean.

Themes own the quality criteria. The composer is theme-agnostic.

## Operating mode

When invoked with a job + theme name:

1. **Resolve theme** — read `skills/<theme>/themespec.json` and load the
   theme's `tokens.md`, `criteria.md`, `patterns.md`, `palette.md`.
2. **Draft** — invoke the drafter per `references/drafter-protocol.md`.
3. **Render** — write artifact to session dir; render via Claude Preview.
4. **Inject HUD** — overlay `scripts/hud.js` per `references/hud-protocol.md`.
5. **Validate** — run mechanical checks via `preview_eval`, then LLM-as-judge
   for the rest, per `references/validator-protocol.md`. Repeat at three
   viewports (mobile 375 / tablet 768 / desktop 1280).
6. **Aggregate failures** — per `references/loop-protocol.md`.
7. **Loop** — if any failure, feed back to drafter and goto step 2.
   If stuck, surface to user via HUD + chat.
8. **Emit** — final HTML + PNG (via `scripts/export-png.js`) + PDF (via
   `scripts/export-pdf.js`) + audit summary + iteration history.

## References

- `references/drafter-protocol.md` — drafter LLM behavior
- `references/validator-protocol.md` — hybrid validator behavior
- `references/loop-protocol.md` — loop steps, stuck detection, audit format
- `references/theme-spec.md` — theme interface contract
- `references/output-style.md` — single-file HTML style anchor
- `references/hud-protocol.md` — HUD injection + state polling

## Scripts

- `scripts/mechanical-checks.js` — 9 pure validator check functions
- `scripts/hud.js` — in-loop HUD overlay (vanilla JS)
- `scripts/export-png.js` — PNG export
- `scripts/export-pdf.js` — PDF export

## Template

- `template/base.html` — HTML skeleton with `:root` token slots
```

- [ ] **Step 2: Commit**

```bash
git add skills/component-composer/SKILL.md
git commit -m "feat(component-composer): add SKILL.md"
```

### Task 3: Write README.md

**Files:**
- Create: `skills/component-composer/README.md`

- [ ] **Step 1: Write README**

```markdown
# component-composer

Generator-critic loop for single-file HTML data graphics.

The composer drafts an artifact via an LLM drafter, renders it in Claude
Preview, validates with mechanical + LLM-judge checks at three viewports,
and iterates until every active-theme criterion passes. Themes own the
quality bar. Output is one self-contained HTML file with optional PNG +
PDF exports.

See `SKILL.md` for operating mode. See `references/` for protocol details.

Themes: `atomic-data-viz` (Tufte-style) and `bloomberg-dense` (terminal
aesthetic) ship as sibling skills.
```

- [ ] **Step 2: Commit**

```bash
git add skills/component-composer/README.md
git commit -m "docs(component-composer): add README"
```

### Task 4: Write `references/output-style.md`

**Files:**
- Create: `skills/component-composer/references/output-style.md`

- [ ] **Step 1: Write output-style.md**

```markdown
# Output Style — Single-File HTML

The drafter's output is one self-contained `.html` file. No build step.
No npm dependencies. No external requests. The artifact must open
correctly when the user double-clicks it on any modern browser, online
or offline.

Style anchor: `ThariqS/html-effectiveness` — a gallery of single-file
HTML examples demonstrating how much fidelity a static file can carry.

## Required structure

1. `<!DOCTYPE html>` + `<html lang="en">` + `<meta charset>` + viewport meta.
2. Inline `<style>` in `<head>`. **All** styling lives here.
3. CSS custom properties declared on `:root` — every color, type size,
   spacing, and radius is a `var(--...)` reference. No literal hex codes
   or px values outside the `:root` block.
4. The body uses semantic HTML — `<header>`, `<section>`, `<table>`,
   `<figure>` — not generic `<div>` soup.
5. Inline `<svg>` for every chart. No `<img>` for chart content.
6. Vanilla `<script>` only when interaction is real (theme switcher,
   tooltips, filtering). No external libraries. No `import` statements.

## Required token vocabulary (declared on `:root`)

Theme `tokens.md` files declare which of these are required for that
theme. The composer enforces presence via the `token_compliance`
mechanical check.

- `--paper`, `--paper-soft` — surfaces
- `--ink`, `--ink-soft` — text/data
- `--accent-warm`, `--accent-cool`, `--accent-quiet` — highlights
- `--gray-100` through `--gray-900` — neutral ramp
- `--serif`, `--sans`, `--mono` — font families
- `--font-size-h1` through `--font-size-caption` — type scale
- `--space-1` through `--space-12` — spacing scale
- `--radius-panel`, `--border` — structural

## Required class conventions

Themes may add more, but the drafter always uses these structural classes:

- `.page` — max-width container
- `.figure` — wraps an SVG chart + caption
- `.data-table` — quantitative tables
- `.annotation` — callouts and notes
- `.axis`, `.tick`, `.tick-label`, `.data-mark` — SVG chart parts

## Forbidden in artifact

- External fonts, scripts, stylesheets, images.
- `<link rel="stylesheet">` to anything.
- CSS frameworks (Bootstrap, Tailwind utility classes if not generated).
- `import` / `require` / `from` JS module syntax.
- Build-tool comments (`/* eslint */`, `/* @ts-ignore */`).

## File size guideline

Target 12-30KB for a complete chart page. The html-effectiveness gallery
files range 12-28KB. Above 50KB suggests embedded base64 images or
chartjunk — investigate before shipping.

## Why this style

The artifact is portable. It survives email, paste, Slack, archive.org.
It opens offline. It's reviewable in a diff. It can be edited by humans.
A React build is none of these.
```

- [ ] **Step 2: Commit**

```bash
git add skills/component-composer/references/output-style.md
git commit -m "docs(component-composer): add output-style protocol"
```

### Task 5: Write `references/theme-spec.md`

**Files:**
- Create: `skills/component-composer/references/theme-spec.md`

- [ ] **Step 1: Write theme-spec.md**

```markdown
# Theme Spec — Interface Contract

A skill conforms to the theme-spec interface by providing:

```
skills/<theme-name>/
  SKILL.md                    declares itself as a theme
  themespec.json              machine-readable manifest
  references/
    tokens.md                 CSS variable schema (which vars, what they mean)
    palette.md                concrete palette values
    criteria.md               validator rules
    patterns.md               preferred component patterns
    principles.md             (optional) foundational reference
```

## themespec.json schema

```json
{
  "name": "atomic-data-viz",
  "version": "1.0.0",
  "context": "data-graphics",
  "capabilities": ["chart", "table", "sparkline", "small-multiples"],
  "output_formats": ["html", "png", "pdf"],
  "style_anchor": "single-file-html"
}
```

Required fields: `name`, `version`, `context`, `output_formats`.

## tokens.md

Markdown with one section per token category. Each section declares which
CSS variables that theme uses and what role they play. Example:

```markdown
## Color

| Variable | Role |
|---|---|
| `--paper` | primary background |
| `--ink` | primary text/data |
| `--accent-warm` | single highlight (90% gray + 10% color rule) |
```

The composer reads tokens.md to know which variables the artifact must
declare on `:root`. The `token_compliance` mechanical check enforces it.

## palette.md

Concrete values. Example:

```markdown
## Color values

```css
:root {
  --paper: #fafaf7;
  --ink: #1a1a1a;
  --accent-warm: #c8553d;
}
```
```

## criteria.md

Each criterion has an id (markdown H2) and a check description (prose).
No severity, no priority. The composer concatenates all criteria into the
LLM-judge prompt; the mechanical layer dispatches by id.

```markdown
## text_collision

No text labels overlap each other or data marks.

## missing_range_frame

Axis terminates at data extent, not arbitrary round numbers.
```

## patterns.md

Preferred component patterns. The drafter reads these before composing.

```markdown
## Time-series → line, not bar

Lines preserve sequence; bars imply discreteness.

## Many-to-many comparison → small multiples

A single overloaded chart with N colors fails. N panels with identical
encoding succeeds.
```

## Theme discovery

The composer scans `skills/*/themespec.json` at session start. Themes are
keyed by `name`. The user names a theme; composer resolves and loads.
```

- [ ] **Step 2: Commit**

```bash
git add skills/component-composer/references/theme-spec.md
git commit -m "docs(component-composer): add theme-spec interface contract"
```

### Task 6: Write `references/drafter-protocol.md`

**Files:**
- Create: `skills/component-composer/references/drafter-protocol.md`

- [ ] **Step 1: Write drafter-protocol.md**

```markdown
# Drafter Protocol

The drafter is an LLM agent that emits a single self-contained HTML file
matching the active theme's tokens, patterns, and criteria.

## Iteration 1 input

The drafter receives:

1. **Job description** — what the user asked for (e.g., "render this
   GitHub usage data as a Tufte-style chart page").
2. **Data** — the raw dataset (JSON, CSV, or inline values).
3. **Theme tokens** — the contents of `<theme>/references/tokens.md`.
4. **Theme palette** — the contents of `<theme>/references/palette.md`.
5. **Theme patterns** — the contents of `<theme>/references/patterns.md`.
6. **Theme criteria** — the contents of `<theme>/references/criteria.md`.
7. **Output style** — the contents of `output-style.md`.
8. **Template** — the contents of `template/base.html` as a starting
   point (the drafter may modify freely).

## Iteration N input (N > 1)

All iteration-1 inputs plus:

1. **Previous artifact source** — the full HTML from iteration N-1,
   verbatim.
2. **Validator failure list (JSON)** — every `{ id, result: "fail",
   viewport, evidence, suggested_fix }` from validator-protocol's
   output schema.
3. **Composer NL summary** — composer-generated. One line per failure:

   > "On `<viewport>`, criterion `<id>` failed. Evidence: `<evidence>`.
   > Suggested fix: `<suggested_fix>`."

## Output

One HTML file matching `output-style.md`. Nothing else — no preamble,
no explanation, no markdown wrapper.

## Drafter behavior rules

1. **Token discipline.** Every color, font-size, spacing, and radius
   in the output uses a `var(--...)` reference. Literal values appear
   only inside `:root`.
2. **Pattern selection.** The drafter consults `patterns.md` before
   choosing a chart type. When a pattern fits, use it.
3. **Fail-fixing precedence.** On iteration N, the drafter addresses
   every failure in the JSON list. If two failures conflict (e.g., one
   suggests larger text, another suggests denser layout), the drafter
   resolves toward the theme's `principles.md` — or, when ambiguous,
   prefers truthfulness and comparison over density.
4. **No new failures.** When fixing one failure, do not introduce
   another. Verify the broader artifact mentally before emitting.
5. **Preserve intent.** Do not rewrite the entire artifact between
   iterations unless the previous structure is unsalvageable. Prefer
   surgical edits.
```

- [ ] **Step 2: Commit**

```bash
git add skills/component-composer/references/drafter-protocol.md
git commit -m "docs(component-composer): add drafter protocol"
```

### Task 7: Write `references/validator-protocol.md`

**Files:**
- Create: `skills/component-composer/references/validator-protocol.md`

- [ ] **Step 1: Write validator-protocol.md**

```markdown
# Validator Protocol

The validator runs after each draft to check whether the rendered artifact
satisfies the active theme's criteria.

## Two-layer hybrid

### Mechanical layer

Pure functions in `scripts/mechanical-checks.js`. Each check has a
criterion id and returns the shared validator output shape. The browser
adapter (`runInBrowser`) extracts DOM data via `getBoundingClientRect`,
`getComputedStyle`, etc., and dispatches to the pure check function.

Built-in mechanical check registry (criterion id → check function):

| id | What it measures |
|---|---|
| `text_collision` | Pairwise bounding-box overlap across text/label nodes |
| `text_truncation` | `scrollWidth > clientWidth` on text containers |
| `contrast_failure` | WCAG ratio computed from text + background colors |
| `font_size_too_small` | Computed `font-size` below 10px display (after viewBox scaling) |
| `overflow` | Body/figure `scrollWidth > clientWidth` per viewport |
| `responsive_break` | Horizontal scroll present at mobile viewport |
| `chartjunk_decorative_css` | `box-shadow`, `text-shadow`, gradient `background`, 3D `transform` on data marks |
| `hidden_mark` | Marks with `width`/`height` < 2px or `opacity` < 0.3 |
| `token_compliance` | Every CSS color/spacing/font value resolves to a `var(--...)` reference, not a literal |

### LLM-as-judge layer

A vision LLM call. Receives the screenshot + the subset of theme criteria
without a built-in mechanical check + the viewport label. Returns the same
output shape.

### Dispatch rule

For each criterion in the active theme's `criteria.md`:

1. If a built-in mechanical check exists for this criterion id, run it
   first. Trust the result.
2. If the mechanical check throws or returns an error, fall back to LLM-as-
   judge for this criterion.
3. If no built-in mechanical check exists for this criterion id, use
   LLM-as-judge.

## Run per viewport

The composer resizes Claude Preview to each of `{mobile: 375, tablet: 768,
desktop: 1280}` × default height, then runs the validator. Three runs
per iteration total.

## Output schema

Per viewport, the validator returns:

```json
[
  {
    "id": "text_collision",
    "result": "pass",
    "viewport": "mobile"
  },
  {
    "id": "chartjunk_present",
    "result": "fail",
    "viewport": "mobile",
    "evidence": "drop shadows on each bar",
    "suggested_fix": "remove box-shadow; rely on position alone"
  }
]
```

## Aggregation

After all three viewport runs, the composer concatenates the failure lists
verbatim with viewport label preserved. Same criterion failing on multiple
viewports appears multiple times in the aggregated list. No deduplication —
the drafter needs per-viewport context.

## LLM-judge prompt template

The vision LLM is invoked with the following prompt structure:

```
You are a visual auditor for data graphics. The active theme is <theme-name>.

Below is the theme's criteria. For each criterion id that I list as
"check this", evaluate the screenshot. Return ONLY a JSON array matching
this schema:

[{"id": "...", "result": "pass" | "fail", "viewport": "<viewport>",
  "evidence": "...", "suggested_fix": "..."}]

Criteria to check (theme: <theme-name>):

<concatenated criteria.md content for criteria without built-in mechanical>

Viewport: <viewport>

Screenshot attached.
```
```

- [ ] **Step 2: Commit**

```bash
git add skills/component-composer/references/validator-protocol.md
git commit -m "docs(component-composer): add validator protocol"
```

### Task 8: Write `references/loop-protocol.md`

**Files:**
- Create: `skills/component-composer/references/loop-protocol.md`

- [ ] **Step 1: Write loop-protocol.md**

```markdown
# Loop Protocol

The composer's main control loop.

## Steps

```
1. Drafter composes initial artifact (per drafter-protocol.md)
2. Composer writes file to <session-dir>/iterations/iter-01.html
3. Composer starts Claude Preview serving <session-dir>
4. Composer injects HUD (per hud-protocol.md)
5. For viewport in [mobile, tablet, desktop]:
     a. Resize Claude Preview to that viewport
     b. preview_screenshot → save to iter-01-<viewport>.png
     c. Run mechanical checks via preview_eval
     d. Run LLM-judge for remaining criteria
     e. Append failure list to iter-01.json
6. Aggregate failure list across viewports
7. If empty → SUCCESS:
     - Strip HUD from artifact (per hud-protocol.md)
     - Save final HTML as final.html
     - Run export-png.js → final.png
     - Run export-pdf.js → final.pdf
     - Emit audit summary
     - Loop ends
8. Otherwise:
     - Composer generates NL summary of failures
     - Feed failures (JSON) + NL summary back to drafter
     - Drafter redrafts → iter-NN.html
     - goto step 3 (but reuse already-running Claude Preview)
```

## Stuck detection

If `set(failure_ids_at_iter_N) == set(failure_ids_at_iter_N-1)`, treat
as stuck. Composer:

1. Updates HUD with "stuck" banner showing the persisting failure ids.
2. Surfaces a chat prompt via `AskUserQuestion`:

   > Stuck on [criterion-ids] at [viewports]. Keep iterating, abort, or
   > give guidance?

User options:
- **Keep iterating** → loop continues, stuck count resets only on
  progress.
- **Abort** → loop halts; current iter-NN.html becomes final.
- **Give guidance** → user types a hint via chat or HUD textarea; the
  hint is appended to the drafter's iteration N+1 prompt as a system
  note.

## No hard iteration cap

The loop runs until pass, until stuck-with-abort, or until user
interrupt.

## Audit summary format

Emitted on success or abort:

```text
Composer audit
- Theme: atomic-data-viz v1.0.0
- Iterations: 4
- Final result: pass
- Drafter calls: 4 (~12K tokens in, ~8K tokens out)
- LLM-judge calls: 12 (3 viewports × 4 iterations, ~24K tokens total)
- Mechanical-check runs: 36 (9 checks × 3 viewports × 4 iter), avg 80ms
- Wallclock: 1m 42s
- Viewports: mobile, tablet, desktop
- Resolved during loop: text_collision (iter 2), chartjunk (iter 3),
  missing_range_frame (iter 4)
- Persistent history: <session-dir>/iterations/
- Final artifact: <session-dir>/final.html
- Exports: <session-dir>/final.png, <session-dir>/final.pdf
```

## Cost tracking implementation

The composer maintains a counters object per session:

```json
{
  "drafter": { "calls": 0, "tokens_in": 0, "tokens_out": 0 },
  "judge":   { "calls": 0, "tokens_in": 0, "tokens_out": 0 },
  "mechanical": { "runs": 0, "ms_total": 0 },
  "wallclock_ms": 0
}
```

Increment on each call. Surface in the audit summary at end.
```

- [ ] **Step 2: Commit**

```bash
git add skills/component-composer/references/loop-protocol.md
git commit -m "docs(component-composer): add loop protocol"
```

### Task 9: Write `references/hud-protocol.md`

**Files:**
- Create: `skills/component-composer/references/hud-protocol.md`

- [ ] **Step 1: Write hud-protocol.md**

```markdown
# HUD Protocol

A vanilla-JS overlay injected into the rendered artifact while the loop
runs. The HUD shows iteration count + current failures + intervention
buttons. The HUD is stripped from the final artifact.

## Injection

After writing iter-NN.html, the composer appends to the rendered DOM (via
`preview_eval`) the contents of `scripts/hud.js`. The script:

1. Creates a fixed-position `<div id="__composer_hud">` at the top-right
   of the viewport.
2. Renders: iteration count, pass/fail counts, currently-failing criteria
   list, three buttons (continue / abort / give guidance), and a textarea
   for guidance.
3. Initializes `window.__composer_state = { command: null, guidance: "" }`.
4. Wires button clicks → write to `window.__composer_state.command`.

## State polling

Between iterations, before invoking the drafter again, the composer reads
`window.__composer_state` via:

```js
preview_eval(`JSON.stringify(window.__composer_state)`)
```

The composer reacts:
- `command === "continue"` (or `null`) → proceed to next iteration.
- `command === "abort"` → exit loop, treat current iter-NN as final.
- `command === "guidance"` → append `state.guidance` to the drafter's
  next-iteration prompt.

## HUD update across iterations

After each iteration's validation, composer updates HUD content via
`preview_eval`:

```js
preview_eval(`
  window.__composer_update({
    iteration: 3,
    failures: [{id: "text_collision", viewport: "mobile"}, ...],
    stuck: false
  })
`)
```

The HUD script exposes `window.__composer_update` for the composer.

## Stripping from final

On SUCCESS, after copying iter-NN.html to final.html, the composer removes
the HUD `<script>` tag and `<div id="__composer_hud">` element via regex
from final.html. The artifact then has zero loop scaffolding.

## HUD styling

The HUD uses a fixed, semi-transparent dark panel with white text. Never
the active theme's colors — the HUD is a tool, not part of the artifact's
aesthetic. Z-index 99999 to float above all content.
```

- [ ] **Step 2: Commit**

```bash
git add skills/component-composer/references/hud-protocol.md
git commit -m "docs(component-composer): add hud protocol"
```

### Task 10: Register component-composer in marketplace.json

**Files:**
- Modify: `marketplace.json`

- [ ] **Step 1: Read current marketplace.json**

Run: `cat marketplace.json`

- [ ] **Step 2: Add component-composer entry**

Add an entry under the plugins array (preserving existing entries):

```json
{
  "name": "component-composer",
  "source": "./skills/component-composer",
  "version": "1.0.0",
  "description": "Generator-critic loop for single-file HTML data graphics."
}
```

- [ ] **Step 3: Commit**

```bash
git add marketplace.json
git commit -m "feat(marketplace): register component-composer"
```

---

## Phase 2 — Mechanical validator (TDD)

For each of the 9 mechanical checks, the cycle is: write test, run-fail,
implement, run-pass, commit. Each check is a pure function that takes
extracted DOM data (as plain objects) and returns the validator output
shape. A separate `runInBrowser` adapter handles DOM extraction.

### Task 11: Set up the mechanical-checks test scaffold

**Files:**
- Create: `skills/component-composer/scripts/mechanical-checks.js`
- Create: `skills/component-composer/scripts/mechanical-checks.test.js`

- [ ] **Step 1: Write the empty checks module**

```js
// skills/component-composer/scripts/mechanical-checks.js
//
// Mechanical validator checks. Each exported function is pure: takes
// extracted DOM data (as plain objects) + theme context, returns the
// validator output shape:
//
//   { id, result: 'pass' | 'fail', viewport,
//     evidence?: string, suggested_fix?: string }
//
// The runInBrowser adapter (bottom of file) extracts DOM data via
// browser APIs and dispatches to these functions.

export const CHECKS = {};

export function runInBrowser(criterionId, viewport) {
  throw new Error('not implemented yet');
}
```

- [ ] **Step 2: Write the test scaffold**

```js
// skills/component-composer/scripts/mechanical-checks.test.js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { CHECKS } from './mechanical-checks.js';

test('scaffold sanity', () => {
  assert.equal(typeof CHECKS, 'object');
});
```

- [ ] **Step 3: Run test, verify pass**

```bash
cd skills/component-composer/scripts
node --test mechanical-checks.test.js
```

Expected: 1 test passing.

- [ ] **Step 4: Commit**

```bash
git add skills/component-composer/scripts/
git commit -m "feat(mechanical-checks): scaffold module + test runner"
```

### Task 12: Implement `text_collision` (TDD)

**Files:**
- Modify: `skills/component-composer/scripts/mechanical-checks.js`
- Modify: `skills/component-composer/scripts/mechanical-checks.test.js`

- [ ] **Step 1: Write failing tests**

Append to `mechanical-checks.test.js`:

```js
test('text_collision: pass when no boxes overlap', () => {
  const result = CHECKS.text_collision({
    boxes: [
      { x: 0, y: 0, w: 50, h: 20, text: 'A' },
      { x: 100, y: 0, w: 50, h: 20, text: 'B' }
    ],
    viewport: 'mobile'
  });
  assert.equal(result.id, 'text_collision');
  assert.equal(result.result, 'pass');
  assert.equal(result.viewport, 'mobile');
});

test('text_collision: fail when two boxes overlap', () => {
  const result = CHECKS.text_collision({
    boxes: [
      { x: 0, y: 0, w: 50, h: 20, text: '2025' },
      { x: 40, y: 10, w: 50, h: 20, text: 'Dec' }
    ],
    viewport: 'mobile'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /2025.*Dec|Dec.*2025/);
  assert.ok(result.suggested_fix);
});

test('text_collision: pass on empty input', () => {
  const result = CHECKS.text_collision({ boxes: [], viewport: 'desktop' });
  assert.equal(result.result, 'pass');
});
```

- [ ] **Step 2: Run tests, verify failure**

```bash
node --test mechanical-checks.test.js
```

Expected: 3 failures with "CHECKS.text_collision is not a function".

- [ ] **Step 3: Implement**

Edit `mechanical-checks.js`:

```js
function overlaps(a, b) {
  return !(a.x + a.w <= b.x || b.x + b.w <= a.x ||
           a.y + a.h <= b.y || b.y + b.h <= a.y);
}

CHECKS.text_collision = function ({ boxes, viewport }) {
  for (let i = 0; i < boxes.length; i++) {
    for (let j = i + 1; j < boxes.length; j++) {
      if (overlaps(boxes[i], boxes[j])) {
        return {
          id: 'text_collision',
          result: 'fail',
          viewport,
          evidence: `'${boxes[i].text}' overlaps '${boxes[j].text}'`,
          suggested_fix: `move or shorten one of the labels`
        };
      }
    }
  }
  return { id: 'text_collision', result: 'pass', viewport };
};
```

- [ ] **Step 4: Run tests, verify pass**

```bash
node --test mechanical-checks.test.js
```

Expected: 4 tests passing (3 new + scaffold).

- [ ] **Step 5: Commit**

```bash
git add skills/component-composer/scripts/
git commit -m "feat(mechanical-checks): implement text_collision"
```

### Task 13: Implement `text_truncation` (TDD)

**Files:**
- Modify: `skills/component-composer/scripts/mechanical-checks.{js,test.js}`

- [ ] **Step 1: Write failing tests**

```js
test('text_truncation: pass when scrollWidth fits clientWidth', () => {
  const result = CHECKS.text_truncation({
    elements: [{ scrollWidth: 100, clientWidth: 120, text: 'short' }],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'pass');
});

test('text_truncation: fail when scrollWidth exceeds clientWidth', () => {
  const result = CHECKS.text_truncation({
    elements: [{ scrollWidth: 200, clientWidth: 100, text: 'a-very-long-label' }],
    viewport: 'mobile'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /a-very-long-label/);
});
```

- [ ] **Step 2: Run-fail.** `node --test mechanical-checks.test.js` → 2 failures.

- [ ] **Step 3: Implement**

```js
CHECKS.text_truncation = function ({ elements, viewport }) {
  const truncated = elements.filter(e => e.scrollWidth > e.clientWidth);
  if (truncated.length === 0) {
    return { id: 'text_truncation', result: 'pass', viewport };
  }
  return {
    id: 'text_truncation',
    result: 'fail',
    viewport,
    evidence: `truncated: ${truncated.map(e => `'${e.text}'`).join(', ')}`,
    suggested_fix: 'shorten the label, increase container width, or use abbreviation'
  };
};
```

- [ ] **Step 4: Run-pass.** All tests pass.

- [ ] **Step 5: Commit.**

```bash
git commit -am "feat(mechanical-checks): implement text_truncation"
```

### Task 14: Implement `contrast_failure` (TDD)

**Files:**
- Modify: `skills/component-composer/scripts/mechanical-checks.{js,test.js}`

- [ ] **Step 1: Write failing tests**

```js
test('contrast_failure: pass when text contrast ≥ 4.5:1', () => {
  // black on white: ~21:1
  const result = CHECKS.contrast_failure({
    pairs: [{ kind: 'text', fg: '#000000', bg: '#ffffff', sample: 'h1 title' }],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'pass');
});

test('contrast_failure: fail when text contrast < 4.5:1', () => {
  // light gray on white: ~2.5:1
  const result = CHECKS.contrast_failure({
    pairs: [{ kind: 'text', fg: '#bbbbbb', bg: '#ffffff', sample: 'body' }],
    viewport: 'mobile'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /body/);
});

test('contrast_failure: pass when mark contrast ≥ 3:1', () => {
  // mid-gray mark on white: ~4.5:1
  const result = CHECKS.contrast_failure({
    pairs: [{ kind: 'mark', fg: '#888888', bg: '#ffffff', sample: 'data-mark' }],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'pass');
});

test('contrast_failure: fail when mark contrast < 3:1', () => {
  const result = CHECKS.contrast_failure({
    pairs: [{ kind: 'mark', fg: '#dddddd', bg: '#ffffff', sample: 'data-mark' }],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'fail');
});
```

- [ ] **Step 2: Run-fail.**

- [ ] **Step 3: Implement**

```js
function relLuminance(hex) {
  // Strip # and parse RGB
  const h = hex.replace('#', '');
  const r = parseInt(h.substring(0, 2), 16) / 255;
  const g = parseInt(h.substring(2, 4), 16) / 255;
  const b = parseInt(h.substring(4, 6), 16) / 255;
  const lin = (c) => c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
}

function contrastRatio(fg, bg) {
  const L1 = relLuminance(fg);
  const L2 = relLuminance(bg);
  const lighter = Math.max(L1, L2);
  const darker  = Math.min(L1, L2);
  return (lighter + 0.05) / (darker + 0.05);
}

CHECKS.contrast_failure = function ({ pairs, viewport }) {
  const fails = pairs.filter(p => {
    const ratio = contrastRatio(p.fg, p.bg);
    const threshold = p.kind === 'text' ? 4.5 : 3.0;
    return ratio < threshold;
  });
  if (fails.length === 0) {
    return { id: 'contrast_failure', result: 'pass', viewport };
  }
  return {
    id: 'contrast_failure',
    result: 'fail',
    viewport,
    evidence: fails.map(p => {
      const r = contrastRatio(p.fg, p.bg).toFixed(2);
      return `${p.sample} (${p.kind}): ${p.fg} on ${p.bg} = ${r}:1`;
    }).join('; '),
    suggested_fix: 'darken the foreground or lighten the background until threshold passes'
  };
};
```

- [ ] **Step 4: Run-pass.**

- [ ] **Step 5: Commit.**

```bash
git commit -am "feat(mechanical-checks): implement contrast_failure"
```

### Task 15: Implement `font_size_too_small` (TDD)

**Files:**
- Modify: `skills/component-composer/scripts/mechanical-checks.{js,test.js}`

- [ ] **Step 1: Write failing tests**

```js
test('font_size_too_small: pass when display size ≥ 10px', () => {
  const result = CHECKS.font_size_too_small({
    elements: [{ tag: 'text', computedFontPx: 14, displayFontPx: 14, sample: 'tick' }],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'pass');
});

test('font_size_too_small: fail when display size < 10px', () => {
  const result = CHECKS.font_size_too_small({
    // SVG text at font-size:11 inside viewBox=360 rendered at width=180 → 5.5px effective
    elements: [{ tag: 'text', computedFontPx: 11, displayFontPx: 5.5, sample: 'lang label' }],
    viewport: 'mobile'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /5\.5/);
});
```

- [ ] **Step 2: Run-fail.**

- [ ] **Step 3: Implement**

```js
CHECKS.font_size_too_small = function ({ elements, viewport }) {
  const fails = elements.filter(e => e.displayFontPx < 10);
  if (fails.length === 0) {
    return { id: 'font_size_too_small', result: 'pass', viewport };
  }
  return {
    id: 'font_size_too_small',
    result: 'fail',
    viewport,
    evidence: fails.map(e =>
      `'${e.sample}' renders at ${e.displayFontPx.toFixed(1)}px (computed ${e.computedFontPx}px)`
    ).join('; '),
    suggested_fix: 'increase font-size, or widen container/SVG to reduce viewBox downscale'
  };
};
```

- [ ] **Step 4: Run-pass.**

- [ ] **Step 5: Commit.**

```bash
git commit -am "feat(mechanical-checks): implement font_size_too_small"
```

### Task 16: Implement `overflow` (TDD)

**Files:**
- Modify: `skills/component-composer/scripts/mechanical-checks.{js,test.js}`

- [ ] **Step 1: Write failing tests**

```js
test('overflow: pass when no container overflows', () => {
  const result = CHECKS.overflow({
    containers: [
      { selector: 'body', scrollWidth: 375, clientWidth: 375 },
      { selector: '.figure', scrollWidth: 350, clientWidth: 360 }
    ],
    viewport: 'mobile'
  });
  assert.equal(result.result, 'pass');
});

test('overflow: fail when a container overflows horizontally', () => {
  const result = CHECKS.overflow({
    containers: [
      { selector: 'body', scrollWidth: 400, clientWidth: 375 }
    ],
    viewport: 'mobile'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /body/);
});
```

- [ ] **Step 2: Run-fail.**

- [ ] **Step 3: Implement**

```js
CHECKS.overflow = function ({ containers, viewport }) {
  const fails = containers.filter(c => c.scrollWidth > c.clientWidth);
  if (fails.length === 0) {
    return { id: 'overflow', result: 'pass', viewport };
  }
  return {
    id: 'overflow',
    result: 'fail',
    viewport,
    evidence: fails.map(c =>
      `'${c.selector}': scrollWidth=${c.scrollWidth} > clientWidth=${c.clientWidth}`
    ).join('; '),
    suggested_fix: 'shrink content, increase container max-width, or wrap long lines'
  };
};
```

- [ ] **Step 4: Run-pass.**

- [ ] **Step 5: Commit.**

```bash
git commit -am "feat(mechanical-checks): implement overflow"
```

### Task 17: Implement `responsive_break` (TDD)

**Files:**
- Modify: `skills/component-composer/scripts/mechanical-checks.{js,test.js}`

- [ ] **Step 1: Write failing tests**

```js
test('responsive_break: pass at desktop regardless', () => {
  const result = CHECKS.responsive_break({
    documentScrollWidth: 1400, viewportWidth: 1280, viewport: 'desktop'
  });
  assert.equal(result.result, 'pass');
});

test('responsive_break: pass at mobile when no horizontal scroll', () => {
  const result = CHECKS.responsive_break({
    documentScrollWidth: 375, viewportWidth: 375, viewport: 'mobile'
  });
  assert.equal(result.result, 'pass');
});

test('responsive_break: fail at mobile when horizontal scroll', () => {
  const result = CHECKS.responsive_break({
    documentScrollWidth: 500, viewportWidth: 375, viewport: 'mobile'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /500.*375|125/);
});
```

- [ ] **Step 2: Run-fail.**

- [ ] **Step 3: Implement**

```js
CHECKS.responsive_break = function ({ documentScrollWidth, viewportWidth, viewport }) {
  if (viewport !== 'mobile') {
    return { id: 'responsive_break', result: 'pass', viewport };
  }
  if (documentScrollWidth <= viewportWidth) {
    return { id: 'responsive_break', result: 'pass', viewport };
  }
  const overflowPx = documentScrollWidth - viewportWidth;
  return {
    id: 'responsive_break',
    result: 'fail',
    viewport,
    evidence: `document scroll width ${documentScrollWidth}px exceeds viewport ${viewportWidth}px by ${overflowPx}px`,
    suggested_fix: 'add CSS for narrow viewports; ensure tables wrap or hide non-essential columns'
  };
};
```

- [ ] **Step 4: Run-pass.**

- [ ] **Step 5: Commit.**

```bash
git commit -am "feat(mechanical-checks): implement responsive_break"
```

### Task 18: Implement `chartjunk_decorative_css` (TDD)

**Files:**
- Modify: `skills/component-composer/scripts/mechanical-checks.{js,test.js}`

- [ ] **Step 1: Write failing tests**

```js
test('chartjunk_decorative_css: pass when no decorative CSS on data marks', () => {
  const result = CHECKS.chartjunk_decorative_css({
    marks: [
      { selector: '.data-mark', boxShadow: 'none', textShadow: 'none',
        background: 'none', transform: 'none' }
    ],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'pass');
});

test('chartjunk_decorative_css: fail on box-shadow', () => {
  const result = CHECKS.chartjunk_decorative_css({
    marks: [
      { selector: '.data-mark', boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
        textShadow: 'none', background: 'none', transform: 'none' }
    ],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /box-shadow/);
});

test('chartjunk_decorative_css: fail on gradient background', () => {
  const result = CHECKS.chartjunk_decorative_css({
    marks: [
      { selector: 'rect.bar', boxShadow: 'none', textShadow: 'none',
        background: 'linear-gradient(to top, #fff, #000)', transform: 'none' }
    ],
    viewport: 'tablet'
  });
  assert.equal(result.result, 'fail');
});

test('chartjunk_decorative_css: fail on 3D transform', () => {
  const result = CHECKS.chartjunk_decorative_css({
    marks: [
      { selector: '.bar', boxShadow: 'none', textShadow: 'none',
        background: 'none', transform: 'rotateY(15deg)' }
    ],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /transform/);
});
```

- [ ] **Step 2: Run-fail.**

- [ ] **Step 3: Implement**

```js
CHECKS.chartjunk_decorative_css = function ({ marks, viewport }) {
  const violations = [];
  for (const m of marks) {
    if (m.boxShadow && m.boxShadow !== 'none') {
      violations.push(`${m.selector}: box-shadow=${m.boxShadow}`);
    }
    if (m.textShadow && m.textShadow !== 'none') {
      violations.push(`${m.selector}: text-shadow=${m.textShadow}`);
    }
    if (m.background && /gradient/i.test(m.background)) {
      violations.push(`${m.selector}: gradient background=${m.background}`);
    }
    if (m.transform && /rotate[XY]|matrix3d|perspective/.test(m.transform)) {
      violations.push(`${m.selector}: 3D transform=${m.transform}`);
    }
  }
  if (violations.length === 0) {
    return { id: 'chartjunk_decorative_css', result: 'pass', viewport };
  }
  return {
    id: 'chartjunk_decorative_css',
    result: 'fail',
    viewport,
    evidence: violations.join('; '),
    suggested_fix: 'remove decorative CSS; rely on position, shape, and saturation alone'
  };
};
```

- [ ] **Step 4: Run-pass.**

- [ ] **Step 5: Commit.**

```bash
git commit -am "feat(mechanical-checks): implement chartjunk_decorative_css"
```

### Task 19: Implement `hidden_mark` (TDD)

**Files:**
- Modify: `skills/component-composer/scripts/mechanical-checks.{js,test.js}`

- [ ] **Step 1: Write failing tests**

```js
test('hidden_mark: pass when marks have width≥2 and opacity≥0.3', () => {
  const result = CHECKS.hidden_mark({
    marks: [
      { selector: '.dot', width: 4, height: 4, opacity: 1, sample: 'data point' }
    ],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'pass');
});

test('hidden_mark: fail when mark width < 2px', () => {
  const result = CHECKS.hidden_mark({
    marks: [
      { selector: '.bar', width: 1, height: 10, opacity: 1, sample: 'short bar' }
    ],
    viewport: 'mobile'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /width/);
});

test('hidden_mark: fail when opacity < 0.3', () => {
  const result = CHECKS.hidden_mark({
    marks: [
      { selector: '.line', width: 5, height: 5, opacity: 0.2, sample: 'faint annotation' }
    ],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /opacity/);
});
```

- [ ] **Step 2: Run-fail.**

- [ ] **Step 3: Implement**

```js
CHECKS.hidden_mark = function ({ marks, viewport }) {
  const violations = [];
  for (const m of marks) {
    if (m.width < 2 || m.height < 2) {
      violations.push(`'${m.sample}': width=${m.width}, height=${m.height}`);
    }
    if (m.opacity < 0.3) {
      violations.push(`'${m.sample}': opacity=${m.opacity}`);
    }
  }
  if (violations.length === 0) {
    return { id: 'hidden_mark', result: 'pass', viewport };
  }
  return {
    id: 'hidden_mark',
    result: 'fail',
    viewport,
    evidence: violations.join('; '),
    suggested_fix: 'increase mark dimensions, raise opacity ≥ 0.3, or use a denser encoding'
  };
};
```

- [ ] **Step 4: Run-pass.**

- [ ] **Step 5: Commit.**

```bash
git commit -am "feat(mechanical-checks): implement hidden_mark"
```

### Task 20: Implement `token_compliance` (TDD)

**Files:**
- Modify: `skills/component-composer/scripts/mechanical-checks.{js,test.js}`

- [ ] **Step 1: Write failing tests**

```js
test('token_compliance: pass when every value is a var() reference', () => {
  const result = CHECKS.token_compliance({
    declarations: [
      { selector: '.bar', property: 'background', value: 'var(--accent-warm)' },
      { selector: '.bar', property: 'padding', value: 'var(--space-2) var(--space-3)' }
    ],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'pass');
});

test('token_compliance: fail when a literal hex appears outside :root', () => {
  const result = CHECKS.token_compliance({
    declarations: [
      { selector: '.bar', property: 'background', value: '#0066ff' }
    ],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'fail');
  assert.match(result.evidence, /#0066ff/);
});

test('token_compliance: fail when a literal px appears outside :root', () => {
  const result = CHECKS.token_compliance({
    declarations: [
      { selector: '.title', property: 'font-size', value: '24px' }
    ],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'fail');
});

test('token_compliance: ignore declarations inside :root', () => {
  const result = CHECKS.token_compliance({
    declarations: [
      { selector: ':root', property: '--accent-warm', value: '#c8553d' }
    ],
    viewport: 'desktop'
  });
  assert.equal(result.result, 'pass');
});
```

- [ ] **Step 2: Run-fail.**

- [ ] **Step 3: Implement**

```js
const TOKEN_PROPERTIES = new Set([
  'color', 'background', 'background-color', 'border', 'border-color',
  'fill', 'stroke', 'font-size', 'font-family', 'padding', 'margin',
  'gap', 'border-radius'
]);

function looksLikeLiteralValue(value) {
  // hex
  if (/#[0-9a-f]{3,8}\b/i.test(value)) return true;
  // px (other than 0)
  if (/\b\d+px\b/.test(value) && !/0px\b/.test(value)) return true;
  // rgb/rgba/hsl literals
  if (/\b(rgb|hsl)a?\(/.test(value)) return true;
  return false;
}

CHECKS.token_compliance = function ({ declarations, viewport }) {
  const violations = [];
  for (const d of declarations) {
    if (d.selector === ':root') continue;
    if (!TOKEN_PROPERTIES.has(d.property)) continue;
    if (d.value.includes('var(--')) continue;
    if (d.value === 'none' || d.value === 'inherit' || d.value === 'initial' ||
        d.value === 'transparent' || d.value === 'currentColor' || d.value === '0') continue;
    if (looksLikeLiteralValue(d.value)) {
      violations.push(`${d.selector} { ${d.property}: ${d.value} }`);
    }
  }
  if (violations.length === 0) {
    return { id: 'token_compliance', result: 'pass', viewport };
  }
  return {
    id: 'token_compliance',
    result: 'fail',
    viewport,
    evidence: violations.slice(0, 5).join('; ') + (violations.length > 5 ? '; ...' : ''),
    suggested_fix: 'replace literal values with var(--...) references; declare the value on :root'
  };
};
```

- [ ] **Step 4: Run-pass.**

- [ ] **Step 5: Commit.**

```bash
git commit -am "feat(mechanical-checks): implement token_compliance"
```

### Task 21: Implement `runInBrowser` adapter

**Files:**
- Modify: `skills/component-composer/scripts/mechanical-checks.js`

- [ ] **Step 1: Replace the `runInBrowser` stub**

```js
// runInBrowser is executed inside the rendered page via preview_eval.
// It extracts DOM data for the requested criterion and dispatches to the
// pure check function. Returns the validator output shape (JSON-safe).

export function runInBrowser(criterionId, viewport) {
  switch (criterionId) {
    case 'text_collision': {
      const nodes = Array.from(document.querySelectorAll(
        'svg text, svg tspan, .tick-label, .annotation, .row-label, h1, h2, .stat-label'
      ));
      const boxes = nodes.map(n => {
        const b = n.getBoundingClientRect();
        return { x: b.x, y: b.y, w: b.width, h: b.height, text: (n.textContent || '').trim() };
      }).filter(b => b.w > 0 && b.h > 0);
      return CHECKS.text_collision({ boxes, viewport });
    }
    case 'text_truncation': {
      const nodes = Array.from(document.querySelectorAll('td, th, .label, .annotation'));
      const elements = nodes.map(n => ({
        scrollWidth: n.scrollWidth, clientWidth: n.clientWidth,
        text: (n.textContent || '').trim()
      }));
      return CHECKS.text_truncation({ elements, viewport });
    }
    case 'contrast_failure': {
      const samples = Array.from(document.querySelectorAll(
        'p, h1, h2, td, .annotation, .data-mark, circle, rect.bar'
      )).slice(0, 30);
      const pairs = samples.map(n => {
        const s = getComputedStyle(n);
        const isText = n.tagName.match(/^(P|H1|H2|TD|SPAN|DIV)$/i);
        return {
          kind: isText ? 'text' : 'mark',
          fg: rgbToHex(s.color),
          bg: rgbToHex(getEffectiveBackground(n)),
          sample: n.tagName + (n.className ? '.' + n.className.split(' ')[0] : '')
        };
      }).filter(p => p.fg && p.bg);
      return CHECKS.contrast_failure({ pairs, viewport });
    }
    case 'font_size_too_small': {
      const nodes = Array.from(document.querySelectorAll('svg text, svg tspan'));
      const elements = nodes.map(n => {
        const s = getComputedStyle(n);
        const computedFontPx = parseFloat(s.fontSize);
        const b = n.getBoundingClientRect();
        // Approximate display font px from bbox height
        const displayFontPx = b.height;
        return { tag: n.tagName, computedFontPx, displayFontPx,
                 sample: (n.textContent || '').trim().slice(0, 20) };
      });
      return CHECKS.font_size_too_small({ elements, viewport });
    }
    case 'overflow': {
      const containers = Array.from(document.querySelectorAll(
        'body, .page, .figure, .data-table, table'
      )).map(n => ({
        selector: n.tagName.toLowerCase() + (n.className ? '.' + n.className.split(' ')[0] : ''),
        scrollWidth: n.scrollWidth, clientWidth: n.clientWidth
      }));
      return CHECKS.overflow({ containers, viewport });
    }
    case 'responsive_break': {
      return CHECKS.responsive_break({
        documentScrollWidth: document.documentElement.scrollWidth,
        viewportWidth: window.innerWidth, viewport
      });
    }
    case 'chartjunk_decorative_css': {
      const nodes = Array.from(document.querySelectorAll(
        '.data-mark, rect.bar, circle.dot, .tick, line.data-line'
      ));
      const marks = nodes.map(n => {
        const s = getComputedStyle(n);
        return {
          selector: n.tagName.toLowerCase() + (n.className ? '.' + n.className.split(' ')[0] : ''),
          boxShadow: s.boxShadow, textShadow: s.textShadow,
          background: s.background, transform: s.transform
        };
      });
      return CHECKS.chartjunk_decorative_css({ marks, viewport });
    }
    case 'hidden_mark': {
      const nodes = Array.from(document.querySelectorAll(
        '.data-mark, rect.bar, circle.dot, line.data-line'
      ));
      const marks = nodes.map(n => {
        const b = n.getBoundingClientRect();
        const s = getComputedStyle(n);
        return {
          selector: n.tagName.toLowerCase() + (n.className ? '.' + n.className.split(' ')[0] : ''),
          width: b.width, height: b.height, opacity: parseFloat(s.opacity),
          sample: n.getAttribute('data-label') || n.tagName
        };
      });
      return CHECKS.hidden_mark({ marks, viewport });
    }
    case 'token_compliance': {
      const declarations = [];
      for (const sheet of document.styleSheets) {
        try {
          for (const rule of sheet.cssRules) {
            if (rule.style) {
              for (let i = 0; i < rule.style.length; i++) {
                const property = rule.style[i];
                const value = rule.style.getPropertyValue(property);
                declarations.push({ selector: rule.selectorText, property, value });
              }
            }
          }
        } catch (_) { /* CORS sheet — skip */ }
      }
      return CHECKS.token_compliance({ declarations, viewport });
    }
    default:
      return { id: criterionId, result: 'pass', viewport,
               evidence: 'no mechanical check; dispatched to LLM-judge', _no_mechanical: true };
  }
}

// Helpers
function rgbToHex(rgb) {
  const m = rgb.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
  if (!m) return null;
  const toHex = n => parseInt(n, 10).toString(16).padStart(2, '0');
  return '#' + toHex(m[1]) + toHex(m[2]) + toHex(m[3]);
}

function getEffectiveBackground(el) {
  let cur = el;
  while (cur && cur !== document.documentElement) {
    const bg = getComputedStyle(cur).backgroundColor;
    if (bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') return bg;
    cur = cur.parentElement;
  }
  return getComputedStyle(document.documentElement).backgroundColor || 'rgb(255,255,255)';
}
```

- [ ] **Step 2: Run tests, verify still all pass**

```bash
node --test mechanical-checks.test.js
```

Expected: all 9 pure-function tests still pass; `runInBrowser` is not unit-tested (it's an adapter; tested at the end-to-end stage).

- [ ] **Step 3: Commit.**

```bash
git commit -am "feat(mechanical-checks): add runInBrowser browser adapter"
```

---

## Phase 3 — HUD + template + exports

### Task 22: Write `template/base.html`

**Files:**
- Create: `skills/component-composer/template/base.html`

- [ ] **Step 1: Write the skeleton**

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}}</title>
<style>
  :root {
    /* paper / ink — theme fills these */
    --paper: #fafaf7;
    --paper-soft: #f3f1ea;
    --ink: #1a1a1a;
    --ink-soft: #555;

    /* accents */
    --accent-warm: #c8553d;
    --accent-cool: #2c5e6f;
    --accent-quiet: #888;

    /* gray ramp */
    --gray-100: #f0eee6;
    --gray-300: #d1cfc5;
    --gray-500: #87867f;
    --gray-700: #3d3d3a;
    --gray-900: #141413;

    /* type */
    --serif: ui-serif, Georgia, serif;
    --sans: system-ui, -apple-system, sans-serif;
    --mono: ui-monospace, "SF Mono", Menlo, monospace;
    --font-size-h1: 1.8rem;
    --font-size-h2: 1.1rem;
    --font-size-body: 0.95rem;
    --font-size-caption: 0.78rem;

    /* spacing */
    --space-1: 4px;
    --space-2: 8px;
    --space-3: 12px;
    --space-4: 16px;
    --space-6: 24px;
    --space-8: 32px;
    --space-12: 48px;

    /* structural */
    --radius-panel: 12px;
    --border: 1px solid var(--gray-300);
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    padding: var(--space-12) var(--space-6);
    background: var(--paper);
    color: var(--ink);
    font-family: var(--sans);
    font-size: var(--font-size-body);
    line-height: 1.5;
  }
  .page { max-width: 720px; margin: 0 auto; }
  h1 { font-family: var(--serif); font-weight: 600; font-size: var(--font-size-h1); margin: 0; }
  h2 { font-family: var(--serif); font-weight: 500; font-size: var(--font-size-h2);
       margin: var(--space-12) 0 var(--space-3); color: var(--ink-soft); }
  .annotation { color: var(--ink-soft); font-size: var(--font-size-caption); }
</style>
</head>
<body>
  <main class="page">
    {{CONTENT}}
  </main>
</body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add skills/component-composer/template/base.html
git commit -m "feat(component-composer): add base.html template"
```

### Task 23: Write `scripts/hud.js`

**Files:**
- Create: `skills/component-composer/scripts/hud.js`

- [ ] **Step 1: Write the HUD code**

```js
// hud.js — injected into the rendered artifact during iteration.
// Reads from window.__composer_state for user commands.

(function () {
  const HUD_ID = '__composer_hud';
  if (document.getElementById(HUD_ID)) return; // already injected

  window.__composer_state = window.__composer_state || {
    command: null,
    guidance: ''
  };

  const hud = document.createElement('div');
  hud.id = HUD_ID;
  hud.style.cssText = [
    'position:fixed', 'top:8px', 'right:8px',
    'z-index:99999',
    'background:rgba(20,20,18,0.92)', 'color:#fff',
    'padding:10px 12px', 'border-radius:8px',
    'font-family:ui-monospace,SF Mono,Menlo,monospace',
    'font-size:11px', 'line-height:1.5',
    'max-width:300px', 'box-shadow:0 4px 16px rgba(0,0,0,0.3)'
  ].join(';');

  hud.innerHTML = `
    <div style="font-weight:600;margin-bottom:6px">composer · iter <span id="${HUD_ID}_iter">1</span></div>
    <div id="${HUD_ID}_status" style="margin-bottom:8px;color:#aaa">drafting…</div>
    <div id="${HUD_ID}_failures" style="margin-bottom:8px;font-size:10px"></div>
    <div style="display:flex;gap:4px;margin-bottom:6px">
      <button data-cmd="continue" style="flex:1;background:#2c5e6f;color:#fff;border:none;padding:4px 8px;border-radius:4px;font-size:10px;cursor:pointer">continue</button>
      <button data-cmd="abort" style="flex:1;background:#c8553d;color:#fff;border:none;padding:4px 8px;border-radius:4px;font-size:10px;cursor:pointer">abort</button>
    </div>
    <textarea id="${HUD_ID}_guidance" placeholder="optional: nudge the drafter…" style="width:100%;background:#000;color:#fff;border:1px solid #444;border-radius:4px;padding:4px;font-size:10px;font-family:inherit;resize:vertical;min-height:32px"></textarea>
    <button data-cmd="guidance" style="width:100%;margin-top:4px;background:#3d3d3a;color:#fff;border:none;padding:4px 8px;border-radius:4px;font-size:10px;cursor:pointer">apply guidance</button>
  `;

  document.body.appendChild(hud);

  hud.addEventListener('click', (e) => {
    const cmd = e.target?.dataset?.cmd;
    if (!cmd) return;
    if (cmd === 'guidance') {
      window.__composer_state.guidance = document.getElementById(HUD_ID + '_guidance').value;
    }
    window.__composer_state.command = cmd;
  });

  window.__composer_update = function ({ iteration, failures, stuck }) {
    document.getElementById(HUD_ID + '_iter').textContent = String(iteration);
    const statusEl = document.getElementById(HUD_ID + '_status');
    const failsEl = document.getElementById(HUD_ID + '_failures');
    if (stuck) {
      statusEl.textContent = 'STUCK — same failures 2x';
      statusEl.style.color = '#c8553d';
    } else if (failures.length === 0) {
      statusEl.textContent = 'all clear';
      statusEl.style.color = '#8aa67c';
    } else {
      statusEl.textContent = `${failures.length} failing`;
      statusEl.style.color = '#d6a544';
    }
    failsEl.innerHTML = failures.slice(0, 5).map(f =>
      `<div style="color:#aaa">· ${f.id} @${f.viewport}</div>`
    ).join('');
  };
})();
```

- [ ] **Step 2: Commit**

```bash
git add skills/component-composer/scripts/hud.js
git commit -m "feat(component-composer): add HUD script"
```

### Task 24: Write `scripts/export-png.js`

**Files:**
- Create: `skills/component-composer/scripts/export-png.js`

- [ ] **Step 1: Write export-png.js**

```js
// export-png.js — protocol for emitting final.png from the composer.
//
// Invocation contract:
//   The composer, after stripping the HUD from final.html, calls:
//     1. preview_resize(width=1280, height=2400)   (tall, to fit page)
//     2. preview_screenshot()                       (returns image bytes)
//     3. Save returned bytes to <session-dir>/final.png
//
// This file documents the contract. The composer SKILL.md operating mode
// owns the actual invocation; no runtime JS is needed here.

export const PNG_EXPORT_CONTRACT = {
  width: 1280,
  height: 2400,
  format: 'png',
  filename: 'final.png'
};
```

- [ ] **Step 2: Commit**

```bash
git add skills/component-composer/scripts/export-png.js
git commit -m "feat(component-composer): add PNG export contract"
```

### Task 25: Write `scripts/export-pdf.js`

**Files:**
- Create: `skills/component-composer/scripts/export-pdf.js`

- [ ] **Step 1: Write export-pdf.js**

```js
// export-pdf.js — protocol for emitting final.pdf via preview_eval +
// browser print-to-PDF.
//
// Invocation contract:
//   1. Composer ensures final.html has print-friendly CSS @media print
//      block — body padding 0, no fixed elements, default page size.
//   2. preview_eval runs: window.print() — but this opens a dialog in
//      regular Chromium, not Claude Preview's headless mode.
//   3. Claude Preview exposes Page.printToPDF via the Chrome DevTools
//      Protocol when running in headless mode. The composer's SKILL.md
//      operating mode declares: if printToPDF is available, use it; else
//      mark PDF export as "manual: open final.html in a browser and print
//      to PDF" and continue.
//   4. Save returned PDF bytes to <session-dir>/final.pdf.
//
// At v1.0, PDF export is best-effort. If Claude Preview doesn't expose
// printToPDF, the composer emits a one-line note in the audit summary:
// "PDF export skipped — printToPDF unavailable in this Claude Preview build."

export const PDF_EXPORT_CONTRACT = {
  format: 'pdf',
  filename: 'final.pdf',
  best_effort: true,
  print_css_requirement: `@media print {
    body { padding: 0; }
    #__composer_hud { display: none; }
  }`
};
```

- [ ] **Step 2: Commit**

```bash
git add skills/component-composer/scripts/export-pdf.js
git commit -m "feat(component-composer): add PDF export contract"
```

---

## Phase 4 — atomic-data-viz refactor

### Task 26: Rename tufte-love → atomic-data-viz

**Files:**
- Move: `skills/tufte-love/` → `skills/atomic-data-viz/`

- [ ] **Step 1: Git-move the directory**

```bash
git mv skills/tufte-love skills/atomic-data-viz
git status
```

- [ ] **Step 2: Rename tufte-principles.md → principles.md**

```bash
git mv skills/atomic-data-viz/references/tufte-principles.md \
       skills/atomic-data-viz/references/principles.md
```

- [ ] **Step 3: Commit the rename**

```bash
git commit -m "refactor: rename tufte-love → atomic-data-viz; principles.md"
```

### Task 27: Update plugin.json + SKILL.md frontmatter

**Files:**
- Modify: `skills/atomic-data-viz/.claude-plugin/plugin.json`
- Modify: `skills/atomic-data-viz/SKILL.md` (frontmatter only)

- [ ] **Step 1: Read current plugin.json**

```bash
cat skills/atomic-data-viz/.claude-plugin/plugin.json
```

- [ ] **Step 2: Update plugin.json**

```json
{
  "name": "atomic-data-viz",
  "version": "1.0.0",
  "description": "Theme for component-composer: Tufte-style data graphics with quiet palette, range-frame axes, and high data-ink discipline.",
  "author": {
    "name": "Information Logistics",
    "email": "bdl@infolog.io"
  }
}
```

- [ ] **Step 3: Replace SKILL.md (full rewrite — much shorter)**

Replace the entire SKILL.md with:

```markdown
---
name: atomic-data-viz
description: >
  Theme bundle for component-composer. Provides tokens, criteria, patterns,
  and palette for Tufte-style data graphics: range-frame axes, small
  multiples, high data-ink, single highlight, no chartjunk. Activated when
  component-composer is invoked with `atomic-data-viz` as the theme name.
---

# atomic-data-viz

This skill is a **theme** for `component-composer`. It does not run on
its own. The composer reads this skill's references when the user invokes
composition with `atomic-data-viz` as the active theme.

## What this theme provides

- `themespec.json` — manifest
- `references/tokens.md` — CSS variable schema (which vars, what role)
- `references/palette.md` — concrete values for the Tufte-quiet aesthetic
- `references/criteria.md` — validator rules (no chartjunk, range-frame, etc.)
- `references/patterns.md` — preferred chart patterns
- `references/principles.md` — foundational Tufte principles
- `references/analytical-design.md` — extended principles (sparklines, layering, micro/macro)
- `references/chart-patterns.md` — supplementary chart-selection patterns
- `references/chart-rules-extras.md` — supplementary number-formatting and time-axis rules

## Aesthetic

Quiet. Most ink is gray. One warm accent reserved for the single
highlighted mark. Range-frame axes terminating at data extent. Direct
labels over legends. Words integrated with numbers and images. Multiple
levels of detail (micro + macro). Sparklines and small multiples preferred
over single overloaded charts.

## To invoke

> "compose a chart with atomic-data-viz showing my GitHub usage data"

The composer resolves `atomic-data-viz` via `themespec.json`, reads the
references, drafts an HTML artifact, validates against `criteria.md`, and
iterates until clean.
```

- [ ] **Step 4: Commit**

```bash
git add skills/atomic-data-viz/.claude-plugin/plugin.json skills/atomic-data-viz/SKILL.md
git commit -m "refactor(atomic-data-viz): rewrite SKILL.md as theme declaration; bump v1.0.0"
```

### Task 28: Write `themespec.json`

**Files:**
- Create: `skills/atomic-data-viz/themespec.json`

- [ ] **Step 1: Write themespec.json**

```json
{
  "name": "atomic-data-viz",
  "version": "1.0.0",
  "context": "data-graphics",
  "capabilities": [
    "chart", "table", "sparkline", "small-multiples",
    "dot-plot", "strip-plot", "slopegraph", "range-frame-axis"
  ],
  "output_formats": ["html", "png", "pdf"],
  "style_anchor": "single-file-html"
}
```

- [ ] **Step 2: Commit**

```bash
git add skills/atomic-data-viz/themespec.json
git commit -m "feat(atomic-data-viz): add themespec manifest"
```

### Task 29: Write `references/tokens.md`

**Files:**
- Create: `skills/atomic-data-viz/references/tokens.md`

- [ ] **Step 1: Write tokens.md**

```markdown
# atomic-data-viz · Token schema

This theme requires the following CSS custom properties on `:root`. The
composer's `token_compliance` check verifies every styled property in the
artifact resolves to one of these via `var(--...)`.

## Surface

| Variable | Role |
|---|---|
| `--paper` | Primary background — pages, panels |
| `--paper-soft` | Secondary surface — alternate row, callout box |

## Ink

| Variable | Role |
|---|---|
| `--ink` | Primary text + data marks |
| `--ink-soft` | Annotation, secondary text, axis labels |

## Accents

Used sparingly. The 90/10 rule: 90% gray, 10% accent.

| Variable | Role |
|---|---|
| `--accent-warm` | The single highlighted mark (one per chart) |
| `--accent-cool` | Reference line, regression, threshold annotation |
| `--accent-quiet` | Footnote, deemphasized callout |

## Gray ramp

Five stops for hierarchy. Most chart elements use these.

| Variable | Use |
|---|---|
| `--gray-100` | Backgrounds, page-soft fills |
| `--gray-300` | Borders, grid lines, deemphasized strokes |
| `--gray-500` | Mid-emphasis text, axis labels |
| `--gray-700` | Body text |
| `--gray-900` | Headings, primary marks |

## Type

| Variable | Role |
|---|---|
| `--serif` | Headings (h1, h2, large numerics in stat cards) |
| `--sans` | Body, axis labels, annotations |
| `--mono` | Tabular numerics, code, identifiers |
| `--font-size-h1` | Page title |
| `--font-size-h2` | Section heading |
| `--font-size-body` | Default text |
| `--font-size-caption` | Annotation, footer |

## Spacing scale

Multiples of 4px. Use these — never raw px values.

| Variable | Pixels |
|---|---|
| `--space-1` | 4 |
| `--space-2` | 8 |
| `--space-3` | 12 |
| `--space-4` | 16 |
| `--space-6` | 24 |
| `--space-8` | 32 |
| `--space-12` | 48 |

## Structural

| Variable | Role |
|---|---|
| `--radius-panel` | Card / panel border radius |
| `--border` | Default thin border for panels and tables |
```

- [ ] **Step 2: Commit**

```bash
git add skills/atomic-data-viz/references/tokens.md
git commit -m "feat(atomic-data-viz): add tokens.md schema"
```

### Task 30: Write `references/palette.md`

**Files:**
- Create: `skills/atomic-data-viz/references/palette.md`

- [ ] **Step 1: Write palette.md**

```markdown
# atomic-data-viz · Palette

Concrete values for the Tufte-quiet aesthetic. Drafter copies this into
the artifact's `:root` declaration.

## Color values

```css
:root {
  /* surfaces */
  --paper: #fafaf7;
  --paper-soft: #f3f1ea;

  /* ink */
  --ink: #1a1a1a;
  --ink-soft: #555555;

  /* accents — 90/10 rule */
  --accent-warm: #c8553d;   /* Okabe-Ito vermillion, adapted */
  --accent-cool: #2c5e6f;
  --accent-quiet: #888888;

  /* gray ramp */
  --gray-100: #f0eee6;
  --gray-300: #d1cfc5;
  --gray-500: #87867f;
  --gray-700: #3d3d3a;
  --gray-900: #141413;
}
```

## Type values

```css
:root {
  --serif: ui-serif, Georgia, "Times New Roman", serif;
  --sans:  system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --mono:  ui-monospace, "SF Mono", Menlo, "Courier New", monospace;

  --font-size-h1: 1.6rem;
  --font-size-h2: 1.05rem;
  --font-size-body: 0.92rem;
  --font-size-caption: 0.78rem;
}
```

## Spacing + structural

```css
:root {
  --space-1: 4px;  --space-2: 8px;   --space-3: 12px;
  --space-4: 16px; --space-6: 24px;  --space-8: 32px; --space-12: 48px;

  --radius-panel: 10px;
  --border: 1px solid var(--gray-300);
}
```

## Palette rules

1. Most marks default to `var(--ink)` or `var(--gray-700)`.
2. At most one mark per chart uses `var(--accent-warm)`.
3. Reference lines + thresholds use `var(--accent-cool)` at lower
   opacity (0.6) or a dashed stroke.
4. The page background is `var(--paper)` — never pure white.
5. Borders default to `var(--border)` — always token-referenced.

## Monochrome survival

The palette survives grayscale conversion because all encoding uses
position, size, and shape — never hue alone. The accent is salience-only,
not data-encoding.
```

- [ ] **Step 2: Commit**

```bash
git add skills/atomic-data-viz/references/palette.md
git commit -m "feat(atomic-data-viz): add concrete palette"
```

### Task 31: Write `references/criteria.md`

**Files:**
- Create: `skills/atomic-data-viz/references/criteria.md`

- [ ] **Step 1: Write criteria.md**

```markdown
# atomic-data-viz · Validator criteria

Each criterion has an id (the markdown H2) and a check description. The
composer dispatches mechanical checks first; remaining criteria go to
LLM-as-judge.

---

## text_collision

No text labels overlap each other or data marks. Tick labels touching,
axis labels crossing a data dot, year label merging with month tick — all
violate.

## text_truncation

No text container has hidden overflow content. If text would wrap or
clip, shorten the text or widen the container.

## contrast_failure

Text contrast against effective background ≥ 4.5:1 (WCAG AA). Mark
contrast ≥ 3:1. Computed colors only — not the declared variable.

## font_size_too_small

Every rendered text element ≥ 10px display size. Account for SVG
viewBox downscale — a `font-size: 11px` inside a 360-wide viewBox shown
at 180px is effectively 5.5px, which fails.

## overflow

Body, page container, figures, and tables have `scrollWidth ≤ clientWidth`
at every viewport.

## responsive_break

At mobile viewport (375px), `document.documentElement.scrollWidth ≤ 375`.
No horizontal scroll under any normal interaction.

## chartjunk_decorative_css

No `box-shadow`, `text-shadow`, gradient `background`, or 3D `transform`
on data marks, axes, or chart elements. Decoration that does not encode
data is forbidden.

## hidden_mark

Every data mark has computed `width ≥ 2px`, `height ≥ 2px`, and
`opacity ≥ 0.3`. Marks invisible to a casual reader violate.

## token_compliance

Every CSS property in the `color | background | border | fill | stroke
| font-size | font-family | padding | margin | gap | border-radius`
family resolves to a `var(--...)` reference, not a literal hex or px
value. The `:root` block is exempt.

---

## missing_range_frame

Axes terminate at data extent, not arbitrary round numbers. If the data
range is 12–87, the axis runs from 12 to 87, not 0 to 100. Subjective
judgment — confirmed by LLM-judge.

## insufficient_data_ink

Every visible element earns its place. Erasing any element loses data
information. Heavy gridlines, decorative borders, redundant labels
violate. Subjective judgment — confirmed by LLM-judge.

## comparison_failure

The chart enables the comparison its labels imply. A "vs" or "before/
after" framing demands visible alignment. Subjective judgment.

## hierarchy_failure

Primary data dominates secondary elements visually. Axes recede; data
projects forward. Subjective judgment.

## chartjunk_subjective

Visual decoration competing with evidence beyond CSS-detectable patterns.
Decorative icons, clip art, redundant illustrations, ornamental
typography. Subjective judgment.

## missing_direct_label

When a legend can be replaced by a direct label, the direct label is
preferred. Charts with two or more colors and a legend in the corner
that could instead label lines directly violate. Subjective judgment.
```

- [ ] **Step 2: Commit**

```bash
git add skills/atomic-data-viz/references/criteria.md
git commit -m "feat(atomic-data-viz): add validator criteria"
```

### Task 32: Write `references/patterns.md`

**Files:**
- Create: `skills/atomic-data-viz/references/patterns.md`

- [ ] **Step 1: Write patterns.md**

```markdown
# atomic-data-viz · Patterns

Preferred chart patterns. The drafter consults these before composing.
When a pattern fits, use it.

## Time-series → line chart, not bar

Lines preserve sequence. Bars imply discrete intervals. Use line for any
ordered continuous quantity over time.

## Many-to-many comparison → small multiples

A single overloaded chart with N colors fails. N panels with identical
encoding, sorted meaningfully, succeeds. Use small multiples for any
comparison across categories, regions, cohorts, or time periods.

## Part-to-whole → bar or table, never pie

Pies prevent precise comparison. Bars and tables enable it. If exact
values matter, use a table.

## Tiny N (≤ 5) → table

When you have ≤ 5 data points, a table is more honest than a chart. The
chart pretends pattern; the table shows truth.

## Trend at a glance → sparkline

For each row in a metrics table, append a sparkline of the last 30 days.
Sparkline ≤ 80px wide, ≤ 16px tall, no axis. End-value labeled.

## Before vs after → slopegraph

Two ordered points per entity. Connect with a line. Sort by ending
value. Direct labels on left and right.

## Distribution + comparison → dot plot, not bar

Dots are more precise than bars. Each row: category label on left,
horizontal line + dot at value. Sort by value.

## Categorical magnitude → strip plot

When you want to show the spread of individual values within a category.
Each entity is one dot on a horizontal axis.

## Range-frame axes

Axis lines start at the minimum data value and end at the maximum. The
axis communicates the data extent without explicit annotation.

## Direct labels over legends

When two or more colors encode categories, label the lines directly at
their right edge instead of using a legend. Eye doesn't have to bounce
between key and chart.

## One highlight per chart

90% gray + 10% color. At most one mark uses `--accent-warm`. Two
highlights destroy the focal effect.

## Words integrate with numbers

Sentence fragments next to data: "Revenue trended up ▁▂▄▆▇ over Q3."
Sparkline inline. Don't segregate "narrative" from "chart".

## Footer with provenance

Every artifact carries a footer line: source, date pulled, methodology
note if needed. Tufte: thoroughly describe the evidence.
```

- [ ] **Step 2: Commit**

```bash
git add skills/atomic-data-viz/references/patterns.md
git commit -m "feat(atomic-data-viz): add patterns library"
```

### Task 33: Delete superseded references

**Files:**
- Delete: `skills/atomic-data-viz/references/audit-rubric.md`
- Delete: `skills/atomic-data-viz/references/color-palette.md`

- [ ] **Step 1: Verify content has migrated**

```bash
diff <(grep -h '^##' skills/atomic-data-viz/references/audit-rubric.md) \
     <(grep -h '^##' skills/atomic-data-viz/references/criteria.md)
diff <(head -50 skills/atomic-data-viz/references/color-palette.md) \
     <(head -50 skills/atomic-data-viz/references/palette.md)
```

Manually confirm: every dimension from audit-rubric.md is represented
as a criterion in criteria.md, and every concrete color from color-
palette.md is in palette.md.

- [ ] **Step 2: Delete the superseded files**

```bash
git rm skills/atomic-data-viz/references/audit-rubric.md
git rm skills/atomic-data-viz/references/color-palette.md
```

- [ ] **Step 3: Commit**

```bash
git commit -m "refactor(atomic-data-viz): remove audit-rubric.md and color-palette.md (merged into criteria.md + palette.md)"
```

### Task 34: Update marketplace.json entry

**Files:**
- Modify: `marketplace.json`

- [ ] **Step 1: Rename `tufte-love` → `atomic-data-viz` in marketplace.json**

Update the relevant entry. Old:
```json
{ "name": "tufte-love", "source": "./skills/tufte-love", ... }
```
New:
```json
{
  "name": "atomic-data-viz",
  "source": "./skills/atomic-data-viz",
  "version": "1.0.0",
  "description": "Tufte-style theme for component-composer."
}
```

- [ ] **Step 2: Commit**

```bash
git add marketplace.json
git commit -m "chore(marketplace): rename tufte-love → atomic-data-viz"
```

---

## Phase 5 — atomic-brand components.md

### Task 35: Write `skills/atomic-brand/references/components.md`

**Files:**
- Create: `skills/atomic-brand/references/components.md`

- [ ] **Step 1: Write components.md**

```markdown
# atomic-brand · Components

Structural primitives that themes decorate. Each component has an HTML
skeleton + CSS variable contract. Themes set the variables; this catalog
owns the structure.

These are atomic-design "molecules" — small reusable bits one level above
tokens.

---

## axis

A range-frame axis for an SVG chart. Terminates at data extent.

```html
<line class="axis" x1="0" y1="100" x2="600" y2="100" />
<g class="ticks">
  <line class="tick" x1="0" y1="100" x2="0" y2="104" />
  <text class="tick-label" x="0" y="116">2025</text>
</g>
```

CSS contract:
- `.axis { stroke: var(--gray-300); stroke-width: 1; }`
- `.tick { stroke: var(--gray-300); }`
- `.tick-label { font-family: var(--sans); font-size: var(--font-size-caption); fill: var(--ink-soft); }`

Variants: range-frame (default — line spans data extent only) and
full-grid (line spans full available width with regular tick marks).

---

## legend

Inline color-name pairs near the chart. Themes prefer direct labels;
legend is fallback.

```html
<div class="legend">
  <span class="legend-item"><span class="legend-swatch warm"></span>highlighted cohort</span>
  <span class="legend-item"><span class="legend-swatch cool"></span>reference</span>
</div>
```

CSS contract:
- `.legend { display: flex; gap: var(--space-3); font-size: var(--font-size-caption); color: var(--ink-soft); }`
- `.legend-swatch { width: 12px; height: 3px; display: inline-block; margin-right: var(--space-1); border-radius: 2px; }`
- `.legend-swatch.warm { background: var(--accent-warm); }`
- `.legend-swatch.cool { background: var(--accent-cool); }`

---

## annotation

Callout near a data mark. Inline italic, gray text.

```html
<text class="annotation" x="42" y="22">first 2 repos · Nov 27</text>
```

CSS contract:
- `.annotation { font-family: var(--sans); font-size: var(--font-size-caption); font-style: italic; fill: var(--ink-soft); }`

---

## sparkline

Word-sized inline graphic. No axes, no labels. End value optionally
labeled.

```html
<svg class="sparkline" width="80" height="16" viewBox="0 0 80 16" preserveAspectRatio="none">
  <polyline points="0,12 10,8 20,9 30,5 40,6 50,3 60,4 70,1 80,2"
            class="sparkline-path" />
  <circle class="sparkline-end" cx="80" cy="2" r="2" />
</svg>
```

CSS contract:
- `.sparkline-path { fill: none; stroke: var(--ink); stroke-width: 1; }`
- `.sparkline-end { fill: var(--accent-warm); }`

---

## data-mark

A single data point. Dot, bar, or short line.

```html
<circle class="data-mark" cx="100" cy="50" r="3" />
<rect class="data-mark bar" x="120" y="40" width="6" height="20" />
```

CSS contract:
- `.data-mark { fill: var(--ink); }`
- `.data-mark.highlight { fill: var(--accent-warm); }`
- `.data-mark.bar { /* same fill rules */ }`

---

## table-row

Quantitative data table row.

```html
<table class="data-table">
  <thead><tr><th>repo</th><th class="num">days</th></tr></thead>
  <tbody>
    <tr><td>crow.pet</td><td class="num">62</td></tr>
  </tbody>
</table>
```

CSS contract:
- `.data-table { border-collapse: collapse; width: 100%; font-size: var(--font-size-body); font-variant-numeric: tabular-nums; }`
- `.data-table th { font-family: var(--sans); font-weight: 500; color: var(--ink-soft); border-bottom: var(--border); padding: var(--space-1) var(--space-2); text-align: left; }`
- `.data-table .num { text-align: right; }`
- `.data-table tbody tr { border-bottom: 1px solid var(--gray-100); }`

---

## small-multiple-cell

One faceted panel in a small-multiples grid.

```html
<div class="sm-grid">
  <figure class="sm-cell">
    <figcaption class="sm-label">2025</figcaption>
    <svg viewBox="0 0 100 60">...</svg>
  </figure>
</div>
```

CSS contract:
- `.sm-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: var(--space-3); }`
- `.sm-cell { margin: 0; }`
- `.sm-label { font-size: var(--font-size-caption); color: var(--ink-soft); margin-bottom: var(--space-1); }`

---

## slopegraph-line

Before/after comparison line.

```html
<g class="slopegraph">
  <text class="slope-label-left" x="0" y="22">2024 · $4.2M</text>
  <line class="slope-line" x1="80" y1="20" x2="200" y2="60" />
  <text class="slope-label-right" x="208" y="62">2025 · $3.1M</text>
</g>
```

CSS contract:
- `.slope-line { stroke: var(--ink); stroke-width: 1.5; }`
- `.slope-line.highlight { stroke: var(--accent-warm); stroke-width: 2; }`
- `.slope-label-left, .slope-label-right { font-family: var(--sans); font-size: var(--font-size-caption); fill: var(--ink); }`

---

## strip-plot-tick

One vertical tick on a horizontal axis. Used for distributions of
discrete events.

```html
<line class="strip-tick" x1="120" y1="38" x2="120" y2="42" />
```

CSS contract:
- `.strip-tick { stroke: var(--ink); stroke-width: 1; opacity: 0.7; }`
- `.strip-tick.highlight { stroke: var(--accent-warm); stroke-width: 1.5; opacity: 1; }`

---

## Composition rules

1. Components are decorated by theme tokens. A theme cannot redefine the
   structure — only the variable values.
2. Drafters use the class names exactly. Selectors stay stable across
   themes.
3. Themes that need new components extend this catalog. atomic-brand
   curates additions.
```

- [ ] **Step 2: Commit**

```bash
git add skills/atomic-brand/references/components.md
git commit -m "feat(atomic-brand): add structural components catalog"
```

---

## Phase 6 — bloomberg-dense sibling theme

### Task 36: Scaffold bloomberg-dense directory + plugin.json

**Files:**
- Create: `skills/bloomberg-dense/.claude-plugin/plugin.json`

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p skills/bloomberg-dense/.claude-plugin \
         skills/bloomberg-dense/references
```

- [ ] **Step 2: Write plugin.json**

```json
{
  "name": "bloomberg-dense",
  "version": "1.0.0",
  "description": "Theme for component-composer: terminal-aesthetic data graphics. Green-on-black, monospace, high density. Proves multi-theme architecture works.",
  "author": {
    "name": "Information Logistics",
    "email": "bdl@infolog.io"
  }
}
```

- [ ] **Step 3: Commit**

```bash
git add skills/bloomberg-dense/
git commit -m "feat(bloomberg-dense): scaffold skill directory"
```

### Task 37: Write SKILL.md

**Files:**
- Create: `skills/bloomberg-dense/SKILL.md`

- [ ] **Step 1: Write SKILL.md**

```markdown
---
name: bloomberg-dense
description: >
  Theme bundle for component-composer. Terminal/Bloomberg-terminal
  aesthetic: green-on-black, monospace everywhere, maximum data density,
  no chartjunk. Activated when component-composer is invoked with
  `bloomberg-dense` as the theme name.
---

# bloomberg-dense

This skill is a **theme** for `component-composer`. It does not run on
its own.

## What this theme provides

- `themespec.json` — manifest
- `references/tokens.md` — CSS variable schema (same structural tokens as
  atomic-data-viz; different values)
- `references/palette.md` — green-on-black, monospace
- `references/criteria.md` — density-first criteria
- `references/patterns.md` — dense-table-first patterns

## Aesthetic

Dark background. Bright green primary ink. Tabular monospace everywhere.
Maximum information per pixel. No serifs. No drop-shadows. No gradients.
Looks like a Bloomberg terminal or top from 1995.

This theme exists to prove the multi-theme architecture: it shares the
same component catalog as atomic-data-viz, but the rendered output is
visually completely different.

## To invoke

> "compose with bloomberg-dense showing the same GitHub data"
```

- [ ] **Step 2: Commit**

```bash
git add skills/bloomberg-dense/SKILL.md
git commit -m "feat(bloomberg-dense): add SKILL.md"
```

### Task 38: Write themespec.json

**Files:**
- Create: `skills/bloomberg-dense/themespec.json`

- [ ] **Step 1: Write themespec.json**

```json
{
  "name": "bloomberg-dense",
  "version": "1.0.0",
  "context": "data-graphics",
  "capabilities": [
    "chart", "table", "sparkline", "small-multiples", "dense-table"
  ],
  "output_formats": ["html", "png", "pdf"],
  "style_anchor": "single-file-html"
}
```

- [ ] **Step 2: Commit**

```bash
git add skills/bloomberg-dense/themespec.json
git commit -m "feat(bloomberg-dense): add themespec manifest"
```

### Task 39: Write `references/tokens.md`

**Files:**
- Create: `skills/bloomberg-dense/references/tokens.md`

- [ ] **Step 1: Write tokens.md**

```markdown
# bloomberg-dense · Token schema

Same structural tokens as atomic-data-viz. Different values.

Required `:root` variables:

| Variable | Role |
|---|---|
| `--paper`, `--paper-soft` | Surfaces (very dark) |
| `--ink`, `--ink-soft` | Primary + secondary text (bright green) |
| `--accent-warm`, `--accent-cool`, `--accent-quiet` | Highlights (amber, cyan, dim-green) |
| `--gray-100`..`--gray-900` | Grays (cool, near-black to off-white) |
| `--serif`, `--sans`, `--mono` | All resolve to the same monospace stack |
| `--font-size-h1`, `--font-size-h2`, `--font-size-body`, `--font-size-caption` | Type scale (tighter than atomic-data-viz) |
| `--space-1`..`--space-12` | Spacing scale (tighter than atomic-data-viz — values divided by 1.25) |
| `--radius-panel`, `--border` | Structural (radius 0; borders 1px solid green) |
```

- [ ] **Step 2: Commit**

```bash
git add skills/bloomberg-dense/references/tokens.md
git commit -m "feat(bloomberg-dense): add tokens schema"
```

### Task 40: Write `references/palette.md`

**Files:**
- Create: `skills/bloomberg-dense/references/palette.md`

- [ ] **Step 1: Write palette.md**

```markdown
# bloomberg-dense · Palette

```css
:root {
  --paper: #0a0e0a;          /* near-black with green tint */
  --paper-soft: #14181a;

  --ink: #4ade80;            /* bright green */
  --ink-soft: #22c55e;

  --accent-warm: #fbbf24;    /* amber for highlights */
  --accent-cool: #06b6d4;    /* cyan for references */
  --accent-quiet: #166534;   /* dim green for footnotes */

  --gray-100: #1f2937;
  --gray-300: #374151;
  --gray-500: #6b7280;
  --gray-700: #9ca3af;
  --gray-900: #e5e7eb;

  --serif: ui-monospace, "SF Mono", Menlo, monospace;
  --sans: ui-monospace, "SF Mono", Menlo, monospace;
  --mono: ui-monospace, "SF Mono", Menlo, monospace;

  --font-size-h1: 1.2rem;
  --font-size-h2: 0.95rem;
  --font-size-body: 0.78rem;
  --font-size-caption: 0.68rem;

  --space-1: 3px; --space-2: 6px;  --space-3: 10px;
  --space-4: 13px; --space-6: 19px; --space-8: 26px; --space-12: 38px;

  --radius-panel: 0;
  --border: 1px solid var(--ink-soft);
}
```

## Palette rules

1. Everything is monospace. Period.
2. Borders are sharp (radius 0).
3. The dominant color is `var(--ink)` — bright green text on dark.
4. Amber highlights for the one mark per chart that matters.
5. Cyan only for reference lines / thresholds.
```

- [ ] **Step 2: Commit**

```bash
git add skills/bloomberg-dense/references/palette.md
git commit -m "feat(bloomberg-dense): add palette"
```

### Task 41: Write `references/criteria.md`

**Files:**
- Create: `skills/bloomberg-dense/references/criteria.md`

- [ ] **Step 1: Write criteria.md**

```markdown
# bloomberg-dense · Validator criteria

Inherits the structural mechanical checks (text_collision, overflow, etc.)
from the composer's built-in registry. Adds these subjective criteria
(LLM-judge):

## insufficient_density

This theme demands maximum information per pixel. A chart with more
than 40% empty space below the fold is too sparse. Subjective judgment.

## missing_monospace_alignment

Every numeric column is right-aligned and uses `font-variant-numeric:
tabular-nums`. Subjective check on rendered output.

## non_monospace_font

Any text rendered in a non-monospace font violates the aesthetic.
Subjective.

## color_outside_palette

The artifact uses any color outside the declared palette
(`--paper`, `--ink`, `--accent-*`, `--gray-*`). Verified by the
mechanical `token_compliance` check; LLM-judge confirms aesthetic.
```

- [ ] **Step 2: Commit**

```bash
git add skills/bloomberg-dense/references/criteria.md
git commit -m "feat(bloomberg-dense): add density-first criteria"
```

### Task 42: Write `references/patterns.md`

**Files:**
- Create: `skills/bloomberg-dense/references/patterns.md`

- [ ] **Step 1: Write patterns.md**

```markdown
# bloomberg-dense · Patterns

## Default form is a dense table

Most output is a table with many rows, tabular numerics, monospace.

## Sparklines belong inline with numbers

Pair every numeric column with a sparkline of its trend.

## Charts only when comparison is the point

A chart wins only if a table can't show the comparison directly.

## ASCII-art divider lines

Use unicode box-drawing characters for separators between sections:
`────────`, `═══════`, `┄┄┄┄┄┄`.

## Header rows in uppercase

Section labels in caps and letter-spaced for the terminal feel.

## Status indicators inline

Use abbreviations directly in cells: `OK`, `WARN`, `ERR`, `--`. No
icons; no badges; no emoji.
```

- [ ] **Step 2: Commit**

```bash
git add skills/bloomberg-dense/references/patterns.md
git commit -m "feat(bloomberg-dense): add patterns"
```

### Task 43: Register bloomberg-dense in marketplace.json

**Files:**
- Modify: `marketplace.json`

- [ ] **Step 1: Append entry**

```json
{
  "name": "bloomberg-dense",
  "source": "./skills/bloomberg-dense",
  "version": "1.0.0",
  "description": "Terminal-aesthetic theme for component-composer."
}
```

- [ ] **Step 2: Commit**

```bash
git add marketplace.json
git commit -m "chore(marketplace): register bloomberg-dense"
```

---

## Phase 7 — End-to-end verification

### Task 44: Smoke-test all mechanical checks

**Files:**
- (read-only verification)

- [ ] **Step 1: Run the full test suite**

```bash
cd skills/component-composer/scripts
node --test mechanical-checks.test.js
```

Expected: every test passes. Count ≥ 22 tests (scaffold + 3 per check × 9 checks, minus a few that combine cases).

- [ ] **Step 2: Confirm no test runs are skipped**

The output must include the word "pass" or equivalent for each test;
no "skip" or "todo" markers.

### Task 45: Manual integration test — rebuild GitHub chart with atomic-data-viz

**Files:**
- (verification — produces `/tmp/composer-test/session-01/`)

- [ ] **Step 1: Invoke the composer**

In a Claude Code session, say:

> "Use component-composer with atomic-data-viz to render the GitHub usage
> data from /tmp/tufte-gh/repos.json and /tmp/tufte-gh/events.json. Build
> the same four charts we built before. Run the full loop and surface the
> audit summary."

- [ ] **Step 2: Verify the loop runs**

Expected behavior:
- Composer reads atomic-data-viz/themespec.json + references.
- Drafter produces iter-01.html.
- Composer renders, screenshots at 3 viewports.
- Validator returns failure list (likely text_collision, font_size_too_small).
- Drafter redrafts.
- Loop converges in ≤ 6 iterations.

- [ ] **Step 3: Verify outputs**

After the loop ends, check `<session-dir>/`:
- `iterations/iter-NN.html` for every iteration
- `iterations/iter-NN.json` validator output per iteration
- `final.html` (HUD stripped)
- `final.png`
- `final.pdf` (best-effort; may be absent with a note in audit)
- `audit.txt` or `audit.json` with the summary block

- [ ] **Step 4: Open final.html in a browser**

```bash
open <session-dir>/final.html
```

Verify:
- Loads without console errors.
- No external network requests in DevTools network tab.
- No HUD visible.
- Page reads correctly at desktop / tablet / mobile.

### Task 46: Verify the original bugs are now caught

**Files:**
- (verification — uses `/tmp/tufte-gh/charts.html` as a regression fixture)

- [ ] **Step 1: Run mechanical-checks against the v1 fixture**

The original charts.html (before fixes) had three known defects:
- `text_collision` (2025/Dec label merge at chart 1 start)
- `font_size_too_small` (chart 2 language labels rendered at ~22px because of viewBox scaling — wait, those were too BIG, not small. Skip this one.)
- `hidden_mark` (chart 3 short bars rendered as ~2px or thinner)

Save the original buggy version of charts.html (commit `<sha-of-first-render>`) as `/tmp/tufte-gh/charts-v0.html`. Open it in Claude Preview and run `runInBrowser` for each mechanical check.

- [ ] **Step 2: Confirm the defects are detected**

Expected:
- `text_collision` returns `fail` with evidence mentioning '2025' or 'Dec'.
- `hidden_mark` returns `fail` listing the short-bar marks.

Document the result in a brief `tests/regression-fixture-result.md` file.

- [ ] **Step 3: Commit the regression result**

```bash
git add tests/regression-fixture-result.md
git commit -m "test(component-composer): confirm mechanical checks catch original session bugs"
```

### Task 47: Re-run with bloomberg-dense theme

**Files:**
- (verification — produces `/tmp/composer-test/session-02/`)

- [ ] **Step 1: Re-invoke the composer**

> "Now compose the same GitHub data with bloomberg-dense theme."

- [ ] **Step 2: Verify the output is visually distinct**

Open `<session-02-dir>/final.html`. Expected:
- Dark background, bright green ink.
- Monospace everywhere.
- No serifs.
- Same data, visually completely different.

- [ ] **Step 3: Verify composer was unchanged**

```bash
git status skills/component-composer/
```

Expected: no uncommitted changes since Phase 3 finished. The theme swap
required zero composer-code changes.

### Task 48: Verify the 10 success criteria

Walk through `docs/superpowers/specs/2026-05-23-component-composer-goal.md`
§ "Success criteria (binary)" and verify each:

- [ ] 1. atomic-data-viz composer run produced single HTML in html-effectiveness style.
- [ ] 2. Mechanical layer flagged every defect from the previous session (text_collision, hidden_mark).
- [ ] 3. Loop ran to convergence without manual intervention.
- [ ] 4. Switching theme name to bloomberg-dense and re-running produced a visually different chart with zero composer code changes.
- [ ] 5. Audit summary showed iteration count, drafter+judge token usage, resolved-during-loop list.
- [ ] 6. HUD overlaid the preview during iteration; absent from final.html.
- [ ] 7. final.html opens with no console errors and no external requests.
- [ ] 8. final.png and (best-effort) final.pdf were emitted alongside.
- [ ] 9. Theme discovery scan finds atomic-data-viz and bloomberg-dense via themespec.json.
- [ ] 10. Persistent iteration history saved to `<session-dir>/iterations/`.

If any criterion fails, file a TODO in `docs/superpowers/specs/2026-05-23-component-composer-goal.md` § "Open questions" and fix before tagging.

### Task 49: Tag v1.0.0

**Files:**
- (git operations only)

- [ ] **Step 1: Verify clean tree**

```bash
git status
```

Expected: clean working tree, all phases committed.

- [ ] **Step 2: Tag**

```bash
git tag -a v1.0.0 -m "component-composer + atomic-data-viz + bloomberg-dense v1.0.0

Generator-critic loop for single-file HTML data graphics.
Hybrid mechanical + LLM-judge validator.
9 mechanical checks. HUD-during-loop. Multi-theme support proved.

See docs/superpowers/specs/2026-05-23-component-composer-goal.md"
```

- [ ] **Step 3: Confirm tag**

```bash
git tag -l v1.0.0
git show v1.0.0
```

---

## Self-review (do not commit this section)

1. **Spec coverage:** every section of the goal doc — purpose, architecture, all three skills, theme-spec interface, atomic-data-viz refactor, atomic-brand changes, full in-scope list, success criteria — has a task. ✓
2. **Placeholders:** no "TBD", "TODO", "implement later", "appropriate error handling", "similar to Task N". ✓
3. **Type consistency:** validator output shape (`{id, result, viewport, evidence?, suggested_fix?}`) is identical across tasks 12-21. Criterion ids are stable. ✓
4. **CSS variable names:** `--paper`, `--ink`, `--accent-warm`, `--gray-100..900`, `--space-1..12`, `--font-size-h1..caption` consistent across tokens.md, palette.md, base.html, components.md. ✓
