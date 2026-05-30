# Handoff — infolog.lib design system session

Date: 2026-05-30
Branch: `feat/component-composer` (repo: infolog-skills)

## ⚠️ Volatile artifact

The live page is `/tmp/composer-e2e/spraypixel-state.html` (~1500 lines, no build
step). `/tmp` clears on reboot and **this page is the only copy** — it is not
repo-tracked. All design work below lives in it. Consider copying it somewhere
durable if continuing. Everything else (specs, plan, the consolidated skills) is
committed.

## What this is

A comprehensive enterprise design system, wordmark **infolog.lib**, shown as a
9-section living reference page with a per-section AND per-visualization feedback
loop (type notes → "Copy as prompt" in §10 compiles them). It is the reference
instance for a planned generic `design-system` skill.

## The arc this session

1. **Tonal color tier** (built): OKLCH recipe "lever a" — pale fill + AA-safe
   vivid label. Engine `/tmp/composer-e2e/scripts/tonal-values.mjs`. Spec:
   `docs/superpowers/specs/2026-05-30-tonal-buttons-design.md`.
2. **Constitution spec** (committed): `docs/superpowers/specs/2026-05-30-design-system-constitution-design.md` — 10-pillar map, hallmark-shaped audit+build skill.
3. **Repo consolidation** (committed, `6c2cd58`): reversed the spraypixel spin-out.
   The 5 composition skills are back in `infolog-skills/skills/`, with
   `spraypixel`→`infolog-io`, `spraypixel-terminal`→`infolog-terminal`. Marketplace
   now 12 plugins. `spraypixel-skills` archived.
4. **Implementation plan** (committed): `docs/superpowers/plans/2026-05-30-design-system-skill.md` — first increment scaffolds the skill + ports the OKLCH engine (TDD). Skill name `design-system` is PROVISIONAL.
5. **Apple scrub** (committed, `d145fe9`): zero Apple/HIG references.
6. **Two feedback rounds applied to the page** (see below).

## Page state — current (all applied + verified)

- **Brand** infolog.lib (green tonal pill); all "spraypixel" swept off the page.
- **§02 Color**: 3 feedback colors only — **success / info / danger. NO warning, NO yellow.** One dark gray (gray-700; gray-900 removed). paper-soft `#eaeaef`, ink softened `#2a2a2a`.
- **§03 Buttons**: tiers solid > tonal > neutral > ghost. Radius 16px. neutral has no border; ghost border gray-500.
- **§04 Alerts**: banner-rounded (4px) + × close (currentColor, 26px hit area, focus ring, `.dismissed`).
- **§05 tiles**: each label matches its metric color. **dots/tiles use only green/blue/red now.**
- **§06 mockup**: blocks one grey (gray-300); terminal fixed-dark `#1c1c1e`.
- **§07 data-viz**: **binary rule** — green=up, red=down, gray=quiet. Rubric rewritten to 6 rules + 3-color palette. a11y focus ring hides at rest, shows on keyboard focus.
- **§08 table**: statuses are tonal **pills**; 6/10 pass red.
- Reusable `.pill.{success,info,danger}` (tonal chip = brand-mark pattern).

## THE COLOR RULE (latest, locked)

success / info / danger only. **Yellow is gone.** Non-critical warnings → **info (blue)**. Critical → **danger (red)**. Charts: binary green(up)/red(down)/gray(quiet).

## Queued — dedicated passes (tasks 20-23)

1. **Animation / Motion section** — new pillar, its own section + tokens (duration/easing, reduced-motion).
2. **Z-axis / elevation / layering** — user-flagged critical: z-index tiers + shadow/overlay tokens.
3. **Modal pattern** — overlay/scrim, focus trap, ESC chip; needs the elevation scale first.
4. **Card/section height tokens** — 8px-baseline `--h-*` + max-height/scroll for dense panels.
Plus: build the `design-system` skill per the committed plan.

## Recipes / workflow

- Preview: `agent-browser open "file://<path>"` → `screenshot --full PATH` → Read. NO localhost server (PIP e3c9a7d4).
- Force theme: `agent-browser click "[data-mode=light|dark]"`.
- OKLCH tonal values (light): success `#ddf9df`/`#008104` · info `#def2ff`/`#0063e6` · danger `#ffe6df`/`#da0000`. Dark: success `#194220`/`#30d158` · info `#1b385e`/`#3ca5ff` · danger `#592721`/`#ff5f51`.
- Feedback compiles via the JS `ALL` list (SECTIONS + 6 viz dimensions); `PREFIX='spraypixel-state-fb-'` (localStorage key, left as-is).

## PIP status

Both rules in `.claude/CLAUDE-PIP.md` (e3c9a7d4 file:// preview, 7c4d9e2a no SemVer) fired correctly and remain valid. No pruning. No promotion requested.
