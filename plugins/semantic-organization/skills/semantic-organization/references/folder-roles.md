# Folder Roles

The Agent Skills spec at https://agentskills.io/specification is the source
of truth for what a skill is. This reference applies that spec to the
infolog-io marketplace, distinguishes spec-level rules from
marketplace-level conventions, and names every folder's role.

## The two layers

A plugin in this marketplace has two layers:

- **Skill layer** — governed by the Agent Skills spec. Anyone can read a
  skill and recognize it as compliant.
- **Plugin layer** — marketplace wrapper. Adds installation manifest,
  marketplace-listing README, and a test plan. Not part of the spec.

Treat the two layers separately. Spec rules are non-negotiable. Plugin
conventions can evolve.

## Skill layer (Anthropic spec)

### Required

| File | Purpose |
|---|---|
| `SKILL.md` | YAML frontmatter (`name`, `description`) + markdown body. The only required file. |

### Optional canonical folders

These three folders are named in the spec. If a folder fits one of these
roles, use the spec name.

| Folder | Holds | Loaded |
|---|---|---|
| `scripts/` | Executable code the skill runs (Python, Bash, JS, etc.) | On demand |
| `references/` | Additional documentation. Domain context, frameworks, lookup tables, glossaries | On demand |
| `assets/` | Static resources. Templates, images, schemas, sample data, fonts | On demand |

### Other folders are allowed but discouraged

The spec allows "any additional files or directories." Use that latitude
sparingly. If new role names creep in (`prompts/`, `templates/`,
`fixtures/`, `schemas/`), each one is one more thing readers must learn
before navigating the skill.

Default behavior: put templates and schemas in `assets/`. Put test fixtures
in `assets/` or omit (the SKILL.md often includes examples inline).

### Accepted non-spec folders in this marketplace

These folders are used by existing skills and accepted by the audit when
documented in the skill's SKILL.md. See `references/spec-vs-conventions.md`
for the full list and rationale.

| Folder | Convention purpose |
|---|---|
| `prompts/` | Mode-specific instruction files |
| `templates/` | Canonical output templates |
| `schemas/` | JSON Schema contracts |
| `fixtures/` | Test inputs and expected outputs |

New skills should prefer spec folders. Use convention folders only when
the content does not fit `references/`, `assets/`, or `scripts/`.

## Plugin layer (marketplace conventions)

### Required at plugin root

| File | Purpose |
|---|---|
| `.claude-plugin/plugin.json` | Plugin manifest. Required by Claude Code. |
| `README.md` | Marketplace listing. ≤200 words. What + when + install. |
| `TESTS.md` | End conditions and test cases. Forces "definition of done" before build. |

### Required structure

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── TESTS.md
└── skills/<skill-name>/      ← the spec-compliant skill lives here
    └── SKILL.md
```

The `skills/<skill-name>/` wrapper lets a plugin host more than one skill
in the future without restructuring.

## Forbidden folder names

These name implementation or are catch-alls. Reject on sight.

| Folder | Why forbidden | Replacement |
|---|---|---|
| `src/`, `lib/` | Implementation, not role | `scripts/` for executable code |
| `utils/`, `helpers/`, `common/`, `misc/` | Catch-alls; hide poor organization | Split by role |
| `docs/` | Skill body is the docs; references go in `references/` | `references/` or inline |
| `tests/` | Test definitions go in plugin's `TESTS.md` | `TESTS.md` |
| `examples/` | Examples live inline or in `assets/` | inline or `assets/` |
| `legacy/` | Use git history | git history |

## When to create a non-spec folder

If you need something the spec doesn't name, ask in this order:

1. Can it go in `references/`? (knowledge) → use `references/`
2. Can it go in `assets/`? (static resource) → use `assets/`
3. Can it go in `scripts/`? (executable) → use `scripts/`
4. Could the content live inline in SKILL.md or a single reference file?
5. If still no — name the new folder by its role, document the role in
   SKILL.md, and accept the cost of one more folder concept.

## Naming a folder

Ask: "What is the role of every file in this folder?"

- If they're all docs → `references/`
- If they're all executables → `scripts/`
- If they're all static resources → `assets/`
- If they're a mix → split the folder

## Worked examples

### Spec-minimum skill

```
brand-guidelines/
├── SKILL.md
└── LICENSE.txt
```

Two files. Compliant.

### Skill with references

```
algorithmic-art/
├── SKILL.md
└── templates/         ← strictly speaking should be `assets/`, but spec is permissive
```

### Skill with scripts

```
docx/
├── SKILL.md
└── scripts/
    └── office/        ← sub-folders inside scripts/ are fine
        ├── helpers/
        ├── schemas/
        └── validators/
```

### Full plugin in this marketplace

```
plugins/jtbd-prd/
├── .claude-plugin/
│   └── plugin.json
├── README.md          ← plugin layer
├── TESTS.md           ← plugin layer
└── skills/jtbd-prd/   ← spec-compliant skill begins here
    ├── SKILL.md
    ├── references/
    ├── assets/        ← templates, schemas, fixtures all live here in revised standard
    └── scripts/       (optional, only if needed)
```
