# Handoff — infolog.lib §08 field guide: polish iteration

Date: 2026-06-01
Branch: `feat/component-composer` (repo: infolog-skills)
Supersedes for active work: continues from `docs/superpowers/2026-05-31-design-system-session-handoff.md`
(that doc has the field-guide BUILD history; this doc is the POLISH iteration, mid-flight).

## UPDATE — P4 + P5 COMPLETE (commit `aeff763`)

The Apple-augmented polish pass landed and is verified light + dark. What shipped:

- **Rounded corners** — `rx="2"` on 36 data-bar rects (both funnels, ARR waterfall,
  Repos-by-month, §08 Marks "Bar", a11y installs); `rx="1.5"` on 41 heatmap cells +
  legend. OHLC candles, box-plot box, stacked/tristate marks left sharp by convention.
- **Network edges** `gray-300 → gray-500` (10 Bézier paths) — now traceable on both
  themes; the dark-mode win is large (gray-300 `#3A3A3C` was near-invisible on `#161413`).
- **Stroke orphan** — the lone `1.25` (latest OHLC wick) normalized to `1`. Vocab now
  clean: 0.5 / 1 / 1.5 + accents 2 / 2.5 / 3 (median tick, bullet target, focus ring).
- **Two clipping fixes** found in the squint pass (item 7):
  - Funnel values `1000`/`480` were clipped to `10`/`48` at the 320 viewBox edge →
    both funnel viewBoxes widened to **340**; values now render in full.
  - Throughput `req/s` used a CSS `rotate(180deg)` (spins about SVG origin → off-canvas)
    → switched to the house `transform="rotate(-90,14,113)"`; now sits on the y-axis.
- **No-change verifications**: tabular-nums already satisfied (mono + CSS `font-variant-numeric`
  on `.metric`/`td.num`/`.z-val`); ink-soft AA contrast **7.5:1** light / **7.3:1** dark;
  plot insets fine (continuous series span full width by design; scatters have margins).

Deliberately **not** done: thousands separators (tried `1000→1,000`, reverted — off-brand
for this mono-tabular terminal aesthetic and it over-ran the funnel edge). Residual: x-axis
titles `day`/`concurrency`/`step` clip **1.2px** at descender tips — sub-perceptual, verified
legible by eye, left as-is. Marks `Stacked`/`Tristate` left sharp (rounding stacked segments
notches the joins) — easy opt-in if wanted.

**Next: push + PR-base decision — still the user's call (HELD).** Branch `feat/component-composer`
is now 83 commits ahead of `origin/main`. Field-guide polish iteration is complete.

---

## State: where we are

The §08 chart field guide is **built and verified** (13 figures, 5 families + catch-all, 5
illustrative-tagged). Then a **believability redesign** of the 3 weak charts **landed**:

- **PCA + UMAP** — replaced hand-placed dots with seeded-Gaussian clouds: PCA = elongated
  cloud, 3 overlapping clusters + 2 outliers; UMAP = 4 tight irregular blobs + 3 stray bridge
  points. Now believable.
- **Network** — full redesign: deliberate hierarchy (3 labeled plugin hubs → grouped skills),
  `html-sketch` + `generator-critic` as the genuinely-shared nodes, curved Bézier edges,
  minimal crossings. Now reads as a real skill-relationship map.

Verified light + dark, console clean, mirrors md5-identical. Committed `4d1b33b`. Nothing pushed.

## IMMEDIATE NEXT ACTION — P4: Apple-augmented polish sweep (all 13 charts)

User feedback that triggered this iteration (from the feedback compiler):
> "make them believable AND legible … augment our rules with Apple Data Visualization, HIG, so
> these look consumer-grade." (Believability already addressed by the redesign above.)

Apply across every figure (cheap, high-leverage; most charts already follow the doctrine so this
is refinement, not rework):

1. **Rounded corners** — add `rx="2"` to every bar `<rect>` (funnels, sales funnel, ARR waterfall,
   the §08 Marks bar example, a11y bars) and `rx="1.5"` to heatmap cells. *The single biggest
   consumer-grade signal per Apple.*
2. **Tabular numerals** — numeric tick/value text already uses `var(--mono)` (monospaced =
   tabular), so this is mostly satisfied; add `font-variant-numeric: tabular-nums` to any
   sans-set metric text for safety.
3. **Thousands separators** — funnel values `1000`→`1,000`, `840` etc. stay; abbreviate only if
   space-tight. Low priority.
4. **Plot insets / breathing room** — confirm marks aren't flush to axes (Apple: ~8-16px inset
   before first tick). Spot-check the line + error-band charts.
5. **Stroke vocabulary** — already normalized to 0.5 / 1 / 1.5 (the `1.2` PCA-arrow orphan was
   fixed in `9addfcf`). Verify no new orphans introduced.
6. **Contrast (AA)** — verify `var(--ink-soft)` axis labels hit ≥4.5:1 on both `--paper` themes;
   marks ≥3:1. Bump toward `--ink` if any label is borderline.
7. **No collisions / clipping** — final pass (SLO label + ROC/PR titles already fixed). Squint at
   every figure in both themes.
8. **Network edge weight (user-offered)** — optionally bump network edges `gray-300`→`gray-500`
   so connections read more strongly. ASK or just try it and screenshot — the user flagged the
   edges are "a touch subtle to trace."

Then **P5**: full-guide light+dark verify, console clean, mirrors md5-identical, holistic
consistency review, commit (`feat(design-system): field guide — Apple-augmented polish pass`).

**Recommendation:** run P4 subagent-driven (one implementer + one reviewer per the prior pattern)
OR inline; verify each change in-browser. The charts are SVG — converge in the browser.

## The augmented rules (the polish bar = our doctrine + Apple + impeccable)

Our six-dimension doctrine (Goal/Marks/Axes/Descriptions/Accessibility/Color, rules R01-R06) stays
the base. Augment with:

- **Believability is Apple's #1 tell**: real-shaped data — variance, cluster overlap, outliers,
  gaps. (Done for projections/network; keep for any new chart.)
- **Numbers**: tabular figures; abbreviate large axis values (1.2K); right-align numeric ticks.
- **Finish**: rounded corners 2-3px on bars/cells; consistent stroke vocab 0.5/1/1.5; ~8-16px plot
  inset; balanced saturation so no color accidentally dominates.
- **Color stays semantic** (green-up/red-down/blue-ref/gray-context) — it's directional + paired
  with position/labels, so it passes Apple's "color is additive" test. Keep.
- **Legibility/contrast**: WCAG AA; no collisions; no clipping; quiet secondary-label axis treatment.

Apple sources: HIG "Charting data", WWDC22 "Design an Effective Chart" / "Design App Experiences
with Charts" / "Swift Charts: Raise the Bar". impeccable `polish` flow: align to existing design
system first (done — the page IS the system), then sweat details, verify in-browser.

## Canonical + mirror + preview (PIP e3c9a7d4 — file://, NO localhost)

- Canonical (edit this): `docs/superpowers/reference/infolog-lib-design-system.html` (~2050 lines).
- After EVERY edit, `cp` to BOTH: `/tmp/dslib.html` AND `/tmp/composer-e2e/spraypixel-state.html`
  (the composer-e2e dir EXISTS; if a `cp` errors, `mkdir -p /tmp/composer-e2e` — a subagent once
  misreported it missing). Verify with `md5 -q` on all three.
- Preview:
  ```
  agent-browser open "file:///Users/informationlogistics/Developer/infolog-skills/docs/superpowers/reference/infolog-lib-design-system.html"
  agent-browser eval "document.querySelector('svg[aria-label*=\"PCA\"]').closest('figure').scrollIntoView({block:'center'})"
  agent-browser screenshot /tmp/x.png            # viewport shot — ALWAYS renders
  agent-browser eval "document.documentElement.setAttribute('data-theme','dark')"   # dark
  agent-browser console                          # empty = clean
  ```
- **Full-page render**: `agent-browser screenshot --full /tmp/full.png` (the flag is `--full`, NOT
  `--full-page`). Page is ~23000px tall and renders fine via `--full`.

## Gotchas (learned this session)

- **Feedback-injection boundary**: the field-guide opener `<div class="viz-chapter" id="dv-guide">`
  MUST keep `class="viz-chapter"` — it stops `dv-color`'s sibling-walk; without it the Color panel
  jumps past the guide.
- **`color-mix(... white N%)` not `fill-opacity`** for theme-robust fills. BUT large white-mix
  region fills (kNN zones, heatmap cells) render as a **light plotting surface on dark** — legible,
  intentional, cell strokes keep edges visible. If a subtler dark look is wanted later, mix toward
  `--paper` instead of `white` (applies to kNN + heatmap consistently). Flagged, not changed.
- **agent-browser element screenshots go BLANK on very tall elements** (`screenshot "section#dataviz"`
  returned 1280×12617 all-white). Use `--full` for whole-page, or viewport shots for sections.
- **Feedback compile is debounced 250ms** — a synchronous eval right after dispatching `input`
  reads stale `compiled-out` (false negative). Sleep ≥0.3s before checking.
- Charts converge in the browser (render→eyeball→nudge); the data + formulas are exact, pixels
  are tuned live. Don't blind-author SVG coordinates.

## Believable-data generator (reproducible — already applied, in case of regen)

Seeded Python (seed 7) wrote the PCA (42 pts) + UMAP (50 pts) circles now in the HTML. To regen:
PCA viewBox 320×300 plot [52,296]×[30,250], 3 rotated-Gaussian clusters (success/info/gray-700) +
2 outliers; UMAP viewBox 320×300 plot [30,300]×[32,262], 4 tight clusters (success/info/danger/
gray-700) + 3 strays. Full script is in the 2026-06-01 session transcript (P1 step).

## Commit state + PIP

- This session added 11 commits, `1a42226` → `4d1b33b`, on `feat/component-composer`. NOT pushed.
  Field-guide build: `9b7fe99`→`2caafbe`, verify `0919b6a`, polish-fix `9addfcf`, redesign `4d1b33b`.
- Branch ~80 commits ahead of `origin/main`. Push + PR-base decision still the user's call (held).
- Untracked on purpose: `tasks/`, `docs/BACKLOG.md`.
- **PIP audit (2026-06-01)**: `.claude/CLAUDE-PIP.md` — 3 rules, all exercised this session, all
  **keep**: 7c4d9e2a (SemVer pre-0.1/0.0.x; version still V0.0.3, no tag), e3c9a7d4 (file:// preview;
  used all session), a9d2f4c1 (resume block; firing now). No drops. No promotions requested.
