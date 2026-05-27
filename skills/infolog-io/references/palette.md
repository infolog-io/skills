# infolog-io · Palette

Concrete values for the Tufte-quiet aesthetic. Drafter copies the relevant blocks into the artifact's `:root` declaration. Token *names* are fixed by `output-style.md` § "Token baseline"; values below are this theme's overrides.

## Type families

```css
:root {
  --sans:  "DM Sans", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --mono:  "JetBrains Mono", ui-monospace, "SF Mono", Menlo, "Courier New", monospace;
  --serif: ui-serif, Georgia, "Times New Roman", serif; /* optional; unused by headings */
}
```

Headings use `--sans` (DM Sans). `--serif` is retained for any element that wants editorial contrast, but the heading scale is sans throughout.

## Type scale

Perfect 5th heading scale + 16/14 body floor. See `output-style.md` § "Type scale" for the full rationale.

```css
:root {
  --font-size-h1: 5.063rem;   /* 81px */
  --font-size-h2: 3.375rem;   /* 54px */
  --font-size-h3: 2.25rem;    /* 36px */
  --font-size-h4: 1.5rem;     /* 24px */
  --font-size-h5: 1.125rem;   /* 18px */

  --font-size-body:    1rem;       /* 16px */
  --font-size-caption: 0.875rem;   /* 14px */
}
```

## Weights, leading, tracking

```css
:root {
  --weight-regular:  400;
  --weight-medium:   500;
  --weight-semibold: 600;
  --weight-bold:     700;

  --leading-tight:  1.15;
  --leading-snug:   1.3;
  --leading-normal: 1.5;

  --tracking-tight:  -0.02em;
  --tracking-normal: 0;
  --tracking-wide:   0.06em;

  --features-tabular:      "tnum" 1, "liga" 0;
  --features-no-ligatures: "liga" 0;
}
```

## Light mode palette (default)

```css
:root {
  /* surfaces */
  --paper:      #fafaf7;
  --paper-soft: #f3f1ea;

  /* ink */
  --ink:      #1a1a1a;
  --ink-soft: #555555;

  /* accents — 90/10 rule */
  --accent-warm:  #c8553d;   /* Okabe-Ito vermillion, adapted */
  --accent-cool:  #2c5e6f;
  --accent-quiet: #888888;

  /* gray ramp */
  --gray-100: #f0eee6;
  --gray-300: #d1cfc5;
  --gray-500: #87867f;
  --gray-700: #3d3d3a;
  --gray-900: #141413;
}
```

## Dark mode palette (mode switch + system preference)

```css
[data-theme="dark"] {
  --paper:      #161413;
  --paper-soft: #1f1c1a;

  --ink:      #f5f1e9;
  --ink-soft: #a8a39b;

  --accent-warm:  #d97757;   /* lighter vermillion for dark bg legibility */
  --accent-cool:  #5fa3b7;
  --accent-quiet: #6b6b6b;

  --gray-100: #2a2724;
  --gray-300: #3d3a35;
  --gray-500: #6d6a64;
  --gray-700: #adaaa3;
  --gray-900: #e8e3d8;
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --paper:      #161413;
    --paper-soft: #1f1c1a;
    --ink:        #f5f1e9;
    --ink-soft:   #a8a39b;
    --accent-warm:  #d97757;
    --accent-cool:  #5fa3b7;
    --accent-quiet: #6b6b6b;
    --gray-100: #2a2724;
    --gray-300: #3d3a35;
    --gray-500: #6d6a64;
    --gray-700: #adaaa3;
    --gray-900: #e8e3d8;
  }
}
```

The `:not([data-theme="light"])` guard lets the user-pressed Light button beat the OS preference.

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
3. Reference lines + thresholds use `var(--accent-cool)` at lower opacity (0.6) or a dashed stroke.
4. The page background is `var(--paper)` — never pure white in light, never pure black in dark.
5. Borders default to `var(--border)` — always token-referenced.
6. Dark mode inverts paper/ink but does NOT invert accent values — adapted lighter accents preserve perceived weight against the darker surface.

## Monochrome survival

The palette survives grayscale conversion because all encoding uses position, size, and shape — never hue alone. The accent is salience-only, not data-encoding. Both light and dark palettes maintain this property.
