# E2E — component-composer (infolog-io + infolog-terminal)

**Date:** 2026-05-26
**Branch:** `feat/component-composer` at HEAD (post-v0.0.x; the `v1.0.0` tag is misnamed per `CLAUDE-PIP.md` rule `7c4d9e2a` and should be deleted)
**Driver:** single Claude Code session acting as composer + drafter + LLM-judge
**Inputs:** `/tmp/composer-e2e/data/{repos.json, events.json}` (23 repos, 100 events, 6-month window)
**Outputs:** `/tmp/composer-e2e/{iterations/, final-infolog-io.html, final-infolog-terminal.html}`
**Validator:** `node --test mechanical-checks.test.js` → 31/31 green pre- and post-E2E
**Confidence:** high on the observations below; medium on the v0.1 verdict (one full pass on one dataset, no external user, no PNG/PDF emission yet).

---

## TL;DR

The architecture works end-to-end. The drafter produces conformant artifacts. The mechanical validator runs in the real browser via `preview_eval` and catches real defects. The loop iterates on failures and converges. Two themes produce visually divergent outputs from the same data with zero composer code changes.

The E2E surfaced three real bugs in the v0.0.x mechanical-check implementation (all caught + fixed mid-run), one missing typographic rule (added across `output-style.md` + both theme criteria files), and three architectural tensions that block a v0.1 declaration — most importantly, SVG viewBox scaling forces a hard tradeoff between mobile font readability and desktop label fit.

---

## Success criteria verdict (against `docs/superpowers/specs/2026-05-23-component-composer-goal.md`)

| # | Criterion | Verdict | Evidence |
|---|---|---|---|
| 1 | Composer + `infolog-io` against GitHub data produces a single conformant HTML file | **PASS** | `final-infolog-io.html` 16.2KB, validates clean mechanically at 3 viewports |
| 2 | Mechanical layer flags every defect in the previous-session reference chart | **PASS (re-verified)** | `node regression-test.js` still: 3 fails on buggy fixture, 3 passes on clean — unchanged |
| 3 | Loop runs to convergence without manual intervention on the GitHub chart job | **PARTIAL** | Two iterations converged mechanically. Required two validator code patches mid-loop (not a drafter issue but a validator-defect issue). Counts as "manual intervention." |
| 4 | Switching theme name and re-running produces a visually different chart, no composer changes | **PASS** | `final-infolog-terminal.html` is dark green-on-black terminal density tables; `final-infolog-io.html` is light Tufte SVG. Zero composer code touched between runs. |
| 5 | Audit summary shows iteration count, token usage, resolved-during-loop list | **FAIL** | No audit summary was emitted. Cost tracking object exists in protocol but no scaffolding writes it. Counts/timings not captured. |
| 6 | HUD overlays during iteration, absent from final | **PASS** | HUD visible in iter-01 desktop screenshot via `preview_eval` injection of `hud.js`. Final artifacts contain no HUD scaffolding (navigated away cleared it; no `<script>` source remained). |
| 7 | Final artifact opens in any modern browser, no console errors, no external requests | **PASS** | `final-infolog-io.html` and `final-infolog-terminal.html` both render clean. No `<link>`, no `<script src>`, no `<img>`, no `import`. |
| 8 | PNG and PDF exports written alongside HTML | **FAIL** | `export-png.js` and `export-pdf.js` are protocol docs only. `preview_screenshot` returns a JPEG into the conversation but no built-in path to save bytes to disk from the Claude Code side. PDF via `printToPDF` not attempted. |
| 9 | Theme discovery finds both themes via `themespec.json` scan | **NOT TESTED** | Both themes resolved correctly by reading their `references/*.md` directly. The scan-based discovery code path was not exercised. |
| 10 | Persistent iteration history saved to session-dir/iterations/ | **PASS** | `/tmp/composer-e2e/iterations/` contains `iter-01.html`, `iter-02.html`, `iter-01-bloomberg.html`, `iter-02-bloomberg.html`. |

**Score: 6 PASS, 1 PARTIAL, 2 FAIL, 1 NOT TESTED.** This is pre-0.1 territory, consistent with the new `CLAUDE-PIP.md` rule.

---

## Bugs found + fixed during the run

### 1. `mechanical-checks.js` — `n.className.split is not a function` on SVG elements

**Symptom:** First call to `runInBrowser('contrast_failure', 'desktop')` threw immediately. The check selector matched SVG `circle` / `rect`, whose `className` is an `SVGAnimatedString`, not a string.

**Root cause:** Four CHECKS adapters used `n.className.split(' ')[0]` to derive a selector hint. The unit test suite operates on plain-object inputs (the pure check functions), so the SVG-element branch was never exercised in tests.

**Fix:** Added a `selectorHint(n)` helper that handles both string and `SVGAnimatedString` cases; replaced all 4 occurrences. Source file: `skills/component-composer/scripts/mechanical-checks.js`.

**Coverage gap:** No unit test covers SVG element class-name extraction. Follow-up: add a test that constructs a mock with `className.baseVal`.

### 2. `mechanical-checks.js` — `hidden_mark` false-positives on horizontal/vertical SVG lines

**Symptom:** Validator reported 17 line elements with `height=0` as hidden marks. These were horizontal `<line>` elements (x1≠x2, y1=y2), whose bounding-box height is always 0 by SVG geometry.

**Root cause:** Check required `width ≥ 2 AND height ≥ 2`. Lines are 1D — one dimension is always 0.

**Fix:** 1D special case — if exactly one of `width`/`height` is 0, treat as a line and require `max(width, height) ≥ 4`. Otherwise apply the 2D rule. Source file: same.

**Coverage gap:** Same as #1 — no DOM-level unit test exists; the pure check function tests use synthetic inputs that don't represent SVG line geometry. Follow-up: add a unit test for 1D marks.

### 3. `mechanical-checks.js` — `text_truncation` misses SVG `<text>` overflow

**Symptom:** iter-02 visually showed `informationlog.github.io` clipped to `ionlog.github.io` (24 chars extending past the SVG viewBox left edge) and `22d` clipped to `22c` (extending past right edge). Mechanical `text_truncation` returned PASS at all viewports.

**Root cause:** The check selector is `td, th, .label, .annotation` — HTML elements only. SVG `<text>` overflow against the viewBox is not measured.

**Status:** Logged, not fixed during E2E. Fixing requires a separate SVG-text-overflow check that compares each text bbox against the parent SVG `getBBox()` or viewBox bounds. Follow-up.

---

## Missing rule, added during the run

**`orphan_widow` typographic discipline.** The iter-02 lede stranded "Pulled 2026-05-23." on a final line shorter than 25% of the block measure. Added in three places:

- `skills/component-composer/references/output-style.md` § "Typographic discipline" — drafter-level baseline rule with `text-wrap: balance` guidance.
- `skills/infolog-io/references/criteria.md` § `orphan_widow` — LLM-judge criterion for this theme.
- `skills/infolog-terminal/references/criteria.md` § `orphan_widow` — same for the sibling theme.

Both finals applied `text-wrap: balance` on `h1`, `h2`, `.lede`, `.annotation`, `footer` and the orphan disappeared.

---

## Iteration history

### infolog-io: 2 iterations (mechanical-converged, LLM-judge unresolved)

| Iter | Mechanical failures | LLM-judge failures | Verdict |
|---|---|---|---|
| iter-01 | desktop/tablet: `text_collision`. mobile: `text_collision`, `font_size_too_small`, `hidden_mark` | not run (skipped during validator-bug fix pass) | Discarded — bugs in validator were the priority |
| iter-02 | none at any viewport | `comparison_failure` on activity-windows (long row labels + value labels clipped at viewBox edges) | Mechanical pass; subjective fail logged. Accepted as the E2E final with caveat. |

### infolog-infolog-terminal: 2 iterations (full convergence)

| Iter | Mechanical failures | LLM-judge failures | Verdict |
|---|---|---|---|
| iter-01-bloomberg | mobile: `overflow` (activity table 497px wide on 375 viewport) | not run | Fixed via mobile media query |
| iter-02-bloomberg | none at any viewport | none on 5 subjective criteria including new `orphan_widow` | Final |

### Stuck-detection behavior

Not exercised. Neither theme triggered the same-failure-set-twice path. The composer's `AskUserQuestion` prompt for stuck state was not invoked.

---

## Architectural tensions surfaced (block v0.1)

### A. SVG viewBox scaling vs. mobile font readability vs. label fit

The dominant friction in the infolog-io cycle. The constraint chain:

- SVG with `viewBox="0 0 W H"` + `width: 100%` scales by `actualPx / W`.
- SVG `<text>` font-size is interpreted in user units of the viewBox, so the on-screen text size scales identically with the SVG.
- For a 720-wide viewBox in a 343-wide mobile container, 12.48px text renders at 5.94px — fails the 10px floor.
- Solving by reducing viewBox to 400 fixes mobile font but shrinks horizontal label space — long row labels like `informationlog.github.io` (24 chars at 14 user units = 168 user units) overflow the viewBox.

The pragmatic fixes (HTML+SVG hybrid layouts where labels are HTML and only geometry is SVG; per-viewport viewBox swaps; absolute fixed-px SVG with horizontal scroll wrapper) all require structural changes beyond what the drafter protocol currently codifies. **This is the single biggest architectural item to resolve before v0.1.**

### B. Shorthand CSS properties may hide token violations from `token_compliance`

`padding: var(--space-12) var(--space-4)` — when the browser computes longhand `padding-top: 48px` etc., the literal `48px` shows up in `rule.style[i]` iteration if the engine drops the shorthand. Behavior varies by browser. The current check is not deterministic across engines. Either iterate the shorthand alone, or normalize before the literal check.

### C. The "loop" today is a Claude session manually running the steps

The composer SKILL.md describes the loop as if a runtime executes it. In practice, the loop is a Claude conversation reading the protocol files and acting them out — which means cost tracking (criterion 5) has no scaffolding to write into and the audit summary has nobody to emit it. Either (a) accept that the composer IS a Claude session and add explicit instructions for the model to emit the audit summary at the end, or (b) build a tiny Node runtime that loops the drafter + validator. (a) is the cheap path; (b) is more honest.

---

## Gaps (no defect, just missing scaffolding)

- **No audit-summary emitter.** Protocol describes the shape (`loop-protocol.md`) but no code writes it. Add a final-step note to `SKILL.md` directing the model to emit the audit summary block to chat + as `<session-dir>/audit.md`.
- **No PNG saved to disk.** `preview_screenshot` returns a JPEG into the conversation, not bytes-to-file. Either (a) document that the screenshot is the user-visible PNG (it is), (b) add a tiny Bash export step using Chrome headless / Playwright, or (c) remove the criterion.
- **No PDF emission.** `printToPDF` via CDP is gated by what Claude Preview exposes; not attempted. Same options as PNG.
- **Theme-discovery scan not exercised.** I read theme refs by direct path rather than scanning for `themespec.json`. The scan code path exists in the protocol but has no test.

---

## Recommended v0.1 punch list

In order:

1. Add the three follow-up unit tests for the validator (SVG className, 1D line, SVG text-overflow stub).
2. Build the SVG-text-overflow mechanical check (closes finding #3 above).
3. Resolve architectural tension A — pick the HTML+SVG hybrid layout strategy and document it in `output-style.md` (probably the simplest path).
4. Add a "emit audit summary" terminal step to `component-composer/SKILL.md`; emit shape per protocol.
5. Replace the misnamed `v1.0.0` tag (delete it; do not retag yet — wait for the punch list to clear).
6. Either ship PNG/PDF for real or remove from success criteria.
7. Run a fresh-session E2E (no preloaded context) and see whether the protocol files alone produce a clean run.

---

## What we learned

The generator-critic loop pattern works for HTML artifacts. The mechanical validator catches structural defects that LLM-judge cannot reliably catch (token discipline, geometry, contrast math). The LLM-judge catches semantic defects the mechanical layer cannot reach (label clipping in SVG, subjective hierarchy, range-frame appropriateness). Together they cover meaningfully more than either alone.

The brittle parts: anywhere the protocol assumed runtime support that doesn't exist (PNG/PDF emit, cost tracking, automatic loop continuation). These need either real plumbing or honest scope removal.

The hidden cost: a v0.0.x mechanical-checks implementation that passed 31/31 unit tests still had two production-blocking bugs because the unit tests exercised pure-function inputs, not browser DOM. **Unit-test coverage of DOM adapters needs a separate strategy — JSDOM, integration tests in a headless browser, or fixture-driven preview_eval runs.**

The pleasant surprise: infolog-terminal converged cleanly in two iterations because table-based density sidesteps the SVG scaling problem entirely. The theme's "tables-first" pattern is genuinely the right call for terminal-density aesthetics.
