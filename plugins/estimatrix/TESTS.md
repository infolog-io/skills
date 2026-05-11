# estimatrix — Tests & End Conditions

## Profile

**Single-rule skill.** One durable rule: effort and complexity are
T-shirt sizes, never hours or days. SKILL.md carries the entire skill.

## End conditions (skill ships when all are true)

1. Plugin installs cleanly via `claude plugin install estimatrix@infolog-io`
2. Skill activates on every trigger phrase listed in SKILL.md
3. SKILL.md states the six T-shirt sizes (XS / S / M / L / XL / XXL) with definitions
4. SKILL.md states the anti-rule (no hours, no days, no weeks)
5. README ≤200 words

## Test cases

### T1 — Hour estimate rejection
- Input: "This will take about 6 hours"
- Expected: skill activates; converts to T-shirt size (likely M) with rationale citing complexity and unknowns

### T2 — "How long" question
- Input: "How long will this take?"
- Expected: skill activates; emits T-shirt size, not hours; references rubric

### T3 — Scoping table column conversion
- Input: a table with a column named "Effort" or "Duration" or "Hours"
- Expected: skill auto-applies; the column is filled with T-shirt sizes, not numeric durations

### T4 — XXL decomposition rule
- Input: a task sized XXL
- Expected: skill flags that XXL is a decomposition signal, not a final size; emits a breakdown plan into L-or-smaller pieces

### T5 — Anti-rule for wall-clock scheduling
- Input: "Let's meet at 3pm" or "Build runtime is 90 seconds"
- Expected: skill does NOT convert these — they are wall-clock or measurement, not estimates

### T6 — Calibration loop
- Input: a task previously sized M that the user reports took XS effort
- Expected: skill captures the calibration miss and recommends demoting similar tasks next time

## Acceptance rubric per artifact

| Artifact | Must |
|---|---|
| SKILL.md | Single durable rule; sizing rubric table; anti-rule; calibration guidance; trigger phrases |

## Out of scope for v1

- Hour-to-size conversion lookup (the user should re-estimate, not translate)
- Sprint planning integration
- Calibration history database (deferred to a `mrkrabs`-like tracker if needed)
- Multi-rater Delphi sizing (single-rater rubric only)
