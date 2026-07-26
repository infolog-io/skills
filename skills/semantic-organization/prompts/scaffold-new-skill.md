---
type: prompt
---

# Prompt — Scaffold a new skill

**Purpose:** Generate the canonical folder tree and placeholder files for a
new skill. The scaffold must pass the audit rubric at ≥4 on every
dimension on first emission.

## Input contract

The user provides (or the model asks for):

- **`skill_name`** — kebab-case, unique within the marketplace, ≤30 chars
- **`description`** — one sentence, what the skill does and when to use it
- **`profile`** — `single-rule` or `full-shape`; default to `single-rule` unless multiple modes, references, scripts, or artifacts are already known
- **`target_host`** — default `infolog-marketplace`; see `references/host-standards.md`
- **`marketplace_path`** — default `infolog-io/skills` when target host is `infolog-marketplace`
- **`triggers`** (optional) — list of activation phrases; default to a generic set
- **`primary_artifact`** (optional) — name of the canonical output (e.g., "Job Article")

## Output contract

A complete profile-aware folder tree for the chosen target host. In this
repo, default to `skills/<skill_name>/` — flat, matching the Anthropic
Agent Skills convention. No `plugins/` wrapper for `infolog-marketplace`.

For single-rule skills, emit only the identity files:

```
skills/<skill_name>/
├── .claude-plugin/
│   └── plugin.json                       # pre-filled manifest
├── SKILL.md                              # frontmatter + flow skeleton
├── README.md                             # skeleton ≤200 words
└── TESTS.md                              # skeleton with end-conditions section
```

For full-shape skills, add only folders that contain a named first file or
an `index.md` explaining the layer:

```
skills/<skill_name>/
├── .claude-plugin/
│   └── plugin.json
├── SKILL.md
├── README.md
├── TESTS.md
├── references/
│   └── index.md                          # folder map
├── prompts/
│   └── <verb-led-mode>.md                 # first stage contract
└── templates/ | schemas/ | fixtures/      # only when a primary artifact exists
```

For `codex-repo-skill`, root the tree at `.agents/skills/<skill_name>/`
and omit Claude marketplace files unless explicitly requested.

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

See references/index.md for the folder map.
- references/<file>.md — [purpose]

## Triggers

| Phrase | Mode |
|---|---|
| <phrase> | <mode> |
```

For single-rule skills, omit the Operating modes and References sections
unless a real mode or reference exists. For `codex-repo-skill`, omit
`.claude-plugin/plugin.json`, README.md, and TESTS.md unless the user asks
for marketplace packaging too.

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

A new directory `skills/hello-world/` with a profile-aware scaffold,
pre-filled with the skill name and description. If the skill is
single-rule, it contains only the identity files. If it is full-shape, it
contains only folders with real first files or an index.

## Verification before returning

Run a self-audit on the scaffold:

- All 8 audit dimensions score ≥4
- Reference-integrity gate passes (every reference in SKILL.md resolves)
- No forbidden folders present
- Naming consistent (kebab-case throughout)
- Plugin name matches across `plugin.json`, directory, and `SKILL.md`
- Host-standard facet passes for the chosen `target_host`
- Context-fit advisory passes: each emitted folder carries one real layer

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
