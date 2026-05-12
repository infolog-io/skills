# Prompt — Scaffold a new skill

**Purpose:** Generate the canonical folder tree and placeholder files for a
new skill. The scaffold must pass the audit rubric at ≥4 on every
dimension on first emission.

## Input contract

The user provides (or the model asks for):

- **`skill_name`** — kebab-case, unique within the marketplace, ≤30 chars
- **`description`** — one sentence, what the skill does and when to use it
- **`marketplace_path`** — default `infolog-io/skills` (the path under `skills/`)
- **`triggers`** (optional) — list of activation phrases; default to a generic set
- **`primary_artifact`** (optional) — name of the canonical output (e.g., "Job Article")

## Output contract

A complete folder tree at `skills/<skill_name>/` — flat, matching the
Anthropic Agent Skills convention. No `plugins/` wrapper.

```
skills/<skill_name>/
├── .claude-plugin/
│   └── plugin.json                       # pre-filled manifest
├── SKILL.md                              # frontmatter + flow skeleton
├── README.md                             # skeleton ≤200 words
├── TESTS.md                              # skeleton with end-conditions section
├── references/
│   └── .gitkeep                          # placeholder until first reference
├── prompts/
│   └── .gitkeep
├── templates/
│   └── .gitkeep
├── schemas/
│   └── .gitkeep
└── fixtures/
    └── .gitkeep
```

## Pre-filled content

### `plugin.json`

```json
{
  "name": "<skill_name>",
  "version": "0.1.0",
  "description": "<description>",
  "author": { "name": "Information Logistics", "url": "https://github.com/infolog-io" }
}
```

### `SKILL.md`

```
---
name: <skill_name>
description: >
  <description>
  Activates on <trigger 1>, <trigger 2>, ..., or "/<skill_name>".
---

# <skill_name>

## Purpose

[One paragraph: what this skill does, when to activate, what it produces.]

## Operating modes

[Enumerate modes with one paragraph each.]

## References

- references/<file>.md — [purpose]

## Triggers

| Phrase | Mode |
|---|---|
| <phrase> | <mode> |
```

### `README.md`

```
# <skill_name>

<description>

## Why

[One paragraph.]

## When to use

[Bullets.]

## When not to use

[Bullets.]

## Install

\`\`\`bash
claude plugin marketplace add infolog-io/skills
claude plugin install <skill_name>@infolog-io
\`\`\`

## Triggers

[Comma-separated trigger phrases.]
```

Total word count target: ≤ 200.

### `TESTS.md`

```
# <skill_name> — Tests & End Conditions

## End conditions (skill ships when all are true)

1. Plugin installs cleanly via \`claude plugin install <skill_name>@infolog-io\`
2. Skill activates on every trigger phrase listed in SKILL.md
3. All referenced files exist at the paths declared in SKILL.md
4. [Add skill-specific end conditions]

## Test cases

### T1 — [name]
- Input: [...]
- Expected: [...]

## Out of scope for v1

- [List intentionally absent features]
```

## Worked example

### Input

```
skill_name: hello-world
description: A starter skill that prints a greeting.
```

### Output

A new directory `skills/hello-world/` with the full scaffold, pre-filled
with the skill name and description, ready for the author to add real
references, prompts, templates, schemas, and fixtures.

## Verification before returning

Run a self-audit on the scaffold:

- All 7 audit dimensions score ≥4
- No forbidden folders present
- Naming consistent (kebab-case throughout)
- Plugin name matches across `plugin.json`, directory, and `SKILL.md`

If any check fails, fix the scaffold before returning.

## Negative example

### Input

```
skill_name: Hello_World
description: ""
```

### Output

```
(rejected — name is not kebab-case; description is empty)
```

Reject input that violates the naming rules or that lacks a description.
Ask the user to correct before scaffolding.
