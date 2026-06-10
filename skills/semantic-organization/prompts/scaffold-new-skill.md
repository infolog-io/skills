# Prompt — Scaffold a new skill

**Purpose:** Generate the canonical folder tree and placeholder files for a
new skill. The scaffold must pass the audit rubric at ≥4 on every
dimension on first emission.

## Input contract

The user provides (or the model asks for):

- **`skill_name`** — kebab-case, unique within the marketplace, ≤30 chars
- **`description`** — triggering conditions only; see the description rule below
- **`profile`** — `single-rule` or `full-shape`; gates which folders are emitted
- **`marketplace_path`** — default `infolog-io/skills` (the path under `skills/`)
- **`triggers`** (optional) — list of activation phrases; default to a generic set
- **`primary_artifact`** (optional) — name of the canonical output (e.g., "Job Article")

## Output contract

A folder tree at `skills/<skill_name>/` — flat, matching the canonical
layout in this skill's SKILL.md (the single canonical copy of the tree).
No `plugins/` wrapper.

Both profiles always get:

```
skills/<skill_name>/
├── .claude-plugin/
│   └── plugin.json                       # pre-filled manifest
├── SKILL.md                              # frontmatter + flow skeleton
├── README.md                             # skeleton ≤200 words
└── TESTS.md                              # skeleton with end-conditions section
```

Folder emission is gated by `profile` — not every skill needs every
folder:

- **`single-rule`** — emit NO sub-folders. The SKILL.md body carries
  everything.
- **`full-shape`** — emit only the folders the skill actually needs, and
  at least one supporting folder (`references/`, `scripts/`, `assets/`,
  or an accepted convention folder such as `prompts/`, `templates/`,
  `schemas/`, `fixtures/`). Never emit empty placeholder folders with
  `.gitkeep` "just in case" — ask which folders the skill's content
  requires and emit only those.

## The description rule (applies to every scaffolded skill)

The frontmatter `description` is the skill's discovery surface. It must
contain **triggering conditions ONLY**:

- "Use when..." style, third person, under 500 characters
- Include concrete activation phrases (quoted) and the slash command
- NO workflow summary, NO output summary, NO feature list — what the
  skill does belongs in the SKILL.md body, not the description

**Good** (triggers only):

```yaml
description: >
  Use when extracting structured job data from interview transcripts.
  Triggers: "extract from interview", "turn this transcript into a Job
  Article", "/extract-job", or any request to classify interview
  statements into job stories.
```

**Bad** (what + when — rejected):

```yaml
description: >
  Parses interview transcripts, classifies statements by job type, and
  renders a Job Article with citations. Use when processing interviews.
```

Why it fails: it leads with a workflow/output summary ("parses...
classifies... renders") and buries a vague trigger at the end. Rewrite
so every clause describes WHEN to activate, not WHAT happens after.

## Pre-filled content

### `plugin.json`

```json
{
  "name": "<skill_name>",
  "version": "0.1.0",
  "description": "<same triggers-only description as the SKILL.md frontmatter>",
  "author": { "name": "Information Logistics", "url": "https://github.com/infolog-io" }
}
```

### `SKILL.md`

```
---
name: <skill_name>
description: >
  Use when <triggering condition>. Triggers: "<phrase 1>", "<phrase 2>",
  "/<skill_name>", or <catch-all condition>.
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

<one-paragraph what + when>

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

## Register in the marketplace

After emitting the scaffold, add the plugin entry to
`.claude-plugin/marketplace.json` at the repo root — without this entry
the skill is not installable via `claude plugin install`:

```json
{
  "name": "<skill_name>",
  "description": "<same triggers-only description>",
  "source": "./skills/<skill_name>",
  "version": "0.1.0",
  "category": "<engineering | design | ...>",
  "author": { "name": "Information Logistics" }
}
```

## Worked example

### Input

```
skill_name: hello-world
description: Use when the user asks for a greeting demo. Triggers: "say hello", "/hello-world".
profile: single-rule
```

### Output

A new directory `skills/hello-world/` containing only `SKILL.md`,
`README.md`, `TESTS.md`, and `.claude-plugin/plugin.json` (single-rule:
no sub-folders), pre-filled with the skill name and description, plus a
new plugin entry in the root `.claude-plugin/marketplace.json`.

## Verification before returning

Run a self-audit on the scaffold:

- All 8 audit dimensions score ≥4 (see `references/audit-rubric.md`)
- No forbidden folders present; no empty `.gitkeep` placeholder folders
- Naming consistent (kebab-case throughout)
- Plugin name matches across `plugin.json`, directory, and `SKILL.md`
- Description is triggers-only, "Use when..." style, <500 chars
- Plugin entry exists in the root `.claude-plugin/marketplace.json`

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

Reject input that violates the naming rules, lacks a description, or
supplies a "what + when" description (workflow summary) instead of a
triggers-only one. Ask the user to correct before scaffolding.
