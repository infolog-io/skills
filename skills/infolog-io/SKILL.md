---
name: infolog-io
description: >
  Theme bundle for component-composer. Provides tokens, criteria, patterns,
  and palette for Tufte-style data graphics: range-frame axes, small
  multiples, high data-ink, single highlight, no chartjunk. Activated when
  component-composer is invoked with `infolog-io` as the theme name.
---

# infolog-io

This skill is a **theme** for `component-composer`. It does not run on
its own. The composer reads this skill's references when the user invokes
composition with `infolog-io` as the active theme.

## What this theme provides

- `themespec.json` — manifest
- `references/tokens.md` — CSS variable schema (which vars, what role)
- `references/palette.md` — concrete values for the Tufte-quiet aesthetic
- `references/criteria.md` — validator rules (no chartjunk, range-frame, etc.)
- `references/patterns.md` — preferred chart patterns
- `references/principles.md` — foundational Tufte principles
- `references/analytical-design.md` — extended principles (sparklines, layering, micro/macro)
- `references/chart-patterns.md` — supplementary chart-selection patterns
- `references/chart-rules-extras.md` — supplementary number-formatting and time-axis rules

## Aesthetic

Quiet. Most ink is gray. One warm accent reserved for the single
highlighted mark. Range-frame axes terminating at data extent. Direct
labels over legends. Words integrated with numbers and images. Multiple
levels of detail (micro + macro). Sparklines and small multiples preferred
over single overloaded charts.

## To invoke

> "compose a chart with infolog-io showing my GitHub usage data"

The composer resolves `infolog-io` via `themespec.json`, reads the
references, drafts an HTML artifact, validates against `criteria.md`, and
iterates until clean.
