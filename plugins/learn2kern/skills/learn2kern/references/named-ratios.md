# Named Ratios

Eight canonical modular ratios. Each comes from a musical interval — the
correspondence is not coincidence; musical intervals describe ratios of
frequencies, and our eye finds the same ratios pleasant in visual scale.

## The eight

### Minor Second — 1.067

- **Decimal**: 1.067
- **Musical**: minor second (chromatic half-step, 16:15)
- **Derivation**: `2^(1/12)` ≈ 1.0595 (semi-tempered) rounded conventionally to 1.067
- **Use case**: very dense UI, data-heavy tables where every step must be readable
- **Feel**: nearly imperceptible scale change between steps; feels uniform
- **Warning**: at 6+ steps up, sizes are very close; hierarchy gets muddy

### Major Second — 1.125

- **Decimal**: 1.125
- **Musical**: major second (whole step, 9:8)
- **Derivation**: 9/8 exactly
- **Use case**: dense product UI; admin dashboards
- **Feel**: subtle hierarchy; appropriate for utility-heavy interfaces
- **Caveat**: not enough contrast for marketing surfaces

### Minor Third — 1.200

- **Decimal**: 1.200
- **Musical**: minor third (6:5)
- **Derivation**: 6/5 exactly
- **Use case**: **standard product UI — the safest recommendation**
- **Feel**: clean hierarchy; works for both UI and content
- **Notes**: 16px base with Minor Third gives a familiar 12/14/16/19/23/27/33 progression

### Major Third — 1.250

- **Decimal**: 1.250
- **Musical**: major third (5:4)
- **Derivation**: 5/4 exactly
- **Use case**: marketing pages, blogs, content-forward sites
- **Feel**: more expressive than Minor Third; comfortable hierarchy
- **Sample at base=16**: 10.24, 12.80, 16, 20, 25, 31.25, 39.06, 48.83, 61.04

### Perfect Fourth — 1.333

- **Decimal**: 1.333
- **Musical**: perfect fourth (4:3)
- **Derivation**: 4/3 (1.333...)
- **Use case**: expressive marketing; product pages with display headlines
- **Feel**: noticeable rhythm between sizes; energetic
- **Caveat**: at small bases, the smallest steps get tight

### Augmented Fourth — 1.414

- **Decimal**: 1.414
- **Musical**: tritone, augmented fourth (∝ √2)
- **Derivation**: √2 (paper-size aspect ratio; 1.4142...)
- **Use case**: editorial, magazine layouts
- **Feel**: strong contrast; demands attention to hierarchy decisions
- **Notes**: same ratio governs ISO paper sizes (A4 to A5)

### Perfect Fifth — 1.500

- **Decimal**: 1.500
- **Musical**: perfect fifth (3:2)
- **Derivation**: 3/2 exactly
- **Use case**: display-heavy editorial; landing pages with hero typography
- **Feel**: bold, confident hierarchy
- **Warning**: at 5+ steps up, sizes get very large fast; clamp at viewport widths

### Golden Ratio — 1.618

- **Decimal**: 1.618
- **Musical**: just sharp of major sixth
- **Derivation**: φ = (1 + √5) / 2 ≈ 1.6180339...
- **Use case**: posters, hero displays, brand systems where typography IS the design
- **Feel**: dramatic; the largest step easily reaches poster sizes
- **Notes**: aesthetically idealized; mathematically self-similar across multiplications

## Choosing a ratio

| If your project is... | Recommended ratio |
|---|---|
| Admin dashboard, data-heavy | Major Second (1.125) or Minor Third (1.200) |
| Standard product (most cases) | **Minor Third (1.200)** |
| Marketing site, blog | Major Third (1.250) or Perfect Fourth (1.333) |
| Editorial publication | Augmented Fourth (1.414) or Perfect Fifth (1.500) |
| Hero-focused landing, poster | Golden Ratio (1.618) |

## Combining ratios across responsive breakpoints (v0.2, deferred)

In v0.2 of learn2kern, the responsive feature will let you use different
ratios at different viewport widths. Common pattern:

- Mobile: Minor Third (1.200) — denser hierarchy on small screens
- Desktop: Major Third (1.250) — more expressive on larger screens

Deferred until v0.2.

## Anti-patterns

| Pattern | Why it fails |
|---|---|
| Picking ratio by aesthetic gut feel without considering content density | Wrong ratio for the content type |
| Switching ratios mid-project | Existing components have already settled at the old scale; you'll fight every component |
| Picking Golden Ratio for a product UI | The largest step (display) will dwarf the content |
| Picking Minor Second for a marketing site | Hierarchy disappears at distance |
| Custom ratios for novelty | The eight canonical values cover every practical use case |

## Derivation cheat sheet

To compute step N from base B and ratio R:

```
step_N = B × R^N
```

Negative N for steps down (smaller than base):

```
step_-1 = B × R^-1 = B / R
step_-2 = B / R^2
```

All step sizes preserve the same ratio between adjacent steps. That
consistency is the entire point of a modular scale — every comparison
between two adjacent sizes feels the same.
