# Fixture — a semantically-healthy skill

This is a textual representation of a well-organized skill. The audit
prompt should score this at 5/5 on every dimension.

## Tree

```
plugins/example-good/
├── .claude-plugin/
│   └── plugin.json                  # name: example-good, v0.1.0, 60-word description
├── README.md                        # 180 words, what + when + install + triggers
├── TESTS.md                         # end conditions, 6 test cases, out-of-scope listed
└── skills/example-good/
    ├── SKILL.md                     # frontmatter, triggers, references, flow
    ├── references/
    │   ├── core-framework.md
    │   ├── naming-conventions.md
    │   └── audit-rubric.md
    ├── prompts/
    │   ├── extract-from-source.md
    │   ├── classify-and-tag.md
    │   └── render-output.md
    ├── templates/
    │   └── output-report.md
    ├── schemas/
    │   ├── input-record.json
    │   └── output-report.json
    └── fixtures/
        ├── input-canonical-sample.md
        └── expected-canonical-output.md
```

## Frontmatter consistency

```
plugin.json name:            example-good
plugins/<dir>:               example-good
skills/<dir>:                example-good
SKILL.md frontmatter name:   example-good
```

All four match.

## Naming check

- All files kebab-case
- references named as nouns
- prompts verb-led
- templates and schemas named for the artifact
- fixtures use `input-` / `expected-` prefixes

## Expected audit result

```
Semantic Organization Audit — example-good

- Folder role clarity:        5 — every folder names a canonical role
- Folder responsibility:      5 — folders are pure; no mixing
- Common shape conformance:   5 — full canonical layout
- Naming consistency:         5 — kebab-case throughout; role-noun rules followed
- Migration health:           5 — no overgrown folders
- README discipline:          5 — 180 words; clear what/when/install
- TESTS.md presence/quality:  5 — end conditions + 6 test cases + out-of-scope
- Recommended next change:    none — skill is canonical
- Verdict:                    semantically-healthy
- Confidence:                 High
```
