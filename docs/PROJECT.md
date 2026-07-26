# Project Orientation

This repository is a public Agent Skills marketplace maintained by
Information Logistics. It contains reusable skills, marketplace metadata,
local optimization tooling, and design/implementation notes.

## What Ships

The shipped surface is the skill marketplace:

- `.claude-plugin/marketplace.json` is the marketplace catalog.
- `skills/<name>/` is one installable skill.
- `skills/<name>/SKILL.md` is the portable Agent Skills entrypoint.
- `skills/<name>/.claude-plugin/plugin.json` makes the skill installable
  from this marketplace in Claude Code.

The current marketplace contains 12 skills across engineering and design.
Use the root [README](../README.md) or the marketplace JSON for the current
list.

## Structural Philosophy

The repo follows the "folders over agents" principle: durable agent work
comes from interpretable context architecture, not one-off agent wiring.

The five context layers are:

| Layer | Typical home |
|---|---|
| Identity | `SKILL.md`, `README.md`, `plugin.json` |
| Routing | triggers, operating modes, indexes |
| Stage contract | `prompts/` |
| Reference material | `references/` |
| Working artifact | `templates/`, `schemas/`, `fixtures/`, `assets/`, `scripts/` |

The local authority for these rules is
[`skills/semantic-organization`](../skills/semantic-organization).

## Host Standards

Different hosts use different roots and packaging conventions. In this repo
the default target is `infolog-marketplace`:

```text
skills/<name>/SKILL.md
skills/<name>/.claude-plugin/plugin.json
.claude-plugin/marketplace.json
```

Other supported targets are documented in
[`skills/semantic-organization/references/host-standards.md`](../skills/semantic-organization/references/host-standards.md):

- `agent-skills-portable`
- `infolog-marketplace`
- `codex-repo-skill`
- `claude-code-plugin-package`

Do not mix host layouts inside one scaffold. Generate for the target host.

## Documentation Map

| Path | Purpose |
|---|---|
| [README.md](../README.md) | Public entrypoint, install commands, skill list |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | How to add or update skills |
| [CLAUDE.md](../CLAUDE.md) | Claude Code agent guidance for this repo |
| [skills/*/README.md](../skills) | Marketplace listings for individual skills |
| [skills/*/TESTS.md](../skills) | End conditions and test cases per skill |
| [docs/superpowers/specs](superpowers/specs) | Design specs from prior implementation sessions |
| [docs/superpowers/plans](superpowers/plans) | Implementation plans from prior sessions |
| [tools/skillopt/README.md](../tools/skillopt/README.md) | Local SkillOpt-style improvement harness |
| [tools/skillopt/HANDOFF.md](../tools/skillopt/HANDOFF.md) | Proven run pattern for SkillOpt eval/optimize |

## Tooling

`tools/skillopt/` is local optimization tooling. It is not registered in
the marketplace. It evaluates and improves selected `SKILL.md` files through
rollout, scoring, reflection, edit, and gate stages.

Common checks:

```bash
jq empty .claude-plugin/marketplace.json
tools/skillopt/.venv/bin/python -m pytest tools/skillopt/tests -q
```

For model-backed skill evaluation, read
[`tools/skillopt/HANDOFF.md`](../tools/skillopt/HANDOFF.md) first.

## Maintenance Notes

- Keep the root README skill list synchronized with
  `.claude-plugin/marketplace.json`.
- Keep skill READMEs under 200 words.
- Run `semantic-organization` before shipping structure changes.
- Prefer profile-aware scaffolds over empty placeholder folders.
- Keep `docs/superpowers/` as historical planning context, not the public
  source of truth.
