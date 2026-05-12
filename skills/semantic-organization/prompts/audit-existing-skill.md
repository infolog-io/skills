# Prompt — Audit an existing skill

**Purpose:** Walk a skill's file tree, classify the skill profile,
score against the two-layer rubric in `references/audit-rubric.md`, and
emit a Semantic Organization Audit with a verdict.

## Input contract

A path to a skill directory (e.g., `skills/<skill-name>/`). The skill
folder contains both the spec-required files (SKILL.md, optional
scripts/references/assets) and the marketplace files (plugin.json,
README.md, TESTS.md) in one place — no wrapper directory.

## Output contract

A markdown audit report following the format in
`references/audit-rubric.md`, plus an actionable findings section.

## Procedure

### 1. Walk the file tree

List every file and folder under `skills/<skill-name>/`. Stop at depth 5.

Before scoring, check for forbidden layouts. If any of these appear,
the verdict is `broken` regardless of other dimensions:

- A `plugins/<name>/skills/<name>/SKILL.md` structure (old wrapper form)
- `.claude-plugin/plugin.json` outside any skill folder
- SKILL.md at the marketplace repo root (skills must live in `skills/<name>/`)

### 2. Detect profile

- **Single-rule skill**: SKILL.md is under 200 lines AND has no
  sub-folders (no `references/`, `scripts/`, `assets/`, or convention
  folders).
- **Full-shape skill**: anything else.

The profile changes which dimensions are scored strictly. Single-rule
skills are not penalized for absent sub-folders.

### 3. Score skill-layer dimensions (spec)

| Dimension | Check |
|---|---|
| S1. SKILL.md presence/validity | File exists; YAML frontmatter; `name` and `description` valid per spec |
| S2. Naming conformance | `name` matches parent dir; agrees with `plugin.json`; kebab-case; 1-64 chars; no leading/trailing/consecutive hyphens |
| S3. Body discipline | Under 500 lines; references one level deep |
| S4. Folder discipline | Only spec folders, OR non-spec folders documented and accepted per `references/spec-vs-conventions.md` |

### 4. Score plugin-layer dimensions (marketplace)

| Dimension | Check |
|---|---|
| P1. Plugin manifest | `.claude-plugin/plugin.json` present; `name`/`version`/`description` valid |
| P2. README discipline | `README.md` present; ≤200 words; what/when/install |
| P3. TESTS.md presence/quality | `TESTS.md` present; end conditions; ≥3 test cases; out-of-scope listed |
| P4. Migration health | No folders meeting migration triggers without action |

### 5. Apply verdict thresholds

| Verdict | Rule |
|---|---|
| `spec-compliant + marketplace-ready` | All 4 skill-layer dims ≥4 AND all 4 plugin-layer dims ≥4 |
| `spec-compliant, marketplace-drift` | Skill-layer all ≥4, plugin-layer has ≥1 at 2-3 |
| `spec-drift` | ≥1 skill-layer dim at 2-3, none at 1 |
| `broken` | Any dim at 1 |

### 6. Emit findings

For each dim scoring <5, list specific actions:
- Renames (file or folder)
- Deletions (forbidden folders)
- Migrations (folders meeting promotion triggers)
- Additions (missing required files)

### 7. Pick one recommended next change

The highest-leverage fix. If verdict is `broken`, this is the fix that
moves it to `spec-drift`. If `spec-drift`, the fix that moves to
`spec-compliant`. If `spec-compliant, marketplace-drift`, the fix that
moves to `marketplace-ready`.

## Output format

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
Verdict:                           [one of four]
Confidence:                        High | Medium | Low

## Findings

### Renames
- ...

### Deletions
- ...

### Migrations
- ...

### Additions
- ...
```

## Worked examples

### Full-shape skill, marketplace-ready

Input: a skill matching the canonical full-shape (SKILL.md + references/
+ prompts/ + templates/ + schemas/ + fixtures/ + plugin.json + README + TESTS).

Output:

```text
Profile: full-shape

Skill-layer:
- S1. SKILL.md presence/validity:  5 — Frontmatter valid; name + description compliant
- S2. Naming conformance:          5 — All four name locations agree
- S3. Body discipline:             5 — SKILL.md is 280 lines; refs shallow
- S4. Folder discipline:           5 — Uses spec references/; non-spec prompts/templates/schemas/fixtures all documented and accepted

Plugin-layer:
- P1. Plugin manifest:             5 — Valid
- P2. README discipline:           5 — 199 words; clear sections
- P3. TESTS.md presence/quality:   5 — End conditions + 7 test cases + out-of-scope
- P4. Migration health:            5 — Sized appropriately

Recommended next change:           none — skill is canonical
Verdict:                           spec-compliant + marketplace-ready
Confidence:                        High
```

### Single-rule skill, marketplace-drift

Input: a skill matching the single-rule shape (SKILL.md + plugin.json +
README only — no sub-folders).

Output:

```text
Profile: single-rule

Skill-layer:
- S1. SKILL.md presence/validity:  5 — Frontmatter valid
- S2. Naming conformance:          5 — Names agree
- S3. Body discipline:             5 — Under 200 lines
- S4. Folder discipline:           5 — No sub-folders, appropriate for single-rule

Plugin-layer:
- P1. Plugin manifest:             5 — Valid
- P2. README discipline:           5 — 195 words
- P3. TESTS.md presence/quality:   1 — File does not exist
- P4. Migration health:            5 — No folders to evaluate

Recommended next change:           Add TESTS.md with end conditions and test cases
Verdict:                           spec-compliant + marketplace-drift
Confidence:                        High

## Findings

### Additions
- TESTS.md at plugin root: end conditions, ≥3 test cases, out-of-scope list
```

### Spec-drift example

Input: a skill where SKILL.md `name` is `MyPDFSkill` but parent dir is `pdf-skill`.

Output:

```text
Profile: full-shape

Skill-layer:
- S1. SKILL.md presence/validity:  3 — Frontmatter valid except name field
- S2. Naming conformance:          1 — Name violates spec (uppercase); does not match parent dir
- S3. Body discipline:             5
- S4. Folder discipline:           5

[plugin-layer scores omitted for brevity]

Verdict:                           broken (S2 at 1)
Recommended next change:           Rename to comply with spec; update all four name locations
```

## Edge cases

| Situation | Handling |
|---|---|
| Skill is missing one optional spec folder it doesn't need | Score 5 — optional folders are optional |
| Skill uses non-spec folder documented in SKILL.md with rationale | Score 5 on S4 |
| Skill uses non-spec folder with no rationale | Score 3 on S4; recommend documenting or moving to spec folder |
| Single-rule skill has SKILL.md over 200 lines | Re-classify as full-shape; re-score |
| Plugin has no `skills/<name>/` wrapper, SKILL.md is at plugin root | Score 3 on P1; plugin layer assumes wrapper |

## Verification before returning output

- All 8 dimensions scored with a one-sentence reason
- Verdict matches the threshold rules exactly
- Findings cite specific file paths
- Recommended next change is concrete and immediately actionable
- Profile (single-rule vs. full-shape) is declared upfront
