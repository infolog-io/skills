# bloomberg-dense · Palette

```css
:root {
  --paper: #0a0e0a;          /* near-black with green tint */
  --paper-soft: #14181a;

  --ink: #4ade80;            /* bright green */
  --ink-soft: #22c55e;

  --accent-warm: #fbbf24;    /* amber for highlights */
  --accent-cool: #06b6d4;    /* cyan for references */
  --accent-quiet: #166534;   /* dim green for footnotes */

  --gray-100: #1f2937;
  --gray-300: #374151;
  --gray-500: #6b7280;
  --gray-700: #9ca3af;
  --gray-900: #e5e7eb;

  --serif: ui-monospace, "SF Mono", Menlo, monospace;
  --sans: ui-monospace, "SF Mono", Menlo, monospace;
  --mono: ui-monospace, "SF Mono", Menlo, monospace;

  --font-size-h1: 1.2rem;
  --font-size-h2: 0.95rem;
  --font-size-body: 0.78rem;
  --font-size-caption: 0.68rem;

  --space-1: 3px; --space-2: 6px;  --space-3: 10px;
  --space-4: 13px; --space-6: 19px; --space-8: 26px; --space-12: 38px;

  --radius-panel: 0;
  --border: 1px solid var(--ink-soft);
}
```

## Palette rules

1. Everything is monospace. Period.
2. Borders are sharp (radius 0).
3. The dominant color is `var(--ink)` — bright green text on dark.
4. Amber highlights for the one mark per chart that matters.
5. Cyan only for reference lines / thresholds.
