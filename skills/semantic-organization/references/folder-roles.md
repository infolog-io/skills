# Folder Roles

The Agent Skills spec at https://agentskills.io/specification is the source
of truth for what a skill is. The Anthropic reference repo at
https://github.com/anthropics/skills shows the canonical directory shape.
This reference applies both to the infolog-io marketplace.

## The canonical layout

Skills live at `skills/<skill-name>/` at the marketplace repo root. Each
skill folder carries both its spec-required files AND its marketplace
manifest. There is no wrapper directory.

```
<marketplace-repo>/
├── .claude-plugin/
│   └── marketplace.json                ← marketplace manifest (lists skills)
├── skills/                             ← all skills live here
│   └── <skill-name>/
│       ├── .claude-plugin/
│       │   └── plugin.json             ← plugin manifest (INSIDE the skill)
│       ├── SKILL.md                    ← required by spec
│       ├── README.md                   ← marketplace listing (≤200 words)
│       ├── TESTS.md                    ← end conditions + test cases
│       ├── scripts/                    ← spec-canonical, optional
│       ├── references/                 ← spec-canonical, optional
│       ├── assets/                     ← spec-canonical, optional
│       ├── prompts/                    ← convention, optional
│       ├── templates/                  ← convention, optional
│       ├── schemas/                    ← convention, optional
│       └── fixtures/                   ← convention, optional
├── README.md
└── LICENSE
```

This mirrors Anthropic's reference repo. The only addition is
`.claude-plugin/plugin.json` inside each skill folder for Claude Code
plugin install.

## Spec-canonical folders (Agent Skills spec)

### Required

| File | Purpose |
|---|---|
| `SKILL.md` | YAML frontmatter (`name`, `description`) + markdown body. The only spec-required file. |

### Optional

| Folder | Holds | Loaded |
|---|---|---|
| `scripts/` | Executable code the skill runs (Python, Bash, JS, etc.) | On demand |
| `references/` | Additional documentation. Domain context, frameworks, lookup tables, glossaries | On demand |
| `assets/` | Static resources. Templates, images, schemas, sample data, fonts | On demand |

## Marketplace files (this repo's conventions)

These live IN THE SAME folder as the skill — not in a wrapper directory.

| File | Purpose |
|---|---|
| `.claude-plugin/plugin.json` | Plugin manifest. Required by Claude Code's plugin install. |
| `README.md` | Marketplace listing. ≤200 words. What + when + install. |
| `TESTS.md` | End conditions and test cases. Forces "definition of done" before build. |

## Accepted convention folders

Used by full-shape skills. Documented here so the audit accepts them
without penalty. New skills should prefer spec-canonical folders when
the content fits; use these when it doesn't.

| Folder | Convention purpose | Spec equivalent (if any) |
|---|---|---|
| `prompts/` | Mode-specific instruction files | Could fold into SKILL.md or `references/` |
| `templates/` | Canonical output templates | `assets/` |
| `schemas/` | JSON Schema contracts | `assets/` |
| `fixtures/` | Test inputs and expected outputs | `assets/` or omitted |

## Forbidden layouts

The audit returns `broken` if any of these appear:

| Forbidden | Why | Replacement |
|---|---|---|
| `plugins/<name>/` directory at repo root | Old wrapped form; not canonical | Move contents to `skills/<name>/` |
| `plugins/<name>/skills/<name>/SKILL.md` | Double nesting; SKILL.md should be one level deep | Flatten to `skills/<name>/SKILL.md` |
| `.claude-plugin/plugin.json` outside the skill folder | Plugin manifest belongs INSIDE the skill | Move to `skills/<name>/.claude-plugin/plugin.json` |

## Forbidden folder names

These name implementation or are catch-alls. Reject on sight.

| Folder | Why forbidden | Replacement |
|---|---|---|
| `src/`, `lib/` | Implementation, not role | `scripts/` for executable code |
| `utils/`, `helpers/`, `common/`, `misc/` | Catch-alls; hide poor organization | Split by role |
| `docs/` | Skill body is the docs; references go in `references/` | `references/` or inline |
| `tests/` | Test definitions go in `TESTS.md` | `TESTS.md` |
| `examples/` | Examples live inline or in `assets/`/`fixtures/` | inline, `assets/`, or `fixtures/` |
| `legacy/` | Use git history | git history |

## When to create a non-canonical folder

If you need something neither spec nor convention names, ask in this order:

1. Can it go in `references/`? (knowledge) → use `references/`
2. Can it go in `assets/`? (static resource) → use `assets/`
3. Can it go in `scripts/`? (executable) → use `scripts/`
4. Could the content live inline in SKILL.md or a single reference file?
5. If still no — name the new folder by its role, document it in SKILL.md, and accept the cost of one more concept.

## Naming a folder

Ask: "What is the role of every file in this folder?"

- If they're all docs → `references/`
- If they're all executables → `scripts/`
- If they're all static resources → `assets/`
- If they're a mix → split the folder

## Worked examples

### Spec-minimum skill (single-rule)

```
skills/brand-guidelines/
├── SKILL.md
├── README.md
├── TESTS.md
├── LICENSE.txt
└── .claude-plugin/plugin.json
```

Five files. Compliant. Installable via Claude Code marketplace.

### Skill with references

```
skills/algorithmic-art/
├── SKILL.md
├── README.md
├── TESTS.md
├── .claude-plugin/plugin.json
└── templates/         ← strictly speaking should be `assets/`, but spec is permissive
```

### Skill with scripts

```
skills/docx/
├── SKILL.md
├── README.md
├── TESTS.md
├── .claude-plugin/plugin.json
└── scripts/
    └── office/        ← sub-folders inside scripts/ are fine
        ├── helpers/
        ├── schemas/
        └── validators/
```

### Full-shape skill in this marketplace

```
skills/<skill-name>/
├── .claude-plugin/
│   └── plugin.json
├── SKILL.md
├── README.md          ← ≤200 words
├── TESTS.md
├── references/        ← spec-canonical
├── assets/            ← spec-canonical (templates, schemas, fixtures all live here in revised standard)
├── prompts/           ← convention
├── templates/         ← convention
├── schemas/           ← convention
└── fixtures/          ← convention
```
