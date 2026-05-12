# Information Logistics Skills

Public skill collection following the
[Anthropic Agent Skills spec](https://agentskills.io/specification) and
mirroring the directory convention from
[anthropics/skills](https://github.com/anthropics/skills).

Skills are installable from any Agent-Skills-compatible host:
Claude Code, Codex, Cursor, OpenHands, and many others. For Claude
Code, this repo is also a plugin marketplace.

## Install

In Claude Code:

```bash
claude plugin marketplace add infolog-io/skills      # one-time
claude plugin install <skill-name>@infolog-io        # per skill
```

Or via slash commands:

```
/plugin marketplace add infolog-io/skills
/plugin install <skill-name>@infolog-io
/plugin marketplace list infolog-io
```

## Available skills

### Engineering

| Skill | Description | Install |
|---|---|---|
| [`claude-pip`](skills/claude-pip) | Performance Improvement Plan for Claude. Type `CLAUDE PIP` to lock in a behavioral discipline (TDD, plan mode, sub-agents, adversarial review) as a deterministic project rule. | `/plugin install claude-pip@infolog-io` |
| [`jtbd-prd`](skills/jtbd-prd) | Validate customer need before any build. Produces a Job Article (JTBD-grounded) that functions as PRD framing. Three modes: discovery, validation, reverse. | `/plugin install jtbd-prd@infolog-io` |
| [`estimatrix`](skills/estimatrix) | Two-axis sizing rubric. Effort as T-shirt (XS–XXL); complexity as low/medium/high. Runs active conversational intake before sizing. Applies Karpathy's four code rules. | `/plugin install estimatrix@infolog-io` |
| [`semantic-organization`](skills/semantic-organization) | Meta-skill that governs how every skill is structured. Codifies folder roles, naming rules, migration triggers. Scaffolds and audits skills. | `/plugin install semantic-organization@infolog-io` |
| [`github-issues-kanban`](skills/github-issues-kanban) | Agent orchestration substrate on GitHub Issues + Projects V2. Three concurrency primitives: access lock with TTL, dependency-chain DAG, comment-based event bus. Parallel-capable. Four board archetypes. | `/plugin install github-issues-kanban@infolog-io` |

### Design

| Skill | Description | Install |
|---|---|---|
| [`tufte-love`](skills/tufte-love) | Tufte-style audits, redesigns, and reviews for data visualizations, dashboards, and quantitative UI. Nine-dimension scored audit including color and formatting. | `/plugin install tufte-love@infolog-io` |
| [`atomic-brand`](skills/atomic-brand) | Audits web projects against atomic design discipline and brand-token coherence. Detects token violations, hierarchy drift, naming-by-appearance. Emits refactor or build-out plan. Failover chain: explicit tokens → image parse → URL scrape. | `/plugin install atomic-brand@infolog-io` |
| [`learn2kern`](skills/learn2kern) | Typography. Generates modular type scales (eight named ratios from Minor Second to Golden Ratio) with BODY and HEADINGS as separate token families. Emits CSS + Tailwind. | `/plugin install learn2kern@infolog-io` |

## How the skills compose

Each skill is self-contained — none reference siblings by name. They
compose via interface conventions only (CSS variable names, output
formats, JSON schemas), so removing or renaming any skill never breaks
another.

## Repo layout

```
infolog-io/skills/
├── .claude-plugin/
│   └── marketplace.json         # marketplace manifest (lists all skills)
├── skills/                      # one directory per skill (mirrors anthropics/skills)
│   ├── claude-pip/
│   ├── jtbd-prd/
│   ├── estimatrix/
│   ├── semantic-organization/
│   ├── github-issues-kanban/
│   ├── tufte-love/
│   ├── atomic-brand/
│   └── learn2kern/
├── CLAUDE.md                    # agent guidance
├── README.md                    # this file
├── CONTRIBUTING.md              # how to add a skill
└── LICENSE                      # MIT
```

Each skill follows this shape:

```
skills/<name>/
├── .claude-plugin/plugin.json   # plugin manifest (for Claude Code marketplace install)
├── SKILL.md                     # required (per Agent Skills spec)
├── README.md                    # marketplace listing (≤200 words)
├── TESTS.md                     # end conditions + test cases
├── references/                  # optional — knowledge files (spec)
├── scripts/                     # optional — executable code (spec)
├── assets/                      # optional — static resources (spec)
├── prompts/                     # convention — mode-specific operations
├── templates/                   # convention — output shapes
├── schemas/                     # convention — JSON Schema contracts
└── fixtures/                    # convention — test inputs + expected outputs
```

## Authoring a new skill

Use [`semantic-organization`](skills/semantic-organization) to scaffold:

```
"scaffold a new skill called my-skill"
```

It creates the canonical folder tree and runs a self-audit so the
scaffold is immediately marketplace-ready.

See [CONTRIBUTING.md](CONTRIBUTING.md) for PR conventions.

## License

[MIT](LICENSE).
