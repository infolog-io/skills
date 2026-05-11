---
name: semantic-organization
description: >
  Governs how every skill in this marketplace is structured. Distinguishes
  the Anthropic Agent Skills spec (skill layer) from infolog-io marketplace
  conventions (plugin layer). Scaffolds new skills against both, audits
  existing skills, and recommends when a folder should become its own
  sibling skill. Applies Unix philosophy: one skill = one purpose, compose
  via plain text, prefer small over large. Activates on "scaffold a new
  skill", "/new-skill", "audit this skill", "/semantic-audit", "should this
  be a folder or its own skill", or any time a skill structure is being
  designed or evaluated.
---

# semantic-organization

## Purpose

Two layers govern a plugin in this marketplace:

- **Skill layer** — the Agent Skills spec at https://agentskills.io/specification.
  Non-negotiable. Mandates one file: `SKILL.md` with `name` and
  `description` frontmatter. Allows three canonical optional folders:
  `scripts/`, `references/`, `assets/`. Recommends SKILL.md under 500
  lines and progressive disclosure.
- **Plugin layer** — marketplace conventions. Adds `plugin.json`,
  `README.md` (≤200 words), `TESTS.md`, and the `skills/<name>/` wrapper.
  Evolvable; not part of the spec.

This skill applies Unix philosophy to both layers: one skill per purpose,
plain-text composition, small over large, no captive interfaces. See
`references/unix-philosophy.md`.

## Canonical layout

```
plugins/<plugin-name>/                  ← plugin layer (marketplace convention)
├── .claude-plugin/
│   └── plugin.json                     ← plugin layer
├── README.md                           ← plugin layer (≤200 words)
├── TESTS.md                            ← plugin layer
└── skills/<skill-name>/                ← plugin layer wrapper
    ├── SKILL.md                        ← skill layer (spec-required)
    ├── scripts/                        ← skill layer (spec optional)
    ├── references/                     ← skill layer (spec optional)
    └── assets/                         ← skill layer (spec optional)
```

## Skill profiles

Not every skill needs every folder. Two profiles:

### Single-rule skill

One durable rule or principle. SKILL.md body carries everything.

Required: SKILL.md, plugin.json, README.md, TESTS.md.
No required sub-folders.

Examples in this marketplace: `claude-pip`, `estimatrix`.

### Full-shape skill

Multiple modes, references, optional scripts and assets. SKILL.md is the
entry point; detail lives in `references/` and `assets/`.

Required: SKILL.md + plugin layer + at least one of `references/`,
`scripts/`, `assets/` per actual need.

Examples: `tufte-love`, `jtbd-prd`, `semantic-organization`.

## The eight audit dimensions

Four for the skill layer (spec compliance), four for the plugin layer
(marketplace conventions). See `references/audit-rubric.md`.

| Layer | Dimension |
|---|---|
| Skill (spec) | S1. SKILL.md presence and validity |
| Skill (spec) | S2. Naming conformance (parent dir, plugin.json, frontmatter agree) |
| Skill (spec) | S3. Body discipline (<500 lines; shallow references) |
| Skill (spec) | S4. Folder discipline (only spec folders, or documented non-spec) |
| Plugin | P1. Plugin manifest valid |
| Plugin | P2. README discipline (≤200 words, what/when/install) |
| Plugin | P3. TESTS.md presence and quality |
| Plugin | P4. Migration health (no overgrown folders) |

## Verdicts

| Verdict | Rule | Allowed downstream |
|---|---|---|
| `spec-compliant + marketplace-ready` | All 8 dims ≥4 | Ship |
| `spec-compliant, marketplace-drift` | Skill layer ≥4, plugin layer has 2-3 | Fix conventions before ship |
| `spec-drift` | One or more skill-layer dims at 2-3 | Fix spec violations first |
| `broken` | Any dim at 1 | Halt; restore canonical shape |

## Operating modes

### Scaffold mode

Trigger: "scaffold a new skill", "/new-skill", "create a skill"

Behavior:
1. Ask for skill name (kebab-case, matches spec rules)
2. Ask for one-sentence description (what + when)
3. Ask for profile: single-rule or full-shape
4. Emit canonical folder tree with placeholder content
5. Run immediate self-audit — confirm scaffold scores ≥4 on all dimensions

See `prompts/scaffold-new-skill.md`.

### Audit mode

Trigger: "audit this skill", "/semantic-audit"

Behavior:
1. Walk the plugin's file tree
2. Detect profile (single-rule vs. full-shape)
3. Score each of the 8 dimensions per `references/audit-rubric.md`
4. Emit Semantic Organization Audit with findings
5. Verdict per the table above

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

- `references/spec-vs-conventions.md` — the two-layer model explained
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

This skill must pass its own audit. The audit applies the two-layer rubric.
Self-test target: all skill-layer dimensions at 5; all plugin-layer
dimensions at 5; verdict = `spec-compliant + marketplace-ready`.

If the skill cannot meet its own bar, fix the rubric or fix the skill.
