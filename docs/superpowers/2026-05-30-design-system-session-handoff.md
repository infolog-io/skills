# Handoff — infolog.lib design system

Date: 2026-05-30
Branch: `feat/component-composer` (repo: infolog-skills)

## ⚠️ Volatile artifact

Live page: `/tmp/composer-e2e/spraypixel-state.html` (~1600 lines, no build step).
`/tmp` clears on reboot and **this page is the only copy** — not repo-tracked.
Copy it somewhere durable before continuing. Specs/plan/consolidated skills are
committed; the page is not.

Preview (PIP e3c9a7d4 — file://, NO localhost server):
`agent-browser open "file:///tmp/composer-e2e/spraypixel-state.html"` →
`agent-browser screenshot --full PATH` → Read. Theme:
`agent-browser click "[data-mode=light|dark]"`. Verify computed values with
`agent-browser eval "<js returning JSON.stringify(...)>"`.

## What this is

A comprehensive enterprise design system, wordmark **infolog.lib**, shown as a
10-section living reference page with a per-section AND per-visualization
feedback loop (type notes → "Copy as prompt" in §10 compiles them). Reference
instance for a planned generic `design-system` skill.

## Committed (durable)

- Color pillar spec: `docs/superpowers/specs/2026-05-30-tonal-buttons-design.md`
- Constitution: `docs/superpowers/specs/2026-05-30-design-system-constitution-design.md`
- Data-viz spec: `docs/superpowers/specs/2026-05-29-spraypixel-chart-six-dimensions-design.md`
- Skill plan: `docs/superpowers/plans/2026-05-30-design-system-skill.md` (name `design-system` PROVISIONAL)
- Repo consolidation `6c2cd58`: 5 composition skills back in `infolog-skills/skills/` (spraypixel→infolog-io, spraypixel-terminal→infolog-terminal); marketplace = 12 plugins; spraypixel-skills archived.

## THE COLOR RULE (locked, current)

Four roles, NO yellow:
- **success / green** — up · positive · growing · shipped
- **info / blue** — non-directional reference · baseline · neutral metric (NOT warnings-as-info-anymore: see below)
- **danger / red** — down · negative · declining · critical
- **gray** — quiet context (axes, gridlines, past/neutral marks)

Charts (§07 rubric, 6 rules): green up, red down, blue for a non-directional
reference/baseline, gray quiet. Warnings removed entirely — non-critical → info
(blue), critical → danger (red).

## Page state — CURRENT (every feedback round applied)

- **Brand** infolog.lib (green tonal pill). No "spraypixel" visible anywhere.
- **§02 Color** chips: success / info / danger + paper / neutral (was paper-soft) / ink (was gray-700). One dark gray; `--paper-soft` `#eaeaef`; `--ink` `#2a2a2a`.
- **§03 Buttons** — tiers **tonal > neutral > ghost** in the showcase (solid primary REMOVED from showcase but still the form's "Ship it" submit). Radius 16px, **medium** weight. `.btn.primary` = brand `--success` + **white** text (user accepted sub-AA contrast). `.btn.neutral` no border. `.btn.ghost` 2px `--gray-500`. Row: Deploy(tonal success) · Learn more(info) · Delete(danger) · Cancel(neutral) · Dismiss(ghost).
- **§04 Alerts** — banner radius 4px, each with an accessible × close (`currentColor`, 26px hit area, focus ring). One of each: success/info/danger.
- **§05** — stat-tile labels match their metric color. Dots: Up/Syncing/Down (Degraded removed). Tiles: Uptime/Queue/Errors (Requests removed).
- **§06 Mockup** — 4 chrome (Browser/Document/Sketch/Terminal) + 4 **chart skeletons** (Line/Bars/Dots/Candles, grey wireframes, capped `max-width:200px` = smaller than chrome). Terminal fixed-dark `#1c1c1e`, code-like.
- **§07 Data-viz** — binary green/red + blue reference + gray; a11y focus ring hides at rest (shows on keyboard focus); rubric = 6 rules, 4-row palette.
- **§08 Data table** — pill statuses; **Trend** column (line / bar / stacked sparklines); **sparkline-types gallery** below: line·bar·stacked·tristate·discrete·bullet·box (NO pie, Tufte). Box sparkline is blue (non-directional).
- **§09 Forms** — composed form: white bg + 2px border.
- Reusable: `.pill.{success,info,danger}`, `.spark` (table), `.spark-lg` (gallery). Theme switch active state = `--ink` bg (was invisible).

## Queued — dedicated passes (tasks 20-23)

1. Animation / Motion section (new pillar: duration/easing tokens, reduced-motion).
2. Z-axis / elevation / layering (user-flagged critical: z-index tiers + shadow/overlay tokens).
3. Modal pattern (overlay/scrim, focus trap, ESC chip — needs elevation first).
4. Card/section height tokens (8px baseline `--h-*` + max-height/scroll).
Plus: build the generic `design-system` skill per the committed plan.

## Recipes

- OKLCH tonal pairs (light): success `#ddf9df`/`#008104` · info `#def2ff`/`#0063e6` · danger `#ffe6df`/`#da0000`. (dark): success `#194220`/`#30d158` · info `#1b385e`/`#3ca5ff` · danger `#592721`/`#ff5f51`.
- Feedback JS: `ALL` list (sections + 6 viz dims); `PREFIX='spraypixel-state-fb-'`.
- Sparklines are inline SVG (viewBox 84×22 table, 104×28 gallery), grey/green/red/blue per the color rule.

## PIP status

`.claude/CLAUDE-PIP.md` rules e3c9a7d4 (file:// preview) and 7c4d9e2a (no SemVer
bumps) both fired correctly and remain valid. No pruning. No promotion requested.
