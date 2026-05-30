# Validator Protocol (HTML)

Extends the abstract [validator contract](../../generator-critic/references/validator-contract.md)
from the `generator-critic` skill. This file specifies the HTML-flavored
implementation: which mechanical checks are built-in, how the LLM-judge
prompt is shaped for HTML artifacts, and the per-viewport context label
scheme. The abstract dispatch rule (mechanical first, LLM-judge fallback)
applies unconditionally.

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
