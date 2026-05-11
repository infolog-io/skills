# semantic-organization

Meta-skill that governs how every skill is structured. Codifies folder
roles, naming rules, and migration triggers so a reader can guess where
any file lives before opening it.

## Three operating modes

| Mode | Trigger | Output |
|---|---|---|
| Scaffold | "/new-skill", "scaffold a new skill" | Canonical skill skeleton |
| Audit | "/semantic-audit", "audit this skill" | 7-dim scored audit + findings |
| Migrate | "should this folder be its own skill?" | Verdict + migration plan |

## Why

Predictable structure makes refactors mechanical, makes onboarding fast,
and makes a marketplace of skills compose cleanly. Drift in folder names
and file naming is the most common kind of structural rot.

## Rubric (7 dimensions, scored 1–5)

Folder role clarity · folder responsibility purity · common shape
conformance · naming consistency · migration health · README discipline ·
TESTS.md presence and quality.

Verdicts: **semantically-healthy** (all ≥4) · **drifting** (any 2–3) ·
**broken** (any 1 or three 2s).

## Install

```bash
claude plugin marketplace add infolog-io/skills
claude plugin install semantic-organization@infolog-io
```

## Triggers

`scaffold a new skill` · `/new-skill` · `/semantic-audit` · `rename this folder` · `should this be its own skill?`
