---
id: "001"
name: "a0-power-eval-sets"
repo: "/Users/informationlogistics/Developer/infolog-skills"
date: "2026-07-26"
status: BLOCKED
wargamer: "Opus 5, maximum effort, recon read-only"
executor: "Sonnet via build-loop-claude-code"
---

# Mission 001: A0 — power the eval sets

## Context

SkillOpt has run ten scored optimizations between 2026-05-27 and 2026-06-15 for
about $34. Zero accepted epochs. Six of ten produced a Δval of exactly +0.000.
`docs/skill-audit-plan.md` traces the cause to eval-set size, not to the skills:
`lib/gate.py` needs a +0.02 mean gain on a val split of three to five tasks,
where one task moving swamps the threshold. Phase A0 of that plan measures the
val-split spread so the required task count can be computed instead of guessed.
Nothing else in the plan runs until this returns a number.

## The mission

Measure the run-to-run spread of the `semantic-organization` val split under an
unchanged skill, and report the val-set size needed to detect a +0.02 effect.

When this mission is done:

- Five completed `eval --split val` runs against an unedited
  `skills/semantic-organization/SKILL.md` exist, each with its stdout captured
  to a file under `tools/skillopt/runs/semantic-organization/a0-variance/`.
- Every run is classified valid or void. A run is void when any task scored 0.0
  with a rationale beginning `rollout failed:`. Void runs are recorded and
  replaced, never averaged.
- The five valid val means, their standard deviation, and their full range are
  recorded in `tools/skillopt/SCORES.md` under the Eval log.
- A required-n figure is computed from the observed standard deviation and
  written into `SCORES.md` with the formula used and its inputs.
- A one-line verdict states whether the observed spread is smaller than
  `accept_delta` of 0.02. That is A0's pass condition from the plan.
- `adapters/estimatrix.py` is retired from the registry, with the reason
  recorded in `SCORES.md`.

Amended 2026-07-26, before execution, after wargame v1 recon. The original
brief listed the `adapters/spraypixel.py` repoint as a done-condition on the
plan's description of it as one cleanup. Recon measured 20 live references, and
17 of them sit inside judge-prompt and frozen-criteria strings that SUCCESS
extension 12 protects. Repointing them in the same run as a measurement mixes
an edit to a graded artifact with a graded measurement. The repoint moves whole
to mission 002 and is no longer a done-condition here.

Explicitly OUT of scope:

- Authoring new eval tasks. A0 reports the required n; raising the val split to
  that number is a later mission.
- Any edit to `skills/semantic-organization/SKILL.md`. The measurement depends
  on the skill being unchanged across all five runs.
- Any edit to task definitions, `expected_pattern` rubrics, or judge prompts.
- Repairing the `estimatrix` grader. The decision is to retire, not to fix.
- Running `optimize` or `sweep`. A0 makes no edits and tests no framework.
- Repointing `adapters/spraypixel.py`. Deferred whole to mission 002.

## Materials

- `docs/skill-audit-plan.md` — the plan this mission implements; phase A0.
- `tools/skillopt/harness.py` — `_eval` prints results and persists nothing.
- `tools/skillopt/lib/rollout.py` — `run_batch` and `_bounded`; the exception
  path that turns a failed rollout into a 0.0 score.
- `tools/skillopt/lib/budget.py` — `BudgetExceeded` subclasses `RuntimeError`.
- `tools/skillopt/lib/gate.py` — `accept_delta` 0.02, the effect being powered for.
- `tools/skillopt/adapters/semantic_organization.py` — 9 train / 5 val / 3 test.
- `tools/skillopt/SCORES.md` — the experiment record and its Eval log format.
- `SUCCESS.md` — extensions 11 through 14 bite hardest here.

## Constraints

- SUCCESS.md 11: every Python command runs through `tools/skillopt/.venv/bin/python`.
- SUCCESS.md 12: adapters, rubrics, and judge prompts are read-only in this mission.
- SUCCESS.md 13: the verdict cites the five runs by date, command, mean, and cost.
- SUCCESS.md 14: `--max-cost-usd` is passed explicitly on every run.
- Total spend ceiling for this mission: $12. At the ceiling, stop and hand back.
- Out of scope: everything in the mission's OUT list above.

## Verification

- Five valid run logs exist and each names five scored tasks.
- No valid run contains the string `rollout failed:`.
- `skills/semantic-organization/SKILL.md` is byte-identical before and after.
- The harness unit tests pass.
- The marketplace integrity check passes.
- Repo standard: every verification-command point in SUCCESS.md applies.

## Routing

- Wargamer: Opus 5, maximum effort, recon read-only
- Executor: Sonnet via build-loop-claude-code; alternate: Codex CLI via HANDOFF-CODEX
- Grader: fresh subagent, no authoring context
- Red-team: fresh subagent, executor roleplay
