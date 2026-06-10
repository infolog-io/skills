# estimatrix — Tests & End Conditions

## Profile

**Full-shape skill.** Compact SKILL.md body (axes, rules, intake, output
contract) plus `references/` (worked examples K1-K8, multi-turn intake
example). Two durable rules:
1. Effort sized as T-shirt (XS / S / M / L / XL / XXL), never hours
2. Complexity sized separately (low / medium / high)

Karpathy's four code rules apply before any size emits.

## End conditions (skill ships when all are true)

1. Plugin installs cleanly via `claude plugin install estimatrix@infolog-io`
2. Skill activates on every trigger phrase listed in SKILL.md
3. SKILL.md states the six T-shirt sizes with definitions
4. SKILL.md states the three complexity levels with definitions
5. SKILL.md applies Karpathy's four rules to estimation: assumptions, simplicity, surgical scope, goal-driven success criteria
6. SKILL.md states the anti-rule (no hours, no days, no weeks)
7. README ≤200 words

## Test cases — Karpathy rules

### K1 — Ambiguity intake (rule 1: Think Before Coding)

- Input: "estimate adding a feature flag"
- Expected: skill withholds the size and runs active intake (one focused question with 2–4 options) about which flag system, scope, use case, and rollout target
- Negative: skill does not guess "M" and move on

### K2 — Multiple interpretations (rule 1)

- Input: "estimate refactoring the auth code" with ambiguous scope
- Expected: skill emits an interpretations table with size + complexity for each plausible scope (e.g., A: rename a function = `Size: XS, Complexity: low`; B: replace JWT with sessions = `Size: L, Complexity: high`)
- Negative: skill does not silently pick one interpretation

### K3 — Simpler alternative (rule 2: Simplicity First)

- Input: "estimate adding 'enterprise SSO' to login"
- Expected: skill sizes the asked scope AND proposes a simpler alternative (start with one IdP) with its own sizing
- Negative: skill does not just size the maximalist scope without questioning

### K4 — Missing success criterion (rule 4: Goal-Driven Execution)

- Input: "estimate fixing the bug" with no test, behavior, or expected outcome
- Expected: skill withholds the size and runs active intake (one focused question with 2–4 options) for the failing test, observed behavior, or expected post-fix state
- Negative: skill does not size a vague "fix" task

### K5 — Surgical scope (rule 3: Surgical Changes)

- Input: "estimate adding a button to the login form" — context mentions adjacent cleanup opportunities
- Expected: skill sizes ONLY the asked work; if adjacent improvements are mentioned, they go in separate table rows with their own sizing
- Negative: skill does not roll adjacent work into the primary size

## Test cases — sizing accuracy

### K5b — Hour estimate rejection
- Input: "This will take about 6 hours"
- Expected: skill rejects hour anchor; restates as `Size: M, Complexity: <inferred from task>`

### K6 — Small task, high complexity
- Input: "estimate fixing the intermittent race condition in checkout"
- Expected: `Size: XS-S, Complexity: high`
- Why: small code change, but uncertainty + reproduction difficulty makes complexity high

### K7 — Large task, low complexity
- Input: "estimate renaming `getUserData` to `fetchUser` across the codebase"
- Expected: `Size: M-L (depending on usage count), Complexity: low`
- Why: mechanical work, well-understood, no architectural decisions

### K8 — XXL trigger (rule per existing rubric)

- Input: "estimate rewriting auth across 200 files"
- Expected: `Size: XL, Complexity: high`; skill flags XXL is a decomposition signal if scope grows; proposes phasing
- Negative: skill does not emit XXL without recommending decomposition

## Test cases — column conversion (existing behavior preserved)

### K9 — Scoping table column conversion
- Input: a table with a column named "Effort", "Duration", or "Hours"
- Expected: skill auto-applies; column filled with T-shirt sizes; a Complexity column is offered as an addition

### K10 — Wall-clock anti-rule
- Input: "Let's meet at 3pm" or "Build runtime is 90 seconds"
- Expected: skill does NOT convert; these are wall-clock or measurement, not effort estimates

## Test cases — output format

### K11 — Full output shape
- Input: any non-ambiguous task with a clear success criterion
- Expected output structure:

```
Task: <verbatim phrasing>

Assumptions stated:
- <assumption 1>
- <assumption 2>

Success criterion:
- <verifiable test, behavior, or output>

Size: <XS-XXL>
Complexity: <low | medium | high>
Confidence: <high | medium | low>
```

### K12 — Decomposition output for XXL

- Input: a task that sizes to XXL
- Expected: skill flags XXL as a decomposition signal, then breaks into L-or-smaller pieces, each with its own size + complexity

## Test cases — conversational intake (the main behavior)

### K13 — Active question-asking, not passive refusal

- Input: any ambiguous or underspecified task (e.g., "estimate the dashboard work")
- Expected: skill runs an active intake interview:
  1. Identifies which blanks must be filled (scope, success criterion, dependencies, constraints)
  2. Asks ONE focused question at a time (or a tight numbered list of 2-4)
  3. Waits for the user's answer
  4. Updates its understanding
  5. Asks the next blank
  6. Loops until enough info exists to size
  7. Emits Size + Complexity + Confidence
- Negative: skill does NOT just list "I need to know X, Y, Z" and stop. It must run the back-and-forth.

### K14 — Blank-detection ordering

- Input: a task where multiple blanks exist (e.g., scope is clear but success criterion is missing AND adjacent cleanup is mentioned)
- Expected: skill asks about the highest-leverage blank first:
  - Missing success criterion (rule 4) before complexity-affecting blanks
  - Scope ambiguity (rule 1) before adjacent-work questions (rule 3)
  - Adjacent work (rule 3) is asked LAST as a separate row, not folded in
- Negative: skill does not ask about every blank in random order

### K15 — Stop-asking signal

- Input: user, after one or two clarifications, says "just give me a rough size"
- Expected: skill emits size + complexity with what it knows; flags `Confidence: low` and states the remaining blanks
- Negative: skill does not keep asking questions when user has signaled they want a rough answer

### K16 — Single-turn happy path

- Input: a task that is fully specified ("rename `getUserData` to `fetchUser` across our 80-file Next.js app; success = all tests pass and grep returns 0 hits for the old name")
- Expected: skill skips the conversational intake; emits estimate in one response
- Negative: skill does not ask unnecessary questions when the request already states scope + success criterion

## Acceptance rubric per artifact

| Artifact | Must |
|---|---|
| SKILL.md | States both axes (tables inline); four Karpathy rules; intake with priority-ordered blank checklist; output contract with adjacent-size-range rule and Confidence rubric; ≈500-word body |
| references/worked-examples.md | Worked examples K1-K8 plus question style, happy path, calibration |
| references/intake-example.md | Multi-turn intake example, refusal anti-pattern, stop-asking signal (K11-K15 shapes) |
| README.md | Mentions both axes; ≤200 words; states triggers |

## Out of scope for v0.3.0

- Hour-to-size conversion lookup
- 4-tier complexity scale (low/medium/high is sufficient; finer granularity adds noise)
- Calibration history database (belongs in a future telemetry skill, not estimatrix)
- Multi-rater Delphi sizing
- Python script to compute complexity from description (skill stays prompt-only)
- Cross-skill sizing aggregation
- Recalibration of already-completed work
