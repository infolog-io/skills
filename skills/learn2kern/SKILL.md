---
name: learn2kern
description: >-
  Use when the user asks for a type scale, typography tokens, font sizes,
  modular scale, line height, letter-spacing/kerning defaults, or typographic
  hierarchy for a web project, or invokes "/learn2kern". Also use when
  choosing a scale ratio (Minor Third, Major Third, Golden Ratio) or pairing
  body and heading fonts. Run conversational intake first if base size or
  ratio is not stated. Not for color tokens, font loading, or rendered
  previews.
---

# learn2kern

## Purpose

Generate a typography token set from two inputs: a base size and a named
modular ratio. BODY and HEADINGS emit as separate token families, each
with its own font, weight, line-height, letter-spacing, and color. Color
is external — tokens reference `var(--color-*)` with hex fallbacks.

## Named ratios

Minor Second=1.067 · Major Second=1.125 · Minor Third=1.200 (default
recommendation) · Major Third=1.250 · Perfect Fourth=1.333 ·
Augmented Fourth=1.414 · Perfect Fifth=1.500 · Golden Ratio=1.618.
Derivations and use cases: `references/named-ratios.md`.

## The math

```
step[n].px  = base × (ratio ^ n)
step[n].rem = step[n].px / 16     (CSS root default; configurable)
step[n].pt  = step[n].px × 0.75   (CSS spec: 1px = 0.75pt; 1pt = 1.333px)
```

Round to two decimal places; never round to integer pixels. Default span
`up=6, down=2` gives nine steps, `--font-size-2xs` through
`--font-size-5xl`. The worked Major Third / base-16 scale is in the
canonical fixture and TESTS.md T1.

## Band defaults

| Band | Steps | Line-height | Letter-spacing |
|---|---|---|---|
| Body | -2 to 0 | 1.5 (`--line-height-normal`) | 0em (`--letter-spacing-body`) |
| Heading | 1 to 4 | 1.25 (`--line-height-tight`) | -0.011em (`--letter-spacing-heading`) |
| Display | 5+ | 1.10 (`--line-height-display`) | -0.022em (`--letter-spacing-display`) |

BODY defaults to weight 400; HEADINGS to weight 700 and family `inherit`.
Colors emit as `--font-body-color: var(--color-text, #222)` and
`--bg-page: var(--color-bg, #fff)`.

## Intake

Items 1–2 are REQUIRED. If either is missing, ask for both in ONE
combined question — never default them silently.

1. **Base size** — px
2. **Ratio** — named or custom decimal

Items 3–8 have defaults, applied silently and listed in the emission
header comment:

3. **Steps** — `up=6, down=2`
4. **Body family** — Inter
5. **Heading family** — `inherit`
6. **Weights** — body 400, heading 700
7. **Colors** — external `--color-*` tokens with hex fallbacks
8. **Targets** — CSS always; Tailwind or JSON on request

Run ONE intake turn covering all remaining blanks — never item-by-item
across turns. **Happy path:** when base AND ratio are both stated, skip
intake and emit in one response.

## Output emission

`fixtures/expected-scale-major-third.css` is the single canonical CSS
emission (TESTS.md T12 round-trips against it byte-for-byte). Element
bindings — `body`, `h1`–`h6`, `small` — are included after the `:root`
block in every CSS output. Skeleton:

```css
:root {
  /* learn2kern — <ratio>, base <N>px; applied defaults: <list> */
  /* --font-size-2xs … --font-size-5xl (9 steps) */
  /* --line-height-* and --letter-spacing-* band tokens */
  /* --font-body-* and --font-heading-* (family, weight,
     line-height, letter-spacing, color) */
  --bg-page: var(--color-bg, #fff);
}
/* + element bindings: body, h1–h6, small */
```

Tailwind output follows `fixtures/expected-tailwind.js`. JSON token
output on request, conforming to `assets/scale-tokens-schema.json`.

Include a plain-text sample preview, one row per step (two shown):

```
h1  1.953rem (31.25px)  How vexingly quick daft zebras jump
p   1.000rem (16.00px)  How vexingly quick daft zebras jump (base)
```

## Scope and interfaces

| Layer | Emits | Doesn't emit |
|---|---|---|
| CSS | Custom properties + element bindings | Rendered HTML preview |
| Tailwind | Per `fixtures/expected-tailwind.js` | Device-variant rendering |
| JSON | Per schema, on request | Save/load named scales |
| Preview | Plain-text sample rows | Visual content templates |
| Color | `var(--color-*, fallback)` references | Color token definitions |
| Pairing | Answers from `references/font-pairing.md` | Font loading / `@font-face` |

## Anti-rules

- Do not emit a scale while base size or ratio is unknown — ask the combined intake question first
- Do not collapse BODY and HEADINGS into one token family
- Do not hardcode color values when external `--color-*` tokens are available
- Do not round to integer pixels — subpixel typography is fine
- Do not invent new named ratios or off-scale alias steps (no 0.875rem `sm`/`md`)
