# Handoff — infolog.lib design system (post §11 + Charts reorg)

Date: 2026-05-31 (refreshed end-of-session)
Branch: `feat/component-composer` (repo: infolog-skills)
Supersedes: the earlier 2026-05-31 handoff (post §10 + theme fix).

## Canonical page + preview

Canonical live page: `docs/superpowers/reference/infolog-lib-design-system.html`
(repo, now **tracked** as of this session's commit). ~1740 lines. Byte-identical working copies at
`/tmp/dslib.html` and `/tmp/composer-e2e/spraypixel-state.html`. Edit the canonical;
`cp` to both after every change (the feedback compiler's prompt path expects the
composer-e2e copy).

Preview (PIP e3c9a7d4 — file://, NO localhost): `agent-browser open "file://<abs path>"`.
Dark: `eval "document.documentElement.setAttribute('data-theme','dark')"`, or click the
theme switch by index `eval "document.querySelectorAll('.theme-switch button')[1].click()"`
(0=light, 1=dark, 2=system). Targeted shot: `scrollintoview "#id"` THEN `screenshot`.
Console: `agent-browser console` (empty = clean). Measure geometry with
`eval "...getBoundingClientRect()..."` — caught the §10 alignment bug deterministically.

⚠️ **Chromium masks Safari.** agent-browser drives Chromium (allows file:// localStorage;
Safari throws). To test as the user sees it, inject the localStorage-throw shim at the
top, then exercise. Memory: `file-url-localstorage-guard`.

## This session — completed + verified (light & dark, console clean)

1. **§11 Motion & animation — BUILT.** Tokens `--dur-fast/base/slow` (120/160/240ms) +
   `--ease-standard` / `--ease-out`. All 9 hardcoded transitions/animations graduated to
   `var(--dur/--ease)`. Reduced-motion = one `:root` token override (`0.01ms`, not `none`,
   so `animationend` still fires). §11 section: duration + easing readout tables + a
   ping-pong Replay demo (two lanes, `--dur-slow`). Spec/plan: `docs/superpowers/specs/2026-05-31-motion-animation-design.md`, `docs/superpowers/plans/2026-05-31-motion-animation.md` (both untracked).
2. **Ghost button** border 2px → 1px (dropped the `.btn.ghost` `border-width` override;
   it now inherits the base 1px, distinguished only by grey colour).
3. **Removed chart skeletons** from §06 Mockup primitives (4 SVG figures + the dead
   `.mockup-frame.chart` CSS; h2 → "Four chrome surfaces."; desc trimmed).
4. **§08 sparkline fixes:** showcase → responsive grid of framed "chart space" cells,
   titles `white-space: nowrap`, label simplified to "Sparkline types". Stacked = one
   colour, two shades (`--success` bottom, `color-mix(... white 45%)` top — NOT
   `fill-opacity`, which inverts darker/lighter on a dark bg). Tristate middle → `--info`
   blue. Bullet → all greyscale (`gray-100` track / `gray-300` range / `gray-700` measure /
   `ink` target).
5. **Charts section reorg.** Relocated the entire former §07 Data viz to AFTER §08 Data
   table, renamed it **Charts**, folded the sparkline showcase in as its own grid at the
   end. Renumbered: Data table → `07`, Charts → `08`. Updated the JS feedback arrays:
   `SECTIONS` datatable label → 07, `VIZ` labels 07 → 08, and `ALL = SECTIONS.slice(0, 7)
   .concat(VIZ, SECTIONS.slice(7))` so compiled order tracks the new DOM order.
6. **§10 Elevation alignment fix.** `.e-raised/.e-overlay/.e-modal` were misaligned: the
   `lg-span-8` header + `lg-span-4` first card summed to 12 cols, pulling the first card
   into the header row. Split into two grids (header, then cards) — the §06 pattern.
   Verified all three cards now top=47 / h=132.

Current section order: 01 Type · 02 Color · 03 Buttons · 04 Alerts · 05 Inline + tiles ·
06 Mockup primitives · **07 Data table** · **08 Charts** (doctrine + example charts +
sparkline gallery) · 09 Inputs & forms · 10 Elevation · 11 Motion · feedback coda.

## Lessons / cautions for next session

- **`color-mix`, not `fill-opacity`, for theme-robust two-shade fills.** Opacity over a
  dark background darkens — inverts "lighter on top." `color-mix(in srgb, X, white N%)`
  stays lighter in both themes.
- **Grid auto-flow trap.** A `lg-span-8` header followed by a child that fits the
  remaining columns (e.g. `lg-span-4`) flows up into the header row. Split header and
  content into separate `.grid` blocks (the §06 pattern).
- **Feedback system is data-driven.** Panels + compiled order come from the `SECTIONS` /
  `VIZ` arrays and `ALL = SECTIONS.slice(0,N).concat(VIZ, SECTIONS.slice(N))`. Reordering
  or renumbering sections means updating these too, not just the eyebrows.
- **Grey tokens invert by theme by design** (gray-100 = subtle bg, gray-700 = strong fg in
  both). Greyscale specimens stay readable across themes for free.
- **Never `unicode_escape` strings with literal `·`/`—`** (mojibake). Write UTF-8 direct.
- **Verify structure with deterministic Python byte reads, behaviour with real clicks /
  getBoundingClientRect.** Big structural moves: content-anchored Python transform with
  assertions, not 50-line string edits.

## Still queued

- **§11 Motion has no feedback panel** — it was never added to the `SECTIONS` array. Quick
  fix: add `{ id: 'motion', label: '11 · Motion & animation' }`. (Offered, not yet done.)
- **Card / section height tokens** — 8px-baseline `--h-*`, max-height + scroll.
- **Build the generic `design-system` skill** per
  `docs/superpowers/plans/2026-05-30-design-system-skill.md`.

## Housekeeping

- Committed this session (one commit on `feat/component-composer`, not pushed, no tag):
  the canonical reference page + the §11 motion spec/plan + this handoff. The canonical
  page is now **TRACKED** — future edits show as modifications; keep `cp`-ing to the two
  `/tmp` mirrors after each change.
- The unrelated in-progress SkillOpt work (`tools/skillopt/*`,
  `skills/semantic-organization/SKILL.md`, `tasks/`, `docs/BACKLOG.md`) stays UNCOMMITTED
  — separate effort, do NOT clobber or fold into design-system commits.
- Stray `./--full-page` PNG at repo root predates this session; untracked.

## PIP status

`.claude/CLAUDE-PIP.md` — 3 rules, all audited **keep** this session (7c4d9e2a SemVer,
e3c9a7d4 file:// preview, a9d2f4c1 resume block). No drops, no refines, no promotions.
