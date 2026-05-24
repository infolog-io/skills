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
