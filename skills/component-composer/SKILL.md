---
name: component-composer
description: >
  Generator-critic loop for single-file HTML artifacts. Drafts via theme,
  renders in Claude Preview, validates with hybrid mechanical + LLM-as-judge
  checks at three viewports, iterates until every active-theme criterion
  passes. Activates on "compose with <theme>", "render this chart",
  "/compose", or any data-graphics composition request that names a theme.
---

# component-composer

## Purpose

Build single-file HTML data graphics through a generator-critic loop. The
drafter writes HTML; the validator critiques the rendered output; the
composer feeds failures back to the drafter and iterates until clean.

Themes own the quality criteria. The composer is theme-agnostic.

## Operating mode

When invoked with a job + theme name:

1. **Resolve theme** — read `skills/<theme>/themespec.json` and load the
   theme's `tokens.md`, `criteria.md`, `patterns.md`, `palette.md`.
2. **Draft** — invoke the drafter per `references/drafter-protocol.md`.
3. **Render** — write artifact to session dir; render via Claude Preview.
4. **Inject HUD** — overlay `scripts/hud.js` per `references/hud-protocol.md`.
5. **Validate** — run mechanical checks via `preview_eval`, then LLM-as-judge
   for the rest, per `references/validator-protocol.md`. Repeat at three
   viewports (mobile 375 / tablet 768 / desktop 1280).
6. **Aggregate failures** — per `references/loop-protocol.md`.
7. **Loop** — if any failure, feed back to drafter and goto step 2.
   If stuck, surface to user via HUD + chat.
8. **Emit** — final HTML + PNG (via `scripts/export-png.js`) + PDF (via
   `scripts/export-pdf.js`) + audit summary + iteration history.

## References

- `references/drafter-protocol.md` — drafter LLM behavior
- `references/validator-protocol.md` — hybrid validator behavior
- `references/loop-protocol.md` — loop steps, stuck detection, audit format
- `references/theme-spec.md` — theme interface contract
- `references/output-style.md` — single-file HTML style anchor
- `references/hud-protocol.md` — HUD injection + state polling

## Scripts

- `scripts/mechanical-checks.js` — 9 pure validator check functions
- `scripts/hud.js` — in-loop HUD overlay (vanilla JS)
- `scripts/export-png.js` — PNG export
- `scripts/export-pdf.js` — PDF export

## Template

- `template/base.html` — HTML skeleton with `:root` token slots
