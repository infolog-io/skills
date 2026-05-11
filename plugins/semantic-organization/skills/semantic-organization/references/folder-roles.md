# Folder Roles

Every folder in a skill has exactly one role. The folder name declares that
role. A reader who knows the role taxonomy can find what they need without
opening anything.

## Canonical folders

### `references/`

Knowledge. Theory, frameworks, distillations, principles. Read-only for the
model. Files describe how something works, not what to do.

Belongs:
- Framework distillations (Christensen + Ulwick, Tufte principles)
- Naming conventions
- Glossary entries
- Background context that supports prompts

Does not belong:
- Step-by-step operations (those go in `prompts/`)
- Canonical output shapes (those go in `templates/`)
- Schemas (those go in `schemas/`)

### `prompts/`

Actions. Mode-specific operations. Each file is one purpose, callable by a
single triggering condition. Files describe what to do and how to do it.

Belongs:
- One prompt file per operating mode
- Input/output contracts
- Worked examples
- Negative cases

Does not belong:
- Theory or framework grounding (`references/`)
- Output structure definitions (`templates/`)
- Test data (`fixtures/`)

### `templates/`

Canonical output shapes. The structure the skill emits, with placeholder
slots. One template per kind of artifact the skill produces.

Belongs:
- Markdown templates with `{{slot}}` placeholders
- Renderable canonical artifacts
- Empty/skeleton versions of skill outputs

Does not belong:
- Live examples filled with data (those go in `fixtures/`)
- Schemas that validate the template (those go in `schemas/`)

### `schemas/`

Validation contracts. JSON Schema (draft 2020-12 preferred) for any
structured output the skill emits. Used to validate that the skill's output
is well-formed.

Belongs:
- One schema per structured artifact
- Field-level constraints
- Required vs. optional declarations

Does not belong:
- Templates (those are presentation; schemas are validation)
- Test data (`fixtures/`)

### `fixtures/`

Test inputs and expected outputs. Concrete examples used to verify the
skill works. Pair each input with its expected output.

Belongs:
- `input-*.md` — example inputs the skill should handle
- `expected-*.md` — what the skill should produce for that input
- Labeled known cases (good / drifted / broken)

Does not belong:
- Test runners (test definitions go in `TESTS.md`)
- Production data (fixtures are synthetic; never real PII)

## Optional folders

### `tools/`

Runnable scripts bundled with the skill. Use when the skill performs work
that requires real computation, not just prompt logic.

Belongs:
- Python, JS, shell scripts
- A `README.md` in `tools/` explaining each script's purpose

Trigger to add: the skill cannot reasonably do its job in prompt alone.

### `assets/`

Non-text artifacts. Images, fonts, binary samples needed by the skill.

Belongs:
- PNG, SVG, WOFF2, sample binaries
- Reference images for visual audits

Trigger to add: the skill consumes or emits non-text content.

### `migrations/`

Version-bump migration notes. One file per breaking change.

Belongs:
- `0.1.0-to-0.2.0.md` — what changed, how consumers adapt

Trigger to add: the skill is shipping a breaking change.

## Forbidden folders

| Folder | Why forbidden | Replacement |
|---|---|---|
| `src/` | Names implementation, not intent | `prompts/` or `tools/` |
| `lib/` | Same — implementation | `tools/` |
| `utils/` | Catch-all for "stuff I don't know where to put" | Split by role |
| `helpers/` | Same | Split by role |
| `common/` | Same | Split by role |
| `docs/` | Documentation belongs at the boundary (README) or inside a role folder | `README.md` or `references/` |
| `tests/` | Test definitions go in TESTS.md; test data in `fixtures/` | `TESTS.md` + `fixtures/` |
| `examples/` | Examples live inside the file that uses them | Inline in prompt or reference |
| `misc/` | Always wrong | Split by role |
| `legacy/` | Use `migrations/` or git history | `migrations/` or delete |

## Naming a folder

Ask: "What is the role of every file in this folder?"

- If the answer is "they're all knowledge" → `references/`
- If the answer is "they're all actions" → `prompts/`
- If the answer is "they're all output shapes" → `templates/`
- If the answer is "they're all validation contracts" → `schemas/`
- If the answer is "they're all test data" → `fixtures/`
- If the answer is "they're all different things" → split the folder

## Worked example

### Bad

```
my-skill/
├── code/
├── stuff/
├── examples/
└── docs/
```

Audit verdict: `broken`. No folder names a role. Reader cannot guess what
lives where.

### Drifted

```
my-skill/
├── references/
├── prompts/
├── utils/              ← forbidden
└── tests/              ← forbidden
```

Audit verdict: `drifting`. Two role-named folders, two forbidden. Action:
move `utils/` content into the role that fits; move `tests/` content into
`fixtures/` + `TESTS.md`.

### Healthy

```
my-skill/
├── references/
├── prompts/
├── templates/
├── schemas/
└── fixtures/
```

Audit verdict: `semantically-healthy`. Every folder names a role; reader
can predict where any file lives.
