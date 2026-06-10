# Active intake — full multi-turn example

Shows the conversational intake loop from SKILL.md: one focused question
per turn with 2-4 concrete options, looping until the material blanks
(scope + success criterion) are filled.

## Multi-turn worked example

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

## Refusal-style intake (anti-pattern)

Wrong:

> User: "estimate the dashboard work"
> Skill: "I cannot size this without knowing scope, success criterion, constraints, dependencies, and complexity inputs. Please provide:
> - Scope
> - Success criterion
> - Constraints
> - ...
> [end of response]"

This is passive. The user has to do all the work. estimatrix should
drive the conversation, not block on it.

Right:

> User: "estimate the dashboard work"
> Skill: [asks ONE focused question with concrete options]

## Stop-asking signal

If the user says "just give me a rough size" or similar after one or two
questions, emit the estimate with whatever information is in hand:

```
Size: M (best guess given what I know)
Complexity: medium
Confidence: low
Remaining blanks (would tighten this if filled):
- Which dashboard
- Whether to include adjacent refactor
```

Confidence is `low` because material blanks remain. That's an honest
signal, not a hedge.
