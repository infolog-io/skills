# semantic-organization

Meta-skill that governs how every skill is structured. Codifies folder
roles, naming rules, and migration triggers so a reader can guess where
any file lives before opening it.

## Three operating modes

| Mode | Trigger | Output |
|---|---|---|
| Scaffold | "/new-skill", "scaffold a new skill" | Canonical skill skeleton |
| Audit | "/semantic-audit", "audit this skill" | 8-dim scored audit + integrity gate + findings |
| Migrate | "should this folder be its own skill?" | Verdict + migration plan |

## Why

Predictable structure makes refactors mechanical and lets a marketplace of
skills compose cleanly. Naming drift is the most common structural rot.

## Rubric (8 dimensions, scored 1–5)

Skill-layer (spec): SKILL.md validity · naming · body · folder discipline.
Marketplace-layer: plugin manifest · README · TESTS.md · migration health.

A non-scored reference-integrity gate forces `broken` on any dead
reference. Aligns with the Open Knowledge Format.

Verdicts: **spec-compliant + marketplace-ready** · **spec-compliant,
marketplace-drift** · **spec-drift** · **broken**.

## Install

```bash
claude plugin marketplace add infolog-io/skills
claude plugin install semantic-organization@infolog-io
```

## Triggers

`scaffold a new skill` · `/new-skill` · `/semantic-audit` · `rename this folder` · `should this be its own skill?`
