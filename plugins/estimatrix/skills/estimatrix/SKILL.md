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
- If the request is ambiguous, refuse to size; ask
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

### K1 — Ambiguity (rule 1 refusal)

User: "estimate adding a feature flag"

Skill response: refuses to size; asks:
- Which flag system (GrowthBook, LaunchDarkly, custom)?
- Which feature does the flag gate?
- Server-side, client-side, or both?
- Targeting rules: user attributes, percentage rollout, both?

No size emits until clarified.

### K2 — Multiple interpretations (rule 1)

User: "estimate refactoring the auth code"

Skill response:

```
Interpretations:
- A: Rename auth helper functions for clarity
  → Size: XS, Complexity: low
- B: Move auth logic from middleware into a service module
  → Size: M, Complexity: medium
- C: Replace JWT-based auth with session-based
  → Size: L, Complexity: high
- D: Migrate from custom auth to a managed identity provider
  → Size: XL, Complexity: high

Which scope?
```

### K3 — Simpler alternative (rule 2)

User: "estimate adding 'enterprise SSO' to login"

Skill response:

```
Asked scope: Support SAML, OIDC, and Microsoft Entra
- Size: XL, Complexity: high

Simpler alternative (rule 2):
- Start with one IdP (most-requested by current customers)
- Size: M, Complexity: medium
- Ship MVP; add other IdPs as inbound demand justifies

Which scope?
```

### K4 — Missing success criterion (rule 4 refusal)

User: "estimate fixing the bug"

Skill response: refuses to size; asks:
- What is the failing test or reproduction case?
- What is the observed (broken) behavior?
- What is the expected (fixed) behavior?

No size emits without a success criterion.

### K5 — Surgical scope (rule 3)

User: "estimate adding a button to the login form. Also the form has some old margin hacks we should clean up."

Skill response:

```
| Task | Size | Complexity |
|---|---|---|
| Add button to login form | XS | low |
| Clean up margin hacks (adjacent) | S | low |
```

Two rows, not one rolled-up size. The user can ship the button without
the cleanup.

### K6 — Small task, high complexity

User: "estimate fixing the intermittent race condition in checkout"

Skill response:

```
Assumptions:
- Race happens between order-write and inventory-decrement
- Reproduction is intermittent (already observed)

Success criterion:
- A deterministic test reproduces the race, then passes after the fix

Size: XS-S
Complexity: high
Confidence: medium (until reproduction is in hand)
```

Small change in code, high uncertainty in diagnosis.

### K7 — Large task, low complexity

User: "estimate renaming getUserData to fetchUser across the codebase"

Skill response:

```
Assumptions:
- The rename is global; no semantic change
- Tests cover the renamed function's behavior

Success criterion:
- All call sites use the new name; tests pass; no string-literal references remain

Size: M (assuming 50-200 call sites)
Complexity: low
Confidence: high
```

Mechanical, well-understood. If call-site count is 500+, bumps to L
without changing complexity.

### K8 — XXL decomposition

User: "estimate the auth rewrite"

Skill response:

```
Initial sizing: XL-XXL

XXL is a decomposition signal. Breaking down:

| Phase | Task | Size | Complexity |
|---|---|---|---|
| 1 | Define auth contract; document target API | M | medium |
| 2 | Build new auth service alongside existing | L | high |
| 3 | Shadow-write to new service; compare | M | medium |
| 4 | Cut over read traffic | L | medium |
| 5 | Cut over write traffic; remove old | L | medium |

Total: 5 phases, sized L-or-smaller. Sequencing per phase.
```

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
