# Skill Scaffold Template

This template is the canonical shape every new skill must conform to.
Used by the scaffold prompt to generate a new skill skeleton.

## Tree

Flat structure at `skills/<name>/` — matches the Anthropic Agent Skills
convention. All marketplace files (plugin.json, README, TESTS) live in
the same folder as SKILL.md. No wrapper.

```
skills/{{skill_name}}/
├── .claude-plugin/
│   └── plugin.json
├── SKILL.md
├── README.md
├── TESTS.md
├── references/
│   └── .gitkeep
├── prompts/
│   └── .gitkeep
├── templates/
│   └── .gitkeep
├── schemas/
│   └── .gitkeep
└── fixtures/
    └── .gitkeep
```

## File: `.claude-plugin/plugin.json`

```json
{
  "name": "{{skill_name}}",
  "version": "0.1.0",
  "description": "{{description}}",
  "author": { "name": "{{author_name}}", "url": "{{author_url}}" }
}
```

## File: `README.md`

```markdown
# {{skill_name}}

{{description}}

## Why

{{one_paragraph_motivation}}

## When to use

- {{use_case_1}}
- {{use_case_2}}
- {{use_case_3}}

## When not to use

- {{anti_case_1}}
- {{anti_case_2}}

## Install

\`\`\`bash
claude plugin marketplace add {{marketplace}}
claude plugin install {{skill_name}}@{{marketplace_short}}
\`\`\`

## Triggers

`{{trigger_1}}` · `{{trigger_2}}` · `/{{skill_name}}`
```

Word budget: ≤ 200.

## File: `TESTS.md`

```markdown
# {{skill_name}} — Tests & End Conditions

## End conditions (skill ships when all are true)

1. Plugin installs cleanly via `claude plugin install {{skill_name}}@{{marketplace_short}}`
2. Skill activates on every trigger phrase listed in SKILL.md
3. All referenced files exist at the paths declared in SKILL.md
4. JSON schemas validate canonical examples
5. {{skill_specific_end_condition}}

## Test cases

### T1 — {{test_name}}
- Input: {{...}}
- Expected: {{...}}

## Acceptance rubric per artifact

| Artifact | Must |
|---|---|
| SKILL.md | {{requirement}} |

## Out of scope for v1

- {{out_of_scope_1}}
```

## File: `skills/{{skill_name}}/SKILL.md`

```markdown
---
name: {{skill_name}}
description: >
  {{description}}
  Activates on {{trigger_1}}, {{trigger_2}}, or "/{{skill_name}}".
---

# {{skill_name}}

## Purpose

{{one_paragraph_purpose}}

## Operating modes

### {{mode_1_name}} mode

Trigger: {{mode_1_trigger}}

Behavior: {{mode_1_behavior}}

See `prompts/{{mode_1_prompt_file}}.md`.

## References

- `references/{{ref_1}}.md` — {{ref_1_purpose}}
- `references/{{ref_2}}.md` — {{ref_2_purpose}}

## Triggers

| Phrase | Mode |
|---|---|
| `{{trigger_1}}` | {{mode_1_name}} |
| `{{trigger_2}}` | {{mode_2_name}} |
```

## File placeholders for each canonical folder

| Folder | First file (created later, not by scaffold) |
|---|---|
| `references/` | A foundational reference (theory or rule set) |
| `prompts/` | A verb-led action file |
| `templates/` | A canonical output shape |
| `schemas/` | A JSON Schema for the output |
| `fixtures/` | A paired `input-*.md` and `expected-*.md` |

## Post-scaffold audit

After scaffolding, immediately run the audit prompt against the new
skill. Required result: ≥4 on every dimension.

If any dimension scores <4 on the empty scaffold, the scaffold itself is
broken — fix the template.

## Self-test

This template scaffolds a skill that, when populated, must pass the audit
rubric at 5/5 on every dimension. If not, the template needs revision.
