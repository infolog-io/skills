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
   ping-pong Replay demo (two lanes, `--dur-slow`). Spec/plan: `docs/superpowers/specs/2026-05-31-motion-animation-design.md`, `docs/superpowers/plans/2026-05-31-motion-animation.md` (committed in `c60a96e`).
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
   table, renamed it **Charts**. Renumbered: Data table → `07`, Charts → `08`. Updated the
   JS feedback arrays: `SECTIONS` datatable label → 07, `VIZ` labels 07 → 08, and
   `ALL = SECTIONS.slice(0, 7).concat(VIZ, SECTIONS.slice(7))` so compiled order tracks DOM.
7. **Sparklines integrated into Marks (de-bolted).** The sparkline gallery was first
   appended as a trailing grid (felt bolted on), then moved INTO the **Marks** dimension
   (dv-marks group) after the bar/dot examples, introduced by a lede ("The same marks
   shrink to sparklines…"). The "08 · Marks" feedback panel now follows it. All §08
   sparkline fixes (above) carried over.
6. **§10 Elevation alignment fix.** `.e-raised/.e-overlay/.e-modal` were misaligned: the
   `lg-span-8` header + `lg-span-4` first card summed to 12 cols, pulling the first card
   into the header row. Split into two grids (header, then cards) — the §06 pattern.
   Verified all three cards now top=47 / h=132.

Current section order: 01 Type · 02 Color · 03 Buttons · 04 Alerts · 05 Inline + tiles ·
06 Mockup primitives · **07 Data table** · **08 Charts** (doctrine + example charts;
sparkline gallery now inside the Marks dimension) · 09 Inputs & forms · 10 Elevation ·
11 Motion · feedback coda.

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

## Session update — 2026-06-01

- **§11 Motion feedback panel — DONE.** Added `{ id: 'motion', label: '11 · Motion & animation' }`
  to `SECTIONS`; `ALL`'s `slice(7)` auto-flows it last. Verified light/dark, feedback compiles.
  Commit `1a42226`.
- **§08 Chart field guide — DONE.** 13 figures in 5 job families + a catch-all, appended after
  the six dimensions. Opener `id="dv-guide"` carries the `viz-chapter` class — that is the
  feedback-injection boundary (stops `dv-color`'s sibling walk; without it the Color panel jumps
  past the guide). 8 figures implemented for real, 5 tagged `illustrative` (kNN, PCA, UMAP,
  network, correlation heatmap). New CSS `.fg-family/.fg-family-name/.fg-q/.fg-use/.fg-tag`; new
  `VIZ` entry `dv-guide`. Examples span AI/ML, finance, ops. Built subagent-driven (7 tasks,
  independent review each), verified light+dark, console clean, feedback live, three mirrors
  md5-identical. Spec `docs/superpowers/specs/2026-05-31-chart-field-guide-design.md`; plan
  `docs/superpowers/plans/2026-06-01-chart-field-guide.md`. Commits `9b7fe99` → `2caafbe`.
- Open design note: large `color-mix(... white N%)` region fills (kNN zones, heatmap cells) read
  as a light plotting surface on dark — intentional + legible, cell strokes keep edges visible.
  If a subtler dark treatment is wanted, switch those fills to mix toward `--paper` instead of
  `white` (consistent across both charts). Flagged, not changed.

## Still queued

- **Layout section (A)** — approved in brainstorm, not yet spec'd. Combined section documenting
  the existing column grid (4/8/12 + `.span-full`/`.md-span-*`/`.lg-span-*`, currently
  undocumented) AND adding `--h-*` height tokens (8px baseline) + max-height/scroll. Card/section
  height tokens fold into this. Placement (early-with-renumber vs append) still open. Needs its
  own spec → plan.
- **Build the generic `design-system` skill** per
  `docs/superpowers/plans/2026-05-30-design-system-skill.md`.

## Housekeeping

- Two commits this session on `feat/component-composer` (NOT pushed, no tag):
  - `c60a96e` feat(design-system) — canonical reference page (now **TRACKED**) + §11 motion
    spec/plan + this handoff. Future edits show as modifications; keep `cp`-ing to the two
    `/tmp` mirrors after each change.
  - `69a6372` chore(skillopt) — SkillOpt harness WIP (separate effort): accepted_epochs +
    minibatch fixes, lib refinements, 5 new adapters, `render/` node module (node_modules
    now gitignored), test_alignment, semantic-organization SKILL.md. 36 unit tests pass; NOT
    reviewed/optimized. `tasks/todo.md`'s scoped single-file PR plan is now stale (committed
    directly instead of as that PR).
- Branch is ~78 commits ahead of `origin/main` (9 added 2026-06-01), nothing pushed. Pushing
  publishes all of them + needs a PR-base decision — left to the user.
- Untracked, left out on purpose: `tasks/` (planning TODO), `docs/BACKLOG.md` (design
  backlog). The stray `./--full-page` PNG was deleted this session.

## PIP status

`.claude/CLAUDE-PIP.md` — 3 rules, all audited **keep** this session (7c4d9e2a SemVer,
e3c9a7d4 file:// preview, a9d2f4c1 resume block). No drops, no refines, no promotions.
