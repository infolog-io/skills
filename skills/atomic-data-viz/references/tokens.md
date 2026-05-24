# atomic-data-viz · Token schema

This theme requires the following CSS custom properties on `:root`. The
composer's `token_compliance` check verifies every styled property in the
artifact resolves to one of these via `var(--...)`.

## Surface

| Variable | Role |
|---|---|
| `--paper` | Primary background — pages, panels |
| `--paper-soft` | Secondary surface — alternate row, callout box |

## Ink

| Variable | Role |
|---|---|
| `--ink` | Primary text + data marks |
| `--ink-soft` | Annotation, secondary text, axis labels |

## Accents

Used sparingly. The 90/10 rule: 90% gray, 10% accent.

| Variable | Role |
|---|---|
| `--accent-warm` | The single highlighted mark (one per chart) |
| `--accent-cool` | Reference line, regression, threshold annotation |
| `--accent-quiet` | Footnote, deemphasized callout |

## Gray ramp

Five stops for hierarchy. Most chart elements use these.

| Variable | Use |
|---|---|
| `--gray-100` | Backgrounds, page-soft fills |
| `--gray-300` | Borders, grid lines, deemphasized strokes |
| `--gray-500` | Mid-emphasis text, axis labels |
| `--gray-700` | Body text |
| `--gray-900` | Headings, primary marks |

## Type

| Variable | Role |
|---|---|
| `--serif` | Headings (h1, h2, large numerics in stat cards) |
| `--sans` | Body, axis labels, annotations |
| `--mono` | Tabular numerics, code, identifiers |
| `--font-size-h1` | Page title |
| `--font-size-h2` | Section heading |
| `--font-size-body` | Default text |
| `--font-size-caption` | Annotation, footer |

## Spacing scale

Multiples of 4px. Use these — never raw px values.

| Variable | Pixels |
|---|---|
| `--space-1` | 4 |
| `--space-2` | 8 |
| `--space-3` | 12 |
| `--space-4` | 16 |
| `--space-6` | 24 |
| `--space-8` | 32 |
| `--space-12` | 48 |

## Structural

| Variable | Role |
|---|---|
| `--radius-panel` | Card / panel border radius |
| `--border` | Default thin border for panels and tables |
