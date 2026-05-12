---
name: semantic-organization
description: >
  Governs how every skill in this marketplace is structured. Codifies the
  Anthropic Agent Skills directory convention (skills/<name>/SKILL.md at
  the repo root — no plugin wrapper), folder roles, naming rules, and
  migration triggers. Scaffolds new skills against the canonical layout,
  audits existing skills, and recommends when a folder should become its
  own sibling skill. Applies Unix philosophy: one skill = one purpose,
  compose via plain text, prefer small over large. Activates on "scaffold
  a new skill", "/new-skill", "audit this skill", "/semantic-audit",
  "should this be a folder or its own skill", or any time a skill
  structure is being designed or evaluated.
---

# semantic-organization

## Purpose

Every skill in this marketplace must match the Anthropic Agent Skills
directory convention at https://github.com/anthropics/skills. This skill
encodes that convention and audits against it.

## Canonical layout

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

## The two layers — same directory

A skill carries both layers in the same folder:

| Layer | Files | Source |
|---|---|---|
| **Spec layer** (Anthropic) | `SKILL.md`, optional `scripts/`, `references/`, `assets/` | https://agentskills.io/specification |
| **Marketplace layer** (Claude Code) | `.claude-plugin/plugin.json`, `README.md`, `TESTS.md` | This skill's conventions |

There is no separate plugin-wrapper directory. The plugin manifest lives
INSIDE the skill folder, so the skill is simultaneously
spec-compliant AND installable via `claude plugin install`.

## Skill profiles

Not every skill needs every folder. Two profiles:

### Single-rule skill

One durable rule or principle. SKILL.md body carries everything.

Required: `SKILL.md`, `.claude-plugin/plugin.json`, `README.md`, `TESTS.md`.
No required sub-folders.

A skill is single-rule when SKILL.md is under 200 lines and there are no
sub-folders.

### Full-shape skill

Multiple modes, references, optional scripts and assets. SKILL.md is the
entry point; detail lives in `references/` and `assets/`.

Required: same as single-rule, plus at least one of `references/`,
`scripts/`, `assets/` per actual need.

A skill is full-shape when it has multiple operating modes, references
broken out from SKILL.md, and (usually) prompts or assets.

## The eight audit dimensions

See `references/audit-rubric.md`.

| Layer | Dimension |
|---|---|
| Spec | S1. SKILL.md presence and validity |
| Spec | S2. Naming conformance (parent dir, plugin.json, frontmatter agree) |
| Spec | S3. Body discipline (<500 lines; shallow references) |
| Spec | S4. Folder discipline (only spec or convention folders; no forbidden) |
| Marketplace | P1. Plugin manifest valid (inside skill folder) |
| Marketplace | P2. README discipline (≤200 words, what/when/install) |
| Marketplace | P3. TESTS.md presence and quality |
| Marketplace | P4. Migration health (no overgrown folders; no wrapper layers) |

## Verdicts

| Verdict | Rule | Allowed downstream |
|---|---|---|
| `spec-compliant + marketplace-ready` | All 8 dims ≥4 | Ship |
| `spec-compliant, marketplace-drift` | Spec ≥4, marketplace has 2-3 | Fix conventions before ship |
| `spec-drift` | One or more spec dims at 2-3 | Fix spec violations first |
| `broken` | Any dim at 1, OR a forbidden layout is present | Halt; restore canonical shape |

## Operating modes

### Scaffold mode

Trigger: "scaffold a new skill", "/new-skill", "create a skill"

Behavior:
1. Ask for skill name (kebab-case, matches spec rules)
2. Ask for one-sentence description (what + when)
3. Ask for profile: single-rule or full-shape
4. Emit canonical folder tree at `skills/<name>/` with placeholder content
5. Run immediate self-audit — confirm scaffold scores ≥4 on all dimensions

See `prompts/scaffold-new-skill.md`.

### Audit mode

Trigger: "audit this skill", "/semantic-audit"

Behavior:
1. Walk the skill's file tree at `skills/<name>/`
2. Detect profile (single-rule vs. full-shape)
3. Check for forbidden layouts (`plugins/` wrapper, double nesting)
4. Score each of the 8 dimensions per `references/audit-rubric.md`
5. Emit Semantic Organization Audit with findings
6. Verdict per the table above

See `prompts/audit-existing-skill.md`.

### Migration mode

Trigger: "should this be a folder or its own skill?"

Behavior:
1. Check folder against migration triggers
2. Return: `stay-as-folder` / `promote-to-sibling-skill` / `already-its-own-skill`
3. If promote, emit migration plan

See `references/migration-triggers.md` and `prompts/evaluate-migration.md`.

### Rename mode

Trigger: "rename this folder", "is this folder name semantic?"

Behavior:
1. Compare folder name against the role taxonomy
2. Propose a spec-canonical name or flag for deletion
3. Refuse to rename spec-canonical folders (`scripts/`, `references/`, `assets/`) to non-spec names

See `prompts/rename-for-semantics.md`.

## References

- `references/spec-vs-conventions.md` — how spec and marketplace layers coexist in one directory
- `references/folder-roles.md` — what each canonical folder holds; forbidden names
- `references/naming-rules.md` — spec-mandated and convention-mandated naming
- `references/migration-triggers.md` — when a folder becomes its own skill
- `references/audit-rubric.md` — the 8-dimension scored rubric
- `references/unix-philosophy.md` — Unix tenets applied to skills

## Triggers

| Phrase | Mode |
|---|---|
| `scaffold a new skill`, `/new-skill`, `create a skill` | Scaffold |
| `audit this skill`, `/semantic-audit` | Audit |
| `should this be a folder or its own skill?` | Migration |
| `rename this folder`, `is this folder name semantic?` | Rename |

## Self-application

This skill must pass its own audit. The audit applies the 8-dimension
rubric. Self-test target: all skill-layer dimensions at 5; all
marketplace-layer dimensions at 5; verdict =
`spec-compliant + marketplace-ready`.

If the skill cannot meet its own bar, fix the rubric or fix the skill.
