# semantic-organization

Meta-skill for skill structure. Codifies folder roles, naming,
context layers, host profiles, and migration triggers so a reader can
guess where any file lives before opening it.

## Operating modes

| Mode | Trigger | Output |
|---|---|---|
| Scaffold | "/new-skill", "scaffold a new skill" | Host/profile-aware skeleton |
| Audit | "/semantic-audit", "audit this skill" | 8-dim audit + host/context facets |
| Migrate | "should this folder be its own skill?" | Verdict + migration plan |
| Rename | "is this folder name semantic?" | Keep / rename / delete verdict |

## Why

Predictable structure makes refactors mechanical and lets skills compose.
Naming drift and over-scaffolded folders are common rot.

## Rubric (8 dimensions, scored 1–5)

Skill-layer (spec): SKILL.md validity · naming · body · folder discipline.
Marketplace-layer: plugin manifest · README · TESTS.md · migration health.

Reference-integrity can force `broken`; host-standard and context-fit
facets guide portable generation without changing the core 8 scores.

Verdicts: **spec-compliant + marketplace-ready** · **spec-compliant,
marketplace-drift** · **spec-drift** · **broken**.

## Install

```bash
claude plugin marketplace add infolog-io/skills
claude plugin install semantic-organization@infolog-io
```

## Triggers

`scaffold a new skill` · `/new-skill` · `/semantic-audit` · `rename this folder`
