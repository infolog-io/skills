---
name: learn2kern
description: >
  Typography skill. Generates modular type scales from a base size and
  named ratio, emits BODY and HEADINGS token families separately, with
  line-height bands and letter-spacing defaults per band. Outputs CSS
  custom properties and Tailwind theme.fontSize. Color slots reference
  external `--color-*` custom properties via var() with sensible
  fallbacks. Runs conversational intake when inputs are missing.
  Activates on "type scale", "typography", "font sizes", "modular scale",
  "kerning", "line height", "typographic hierarchy", or "/learn2kern".
---

# learn2kern

## Purpose

Generate a complete typography token set from two inputs: a base size and
a named modular ratio. Emit BODY and HEADINGS as separate token families
so each can have its own font, weight, line-height, letter-spacing, and
color. Color tokens are external — the emit references `var(--color-*)`
with hex fallbacks, so the skill composes with any project that defines
those custom properties.

## The eight named ratios

| Name | Ratio | Musical interval | Use case |
|---|---|---|---|
| Minor Second | 1.067 | m2 | Very dense UI, compact tables |
| Major Second | 1.125 | M2 | Dense product UI |
| Minor Third | 1.200 | m3 | Standard product UI (default recommendation) |
| Major Third | 1.250 | M3 | Marketing pages |
| Perfect Fourth | 1.333 | P4 | Expressive marketing |
| Augmented Fourth | 1.414 | A4 (tritone) | Editorial |
| Perfect Fifth | 1.500 | P5 | Display-heavy editorial |
| Golden Ratio | 1.618 | φ | Posters, brand systems, hero displays |

See `references/named-ratios.md` for derivation and use-case notes.

## The math

For a scale with `base` (px), `ratio` (decimal), `steps_up` and `steps_down`:

```
step[n].px = base × (ratio ^ n)
step[n].rem = step[n].px / 16     (CSS root default; can be configured)
step[n].pt  = step[n].px × 0.75   (CSS spec: 1pt = 1.333px = 0.75 inverse)
```

For Major Third (`ratio = 1.250`, `base = 16`):

| Step | Px | Rem | Pt |
|---|---|---|---|
| -2 | 10.24 | 0.640 | 7.68 |
| -1 | 12.80 | 0.800 | 9.60 |
|  0 | 16.00 | 1.000 | 12.00 |
|  1 | 20.00 | 1.250 | 15.00 |
|  2 | 25.00 | 1.563 | 18.75 |
|  3 | 31.25 | 1.953 | 23.44 |
|  4 | 39.06 | 2.441 | 29.30 |
|  5 | 48.83 | 3.052 | 36.62 |
|  6 | 61.04 | 3.815 | 45.78 |

Round to two decimal places. No rounding to integer pixels (subpixel
typography renders fine on modern displays).

## Line-height bands

| Band | Steps | Default line-height | Token |
|---|---|---|---|
| Body | -2 to 0 | 1.5 | `--line-height-normal` |
| Heading | 1 to 4 | 1.25 | `--line-height-tight` |
| Display | 5+ | 1.10 | `--line-height-display` |

User overrides per call accepted; defaults match common publishable
typography.

## Letter-spacing per band

| Band | Default letter-spacing | Token |
|---|---|---|
| Body | 0em | `--letter-spacing-body` |
| Heading | -0.011em | `--letter-spacing-heading` |
| Display | -0.022em | `--letter-spacing-display` |

Tighter at larger sizes is the convention because optical spacing
loosens as type grows.

## BODY and HEADINGS as separate token families

Two independent sets. Each can have its own font, weight, line-height,
letter-spacing, color.

```css
/* BODY family */
--font-body-family
--font-body-weight
--font-body-line-height
--font-body-letter-spacing
--font-body-color

/* HEADINGS family */
--font-heading-family
--font-heading-weight
--font-heading-line-height
--font-heading-letter-spacing
--font-heading-color
```

If the user does not specify a HEADINGS family, default to `inherit`
(matches BODY). If the user does not specify weight, default to 400 for
BODY and 700 for HEADINGS.

## Color slots — external color tokens

Color tokens reference external `--color-*` custom properties with
fallback values:

```css
--font-body-color: var(--color-text, #222);
--font-heading-color: var(--color-text, #222);
--bg-page: var(--color-bg, #fff);
```

This skill owns typography only. Color comes from whatever defines the
`--color-text` and `--color-bg` custom properties in the consuming
project. If nothing defines them, the fallback hex applies.

## Conversational intake

When inputs are missing, run an active intake — one focused question per
turn — until enough info exists to emit.

### Blank-Detection Checklist

1. **Base size** — px (default 16, but ask if not stated)
2. **Ratio** — named or custom decimal (default Minor Third if unsure)
3. **Steps up / steps down** — default `up=6, down=2`
4. **Body family** — recommend Inter as a safe default
5. **Heading family** — `inherit` unless user specifies
6. **Weights** — body 400, heading 700 (recommend; ask if uncommon)
7. **Color tokens** — defer to external `--color-*` tokens or accept hex fallbacks
8. **Emission targets** — CSS (always); Tailwind (ask if relevant)

### Intake ordering

1. Base + ratio (without these, no scale)
2. Family choices (body, then heading)
3. Optional overrides (weights, line-heights, letter-spacings)
4. Emission targets

### Single-turn happy path

If the user states base, ratio, family choices, and intent, skip intake:

> User: "Generate a type scale with base=16, Major Third, 6 up 2 down, Inter for body and headings, emit CSS and Tailwind"
>
> Skill: [emits the full scale + CSS + Tailwind in one response]

## Output emission

### CSS custom properties

```css
:root {
  /* Type scale (Major Third, base 16px) */
  --font-size-2xs: 0.640rem;   /* 10.24px */
  --font-size-xs:  0.800rem;   /* 12.80px */
  --font-size-sm:  0.875rem;   /* alias if needed */
  --font-size-base: 1.000rem;  /* 16.00px */
  --font-size-md:  1.000rem;   /* alias if needed */
  --font-size-lg:  1.250rem;   /* 20.00px */
  --font-size-xl:  1.563rem;   /* 25.00px */
  --font-size-2xl: 1.953rem;   /* 31.25px */
  --font-size-3xl: 2.441rem;   /* 39.06px */
  --font-size-4xl: 3.052rem;   /* 48.83px */
  --font-size-5xl: 3.815rem;   /* 61.04px */

  /* Line-height bands */
  --line-height-normal: 1.5;
  --line-height-tight: 1.25;
  --line-height-display: 1.10;

  /* Letter-spacing per band */
  --letter-spacing-body: 0em;
  --letter-spacing-heading: -0.011em;
  --letter-spacing-display: -0.022em;

  /* BODY family */
  --font-body-family: 'Inter', system-ui, sans-serif;
  --font-body-weight: 400;
  --font-body-line-height: var(--line-height-normal);
  --font-body-letter-spacing: var(--letter-spacing-body);
  --font-body-color: var(--color-text, #222);

  /* HEADINGS family */
  --font-heading-family: inherit;
  --font-heading-weight: 700;
  --font-heading-line-height: var(--line-height-tight);
  --font-heading-letter-spacing: var(--letter-spacing-heading);
  --font-heading-color: var(--color-text, #222);

  /* Page background (for completeness) */
  --bg-page: var(--color-bg, #fff);
}
```

### Tailwind theme.fontSize

```js
// tailwind.config.{js,ts}
module.exports = {
  theme: {
    extend: {
      fontSize: {
        '2xs':  ['0.640rem', { lineHeight: '1.5' }],
        'xs':   ['0.800rem', { lineHeight: '1.5' }],
        'base': ['1.000rem', { lineHeight: '1.5' }],
        'lg':   ['1.250rem', { lineHeight: '1.25' }],
        'xl':   ['1.563rem', { lineHeight: '1.25' }],
        '2xl':  ['1.953rem', { lineHeight: '1.25' }],
        '3xl':  ['2.441rem', { lineHeight: '1.25' }],
        '4xl':  ['3.052rem', { lineHeight: '1.10' }],
        '5xl':  ['3.815rem', { lineHeight: '1.10' }],
      },
      letterSpacing: {
        body:    '0em',
        heading: '-0.011em',
        display: '-0.022em',
      },
      fontFamily: {
        body:    ['Inter', 'system-ui', 'sans-serif'],
        heading: ['inherit'],
      },
    },
  },
};
```

## Sample-content preview (text-based)

When emitting, include a text preview showing each step with a sample
sentence. The user's demo UI can render this visually; the skill emits
the data.

```
h1  1.953rem (31.25px)  How vexingly quick daft zebras jump
h2  1.563rem (25.00px)  How vexingly quick daft zebras jump
h3  1.250rem (20.00px)  How vexingly quick daft zebras jump
h4  1.000rem (16.00px)  How vexingly quick daft zebras jump (base)
h5  0.800rem (12.80px)  How vexingly quick daft zebras jump
h6  0.640rem (10.24px)  How vexingly quick daft zebras jump
p   1.000rem (16.00px)  How vexingly quick daft zebras jump
small 0.875rem (14.00px) How vexingly quick daft zebras jump
```

## Worked example — happy path (T10)

User: "Generate a type scale with base=16, Major Third, 6 up 2 down, Inter for body and headings, emit CSS and Tailwind"

Skill:

```
Type Scale — Major Third, base 16px

Steps:
  -2: 10.24px / 0.640rem / 7.68pt
  -1: 12.80px / 0.800rem / 9.60pt
   0: 16.00px / 1.000rem / 12.00pt   ← base
   1: 20.00px / 1.250rem / 15.00pt
   2: 25.00px / 1.563rem / 18.75pt
   3: 31.25px / 1.953rem / 23.44pt
   4: 39.06px / 2.441rem / 29.30pt
   5: 48.83px / 3.052rem / 36.62pt
   6: 61.04px / 3.815rem / 45.78pt

Line-heights:
  body (-2..0):    1.5
  heading (1..4):  1.25
  display (5+):    1.10

Letter-spacing:
  body:    0em
  heading: -0.011em
  display: -0.022em

CSS:
[full CSS block as above]

Tailwind:
[full Tailwind block as above]
```

## Worked example — conversational intake (T9)

User: "generate a type scale"

Skill (turn 1): To generate a scale, I need two inputs:

1. **Base size** — typically 16px for web. Use 16, or another value?
2. **Ratio** — Minor Third (1.200) is the safest starting point for product UI;
   Major Third (1.250) for marketing pages; Golden Ratio (1.618) for hero displays.
   Pick a named ratio, or specify a decimal.

User: "16px base, Major Third"

Skill (turn 2): Good. Two more:

3. **Body font family** — Inter is a safe default. Override or accept?
4. **Heading font family** — usually inherits from body unless you have a display face.

User: "Inter for both, default everything else"

Skill (final): [emits the scale + CSS + Tailwind as in the happy-path example]

## References

- `references/named-ratios.md` — derivation and use case for each named ratio
- `references/font-pairing.md` — body + heading family pairing principles

## Triggers

`type scale` · `typography` · `font sizes` · `modular scale` · `kerning` ·
`line height` · `typographic hierarchy` · `/learn2kern`

## Interfaces

| Layer | Convention |
|---|---|
| Color | References external `--color-text` and `--color-bg` custom properties via `var()` with hex fallbacks |
| Type scale output | Markdown table + CSS custom properties + Tailwind `theme.fontSize` object + JSON conforming to `assets/scale-tokens-schema.json` |
| Sample preview | Plain-text table with step / size / sample sentence; consumers render visually |

## What this skill emits — and what it doesn't

| Emits | Doesn't emit (UI tool's job) |
|---|---|
| CSS custom properties | Rendered HTML preview |
| Tailwind theme.fontSize | Mobile/desktop variant rendering |
| Structured token JSON (per schema) | Save/load named scales (persistence) |
| Text-based sample-content preview | Visual content templates (blog post, landing page) |

The skill is portable across consumers. Your demo UI renders. The
skill is the source of truth for the scale.

## Anti-rules

- Do not emit a scale without first satisfying the Blank-Detection Checklist
- Do not collapse BODY and HEADINGS into one token family
- Do not hardcode color values when external `--color-*` tokens are available
- Do not round to integer pixels — subpixel typography is fine
- Do not invent new named ratios; the eight are canonical
