# generator-critic — Tests

## End conditions

- A consumer skill can build a working refinement pipeline by reading only the four references (loop-protocol, drafter-contract, validator-contract, hud-protocol) plus this skill's SKILL.md.
- `component-composer` (the first consumer) builds correctly on top of this skill — its drafter-protocol.md and validator-protocol.md reference these contracts and the rest of the loop machinery is inherited.

## Test cases

### TC1 — Consumer can sketch a new composer from scratch

Given: a developer wants to build `markdown-composer`.
When: they read this skill's SKILL.md + the 5 references.
Then: they can identify which abstract contracts to satisfy (drafter-contract, validator-contract) and which mechanics they inherit unchanged (loop-protocol, hud-protocol, audit-summary-format).

### TC2 — The loop converges

Given: a consumer skill with a working drafter, mechanical checks, LLM-judge.
When: a draft fails one criterion and the drafter receives the failure list.
Then: iteration N+1 addresses the failure without introducing new failures (per drafter-contract behavior rules).

### TC3 — Stuck detection triggers user intervention

Given: two consecutive iterations produce the same failure set.
When: the loop detects stuck state.
Then: HUD shows "stuck" banner and the orchestrator prompts the user via AskUserQuestion (continue, abort, give guidance) per loop-protocol § "Stuck detection".

### TC4 — Final iteration emits audit summary

Given: a loop converges to zero failures.
When: the orchestrator emits.
Then: the audit summary matches the shape in `references/audit-summary-format.md` — theme, iterations, drafter calls, judge calls, mechanical runs, wallclock, resolved-during-loop list.
