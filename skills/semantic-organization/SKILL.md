---
name: semantic-organization
description: >
  Use when designing, scaffolding, auditing, renaming, or restructuring
  a skill in this marketplace. Triggers: "scaffold a new skill", "add a
  skill", "create a skill", "/new-skill", "audit this skill",
  "/semantic-audit", "should this be a folder or its own skill",
  "rename this folder", "is this folder name semantic", or any question
  about skill directory layout, folder roles, naming, or promoting a
  sub-folder to a sibling skill.
---

# semantic-organization

## Purpose

Every skill in this marketplace must match the Anthropic Agent Skills
directory convention at https://github.com/anthropics/skills. This skill
encodes that convention, scaffolds new skills against it, and audits
existing ones.

## Canonical layout

This tree is the single canonical copy; all other files point here.

```
<marketplace-repo>/
├── .claude-plugin/
│   └── marketplace.json                ← marketplace manifest (lists skills)
├── skills/                             ← all skills live here (mirrors anthropics/skills)
│   └── <skill-name>/
│       ├── .claude-plugin/
│       │   └── plugin.json             ← plugin manifest (inside the skill)
│       ├── SKILL.md                    ← required by spec
│       ├── README.md                   ← marketplace listing (≤200 words)
│       ├── TESTS.md                    ← end conditions + test cases
│       ├── scripts/                    ← spec-canonical optional folder
│       ├── references/                 ← spec-canonical optional folder
│       ├── assets/                     ← spec-canonical optional folder
│       ├── prompts/                    ← convention (mode-specific operations)
│       ├── templates/                  ← convention (output shapes)
│       ├── schemas/                    ← convention (JSON Schema contracts)
│       └── fixtures/                   ← convention (test inputs + expected outputs)
├── README.md
└── LICENSE
```

## Forbidden layouts

These are NOT canonical. Audit returns `broken` if found:

| Forbidden | Reason |
|---|---|
| `plugins/<name>/skills/<name>/SKILL.md` | Old wrapped form; double nesting |
| `plugins/<name>/SKILL.md` | Wrong directory name; should be `skills/` |
| `<repo-root>/SKILL.md` (skill at repo root) | Multi-skill repos must use `skills/<name>/` |

## The two layers

Spec files (`SKILL.md`, optional `scripts/`, `references/`, `assets/`)
and marketplace files (`.claude-plugin/plugin.json`, `README.md`,
`TESTS.md`) live in the SAME skill folder — no wrapper directory. See
`references/spec-vs-conventions.md`.

## Skill profiles

Not every skill needs every folder.

- **Single-rule** — one durable rule; SKILL.md under 200 lines, no
  sub-folders. Required: `SKILL.md`, `.claude-plugin/plugin.json`,
  `README.md`, `TESTS.md`.
- **Full-shape** — multiple modes or references. Same required files,
  and SHOULD have at least one supporting folder (`references/`,
  `scripts/`, `assets/`, or an accepted convention folder).

A 200–500-line SKILL.md with no sub-folders is a drifting full-shape
skill: the audit emits migration trigger "extract references/"; verdict
at best `spec-drift`.

## Audit dimensions and verdicts

The audit scores 8 dimensions (four spec-layer S1–S4, four
marketplace-layer P1–P4) and returns one of four verdicts, from
`spec-compliant + marketplace-ready` down to `broken`. The scored
rubric and verdict-threshold table live in `references/audit-rubric.md`
(canonical copy).

## Operating modes

- **Scaffold** — emit a profile-gated canonical skeleton at
  `skills/<name>/`, self-audit it, register it in the root
  `.claude-plugin/marketplace.json`. See `prompts/scaffold-new-skill.md`.
- **Audit** — walk the tree, check forbidden layouts, score the 8
  dimensions, emit an audit with verdict. See
  `prompts/audit-existing-skill.md`.
- **Migration** — return `stay-as-folder` / `promote-to-sibling-skill` /
  `already-its-own-skill`, plus a plan when promoting. See
  `references/migration-triggers.md` and `prompts/evaluate-migration.md`.
- **Rename** — propose spec-canonical folder names; never rename spec
  folders (`scripts/`, `references/`, `assets/`) to non-spec names. See
  `prompts/rename-for-semantics.md`.

## References

- `references/spec-vs-conventions.md` — how spec and marketplace layers coexist in one directory
- `references/folder-roles.md` — what each canonical folder holds; forbidden names
- `references/naming-rules.md` — spec-mandated and convention-mandated naming
- `references/migration-triggers.md` — when a folder becomes its own skill
- `references/audit-rubric.md` — the 8-dimension scored rubric and verdict thresholds
- `references/unix-philosophy.md` — Unix tenets applied to skills

## Triggers

| Phrase | Mode |
|---|---|
| `scaffold a new skill`, `add a skill`, `create a skill`, `/new-skill` | Scaffold |
| `audit this skill`, `/semantic-audit` | Audit |
| `should this be a folder or its own skill?` | Migration |
| `rename this folder`, `is this folder name semantic?` | Rename |

## Self-application

This skill must pass its own audit. The audit applies the 8-dimension
rubric. Self-test target: all skill-layer dimensions at 5; all
marketplace-layer dimensions at 5; verdict =
`spec-compliant + marketplace-ready`.

If the skill cannot meet its own bar, fix the rubric or fix the skill.
