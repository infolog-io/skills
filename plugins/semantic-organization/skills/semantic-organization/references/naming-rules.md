# Naming Rules

A file name is a contract. The reader infers the file's purpose from its
name without opening it. These rules make that contract reliable.

The spec rules below come from https://agentskills.io/specification and are
non-negotiable. Convention rules are marketplace-specific and apply across
infolog-io plugins.

## Skill name (spec-mandated)

| Rule | Source |
|---|---|
| 1–64 characters | Spec |
| Lowercase alphanumeric (`a-z`, `0-9`) and hyphens only | Spec |
| Must not start or end with a hyphen | Spec |
| Must not contain consecutive hyphens (`--`) | Spec |
| Must match the parent directory name exactly | Spec |

| Pass | Fail | Why |
|---|---|---|
| `pdf-processing` | `PDF-Processing` | uppercase forbidden |
| `code-review` | `-pdf` | leading hyphen |
| `data-analysis` | `pdf--processing` | consecutive hyphens |
| `my-skill` | `my_skill` | underscores forbidden |

The same name appears in four places — all must match:
1. Parent directory name (`plugins/<name>/skills/<name>/`)
2. `plugin.json` `name` field
3. `SKILL.md` frontmatter `name` field
4. The directory under `skills/`

## Description (spec-mandated)

| Rule | Source |
|---|---|
| 1–1024 characters | Spec |
| Names what the skill does AND when to use it | Spec |
| Includes keywords agents look for | Spec recommendation |

**Good:** "Extracts text and tables from PDF files, fills PDF forms, and
merges multiple PDFs. Use when working with PDF documents or when the user
mentions PDFs, forms, or document extraction."

**Bad:** "Helps with PDFs."

## SKILL.md body (spec-recommended)

| Rule | Source |
|---|---|
| Under 500 lines | Spec recommendation |
| File references one level deep from SKILL.md | Spec recommendation |
| No restrictions on internal format | Spec |

## File naming inside `references/`, `scripts/`, `assets/`

Convention rules (marketplace, not spec).

### Case

Kebab-case throughout. Never `snake_case`, `camelCase`, `PascalCase`, or
`Title-Case`.

Exception: platform-required names keep their case (`SKILL.md`,
`README.md`, `TESTS.md`, `LICENSE`, `LICENSE.txt`).

| Pass | Fail |
|---|---|
| `tufte-principles.md` | `TuftePrinciples.md` |
| `chart-patterns.md` | `chart_patterns.md` |

### Inside `references/` — nouns

Files name a concept, framework, or rule set.

| Pass | Fail | Why |
|---|---|---|
| `tufte-principles.md` | `apply-tufte.md` | reference is the principles, not the action |
| `job-statement-grammar.md` | `validate-grammar.md` | reference is the grammar, not the act |
| `color-palette.md` | `pick-colors.md` | reference is the palette |

### Inside `scripts/` — verb-led or named for the operation

Files name the action the script performs.

| Pass | Fail |
|---|---|
| `extract-text.py` | `extract.py` |
| `validate-schema.sh` | `script.sh` |

### Inside `assets/` — named for the artifact

Templates and schemas use the artifact's name.

| Pass | Fail |
|---|---|
| `job-article-template.md` | `template.md` |
| `audit-report-schema.json` | `schema.json` |

## Specificity

Every name distinguishes itself from its siblings.

| Pass | Fail |
|---|---|
| `extract-from-interview.md` vs. `extract-from-tickets.md` | `extract1.md` vs. `extract2.md` |
| `tufte-principles.md` vs. `chart-patterns.md` | `ref-a.md` vs. `ref-b.md` |

## Length

| Length | Use |
|---|---|
| 1 word | Reserved for platform names: `SKILL.md`, `README.md`, `TESTS.md`, `LICENSE` |
| 2–4 hyphenated words | Default |
| 5+ hyphenated words | Acceptable when the precision matters |
| 1 generic word like `template.md` | Always wrong |

## Forbidden tokens

| Token | Why |
|---|---|
| `_v1`, `_v2`, `_old`, `_new` | Use git history |
| `_final`, `_draft`, `_wip` | Same |
| `_copy`, `_backup` | Same |
| `temp`, `tmp`, `scratch` | If worth committing, name it properly |

## Reserved names

These names mean specific things; never use them for something else.

| Name | Meaning |
|---|---|
| `SKILL.md` | Skill entry point (spec-required) |
| `README.md` | Plugin overview (marketplace convention) |
| `TESTS.md` | Plugin test plan (marketplace convention) |
| `LICENSE` / `LICENSE.txt` | Standard license file |
| `plugin.json` | Plugin manifest |
| `marketplace.json` | Marketplace manifest |

## Self-check before commit

1. Is the case kebab-case (or a reserved platform name)?
2. Does the name match the role of its folder?
3. Is the name specific?
4. Is the name unique among its siblings?
5. Does the name contain forbidden tokens?
6. If this is a skill name, does it match the parent directory and all four declared locations?

If any answer is no, rename before commit.
