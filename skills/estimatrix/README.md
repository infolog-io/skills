# estimatrix

Sizing rubric for **effort and complexity**. Two axes, never hours.

## The two rules

- **Effort** is a T-shirt size: XS / S / M / L / XL / XXL
- **Complexity** is low / medium / high

A task can be small but complex (race-condition fix). A task can be large
but simple (mechanical rename across 200 files). Collapsing the two loses
signal.

## Karpathy's four rules apply before sizing

1. **Think Before Coding** — state assumptions; refuse to size if ambiguous; list interpretations if multiple
2. **Simplicity First** — propose smaller scope if it satisfies the goal
3. **Surgical Changes** — size only what was asked, not adjacent improvements
4. **Goal-Driven Execution** — no size without a success criterion

## When it applies

Any "effort", "complexity", "duration", or "how long" question. Skip
wall-clock scheduling and runtime metrics — those are measurements, not
estimates.

## Install

```bash
claude plugin marketplace add infolog-io/skills
claude plugin install estimatrix@infolog-io
```

## Triggers

`estimate` · `scope` · `how long` · `effort` · `complexity` · `size this` · `/estimatrix`

Also activates automatically when a table column is named effort,
time, duration, hours, or complexity.
