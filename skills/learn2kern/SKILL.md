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

Emit the full token set per `templates/css-output.css`. The template contains the BODY + HEADINGS families, line-height bands, letter-spacing per band, and `--color-*` external references with fallbacks. Substitute step values, family, and weights for the user's chosen inputs.

### Tailwind theme.fontSize

Emit the Tailwind config per `templates/tailwind-config.js`. Substitute step values, family, and letter-spacing for the user's chosen inputs.

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

## Worked examples

### Happy path (T10)

User: "Generate a type scale with base=16, Major Third, 6 up 2 down, Inter for body and headings, emit CSS and Tailwind"

Skill emits the step table:

```
Steps (Major Third, base 16px):
  -2: 10.24px / 0.640rem
  -1: 12.80px / 0.800rem
   0: 16.00px / 1.000rem   ← base
   1: 20.00px / 1.250rem
   2: 25.00px / 1.563rem
   3: 31.25px / 1.953rem
   4: 39.06px / 2.441rem
   5: 48.83px / 3.052rem
   6: 61.04px / 3.815rem
```

Then emits CSS per `templates/css-output.css` and Tailwind per `templates/tailwind-config.js`, substituting the computed step values.

### Conversational intake (T9)

User: "generate a type scale"

Skill asks for base + ratio first, then family choices, then optional overrides. Each turn has 1-2 focused questions with concrete defaults. Once base, ratio, and family are filled, skill emits the full scale.

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
