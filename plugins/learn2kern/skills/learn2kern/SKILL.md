---
name: learn2kern
description: >
  STUB. Typography skill. Generates modular type scales from a base size and
  ratio, recommends pairings, audits kerning and tracking, sets line-height
  defaults, and emits ready-to-use CSS / Swift / Compose token files.
  Activates on "type scale", "typography", "font sizes", "modular scale",
  "kerning", "line height", "typographic hierarchy", or "/learn2kern".
---

# learn2kern

**Status: STUB — TypeScale generator is the v1 cornerstone; other features deferred.**

This skill is a placeholder. The intent and the TypeScale generator contract
are below.

## Intent

Typography is the layer where brand systems most often drift. learn2kern
gives a deterministic way to:

- Generate a modular type scale from a base size + ratio
- Audit an existing type scale for irregularity
- Recommend font pairings by classification (sans + serif, neo-grotesque + slab, etc.)
- Set line-height defaults that survive at every scale step
- Emit token files in CSS, Swift, and Compose

## v1 cornerstone — TypeScale generator

### Input

| Field | Required | Example |
|---|---|---|
| `base_size_px` | Yes | `16` |
| `ratio` | Yes | `1.25` (Major Third) |
| `steps_up` | Yes | `6` |
| `steps_down` | Yes | `2` |
| `unit` | No | `rem` (default), `px`, `em`, `pt`, `sp` |
| `rounding` | No | `none` (default), `0.25`, `0.5`, `1` |

### Ratios (named)

| Name | Ratio | Use case |
|---|---|---|
| Minor Second | 1.067 | Very dense UI |
| Major Second | 1.125 | Dense product UI |
| Minor Third | 1.200 | Standard product UI |
| Major Third | 1.250 | Marketing pages |
| Perfect Fourth | 1.333 | Expressive marketing |
| Augmented Fourth | 1.414 | Editorial |
| Perfect Fifth | 1.500 | Display-heavy editorial |
| Golden Ratio | 1.618 | Posters, brand systems |

### Output (canonical)

```
type-scale:
  base: 16px
  ratio: 1.250 (Major Third)
  steps:
    -2: 10.24px   (0.640rem)
    -1: 12.80px   (0.800rem)
     0: 16.00px   (1.000rem)   ← base
     1: 20.00px   (1.250rem)
     2: 25.00px   (1.563rem)
     3: 31.25px   (1.953rem)
     4: 39.06px   (2.441rem)
     5: 48.83px   (3.052rem)
     6: 61.04px   (3.815rem)
  line-height-defaults:
    body:    1.5    (steps -2 to 0)
    heading: 1.25   (steps 1 to 4)
    display: 1.10   (steps 5+)
```

### Token emission targets

| Target | Format |
|---|---|
| CSS | Custom properties (`--type-0`, `--type-1`, …) |
| Tailwind | `theme.fontSize` extension |
| Swift | `Font.system(size:)` constants |
| Compose | `TextStyle` definitions |
| Design tokens | W3C Design Tokens JSON |

## v2 features (deferred)

| Feature | Notes |
|---|---|
| Pair recommender | Given a primary typeface, suggest 2–3 complementary pairings |
| Kerning audit | Check letter-pair spacing in rendered output |
| Tracking rules | Set letter-spacing by size step (tighter at display, looser at small) |
| Optical alignment audit | Identify visual misalignment between adjacent text blocks |
| Vertical rhythm | Snap to a baseline grid; emit grid-aligned line-heights |
| Variable-font axis ranges | Constrain `wght`, `wdth`, `opsz` axes by use case |
| Accessibility | Min size, contrast, dyslexia-friendly fallbacks |

## Open questions for the build

1. Generator runtime — embedded prompt logic, or a small TypeScript module called by the prompt?
2. Token-emission format — emit one canonical JSON, then translate; or emit each target natively?
3. Audit mode — should kerning audit require a rendered screenshot, or work from CSS only?
4. Integration with `atomic-brand` — does learn2kern produce `tokens/type.md` directly, or hand off?

## Sizes

| Phase | Size |
|---|---|
| Scaffold + plugin.json + SKILL.md (this stub) | XS |
| TypeScale generator (v1 cornerstone, CSS + Tailwind targets) | M |
| Add Swift + Compose + design-tokens targets | S |
| Pair recommender | M |
| Kerning audit | L |
| Vertical rhythm + variable-font ranges | L |

## Triggers

`type scale` · `typography` · `font sizes` · `modular scale` · `kerning` ·
`line height` · `typographic hierarchy` · `/learn2kern`
