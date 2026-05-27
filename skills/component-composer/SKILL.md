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

## Dependency

This skill is a **consumer of the `generator-critic` skill**. The
abstract loop pattern (cycle, HUD, stuck detection, audit-summary format,
drafter+validator contracts) lives there. Install both:

```
/plugin install generator-critic@infolog-io
/plugin install component-composer@infolog-io
```

`component-composer` provides the HTML-specific implementation:
`output-style.md`, `theme-spec.md`, `mechanical-checks.js`, the HTML
drafter rules, and the HTML validator dispatch.

## Operating mode

When invoked with a job + theme name:

1. **Resolve theme** — read `skills/<theme>/themespec.json` and load the
   theme's `tokens.md`, `criteria.md`, `patterns.md`, `palette.md`.
2. **Draft** — invoke the drafter per `references/drafter-protocol.md`
   (HTML-specific; extends `generator-critic/references/drafter-contract.md`).
3. **Render** — write artifact to session dir; render via Claude Preview.
4. **Inject HUD** — overlay `generator-critic/scripts/hud.js` per
   `generator-critic/references/hud-protocol.md`.
5. **Validate** — run mechanical checks via `preview_eval`, then LLM-as-judge
   for the rest, per `references/validator-protocol.md` (HTML-specific;
   extends `generator-critic/references/validator-contract.md`).
   Repeat at three viewports (mobile 375 / tablet 768 / desktop 1280).
6. **Aggregate failures** — per `generator-critic/references/loop-protocol.md`.
7. **Loop** — if any failure, feed back to drafter and goto step 2.
   If stuck, surface to user via HUD + chat (stuck-detection rules in
   loop-protocol).
8. **Emit** — final HTML + PNG (via `scripts/export-png.js`) + PDF (via
   `scripts/export-pdf.js`) + audit summary (per
   `generator-critic/references/audit-summary-format.md`) + iteration
   history.

## References

This skill (HTML-specific):

- `references/drafter-protocol.md` — HTML drafter rules + required artifact structure
- `references/validator-protocol.md` — HTML validator dispatch + criteria registry
- `references/theme-spec.md` — theme interface contract (HTML-flavored)
- `references/output-style.md` — Atomic Foundation: tokens, base CSS, theme switch

Inherited from `generator-critic`:

- `generator-critic/references/loop-protocol.md` — loop steps, stuck detection
- `generator-critic/references/drafter-contract.md` — abstract drafter interface
- `generator-critic/references/validator-contract.md` — abstract dispatch + output shape
- `generator-critic/references/hud-protocol.md` — HUD injection + state polling
- `generator-critic/references/audit-summary-format.md` — final-emit shape

## Scripts

This skill (HTML-specific):

- `scripts/mechanical-checks.js` — 9 pure DOM check functions + browser adapter
- `scripts/export-png.js` — PNG export contract
- `scripts/export-pdf.js` — PDF export contract

Inherited from `generator-critic`:

- `generator-critic/scripts/hud.js` — in-loop HUD overlay (vanilla JS)

## Template

- `template/base.html` — HTML skeleton with `:root` token slots
