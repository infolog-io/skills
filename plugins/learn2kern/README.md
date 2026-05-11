# learn2kern

**Status: stub.** Typography skill with a TypeScale generator at its core.

## v1 cornerstone — TypeScale generator

Given a base size and a modular ratio, emit a full type scale with:

- Named steps (-2 through +6 by default)
- Line-height defaults per scale band
- Token emissions for CSS, Tailwind, Swift, Compose, W3C design tokens

## Named ratios supported

Minor Second (1.067) · Major Second (1.125) · Minor Third (1.200) ·
Major Third (1.250) · Perfect Fourth (1.333) · Augmented Fourth (1.414) ·
Perfect Fifth (1.500) · Golden Ratio (1.618).

## Deferred to v2

Pair recommender, kerning audit, tracking rules by size band, optical
alignment, vertical rhythm to a baseline grid, variable-font axis
constraints, accessibility checks.

## Sizing (per estimatrix)

| Phase | Size |
|---|---|
| Scaffold (this stub) | XS |
| TypeScale generator (CSS + Tailwind) | M |
| Swift + Compose + W3C targets | S |

## Install (stub)

```bash
claude plugin marketplace add infolog-io/skills
claude plugin install learn2kern@infolog-io
```
