# Output Style — Single-File HTML

The drafter's output is one self-contained `.html` file. No build step.
No npm dependencies. No external requests. The artifact must open
correctly when the user double-clicks it on any modern browser, online
or offline.

Style anchor: `ThariqS/html-effectiveness` — a gallery of single-file
HTML examples demonstrating how much fidelity a static file can carry.

## Required structure

1. `<!DOCTYPE html>` + `<html lang="en">` + `<meta charset>` + viewport meta.
2. Inline `<style>` in `<head>`. **All** styling lives here.
3. CSS custom properties declared on `:root` — every color, type size,
   spacing, and radius is a `var(--...)` reference. No literal hex codes
   or px values outside the `:root` block.
4. The body uses semantic HTML — `<header>`, `<section>`, `<table>`,
   `<figure>` — not generic `<div>` soup.
5. Inline `<svg>` for every chart. No `<img>` for chart content.
6. Vanilla `<script>` only when interaction is real (theme switcher,
   tooltips, filtering). No external libraries. No `import` statements.

## Required token vocabulary (declared on `:root`)

Theme `tokens.md` files declare which of these are required for that
theme. The composer enforces presence via the `token_compliance`
mechanical check.

- `--paper`, `--paper-soft` — surfaces
- `--ink`, `--ink-soft` — text/data
- `--accent-warm`, `--accent-cool`, `--accent-quiet` — highlights
- `--gray-100` through `--gray-900` — neutral ramp
- `--serif`, `--sans`, `--mono` — font families
- `--font-size-h1` through `--font-size-caption` — type scale
- `--space-1` through `--space-12` — spacing scale
- `--radius-panel`, `--border` — structural

## Required class conventions

Themes may add more, but the drafter always uses these structural classes:

- `.page` — max-width container
- `.figure` — wraps an SVG chart + caption
- `.data-table` — quantitative tables
- `.annotation` — callouts and notes
- `.axis`, `.tick`, `.tick-label`, `.data-mark` — SVG chart parts

## Forbidden in artifact

- External fonts, scripts, stylesheets, images.
- `<link rel="stylesheet">` to anything.
- CSS frameworks (Bootstrap, Tailwind utility classes if not generated).
- `import` / `require` / `from` JS module syntax.
- Build-tool comments (`/* eslint */`, `/* @ts-ignore */`).

## File size guideline

Target 12-30KB for a complete chart page. The html-effectiveness gallery
files range 12-28KB. Above 50KB suggests embedded base64 images or
chartjunk — investigate before shipping.

## Why this style

The artifact is portable. It survives email, paste, Slack, archive.org.
It opens offline. It's reviewable in a diff. It can be edited by humans.
A React build is none of these.
