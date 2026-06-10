# claude-pip

A Performance Improvement Plan for Claude. Five triggers cover a rule's
lifecycle: capture, scope, remove, audit, graduate.

## Triggers

| Trigger | What |
|---|---|
| `CLAUDE PIP` | Add a master rule to `<project>/.claude/CLAUDE-PIP.md` |
| `LOCAL PIP` | Add a rule scoped to the current directory's `CLAUDE.md` |
| `OFF THE PIP` | Remove a rule by ID or keyword |
| `PRUNE THE PIP` | Audit rules for staleness; default verdict is keep |
| `PROMOTE THE PIP` | Graduate stable rules to CLAUDE.md / DESIGN.md / user-global — you pick which |

Triggers are case-sensitive, all-caps. Asking to "audit the PIP" or
"graduate a PIP rule" also activates the skill.

## Why

Memory and preferences are not enforced; rules in `CLAUDE.md` are. This
skill turns a one-off correction into a permanent rule that fires every
time — removable, prunable, promotable later.

## How it works

Every rule is wrapped in HTML-comment markers
(`<!-- pip:start id=<id> -->` ... `<!-- pip:end id=<id> -->`) so it can
be removed mechanically. Prune never drops without approval; promote
never proposes — it lists, you pick.

## Install

```bash
claude plugin marketplace add infolog-io/skills
claude plugin install claude-pip@infolog-io
```
