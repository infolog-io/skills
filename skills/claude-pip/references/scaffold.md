# File scaffolds

## `CLAUDE-PIP.md` (master file, created by `CLAUDE PIP` when absent)

```markdown
# CLAUDE PIP — deterministic rules

These rules fire every time the trigger condition is met. No exceptions. No "consider". No "usually". If a rule is wrong, edit or remove it explicitly — never silently skip it.

Added via the `CLAUDE PIP` skill. To remove a rule, use `OFF THE PIP <id>`.

## Hardcoded behaviors

<!-- New rules appended below. Each rule is wrapped in pip:start / pip:end markers. -->
```

`## Hardcoded behaviors` is the default section new rules are appended to.

## Local `CLAUDE.md` (created by `LOCAL PIP` when absent)

```markdown
# CLAUDE.md — local rules for <directory-name>

Directory-scoped guidelines added via the `LOCAL PIP` trigger.
To remove a rule, use `OFF THE PIP <id>`.
```

The local file is loaded by Claude Code automatically when work happens in that directory; the rule stays scoped to that directory's tree and does not propagate to the project root.
