---
name: estimatrix
description: >
  Sizing rubric for effort AND complexity. Use whenever a proposal, plan,
  scoping table, or task list contains an "effort", "duration", or
  "complexity" column, or whenever the user or model is about to give a
  time-based estimate. Two axes: Size as T-shirt (XS / S / M / L / XL /
  XXL) for effort; Complexity as low / medium / high for cognitive load.
  Applies Karpathy's four code rules before sizing: state assumptions,
  ask if ambiguous, prefer simpler scope, require a success criterion.
  Activates on "estimate", "scope", "how long", "effort", "complexity",
  "size this", "/estimatrix", or before any estimation table is produced.
---

# Estimatrix

## The two rules

**Effort is a T-shirt size. Complexity is low / medium / high. Never hours.**

A task can be small but complex (subtle bug fix). A task can be large but
simple (mechanical rename across 200 files). Collapsing the two into one
number loses the signal.

## Axis 1 — Size (effort)

| Size | Effort | Touch points | Unknowns about HOW MUCH |
|---|---|---|---|
| **XS** | Trivial | One decision, one file | None |
| **S** | Localized | One component, one prompt, one config | Few |
| **M** | Multi-file | Some integration; touches a small system | Some |
| **L** | Cross-cutting | Multiple systems; coordination required | Meaningful |
| **XL** | Major | Architecture decisions required | Many |
| **XXL** | Epic | Sequence of L+ chunks; needs decomposition | Dominates |

XXL is a decomposition signal, not a final size. Break into L-or-smaller
pieces before proceeding.

## Axis 2 — Complexity (cognitive load)

| Complexity | Definition | Examples |
|---|---|---|
| **low** | Mechanical, well-understood, predictable | Rename a function across many files; replace literals with token references |
| **medium** | Some thinking required, mostly known, some unknowns | Refactor a component to extract a hook; migrate from one well-documented API to another |
| **high** | Significant uncertainty, exploration needed, multiple valid approaches, or subtle behavior | Diagnose an intermittent race condition; design a new architecture; integrate against an undocumented system |

## Karpathy's four rules — applied before sizing

estimatrix does not emit a size until these four rules are satisfied.

### Rule 1 — Think Before Coding (no silent assumptions)

- State assumptions explicitly before sizing
- If the request is ambiguous, run the **Conversational Intake** below — do not just refuse and stop
- If multiple interpretations exist, list them with separate sizings; do not silently pick one

### Rule 2 — Simplicity First

- If a smaller scope satisfies the actual goal, propose it and size THAT
- Push back on speculative future-proofing folded into the estimate
- Do not size for hypothetical configurability the user did not request

### Rule 3 — Surgical Changes

- Size only what was asked for, not adjacent improvements
- If adjacent work is mentioned, it goes in a separate table row with its own size
- Do not roll cleanup into the primary task's size

### Rule 4 — Goal-Driven Execution (verifiable success)

- Do not size a task without a success criterion
- Transform vague requests: "fix the bug" → "write a test that reproduces it, then make it pass"
- For multi-step tasks, state the plan with verify steps before sizing the whole

## Conversational Intake (the main behavior)

When a task is underspecified, estimatrix runs an active intake — it asks
the user questions, ONE focused question at a time (or a tight numbered
list of 2-4), and loops until enough information exists to emit a
defensible estimate.

### Blank-Detection Checklist

Walk this list before sizing. Each unchecked blank becomes a question.

1. **Scope** (rule 1) — Is the boundary of "done" defined? What's in, what's out?
2. **Success criterion** (rule 4) — Is there a test, behavior, or observable output that confirms done?
3. **Simpler alternative** (rule 2) — Could a smaller scope satisfy the same goal?
4. **Adjacent work** (rule 3) — Is the user lumping in nearby improvements?
5. **Constraints** — Deadline, performance target, compatibility floor, security floor?
6. **Dependencies** — External APIs, other teams, sequencing with other work?
7. **Sizing inputs for complexity** — Known/unknown ratio? Familiar pattern or novel?
8. **Calibration anchor** — Comparable past work to anchor against?

A blank is "filled" when the user's answer is concrete enough to size against.

### Intake ordering

Ask blanks in this priority:

1. **Scope ambiguity** (rule 1) — without this, every other question is premature
2. **Success criterion** (rule 4) — without this, "done" is undefined
3. **Simpler alternative** (rule 2) — only after scope is known
4. **Constraints + dependencies** — affects complexity
5. **Adjacent work** (rule 3) — asked last, as a separate row

Stop asking when:
- All material blanks are filled, OR
- The user signals "just give me a rough size" — emit with `Confidence: low` and flag the remaining blanks

### Question style

| Do | Don't |
|---|---|
| Ask one focused question per turn, or a tight numbered list of 2-4 | Dump a bullet list of 8 questions |
| Quote the user's exact phrase when probing ambiguity | Paraphrase in ways that drift from intent |
| Offer 2-4 concrete options when scope is open | Ask open-ended "what do you want?" |
| Include a rough estimate range in every turn | Send questions without any sizing information |
| Confirm understanding before finalizing | Lock in a final size without user confirmation |

### Single-turn happy path

If the user's request already states scope AND success criterion AND has
no ambiguity, skip intake. Emit the estimate directly.

A request is "happy path" when:
- The action verb is unambiguous (rename, add, replace, delete, integrate)
- The object is specified (which function, which page, which API)
- The outcome is testable (grep returns 0, all tests pass, X renders Y)

### Multi-turn worked example

User: "estimate the dashboard work"

Skill (turn 1): I need to disambiguate scope before sizing. Which dashboard?

  A. The internal admin dashboard
  B. The customer-facing usage dashboard
  C. A new dashboard not yet built

Which?

User: "B"

Skill (turn 2): For the customer-facing usage dashboard, what's the scope?

  A. Add one new metric tile
  B. Redesign the layout
  C. Migrate from one charting library to another
  D. Rebuild from scratch

Which?

User: "A — adding a tile for monthly active sessions"

Skill (turn 3): Good — scope is clear. What's the success criterion?

  A. The tile renders the value pulled from the existing API
  B. Same as A, plus a sparkline of the last 12 weeks
  C. Same as B, plus drill-down to per-day data

Which?

User: "B"

Skill (turn 4): Any adjacent improvements you want sized at the same time?
For example, refactoring the existing tile component or updating the
analytics pipeline that feeds it?

User: "no, just the tile"

Skill (final):

```
Task: Add a monthly-active-sessions tile with 12-week sparkline to the customer-facing usage dashboard

Assumptions:
- The existing API exposes the metric (no new endpoint needed)
- The dashboard's tile component pattern accepts a sparkline addition
- 12-week data is already retained

Success criterion:
- Tile renders the current MAS value
- Sparkline shows the last 12 weekly data points
- Tile passes the existing dashboard tile tests

Size: S
Complexity: low
Confidence: medium (pending confirmation that the API exposes the metric)
```

### Stop-asking signal

### Every turn carries an estimate

Never send a turn with ONLY questions — always include a rough estimate
alongside any clarifying questions. This applies to every intake turn.

For canonical patterns (debugging, rewrite, migration, integration), size the
pattern itself even when details are sparse:

```
Rough estimate (pending your answers):
- Size: M–L (debugging tasks with no repro typically land here)
- Complexity: high (intermittent issues require exploration)
- Confidence: low

To tighten this, I need to know:
1. [focused question]
```

Canonical pattern defaults:
- **Race condition / intermittent bug, no repro**: XS–M size, high complexity
- **Major rewrite (auth, payments, data layer)**: L–XXL size, high complexity
- **Migration to documented system**: M–L size, medium complexity

Confidence is `low` because blanks remain — that's honest, not a hedge. As
blanks fill, the range narrows and confidence rises.

## Output format

```
Task: <verbatim user phrasing>

Assumptions (rule 1):
- <assumption 1>
- <assumption 2>

Interpretations (rule 1, only if ambiguous):
- A: <interpretation> → Size: <X>, Complexity: <Y>
- B: <interpretation> → Size: <X>, Complexity: <Y>

Simpler alternative (rule 2, only if applicable):
- <smaller scope> → Size: <X>, Complexity: <Y>

Success criterion (rule 4):
- <verifiable test, behavior, or output>

Final estimate:
- Size: <XS | S | M | L | XL | XXL>
- Complexity: <low | medium | high>
- Confidence: <high | medium | low>
```

For tables:

```markdown
| Task | Size | Complexity |
|---|---|---|
| Replace literals with token refs | M | low |
| Investigate the flaky test | XS | high |
| Migrate auth across 200 files | XL | medium |
```

## Worked examples

Eight canonical scenarios live in `references/worked-examples.md`:

| # | Scenario | Lesson |
|---|---|---|
| K1 | Ambiguity (rule 1) | Active intake; one focused question |
| K2 | Multiple interpretations | List sized interpretations, ask which |
| K3 | Simpler alternative (rule 2) | Offer smaller scope alongside asked scope |
| K4 | Missing success criterion (rule 4) | Quick triage of three blanks |
| K5 | Surgical scope (rule 3) | Adjacent work goes in a separate row |
| K6 | Small task, high complexity | XS-S size, high cognitive load |
| K7 | Large task, low complexity | M-L size, mechanical work |
| K8 | XXL decomposition | Break into L-or-smaller phases before sizing |

Load the reference when a scenario maps cleanly to one of these.

## When to apply

| Context | Apply? |
|---|---|
| Any proposal with an "effort" column | Yes — fill with Size; add Complexity column |
| Any plan with "time" or "duration" estimate | Yes — replace with Size; add Complexity |
| Any "how long" question | Yes |
| Any commit-time effort note | Yes |
| Sprint planning, capacity discussions | Yes |
| Calendar scheduling ("meet at 3pm") | No — wall-clock time, not effort |
| Build pipeline runtime, SLO metrics | No — measurement, not estimate |

## Calibration

Re-calibrate when:

- An XS-sized, low-complexity task takes a full session → re-classify; either size was wrong or complexity was higher than estimated
- An L task lands in two messages → demote; L was wrong
- A pattern of "small but complex" tasks accumulates → complexity is the binding constraint, not size

## Anti-rule

**Do not** size effort in hours, days, or weeks. **Do not** collapse
complexity into the size dimension. **Do not** emit a size for a task
without first satisfying Karpathy's four rules.

If the user explicitly asks for hours, give the T-shirt size and complexity
and (only if pressed) state that hour-anchored estimates from a model are
unreliable.

## Triggers

`estimate` · `scope` · `how long` · `effort` · `complexity` · `size this` · `/estimatrix`

Also auto-applies whenever a table column is named "effort", "time",
"duration", "hours", or "complexity" — convert the column.
