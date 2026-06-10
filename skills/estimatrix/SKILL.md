---
name: estimatrix
description: >-
  Use when the user asks for an estimate, sizing, or scoping call —
  "estimate", "how long", "how much effort", "size this", "scope this",
  "/estimatrix" — when you are about to state a time-based or effort
  estimate yourself, or when a proposal, plan, or task table contains an
  effort, time, duration, hours, or complexity column. Not for wall-clock
  scheduling ("meet at 3pm") or runtime/SLO measurements.
---

# Estimatrix

**Effort is a T-shirt size. Complexity is low / medium / high. Never
hours.** A task can be small but complex (subtle race-condition fix) or
large but simple (mechanical 200-file rename); one number loses the signal.

## Axis 1 — Size (effort)

| Size | Effort | Touch points |
|---|---|---|
| **XS** | Trivial | One decision, one file |
| **S** | Localized | One component, one prompt, one config |
| **M** | Multi-file | Some integration; touches a small system |
| **L** | Cross-cutting | Multiple systems; coordination required |
| **XL** | Major | Architecture decisions required |
| **XXL** | Epic | Sequence of L+ chunks |

XXL is a decomposition signal, not a final size — break into L-or-smaller
pieces first.

## Axis 2 — Complexity (cognitive load)

| Complexity | Definition | Examples |
|---|---|---|
| **low** | Mechanical, predictable | Mass rename; literal→token swap |
| **medium** | Some thinking; mostly known | Extract a hook; documented API migration |
| **high** | Real uncertainty; exploration; multiple approaches | Intermittent race; new architecture |

## Karpathy's four rules — satisfy before sizing

- **Think before coding** — state assumptions; ambiguous → intake; multiple readings → separate sizings.
- **Simplicity first** — propose and size the smaller scope that meets the goal.
- **Surgical changes** — size only what was asked; adjacent work = own row.
- **Goal-driven execution** — no size without a verifiable success criterion.

## Active intake

Underspecified task? Drive the conversation: ONE focused question per
turn, 2-4 concrete options, loop. Full multi-turn run:
[references/intake-example.md](references/intake-example.md).

Blank checklist, priority-ordered — each unfilled blank becomes a question:

1. **Scope** — in/out boundary of "done" *(material)*
2. **Success criterion** — test or observable output *(material)*
3. **Simpler alternative** — smaller scope, same goal?
4. **Constraints** — deadline, perf, compat, security
5. **Dependencies** — APIs, teams, sequencing
6. **Adjacent work** — ask last; separate row
7. **Complexity inputs** — known/unknown ratio; familiar or novel
8. **Calibration anchor** — comparable past work

**Material** = items 1-2; mandatory before a confident size. Items 3-8
are best-effort — unfilled ones fold into Confidence.

Stop asking when material blanks are filled or the user says "just give
me a rough size." Skip intake when the request already has an unambiguous
verb, a named object, and a testable outcome.

## Output format

```
Task: <verbatim phrasing>
Assumptions: <bullets>
Interpretations (if ambiguous): <each sized separately>
Simpler alternative (if applicable): <scope> → Size, Complexity
Success criterion: <verifiable test, behavior, or output>
Size: <XS|S|M|L|XL|XXL>
Complexity: <low|medium|high>
Confidence: <high|medium|low>
```

Size may span two ADJACENT sizes (`XS-S`) ONLY when a named blank causes
the spread — name it beside the range.

Confidence rubric:
- **high** — no material blanks remain
- **medium** — one stated assumption pending
- **low** — material blanks remain

| Task | Size | Complexity |
|---|---|---|
| Replace literals with token refs | M | low |
| Investigate the flaky test | XS | high |
| Migrate auth across 200 files | XL | medium |

Worked examples K1-K8 and calibration:
[references/worked-examples.md](references/worked-examples.md).

## Common mistakes

- Never dump a checklist and stop — ask one question with 2-4 options.
- On "just give me a rough size": emit Size + Complexity, `Confidence: low`, and list the remaining blanks.

## When to apply

- Yes: effort/time/duration/hours/complexity columns, "how long" questions, sprint planning → Size + Complexity.
- No: wall-clock scheduling ("meet at 3pm"); runtime/SLO measurements.

Need calendar time anyway? Give Size + Complexity first; convert only if
the user insists, labeled as their conversion, not the skill's.
