# Contributing

How to add or update a skill in the Information Logistics marketplace.

## Canonical Layout

This repository uses the flat Agent Skills layout:

```text
skills/<skill-name>/
├── .claude-plugin/
│   └── plugin.json
├── SKILL.md
├── README.md
└── TESTS.md
```

Optional folders are added only when needed:

```text
references/   background knowledge
prompts/      mode-specific stage contracts
templates/    canonical output shapes
schemas/      JSON Schema contracts
fixtures/     test inputs and expected outputs
assets/       static resources
scripts/      executable support code
```

Do not create a `plugins/<name>/skills/<name>/` wrapper in this repo.

## Add A Skill

1. Scaffold with `semantic-organization`.

   ```text
   scaffold a new skill called <skill-name>
   ```

2. Keep the profile honest.

   - Single-rule skills should usually contain only `SKILL.md`,
     `.claude-plugin/plugin.json`, `README.md`, and `TESTS.md`.
   - Full-shape skills may add `references/`, `prompts/`, `templates/`,
     `schemas/`, `fixtures/`, `assets/`, or `scripts/` when those folders
     carry a real context layer.

3. Write `SKILL.md`.

   Frontmatter must include `name` and `description`. The `description`
   should say what the skill does and when to use it.

4. Write `.claude-plugin/plugin.json`.

   ```json
   {
     "name": "<skill-name>",
     "version": "0.1.0",
     "description": "One sentence describing what this skill does.",
     "author": {
       "name": "Information Logistics",
       "url": "https://github.com/infolog-io"
     }
   }
   ```

5. Write `README.md` and `TESTS.md`.

   `README.md` is the marketplace listing and should stay at or under 200
   words. `TESTS.md` records end conditions, concrete test cases, and
   out-of-scope items.

6. Register the skill in `.claude-plugin/marketplace.json`.

   Add a plugin entry whose `source` is `./skills/<skill-name>`.

7. Run a semantic audit.

   ```text
   /semantic-audit skills/<skill-name>
   ```

   The target verdict for shipping is `spec-compliant + marketplace-ready`.

## Update A Skill

For behavior changes:

- update `SKILL.md`
- update affected references, prompts, templates, schemas, or fixtures
- update `TESTS.md`
- update the skill `README.md` if triggers or usage changed
- bump the skill version in `skills/<name>/.claude-plugin/plugin.json`
- bump the matching version in `.claude-plugin/marketplace.json`

## Validation

Before opening a PR or handing off:

```bash
jq empty .claude-plugin/marketplace.json
jq empty skills/<skill-name>/.claude-plugin/plugin.json
```

For semantic-organization changes, also run:

```bash
tools/skillopt/.venv/bin/python -m pytest tools/skillopt/tests -q
```

## Pull Requests

Use a concise title:

```text
feat(<skill-name>): add <capability>
fix(<skill-name>): clarify <behavior>
docs(<skill-name>): update <topic>
```

Keep unrelated docs, generated artifacts, and local run outputs out of the
PR unless they are part of the change.
