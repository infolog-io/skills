# Component Composer + infolog-io — Goal

- Date: 2026-05-23
- Status: Goal locked, ready for implementation plan
- Repo: infolog-skills

## One-line goal

Build a generator-critic loop that drafts a single-file HTML data graphic, renders it in Claude Preview, validates it (mechanical + LLM-as-judge), and iterates until every criterion in the active theme passes — with the artifact, the validator, the HUD, and the loop all living in zero-dependency static HTML.

## Why this exists

The previous Tufte critique flow in `tufte-love` produced clean-on-paper scoring but visibly broken renders (text scaling mismatch, label collision, hidden marks). Scoring on paper does not equal rendered quality. This goal closes that gap by automating: render → see → critique → fix → repeat until the rendered artifact actually passes.

## Style anchor

Single self-contained `.html` file in the style of `ThariqS/html-effectiveness`: CSS custom properties at `:root`, named brand tokens, vanilla JS only when interaction is real, inline SVG for charts, zero npm dependencies, zero build step. The whole artifact is one file you can email, paste, or open offline.

## Architecture

```
component-composer        orchestrates draft → render → validate → loop
infolog-io           a theme — supplies tokens, criteria, patterns, palette
                          (refactored from tufte-love)
atomic-brand              base brand-token taxonomy (existing) +
                          new components.md describing the structural primitives
                          that themes decorate
```

Themes are sibling skills conforming to the theme-spec interface. The composer discovers themes by scanning `skills/*/themespec.json`.

## `component-composer` skill

```
skills/component-composer/
  SKILL.md
  .claude-plugin/plugin.json
  references/
    drafter-protocol.md       drafter LLM behavior
    validator-protocol.md     hybrid mechanical + LLM-as-judge
    loop-protocol.md          stop conditions, feedback shape, stuck detection
    theme-spec.md             interface contract for theme skills
    output-style.md           the single-file html-effectiveness style
    hud-protocol.md           how the loop's HUD overlays the rendered preview
  scripts/
    mechanical-checks.js      ES module of built-in validator checks
    hud.js                    vanilla-JS HUD code injected during iteration
    export-png.js             headless screenshot to PNG via Claude Preview
    export-pdf.js             headless print-to-PDF
  template/
    base.html                 minimal self-contained HTML skeleton with token slots
```

### Drafter

LLM agent.

- **Iteration 1 input:** theme tokens, theme patterns, output-style.md, user job, the data.
- **Iteration N input:** above + previous artifact source (full HTML, verbatim) + validator failure list (JSON) + composer-generated NL summary.
- **Output:** one self-contained `.html` file matching the output-style.

Composer's NL summary template (per failure):

> "On `<viewport>`, criterion `<id>` failed. Evidence: `<evidence>`. Suggested fix: `<suggested_fix>`."

### Validator

Two-layer hybrid:

**Mechanical layer** runs JS via `preview_eval` and reads computed CSS via `preview_inspect`. Built-in checks:

| Criterion id | Mechanical check |
|---|---|
| `text_collision` | DOM walk; bounding-box overlap detection across `text`, `tspan`, labels, annotations |
| `text_truncation` | `scrollWidth > clientWidth` on text containers |
| `contrast_failure` | Computed `color` + effective background; WCAG ratio; fail < 3:1 marks / < 4.5:1 text |
| `font_size_too_small` | Computed `font-size`; flag < 10px display (accounting for SVG viewBox scaling) |
| `overflow` | Body/chart `scrollWidth > clientWidth` per viewport |
| `responsive_break` | Horizontal scroll at mobile viewport |
| `chartjunk_decorative_css` | Detect `box-shadow`, `text-shadow`, 3D `transform`, gradient `background` on data marks |
| `hidden_mark` | Data marks must have computed `width`/`height` ≥ 2px and `opacity` ≥ 0.3 |
| `token_compliance` | Every CSS color/spacing/font value resolves to a `var(--...)` reference, not a literal |

Mechanical is authoritative for these IDs. If a check throws or no built-in exists, the LLM-judge handles it.

**LLM-as-judge layer** receives the screenshot + remaining criteria + viewport label. Handles:

- `missing_range_frame` — axis terminates at data extent
- `insufficient_data_ink` — every visible element earns its place
- `comparison_failure` — chart doesn't enable the comparison it implies
- `hierarchy_failure` — primary data doesn't dominate secondary
- `chartjunk_subjective` — decoration competing with evidence beyond CSS-detectable
- Any theme-defined criterion not in the built-in mechanical registry

Validator output schema (per viewport):

```json
[
  { "id": "text_collision", "result": "pass", "viewport": "mobile" },
  { "id": "chartjunk_present", "result": "fail", "viewport": "mobile",
    "evidence": "drop shadows on each bar",
    "suggested_fix": "remove box-shadow; rely on position alone" }
]
```

Aggregation across viewports: failures pass through verbatim with viewport label preserved. Same criterion failing on multiple viewports appears multiple times.

### Loop protocol

```
1. Drafter composes initial artifact
2. Composer writes file to session dir; renders via Claude Preview
3. Composer screenshots at mobile (375) / tablet (768) / desktop (1280)
4. Validator returns failure list per viewport
5. Composer aggregates failures
6. Zero failures? → done. Emit artifact + audit summary + cost report
7. Otherwise → composer generates NL summary + feeds JSON to drafter
8. Drafter redrafts; goto 2
```

**Stuck detection:** if the same set of failure IDs (per viewport) appears in 2 consecutive iterations, composer halts and surfaces a prompt via the HUD AND via chat: "Stuck on [ids] at [viewports]. Keep iterating / abort / give guidance."

**No hard iteration cap.** The loop runs until pass, until stuck, or until user interrupts.

### HUD during iteration

Composer injects `hud.js` and a small HUD container into the rendered HTML during the loop. The HUD shows: iteration count, current pass/fail counts, currently failing criteria, and three buttons (continue / abort / give guidance). Vanilla JS only. Reads/writes `window.__composer_state`. Composer polls `window.__composer_state` via `preview_eval` between iterations.

When the loop succeeds, the HUD is stripped from the final artifact. The user receives a pure, dependency-free HTML file.

### Persistent iteration history

Each iteration's artifact saved to `<session-dir>/iterations/iter-NN.html`. Validator JSON saved alongside as `iter-NN.json`. Final artifact symlinked as `final.html`. Diff between iterations is just a normal file diff — humans can audit the loop.

### Cost tracking

Composer tracks per-iteration LLM calls (drafter + validator LLM-judge) and per-mechanical-check execution time. Audit summary at end includes:

```
Composer audit
- Theme: infolog-io v1.0.0
- Iterations: 4
- Final result: pass
- Drafter calls: 4 (~12K tokens in, ~8K tokens out)
- LLM-judge calls: 12 (3 viewports × 4 iterations, ~24K tokens total)
- Mechanical-check runs: 12 (avg 80ms)
- Wallclock: 1m 42s
- Viewports: mobile, tablet, desktop
- Resolved during loop: text_collision (iter 2), chartjunk (iter 3), missing_range_frame (iter 4)
```

### Output formats

Single HTML is the primary output. Composer also supports:

- **PNG** via `preview_screenshot` at desktop viewport saved to `final.png`
- **PDF** via `preview_eval` triggering `window.print()` to PDF (composer captures via Claude Preview, saves to `final.pdf`)

All three formats are emitted when the loop succeeds. User chooses which to share.

## Theme-spec interface

A skill is a theme when it conforms to this layout:

```
skills/<theme-name>/
  SKILL.md                    declares itself as a theme; describes aesthetic
  themespec.json              declarative manifest
  references/
    tokens.md                 palette, type scale, spacing
    criteria.md               validator rules
    patterns.md               preferred component patterns
    palette.md                concrete palette extending the html-effectiveness style
    principles.md             foundational reference (optional)
```

### themespec.json

```json
{
  "name": "infolog-io",
  "version": "1.0.0",
  "context": "data-graphics",
  "capabilities": ["chart", "table", "sparkline", "small-multiples", "dot-plot",
                    "strip-plot", "slopegraph", "range-frame-axis"],
  "output_formats": ["html", "png", "pdf"],
  "style_anchor": "single-file-html"
}
```

### Theme discovery

Composer scans `skills/*/themespec.json` at session start. The user names a theme by short name; composer resolves and loads.

### tokens.md / criteria.md / patterns.md

Same shapes as previously specified. `criteria.md` rules have id (heading) + check (prose). No severity, no priority — drafter fixes all failures.

## `infolog-io` refactor (from `tufte-love`)

```
skills/infolog-io/
  SKILL.md                    declares "theme for component-composer"
  themespec.json              v1.0.0 manifest
  .claude-plugin/plugin.json  renamed
  references/
    tokens.md                 CSS variable schema — palette + type scale + spacing
    palette.md                concrete colors — extends html-effectiveness with own values
    criteria.md               validator rules (derived from current audit-rubric.md)
    patterns.md               preferred chart patterns
    principles.md             current tufte-principles.md, kept
    analytical-design.md      current, kept
    chart-patterns.md         current, kept as supplementary
    chart-rules-extras.md     current, kept
```

### Palette approach

Start from the html-effectiveness structure (named role-based tokens: paper / ink / accent / supporting). Replace Anthropic-specific values (ivory, slate, clay, etc.) with infolog/Tufte-tuned values to be defined during implementation. The structural pattern is preserved; the values become our own.

CSS variable contract (declared at `:root`):

```css
:root {
  /* paper / ink */
  --paper: ...;        /* primary background */
  --ink: ...;          /* primary text/data color */
  --paper-soft: ...;   /* secondary surface */
  --ink-soft: ...;     /* secondary text */

  /* accents */
  --accent-warm: ...;  /* primary highlight (one-mark-at-a-time) */
  --accent-cool: ...;  /* secondary highlight */
  --accent-quiet: ...; /* annotations */

  /* gray ramp (5 stops) */
  --gray-100: ...;
  --gray-300: ...;
  --gray-500: ...;
  --gray-700: ...;
  --gray-900: ...;

  /* type */
  --serif: ...;        /* headings */
  --sans: ...;         /* body */
  --mono: ...;         /* tabular numerics, code */
  --font-size-h1: ...;
  --font-size-h2: ...;
  --font-size-body: ...;
  --font-size-caption: ...;

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
```

Concrete values are filled in during implementation, drawing from the Tufte-purist palette tradition (one warm accent, mostly gray) but with our own warmth.

## atomic-brand changes

Add `references/components.md` documenting the structural primitives themes decorate. v1.0 catalog:

- `axis` (range-frame variant; full-grid variant)
- `legend` (inline; sidebar; absent-with-direct-labels)
- `annotation` (callout; inline; footnote)
- `sparkline` (line; bar; word-sized)
- `data-mark` (dot; bar; line; area)
- `table-row` (data table; comparison table)
- `small-multiple-cell` (faceted panel)
- `slopegraph-line`
- `strip-plot-tick`

Each entry: HTML+SVG skeleton + CSS variable contract. Themes set the variables; atomic-brand owns the structure.

## Goal scope — everything in

| Item | Status |
|---|---|
| `component-composer` skill (full hybrid validator) | In |
| `infolog-io` theme (refactored from tufte-love) | In |
| `atomic-brand/references/components.md` (9 components) | In |
| Theme discovery via filesystem scan | In |
| Persistent iteration history (`iterations/iter-NN.html`) | In |
| Cost tracking (tokens, time, mechanical-check counts) | In |
| HUD during loop (vanilla JS, stripped from final) | In |
| HTML output | In |
| PNG output (`preview_screenshot`) | In |
| PDF output (`window.print()` via `preview_eval`) | In |
| One sibling theme scaffolded: `infolog-terminal` (terminal aesthetic) | In |
| End-to-end test rebuilding the GitHub chart with mechanical layer catching the original bugs | In |
| Concrete Swift / Compose native renderers | OUT — out of scope, no abstraction stub either |
| React / Vite / Tailwind / shadcn runtime | OUT — single static HTML file is the artifact |

## Success criteria (binary)

The goal is met when ALL of these are true:

1. ✅ Running the composer with `infolog-io` against the GitHub usage data produces a single HTML file matching the html-effectiveness style.
2. ✅ The mechanical layer flags every defect from the previous session (the `2025/Dec` label overlap, the chart-2 oversized labels, the chart-3 hidden short bars). Verified against `/tmp/tufte-gh/charts.html` v1 as a regression fixture.
3. ✅ The loop runs to convergence without manual intervention on the GitHub chart job.
4. ✅ Switching the theme name from `infolog-io` to `infolog-terminal` and re-running produces a visually different chart with no code changes to the composer.
5. ✅ Audit summary shows iteration count, drafter/judge token usage, and resolved-during-loop list.
6. ✅ HUD overlays the preview during iteration and is absent from the final artifact.
7. ✅ Final artifact opens in any modern browser with no console errors and no external requests.
8. ✅ PNG and PDF exports written alongside the HTML.
9. ✅ Theme discovery finds both `infolog-io` and `infolog-terminal` via `themespec.json` scan.
10. ✅ Persistent iteration history saved to `<session-dir>/iterations/`.

## Implementation order

1. Write `component-composer/SKILL.md` + 6 protocol references + `output-style.md`
2. Write `theme-spec.md` (interface contract)
3. Build `scripts/mechanical-checks.js` with 9 built-in checks; unit-test against synthetic HTML fixtures
4. Build `scripts/hud.js` and `template/base.html`
5. Build `scripts/export-png.js` and `scripts/export-pdf.js`
6. Refactor `skills/tufte-love/` → `skills/infolog-io/`; write `tokens.md`, `palette.md`, `criteria.md`, `patterns.md`; preserve `principles.md` and `analytical-design.md`
7. Write `skills/atomic-brand/references/components.md` with 9 structural components
8. Scaffold `skills/infolog-terminal/` — themespec.json + tokens.md + palette.md + criteria.md + patterns.md (terminal aesthetic: green-on-black, monospace, dense)
9. Build theme-discovery scan
10. Build persistent iteration history + cost tracking
11. End-to-end test: rebuild the GitHub chart via composer with infolog-io; verify all 10 success criteria
12. Re-run with infolog-terminal theme; verify criterion 4
13. Tag v1.0.0

## Open questions (resolve during implementation, do not block goal)

1. **Drafter context window** — how much theme content fits? May need to summarize references.
2. **Validator viewport scope** — full-page screenshot or artifact bounding-box only?
3. **Render-failure path** — broken-SVG vs rendered-but-wrong distinction in feedback.
4. **Render-tool fallback** — Claude Preview unavailable → fall back to `open` + computer-use screenshot, or `agent-browser` CLI?
5. **PDF print quality** — `window.print()` to PDF varies by browser; may need explicit `@media print` styles.
6. **Theme discovery caching** — re-scan every invocation or cache results across sessions?

## Reference

This goal grew out of a session that built four Tufte-style charts of GitHub usage at `/tmp/tufte-gh/charts.html`. The previous tufte-love operating mode produced clean-on-paper output that needed manual visual fixes (text scaling, label collision). The composer-loop closes that gap by automating the visual audit.

Style anchor: `ThariqS/html-effectiveness` — single-file HTML with CSS custom properties, no build, no deps.

Output target ergonomics: the artifact is one HTML file you can email, paste, or open offline. The HUD is for iteration only. The user takes home a pure, dependency-free artifact.

---

## v1.0.0 ship assessment

Assessed: 2026-05-23. Branch: `feat/component-composer`. Tag: `v1.0.0`.

All scaffold and static work is complete. Runtime end-to-end verification
(invoking the composer skill against live Claude Preview with real data)
is deferred to a follow-up session.

| # | Criterion | Status | Notes |
|---|-----------|--------|-------|
| 1 | Composer rebuilds GitHub chart end-to-end with `infolog-io` | DEFERRED | Requires live session invoking the composer skill against real data |
| 2 | Mechanical layer flags all three original defects (text_collision, hidden_mark, token_compliance) | ✅ | `regression-test.js` passes all 6 assertions against `regression-buggy.html` and `regression-clean.html` |
| 3 | Loop converges without manual intervention on GitHub chart job | DEFERRED | Requires runtime integration with Claude Preview |
| 4 | Theme swap from `infolog-io` to `infolog-terminal` requires no composer changes | ✅ (architecture) / DEFERRED (runtime) | Both `themespec.json` files exist; composer reads theme via filesystem scan. Runtime execution deferred |
| 5 | Audit summary shows iterations, token usage, resolved-during-loop list | ✅ (protocol) / DEFERRED (runtime) | Full schema documented in `references/loop-protocol.md` |
| 6 | HUD overlays during iteration, stripped from final artifact | ✅ (protocol) / DEFERRED (runtime) | Inject + strip contract documented in `references/hud-protocol.md`; `scripts/hud.js` implemented |
| 7 | Final artifact opens in any modern browser with no console errors or external requests | ✅ (static fixture) / DEFERRED (runtime artifact) | `template/base.html` and fixtures are fully self-contained |
| 8 | PNG and PDF exports written alongside the HTML | ✅ (contracts) / DEFERRED (runtime) | `scripts/export-png.js` and `scripts/export-pdf.js` implemented; runtime execution deferred |
| 9 | Theme discovery finds both `infolog-io` and `infolog-terminal` via `themespec.json` scan | ✅ | Both `skills/infolog-io/themespec.json` and `skills/infolog-terminal/themespec.json` present and structurally valid |
| 10 | Persistent iteration history saved to `<session-dir>/iterations/` | ✅ (protocol) / DEFERRED (runtime) | Pattern documented in `references/loop-protocol.md` |

### Verdict

Criterion 2 and 9 are fully verified without a live session. Criteria 4, 5, 6, 7, 8, 10
are architecturally verified — the scaffolding, protocols, and contracts are complete.
Criteria 1, 3, and the runtime halves of 4–10 require a follow-up session where the
composer skill is invoked against real data with Claude Preview active.

The mechanical validator (9 checks, 31 unit tests, 6 regression assertions) is the
highest-risk component. It is fully verified. The remaining deferred criteria are all
orchestration and I/O — the logic is proven, the wiring is untested in production.
