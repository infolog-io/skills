# Handoff — tinted/tonal button system for the spraypixel page

Date: 2026-05-30
Branch: `feat/component-composer` (repo: infolog-skills)
Status: design in flight, NOT yet on the real page, NOT yet specced.

## IMMEDIATE NEXT ACTION

Resolve ONE open design question (button fill weight — see below), then
implement the tonal button family on the real page and write + commit a spec.
Do NOT re-run the exploration: the direction is decided, the color recipe works.

## Where everything lives

Real page (the design-system "current state"):
`/tmp/composer-e2e/spraypixel-state.html` (~1400 lines, no build step). §07 six-
dimension chart work shipped earlier this session and is stable.

Mockups — OPEN FROM DISK, no server (PIP rule e3c9a7d4):
`open "file:///tmp/composer-e2e/<file>"`
- `tinted-buttons-explore.html` — first 3-way: solid / tinted-pure / tinted-AA-safe.
- `tinted-buttons-contrast.html` — measured WCAG ratios per option + the GREY neutral button.
- `tinted-oklch.html` — OKLCH vs sRGB comparison. THE CURRENT FRONTIER. Full
  OKLab↔sRGB transform implemented in JS (Ottosson coefficients).
Screenshots: `/tmp/composer-e2e/shots/`.

NOTE: `/tmp` is volatile. The recipe + facts below are enough to rebuild every
mockup if they vanish.

## Decisions LOCKED (via the user, do not relitigate)

1. **Emphasis = add a tier, keep solid primary.** Hierarchy: Solid (high) →
   Tinted semantic (medium) → Grey neutral (medium-low) → Ghost (low). The one
   main CTA stays solid; tinted does NOT replace it.
2. **Scope** (all four): buttons §03 · chapter code chips G/M/X/D/A/R §07 ·
   stat tiles / data accents §05 · topbar brand/nav.
3. **Pure full-chroma label is REJECTED** — fails WCAG AA. Measured on this
   palette: light success 1.96:1, info 3.30, warning 1.41, danger 2.90; dark
   info 3.87, danger 4.12. Only large-text bar at best. Off the table.
4. **Tinted via plain sRGB darkening is REJECTED** — user called it "yucky."
   Cause: mixing label toward black desaturates → yellow=olive, green=mud,
   red=maroon. Pivoted to OKLCH.

## The GREY neutral button — DONE, settled

User-requested (matched a native "Always quit / Cancel ⎟ESC⎟" confirm dialog).
- "our grey" = `--gray-100` fill (#E5E5EA light / #2C2C2E dark) + `--gray-300`
  hairline border (#D1D1D6 / #3A3A3C) + `--ink` text.
- Contrast 13.86:1 light / 12.37:1 dark. Trivially AA.
- For Cancel / Dismiss / secondary neutral. `ESC` chip reuses the page's
  existing `kbd` style.
- Implemented in `tinted-buttons-contrast.html` (bottom of each panel).

## The OKLCH recipe — WORKING (in tinted-oklch.html)

Why OKLCH: lightness is independent of chroma, so a label can be darkened
*just enough* for AA while HOLDING saturation → vivid, not muddy.

- **Fill** = `oklch(L, min(accentC, Ccap), accentH)`
  - light: L=0.955, Ccap=0.045 · dark: L=0.34, Ccap=0.075
- **Label** = hold accent chroma + hue; move lightness toward AA until
  contrast ≥ 4.6:1 (lower in light, raise in dark). Keeps it the lightest/most
  vivid label that still passes.
- Result: red/blue/green labels read as rich saturated color. Passes AA
  (~4.6–4.8:1) in both themes.

### The yellow caveat
Warning stays olive even in OKLCH — a yellow dark enough to read on a pale
yellow fill IS perceptually olive. This is hue physics, not the color space.
DECISION NEEDED: special-case warning to a darker amber label, OR keep warning
solid (don't tint it).

## OPEN QUESTION (answer first next session)

The OKLCH labels are fixed, but the FILLS are still pale by nature. The user's
"yucky" may be partly the pale fill. Three levers, pick with the user:
- **a. OKLCH as-is** — accept the soft tinted look (labels now vivid).
- **b. Bolder fills** — lower fill L / raise Ccap so the tint has more presence.
- **c. Bordered-tint** — add a full-chroma hairline edge (the bordered-tint pattern)
  so it stops reading anemic.
- **d. Pivot** — solids stay for primary semantic actions; tint only for
  genuinely secondary ones; grey for neutral. (Sidesteps paleness entirely.)
Recommend rendering a/b/c side-by-side from disk, then deciding.

## Then implement (on the real page)

- Add `.btn` modifiers: a tonal/tinted tier (per-intent OKLCH fill+label) and a
  `.btn.neutral` grey tier. Keep `.btn.primary` solid.
- Apply the tonal treatment across scope: §03 buttons, §07 chapter code chips,
  §05 stat tiles, topbar brand/nav.
- Verify light + dark via `agent-browser open "file://…"` + `screenshot --full`.
- Write + commit a spec to `docs/superpowers/specs/YYYY-MM-DD-tonal-buttons-design.md`.

## Token reference (semantic system colors, both themes)

LIGHT: --paper #fff · --ink #1a1a1a · --gray-100 #E5E5EA · --gray-300 #D1D1D6 ·
success #34C759 · info #007AFF · warning #FFCC00 · danger #FF3B30.
DARK: --paper #161413 · --ink #f5f1e9 · --gray-100 #2C2C2E · --gray-300 #3A3A3C ·
success #30D158 · info #0A84FF · warning #FFD60A · danger #FF453A.

## Workflow rules in force

- **PIP e3c9a7d4**: preview self-contained HTML via `open file://<path>`, NOT a
  localhost server. The composer-e2e:7475 server died between turns repeatedly.
- **PIP 7c4d9e2a**: no SemVer bumps for milestone vibes (repo is pre-0.1).
- Screenshots: `agent-browser open "file://…"` → `agent-browser screenshot --full PATH` → Read PNG.

## Repo state

- Committed this session: §07 six-dimension spec (`0ad1865`); this handoff doc.
- PIP rule e3c9a7d4 lives in `.claude/CLAUDE-PIP.md`, which is GITIGNORED in this
  repo — so it's local-only (not tracked) but loads every session via the
  `@.claude/CLAUDE-PIP.md` import in CLAUDE.md, same as the SemVer rule 7c4d9e2a.
- §07 build itself lives in `/tmp/composer-e2e/spraypixel-state.html` (not repo-tracked).
- Pre-existing uncommitted changes (skillopt/*, semantic-organization) are
  unrelated to this work — leave them.
