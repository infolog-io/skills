# claude-pip

A Performance Improvement Plan for Claude. Three triggers lock, scope,
and remove deterministic rules in your project's CLAUDE.md.

## Triggers

| Trigger | What |
|---|---|
| `CLAUDE PIP` | Add a master rule to `<project>/.claude/CLAUDE-PIP.md` |
| `LOCAL PIP` | Add a rule scoped to the current directory's `CLAUDE.md` |
| `OFF THE PIP` | Remove a rule by ID or keyword |

All triggers are case-sensitive, all-caps.

## Why

Memory and preferences are not enforced. Rules in `CLAUDE.md` are. This
skill turns a one-off correction into a permanent rule that fires every
time — and lets you remove it cleanly when it no longer applies.

## How it works

Every rule the skill adds is wrapped in HTML-comment markers
(`<!-- pip:start id=<id> -->` ... `<!-- pip:end id=<id> -->`) so it can
be removed mechanically later. The ID is auto-generated.

- `CLAUDE PIP TDD` infers and writes the TDD rule
- `LOCAL PIP always lint before commit` scopes a rule to the current dir
- `OFF THE PIP <id>` removes that rule cleanly

## Install

```bash
claude plugin marketplace add infolog-io/skills
claude plugin install claude-pip@infolog-io
```
