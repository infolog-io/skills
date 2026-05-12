# Fixture — a drifting skill

A skill that started canonical but has accumulated drift. The audit prompt
should classify this as `drifting` with specific actionable findings.

## Tree

```
plugins/example-drifted/
├── .claude-plugin/
│   └── plugin.json                  # name: example-drifted, v0.4.0, 80-word description
├── README.md                        # 340 words — too long, includes a changelog
├── TESTS.md                         # exists but only 2 vague test cases
└── skills/example-drifted/
    ├── SKILL.md                     # fine, but lists references that no longer exist
    ├── references/
    │   ├── core-framework.md
    │   └── HelperFunctions.md       # PascalCase — fails naming rule
    ├── prompts/
    │   ├── extract.md               # too generic — should name the action precisely
    │   ├── classify-and-tag.md
    │   └── render-output.md
    ├── utils/                       # FORBIDDEN folder
    │   └── shared-stuff.md
    └── fixtures/
        ├── sample1.md               # generic name
        └── sample2.md               # unpaired with expected-* file
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

## Expected audit result

```
Semantic Organization Audit — example-drifted

- Folder role clarity:        3 — utils/ folder is forbidden
- Folder responsibility:      4 — folders mostly pure; utils/ violates
- Common shape conformance:   2 — missing templates/ and schemas/
- Naming consistency:         2 — PascalCase file, generic filenames
- Migration health:           5 — no overgrown folders
- README discipline:          2 — 340 words; includes changelog
- TESTS.md presence/quality:  3 — exists but thin on specifics
- Recommended next change:    Delete utils/ and rename files to follow naming rules
- Verdict:                    drifting
- Confidence:                 High
```
