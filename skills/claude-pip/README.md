# claude-pip

A Performance Improvement Plan for Claude. When you catch Claude skipping
a discipline (TDD, plan mode, sub-agents, adversarial review), type
`CLAUDE PIP` and the rule locks into the project's `CLAUDE.md` as a
deterministic guideline.

## Why

Memory and preferences are not enforced by the harness. Rules in
`CLAUDE.md` are. This skill turns a one-off correction into a permanent
rule that fires every time.

## When to use

- Right after Claude skips a discipline you expected
- When a behavior should hold for the rest of the project
- When the rule is durable across sessions and worth committing

## When not to use

- One-off scope decisions (use plan mode)
- Temporary preferences (use Claude memory)

## How it works

Type `CLAUDE PIP` (all caps). Optional detail follows: `CLAUDE PIP TDD`
infers the rule; `CLAUDE PIP always run X after Y` uses your exact
wording.

The skill writes to `<project>/.claude/CLAUDE-PIP.md` and imports it from
the project's root `CLAUDE.md` as the first line.

## Install

```bash
claude plugin marketplace add infolog-io/skills
claude plugin install claude-pip@infolog-io
```

## Triggers

`CLAUDE PIP` (all caps, anywhere in a message)
