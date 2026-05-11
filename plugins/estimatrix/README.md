# estimatrix

Effort and complexity sizing rule. Express estimates as T-shirt sizes
(**XS / S / M / L / XL / XXL**) — never as hours, never as days.

## Why

Hour estimates from LLMs anchor to training-data assumptions that rarely match
the user's actual work pace. T-shirt sizes encode effort, complexity, and
uncertainty together and stay calibrated against real history.

## Sizes

| Size | What it means |
|---|---|
| XS | Trivial — one decision, one file, no unknowns |
| S | Localized — one component or one prompt |
| M | Multi-file feature, light integration, some unknowns |
| L | Cross-cutting change, multiple systems |
| XL | Major work requiring architecture decisions |
| XXL | Epic — decompose before sizing |

## When it applies

Any "effort", "duration", "how long", or scoping question. Skip it for
wall-clock scheduling, runtime metrics, or SLO measurements.

## Install

```bash
claude plugin marketplace add infolog-io/skills
claude plugin install estimatrix@infolog-io
```

## Triggers

`estimate` · `scope` · `how long` · `effort` · `size this` · `/estimatrix`

Also activates automatically when a table column is named effort, time,
duration, or hours.
