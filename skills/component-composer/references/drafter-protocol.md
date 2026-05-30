# Drafter Protocol (HTML)

Extends the abstract [drafter contract](../../generator-critic/references/drafter-contract.md)
from the `generator-critic` skill. This file specifies the HTML-flavored
implementation. The abstract contract's behavior rules (address every
failure, no new failures, preserve intent, surgical edits) apply
unconditionally and are not repeated here.

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

## Required artifact structure

Every artifact follows these structural rules. The mechanical validator
enforces the ones it can; LLM-judge catches the rest.

1. **HTML heading elements only.** Use `<h1>` through `<h5>` for heading
   roles. No custom `.display`, `.lede`, or `.heading-*` classes for
   headings. The required CSS base in `output-style.md` styles all five
   tags directly.
2. **Metric + unit pattern.** Headline numerics use
   `<span class="metric">N</span><span class="unit">u</span>` so the
   number sits on the type scale and the unit reads as a quiet suffix.
   Bloomberg-style themes may wrap the pair in a flex container with
   `align-items: baseline; gap: var(--space-2);` to lock baseline
   alignment at large sizes.
3. **Semantic data elements.** Use `<time datetime="...">` for
   timestamps, `<code>` for inline identifiers and snippets, `<kbd>`
   for keystrokes, `<pre><code>` for multi-line code, `.id` for repo
   names / hashes that are not strictly code.
4. **Grid for top-level layout.** Wrap every layout block in a `.grid`
   container; children use `.span-*`, `.md-span-*`, `.lg-span-*`
   utilities. Do not invent bespoke flexbox layouts for top-level
   structure. The legacy `.page` class is deprecated — use
   `<div class="grid"><div class="span-full">...</div></div>`.
5. **Theme switch included.** Every artifact ends with the
   `.theme-switch` HTML + the inline switch script from
   `output-style.md`. Themes that support only one mode hide the
   irrelevant buttons via CSS — the markup is still present.
6. **Palette overrides baseline.** The drafter reads `palette.md`
   (theme) AND `output-style.md` (baseline). Where both define the
   same token, palette.md wins. Where palette.md is silent, the
   baseline applies.

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
