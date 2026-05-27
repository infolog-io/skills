---
name: component-composer
description: >
  Production-grade single-file HTML data graphics through a generator-critic
  loop. Drafts via theme, renders in Claude Preview, validates with hybrid
  mechanical + LLM-as-judge checks at three viewports, iterates until every
  active-theme criterion passes. Use for recurring dashboards, multi-theme
  reports, or design-system-enforced artifacts. Do NOT use for casual,
  throwaway, or interactive HTML — just ask Claude directly for those.
  Activates on "compose with <theme>", "render this chart with the design
  system", "/compose", or any composition request that names a theme.
---

# component-composer

## Purpose

Build single-file HTML data graphics through a generator-critic loop. The
drafter writes HTML; the validator critiques the rendered output; the
composer feeds failures back to the drafter and iterates until clean.

Themes own the quality criteria. The composer is theme-agnostic.

## When to use

This skill is for **production-grade data graphics** where consistency
matters across artifacts, themes, viewports, and time:

- Recurring dashboards or reports that must look uniform
- Artifacts that will be shared, archived, or revisited
- Multi-theme work where the same data renders under different aesthetics
- Cases where validator-enforced token discipline (color, type, spacing)
  is worth the loop overhead

## When NOT to use

This skill is the wrong tool for casual or one-off HTML. Thariq Shihipar's
post — [The Unreasonable Effectiveness of HTML](https://www.anthropic.com/engineering/claude-code-html)
— is the canonical guidance for the broader case. He explicitly warned:

> "I'm a little bit afraid that people will read this article and turn it
> into a /html skill or something. While there might be some value in
> that, I want to emphasize that you don't need to do much to get Claude
> to do this. You can just ask it to 'make a HTML file' or 'make a HTML
> artifact'."

For the following cases, **do not invoke `/compose`**; just ask Claude
directly:

- Throwaway editors purpose-built for one piece of data (Linear ticket
  triage, prompt tuner, feature-flag editor)
- Specs, code-review explainers, PR walkthroughs, design mockups,
  research reports
- One-off explorations: "show me 6 different onboarding layouts side by
  side"
- Anything where the artifact's value is in *being made and used once*,
  not in conforming to a recurring quality bar
- Interactive prototypes with sliders, knobs, copy-as-prompt buttons

The composer's industrial QA loop is overkill for these and gets in the
way of Thariq's "just make a HTML file" simplicity.

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
