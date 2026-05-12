# estimatrix — Tests & End Conditions

## Profile

**Single-rule skill.** Two durable rules:
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

### K1 — Ambiguity refusal (rule 1: Think Before Coding)

- Input: "estimate adding a feature flag"
- Expected: skill refuses to emit a size; asks clarifying questions about which flag system, scope, use case, and rollout target
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
- Expected: skill refuses to size; asks for the failing test, observed behavior, or expected post-fix state
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

## Acceptance rubric per artifact

| Artifact | Must |
|---|---|
| SKILL.md | States both axes; lists Karpathy's four rules; shows worked examples for K1-K8 and K11-K12; states anti-rules |
| README.md | Mentions both axes; ≤200 words; states triggers |

## Out of scope for v0.2.0

- Hour-to-size conversion lookup
- 4-tier complexity scale (low/medium/high is sufficient; finer granularity adds noise)
- Calibration history database (would belong in mrkrabs)
- Multi-rater Delphi sizing
- Python script to compute complexity from description (skill stays prompt-only)
- Cross-skill sizing aggregation
- Recalibration of already-completed work
