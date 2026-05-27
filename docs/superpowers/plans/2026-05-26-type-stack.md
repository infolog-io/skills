# Plan — Type stack + column grid + light/dark switch

**Date:** 2026-05-26
**Owner:** bdl@infolog-io
**Scope:** Expand the component-composer type system from "font-family + 4 sizes" to a complete typography + layout foundation. Cover both existing themes (infolog-io, infolog-terminal) plus the baseline that future themes inherit.
**Out of scope:** New themes. Re-running the full E2E. Native renderers. PNG/PDF export plumbing.
**Status:** ready to execute, sequenced in 5 phases.

---

## Goal

Three things land together:

1. **Type stack** — h1–h5 HTML headings + p + small + 8 semantic callouts (code/pre/kbd/time/metric/unit/delta/id), at a perfect-5th heading scale floored at 18px, sized for legibility, with weight/leading/tracking tokenized.
2. **Column grid** — 4/8/12 responsive grid at 640/1024 breakpoints. Tokenized gutters and margins.
3. **Light/dark/system switch** — base capability in every artifact. Themes declare supported modes.

All three are *composer-level baselines* defined in `skills/component-composer/references/output-style.md`. Themes override values in their `palette.md`. Drafters read both before composing.

---

## Decisions (locked in conversation, do not relitigate)

| Decision | Value | Source |
|---|---|---|
| Font baseline (sans) | DM Sans → system stack | This conversation |
| Font baseline (mono) | JetBrains Mono → system mono stack | This conversation |
| Font loading | System-stack only. No CDN, no @font-face base64. | Architectural rule (no external requests) |
| Heading scale | Perfect 5th (×1.5) from body | This conversation |
| Heading floor | h5 = 1.125rem (18px), distinct from p (16px) | Avoid h5 == body collision |
| Body | 1rem (16px) — web default | Legibility |
| Caption | 0.875rem (14px) | Legibility floor; raises infolog-io's previous 10.7px |
| Heading nomenclature | `h1` through `h5` HTML elements | User: "use HTML nomenclature" |
| Heading family | Sans only — DM Sans (atomic) / JetBrains Mono (bloomberg). No serif. | User: "replace Georgia with DM Sans" |
| Weight tokens | regular 400, medium 500, semibold 600, bold 700 | Standard |
| Leading tokens | tight 1.15, snug 1.3, normal 1.45–1.5 (theme-set) | Standard |
| Tracking tokens | tight, normal, wide (theme-set values) | Standard |
| Code/data semantics | `<code>`, `<pre>`, `<kbd>`, `<time>`, `.metric`, `.unit`, `.delta` (+up/+down), `.id` | This conversation |
| Column counts | 4 / 8 / 12 at mobile / tablet / desktop | This conversation |
| Breakpoints | 641px (mobile→tablet), 1024px (tablet→desktop) | This conversation; matches validator viewports closely |
| Gutters | 12 / 16 / 24px (from --space-3, --space-4, --space-6) | Spacing scale |
| Margins | 16 / 32 / 48px (from --space-4, --space-8, --space-12) | Spacing scale |
| Max page width | 1280px desktop | This conversation |
| Theme modes | switch is base capability; themes declare in themespec.json | This message |
| Default mode | `system` (follow OS preference) | UX standard |
| Switch persistence | localStorage key `composer-theme-mode` | Standard pattern |

---

## Phase 1 — Tokens in `output-style.md`

Add a "Token baseline" section to `skills/component-composer/references/output-style.md` declaring the full token vocabulary. Themes still declare concrete values in their `palette.md`; this section defines the *names* and the baseline defaults.

New tokens to add (in addition to existing `--paper`, `--ink`, etc.):

```css
/* Type families — baseline */
--sans: "DM Sans", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
--mono: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, "Courier New", monospace;

/* Heading scale — perfect 5th, h5 floored */
--font-size-h1: 5.063rem;   /* 81px */
--font-size-h2: 3.375rem;   /* 54px */
--font-size-h3: 2.25rem;    /* 36px */
--font-size-h4: 1.5rem;     /* 24px */
--font-size-h5: 1.125rem;   /* 18px */

/* Body scale */
--font-size-body:    1rem;     /* 16px */
--font-size-caption: 0.875rem; /* 14px */

/* Weight */
--weight-regular:  400;
--weight-medium:   500;
--weight-semibold: 600;
--weight-bold:     700;

/* Leading */
--leading-tight:  1.15;
--leading-snug:   1.3;
--leading-normal: 1.5;

/* Tracking */
--tracking-tight:  -0.02em;
--tracking-normal: 0;
--tracking-wide:   0.06em;

/* Font features */
--features-tabular:      "tnum" 1, "liga" 0;
--features-no-ligatures: "liga" 0;

/* Column grid (driven by media queries) */
--grid-cols: 4;
--grid-gutter: var(--space-3);
--grid-margin: var(--space-4);
--grid-max-width: 1280px;

@media (min-width: 641px)  { :root { --grid-cols: 8;  --grid-gutter: var(--space-4); --grid-margin: var(--space-8); } }
@media (min-width: 1024px) { :root { --grid-cols: 12; --grid-gutter: var(--space-6); --grid-margin: var(--space-12); } }
```

Acceptance:
- `output-style.md` documents every new token with a one-line purpose.
- The "Default font stacks" subsection (added in last session) folds into the new "Token baseline" section.
- Drop the old `--serif` from required vocabulary; mark optional. infolog-io keeps Georgia for any element it chooses, but headings are sans now.

---

## Phase 2 — Required CSS base in `output-style.md`

Add a "Required CSS base" subsection. Every artifact must include this block (themes append, do not replace).

Includes:

1. **Reset + box-sizing** — `* { box-sizing: border-box; }` + body margin 0
2. **Body** — uses var(--sans), --font-size-body, --leading-normal, --ink, --paper
3. **h1–h5** — all use var(--sans), perfect-5th sizes, weight cascade (bold→medium), tight→snug leading, tight→normal tracking
4. **p, small** — text scale, body weight regular, max-width 66ch on p
5. **Semantic callouts** — `code`, `pre`, `kbd`, `time`, `.metric`, `.unit`, `.delta` + `.delta-up` + `.delta-down`, `.id`
6. **`.grid`** — `display: grid; grid-template-columns: repeat(var(--grid-cols), 1fr); gap: var(--grid-gutter); max-width: var(--grid-max-width); margin: 0 auto; padding: 0 var(--grid-margin);`
7. **Span utilities** — `.span-1` through `.span-12`, `.span-full`, plus `.md-span-*` (≥641px) and `.lg-span-*` (≥1024px)
8. **Theme mode switch component** — see Phase 4

Themes may *style* (color, weight, casing) the semantic callouts; they may not redefine the structural CSS or rename utilities.

Acceptance:
- `output-style.md` has the entire base CSS as a copyable code block.
- A drafter producing a new artifact must `<style>`-include this base verbatim, then theme overrides.
- `token_compliance` mechanical check expands to validate weight/leading/tracking values resolve to `var(--...)`. (Defer the check expansion to Phase 6 if it complicates.)

---

## Phase 3 — Theme updates: `palette.md` rewrites

Both themes' `palette.md` files declare concrete values for the new tokens.

### infolog-io

```css
/* type — DM Sans + JetBrains Mono baseline (already landed) */
--sans: "DM Sans", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
--mono: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, "Courier New", monospace;
--serif: ui-serif, Georgia, "Times New Roman", serif; /* optional; unused by headings */

/* Sizes — perfect 5th */
--font-size-h1: 5.063rem;
--font-size-h2: 3.375rem;
--font-size-h3: 2.25rem;
--font-size-h4: 1.5rem;
--font-size-h5: 1.125rem;
--font-size-body: 1rem;
--font-size-caption: 0.875rem;

/* Weights — atomic uses semibold for headings to feel editorial-modern */
--weight-regular: 400;
--weight-medium: 500;
--weight-semibold: 600;
--weight-bold: 700;

/* Leading — looser than bloomberg for readability */
--leading-tight: 1.15;
--leading-snug: 1.3;
--leading-normal: 1.5;

/* Tracking — slightly tight for large headings */
--tracking-tight: -0.02em;
--tracking-normal: 0;
--tracking-wide: 0.06em;

/* Light mode palette (current) */
--paper: #fafaf7; --paper-soft: #f3f1ea;
--ink: #1a1a1a;   --ink-soft: #555;
--accent-warm: #c8553d; --accent-cool: #2c5e6f; --accent-quiet: #888;
--gray-100: #f0eee6; --gray-300: #d1cfc5; --gray-500: #87867f; --gray-700: #3d3d3a; --gray-900: #141413;

/* Dark mode palette (new — required by switch) */
[data-theme="dark"] {
  --paper: #161413; --paper-soft: #1f1c1a;
  --ink: #f5f1e9;   --ink-soft: #a8a39b;
  --accent-warm: #d97757; --accent-cool: #5fa3b7; --accent-quiet: #6b6b6b;
  --gray-100: #2a2724; --gray-300: #3d3a35; --gray-500: #6d6a64; --gray-700: #adaaa3; --gray-900: #e8e3d8;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    /* same as [data-theme="dark"] above — DRY via CSS @when when supported, else duplicate */
  }
}
```

### infolog-terminal

```css
/* type — JetBrains Mono everywhere */
--sans: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, monospace;
--mono: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, monospace;
--serif: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, monospace;

/* Sizes — same perfect-5th scale; bloomberg's density comes from line-height and spacing, not type size */
--font-size-h1: 5.063rem; ... (identical to atomic)

/* Weights — bloomberg uses bold/medium for headings to read like terminal output */
--weight-bold: 700;
... (identical names, values)

/* Leading — tighter than atomic */
--leading-tight: 1.15;
--leading-snug: 1.25;
--leading-normal: 1.4;

/* Tracking — wider for caps */
--tracking-tight: 0;
--tracking-normal: 0.02em;
--tracking-wide: 0.08em;

/* Dark-only palette (current) */
--paper: #0a0e0a; ...
```

infolog-terminal declares `"modes": ["dark"]` in its `themespec.json` — switch shows current mode (dark) but cannot toggle. Optional: bloomberg adds a "light" amber-on-cream Bloomberg-Terminal-paper variant; out of scope for this plan unless the user calls it.

Acceptance:
- Both `palette.md` files contain every new token with a concrete value.
- infolog-io adds the dark-mode palette block.
- infolog-terminal's `themespec.json` gains `"modes": ["dark"]`.

---

## Phase 4 — Light/dark/system switch (new base capability)

Lives in `output-style.md` as required component. Every artifact gets it.

### HTML

```html
<div class="theme-switch" role="group" aria-label="Theme">
  <button data-mode="light"  aria-pressed="false" title="Light">☀</button>
  <button data-mode="dark"   aria-pressed="false" title="Dark">☾</button>
  <button data-mode="system" aria-pressed="true"  title="System">⌘</button>
</div>
```

### CSS

```css
.theme-switch {
  position: fixed; top: var(--space-3); right: var(--space-3);
  display: flex; gap: 0;
  background: var(--paper-soft);
  border: 1px solid var(--gray-300);
  border-radius: 6px;
  padding: 2px;
  font-family: var(--mono);
  z-index: 100;
}
.theme-switch button {
  border: 0; background: transparent;
  width: 28px; height: 24px;
  font-size: 14px; line-height: 1;
  cursor: pointer; color: var(--ink-soft);
  border-radius: 4px;
}
.theme-switch button[aria-pressed="true"] {
  background: var(--paper); color: var(--ink);
}
@media (max-width: 480px) { .theme-switch { top: var(--space-2); right: var(--space-2); } }
```

### JS

```js
(function () {
  const KEY = 'composer-theme-mode';
  const html = document.documentElement;
  const apply = (mode) => {
    if (mode === 'system') delete html.dataset.theme;
    else html.dataset.theme = mode;
    document.querySelectorAll('.theme-switch button').forEach(b => {
      b.setAttribute('aria-pressed', b.dataset.mode === mode);
    });
  };
  const init = () => {
    const saved = localStorage.getItem(KEY) || 'system';
    apply(saved);
    document.querySelectorAll('.theme-switch button').forEach(b => {
      b.addEventListener('click', () => {
        const m = b.dataset.mode;
        localStorage.setItem(KEY, m);
        apply(m);
      });
    });
  };
  if (document.readyState !== 'loading') init();
  else document.addEventListener('DOMContentLoaded', init);
})();
```

### Theme integration

Each theme's CSS scopes its dark/light palette via `[data-theme="dark"]` + the `prefers-color-scheme` fallback. The switch only toggles the `data-theme` attribute; CSS does the rest.

Themes that support only one mode (e.g., infolog-terminal) include the switch markup but hide irrelevant buttons via CSS, or render a one-button readout instead. Decision deferred to the bloomberg update.

### Architectural note

This is the first JS in the artifact base. The current `output-style.md` says "Vanilla `<script>` only when interaction is real". A theme switch is real interaction — passes. Bundle stays small (~30 lines).

Acceptance:
- `output-style.md` declares the switch as required, with HTML + CSS + JS blocks.
- infolog-io light + dark both render correctly when toggling.
- infolog-terminal respects its `modes: ["dark"]` declaration.
- `system` mode follows `prefers-color-scheme` and updates live on OS change (CSS media query auto-reacts).
- localStorage persists across reloads.

---

## Phase 5 — Drafter protocol update

`skills/component-composer/references/drafter-protocol.md` gets a new "Required artifact structure" subsection:

1. Every artifact uses `<h1>` through `<h5>` HTML elements for headings. No custom `.display` / `.lead` classes for heading roles.
2. Numeric values that are the headline of a card use `<span class="metric">N</span><span class="unit">u</span>`. Unit margin and spacing per theme.
3. Tabular data cells use `<time>` for timestamps, `<code>` for identifiers/snippets, `.id` class for repo names / hashes.
4. Layout uses `.grid` containers with `.span-*` utilities. No bespoke flex layouts for top-level structure.
5. Every artifact includes the theme switch from Phase 4.
6. Drafter reads `palette.md` AND `output-style.md` baseline. Tokens from `palette.md` take precedence over `output-style.md` defaults.

Acceptance:
- `drafter-protocol.md` reflects all 6 rules.
- A regression test artifact is built that exercises every new pattern at least once.

---

## Known issues to fix as part of this work

1. **bloomberg metric+unit "131days" is janky.** The 54px bold mono number sits flush against the 14px uppercase unit with only 4px gap. Fixes to land in Phase 3:
   - `.metric` weight drops from `--weight-bold` (700) to `--weight-medium` (500) in bloomberg only. Bold mono at 54px reads heavy.
   - `.unit` margin-left bumps from 4px to `var(--space-2)` (6px in bloomberg).
   - `.unit` gets `vertical-align: baseline` and is wrapped in a baseline-shifted span if needed, OR `.metric` and `.unit` are wrapped in a flex container with `align-items: baseline; gap: var(--space-2);`.
   - For numbers with units of 3+ chars (e.g., "days", "events"), consider abbreviating ("d", "ev") in bloomberg to keep the metric-and-unit pair compact.

2. **infolog-io iter-02 still has SVG text overflow on activity-windows** (carried over from E2E findings). Fix is a HTML+SVG hybrid for slopegraph row labels. Not part of this plan; logged in `docs/e2e-component-composer-2026-05-26.md`.

3. **`text_truncation` mechanical check misses SVG `<text>` overflow.** Fix: add an SVG-specific overflow check that compares each text bbox against the parent SVG's viewBox. Not part of this plan; logged in same E2E doc.

4. **Shorthand CSS property literal-leak in `token_compliance`.** `padding: var(--space-12) var(--space-4)` may serialize back to longhand literal px values, slipping past the check. Phase 6 task if `token_compliance` expands.

---

## Phase 6 (optional, deferred decision) — Validator extension

Extend `token_compliance` to require `var(--...)` references for `font-weight`, `line-height`, `letter-spacing`, `font-feature-settings`. New criterion ID: keep `token_compliance` unified or split into `type_token_compliance` + `space_token_compliance`?

Defer unless typography violations slip through during early use. Re-evaluate after the first 3-5 artifacts ship.

---

## Order of operations

| # | Task | File(s) | Effort |
|---|---|---|---|
| 1 | Add Token baseline section to output-style.md | `skills/component-composer/references/output-style.md` | S |
| 2 | Add Required CSS base section (full block) | same | M |
| 3 | Add light/dark/system switch HTML+CSS+JS block | same | M |
| 4 | Rewrite infolog-io palette.md with full token set + dark palette | `skills/infolog-io/references/palette.md` | M |
| 5 | Rewrite terminal palette.md with full token set | `skills/infolog-terminal/references/palette.md` | M |
| 6 | Add `modes: ["dark"]` to terminal themespec.json | `skills/infolog-terminal/themespec.json` | XS |
| 7 | Add `modes: ["light", "dark", "system"]` to infolog-io themespec.json | `skills/infolog-io/themespec.json` | XS |
| 8 | Update drafter-protocol.md with the 6 required-structure rules | `skills/component-composer/references/drafter-protocol.md` | S |
| 9 | Rebuild final-infolog-io.html artifact with new base + grid + switch | `/tmp/composer-e2e/final-infolog-io.html` (test artifact) | M |
| 10 | Fix bloomberg metric+unit jankiness (Phase 3 sub-task) | bloomberg palette.md + base CSS | S |
| 11 | Rebuild final-infolog-terminal.html artifact with new base + grid + switch | `/tmp/composer-e2e/final-infolog-terminal.html` (test artifact) | M |
| 12 | Run mechanical validator on both rebuilt artifacts at 3 viewports | preview_eval | S |
| 13 | Visual LLM-judge pass + switch interaction test | preview screenshot at each mode | S |

Estimated total: ~3 hours of focused work.

---

## Acceptance criteria

1. `output-style.md` declares the full token vocabulary + required CSS base + switch component.
2. Both theme `palette.md` files use the new tokens with concrete values; atomic has both light + dark palettes.
3. Both themes' `themespec.json` declare supported modes.
4. `drafter-protocol.md` reflects the structural requirements.
5. `final-infolog-io.html` rebuilt with the new base passes mechanical validator at 3 viewports + the switch toggles between light/dark/system correctly.
6. `final-infolog-terminal.html` rebuilt likewise; switch hides irrelevant buttons; mechanical passes.
7. `.metric` + `.unit` pair in bloomberg renders without the visual gap-jank.
8. `node --test mechanical-checks.test.js` stays 31/31 green.
9. No external requests in either artifact (network panel verified).
10. Plan doc closes with a one-line outcome at the bottom.

---

## Followups (not in scope, log only)

- HTML+SVG hybrid layout pattern for slopegraphs (atomic activity-windows clipping) — **DONE in-session** as `.windows` grid in `infolog-io` final; promote to `output-style.md` base when a second consumer needs it
- SVG text-overflow mechanical check (validator gap from E2E)
- `font_token_compliance` validator extension (Phase 6 decision)
- infolog-io could add a separate display-only `.lede` class if hero pages need it — wait for use case
- infolog-terminal optional light palette (amber-on-cream Bloomberg-terminal-paper) — wait for ask
- **Split the generator-critic loop into its own skill** — current composer bundles a generic loop pattern with HTML-specific scaffolding. Trigger condition: when sketching a second `<thing>-composer` for a non-HTML artifact (markdown, code, schemas, prose). Extract `loop-protocol.md`, `drafter-contract.md` (abstract), `validator-contract.md` (abstract dispatch), `hud-protocol.md`, iteration history, stuck detection. Keep HTML-specific output-style + mechanical-checks + base.html in `component-composer`.
- **Casual / throwaway HTML extension skill** — `component-composer/SKILL.md` now scopes itself to production-grade data graphics and explicitly defers to Thariq Shihipar's [Unreasonable Effectiveness of HTML](https://www.anthropic.com/engineering/claude-code-html) for casual cases. Followup is a *separate* sibling skill (proposed name: `html-sketch`) that implements his patterns: throwaway editors, sliders/knobs for interactive tuning, copy-as-prompt footer, "make me a one-off HTML to triage these tickets" use cases. Out of scope to build now — would re-architect fresh code immediately after committing. Build when a real throwaway-editor use case lands.

---

## Outcome

Landed 2026-05-26 in one session.

**Files changed (committable):**
- `skills/component-composer/references/output-style.md` — rewritten: Token baseline + Required CSS base + Theme switch component (HTML/CSS/JS)
- `skills/component-composer/references/drafter-protocol.md` — added "Required artifact structure" section with 6 rules
- `skills/infolog-io/references/palette.md` — full token set + dark mode palette
- `skills/infolog-terminal/references/palette.md` — full token set + metric+unit jank fix + delta color inversion
- `skills/infolog-io/themespec.json` — version 0.0.1, modes [light, dark, system]
- `skills/infolog-terminal/themespec.json` — version 0.0.1, modes [dark]

**Artifacts rebuilt:**
- `/tmp/composer-e2e/final-infolog-io.html` — full new base, h1–h5 HTML, .metric/.unit pattern, .grid layout, theme switch with working light/dark/system toggle
- `/tmp/composer-e2e/final-infolog-terminal.html` — same base, JetBrains Mono throughout, dark-only theme switch, fixed metric+unit, progressive table column hiding (5/3/2 cols at desktop/tablet/mobile)

**Verification:**
- Mechanical validator: 9/9 PASS at desktop, tablet, mobile for both artifacts
- Unit tests: 31/31 still green
- Regression fixtures: all assertions pass
- Theme switch verified by toggling and re-reading `data-theme` + computed background

**Bugs caught + fixed during rebuild:**
- `token_compliance` flagged `.theme-switch button { font-size: 14px }` literal — replaced with `var(--font-size-caption)`
- `contrast_failure` flagged bloomberg `.annotation` at `--accent-quiet` (2.73:1) — moved all text-class uses of accent-quiet to `--ink-soft` (~8:1); accent-quiet reserved for decorative prefixes only
- `overflow` at tablet on bloomberg events tables side-by-side — dropped `md-span-4`, tables stack at tablet now, only side-by-side at desktop
- `overflow` at mobile on bloomberg from h1 81px mono caps + wide `.bar` columns — `h1` switched to `clamp(--font-size-h3, 12vw, --font-size-h1)`; `.bar` columns hidden at mobile across all data-tables

**Deferred to followups (out of scope this plan):**
- HTML+SVG hybrid layout for slopegraphs (carried from E2E doc)
- SVG `<text>` overflow mechanical check (carried)
- `token_compliance` expansion to weight/leading/tracking (Phase 6 deferred)
- infolog-io iter-02 activity-windows long-row-label clipping (carried)
- Shorthand-CSS literal-leak in token_compliance (validator gap)

Confidence: high on the docs landing correctly. Medium on the rebuilt artifacts — verified mechanically and visually in Claude Preview, but no real-user round of judgment.
