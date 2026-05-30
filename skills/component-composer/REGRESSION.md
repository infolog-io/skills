# Regression Test Report — Mechanical Validator

## Overview

Three bug types were observed during manual development of component-composer.
This document records each defect type, the fixture that replicates it, and
the mechanical layer's verdict when run against the fixture.

Test command: `node skills/component-composer/scripts/regression-test.js`

---

## Bug types under test

### 1. `text_collision` — overlapping SVG text labels

Original defect: two axis tick labels at nearly identical (x, y) coordinates
produced unreadable overlapping text in the rendered chart.

Fixture defect (`regression-buggy.html`):

```html
<text x="50" y="100" font-size="14">Jan 2024</text>
<text x="52" y="103" font-size="14">Jan 2024</text>
```

Both elements share an approximate bounding box of `x≈50, y≈86, w≈100, h≈14`.
The 2 px horizontal and 3 px vertical offset keeps them visually indistinguishable.

**Mechanical verdict on buggy fixture:** `FAIL`
Evidence: `'Jan 2024' overlaps 'Jan 2024'`

**Mechanical verdict on clean fixture:** `PASS`
Fix: labels placed at x=50 and x=200, no overlap.

---

### 2. `hidden_mark` — sub-pixel data marks

Original defect: a bar chart rect was rendered with `width="1"`, making it
effectively invisible at any reasonable screen DPI.

Fixture defect (`regression-buggy.html`):

```html
<rect class="bar" x="100" y="50" width="1" height="10" data-label="Q1"/>
```

The check requires both width and height ≥ 2 px and opacity ≥ 0.3.

**Mechanical verdict on buggy fixture:** `FAIL`
Evidence: `'Q1': width=1, height=10`

**Mechanical verdict on clean fixture:** `PASS`
Fix: rect uses `width="40" height="80"`.

---

### 3. `token_compliance` — literal CSS values outside `:root`

Original defect: a selector outside `:root` used a hardcoded hex color instead
of a CSS custom property reference. This breaks theme-swapping because the
value cannot be overridden by changing `:root` variables.

Fixture defect (`regression-buggy.html`):

```css
.foo { color: #ff0000; }
```

The check scans CSS declarations, skips `:root`, and flags any token-sensitive
property (color, fill, font-size, padding, etc.) that carries a literal hex,
rgb(), hsl(), or non-zero px value.

**Mechanical verdict on buggy fixture:** `FAIL`
Evidence: `.foo { color: #ff0000 }` (literal hex outside `:root`)

**Mechanical verdict on clean fixture:** `PASS`
Fix: literal moved into `:root { --foo-color: #ff0000; }`, selector uses
`color: var(--foo-color)`.

---

## Summary

| Check             | Buggy fixture | Clean fixture |
|-------------------|--------------|---------------|
| `text_collision`  | FAIL         | PASS          |
| `hidden_mark`     | FAIL         | PASS          |
| `token_compliance`| FAIL         | PASS          |

All 6 assertions in `regression-test.js` pass. The mechanical layer correctly
classifies both fixture types with zero false positives on the clean fixture.

---

## Fixtures

- `skills/component-composer/template/fixtures/regression-buggy.html` — three synthetic defects
- `skills/component-composer/template/fixtures/regression-clean.html` — all defects corrected

## Test runner

- `skills/component-composer/scripts/regression-test.js`

The runner uses lightweight regex-based HTML parsing (no external DOM library)
to construct the plain-object data shapes that each check function expects.
This is intentional: the checks are pure functions and must not require a live
browser to validate their core classification logic.
