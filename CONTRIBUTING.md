# Contributing

How to add a new plugin to the Information Logistics marketplace.

## Add a plugin in five steps

### 1. Create the plugin directory

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── <skill-name>/
        └── SKILL.md
```

Plugin and skill names use kebab-case (e.g., `lexicon-check`, `seo-audit`). The `@infolog-io` marketplace suffix already namespaces them, so no prefix is required.

### 2. Write `plugin.json`

Minimum schema:

```json
{
  "name": "<plugin-name>",
  "version": "0.1.0",
  "description": "One sentence describing what this plugin does.",
  "author": { "name": "Information Logistics", "url": "https://github.com/infolog-io" }
}
```

### 3. Write each `SKILL.md`

Frontmatter must include `name` and `description`. The `description` ends with the activation phrases users will type.

```markdown
---
name: <skill-name>
description: "What it does in one sentence. Activate with '<phrase one>', '<phrase two>', or '/<slash-command>'."
---

# <skill-name>

Body of the skill — workflow, inputs, outputs, failure modes.
```

### 4. Register in `marketplace.json`

Append to the `plugins` array in `.claude-plugin/marketplace.json`:

```json
{
  "name": "<plugin-name>",
  "description": "One sentence summary.",
  "source": "./plugins/<plugin-name>",
  "version": "0.1.0",
  "category": "<marketing|design|seo|engineering|...>",
  "author": { "name": "Information Logistics" }
}
```

### 5. Open a PR

Title: `Add <plugin-name> plugin`. The PR must include all four pieces above and update the README's "Available plugins" table.

## Versioning

SemVer per plugin. Bump the patch version on any `SKILL.md` body change. Bump the minor version on a behavior change. Bump the major version on a breaking interface change (renamed activation phrase, removed flag, changed output schema).

Bump the marketplace `metadata.version` when adding or removing a plugin.

## Validation

Before opening a PR, validate locally:

```bash
jq empty .claude-plugin/marketplace.json
jq empty plugins/<plugin-name>/.claude-plugin/plugin.json
```

Both commands must exit 0 with no output.
