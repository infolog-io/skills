@.claude/CLAUDE-PIP.md

# infolog-io/skills — Agent guidance

This repo is a public Claude Code plugin marketplace for skills authored by Information Logistics.

## Repository conventions

**Match the Anthropic skill directory convention** for any new skill in this repo: `skills/<name>/SKILL.md` flat at repo root; `.claude-plugin/plugin.json` lives inside the skill folder; `.claude-plugin/marketplace.json` registers `./skills/<name>` as source. NEVER nest in a `plugins/<name>/skills/<name>/` wrapper. Reference: https://github.com/anthropics/skills.

## Quick reference

- Spec: https://agentskills.io/specification
- Anthropic's reference repo: https://github.com/anthropics/skills
- Local protocol audit skill: `skills/semantic-organization`

## What this repo provides

11 plugins as of v0.5.0 — claude-pip, infolog-io (formerly tufte-love), jtbd-prd, estimatrix, learn2kern, semantic-organization, atomic-brand, github-issues-kanban, goal, component-composer, infolog-terminal. Spans process discipline, JTBD validation, sizing, structural audit, agent orchestration, type scales, brand audits, data viz audits, generator-critic loops, and theme bundles.
