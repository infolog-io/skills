---
name: estimatrix
description: >
  Sizing rubric for effort and complexity. Use whenever a proposal, plan,
  scoping table, or task list contains an "effort" or "complexity" column,
  or whenever the user or model is about to give a time-based estimate.
  Express size as T-shirt: XS / S / M / L / XL / XXL — never hours, never
  days. Activates on "estimate", "scope", "how long", "effort", "size this",
  "/estimatrix", or before any estimation table is produced.
---

# Estimatrix

## The rule

**All effort and complexity estimates use T-shirt sizes. Never hours. Never days.**

Hours and days anchor to assumptions the model cannot validate. T-shirt sizes
encode effort + complexity + uncertainty together and stay calibrated against
real work history.

## Sizes

| Size | Effort | Complexity | Unknowns |
|---|---|---|---|
| **XS** | Trivial | One decision, one file | None |
| **S** | Localized | One component, one prompt, one config | Few |
| **M** | Multi-file | Some integration; touches a small system | Some |
| **L** | Cross-cutting | Multiple systems; coordination required | Meaningful |
| **XL** | Major | Architecture decisions required | Many |
| **XXL** | Epic | Sequence of L+ chunks; needs decomposition | Dominates |

## When to apply

| Context | Apply? |
|---|---|
| Any proposal with an "effort" column | Yes |
| Any plan with a "time" or "duration" estimate | Yes — replace with T-shirt size |
| Any "how long will this take" question | Yes |
| Any commit-time effort note | Yes |
| Sprint planning, capacity discussions | Yes |
| Calendar scheduling (e.g., "meet at 3pm") | No — wall-clock time, not effort |
| Build pipeline runtime, SLO metrics | No — measurement, not estimate |

## How to size

1. **Compare against known work.** XS = "I've done this in this session." L = "this is the biggest thing I'd attempt without breaking it down."
2. **If the size is XXL, decompose.** XXL is a flag, not a size. Break into L or smaller pieces before proceeding.
3. **Account for uncertainty.** A "simple" task with many unknowns is at least M. Unknowns are work.
4. **Don't ladder up to look diligent.** XS work sized as M wastes capacity.

## Output format

In tables:

```markdown
| Phase | Size | Notes |
|---|---|---|
| Scaffold | XS | Plugin manifest + SKILL.md |
| Build references | M | Three reference files, one rubric |
| Build prompts | L | Four mode-specific prompts with worked examples |
```

In prose:

```
This is a M — multi-file, light integration, few unknowns.
```

## Anti-patterns

| Pattern | Fix |
|---|---|
| "About 6 hours" | "M" |
| "A few days" | "L" |
| "Quick — 30 minutes" | "XS" |
| "It's complicated" without sizing | Pick a size; add unknowns to reasoning |
| Same size across every row in a plan | Re-size; uniform sizing is usually wrong |
| XXL with no decomposition | Decompose first, then size the pieces |

## Calibration

Re-calibrate when:

- An XS task takes a full session — XS was wrong; promote next time
- An L task lands in two messages — L was wrong; demote next time
- A size keeps surprising you — your rubric drifted; restate it explicitly

## Triggers

`estimate` · `scope` · `how long` · `effort` · `size this` · `/estimatrix`

Also auto-applies whenever a table column is named "effort", "time",
"duration", or "hours" — convert the column.

## Anti-rule

**Do not** size in hours, days, or weeks. If the user explicitly asks for an
hour estimate, give the T-shirt size and (only if pressed) state that
hour-anchored estimates from a model are unreliable.
