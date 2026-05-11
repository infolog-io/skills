---
name: claude-pip
description: Performance Improvement Plan for Claude. Invoke by typing `CLAUDE PIP` (all caps) anywhere in a message. Captures a behavioral failure (forgot TDD, skipped plan mode, didn't use sub-agents, etc.) and writes a terse, deterministic rule into the project's `.claude/CLAUDE-PIP.md` so the behavior fires every time going forward.
---

# Claude PIP

A Performance Improvement Plan, for me. When the user catches me skipping a discipline I should have followed (TDD, planning, sub-agents, adversarial review, etc.) they type `CLAUDE PIP` and I lock that discipline in as a deterministic rule.

## Trigger

User types `CLAUDE PIP` (all caps) in any message. May be followed by a description of the rule to lock in:

- `CLAUDE PIP` → ask what behavior to capture
- `CLAUDE PIP TDD` → infer (write the TDD rule)
- `CLAUDE PIP always run pnpm test:locale-routing after locale changes` → use the user's wording

## Procedure

1. **Locate the rules file.** Resolve `<project-root>/.claude/CLAUDE-PIP.md` from the current working directory by walking up to the nearest `.claude/` directory's parent. If the file doesn't exist, create it.
2. **Locate the project CLAUDE.md** (`<project-root>/CLAUDE.md`). If it doesn't already import the rules file, add `@.claude/CLAUDE-PIP.md` as the FIRST non-comment line (before titles, before other imports).
3. **Write the rule** in the deterministic format below. Append to CLAUDE-PIP.md under the correct section. If a similar rule already exists, refine in place rather than duplicating.
4. **Confirm to the user** with the exact rule that was added and where.

## Rule format

Every rule fits one of two shapes:

**Trigger-action**:
```
- **{Action verb in imperative}** {object/scope}, {when the trigger fires}. {Optional one-line rationale.}
```

**Invariant**:
```
- **{NEVER|ALWAYS} {what}** {context}. {Optional why.}
```

Rules MUST be:
- One line. No paragraphs.
- Imperative voice. No "consider", "should", "might", "probably".
- Trigger-specific. "Before X" not "when appropriate".
- Self-contained. Don't reference internal jargon unless it's in the rule index.

## CLAUDE-PIP.md template

When the file doesn't exist yet, create it with this scaffold:

```markdown
# CLAUDE PIP — deterministic rules

These rules fire every time the trigger condition is met. No exceptions. No "consider". No "usually". If a rule is wrong, edit or remove it explicitly — never silently skip it.

Added via the `CLAUDE PIP` skill (`~/.claude/skills/claude-pip/SKILL.md`).

## Hardcoded behaviors

<!-- New rules appended below. Keep terse. -->
```

## Common rules — pre-vetted phrasing

When the user invokes `CLAUDE PIP <topic>`, prefer the phrasing here over inventing fresh wording. Consistent rules are easier to follow.

| Topic | Rule (copy verbatim) |
|---|---|
| **TDD** | **Write a failing test FIRST** for any user-visible behavior, before writing code. Confirm the test fails for the right reason (not "fetch error" or syntax). Only then write the minimum code to make it pass. |
| **Plan mode** | **Enter plan mode** for any task with 3+ steps or any architectural decision. No exploratory coding without a plan in hand. |
| **Sub-agents** | **Dispatch a sub-agent** for research, codebase exploration, parallel work, or anything that would consume >2k tokens of main context. One task per sub-agent. |
| **Adversarial review** | **Run an adversarial review** before claiming any feature shipped. 2-minute hostile pass: where could this break, what was tested vs. assumed, what classes of silent failure exist. |
| **Superpowers brainstorming** | **Start non-trivial creative work with `superpowers:brainstorming`**. Anything that isn't a one-line bug fix or a known-pattern refactor goes through brainstorming first. |
| **End-to-end verification** | **Fetch the deployed page** and grep for the thing the feature is supposed to produce (anchor IDs, button labels, schema markup, expected text) before claiming shipped. "Build green" is not a proxy for "feature works." |
| **Smoke test all paths** | **Smoke-test every affected path**, not just the one most likely to be interesting. If a change touches N pages, check N pages. |
| **Lessons captured** | **Update `tasks/lessons.md`** after every user correction. Name the failure, the fix, the guardrail. |
| **Validator gates** | **Run `pnpm validate:seed`** before any commit that touches `src/blocks/`, `src/seed/`, or `src/components/blocks/`. Run `pnpm test:locale-routing` after any change to a header, footer, nav, or `marketing-links.ts`. |
| **Test the test** | **Watch the test fail first.** A passing test before the implementation exists means the test is vacuously passing — tighten the assertion. |
| **No defensive null guards on required fields** | **NEVER paper over a missing required schema field with a null guard.** Fix the source: the seed is wrong, the schema is wrong, or the locale write orphaned data. |
| **Pre-launch reset posture** | **Prefer `payload migrate:fresh`** for awkward migrations until launch. Transient data loss in dev/preview is acceptable; surgical migrations are post-launch behavior. |
| **No build-green-as-done** | **NEVER claim "shipped" because the build is green.** The build only proves the code compiles. The test gate is what proves the feature works. |
| **No hardcoded user-visible strings** | **Every user-visible string** goes through `useTranslations` or a Payload `localized: true` field. No string literals in components rendering text users will read. |

## Anti-rules

Things that should NOT go in CLAUDE-PIP.md:

- Project setup notes ("we use Tailwind v4") — those belong in CLAUDE.md proper.
- Stylistic preferences ("prefer arrow functions") — those belong in a lint config.
- One-off task notes ("remember to fix the footer copy") — those belong in `tasks/todo.md`.
- Anything with hedge words. If the rule isn't deterministic, it doesn't belong here.

If the user invokes `CLAUDE PIP` for something that fits an anti-rule, push back: "That doesn't fit the deterministic-rule format. Want me to put it in <appropriate-file> instead?"

## Cross-project rules

If the same rule should apply in every project, not just this one, also append it to `~/.claude/CLAUDE.md` after writing to the project file. Ask the user first if they didn't specify.

## Output to user

After writing the rule, confirm in this format:

```
✓ CLAUDE PIP — rule added to <path>

  {rule}

This will fire deterministically on every future session. To remove,
edit the file directly or invoke `CLAUDE PIP REMOVE <rule>`.
```
