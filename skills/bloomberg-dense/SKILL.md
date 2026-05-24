---
name: bloomberg-dense
description: >
  Theme bundle for component-composer. Terminal/Bloomberg-terminal
  aesthetic: green-on-black, monospace everywhere, maximum data density,
  no chartjunk. Activated when component-composer is invoked with
  `bloomberg-dense` as the theme name.
---

# bloomberg-dense

This skill is a **theme** for `component-composer`. It does not run on
its own.

## What this theme provides

- `themespec.json` — manifest
- `references/tokens.md` — CSS variable schema (same structural tokens as
  atomic-data-viz; different values)
- `references/palette.md` — green-on-black, monospace
- `references/criteria.md` — density-first criteria
- `references/patterns.md` — dense-table-first patterns

## Aesthetic

Dark background. Bright green primary ink. Tabular monospace everywhere.
Maximum information per pixel. No serifs. No drop-shadows. No gradients.
Looks like a Bloomberg terminal or top from 1995.

This theme exists to prove the multi-theme architecture: it shares the
same component catalog as atomic-data-viz, but the rendered output is
visually completely different.

## To invoke

> "compose with bloomberg-dense showing the same GitHub data"
