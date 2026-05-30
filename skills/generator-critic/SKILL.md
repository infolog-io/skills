---
name: generator-critic
description: >
  Generator-critic loop pattern for any artifact produced by an LLM and
  judged against declared criteria. A drafter LLM proposes; a hybrid critic
  (mechanical checks + LLM-as-judge) scores; the orchestrator feeds
  failures back to the drafter and iterates until clean. Artifact-agnostic
  — works for HTML, code, schemas, prose, anything with a validator.
  Activates on "generator-critic loop", "iterate this artifact until it
  passes", "/critic-loop", or when designing a refinement pipeline.
  Consumed by `component-composer` for HTML data graphics; future consumers
  for other artifact types declare a dependency on this skill.
---

# generator-critic

## Purpose

This skill defines the **abstract pattern** for iteratively refining
LLM-produced artifacts against a declared quality bar. The pattern has
four invariants:

1. A **drafter** LLM produces a candidate artifact from a job spec + prior
   iteration feedback.
2. A **critic** scores the candidate against criteria. The critic is a
   hybrid: deterministic mechanical checks where possible, LLM-as-judge
   for the rest.
3. An **orchestrator** loops drafter → render → critic → feedback until
   the critic returns zero failures or detects a stuck state.
4. An optional **HUD** overlays loop state on the rendered artifact so
   the user can intervene (continue, abort, give guidance).

The pattern is artifact-agnostic. HTML, code, schemas, prose, JSON, SVG
— any output that can be judged against rules fits.

## What this skill provides

- `references/loop-protocol.md` — the iterate-until-pass cycle, stuck
  detection, audit-summary format, cost tracking
- `references/drafter-contract.md` — abstract drafter interface (inputs,
  outputs, behavior rules)
- `references/validator-contract.md` — abstract hybrid-dispatch logic
  (mechanical-first, LLM-judge fallback)
- `references/hud-protocol.md` — browser-injected loop state overlay
- `references/audit-summary-format.md` — final-iteration emit shape
- `scripts/hud.js` — vanilla-JS HUD implementation (browser artifacts)

## What this skill does NOT provide

- Artifact-specific drafter rules (e.g., "use semantic HTML") — those
  live in the consumer skill
- Mechanical check implementations — those depend on the artifact
  format and live in the consumer
- Output style guides — same
- Themes, templates, palettes — same

## Consumer pattern

A consumer skill (e.g., `component-composer`):

1. Declares this skill as a logical dependency in its README/SKILL.md
2. Implements artifact-specific drafter-protocol.md that references
   `generator-critic/references/drafter-contract.md` for the abstract
   interface
3. Implements artifact-specific validator-protocol.md that references
   `generator-critic/references/validator-contract.md` for dispatch logic
4. Provides concrete mechanical-check implementations (if any) in its
   own scripts
5. Reuses `loop-protocol.md`, `hud-protocol.md`, and `hud.js` directly

The consumer narrows the abstract contracts; the loop pattern is shared.

## When to use this skill directly

You're designing a new `<artifact-type>-composer` skill and need the
refinement-loop machinery. Read these references in order:

1. `loop-protocol.md` — understand the cycle
2. `drafter-contract.md` — design your concrete drafter
3. `validator-contract.md` — design your concrete validator
4. `hud-protocol.md` + `audit-summary-format.md` — wire up overlay + emit

## When NOT to use

- Casual one-off artifacts that don't need a validator gate (Thariq
  Shihipar's "Unreasonable Effectiveness of HTML" pattern — just ask
  Claude directly; see the `html-sketch` skill for casual HTML patterns)
- One-shot generation where no iteration is expected
- Workflows where the critic is a human reviewer, not an LLM or
  mechanical check
