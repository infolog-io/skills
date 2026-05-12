# Fixture — a drifting skill

A skill that started canonical but has accumulated drift. The audit prompt
should classify this as `drifting` with specific actionable findings.

## Tree

```
skills/example-drifted/
├── .claude-plugin/
│   └── plugin.json               # name: example-drifted, v0.4.0, 80-word description
├── SKILL.md                      # fine, but lists references that no longer exist
├── README.md                     # 340 words — too long, includes a changelog
├── TESTS.md                      # exists but only 2 vague test cases
├── references/
│   ├── core-framework.md
│   └── HelperFunctions.md        # PascalCase — fails naming rule
├── prompts/
│   ├── extract.md                # too generic — should name the action precisely
│   ├── classify-and-tag.md
│   └── render-output.md
├── utils/                        # FORBIDDEN folder
│   └── shared-stuff.md
└── fixtures/
    ├── sample1.md                # generic name
    └── sample2.md                # unpaired with expected-* file
```

## Drift findings

| Violation | Fix |
|---|---|
| `utils/` folder is forbidden | Split contents by role or delete |
| `HelperFunctions.md` is PascalCase | Rename to `helper-functions.md`, then question if it belongs in `references/` at all |
| `extract.md` is too generic | Rename to `extract-from-<source-name>.md` |
| `sample1.md` and `sample2.md` are unpaired and unnamed | Rename to `input-*.md` and create matching `expected-*.md` |
| README is 340 words with a changelog | Strip changelog; trim to ≤200 words |
| TESTS.md has only 2 vague cases | Add specific test cases with concrete inputs and outputs |
| Missing `templates/` folder | Add canonical output template |
| Missing `schemas/` folder | Add JSON schema for skill output |

## Forbidden-layout check

- No `plugins/` wrapper directory: PASS (structure is flat)
- No double-nested `skills/<name>/skills/<name>/`: PASS
- Plugin manifest inside the skill folder: PASS

## Expected audit result

```
Semantic Organization Audit — example-drifted

Profile: full-shape

Skill-layer (spec):
- S1. SKILL.md presence/validity:  4 — frontmatter valid; references stale
- S2. Naming conformance:          4 — names agree across the three locations
- S3. Body discipline:             4 — under 500 lines but lists missing refs
- S4. Folder discipline:           2 — utils/ is forbidden; missing templates/ and schemas/

Marketplace-layer:
- P1. Plugin manifest:             5 — valid, inside skill folder
- P2. README discipline:           2 — 340 words; includes a changelog
- P3. TESTS.md presence/quality:   3 — exists but thin on specifics
- P4. Migration health:            5 — no overgrown folders

Recommended next change:           Delete utils/ and rename files to follow naming rules
Verdict:                           spec-compliant, marketplace-drift
Confidence:                        High
```
