# Failover Chain

Brand tokens are the foundation. If no `tokens.css` exists, the audit
must still produce a meaningful result. The failover chain defines three
sources of truth, tried in order, each with a confidence rating.

## The three steps

```
1. Explicit tokens         (confidence: high)
        ↓ (if missing)
2. Parse brand image       (confidence: medium)
        ↓ (if missing)
3. Scrape live URL         (confidence: low)
        ↓ (if all fail)
   Verdict: broken; build-out plan starts with "define tokens"
```

## Step 1 — Explicit tokens

Confidence: **high**.

Look for any of:

| Pattern | Format |
|---|---|
| `tokens.css`, `tokens.scss`, `vars.css` | CSS custom properties |
| `tailwind.config.{js,ts}` | Tailwind theme extension |
| `theme.ts`, `theme.js`, `tokens.ts` | CSS-in-JS / TypeScript constants |
| `tokens.json` | W3C Design Tokens |
| `*.css-module` files declaring custom properties | inline tokens |
| `design-tokens.yaml` | YAML token files |
| Style Dictionary outputs | various formats |

Walk the project directory tree (depth 4). If any of these files exist
AND contain at least 3 color tokens, 3 spacing tokens, and 1 type token,
treat the project as having explicit tokens.

Audit uses these tokens as the comparison set. Compliance is measured
strictly.

### What to do with explicit tokens

1. Parse the file(s) into a token map: `{ color: {...}, spacing: {...}, type: {...}, ... }`
2. For each component file, identify literal values and match them against the token map
3. Each match is a token-compliant usage; each unmatched literal is a `token_violation`

## Step 2 — Parse brand image

Confidence: **medium**.

Trigger: step 1 found no token file, but the user provides a brand asset.

Accepted assets:
- Logo (SVG or high-res PNG)
- Style guide PDF
- Screenshot of a polished page
- Brand book image
- Color palette swatch image

Extract:
- Dominant colors (top 3-5 by area-weighted prominence)
- Typeface families (from rendered text if visible)
- Approximate spacing rhythm (if a layout is visible)

Tag every extracted value as `inferred:image`. Audit confidence drops to
`low` automatically because the inference may misrepresent intent.

Emit a `proposed-tokens.css` containing the inferred tokens with
comments explaining their derivation. Recommend the user review and
formalize.

### Limitations

- Color extraction may capture incidental colors (one accent badge) and
  miss core palette
- Type family detection requires the asset to contain rendered text in
  the brand typeface
- Spacing inference is unreliable from a single image

This path produces a working start, not a finished system.

## Step 3 — Scrape live URL

Confidence: **low**.

Trigger: steps 1 and 2 both unavailable; only a live URL is provided.

Procedure:

1. Render the URL (use a headless browser, screenshot service, or HTTP
   fetch + CSS parsing)
2. Sample computed styles from a diverse set of elements:
   - Body text
   - Headings (h1-h6)
   - Links
   - Buttons (`button`, `[role=button]`)
   - Inputs
   - Borders and dividers
   - Major background regions
3. Cluster values: colors by similarity, spacings by proximity, type by family
4. Identify the dominant patterns

Tag every extracted value as `inferred:url`. Confidence is `low` because
rendered styles include third-party widgets, analytics overlays, and
user-agent defaults that are not part of the intended brand.

### When scraping is required

- The codebase is closed-source but the live site is public
- The audit is being performed before code access is granted
- The user wants a competitive teardown (auditing a competitor's brand
  coherence from their site)

### What to filter out

- Browser default styles (button user-agent styling, link underline color)
- Third-party iframe content (analytics, chat widgets, ad slots)
- A/B test variants if multiple loads show different styles

Audit output flags filtered cases so the user knows what was excluded.

## When all three fail

If the user provides:
- No token file
- No brand image
- No URL

Verdict is automatically `broken`. The build-out plan starts with:

```
1. Establish brand tokens before code can audit reliably.
   - Define `tokens.css` with the minimum token set:
     - 3-5 color tokens (primary, neutral, semantic at minimum)
     - 6-10 spacing tokens (geometric or modular scale)
     - 3-5 type tokens (sizes; family; weight)
   - Bootstrap with learn2kern for the type scale.
   - Document the token decisions in a tokens-decisions.md.
```

## Confidence implications

| Source | Compliance enforcement | Verdict caveat |
|---|---|---|
| Explicit | Strict — every literal counted | Verdict reflects true state |
| Image | Lenient — inferred palette may miss intent | Verdict cannot exceed `drifting` without confirmation |
| URL | Lenient — computed styles include third-party noise | Verdict cannot exceed `drifting` without confirmation |
| None | N/A | Verdict is `broken` |

## When to upgrade from image or URL to explicit

The audit always recommends: when failover step 2 or 3 is used, the
output includes a "promote to explicit tokens" task with the inferred
values written into a `proposed-tokens.css`. The user reviews and
commits, then re-runs the audit.

This upgrade is the highest-leverage next step for any project below
step 1.

## Worked sequence

1. User runs `atomic audit` on a project
2. Skill walks the tree for token files
3. Finds `tailwind.config.ts` with theme extension → step 1 succeeds; confidence = high
4. Skill parses Tailwind config into token map
5. Skill walks component files and counts token references vs. literals
6. Skill emits audit with score and tagged findings
7. If verdict is `drifting`, refactor plan groups literals by category

Or, in a failover case:

1. User runs `atomic audit` on a legacy project with no tokens
2. Skill finds no token file → step 1 fails
3. Skill asks: "Do you have a brand asset (image or PDF) I can analyze?"
4. User provides logo + style guide PDF
5. Skill extracts colors and type families → step 2 succeeds; confidence = medium
6. Skill emits inferred token map + `proposed-tokens.css`
7. Verdict capped at `drifting`; user must formalize tokens before re-audit can verdict `system-healthy`
