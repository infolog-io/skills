# atomic-brand

Audits web projects against atomic design discipline and brand-token
coherence. Catches scattered components, hardcoded values, brand drift,
and naming-by-appearance.

## Why

Design system drift is the most common kind of frontend rot. Three
buttons that should be one. A color hardcoded instead of tokenized. A
"molecule" that's actually a page-level organism. Block the drift at
audit time.

## What you get

A scored audit across 8 dimensions, plus one of three verdicts:

- **system-healthy** — ship
- **drifting** — refactor against the emitted plan
- **broken** — stop; build the missing tokens and patterns first

When verdict is `broken`, the skill emits a `build-out-plan.md` listing
the specific tokens and patterns that need to exist before the project
can recover.

## When to use

- Before shipping a redesign or rebrand
- Auditing inherited code for system coherence
- Standardizing across a multi-team frontend
- Reviewing a component library PR

## Scope (v0.1.0)

Web only (CSS, HTML, React/Vue/Svelte). Native (Swift, Compose), TUI,
print, and email follow as sibling skills in later versions.

## Install

```bash
claude plugin marketplace add infolog-io/skills
claude plugin install atomic-brand@infolog-io
```

## Triggers

`atomic audit` · `brand audit` · `is this on-brand` · `/atomic-brand`
