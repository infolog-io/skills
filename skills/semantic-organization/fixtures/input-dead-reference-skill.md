---
type: fixture
---

# Fixture — a skill with dead references

A textual representation of a skill that scores well on all eight
dimensions but fails the reference-integrity gate. The gate forces
`broken`. This fixture exercises both reference forms: a code-span token
and a markdown link. See `references/okf-alignment.md`.

## Tree

```
skills/example-dead-ref/
├── .claude-plugin/
│   └── plugin.json              # name: example-dead-ref, v0.1.0, 40-word description
├── SKILL.md                     # frontmatter, triggers, references
├── README.md                    # 170 words, what + when + install
├── TESTS.md                     # end conditions, 4 test cases, out-of-scope
└── references/
    ├── core-framework.md
    └── index.md
```

## SKILL.md references (the defect)

The SKILL.md body contains these reference tokens:

- `references/core-framework.md` — resolves. Real file. PASS.
- `references/missing-rubric.md` — code-span token. No such file. DEAD.
- A markdown link `[the workflow](references/workflow.md)` — no such file. DEAD.
- `<theme>/references/tokens.md` — placeholder. Exempt, not resolved.

## Forbidden-layout check

- No `plugins/` wrapper: PASS
- Plugin manifest inside the skill folder: PASS

## Expected audit result

```
Semantic Organization Audit — example-dead-ref

Profile: full-shape

Skill-layer (spec):
- S1. SKILL.md presence/validity:  5 — frontmatter valid; name + description compliant
- S2. Naming conformance:          5 — all 3 name locations agree
- S3. Body discipline:             5 — under 500 lines; references shallow
- S4. Folder discipline:           5 — spec folders only; no forbidden

Marketplace-layer:
- P1. Plugin manifest:             5 — valid, inside skill folder
- P2. README discipline:           5 — 170 words; what/when/install
- P3. TESTS.md presence/quality:   4 — end conditions + 4 test cases
- P4. Migration health:            5 — folders sized appropriately

Reference-integrity gate:          FAIL (dead: SKILL.md → references/missing-rubric.md; SKILL.md → references/workflow.md)
Recommended next change:           Create the two missing references or remove the dead tokens from SKILL.md
Verdict:                           broken (reference-integrity gate fails)
Confidence:                        High
```
