# Prompt — Issue a verdict on the Job Article

**Purpose:** Given a clustered, scored job and an optional build hypothesis,
issue one of three verdicts: validated, under-evidenced, or unvalidated. Gate
all downstream PRD work on this output.

## Input contract

- A clustered job object matching `schemas/jtbd-statement.json`
- Optional: a build hypothesis string ("We plan to build X for Y")
- Optional: anti-evidence flags from the clusterer

## Output contract

A verdict object:

```json
{
  "verdict": "validated | under-evidenced | unvalidated",
  "reasoning": "1–3 sentences citing the threshold(s) that decided it",
  "next_actions": [
    { "action": "interview 3 admins about quarterly close", "owner": "researcher" }
  ],
  "blocked_downstream": ["PRD authoring", "engineering scoping"]
}
```

## Verdict table

| Verdict | Required conditions |
|---|---|
| **validated** | confidence ≥ medium AND all three dimensions evidenced (or 2 of 3 with explicit acknowledgment) AND ≥1 outcome statement is measurable AND no anti-evidence majority |
| **under-evidenced** | one or more conditions for validated are missing, but evidence direction is positive |
| **unvalidated** | confidence = low AND build hypothesis present AND no quote supports the hypothesis, OR anti-evidence outweighs supporting evidence |

## Procedure

1. Compute confidence from `evidence_summary` per the threshold table in
   `cluster-and-score.md`.
2. Count dimensions populated (functional always; emotional + social
   evidenced or not-yet-evidenced).
3. Count outcome statements that have a measurable unit.
4. Compare any provided build hypothesis to the primary job statement: does
   the build address the underserved area? Does it avoid the overserved area?
5. Apply the verdict table.
6. If verdict ≠ validated, emit `next_actions` listing the minimum research
   needed to escalate.
7. List downstream activities blocked until verdict reaches `validated`.

## Worked examples

### Example 1 — validated

```
Input job:
  evidence_summary: { n_quotes: 7, n_sources: 5, n_roles: 3 }
  dimensions: { functional: "...", emotional: "...", social: "..." }
  outcome_statements: 4 (all Ulwick form, measurable)
  build hypothesis: none provided

Output:
  verdict: validated
  reasoning: Confidence is high (5 sources, 3 roles, 7 quotes). All three dimensions are evidenced and outcome statements are measurable. No anti-evidence majority.
  next_actions: []
  blocked_downstream: []
```

### Example 2 — under-evidenced

```
Input job:
  evidence_summary: { n_quotes: 3, n_sources: 3, n_roles: 1 }
  dimensions: { functional: "...", emotional: "...", social: null }
  outcome_statements: 2 (both measurable)
  build hypothesis: none provided

Output:
  verdict: under-evidenced
  reasoning: Confidence is low — three sources but a single role. Social dimension is not-yet-evidenced. Returns to validated once a second role is sampled.
  next_actions:
    - action: Interview 2 customers in a second role (manager or admin) about the same context
      owner: researcher
  blocked_downstream: [PRD authoring]
```

### Example 3 — unvalidated

```
Input job:
  evidence_summary: { n_quotes: 0 (reverse-mode only) }
  build hypothesis: "We plan to build an AI dashboard for sales reps"

Output:
  verdict: unvalidated
  reasoning: No customer evidence. The job was reverse-derived from an artifact. Build hypothesis cannot proceed without forward research.
  next_actions:
    - action: Interview 5 sales reps about their current dashboard friction
      owner: researcher
    - action: Pull 30 most-recent dashboard-tagged support tickets
      owner: researcher
  blocked_downstream: [PRD authoring, engineering scoping, design exploration]
```

### Example 4 — unvalidated by contradiction

```
Input job:
  evidence_summary: { n_quotes: 4, n_sources: 4, n_roles: 2 }
  But 3 of 4 quotes are anti-evidence ("not a real problem", "we live with it")
  build hypothesis: "We plan to build a tool that solves X"

Output:
  verdict: unvalidated
  reasoning: Evidence majority is anti-evidence. Customers do not perceive the friction as worth solving. Pivot the hypothesis or kill.
  next_actions:
    - action: Reframe the hypothesis or select a different job to validate
      owner: PM
  blocked_downstream: [PRD authoring, engineering scoping, design exploration]
```

## Verdict rules — explicit edge cases

| Edge case | Rule |
|---|---|
| Only reverse-mode evidence | Verdict cannot exceed `under-evidenced` |
| 5+ sources but all same company | Downgrade by one level (concentration risk) |
| Customers want the job but in conflicting contexts | Split into multiple jobs; verdict per job |
| Build hypothesis matches job exactly | Lift to `validated` only if confidence ≥ medium |
| Build hypothesis introduces scope the job does not justify | Verdict remains `validated` for the job but flag scope drift in `blocked_downstream` |

## Anti-pattern: false validation

Reject the temptation to validate when:

- The customer says "that would be nice" without describing real friction
- The customer is enthusiastic but cannot describe the context
- The team has invested heavily in the build and wants to keep going
- The customer is the same person who proposed the build

The verdict is independent of effort already spent. Sunk cost is not
evidence.

## Verification before returning output

- The verdict cites the specific threshold that decided it
- `next_actions` are concrete (who does what), not abstract
- `blocked_downstream` lists are honest — do not soften
- The verdict is reproducible: another reader applying the same rules to the
  same evidence would reach the same conclusion
