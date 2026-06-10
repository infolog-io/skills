# semantic-organization

Meta-skill governing how every skill in this marketplace is structured.
Codifies the Anthropic Agent Skills directory convention
(`skills/<name>/SKILL.md` — no plugin wrapper), folder roles, naming
rules, and migration triggers.

## Four operating modes

| Mode | Trigger | Output |
|---|---|---|
| Scaffold | "/new-skill", "scaffold a new skill", "add a skill" | Canonical skeleton, registered in marketplace.json |
| Audit | "/semantic-audit", "audit this skill" | 8-dimension scored audit + findings |
| Migration | "should this folder be its own skill?" | stay-as-folder / promote-to-sibling-skill / already-its-own-skill |
| Rename | "rename this folder" | Spec-canonical name proposal |

## Rubric (8 dimensions, scored 1–5)

Four spec-layer dimensions (SKILL.md validity · naming conformance ·
body discipline · folder discipline) and four marketplace-layer
dimensions (plugin manifest · README discipline · TESTS.md quality ·
migration health).

Verdicts: `spec-compliant + marketplace-ready` (all ≥4) ·
`spec-compliant, marketplace-drift` · `spec-drift` · `broken`.

## Install

```bash
claude plugin marketplace add infolog-io/skills
claude plugin install semantic-organization@infolog-io
```

## Triggers

`scaffold a new skill` · `add a skill` · `create a skill` ·
`/new-skill` · `audit this skill` · `/semantic-audit` ·
`rename this folder` · `should this be a folder or its own skill?`
