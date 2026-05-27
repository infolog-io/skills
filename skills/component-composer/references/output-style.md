# Output Style — Single-File HTML

The drafter's output is one self-contained `.html` file. No build step. No npm dependencies. No external requests. The artifact must open correctly when the user double-clicks it on any modern browser, online or offline.

Style anchor: `ThariqS/html-effectiveness` — a gallery of single-file HTML examples demonstrating how much fidelity a static file can carry.

## Required structure

1. `<!DOCTYPE html>` + `<html lang="en">` + `<meta charset>` + viewport meta.
2. Inline `<style>` in `<head>`. **All** styling lives here.
3. CSS custom properties declared on `:root`. Every color, type size, spacing, weight, leading, and radius is a `var(--...)` reference. No literal hex codes or px values outside the `:root` block (and outside the `[data-theme="dark"]` mode block).
4. The body uses semantic HTML — `<header>`, `<section>`, `<table>`, `<figure>` — not generic `<div>` soup.
5. HTML headings use `<h1>` through `<h5>` directly, not custom heading classes.
6. Inline `<svg>` for every chart. No `<img>` for chart content.
7. Vanilla `<script>` only when interaction is real (theme switch, tooltips, filtering). No external libraries. No `import` statements.

## Token baseline

These tokens are declared on `:root` in every artifact. Themes override the *values*; the *names* are fixed.

### Type families

```css
--sans:  "DM Sans", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
--mono:  "JetBrains Mono", ui-monospace, "SF Mono", Menlo, "Courier New", monospace;
--serif: ui-serif, Georgia, "Times New Roman", serif;
```

Named fonts render on machines that have them installed; everyone else gets the system fallback. The artifact does NOT load these fonts over the network — see § "Forbidden in artifact". This preserves single-file portability.

### Type scale — headings (perfect 5th, h5 floored at 18px)

```css
--font-size-h1: 5.063rem;   /* 81px */
--font-size-h2: 3.375rem;   /* 54px */
--font-size-h3: 2.25rem;    /* 36px */
--font-size-h4: 1.5rem;     /* 24px */
--font-size-h5: 1.125rem;   /* 18px */
```

### Type scale — body

```css
--font-size-body:    1rem;       /* 16px */
--font-size-caption: 0.875rem;   /* 14px */
```

### Weights

```css
--weight-regular:  400;
--weight-medium:   500;
--weight-semibold: 600;
--weight-bold:     700;
```

### Leading

```css
--leading-tight:  1.15;   /* large headings */
--leading-snug:   1.3;    /* mid-size headings */
--leading-normal: 1.5;    /* body — theme may tighten to 1.4 for dense aesthetics */
```

### Tracking

```css
--tracking-tight:  -0.02em;   /* large display headings */
--tracking-normal: 0;
--tracking-wide:   0.06em;    /* uppercase labels, captions */
```

### Font features

```css
--features-tabular:      "tnum" 1, "liga" 0;   /* numerics + disabled ligatures */
--features-no-ligatures: "liga" 0;             /* for code/mono outside actual code blocks */
```

### Surface + ink (theme-defined values)

```css
--paper, --paper-soft        /* surfaces */
--ink, --ink-soft            /* primary + secondary text */
--accent-warm, --accent-cool, --accent-quiet
--gray-100 through --gray-900
```

### Spacing scale

```css
--space-1: 4px;  --space-2: 8px;   --space-3: 12px;
--space-4: 16px; --space-6: 24px;  --space-8: 32px; --space-12: 48px;
```

Themes may tighten by a constant factor (infolog-terminal uses /1.25). Names are fixed.

### Structural

```css
--radius-panel: 6px;  /* themes set their own; 0 for sharp aesthetics */
--border: 1px solid var(--gray-300);
```

### Column grid

```css
--grid-cols: 4;
--grid-gutter: var(--space-3);
--grid-margin: var(--space-4);
--grid-max-width: 1280px;

@media (min-width: 641px)  { :root { --grid-cols: 8;  --grid-gutter: var(--space-4); --grid-margin: var(--space-8); } }
@media (min-width: 1024px) { :root { --grid-cols: 12; --grid-gutter: var(--space-6); --grid-margin: var(--space-12); } }
```

Breakpoints: 641px (mobile→tablet), 1024px (tablet→desktop). Match the validator's mobile (375), tablet (768), desktop (1280) viewports.

## Required CSS base

Every artifact includes the following in its `<style>` block, in addition to theme-specific styles. The drafter may not rename utilities, change span semantics, or drop the switch component.

```css
* { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: var(--sans);
  font-size: var(--font-size-body);
  line-height: var(--leading-normal);
}

/* Heading scale — all sans, weight cascade */
h1, h2, h3, h4, h5 {
  font-family: var(--sans);
  margin: 0;
  color: var(--ink);
}
h1 { font-size: var(--font-size-h1); font-weight: var(--weight-bold);     line-height: var(--leading-tight); letter-spacing: var(--tracking-tight); text-wrap: balance; }
h2 { font-size: var(--font-size-h2); font-weight: var(--weight-semibold); line-height: var(--leading-tight); letter-spacing: var(--tracking-tight); text-wrap: balance; }
h3 { font-size: var(--font-size-h3); font-weight: var(--weight-semibold); line-height: var(--leading-snug);                                       text-wrap: balance; }
h4 { font-size: var(--font-size-h4); font-weight: var(--weight-medium);   line-height: var(--leading-snug);                                       text-wrap: balance; }
h5 { font-size: var(--font-size-h5); font-weight: var(--weight-medium);   line-height: var(--leading-snug);  color: var(--ink-soft); }

/* Body text */
p     { margin: 0; max-width: 66ch; text-wrap: pretty; }
small { font-family: var(--sans); font-size: var(--font-size-caption); color: var(--ink-soft); text-wrap: balance; }

/* Semantic callouts */
code  { font-family: var(--mono); font-size: 0.92em; background: var(--paper-soft); padding: 0 var(--space-1); border-radius: 3px; font-feature-settings: var(--features-no-ligatures); }
pre   { margin: 0; padding: var(--space-3) var(--space-4); background: var(--paper-soft); border-radius: var(--radius-panel); overflow-x: auto; line-height: var(--leading-snug); }
pre code { background: none; padding: 0; font-size: var(--font-size-caption); }
kbd   { font-family: var(--mono); font-size: 0.85em; padding: 2px 6px; border: var(--border); border-bottom-width: 2px; border-radius: 4px; background: var(--paper-soft); font-feature-settings: var(--features-no-ligatures); }
time  { font-family: var(--mono); font-feature-settings: var(--features-tabular); color: var(--ink); }
.metric { font-family: var(--sans); font-size: var(--font-size-h3); font-weight: var(--weight-bold); line-height: 1; color: var(--ink); font-variant-numeric: tabular-nums; letter-spacing: var(--tracking-tight); }
.unit   { font-family: var(--sans); font-size: var(--font-size-caption); font-weight: var(--weight-regular); color: var(--ink-soft); margin-left: var(--space-2); }
.delta       { font-family: var(--mono); font-feature-settings: var(--features-tabular); font-weight: var(--weight-medium); }
.delta-up    { color: var(--accent-cool); }
.delta-down  { color: var(--accent-warm); }
.id { font-family: var(--mono); font-size: 0.92em; color: var(--ink-soft); font-feature-settings: var(--features-no-ligatures); }

/* Column grid */
.grid {
  display: grid;
  grid-template-columns: repeat(var(--grid-cols), 1fr);
  gap: var(--grid-gutter);
  max-width: var(--grid-max-width);
  margin: 0 auto;
  padding: 0 var(--grid-margin);
}
.grid + .grid { margin-top: var(--space-12); }

.span-1  { grid-column: span 1; }
.span-2  { grid-column: span 2; }
.span-3  { grid-column: span 3; }
.span-4  { grid-column: span 4; }
.span-6  { grid-column: span 6; }
.span-8  { grid-column: span 8; }
.span-12 { grid-column: 1 / -1; }
.span-full { grid-column: 1 / -1; }

@media (min-width: 641px) {
  .md-span-4 { grid-column: span 4; }
  .md-span-6 { grid-column: span 6; }
  .md-span-8 { grid-column: span 8; }
}
@media (min-width: 1024px) {
  .lg-span-3 { grid-column: span 3; }
  .lg-span-4 { grid-column: span 4; }
  .lg-span-6 { grid-column: span 6; }
  .lg-span-8 { grid-column: span 8; }
  .lg-span-12 { grid-column: 1 / -1; }
}
```

Themes append their own selectors after this base. They do not override `.grid`, `.span-*`, or rename any utility.

## Theme switch component

Every artifact includes a light/dark/system mode switch. Themes that support only one mode hide irrelevant buttons via CSS but include the markup.

### HTML

```html
<div class="theme-switch" role="group" aria-label="Theme">
  <button data-mode="light"  aria-pressed="false" title="Light">☀</button>
  <button data-mode="dark"   aria-pressed="false" title="Dark">☾</button>
  <button data-mode="system" aria-pressed="true"  title="System">⌘</button>
</div>
```

### CSS

```css
.theme-switch {
  position: fixed; top: var(--space-3); right: var(--space-3);
  display: flex; gap: 0;
  background: var(--paper-soft);
  border: 1px solid var(--gray-300);
  border-radius: 6px;
  padding: 2px;
  font-family: var(--mono);
  z-index: 100;
}
.theme-switch button {
  border: 0; background: transparent;
  width: 28px; height: 24px;
  font-size: 14px; line-height: 1;
  cursor: pointer; color: var(--ink-soft);
  border-radius: 4px;
}
.theme-switch button[aria-pressed="true"] {
  background: var(--paper); color: var(--ink);
}
@media (max-width: 480px) { .theme-switch { top: var(--space-2); right: var(--space-2); } }
```

### JS

```js
(function () {
  const KEY = 'composer-theme-mode';
  const html = document.documentElement;
  const apply = (mode) => {
    if (mode === 'system') delete html.dataset.theme;
    else html.dataset.theme = mode;
    document.querySelectorAll('.theme-switch button').forEach(b => {
      b.setAttribute('aria-pressed', String(b.dataset.mode === mode));
    });
  };
  const init = () => {
    const saved = localStorage.getItem(KEY) || 'system';
    apply(saved);
    document.querySelectorAll('.theme-switch button').forEach(b => {
      b.addEventListener('click', () => {
        const m = b.dataset.mode;
        localStorage.setItem(KEY, m);
        apply(m);
      });
    });
  };
  if (document.readyState !== 'loading') init();
  else document.addEventListener('DOMContentLoaded', init);
})();
```

### Mode handling in palettes

Themes scope dark-mode tokens via `[data-theme="dark"]` plus a `prefers-color-scheme` fallback for `system` mode:

```css
:root {
  /* light palette tokens */
  --paper: #fafaf7;
  --ink: #1a1a1a;
  /* ... */
}

[data-theme="dark"] {
  --paper: #161413;
  --ink: #f5f1e9;
  /* ... */
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --paper: #161413;
    --ink: #f5f1e9;
    /* ... duplicate of [data-theme="dark"] block ... */
  }
}
```

The `:not([data-theme="light"])` guard ensures that an explicit light-mode override beats the system preference.

Themes that support only one mode (e.g., infolog-terminal is dark-only) include the same markup but hide the irrelevant buttons:

```css
.theme-switch button[data-mode="light"]  { display: none; }
.theme-switch button[data-mode="system"] { display: none; }
```

Each theme's `themespec.json` declares `"modes": ["light", "dark", "system"]` or `["dark"]` etc., so future tooling can introspect.

## Required class conventions

Themes may add more, but the drafter always uses these structural classes:

- `.grid`, `.span-*`, `.md-span-*`, `.lg-span-*` — layout
- `.figure` — wraps an SVG chart + caption
- `.data-table` — quantitative tables
- `.annotation` — callouts and notes
- `.axis`, `.tick`, `.tick-label`, `.data-mark` — SVG chart parts
- `.metric`, `.unit`, `.delta`, `.delta-up`, `.delta-down`, `.id` — semantic data callouts
- `.theme-switch` — mode switch (required)

`.page` is deprecated — use a `.grid` with `.span-full` children instead.

## Typographic discipline

No orphans or widows. A single word, a date, or a fragment alone on the final line of a heading, lede, annotation, caption, or footer looks broken.

`text-wrap: balance` is already applied to `h1`–`h5` and `small` in the required base. Apply it explicitly to any custom lede / annotation / footer block. For body paragraphs, the base uses `text-wrap: pretty`. If `text-wrap: balance` is unavailable on a target, rewrite the text shorter or use `&nbsp;` between the last two tokens of the run.

The composer's `orphan_widow` criterion fails when any heading or short-prose block ends with a final line shorter than 25% of the block's measure.

## Forbidden in artifact

- External fonts, scripts, stylesheets, images.
- `<link rel="stylesheet">` to anything.
- CSS frameworks (Bootstrap, Tailwind utility classes if not generated).
- `import` / `require` / `from` JS module syntax.
- Build-tool comments (`/* eslint */`, `/* @ts-ignore */`).

## File size guideline

Target 15–35 KB for a complete chart page. The required CSS base alone is ~3 KB; the theme switch JS adds ~0.5 KB. Above 50 KB suggests embedded base64 images or chartjunk — investigate before shipping.

## Why this style

The artifact is portable. It survives email, paste, Slack, archive.org. It opens offline. It's reviewable in a diff. It can be edited by humans. A React build is none of these.
