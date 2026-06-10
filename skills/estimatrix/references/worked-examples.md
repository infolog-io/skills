# Worked examples (K1-K8)

Each example maps to a test case in TESTS.md. Size ranges of two adjacent
sizes appear ONLY when a named blank causes the spread, per the output
format in SKILL.md.

## K1 — Ambiguity (rule 1, active intake)

User: "estimate adding a feature flag"

Skill (turn 1): Before sizing, two things to nail down. Which flag system?

  A. GrowthBook (already in the codebase)
  B. LaunchDarkly
  C. A custom toggle in env vars
  D. Other — name it

(Once you pick, I'll ask about the feature being gated.)

[Intake continues until scope + success criterion are filled, then emits estimate.]

## K2 — Multiple interpretations (rule 1)

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

## K3 — Simpler alternative (rule 2)

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

## K4 — Missing success criterion (rule 4, active intake)

User: "estimate fixing the bug"

Skill (turn 1): Which bug, and what does "fixed" look like?

  Quick triage:
  1. Is there a failing test, error log, or reproduction case I can anchor to?
  2. What's the observed (broken) behavior, in one sentence?
  3. What's the expected (fixed) behavior, in one sentence?

Once those three are filled, I can size.

## K5 — Surgical scope (rule 3)

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

## K6 — Small task, high complexity

User: "estimate fixing the intermittent race condition in checkout"

Skill response:

```
Assumptions:
- Race happens between order-write and inventory-decrement
- Reproduction is intermittent (already observed)

Success criterion:
- A deterministic test reproduces the race, then passes after the fix

Size: XS-S (range caused by a named blank: no reproduction in hand yet)
Complexity: high
Confidence: medium (until reproduction is in hand)
```

Small change in code, high uncertainty in diagnosis.

## K7 — Large task, low complexity

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
without changing complexity. If the call-site count is unknown, emit
`Size: M-L` and name the count as the blank causing the range.

## K8 — XXL decomposition

User: "estimate the auth rewrite"

Skill response:

```
Initial sizing: XL-XXL (range caused by a named blank: final scope of the
rewrite is undefined until decomposed)

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

## Question style

| Do | Don't |
|---|---|
| Ask one focused question per turn, or a tight numbered list of 2-4 | Dump a bullet list of 8 questions |
| Quote the user's exact phrase when probing ambiguity | Paraphrase in ways that drift from intent |
| Offer 2-4 concrete options when scope is open | Ask open-ended "what do you want?" |
| Confirm understanding back to the user before sizing | Estimate against assumptions the user never confirmed |

## Single-turn happy path

If the user's request already states scope AND success criterion AND has
no ambiguity, skip intake. Emit the estimate directly.

A request is "happy path" when:
- The action verb is unambiguous (rename, add, replace, delete, integrate)
- The object is specified (which function, which page, which API)
- The outcome is testable (grep returns 0, all tests pass, X renders Y)

## Calibration

Re-calibrate when:

- An XS-sized, low-complexity task takes a full session → re-classify; either size was wrong or complexity was higher than estimated
- An L task lands in two messages → demote; L was wrong
- A pattern of "small but complex" tasks accumulates → complexity is the binding constraint, not size
