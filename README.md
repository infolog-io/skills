# Information Logistics Skills

Public Claude Code plugin marketplace.

This repo hosts **plugins** (each containing one or more **skills** per
[Anthropic's Agent Skills spec](https://agentskills.io/specification))
that are installable from any Agent-Skills-compatible host: Claude Code,
Codex, Cursor, OpenHands, and many others.

The repo is named `skills` for backward compatibility; the directory
structure follows Claude Code's plugin marketplace convention (each
plugin lives in `plugins/<name>/` with a `skills/<name>/` inside).

## Install

In Claude Code:

```bash
claude plugin marketplace add infolog-io/skills      # one-time
claude plugin install <plugin-name>@infolog-io       # per plugin
```

Or via slash commands:

```
/plugin marketplace add infolog-io/skills
/plugin install <plugin-name>@infolog-io
/plugin marketplace list infolog-io
```

## Available plugins

### Engineering

| Plugin | Description | Install |
|---|---|---|
| [`claude-pip`](plugins/claude-pip) | Performance Improvement Plan for Claude. Type `CLAUDE PIP` to lock in a behavioral discipline (TDD, plan mode, sub-agents, adversarial review) as a deterministic project rule. | `/plugin install claude-pip@infolog-io` |
| [`jtbd-prd`](plugins/jtbd-prd) | Validate customer need before any build. Produces a Job Article (JTBD-grounded) that functions as PRD framing. Three modes: discovery, validation, reverse. | `/plugin install jtbd-prd@infolog-io` |
| [`estimatrix`](plugins/estimatrix) | Two-axis sizing rubric. Effort as T-shirt (XS–XXL); complexity as low/medium/high. Runs active conversational intake before sizing. Applies Karpathy's four code rules. | `/plugin install estimatrix@infolog-io` |
| [`semantic-organization`](plugins/semantic-organization) | Meta-skill that governs how every skill is structured. Two layers: Agent Skills spec compliance + marketplace conventions. Scaffolds, audits, recommends migrations. | `/plugin install semantic-organization@infolog-io` |
| [`github-issues-kanban`](plugins/github-issues-kanban) | Agent orchestration substrate on GitHub Issues + Projects V2. Three concurrency primitives: access lock with TTL, dependency-chain DAG, comment-based event bus. Parallel-capable. Four board archetypes. | `/plugin install github-issues-kanban@infolog-io` |

### Design

| Plugin | Description | Install |
|---|---|---|
| [`tufte-love`](plugins/tufte-love) | Tufte-style audits, redesigns, and reviews for data visualizations, dashboards, and quantitative UI. Nine-dimension scored audit including color and formatting. | `/plugin install tufte-love@infolog-io` |
| [`atomic-brand`](plugins/atomic-brand) | Audits web projects against atomic design discipline and brand-token coherence. Detects token violations, hierarchy drift, naming-by-appearance. Emits refactor or build-out plan. Failover chain: explicit tokens → image parse → URL scrape. | `/plugin install atomic-brand@infolog-io` |
| [`learn2kern`](plugins/learn2kern) | Typography. Generates modular type scales (eight named ratios from Minor Second to Golden Ratio) with BODY and HEADINGS as separate token families. Emits CSS + Tailwind. | `/plugin install learn2kern@infolog-io` |

## How the plugins compose

Each plugin is self-contained — none reference siblings by name. They
compose via interface conventions only (CSS variable names, output
formats, JSON schemas), so removing or renaming any plugin never breaks
another.

## Repo layout

```
infolog-io/skills/
├── .claude-plugin/
│   └── marketplace.json     # marketplace manifest (lists all plugins)
├── plugins/                 # one directory per plugin
│   ├── claude-pip/
│   ├── jtbd-prd/
│   ├── estimatrix/
│   ├── semantic-organization/
│   ├── github-issues-kanban/
│   ├── tufte-love/
│   ├── atomic-brand/
│   └── learn2kern/
├── README.md                # this file
├── CONTRIBUTING.md          # how to add a plugin
└── LICENSE                  # MIT
```

Each plugin follows the same shape (defined by `semantic-organization`):

```
plugins/<name>/
├── .claude-plugin/plugin.json     # plugin manifest
├── README.md                      # marketplace listing (≤200 words)
├── TESTS.md                       # end conditions + test cases
└── skills/<name>/                 # the spec-compliant skill
    ├── SKILL.md                   # required
    ├── references/                # optional — knowledge files
    ├── prompts/                   # convention — mode-specific operations
    ├── templates/                 # convention — output shapes
    ├── schemas/                   # convention — JSON Schema contracts
    ├── assets/                    # optional — static resources
    └── fixtures/                  # convention — test inputs + expected outputs
```

## Authoring a new plugin

Use [`semantic-organization`](plugins/semantic-organization) to scaffold:

```
"scaffold a new skill called my-skill"
```

It creates the canonical folder tree and runs a self-audit so the
scaffold is immediately marketplace-ready.

See [CONTRIBUTING.md](CONTRIBUTING.md) for PR conventions.

## License

[MIT](LICENSE).
