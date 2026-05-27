# infolog-terminal · Palette

Concrete values for the terminal-density aesthetic. Drafter copies the relevant blocks into the artifact's `:root` declaration. Token *names* are fixed by `output-style.md` § "Token baseline"; values below are this theme's overrides.

This theme is **dark only**. The mode switch is included but its Light + System buttons are hidden via CSS (see end of file).

## Type families

```css
:root {
  --sans:  "JetBrains Mono", ui-monospace, "SF Mono", Menlo, "Courier New", monospace;
  --mono:  "JetBrains Mono", ui-monospace, "SF Mono", Menlo, "Courier New", monospace;
  --serif: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, "Courier New", monospace;
}
```

All three resolve to the same monospace stack. The "everything is mono" rule.

## Type scale

Same perfect-5th heading scale as the composer baseline. Bloomberg's density comes from line-height, weight, and spacing — not from shrinking the type scale.

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
  --leading-snug:   1.25;
  --leading-normal: 1.4;   /* tighter than atomic for density */

  --tracking-tight:  0;
  --tracking-normal: 0.02em;
  --tracking-wide:   0.08em;

  --features-tabular:      "tnum" 1, "liga" 0;
  --features-no-ligatures: "liga" 0;
}
```

## Dark palette (the only palette)

```css
:root {
  --paper:      #0a0e0a;   /* near-black with green tint */
  --paper-soft: #14181a;

  --ink:      #4ade80;     /* bright green */
  --ink-soft: #22c55e;

  --accent-warm:  #fbbf24; /* amber — peak / highlight */
  --accent-cool:  #06b6d4; /* cyan — references, positive deltas */
  --accent-quiet: #166534; /* dim green — footnotes, dividers */

  --gray-100: #1f2937;
  --gray-300: #374151;
  --gray-500: #6b7280;
  --gray-700: #9ca3af;
  --gray-900: #e5e7eb;
}
```

No `[data-theme="dark"]` override needed — the `:root` palette IS the dark palette. The mode switch's Dark button is the active default.

## Spacing + structural

Tighter than infolog-io (divided by ~1.25) to maintain density.

```css
:root {
  --space-1: 3px;  --space-2: 6px;   --space-3: 10px;
  --space-4: 13px; --space-6: 19px;  --space-8: 26px; --space-12: 38px;

  --radius-panel: 0;                       /* sharp borders */
  --border: 1px solid var(--ink-soft);     /* bright green border */
}
```

## Mode switch override (dark-only theme)

```css
.theme-switch button[data-mode="light"],
.theme-switch button[data-mode="system"] {
  display: none;
}
```

Bloomberg-dense's `themespec.json` declares `"modes": ["dark"]`.

## Theme overrides on semantic callouts

Two overrides on the base callouts. Both fix issues surfaced in earlier review.

### `.metric` + `.unit` — fix the "131days" jankiness

Bloomberg-specific changes from the baseline:

```css
.metric {
  font-weight: var(--weight-medium); /* not bold — bold mono at 54px reads too heavy */
}
.unit {
  margin-left: var(--space-2);       /* breathing room between number and unit */
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
}
```

Also acceptable: wrap `.metric` + `.unit` in a flex container with `align-items: baseline; gap: var(--space-2);` to lock baseline alignment when the metric font is large.

### `.delta-up` — cyan, not warm

```css
.delta-up   { color: var(--accent-cool); }   /* cyan — positive change */
.delta-down { color: var(--accent-warm); }   /* amber — negative change */
```

(Inverts the atomic mapping, where warm is the accent for highlights and cool is references. Bloomberg's terminal convention puts positives in cyan, negatives in amber.)

## Palette rules

1. Everything is monospace. Period.
2. Borders are sharp (radius 0).
3. The dominant color is `var(--ink)` — bright green text on dark.
4. Amber highlights for the one mark per chart that matters (and for negative deltas — a terminal-error feel).
5. Cyan for reference lines / thresholds and positive deltas.
6. Dim green (`--accent-quiet`) is the only color allowed for dividers, footnotes, and footer text — pulls back from the bright `--ink`.
