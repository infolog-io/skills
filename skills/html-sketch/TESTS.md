# html-sketch — Tests

## End conditions

- Drafter can produce a working artifact from a one-line prompt using one of the four named patterns without needing to read `component-composer` references.
- All four pattern references include a copy-paste-able skeleton that runs unmodified in any modern browser.
- Copy-as-prompt footer pattern works: the JS reads form state, builds a markdown-ready string, copies to clipboard.

## Test cases

### TC1 — Throwaway editor for ticket triage

Given: "Make me a throwaway editor for these 30 Linear tickets — draggable across Now / Next / Later / Cut, with a copy-as-markdown button."
When: drafter reads `references/throwaway-editor.md` + `references/copy-as-prompt.md`.
Then: emits a single HTML file with drag handles, the four columns, pre-sorted tickets, and a working copy button.

### TC2 — Compare 6 onboarding layouts

Given: "Show me 6 distinctly different onboarding screen approaches in a single HTML grid."
When: drafter reads `references/compare-variants.md`.
Then: emits an HTML grid of 6 panels, each labeled with the tradeoff it makes (per Thariq's example prompt).

### TC3 — Tune an animation with sliders

Given: "I want to prototype a checkout button animation — give me sliders for duration / easing / color and a copy button for the tuned params."
When: drafter reads `references/interactive-tuning.md` + `references/copy-as-prompt.md`.
Then: emits an HTML page with live-preview canvas, sliders bound to CSS vars, and a copy button that exports the tuned values as JSON or as a paste-ready prompt fragment.

### TC4 — Single-page rate-limiter explainer

Given: "Explain how our rate limiter works in one HTML page — diagram, code snippets, gotchas."
When: drafter reads `references/single-page-report.md`.
Then: emits a long-scroll page with sticky TOC, inline SVG diagram, code blocks, and a "gotchas" section at the bottom.

### TC5 — Skill does NOT enforce validator gates

Given: drafter produces an artifact that lacks the Atomic Foundation tokens or has loose contrast.
When: the artifact is delivered.
Then: no validation step runs, no failure is raised, the user sees the file as-is. (The point of `html-sketch` is that there's no quality gate — judgment is the user's.)
