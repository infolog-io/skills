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

### Semantic communication colors (theme-defined, Foundation-declared)

Four semantic tokens for UI feedback. Names are fixed across themes; values vary. Use these whenever a component needs to communicate intent (positive, informational, cautionary, dangerous). Default values below; themes may override.

```css
--success: #1a7d3b;   /* green  · positive state, OK, complete, live */
--info:    #3D81B8;   /* blue   · neutral information, links, references */
--warning: #E3B22F;   /* yellow · caution, pending, requires attention */
--danger:  #c8553d;   /* red    · error, destructive action, critical */
```

Mapped to the existing slot system: `--accent-warm` defaults to `var(--success)`. Themes that want a different highlight can remap `--accent-warm` to any of the four semantic tokens (e.g., `--accent-warm: var(--danger)` for an error-themed view) or define a separate color.

Components opt into semantics via class modifiers (see "Required CSS base" below): `.success`, `.info`, `.warning`, `.danger` apply to `.mockup-dot`, `.mockup-bar`, `.mockup-btn`, `.mockup-stat`, plus utility classes `.text-success`, `.bg-success` etc.

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

/* Mockup primitive — HTML/CSS mock-UI card for showing before/after, screenshots, variants, previews.
   Use when you want to illustrate a UI without embedding an actual image. Pure CSS placeholders. */
.mockup {
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}
.mockup-label {
  font-family: var(--mono);
  font-size: var(--font-size-caption);
  color: var(--ink-soft);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
}
.mockup-frame {
  position: relative;
  background: var(--gray-900);
  border-radius: var(--radius-panel);
  padding: var(--space-3);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  overflow: hidden;
  aspect-ratio: 16 / 10;
}
.mockup-chrome {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding-bottom: var(--space-2);
}
.mockup-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--ink-soft);
  flex-shrink: 0;
}
.mockup-dot.warm    { background: var(--accent-warm); }
.mockup-dot.cool    { background: var(--accent-cool); }
.mockup-dot.success { background: var(--success); }
.mockup-dot.info    { background: var(--info); }
.mockup-dot.warning { background: var(--warning); }
.mockup-dot.danger  { background: var(--danger); }
.mockup-title {
  font-family: var(--mono);
  font-size: var(--font-size-caption);
  color: var(--paper);
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
}
.mockup-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}
.mockup-bar {
  height: 8px;
  width: 60%;
  background: var(--gray-700);
  border-radius: 2px;
}
.mockup-bar.wide   { width: 100%; }
.mockup-bar.narrow { width: 30%; }
.mockup-bar.muted  { background: var(--gray-500); opacity: 0.5; }
.mockup-bar.accent { background: var(--accent-warm); }
.mockup-bar.tall   { height: var(--space-6); }
.mockup-row {
  display: flex;
  gap: var(--space-2);
  align-items: center;
}
.mockup-btn {
  font-family: var(--sans);
  font-size: var(--font-size-caption);
  padding: var(--space-1) var(--space-3);
  border-radius: 4px;
  border: 1px solid transparent;
  cursor: default;
}
.mockup-btn.primary { background: var(--accent-warm); color: var(--paper); }
.mockup-btn.ghost   { background: transparent; color: var(--paper); border-color: var(--gray-500); }
.mockup-cursor {
  position: absolute;
  width: 14px; height: 14px;
  pointer-events: none;
  filter: drop-shadow(0 1px 2px rgba(0,0,0,0.4));
}
.mockup-cursor::before {
  content: "";
  display: block;
  width: 0; height: 0;
  border-left: 8px solid var(--paper);
  border-top: 5px solid transparent;
  border-bottom: 9px solid transparent;
  transform: rotate(-30deg);
}
.mockup-cursor.bottom-left { left: var(--space-4); bottom: var(--space-4); }
.mockup-cursor.center      { left: 50%; top: 50%; transform: translate(-50%, -50%); }

/* Mockup chrome variants — different "device" surfaces */

/* Browser: traffic-light dots + URL bar */
.mockup-frame.browser .mockup-chrome { gap: var(--space-3); padding-bottom: var(--space-2); border-bottom: 1px solid var(--gray-700); }
.mockup-traffic { display: inline-flex; gap: 4px; flex-shrink: 0; }
.mockup-traffic > span { width: 8px; height: 8px; border-radius: 50%; background: var(--gray-500); display: inline-block; }
.mockup-url { font-family: var(--mono); font-size: var(--font-size-caption); color: var(--ink-soft); background: var(--gray-700); padding: 2px var(--space-2); border-radius: 3px; flex: 1; text-align: center; opacity: 0.6; }

/* Document: light paper, optional top accent stripe */
.mockup-frame.document { background: var(--paper); border: var(--border); }
.mockup-frame.document .mockup-title { color: var(--ink); }
.mockup-frame.document .mockup-bar { background: var(--gray-700); }
.mockup-frame.document .mockup-bar.muted { background: var(--gray-300); opacity: 1; }
.mockup-stripe { display: block; height: var(--space-1); width: 40%; background: var(--ink-soft); border-radius: 2px; margin-bottom: var(--space-2); }
.mockup-stripe.warm { background: var(--accent-warm); }
.mockup-stripe.cool { background: var(--accent-cool); }
/* .mockup-accent-stripe — DEPRECATED v2.1, use .mockup-stripe.warm */
.mockup-accent-stripe { display: block; height: var(--space-1); width: 40%; background: var(--ink-soft); border-radius: 2px; margin-bottom: var(--space-2); }

/* Sketch: dashed border, outline-only content */
.mockup-frame.sketch { background: var(--paper); border: 2px dashed var(--ink); }
.mockup-frame.sketch .mockup-title { color: var(--ink); font-style: italic; }
.mockup-frame.sketch .mockup-bar { background: transparent; border: 1px solid var(--ink); height: var(--space-3); }
.mockup-cell { flex: 1; border: 1px solid var(--ink); background: transparent; aspect-ratio: 4 / 3; border-radius: 2px; }

/* Dashboard: inner stat tiles + mini charts (use .mockup-row inside) */
.mockup-frame.dashboard { background: var(--paper); border: var(--border); }
.mockup-frame.dashboard .mockup-title { color: var(--ink); }
.mockup-stat { display: flex; flex-direction: column; gap: 2px; padding: var(--space-2); background: var(--paper-soft); border-radius: 4px; flex: 1; min-width: 60px; }
.mockup-stat-label { font-family: var(--mono); font-size: 0.7em; color: var(--ink-soft); text-transform: uppercase; letter-spacing: var(--tracking-wide); }
.mockup-stat-value { font-family: var(--mono); font-size: 1.2em; font-weight: var(--weight-bold); color: var(--ink); }
.mockup-stat-delta { font-family: var(--mono); font-size: 0.65em; color: var(--accent-cool); }
.mockup-stat.warm    { background: color-mix(in srgb, var(--accent-warm) 15%, var(--paper-soft)); }
.mockup-stat.warm    .mockup-stat-value { color: var(--accent-warm); }
.mockup-stat.cool    { background: color-mix(in srgb, var(--accent-cool) 15%, var(--paper-soft)); }
.mockup-stat.cool    .mockup-stat-value { color: var(--accent-cool); }
.mockup-stat.success { background: color-mix(in srgb, var(--success) 15%, var(--paper-soft)); }
.mockup-stat.success .mockup-stat-value { color: var(--success); }
.mockup-stat.info    { background: color-mix(in srgb, var(--info)    15%, var(--paper-soft)); }
.mockup-stat.info    .mockup-stat-value { color: var(--info); }
.mockup-stat.warning { background: color-mix(in srgb, var(--warning) 15%, var(--paper-soft)); }
.mockup-stat.warning .mockup-stat-value { color: var(--warning); }
.mockup-stat.danger  { background: color-mix(in srgb, var(--danger)  15%, var(--paper-soft)); }
.mockup-stat.danger  .mockup-stat-value { color: var(--danger); }

/* Semantic utility classes — usable on any element */
.text-success { color: var(--success); }
.text-info    { color: var(--info); }
.text-warning { color: var(--warning); }
.text-danger  { color: var(--danger); }
.bg-success { background: var(--success); color: var(--paper); }
.bg-info    { background: var(--info);    color: var(--paper); }
.bg-warning { background: var(--warning); color: var(--ink); }
.bg-danger  { background: var(--danger);  color: var(--paper); }

/* Alert component — banner-style semantic feedback.
   No border stripe, no icon chip. Intent is carried by tinted bg + dark-of-accent text. */
.alert { display: block; padding: var(--space-3) var(--space-4); border-radius: var(--radius-panel); font-size: var(--font-size-body); margin-bottom: var(--space-2); }
.alert.success { background: color-mix(in srgb, var(--success) 12%, var(--paper)); color: color-mix(in srgb, var(--success) 60%, var(--ink)); }
.alert.info    { background: color-mix(in srgb, var(--info)    12%, var(--paper)); color: color-mix(in srgb, var(--info)    60%, var(--ink)); }
.alert.warning { background: color-mix(in srgb, var(--warning) 12%, var(--paper)); color: color-mix(in srgb, var(--warning) 45%, var(--ink)); }
.alert.danger  { background: color-mix(in srgb, var(--danger)  12%, var(--paper)); color: color-mix(in srgb, var(--danger)  60%, var(--ink)); }
.mockup-mini-chart { height: var(--space-8); display: flex; align-items: flex-end; gap: 3px; padding: var(--space-1) 0; }
.mockup-mini-chart .mc-bar { flex: 1; background: var(--gray-700); border-radius: 1px; min-height: 4px; }
.mockup-mini-chart .mc-bar.accent  { background: var(--accent-warm); }
.mockup-mini-chart .mc-bar.cool    { background: var(--accent-cool); }
.mockup-mini-chart .mc-bar.success { background: var(--success); }
.mockup-mini-chart .mc-bar.info    { background: var(--info); }
.mockup-mini-chart .mc-bar.warning { background: var(--warning); }
.mockup-mini-chart .mc-bar.danger  { background: var(--danger); }
.mockup-mini-chart.line { display: block; position: relative; }
.mockup-mini-chart.line svg { width: 100%; height: 100%; }
.mockup-mini-chart.line svg path { stroke: var(--ink-soft); fill: none; }
.mockup-mini-chart.line.accent svg path { stroke: var(--accent-warm); }
.mockup-mini-chart.line.cool   svg path { stroke: var(--accent-cool); }

/* Data-table: CSV/grid-of-rows */
.mockup-frame.data-table { background: var(--paper); border: var(--border); padding: 0; }
.mockup-frame.data-table .mockup-chrome { padding: var(--space-2) var(--space-3); border-bottom: var(--border); background: var(--paper-soft); }
.mockup-frame.data-table .mockup-title { color: var(--ink); }
.mockup-frame.data-table .mockup-body { padding: 0; gap: 0; }
.mockup-data-row { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: var(--space-3); padding: var(--space-1) var(--space-3); font-family: var(--mono); font-size: 0.8em; color: var(--ink); border-bottom: 1px solid var(--gray-100); }
.mockup-data-row.header { color: var(--ink-soft); font-weight: var(--weight-medium); border-bottom: 1px solid var(--gray-300); }
.mockup-data-row:last-child { border-bottom: none; }

/* WRAPPERS — compose mockups into stories */

/* Sequence: horizontal layout of mockups connected by arrows */
.mockup-sequence { display: flex; flex-wrap: wrap; align-items: center; gap: var(--space-4); margin: var(--space-6) 0; padding: var(--space-4); background: var(--paper-soft); border-radius: var(--radius-panel); }
.mockup-sequence > .mockup { flex: 1 1 220px; min-width: 220px; }

/* Arrow: connector with optional top + sub captions */
.mockup-arrow { flex: 0 0 auto; display: flex; flex-direction: column; align-items: center; gap: var(--space-1); min-width: 100px; max-width: 160px; padding: 0 var(--space-2); }
.mockup-arrow-caption { font-family: var(--mono); font-size: var(--font-size-caption); color: var(--ink-soft); text-transform: uppercase; letter-spacing: var(--tracking-wide); }
.mockup-arrow-caption.warm { color: var(--accent-warm); }
.mockup-arrow-line { display: block; width: 100%; text-align: center; color: var(--ink-soft); font-family: var(--mono); letter-spacing: 1px; }
.mockup-arrow-line.warm { color: var(--accent-warm); }
.mockup-arrow-line::after { content: " →"; }
.mockup-arrow-sub { font-family: var(--serif, var(--sans)); font-style: italic; color: var(--ink-soft); font-size: var(--font-size-caption); text-align: center; }

/* Proposal card: section wrapper for documenting a pattern (heading, badges, prose, meta rows) */
.proposal-card { background: var(--paper-soft); border-radius: var(--radius-panel); padding: var(--space-8); margin: var(--space-6) 0; display: flex; flex-direction: column; gap: var(--space-3); }
.proposal-header { display: flex; justify-content: space-between; align-items: baseline; gap: var(--space-3); flex-wrap: wrap; }
.proposal-header h3 { color: var(--ink); margin: 0; }
.proposal-tier { font-family: var(--mono); font-size: var(--font-size-caption); color: var(--ink-soft); text-transform: uppercase; letter-spacing: var(--tracking-wide); white-space: nowrap; }
.proposal-badges { display: flex; gap: var(--space-2); flex-wrap: wrap; }
.proposal-badge { font-family: var(--mono); font-size: 0.75rem; text-transform: uppercase; letter-spacing: var(--tracking-wide); padding: 2px var(--space-2); border-radius: 2px; background: var(--gray-100); color: var(--ink); }
.proposal-meta { display: grid; grid-template-columns: 100px 1fr; gap: var(--space-2) var(--space-4); padding-top: var(--space-3); border-top: var(--border); font-size: var(--font-size-caption); margin: 0; }
.proposal-meta dt { font-family: var(--mono); color: var(--ink-soft); text-transform: uppercase; letter-spacing: var(--tracking-wide); }
.proposal-meta dd { margin: 0; color: var(--ink); }

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
- `.mockup`, `.mockup-label`, `.mockup-frame`, `.mockup-chrome`, `.mockup-dot`, `.mockup-title`, `.mockup-body`, `.mockup-bar` (+ `.wide`/`.narrow`/`.muted`/`.accent`/`.tall`), `.mockup-row`, `.mockup-btn` (+ `.primary`/`.ghost`), `.mockup-cursor` (+ `.bottom-left`/`.center`) — mock-UI cards for before/after, variants, previews
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
