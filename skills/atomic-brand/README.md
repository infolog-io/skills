# atomic-brand

Audits web projects against atomic design discipline and brand-token
coherence. Catches scattered components, hardcoded values, brand drift,
and naming-by-appearance.

## Why

Design system drift is the most common kind of frontend rot: three
buttons that should be one, a color hardcoded instead of tokenized.
Block the drift at audit time.

## What you get

A scored audit across 8 dimensions, plus one of three verdicts:

- **system-healthy** — ship
- **drifting** — refactor against the emitted `refactor-plan.md`
- **broken** — stop; build the missing tokens and patterns per the
  emitted `build-out-plan.md`

## When to use

- Before shipping a redesign or rebrand
- Auditing inherited code for system coherence
- Standardizing across a multi-team frontend
- Reviewing a component library PR
- When tokens exist but components look inconsistent

Not for greenfield projects, non-web design systems, or backend repos.

## Scope (v0.1.0)

Web only (CSS, HTML, React/Vue/Svelte). Native, TUI, print, and email
follow as sibling skills.

## Install

```bash
claude plugin marketplace add infolog-io/skills
claude plugin install atomic-brand@infolog-io
```

## Triggers

`atomic audit` · `brand audit` · `design system audit` · `is this
on-brand` · `find duplicate components` · `what tokens am I missing` ·
`/atomic-brand`
