# /goal

Execute a paired goal-doc + implementation-plan via subagent-driven loops.

## Inputs

- A goal doc at `docs/superpowers/specs/YYYY-MM-DD-<name>-goal.md`
- An implementation plan at `docs/superpowers/plans/YYYY-MM-DD-<name>.md`

Both come from the superpowers brainstorming + writing-plans skills.

## What it does

Dispatches one subagent per plan task per `superpowers:subagent-driven-development`,
reviews between tasks, tracks progress against the goal's binary success criteria,
emits a completion report at the end.

## Usage

```text
/goal                    Find most recent goal doc; execute its paired plan
/goal <name>             Find goal doc matching <name>; execute its plan
resume the goal          Resume from prior ledger at docs/superpowers/goal-state.json
```

See `SKILL.md` for the full operating mode.
