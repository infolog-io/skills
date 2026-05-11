# Naming Rules

A file name is a contract. The reader infers the file's purpose from its
name without opening it. These rules make that contract reliable.

## Case

**Always kebab-case.** Never `snake_case`, `camelCase`, `PascalCase`, or
`Title-Case`. Across every file, folder, and identifier in the skill.

| Pass | Fail |
|---|---|
| `extract-from-interview.md` | `ExtractFromInterview.md` |
| `job-statement-grammar.md` | `job_statement_grammar.md` |
| `tufte-principles.md` | `TuftePrinciples.md` |

Exception: configuration files that the platform demands in another case
(`SKILL.md`, `README.md`, `TESTS.md`). Their case is fixed; the rest is yours.

## Role-noun for artifacts; verb-led for actions

The file name reflects the folder's role.

### In `references/` — nouns

Files name a concept, framework, or rule set. Read-only knowledge.

| Pass | Fail | Why |
|---|---|---|
| `tufte-principles.md` | `apply-tufte.md` | reference is the principles, not the action |
| `job-statement-grammar.md` | `validate-grammar.md` | reference is the grammar, not the act of validating |
| `color-palette.md` | `pick-colors.md` | reference is the palette, not the picking |

### In `prompts/` — verb-led

Files name an action. Each file is one operation.

| Pass | Fail | Why |
|---|---|---|
| `extract-from-interview.md` | `interview-prompt.md` | name the action, not the input |
| `cluster-and-score.md` | `clustering.md` | verbs are precise; gerunds are vague |
| `audit-existing-skill.md` | `audit.md` | name the target too — "audit what?" |

### In `templates/` — noun, prefixed `template-` or named for the artifact

The artifact's shape. Use `template-<artifact>.md` or just `<artifact>.md` if
unambiguous.

| Pass | Fail |
|---|---|
| `job-article.md` | `template.md` |
| `template-audit-report.md` | `audit.md` |

### In `schemas/` — noun, named for what is validated

The schema validates a specific artifact; use that artifact's name.

| Pass | Fail |
|---|---|
| `job-article.json` | `schema.json` |
| `audit-report.json` | `validator.json` |

### In `fixtures/` — paired prefixes `input-` and `expected-`

Every input has a matching expected output (or expected-fail flag).

| Pass | Fail |
|---|---|
| `input-interview-sample.md` + `expected-job-article.md` | `sample1.md` + `out1.md` |
| `input-broken-skill/` + `expected-audit.md` | `bad-example/` + `result.md` |

## Specificity

Every name must distinguish itself from its siblings.

| Pass | Fail | Why |
|---|---|---|
| `extract-from-interview.md` vs. `extract-from-tickets.md` | `extract1.md` vs. `extract2.md` | numbers carry no meaning |
| `audit-rubric.md` vs. `audit-summary.md` | `audit.md` + a second file you can't tell apart | the suffix encodes the difference |

## Length

| Length | Meaning |
|---|---|
| 1 word | Reserved for canonical artifacts: `SKILL.md`, `README.md`, `TESTS.md` |
| 2–4 hyphen-separated words | Default. `job-statement-grammar.md`, `extract-from-interview.md` |
| 5+ words | Acceptable if the precision matters. `evaluate-folder-migration-readiness.md` |
| 1 generic word like `prompt.md` or `template.md` | Always wrong |

## Skill name = plugin name

The plugin name in `.claude-plugin/plugin.json`, the directory under
`plugins/`, the directory under `skills/`, and the `name` field in
`SKILL.md` frontmatter must all match exactly.

| Pass | Fail |
|---|---|
| `plugins/jtbd-prd/skills/jtbd-prd/` with `name: jtbd-prd` everywhere | `plugins/jtbd_prd/skills/JTBD/` with mismatched names |

## Reserved names

These names mean specific things; never use them for something else:

| Name | Meaning |
|---|---|
| `SKILL.md` | The skill's entry point |
| `README.md` | The plugin's overview |
| `TESTS.md` | The plugin's test plan |
| `plugin.json` | The plugin manifest |
| `marketplace.json` | The marketplace manifest |

## Forbidden in names

| Token | Why |
|---|---|
| `_v1`, `_v2`, `_old`, `_new` | Use git history, not filename suffixes |
| `_final`, `_draft`, `_wip` | Same |
| `_copy`, `_backup` | Same |
| Dates in names like `audit-2026-04-12.md` | Unless the file is genuinely time-bound (logs, dated reports) |
| `temp`, `tmp`, `scratch` | If it's worth committing, name it properly |

## Worked transformations

| Before | After |
|---|---|
| `helpers/utils.md` | Split into role folders; each file gets a verb-led or noun-led name |
| `prompt.md` | `extract-from-interview.md` (or whatever the actual action is) |
| `MyTemplate.md` | `my-template.md` then move to `templates/` |
| `code/extract.py` | `tools/extract-from-interview.py` |
| `examples/sample1.md` | `fixtures/input-interview-sample.md` + matching `expected-*.md` |

## Self-check before commit

Before committing a new file, ask:

1. Is the case kebab-case?
2. Does the name match the role of its folder (noun for knowledge, verb for action)?
3. Is the name specific — would a reader guess its purpose?
4. Is the name unique among its siblings?
5. Does the name include any forbidden tokens?

If any answer is no, rename before commit.
