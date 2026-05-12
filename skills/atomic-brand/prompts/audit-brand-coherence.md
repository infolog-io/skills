# Prompt — Audit brand coherence

**Purpose:** Score brand-coherence and scale-discipline dimensions. Identify
visual outliers, off-palette colors, off-scale spacing, type drift, and
shape inconsistencies.

## Input contract

- A parsed token map (or inferred values from image/URL fallback)
- A list of component files OR a set of rendered screenshots OR a live URL
- Optional: brand-coherence overrides documented in `tokens-exceptions.md`

## Output contract

```json
{
  "brand_coherence": { "score": 1-5, "reason": "..." },
  "scale_discipline": { "score": 1-5, "reason": "..." },
  "findings": [ ... ]
}
```

## Procedure

### 1. Identify the brand's value sets

From the token map (or inferred fallback):

- **Color palette**: brand + neutral + semantic + interactive sets
- **Type set**: declared font families (sans, mono, display)
- **Border radius style**: discrete values declared (e.g., sm/md/lg/full) or none
- **Shadow style**: declared elevations or flat (no shadows)
- **Spacing scale**: declared step values

### 2. Walk and compare

For each component file or rendered surface:

#### Color check

- Extract every color literal or token reference
- Compare against the palette
- Flag colors NOT in the palette as `brand_drift`
- Flag colors that are close-but-not-equal to palette colors as `inconsistency`

#### Type check

- Extract every font-family declaration
- Compare against the brand type set
- Flag any family not in the set as `brand_drift`

#### Radius check

- Extract every border-radius declaration
- Compare against declared radius tokens
- Flag radii that violate the brand's overall style (rounded brand using sharp corners on one component, etc.) as `brand_drift`

#### Shadow check

- Extract every box-shadow declaration
- Compare against declared elevation tokens
- Flag custom shadows that don't match any elevation as `brand_drift`

#### Scale check (spacing, type, etc.)

- For every literal that should be on a scale, check against the scale values
- Flag values that are close but off (`13px` when scale is `12px` or `16px`) as `scale_violation`

### 3. Score dimensions

#### Brand coherence

| State | Score |
|---|---|
| Single coherent identity; every element matches the brand value sets | 5 |
| One or two outliers; intentional or documented | 4 |
| Multiple outliers; some unintentional | 3 |
| Many outliers; competing identities present | 2 |
| No coherent identity discernible | 1 |

#### Scale discipline

| State | Score |
|---|---|
| Every value on the defined scales | 5 |
| 1-2 outliers per category, clearly intentional | 4 |
| Several outliers; mixing scale steps and arbitrary values | 3 |
| Many values appear arbitrary | 2 |
| No discernible scale | 1 |

### 4. Emit findings

For each flagged element:

```
- tag: brand_drift | scale_violation | inconsistency
- file: <path>
- line: <number>
- found: <verbatim value>
- expected: <brand-compliant value or scale step>
- confidence: high | medium | low
```

## Worked example

### Input

Brand color palette:
- `--color-primary: #FF6600`
- `--color-secondary: #2233CC`
- Neutrals: `#000000`, `#333333`, `#666666`, `#999999`, `#CCCCCC`, `#FFFFFF`
- Semantic: success `#00AA66`, warning `#FFAA00`, danger `#CC0000`

Spacing scale: `4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px`

Component:
```css
.cta-banner {
  background: linear-gradient(135deg, #FF7711, #FF6600);  /* off-palette accent */
  padding: 17px 13px;                                       /* off-scale */
  color: white;
  border-radius: 8px;                                       /* not on declared scale of 4, 6, 12 */
  box-shadow: 0 4px 18px rgba(255, 102, 0, 0.3);            /* custom shadow */
}
```

### Output

```json
{
  "brand_coherence": {
    "score": 3,
    "reason": "CTA banner uses gradient with off-palette intermediate color and custom shadow not in elevation set"
  },
  "scale_discipline": {
    "score": 2,
    "reason": "Spacing 17px and 13px are off-scale; border-radius 8px is between declared steps"
  },
  "findings": [
    {
      "tag": "brand_drift",
      "file": "src/components/organisms/cta-banner.css",
      "line": 2,
      "found": "linear-gradient(135deg, #FF7711, #FF6600)",
      "expected": "Either use --color-primary solid or define a brand-gradient token; #FF7711 is not in the palette",
      "confidence": "high"
    },
    {
      "tag": "scale_violation",
      "file": "src/components/organisms/cta-banner.css",
      "line": 3,
      "found": "padding: 17px 13px",
      "expected": "padding: var(--space-3) var(--space-3) (16px 12px) — nearest scale steps",
      "confidence": "high"
    },
    {
      "tag": "scale_violation",
      "file": "src/components/organisms/cta-banner.css",
      "line": 5,
      "found": "border-radius: 8px",
      "expected": "Round to --radius-md (6px) or --radius-lg (12px); or add 8px to scale if intentional",
      "confidence": "medium"
    },
    {
      "tag": "brand_drift",
      "file": "src/components/organisms/cta-banner.css",
      "line": 6,
      "found": "box-shadow: 0 4px 18px rgba(255, 102, 0, 0.3)",
      "expected": "Use --shadow-md or define a colored elevation token; this custom shadow is undocumented",
      "confidence": "medium"
    }
  ]
}
```

## Edge cases

| Pattern | Handling |
|---|---|
| Brand requires intentional asymmetry (`13px` is a brand signature) | Document in `tokens-exceptions.md`; skip violation |
| Marketing illustration with custom colors | Out of scope; not a system component |
| Third-party widget with its own visual identity | Note as exception; do not refactor the third party |
| Dark mode tokens that look like off-palette | Verify it's a paired token (`--color-text-dark`); not a violation |
| Generated swatch chart that needs many distinct colors | Use a categorical palette token (Okabe-Ito) rather than ad-hoc colors |

## Visual fallback when only screenshots are available

When auditing from screenshots rather than code:

1. Sample colors from rendered pixels (use color quantization)
2. Compare against the brand palette with a tolerance (within ΔE 5 is "close enough")
3. Identify clusters of similar colors that should be one
4. Flag the rendered surface, not specific files

Confidence drops to `medium` or `low` because rendered pixels include
anti-aliasing, gradient interpolation, and image content that aren't
brand decisions.

## Verification before returning output

- Every flagged element cites the brand value it violated
- Score follows the rubric
- Exceptions consulted if available
- Findings are actionable (the user can see the fix from the output)
