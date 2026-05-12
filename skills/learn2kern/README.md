# learn2kern

Typography skill. Generates a complete modular type scale from a base
size and one of eight named ratios.

## What you get

- Type scale across 9 steps (-2 to +6)
- Eight named ratios: Minor Second (1.067) → Golden Ratio (1.618)
- Three line-height bands (body 1.5, heading 1.25, display 1.10)
- Letter-spacing per band: tighter at display, normal at body
- BODY + HEADINGS as separate token families
- Emissions: CSS custom properties + Tailwind theme.fontSize
- Color slots reference external color tokens via `var()` with fallbacks

## Composition

This skill owns typography only. Color tokens are external — the
emitted output references `var(--color-text, #222)` and similar, so it
composes with any project that defines those custom properties (and
falls back to sensible hex defaults when none are present).

## Modes

- **Single-turn happy path** when inputs are stated
- **Conversational intake** (jtbd-style) when inputs are missing

## Scope (v0.1.0)

CSS + Tailwind emission. Responsive scales, Swift/Compose/W3C emissions,
kerning audit, and font-pair recommender deferred to v0.2+.

## Install

```bash
claude plugin marketplace add infolog-io/skills
claude plugin install learn2kern@infolog-io
```

## Triggers

`type scale` · `typography` · `font sizes` · `modular scale` · `/learn2kern`
