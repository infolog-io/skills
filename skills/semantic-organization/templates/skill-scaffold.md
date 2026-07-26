---
type: template
---

# Skill Scaffold Template

This template is the canonical shape every new skill must conform to for
its target host. Used by the scaffold prompt to generate a profile-aware
skill skeleton.

## Target host

Default in this repo: `infolog-marketplace`.

| Target | Root |
|---|---|
| `agent-skills-portable` | `{{skill_name}}/` |
| `infolog-marketplace` | `skills/{{skill_name}}/` |
| `codex-repo-skill` | `.agents/skills/{{skill_name}}/` |

Do not use a `plugins/<name>/skills/<name>/` wrapper for
`infolog-marketplace`.

## Tree — single-rule profile

Use this when SKILL.md carries the whole durable rule and no mode-specific
stage contracts are needed.

```
skills/{{skill_name}}/
├── .claude-plugin/
│   └── plugin.json
├── SKILL.md
├── README.md
└── TESTS.md
```

## Tree — full-shape profile

Use this only when the skill has multiple modes, references, scripts, or a
canonical output artifact. Omit any folder whose first real file is not yet
known.

```
skills/{{skill_name}}/
├── .claude-plugin/
│   └── plugin.json
├── SKILL.md
├── README.md
├── TESTS.md
├── references/
│   └── index.md
├── prompts/
│   └── {{mode_prompt_file}}.md
└── templates/
    └── {{primary_artifact_template}}.md
```

If the target host is `codex-repo-skill`, replace the root with:

```
.agents/skills/{{skill_name}}/
└── SKILL.md
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

For single-rule skills, omit the Operating modes and References sections
unless a real mode or reference exists. Report the target host in the
scaffold response, not inside the generated SKILL.md, unless the generated
skill carries its own host-standards reference. For `codex-repo-skill`,
omit `.claude-plugin/plugin.json`, README.md, and TESTS.md unless the user
asks for marketplace packaging too.

## First files for each canonical folder

Each real file carries `type:` frontmatter naming its role (OKF alignment;
see `references/okf-alignment.md`). A folder above five files gains an
`index.md` (`type: reference`) mapping its contents.

Never create empty placeholder folders just to reserve future structure.

| Folder | First file (created later, not by scaffold) | `type:` |
|---|---|---|
| `references/` | A foundational reference (theory or rule set) | `reference` |
| `prompts/` | A verb-led action file | `prompt` |
| `templates/` | A canonical output shape | `template` |
| `schemas/` | A JSON Schema for the output | `schema` |
| `fixtures/` | A paired `input-*.md` and `expected-*.md` | `fixture` |

## Post-scaffold audit

After scaffolding, immediately run the audit prompt against the new
skill. Required result: ≥4 on every dimension.

If any dimension scores <4 on the emitted scaffold, the scaffold itself is
broken — fix the template.

## Self-test

This template scaffolds a skill that, when populated, must pass the audit
rubric at 5/5 on every dimension for its target host. If not, the template
needs revision.
