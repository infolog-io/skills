# Prompt — Scrape live URL for brand (failover step 3)

**Purpose:** When no token file or image asset is available, extract
brand values from a rendered live URL. Output is tagged `inferred:url`
and confidence drops to `low`.

## Input contract

- A fully-qualified URL of a live website
- Optional: a list of specific pages to sample (defaults to home page + 2 secondary pages)
- Optional: authentication credentials if the site requires login

## Output contract

A `proposed-tokens.css` and an inference report, similar to
`parse-image-for-brand.md` but tagged `url-scraped`.

```json
{
  "source": "url-scraped",
  "url": "https://example.com",
  "confidence": "low",
  "pages_sampled": ["...", "...", "..."],
  "extracted": {
    "colors": [ ... ],
    "type_families": [ ... ],
    "spacing_rhythm": [ ... ],
    "radius_observed": null,
    "shadow_observed": null
  },
  "third_party_filtered": ["..."],
  "recommendations": [ ... ]
}
```

## Procedure

### 1. Fetch and render the URL

Render with a headless browser (the implementation lives in a future
`tools/` script). Capture:

- HTML structure
- All CSS rules (inline, embedded, external)
- Computed styles for a representative set of elements
- Screenshots for visual comparison

### 2. Sample diverse elements

For each sampled page, query:

| Selector | What to extract |
|---|---|
| `body` | Background color, base text color, base font family |
| `h1`, `h2`, `h3` | Font family, size, weight, color |
| `a`, `a:visited`, `a:hover` | Link colors |
| `button`, `[role=button]`, `[type=submit]` | Primary button styles |
| `input`, `textarea`, `select` | Form element styles |
| `[class*="card" i]` | Card-like patterns |
| `header` | Brand surface treatment |
| `footer` | Secondary brand surface |
| Major background regions | Background palette |

### 3. Cluster computed values

For each property:

1. Collect every observed value
2. Cluster by similarity:
   - Colors: by perceptual distance (ΔE 5 tolerance)
   - Spacing: by proximity (within 2px tolerance)
   - Type sizes: by exact match
3. Identify dominant patterns
4. Discard incidental one-off values

### 4. Filter third-party noise

Computed styles include values from:

- Browser user-agent stylesheets (button defaults, link underlines)
- Third-party iframes (analytics, chat widgets, ad slots)
- A/B test variants
- User customizations (browser zoom, accessibility overrides)

Filter these out by:

- Excluding elements inside `<iframe>` tags
- Excluding elements with class names containing third-party prefixes (`fb-`, `twitter-`, `intercom-`, `drift-`)
- Sampling multiple page loads to detect A/B variants

Document filtered cases in the report.

### 5. Emit proposed tokens

Generate a `proposed-tokens.css` from the most dominant patterns:

```css
/* Proposed tokens — scraped from https://example.com
 * Source: url-scraped
 * Confidence: low
 * Review carefully before committing — computed styles include
 * browser defaults and third-party widget styles.
 */

:root {
  /* Color (most common observed values) */
  --color-primary: #FF6600;     /* button background, link hover; confidence: medium */
  --color-text: #1A1A1A;        /* body text; confidence: high */
  --color-text-muted: #666666;  /* secondary text; confidence: medium */
  --color-bg: #FFFFFF;          /* body background; confidence: high */
  --color-link: #0066CC;        /* link color; confidence: high */

  /* Type */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-size-body: 16px;
  --font-size-h1: 48px;          /* scraped; may not be on a clean scale */

  /* Spacing — extracted by clustering observed margins/paddings */
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;

  /* Radius */
  --radius-md: 6px;              /* most common border-radius */
}
```

### 6. Emit inference report

```json
{
  "source": "url-scraped",
  "url": "https://example.com",
  "confidence": "low",
  "pages_sampled": ["/", "/products", "/about"],
  "extracted": {
    "colors": [
      { "hex": "#FF6600", "role_guess": "primary", "evidence": "8 buttons, 3 links", "confidence": "medium" },
      { "hex": "#1A1A1A", "role_guess": "text", "evidence": "body element, all paragraphs", "confidence": "high" }
    ],
    "type_families": [
      { "name": "Inter", "evidence": "body, all headings", "confidence": "high" }
    ],
    "spacing_rhythm": [
      { "value": "16px", "occurrences": 24, "confidence": "high" },
      { "value": "24px", "occurrences": 18, "confidence": "high" }
    ]
  },
  "third_party_filtered": [
    "Intercom chat widget styles",
    "Google Analytics script (no styles)",
    "Facebook Pixel iframe"
  ],
  "recommendations": [
    "Confidence is low — confirm extracted colors against design files",
    "Type scale from scraping is not modular; recommend learn2kern to regenerate",
    "Validate spacing scale by checking design files; scraped values may include legacy CSS"
  ]
}
```

## Limitations

This path produces a starting point only. Limitations:

- Cannot distinguish intentional design from legacy CSS
- Captures third-party widget styles unless carefully filtered
- Browser defaults leak into samples
- A/B variants may differ across loads
- Audit confidence cannot exceed `low`
- Verdict cannot exceed `drifting`

## Stub status

The actual rendering and CSS extraction requires a `tools/` script
(Playwright, Puppeteer, or browser MCP). v0.1.0 specifies the contract;
implementation deferred to v0.2 unless an existing browser-automation
skill can be composed.

## Composition with other skills

For implementation, atomic-brand can call out to the `agent-browser`
standalone skill (already in `~/.claude/skills/`) which provides
browser automation. The contract here describes what the orchestrator
needs from that automation.

## Verification before returning output

- Every extracted value is tagged with confidence
- Third-party filtering is documented
- Pages sampled are explicit
- Recommendations are concrete
- Source `url-scraped` is recorded on every token
