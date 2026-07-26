---
type: reference
---

# Interpretable Context Layers

Semantic structure is useful only when it helps an agent decide what to
load, what to do next, and what output to produce. Folder names are the
visible part; context layers are the architecture underneath.

## The five layers

| Layer | Question answered | Typical files |
|---|---|---|
| Identity | What is this capability, and when should it activate? | `SKILL.md`, `README.md`, `.claude-plugin/plugin.json` |
| Routing | Which mode should run for this request? | SKILL.md triggers, operating-mode table, `references/index.md` |
| Stage contract | What exact procedure runs at this stage? | `prompts/` files, mode-specific checklists |
| Reference material | What background knowledge is loaded on demand? | `references/` files |
| Working artifact | What input/output shape proves the work is real? | `templates/`, `schemas/`, `fixtures/`, `assets/`, `scripts/` |

This maps the "folders over agents" principle into skill structure. The
agent is replaceable. The context architecture should survive host changes,
model changes, and framework changes.

## Context-fit checks

Ask these before adding or moving a file:

1. Which layer does this file serve?
2. Which agent decision becomes easier because this file exists?
3. Is this file loaded at activation time, mode-selection time, or only
   after a mode is chosen?
4. Does the file mix two layers that should be split?
5. Could a new agent understand the folder role without opening the file?

## Common mismatches

| Mismatch | Why it drifts | Better home |
|---|---|---|
| Long theory in `prompts/` | Stage contracts become slow to scan | `references/` |
| Step-by-step operating instructions in `references/` | Knowledge files start acting like hidden prompts | `prompts/` |
| Output examples buried in `SKILL.md` | Activation body becomes too large | `fixtures/` or `templates/` |
| Empty folders created "just in case" | They communicate fake architecture | Omit until the first real file exists |
| Tool code in `references/` | Executable behavior hides as prose | `scripts/` |

## Profile-aware scaffolding

A single-rule skill should usually have only identity files:
`SKILL.md`, `.claude-plugin/plugin.json`, `README.md`, and `TESTS.md`.
It should not receive empty context folders.

A full-shape skill adds folders only when the layer exists:

- `prompts/` when there are multiple stage contracts or modes.
- `references/` when background knowledge should load on demand.
- `templates/`, `schemas/`, `fixtures/`, or `assets/` when the skill has
  a canonical output or reusable support artifact.
- `scripts/` when executable code is part of the capability.

## Worked example

A skill that only enforces "always ask for a success criterion before
estimating" is single-rule. Its rule fits in SKILL.md; adding empty
`references/` and `prompts/` makes the structure noisier.

A skill that audits a repository has identity in SKILL.md, routing for
"audit", "rename", and "migration" modes, prompts for each mode, references
for the rubric, and fixtures proving expected outputs. That is full-shape.
