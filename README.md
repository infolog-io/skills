# Information Logistics Skills

Public Agent Skills marketplace for Information Logistics.

This repository follows the open [Agent Skills spec](https://agentskills.io/specification)
and the flat skill layout used by [anthropics/skills](https://github.com/anthropics/skills):
each skill lives at `skills/<name>/SKILL.md`. For Claude Code, each skill is
also packaged as an installable marketplace plugin through the local
`.claude-plugin/marketplace.json` catalog.

## Install

In Claude Code:

```bash
claude plugin marketplace add infolog-io/skills
claude plugin install <skill-name>@infolog-io
```

Or with slash commands:

```text
/plugin marketplace add infolog-io/skills
/plugin install <skill-name>@infolog-io
/plugin marketplace list infolog-io
```

## Available Skills

### Engineering

| Skill | Purpose |
|---|---|
| [`claude-pip`](skills/claude-pip) | Performance Improvement Plan for Claude. Adds, scopes, and removes deterministic project rules. |
| [`jtbd-prd`](skills/jtbd-prd) | Validates customer need before build work. Emits JTBD-grounded Job Articles and workflow automation maps. |
| [`estimatrix`](skills/estimatrix) | Sizes work on effort and complexity axes after conversational intake. |
| [`semantic-organization`](skills/semantic-organization) | Audits and scaffolds skill structure across folder roles, context layers, migration triggers, and host standards. |
| [`github-issues-kanban`](skills/github-issues-kanban) | Uses GitHub Issues and Projects V2 as an agent orchestration substrate. |
| [`generator-critic`](skills/generator-critic) | Abstract generator-critic loop pattern for iterative artifact refinement. |

### Design

| Skill | Purpose |
|---|---|
| [`atomic-brand`](skills/atomic-brand) | Audits brand-token coherence, atomic design hierarchy, and component structure. |
| [`learn2kern`](skills/learn2kern) | Generates modular type scales and emits CSS plus Tailwind configuration. |
| [`component-composer`](skills/component-composer) | Production-grade single-file HTML data graphics through a generator-critic loop. |
| [`infolog-io`](skills/infolog-io) | Tufte-quiet theme bundle for `component-composer`. |
| [`infolog-terminal`](skills/infolog-terminal) | Terminal-aesthetic theme bundle for `component-composer`. |
| [`html-sketch`](skills/html-sketch) | Casual single-file HTML artifacts without the production composer loop. |

The source of truth for names, versions, and marketplace descriptions is
[`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json).

## Repository Layout

```text
infolog-skills/
├── .claude-plugin/
│   └── marketplace.json
├── skills/
│   └── <skill-name>/
│       ├── .claude-plugin/plugin.json
│       ├── SKILL.md
│       ├── README.md
│       ├── TESTS.md
│       ├── references/
│       ├── prompts/
│       ├── templates/
│       ├── schemas/
│       ├── fixtures/
│       ├── assets/
│       └── scripts/
├── tools/
│   └── skillopt/
├── docs/
└── CONTRIBUTING.md
```

Not every skill needs every optional folder. Single-rule skills should stay
small; full-shape skills add folders only when a context layer needs them.

## Documentation

- [Project orientation](docs/PROJECT.md) explains the architecture, host
  standards, and documentation map.
- [Contributing](CONTRIBUTING.md) explains how to add or update skills.
- [`semantic-organization`](skills/semantic-organization) is the local
  structural authority for scaffolding and audits.
- [`tools/skillopt`](tools/skillopt) documents the local skill improvement
  harness.

## Authoring A Skill

Use `semantic-organization`:

```text
scaffold a new skill called my-skill
```

Default target host in this repository is `infolog-marketplace`, which means:

- skill root is `skills/<name>/`
- `SKILL.md` is one level deep
- `.claude-plugin/plugin.json` lives inside the skill folder
- `.claude-plugin/marketplace.json` registers `./skills/<name>`
- no `plugins/<name>/skills/<name>/` wrapper

Run a semantic audit before shipping:

```text
/semantic-audit skills/<name>
```

## License

[MIT](LICENSE)
