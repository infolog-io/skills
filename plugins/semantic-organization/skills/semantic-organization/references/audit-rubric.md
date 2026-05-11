# Semantic Organization Audit Rubric

Score each dimension from 1 to 5.

- 1 = broken or misleading
- 2 = weak
- 3 = acceptable
- 4 = strong
- 5 = excellent

## 1. Folder Role Clarity

Questions:

- Does every folder name a role (knowledge, action, artifact, contract, test data)?
- Could a reader who knows the role taxonomy find any file without exploring?
- Are forbidden folders (`src/`, `utils/`, `helpers/`, `common/`, `misc/`) absent?

Score:

- 1: Folders name implementation, not role. Reader must explore.
- 3: Most folders name roles; a few are vague.
- 5: Every folder name maps to a canonical role.

## 2. Folder Responsibility Purity

Questions:

- Does each folder hold exactly one kind of thing?
- Are references and prompts mixed? Schemas and templates?
- Are there orphan files at the skill root that belong in a folder?

Score:

- 1: Folders mix knowledge, actions, and artifacts.
- 3: One or two folders mix concerns.
- 5: Every folder is pure — one role, one responsibility.

## 3. Common Shape Conformance

Questions:

- Does the plugin root contain `.claude-plugin/plugin.json`, `README.md`, `TESTS.md`?
- Does the skill have `SKILL.md` at its root?
- Does the skill have at minimum `references/`, `prompts/`, `templates/`, `schemas/`, `fixtures/` (or justified absence)?
- Does the plugin name match across `plugin.json`, the directory name, and `SKILL.md` frontmatter?

Score:

- 1: Skill is missing core files (no SKILL.md, no README, no TESTS.md).
- 3: Most files present; minor mismatches.
- 5: Full canonical shape. Names match. All required files present.

## 4. Naming Consistency

Questions:

- Is everything kebab-case (folders, files, except platform-required `SKILL.md`, `README.md`, `TESTS.md`)?
- Are references named as nouns? Prompts named with verbs?
- Are templates and schemas named for the artifact they shape?
- Are fixtures paired with `input-` / `expected-` prefixes?
- Are forbidden tokens (`_v1`, `_old`, `_final`, `temp`) absent?

Score:

- 1: Mixed cases throughout. Generic names like `prompt.md` or `template.md`.
- 3: Mostly kebab-case; some misnamed files.
- 5: Every file follows the role-noun or verb-led naming rule.

## 5. Migration Health

Questions:

- Does any folder meet the migration triggers (≥5 prompts, own rubric, own verdict semantics, installable independently)?
- Has the skill outgrown its scope without spinning out siblings?
- Are there sub-skills hidden inside this skill (folders with their own `plugin.json`)?

Score:

- 1: Multiple folders should be sibling skills but remain trapped.
- 3: One overgrown folder identified; migration plan pending.
- 5: Every folder is correctly sized — none over-promoted, none under-promoted.

## 6. README Discipline

Questions:

- Is the plugin's README ≤200 words?
- Does it state: what the skill does, when to use it, and how to install it?
- Is it free of marketing copy, history, and changelogs?

Score:

- 1: README missing, or far over the word budget, or buries the install command.
- 3: README is present and accurate but verbose.
- 5: Exactly the right size; clear what / when / install in under 200 words.

## 7. TESTS.md Presence and Quality

Questions:

- Is `TESTS.md` present at the plugin root?
- Does it list explicit end conditions ("skill ships when X is true")?
- Does it enumerate concrete test cases with inputs and expected outputs?
- Are out-of-scope items declared, so reviewers know what is intentionally absent?

Score:

- 1: No TESTS.md, or TESTS.md is aspirational with no specifics.
- 3: TESTS.md exists but is thin on concrete cases.
- 5: End conditions are unambiguous; ≥5 test cases with inputs and outputs; out-of-scope explicitly listed.

## Final Audit Summary

Use this format:

```text
Semantic Organization Audit
- Folder role clarity:        [1-5] — [reason]
- Folder responsibility:      [1-5] — [reason]
- Common shape conformance:   [1-5] — [reason]
- Naming consistency:         [1-5] — [reason]
- Migration health:           [1-5] — [reason]
- README discipline:          [1-5] — [reason]
- TESTS.md presence/quality:  [1-5] — [reason]
- Recommended next change:    [single highest-leverage fix]
- Verdict:                    semantically-healthy | drifting | broken
- Confidence:                 High | Medium | Low
```

## Verdict thresholds

| Verdict | Rule |
|---|---|
| `semantically-healthy` | All dimensions ≥ 4; no dimension < 3 |
| `drifting` | One or more dimensions at 2–3; no dimension at 1 |
| `broken` | Any dimension at 1, OR ≥3 dimensions at 2 |

## Priority rule

If a skill is well-named but missing TESTS.md, score it low.
If it has TESTS.md but folders mix roles, score it low.
Semantic organization is a system property — every dimension matters.
