# Prompt — Parse image for brand (failover step 2)

**Purpose:** When no explicit token file exists, infer brand values from a
brand asset image. Output is a proposed token set with all values tagged
`inferred:image` and confidence dropped to `medium` (or `low`).

## Input contract

- A path to or URL of an image asset
- Accepted: logo (SVG or PNG), style guide PDF, screenshot of a polished
  page, brand book image, color palette swatch

## Output contract

A `proposed-tokens.css` (or equivalent) plus an inference report:

```json
{
  "source": "image-parsed",
  "asset_path": "...",
  "confidence": "medium" | "low",
  "extracted": {
    "colors": [
      { "hex": "#FF6600", "role_guess": "primary", "evidence": "dominant fill in logo", "confidence": "medium" },
      ...
    ],
    "type_families": [
      { "name": "Inter", "weight_observed": [400, 600], "confidence": "high" },
      ...
    ],
    "spacing_rhythm": [],
    "radius_observed": null
  },
  "recommendations": [
    "Review --color-primary inference; PNG sampling may include anti-aliasing",
    "Add neutral palette manually — image rarely surfaces all neutrals"
  ]
}
```

## Procedure

### 1. Color extraction

For an image:

1. Quantize the image to a manageable palette (16-64 colors)
2. Sort by area-weighted prominence
3. Filter out:
   - Pure white and pure black backgrounds (unless intentional)
   - Anti-aliasing artifacts (very low-prominence intermediate hues)
   - Skin tones if the image is a photograph (likely incidental)
4. Pick the top 3-7 prominent colors
5. Guess roles:
   - Most prominent saturated color → primary
   - Second most prominent saturated color → secondary
   - Greens → success
   - Reds → danger
   - Yellows/oranges → warning
   - Blues that aren't already used → info

Confidence per color:
- High if the color appears in clearly intentional regions (logo, button)
- Medium if extracted from a screenshot or marketing piece
- Low if extracted from a photograph or single instance

### 2. Type extraction

If the image contains rendered text:

1. Use OCR or visual font matching to identify the typeface
2. Note observed weights (regular, medium, bold) by stroke thickness
3. Note observed sizes by relative scale

If no text in the image, return no type inference and request additional
assets (a PDF, a website, etc.).

### 3. Spacing rhythm (limited)

Spacing is hard to extract from a single image. Skip unless the image
shows a recurring layout with measurable margins. If extracted, flag
confidence as low and recommend overriding with a learn2kern modular
scale.

### 4. Radius observation

If the image shows UI elements (buttons, cards):

- Note whether corners are sharp (≤2px), softly rounded (4-12px), or fully rounded (pill/circle)
- Use this to seed the radius style preference (`sharp`, `rounded`, `pill`)
- Do not infer specific radius values without measurement

### 5. Emit proposed tokens

Generate a `proposed-tokens.css`:

```css
/* Proposed tokens — inferred from <asset>
 * Source: image-parsed
 * Confidence: medium
 * Review and adjust before committing.
 */

:root {
  /* Color (inferred from logo + screenshot) */
  --color-primary: #FF6600;       /* dominant fill, confidence: medium */
  --color-secondary: #2233CC;     /* secondary fill, confidence: medium */
  --color-success: #00AA66;       /* greens observed, confidence: low — confirm */

  /* Neutrals — NOT extracted from image; using sensible defaults */
  --color-text: #1A1A1A;
  --color-text-muted: #666666;
  --color-bg: #FFFFFF;
  --color-bg-elevated: #FAFAFA;
  --color-border: #E5E5E5;

  /* Type (inferred from rendered text) */
  --font-sans: 'Inter', sans-serif;          /* confidence: medium */
  --font-display: 'Inter', sans-serif;       /* assume same — confirm */

  /* Type scale — NOT extracted; recommend learn2kern to generate */
  /* --font-size-* tokens deferred */

  /* Spacing — NOT extracted; using a default modular scale */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;

  /* Radius (style hint only) */
  /* Observed style: rounded — recommend --radius-sm 4px, --radius-md 8px, --radius-lg 12px */
}
```

### 6. Emit inference report

Document the reasoning for each inference. The user reviews and either:
1. Commits the proposed tokens as-is
2. Adjusts and commits
3. Rejects and provides explicit tokens

## Worked example

### Input

A logo SVG: a sunburst with two prominent oranges (#FF6600, #FF8833) on a
white background.

### Output

```css
/* Proposed tokens — inferred from sunburst-logo.svg
 * Source: image-parsed
 * Confidence: medium
 * Review and adjust before committing.
 */

:root {
  /* Color */
  --color-primary: #FF6600;        /* dominant orange */
  --color-primary-light: #FF8833;  /* lighter orange, observed in gradient */
  --color-bg: #FFFFFF;             /* logo background */

  /* All other tokens deferred — single asset is insufficient */
}
```

```json
{
  "source": "image-parsed",
  "asset_path": "sunburst-logo.svg",
  "confidence": "medium",
  "extracted": {
    "colors": [
      { "hex": "#FF6600", "role_guess": "primary", "evidence": "dominant fill area (62%)", "confidence": "high" },
      { "hex": "#FF8833", "role_guess": "primary-light", "evidence": "secondary fill (28%)", "confidence": "medium" }
    ],
    "type_families": [],
    "spacing_rhythm": [],
    "radius_observed": null
  },
  "recommendations": [
    "Single-asset extraction provides only the brand color. Provide a style guide PDF or screenshot for type, spacing, radius, and neutrals.",
    "Confirm --color-primary-light is intentional (it may be a gradient artifact rather than a discrete token).",
    "Run learn2kern to generate the type scale once the typeface is confirmed."
  ]
}
```

## Limitations to communicate

The audit must clearly state:

- Image inference is a starting point, not a finished system
- Confidence is medium at best; never high
- The user must review and formalize before re-running the audit at full confidence
- Verdict from image-inferred tokens cannot exceed `drifting`

## Stub status

This prompt currently specifies the contract. The image-parsing
implementation (color quantization, OCR, etc.) requires a `tools/` script
in a future version. v0.1.0 of atomic-brand documents the contract and
calls out the need for explicit tokens.

## Verification before returning output

- Every extracted value is tagged with confidence
- Defaults are clearly marked as defaults, not extracted
- The proposed-tokens.css is reviewable as a draft
- Recommendations are concrete
