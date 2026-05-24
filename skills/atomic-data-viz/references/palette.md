# atomic-data-viz · Palette

Concrete values for the Tufte-quiet aesthetic. Drafter copies this into
the artifact's `:root` declaration.

## Color values

```css
:root {
  /* surfaces */
  --paper: #fafaf7;
  --paper-soft: #f3f1ea;

  /* ink */
  --ink: #1a1a1a;
  --ink-soft: #555555;

  /* accents — 90/10 rule */
  --accent-warm: #c8553d;   /* Okabe-Ito vermillion, adapted */
  --accent-cool: #2c5e6f;
  --accent-quiet: #888888;

  /* gray ramp */
  --gray-100: #f0eee6;
  --gray-300: #d1cfc5;
  --gray-500: #87867f;
  --gray-700: #3d3d3a;
  --gray-900: #141413;
}
```

## Type values

```css
:root {
  --serif: ui-serif, Georgia, "Times New Roman", serif;
  --sans:  system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --mono:  ui-monospace, "SF Mono", Menlo, "Courier New", monospace;

  --font-size-h1: 1.6rem;
  --font-size-h2: 1.05rem;
  --font-size-body: 0.92rem;
  --font-size-caption: 0.78rem;
}
```

## Spacing + structural

```css
:root {
  --space-1: 4px;  --space-2: 8px;   --space-3: 12px;
  --space-4: 16px; --space-6: 24px;  --space-8: 32px; --space-12: 48px;

  --radius-panel: 10px;
  --border: 1px solid var(--gray-300);
}
```

## Palette rules

1. Most marks default to `var(--ink)` or `var(--gray-700)`.
2. At most one mark per chart uses `var(--accent-warm)`.
3. Reference lines + thresholds use `var(--accent-cool)` at lower
   opacity (0.6) or a dashed stroke.
4. The page background is `var(--paper)` — never pure white.
5. Borders default to `var(--border)` — always token-referenced.

## Monochrome survival

The palette survives grayscale conversion because all encoding uses
position, size, and shape — never hue alone. The accent is salience-only,
not data-encoding.
