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

12 plugins as of v0.5.0 — claude-pip, jtbd-prd, estimatrix, learn2kern, semantic-organization, atomic-brand, github-issues-kanban, generator-critic, component-composer, infolog-io, infolog-terminal, html-sketch. Spans process discipline, JTBD validation, sizing, structural audit, agent orchestration, type scales, brand audits, and single-file HTML composition.

**HTML composition family consolidated back into this marketplace (2026-05-30).** generator-critic, component-composer, infolog-io (the Tufte-quiet theme, formerly `spraypixel`), infolog-terminal (formerly `spraypixel-terminal`), and html-sketch live here under `skills/`. They were briefly spun out to a separate SPRAYPIXEL.AI marketplace on 2026-05-26; that split is reversed — everything ships under infolog-io again. The `spraypixel-skills` repo at `/Users/informationlogistics/Developer/spraypixel-skills/` is archived.
