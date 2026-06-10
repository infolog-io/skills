# learn2kern

Typography skill. Generates a complete modular type scale from two
required inputs — a base size and one of eight named ratios. If either
is missing, the skill asks for both in one combined question; it never
defaults them silently.

## What you get

- Type scale across 9 steps (`2xs` to `5xl`, steps -2 to +6)
- Eight named ratios: Minor Second (1.067) → Golden Ratio (1.618)
- Line-height bands (body 1.5, heading 1.25, display 1.10) and
  letter-spacing per band (0 / -0.011em / -0.022em)
- BODY + HEADINGS as separate token families
- CSS custom properties with element bindings (canonical fixture:
  `fixtures/expected-scale-major-third.css`), Tailwind `theme.fontSize`
  (`fixtures/expected-tailwind.js`), and JSON tokens on request
  (`assets/scale-tokens-schema.json`)
- Font-pairing answers from `references/font-pairing.md`

## Composition

This skill owns typography only. Color tokens are external — output
references `var(--color-text, #222)` and similar, composing with any
project that defines `--color-*` custom properties.

## Install

```bash
claude plugin marketplace add infolog-io/skills
claude plugin install learn2kern@infolog-io
```

## Triggers

`type scale` · `typography tokens` · `font sizes` · `modular scale` ·
`line height` · `letter-spacing` · `font pairing` · `/learn2kern`
