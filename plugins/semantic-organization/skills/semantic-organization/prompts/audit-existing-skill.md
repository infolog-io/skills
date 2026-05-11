# Prompt — Audit an existing skill

**Purpose:** Walk a skill's file tree, score it against the 7-dimension
rubric in `references/audit-rubric.md`, and emit a Semantic Organization
Audit with a verdict.

## Input contract

A path to a skill directory. The skill is expected to live under
`plugins/<plugin-name>/` and contain `skills/<skill-name>/` internally.

## Output contract

A markdown audit report following the format in
`references/audit-rubric.md`, plus an actionable findings section.

## Procedure

1. **List the file tree.** Walk every file and folder under
   `plugins/<plugin-name>/`. Stop at depth 5.

2. **Score each of the 7 dimensions** by checking against
   `references/folder-roles.md`, `references/naming-rules.md`, and
   `references/migration-triggers.md`.

3. **For each dimension**, write a one-sentence reason citing specific
   files. "Score 3 — `helpers/` folder violates folder-role rule; rename
   or split."

4. **Apply verdict thresholds** from `references/audit-rubric.md`:
   - All dimensions ≥4 → `semantically-healthy`
   - Any dimension at 2–3, none at 1 → `drifting`
   - Any dimension at 1, or ≥3 dimensions at 2 → `broken`

5. **List specific actionable findings** by category:
   - Renames (file or folder)
   - Deletions (forbidden folders)
   - Migrations (folders that should be sibling skills)
   - Additions (missing required files like TESTS.md, README.md)

6. **Pick one recommended next change** — the highest-leverage fix. If
   verdict is `broken`, this is the fix that moves it to `drifting`. If
   `drifting`, the fix that moves it to `semantically-healthy`.

## Worked example

### Input

```
plugins/example-skill/
├── README.md           (450 words, includes a changelog)
├── src/                (Python helpers)
├── examples/
│   ├── sample1.md
│   └── output1.md
└── skills/example-skill/
    ├── SKILL.md
    ├── references/
    └── prompts/
        ├── do-stuff.md
        └── helpers.md
```

### Output

```markdown
# Semantic Organization Audit — example-skill

- Folder role clarity:        2 — `src/` and `examples/` are forbidden folder names
- Folder responsibility:      3 — `helpers.md` inside prompts/ mixes action with utility
- Common shape conformance:   2 — missing `TESTS.md`, `templates/`, `schemas/`, `fixtures/`
- Naming consistency:         3 — files mostly kebab-case but `sample1.md` is generic
- Migration health:           5 — no overgrown folders; sized appropriately
- README discipline:          1 — 450 words including a changelog
- TESTS.md presence/quality:  1 — file is absent
- Recommended next change:    Create TESTS.md and trim README to ≤200 words
- Verdict:                    broken
- Confidence:                 High

## Findings

### Renames
- `prompts/do-stuff.md` → `prompts/do-<the-actual-thing>.md` (name the action)
- `prompts/helpers.md` → split into role folders; "helpers" is forbidden
- `examples/sample1.md` → `fixtures/input-<descriptive-name>.md`
- `examples/output1.md` → `fixtures/expected-<descriptive-name>.md`

### Deletions / moves
- `src/` → move contents to `tools/` if scripts are needed, otherwise delete
- `examples/` → forbidden; move contents to `fixtures/`

### Migrations
- None (no folder meets migration triggers).

### Additions
- Create `TESTS.md` at the plugin root with end conditions
- Create `skills/example-skill/templates/` (empty or with first canonical template)
- Create `skills/example-skill/schemas/` (empty or with first schema)
- Create `skills/example-skill/fixtures/` with paired input/expected files

### README rewrite
Strip changelog. Cut to ≤200 words. Sections: what, when to use, install, triggers.
```

## Negative example

### Input

```
A skill that is fully canonical (matches jtbd-prd or tufte-love patterns)
```

### Output

```markdown
- Folder role clarity:        5
- Folder responsibility:      5
- Common shape conformance:   5
- Naming consistency:         5
- Migration health:           5
- README discipline:          5
- TESTS.md presence/quality:  5
- Recommended next change:    none — skill is canonical
- Verdict:                    semantically-healthy
- Confidence:                 High
```

Even healthy skills should be audited periodically — drift creeps in with
each feature addition.

## Edge cases

| Situation | Handling |
|---|---|
| Skill has `tools/` with scripts | Acceptable optional folder; pass with score 5 on dim 1 if usage is justified |
| Skill has `assets/` with images | Acceptable optional folder |
| Skill has `migrations/` because v0.2 was a breaking change | Acceptable optional folder; verify content is migration notes |
| Skill is missing one required folder but the omission is reasoned in TESTS.md | Score 4 instead of 1 on common shape conformance |
| Skill mixes English and another language in file names | Score 3 on naming consistency; flag for normalization |

## Verification before returning output

- All 7 dimensions scored with a one-sentence reason
- Verdict matches the threshold rules exactly
- Findings cite specific file paths, not vague pointers
- Recommended next change is concrete and immediately actionable
