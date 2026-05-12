# Semantic Organization Audit Rubric

Two layers, two rubrics. Score each dimension from 1 to 5.

- 1 = broken or misleading
- 2 = weak
- 3 = acceptable
- 4 = strong
- 5 = excellent

## Skill-layer rubric (spec compliance)

Per https://agentskills.io/specification.

### S1. SKILL.md presence and validity

- File exists at the skill root.
- Has YAML frontmatter.
- `name` and `description` are present and valid.

Score:
- 1: Missing, invalid frontmatter, or naming rules violated.
- 3: Present but underdeveloped.
- 5: Compliant; description names both what and when.

### S2. Naming conformance

- `name` matches parent directory.
- `name` is 1-64 chars, kebab-case, no leading/trailing/consecutive hyphens.
- All four name locations agree (parent dir, `plugin.json`, `SKILL.md` frontmatter, skill subdir).

Score:
- 1: Name violates spec or names disagree across files.
- 3: Mostly compliant; minor disagreement.
- 5: Fully compliant.

### S3. Body discipline

- SKILL.md body under 500 lines.
- File references one level deep.
- No format restrictions, but structured for activation-time loading.

Score:
- 1: SKILL.md exceeds 1000 lines or references deeply nested files.
- 3: 500-1000 lines, or references go two levels deep.
- 5: Under 500 lines, references shallow.

### S4. Optional folder discipline

- If any optional folders exist, they are `scripts/`, `references/`, or `assets/`.
- Non-canonical folder names exist only when no spec folder fits.
- Forbidden folders (`src/`, `utils/`, `docs/`, etc.) absent.

Score:
- 1: Forbidden folders present.
- 3: Non-canonical folders present without clear justification.
- 5: Only spec-named folders, or non-canonical folders are documented in SKILL.md with rationale.

## Plugin-layer rubric (marketplace conventions)

For shipping in this marketplace. Not part of the spec.

### P1. Plugin manifest

- `.claude-plugin/plugin.json` exists at plugin root.
- `name`, `version`, `description` fields present.
- `name` matches the directory under `plugins/`.
- Description ≥20 characters.

Score:
- 1: Missing or invalid.
- 3: Present but description is thin.
- 5: Complete and matches all other declared names.

### P2. README discipline

- `README.md` at plugin root.
- ≤200 words.
- States what, when, install.

Score:
- 1: Missing or far over budget.
- 3: Present but verbose or unclear.
- 5: Under 200 words with clear what / when / install.

### P3. TESTS.md presence and quality

- `TESTS.md` at plugin root.
- Lists explicit end conditions ("ships when X is true").
- Enumerates concrete test cases.
- Declares out-of-scope items.

Score:
- 1: Missing, or contains only aspirations.
- 3: Present but thin on specifics.
- 5: ≥3 test cases with inputs and outputs, end conditions unambiguous, out-of-scope listed.

### P4. Migration health

- Are there sub-skills hidden inside this skill (folders with their own `plugin.json`)?
- Does any folder meet the migration triggers (≥5 prompts, own rubric, own verdicts, installable independently)?

Score:
- 1: Multiple folders should be sibling skills but remain trapped.
- 3: One overgrown folder identified; migration plan pending.
- 5: Every folder is correctly sized — none over-promoted, none under-promoted.

## Skill profiles

Not every skill needs the full plugin layer. Two profiles:

### Full-shape skill

A skill with multiple operating modes, prompts, references, and outputs.
Skills with multiple operating modes, multiple references, and optional
scripts and assets fall in this profile.

Required at minimum:
- Spec layer: SKILL.md + references/ (recommended) + assets/ (recommended) when content warrants
- Plugin layer: plugin.json, README.md, TESTS.md

### Single-rule skill

A meta-skill that states one durable rule. The skill IS the rule. No
modes, no prompts, no templates.

A skill that states a single durable rule via SKILL.md alone — no
sub-folders required.

Required at minimum:
- Spec layer: SKILL.md only
- Plugin layer: plugin.json, README.md, TESTS.md

The audit must not penalize single-rule skills for not having `scripts/`,
`references/`, or `assets/`. The body of SKILL.md carries all the content.

Recognize single-rule profile when:
- SKILL.md is under 200 lines
- The skill names exactly one rule, principle, or rubric
- No mode-switching is needed

## Final Audit Summary

Use this format:

```text
Semantic Organization Audit — <skill-name>

Profile: full-shape | single-rule

Skill-layer (spec):
- S1. SKILL.md presence/validity:  [1-5] — [reason]
- S2. Naming conformance:          [1-5] — [reason]
- S3. Body discipline:             [1-5] — [reason]
- S4. Folder discipline:           [1-5] — [reason]

Plugin-layer (marketplace):
- P1. Plugin manifest:             [1-5] — [reason]
- P2. README discipline:           [1-5] — [reason]
- P3. TESTS.md presence/quality:   [1-5] — [reason]
- P4. Migration health:            [1-5] — [reason]

Recommended next change:           [single highest-leverage fix]
Verdict:                           spec-compliant + marketplace-ready
                                   | spec-compliant, marketplace-drift
                                   | spec-drift
                                   | broken
Confidence:                        High | Medium | Low
```

## Verdict thresholds

| Verdict | Rule |
|---|---|
| `spec-compliant + marketplace-ready` | All 4 skill-layer dims ≥4 AND all 4 plugin-layer dims ≥4 |
| `spec-compliant, marketplace-drift` | All 4 skill-layer dims ≥4, but ≥1 plugin-layer dim at 2-3 |
| `spec-drift` | ≥1 skill-layer dim at 2-3, none at 1 |
| `broken` | Any dim at 1 |

## Priority rule

Spec violations are always worse than marketplace drift. A skill that
ships without TESTS.md is fixable in five minutes. A skill that violates
the spec breaks composability with other agents.

When prioritizing fixes, address skill-layer drift first.
