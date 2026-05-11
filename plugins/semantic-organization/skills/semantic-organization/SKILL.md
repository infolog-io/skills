---
name: semantic-organization
description: >
  Governs how every skill is structured. Codifies folder roles, naming rules,
  and migration triggers so that a reader can guess where a file lives before
  opening anything. Three modes: scaffold a new skill, audit an existing
  skill, evaluate whether a sub-folder should become its own sibling skill.
  Activates on "scaffold a new skill", "/new-skill", "create a skill",
  "audit this skill", "/semantic-audit", "should this be a folder or its own
  skill", "rename this folder", or any time a new skill structure is being
  designed.
---

# semantic-organization

## Purpose

A meta-skill. Sits above every other skill in this marketplace and any user
skill the author writes. Defines a single canonical shape so that:

- Readers can find what they need without exploration
- Skills compose predictably across the marketplace
- Refactors are mechanical because the structure is mechanical
- Folders that have outgrown their place are migrated, not bloated

## The canonical skill shape

Every skill must follow this layout. No exceptions without recorded
rationale.

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json              # required — manifest
├── README.md                    # required — ≤200 words; what + when + install
├── TESTS.md                     # required — end conditions + test cases
└── skills/<skill-name>/
    ├── SKILL.md                 # required — frontmatter + triggers + flow
    ├── references/              # knowledge (theory, frameworks)
    ├── prompts/                 # actions (mode-specific operations)
    ├── templates/               # canonical output shapes
    ├── schemas/                 # validation contracts (JSON schema)
    └── fixtures/                # test inputs + expected outputs
```

Optional folders (only when the content cannot live in the above):

- `tools/` — runnable scripts (Python, JS, shell) bundled with the skill
- `assets/` — non-text artifacts (images, fonts, binary samples)
- `migrations/` — version-bump migration notes when the skill ships breaking changes

Forbidden folders:

- `src/`, `lib/`, `utils/`, `helpers/`, `common/` — these name implementation, not intent
- `docs/` — content goes in `references/` (knowledge) or `README.md` (entry)
- `tests/` — test data goes in `fixtures/`; test definitions go in `TESTS.md`
- `examples/` — examples live inside the prompt or reference that uses them

## The seven dimensions of semantic organization

Score each dimension 1–5. See `references/audit-rubric.md` for the full rubric.

1. **Folder role clarity** — does every folder name a role, not an implementation?
2. **Folder responsibility purity** — does each folder hold exactly one kind of thing?
3. **Common shape conformance** — does the skill match the canonical layout?
4. **Naming consistency** — kebab-case throughout; nouns for artifacts, verbs for actions
5. **Migration health** — are any folders overgrown and ready to spin out?
6. **README discipline** — ≤200 words; declares what, when, install
7. **TESTS.md presence and quality** — end conditions stated; test cases enumerated

## Operating modes

### Scaffold mode

Trigger: "scaffold a new skill", "/new-skill", "create a skill"

Behavior:
1. Ask for skill name (kebab-case)
2. Ask for one-sentence description
3. Emit the canonical folder tree with placeholder content
4. Pre-fill SKILL.md frontmatter, README.md skeleton, TESTS.md skeleton
5. Run an immediate audit — confirm scaffold scores 5/5 before handing off

See `prompts/scaffold-new-skill.md`.

### Audit mode

Trigger: "audit this skill", "/semantic-audit"

Behavior:
1. Walk the skill's file tree
2. Score each of the 7 dimensions per `references/audit-rubric.md`
3. Emit a Semantic Organization Audit (mirrors tufte-love format)
4. List specific renames, deletions, or migrations needed
5. Verdict: `semantically-healthy` / `drifting` / `broken`

See `prompts/audit-existing-skill.md`.

### Migration mode

Trigger: "should this be a folder or its own skill?", "is this folder ready to migrate?"

Behavior:
1. Check the folder against migration triggers
2. Return verdict: `stay-as-folder` / `promote-to-sibling-skill` / `already-its-own-skill`
3. If promote, emit a migration plan

See `references/migration-triggers.md` and `prompts/evaluate-migration.md`.

### Rename mode

Trigger: "rename this folder", "is this folder name semantic?"

Behavior:
1. Compare folder name against the role taxonomy in `references/folder-roles.md`
2. Propose a semantic equivalent or flag for deletion
3. Refuse to rename canonical folders (`references/`, `prompts/`, etc.) to non-canonical names

See `prompts/rename-for-semantics.md`.

## Verdict gates

| Verdict | Allowed downstream |
|---|---|
| `semantically-healthy` | Ship; build on top |
| `drifting` | Apply rename/migration plan before next feature |
| `broken` | Halt new feature work; restore the canonical shape first |

## References

- `references/folder-roles.md` — canonical folder taxonomy and what belongs in each
- `references/naming-rules.md` — kebab-case, role-noun pattern, verb-led for actions
- `references/migration-triggers.md` — when a folder becomes its own skill
- `references/audit-rubric.md` — the 7-dimension scored rubric

## Triggers

| Phrase | Mode |
|---|---|
| `scaffold a new skill`, `/new-skill`, `create a skill` | Scaffold |
| `audit this skill`, `/semantic-audit` | Audit |
| `should this be a folder or its own skill?` | Migration |
| `rename this folder`, `is this folder name semantic?` | Rename |
| User about to create a new directory inside a skill | Auto-suggest folder-role check |

## Self-application

This skill must pass its own audit at 5/5 on every dimension. If it does
not, the rubric or the skill is wrong — fix one or the other.
