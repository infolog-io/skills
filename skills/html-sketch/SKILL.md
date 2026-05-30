---
name: html-sketch
description: >
  Casual HTML artifacts in Thariq Shihipar's "Unreasonable Effectiveness
  of HTML" style — throwaway editors, side-by-side variant comparisons,
  interactive tuning with sliders/knobs, single-page reports. No
  validator loop, no themes, no industrial QA. Single-file HTML you make,
  use once, and discard. Includes the "copy-as-prompt" footer pattern
  for round-tripping back into Claude. Activates on "make a throwaway
  HTML", "sketch an editor for", "build a quick HTML to triage", "show
  me N options side by side", "interactive prototype for", "/sketch", or
  any one-off HTML request that does NOT need theme conformance.
---

# html-sketch

## Purpose

Encode the patterns Thariq Shihipar documented in
[The Unreasonable Effectiveness of HTML](https://www.anthropic.com/engineering/claude-code-html)
so the drafter has named templates for casual artifacts without
reaching for the heavy machinery of `component-composer`.

Thariq's thesis, paraphrased: HTML is the best format for agent-to-human
communication. You don't need a skill to use it well — you can just ask
Claude to "make a HTML file." But there ARE recurring patterns worth
naming so they're easy to reach for.

## When to use this skill

Reach for `html-sketch` (or just prompt these patterns directly) when:

- You want a **throwaway editor** for one piece of data (triage 30 Linear
  tickets, edit feature-flag config, tune a system prompt)
- You want to **compare variants side-by-side** ("show me 6 different
  onboarding layouts in a single HTML grid")
- You want an **interactive prototype** with sliders, knobs, and a copy
  button that exports your tuned parameters back to a prompt
- You want a **single-page report or explainer** with TOC, anchors,
  inline SVG diagrams, code snippets
- You want a **PR or code-review explainer** with annotated diffs

## When NOT to use this skill

- The artifact recurs — same shape made many times, with consistency
  requirements. Use `component-composer` for that.
- The artifact is a production dashboard with brand-token enforcement.
  Use `component-composer`.
- You need validated mechanical quality (contrast, font-size floors,
  token compliance). Use `component-composer`.

## Operating mode

When you sketch an artifact, choose a pattern and adapt:

1. **Throwaway editor** — `references/throwaway-editor.md`
2. **Compare variants** — `references/compare-variants.md`
3. **Interactive tuning** — `references/interactive-tuning.md`
4. **Single-page report** — `references/single-page-report.md`

Each reference includes a small copyable template and notes on when to
use it. The drafter adapts the template to the specific job.

## Shared conventions

All four patterns share:

- Single self-contained HTML file (no external requests, opens offline)
- Inline `<style>`, inline `<script>`, no `<link>` to anything
- The Atomic Foundation type tokens are OPTIONAL — use them if you want
  consistency with composer-produced artifacts, skip them otherwise
- A **copy-as-prompt** footer where applicable (see
  `references/copy-as-prompt.md`)

## Not enforced

No validator. No mandatory tokens. No theme switch. No heading-scale
discipline. The drafter has full creative latitude. Quality is judged
by you, the user, opening the file and deciding if it serves.

If you want a quality bar, you want `component-composer`, not this.

## References

- `references/throwaway-editor.md` — single-purpose UI for one data set, with export
- `references/compare-variants.md` — N-up grid for exploring options
- `references/interactive-tuning.md` — sliders, knobs, copy-params button
- `references/single-page-report.md` — long-scroll explainer with TOC + diagrams
- `references/copy-as-prompt.md` — the round-trip footer pattern Thariq highlights
