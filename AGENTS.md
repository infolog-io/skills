@.Codex/Codex-PIP.md

# infolog-io/skills — Agent guidance

This repo is a public Codex plugin marketplace for skills authored by Information Logistics.

## Repository conventions

**Match the Anthropic skill directory convention** for any new skill in this repo: `skills/<name>/SKILL.md` flat at repo root; `.Codex-plugin/plugin.json` lives inside the skill folder; `.Codex-plugin/marketplace.json` registers `./skills/<name>` as source. NEVER nest in a `plugins/<name>/skills/<name>/` wrapper. Reference: https://github.com/anthropics/skills.

## Local preview

**Preview self-contained HTML from disk** — `open file://<path>`, not a localhost dev server. `preview_start` / `python http.server` drop between turns and waste restart cycles. Spin up a server only when the page needs server-dependent resources (same-origin `fetch`, local module/asset imports). For screenshots, point agent-browser at the `file://` URL.

## Quick reference

- Spec: https://agentskills.io/specification
- Anthropic's reference repo: https://github.com/anthropics/skills
- Local protocol audit skill: `skills/semantic-organization`

## What this repo provides

12 plugins as of v0.5.0 — Codex-pip, jtbd-prd, estimatrix, learn2kern, semantic-organization, atomic-brand, github-issues-kanban, generator-critic, component-composer, infolog-io, infolog-terminal, html-sketch. Spans process discipline, JTBD validation, sizing, structural audit, agent orchestration, type scales, brand audits, and single-file HTML composition.

**HTML composition family consolidated back into this marketplace (2026-05-30).** generator-critic, component-composer, infolog-io (the Tufte-quiet theme, formerly `spraypixel`), infolog-terminal (formerly `spraypixel-terminal`), and html-sketch live here under `skills/`. They were briefly spun out to a separate SPRAYPIXEL.AI marketplace on 2026-05-26; that split is reversed — everything ships under infolog-io again. The `spraypixel-skills` repo at `/Users/informationlogistics/Developer/spraypixel-skills/` is archived.
