# Fixture — a semantically-healthy skill

This is a textual representation of a well-organized skill. The audit
prompt should score this at 5/5 on every dimension.

## Tree

```
skills/example-good/
├── .claude-plugin/
│   └── plugin.json              # name: example-good, v0.1.0, 60-word description
├── SKILL.md                     # frontmatter, triggers, references, flow
├── README.md                    # 180 words, what + when + install + triggers
├── TESTS.md                     # end conditions, 6 test cases, out-of-scope listed
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
skills/<dir>:                example-good
SKILL.md frontmatter name:   example-good
```

All three match.

## Naming check

- All files kebab-case
- references named as nouns
- prompts verb-led
- templates and schemas named for the artifact
- fixtures use `input-` / `expected-` prefixes

## Forbidden-layout check

- No `plugins/` wrapper directory: PASS
- No double-nested `skills/<name>/skills/<name>/`: PASS
- Plugin manifest inside the skill folder: PASS

## Expected audit result

```
Semantic Organization Audit — example-good

Profile: full-shape

Skill-layer (spec):
- S1. SKILL.md presence/validity:  5 — frontmatter valid; name + description compliant
- S2. Naming conformance:          5 — all 3 name locations agree
- S3. Body discipline:             5 — SKILL.md under 500 lines; references shallow
- S4. Folder discipline:           5 — spec folders + documented conventions; no forbidden

Marketplace-layer:
- P1. Plugin manifest:             5 — valid, inside skill folder
- P2. README discipline:           5 — 180 words; what/when/install
- P3. TESTS.md presence/quality:   5 — end conditions + 6 test cases + out-of-scope
- P4. Migration health:            5 — folders sized appropriately

Recommended next change:           none — skill is canonical
Verdict:                           spec-compliant + marketplace-ready
Confidence:                        High
```
