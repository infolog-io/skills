# Chart Field Guide Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a "chart field guide" to §08 of the infolog.lib reference page — 11 chart types (13 figures) in 5 job families plus a catch-all, each rendered in the house inline-SVG style, with 5 figures honesty-tagged as illustrative.

**Architecture:** All work is in one file, `docs/superpowers/reference/infolog-lib-design-system.html` — three regions: the `<style>` block (new `.fg-*` classes), the `<section id="dataviz">` content (the field-guide block, appended after the Color chapter's last figure), and the JS `VIZ` array (one new feedback entry). Charts are hand-authored static SVG converged in the browser — there is no build step and no test runner.

**Tech Stack:** Static HTML + inline SVG + CSS custom properties. Preview via agent-browser over `file://` (PIP e3c9a7d4 — never localhost). No JS framework, no charting library, no runtime data.

---

## Critical context for the implementer

You have zero context, so read this first.

**The page.** `docs/superpowers/reference/infolog-lib-design-system.html` (~1675 lines) is a self-contained design-system reference. §08 "Charts" is a *doctrine*: a section (`<section id="dataviz">`) whose single `<div class="grid">` holds a header, six `viz-chapter` blocks (Goal, Marks, Axes, Descriptions, Accessibility, Color — ids `dv-goal`/`dv-marks`/`dv-axes`/`dv-desc`/`dv-a11y`/`dv-color`), and example-chart `<figure>` elements interleaved as direct grid children.

**Mirror after every edit.** The canonical is the reference file above. After *every* edit, copy it to both working mirrors or the feedback compiler breaks:
```bash
cp docs/superpowers/reference/infolog-lib-design-system.html /tmp/dslib.html
cp docs/superpowers/reference/infolog-lib-design-system.html /tmp/composer-e2e/spraypixel-state.html
```

**Preview recipe (no localhost).**
```bash
agent-browser open "file:///Users/informationlogistics/Developer/infolog-skills/docs/superpowers/reference/infolog-lib-design-system.html"
agent-browser eval "document.documentElement.setAttribute('data-theme','dark')"   # dark
agent-browser eval "document.documentElement.removeAttribute('data-theme')"        # back to light
agent-browser scrollintoview "#dv-guide"
agent-browser screenshot /tmp/fg-check.png
agent-browser console     # empty output = clean
```

**The feedback-injection boundary trap (important).** The per-section JS walks siblings from each `viz-chapter` until the next element with class `viz-chapter`, then inserts that chapter's feedback panel. `dv-color` is currently the last chapter, so it absorbs every following figure to the end of the grid. **The field-guide opener MUST carry `class="viz-chapter"`** so it acts as the boundary that stops `dv-color`'s walk; otherwise the Color panel jumps to the end of the entire guide. The opener also gets `id="dv-guide"` so its own panel injects after the guide's last figure. Family sub-headers must NOT be `viz-chapter` (they would create stray panels).

**House-style SVG conventions** (copy these exactly — pattern is the bar chart at lines ~826–861 and dot plot ~865–905):
- `<figure class="span-full lg-span-N" style="margin: 0;">` (N = 4 or 6).
- `<figcaption class="meta" style="margin-bottom: var(--space-3);">Short label</figcaption>` for the label; `<p class="viz-headline">Takeaway sentence.</p>` for the insight headline (place headline above the figcaption/SVG).
- `<svg viewBox="0 0 W H" role="img" aria-label="..." style="width:100%; height:auto; font-family: var(--sans);">`.
- Baseline/axis lines: `stroke="var(--gray-500)"`. Gridlines / dotted references: `stroke="var(--gray-300)" stroke-dasharray="1 4"`.
- Axis + value labels: `style="fill: var(--ink-soft); font-family: var(--mono); font-size: 10-11px;"`. Highlighted value: `fill: var(--success)` + `font-weight: 600`.
- Data marks: quiet `var(--gray-700)` by default; `var(--success)` up/positive/kept, `var(--danger)` down/negative, `var(--info)` for a non-directional reference/baseline. No yellow (R04).
- Two-shade or translucent fills: `fill="color-mix(in srgb, var(--info), white 82%)"` — **never** `fill-opacity` (it inverts lighter/darker on dark backgrounds).
- Leave an HTML comment documenting the data and the coordinate math, exactly like the existing charts (e.g. `<!-- height = (value/max)*h; y = base - height -->`).

**How charts get built.** Author the SVG from the data + coordinate formula in each task, render via the preview recipe, eyeball against light + dark, nudge coordinates, re-render. This convergence loop is the method — it is not a placeholder. Task 2 ships one fully-worked SVG (the funnel) as the canonical pattern; later tasks give exact data + dimensions + colors + text and you author to the same pattern.

**Domain rule (from the spec).** Every example is AI/ML, finance, or time-series/ops — never abstract. Subjects are fixed per figure below; do not invent others.

---

## Task 1: Scaffold — field-guide block, CSS, feedback wiring

**Files:**
- Modify: `docs/superpowers/reference/infolog-lib-design-system.html` (CSS block ~line 326; dataviz content ~line 1184; `VIZ` array ~line 1491)

- [ ] **Step 1: Add the `.fg-*` CSS.** Insert after the `.viz-a11y-readout` rule (the line ending the `/* A — keyboard-navigable exemplar */` group, ~line 326), before `/* --- Form controls`:

```css
  /* --- Field guide: applied chart vocabulary, by job ------------------ */
  .fg-family { grid-column: 1 / -1; margin-top: var(--space-6); display: flex; align-items: baseline; gap: var(--space-3); flex-wrap: wrap; }
  .fg-family:first-of-type { margin-top: var(--space-2); }
  .fg-family-name { font-family: var(--sans); font-size: var(--font-size-h5); font-weight: var(--weight-semibold); color: var(--ink); }
  .fg-q { font-family: var(--mono); font-size: 0.78rem; color: var(--ink-soft); }
  .fg-use { font-size: var(--font-size-caption); color: var(--ink-soft); margin: var(--space-2) 0 0; line-height: var(--leading-snug); }
  .fg-tag { display: inline-block; font-family: var(--mono); font-size: 0.62rem; text-transform: uppercase; letter-spacing: var(--tracking-wide); color: var(--ink-soft); border: 1px solid var(--gray-300); border-radius: 3px; padding: 1px 6px; margin-left: var(--space-2); vertical-align: middle; }
```

- [ ] **Step 2: Add the field-guide opener block.** Insert immediately AFTER the sparkline-row `</div>` (~line 1184) and BEFORE the grid's closing `</div>` (~line 1185):

```html
    <!-- ===== FIELD GUIDE — applied chart vocabulary, by job ===== -->
    <!-- viz-chapter class is load-bearing: it stops dv-color's feedback-injection walk. -->
    <div class="viz-chapter" id="dv-guide">
      <div class="viz-chapter-head">
        <span class="viz-chapter-name">A field guide to chart types</span>
      </div>
      <p class="viz-chapter-lede">The six decisions, applied. Each chart below answers one question, drawn in the house style. Charts we can render honestly are real; charts that need data or compute we cannot reproduce here carry an <em>illustrative</em> tag — the honest-data-viz rule applied to its own limits.</p>
    </div>
```

- [ ] **Step 3: Wire the feedback panel.** In the `VIZ` array (~line 1491), add the `dv-guide` entry as the last item:

```js
    const VIZ = [
      { id: 'dv-goal',  label: '08 · Goal' },
      { id: 'dv-marks', label: '08 · Marks' },
      { id: 'dv-axes',  label: '08 · Axes' },
      { id: 'dv-desc',  label: '08 · Descriptions' },
      { id: 'dv-a11y',  label: '08 · Accessibility' },
      { id: 'dv-color', label: '08 · Color' },
      { id: 'dv-guide', label: '08 · Field guide' },
    ];
```

- [ ] **Step 4: Mirror to both working copies.**

```bash
cp docs/superpowers/reference/infolog-lib-design-system.html /tmp/dslib.html
cp docs/superpowers/reference/infolog-lib-design-system.html /tmp/composer-e2e/spraypixel-state.html
```

- [ ] **Step 5: Verify render + injection boundary.**

```bash
agent-browser open "file:///Users/informationlogistics/Developer/infolog-skills/docs/superpowers/reference/infolog-lib-design-system.html"
agent-browser eval "(() => { const g=document.getElementById('dv-guide'); const guidePanel=document.getElementById('fb-dv-guide'); const colorPanel=document.getElementById('fb-dv-color'); const colorBeforeGuide = colorPanel && (colorPanel.compareDocumentPosition(g) & Node.DOCUMENT_POSITION_FOLLOWING); return JSON.stringify({ guideExists: !!g, guidePanelExists: !!guidePanel, colorPanelExists: !!colorPanel, colorPanelBeforeGuideOpener: !!colorBeforeGuide }); })()"
agent-browser console
```
Expected: `guideExists:true, guidePanelExists:true, colorPanelExists:true, colorPanelBeforeGuideOpener:true`. Console empty. (`colorPanelBeforeGuideOpener:true` confirms the Color panel did NOT jump past the guide.)

- [ ] **Step 6: Verify feedback data path.**

```bash
agent-browser eval "(() => { const t=document.getElementById('fb-dv-guide'); t.value='tighten the funnel drop labels'; t.dispatchEvent(new Event('input',{bubbles:true})); return 'typed'; })()"
agent-browser eval "(() => { const out=document.getElementById('compiled-out').textContent; return JSON.stringify({ hasHeader: out.includes('## 08 · Field guide'), counter: document.getElementById('fb-counter').textContent }); })()"
agent-browser eval "(() => { const t=document.getElementById('fb-dv-guide'); t.value=''; t.dispatchEvent(new Event('input',{bubbles:true})); return 'cleared'; })()"
```
Expected: `hasHeader:true`, counter `1 section with feedback`, then cleared.

- [ ] **Step 7: Verify dark.**

```bash
agent-browser eval "document.documentElement.setAttribute('data-theme','dark')"
agent-browser scrollintoview "#dv-guide"
agent-browser screenshot /tmp/fg-task1-dark.png
agent-browser console
agent-browser eval "document.documentElement.removeAttribute('data-theme')"
```
Expected: opener + lede legible in dark, console clean.

- [ ] **Step 8: Commit.**

```bash
git add docs/superpowers/reference/infolog-lib-design-system.html
git commit -m "feat(design-system): scaffold §08 chart field guide + dv-guide feedback panel"
```

---

## Task 2: Flow / stages — funnel ×2 + waterfall

**Files:**
- Modify: `docs/superpowers/reference/infolog-lib-design-system.html` (insert after the `dv-guide` opener block from Task 1)

Family sub-header + three figures. This task ships the **canonical funnel SVG in full**; author the sales funnel and waterfall to the same pattern from the data + formulas given.

- [ ] **Step 1: Add the family sub-header + the agent-run funnel (full SVG).** Insert after the `dv-guide` `</div>`:

```html
    <div class="fg-family"><span class="fg-family-name">Flow / stages</span><span class="fg-q">— where does volume drop through a sequence?</span></div>

    <!-- FUNNEL · agent run. Left-aligned bars; width = (value/1000)*180, x from 120. Verified = kept = success. -->
    <figure class="span-full lg-span-6" style="margin: 0;">
      <p class="viz-headline">Three in five dispatched runs verify clean.</p>
      <figcaption class="meta" style="margin-bottom: var(--space-3);">Agent run funnel · last 7 days</figcaption>
      <svg viewBox="0 0 320 220" role="img" aria-label="Agent run funnel: dispatched 1000, tool-call 840, response 720, verified 610." style="width:100%; height:auto; font-family: var(--sans);">
        <!-- rows y: 40, 84, 128, 172; bar height 26; widths 180,151,130,110 -->
        <text x="112" y="57"  text-anchor="end" style="fill: var(--ink); font-family: var(--sans); font-size: 11px;">Dispatched</text>
        <rect x="120" y="40"  width="180" height="26" fill="var(--gray-700)"/>
        <text x="308" y="57"  text-anchor="start" style="fill: var(--ink); font-family: var(--mono); font-size: 11px;">1000</text>

        <text x="112" y="101" text-anchor="end" style="fill: var(--ink); font-family: var(--sans); font-size: 11px;">Tool-call</text>
        <rect x="120" y="84"  width="151" height="26" fill="var(--gray-700)"/>
        <text x="279" y="101" text-anchor="start" style="fill: var(--ink); font-family: var(--mono); font-size: 11px;">840</text>
        <text x="120" y="80"  style="fill: var(--ink-soft); font-family: var(--mono); font-size: 9px;">−16%</text>

        <text x="112" y="145" text-anchor="end" style="fill: var(--ink); font-family: var(--sans); font-size: 11px;">Response</text>
        <rect x="120" y="128" width="130" height="26" fill="var(--gray-700)"/>
        <text x="258" y="145" text-anchor="start" style="fill: var(--ink); font-family: var(--mono); font-size: 11px;">720</text>
        <text x="120" y="124" style="fill: var(--ink-soft); font-family: var(--mono); font-size: 9px;">−14%</text>

        <text x="112" y="189" text-anchor="end" style="fill: var(--ink); font-family: var(--sans); font-size: 11px;">Verified</text>
        <rect x="120" y="172" width="110" height="26" fill="var(--success)"/>
        <text x="238" y="189" text-anchor="start" style="fill: var(--success); font-family: var(--mono); font-size: 11px; font-weight: 600;">610</text>
        <text x="120" y="168" style="fill: var(--ink-soft); font-family: var(--mono); font-size: 9px;">−15%</text>
      </svg>
      <p class="fg-use">Use when: sequential stages with monotonic drop-off.</p>
    </figure>
```

- [ ] **Step 2: Add the sales-pipeline funnel.** Same pattern, same viewBox `0 0 320 220`, same row geometry. Data — widths = `(value/480)*180`:

  - Leads 480 → w=180 (y=40); Qualified 300 → w=113 (y=84, −38%); Demo 175 → w=66 (y=128, −42%); Proposal 95 → w=36 (y=172... use 4 rows? this is 5 stages).

  5 stages need 5 rows. Use viewBox `0 0 320 250`, rows y = 36, 76, 116, 156, 196; bar height 24; widths = `(value/480)*180`:
  - Leads 480 → w=180; Qualified 300 → w=113 (−38%); Demo 175 → w=66 (−42%); Proposal 95 → w=36 (−46%); Won 41 → w=15 (−57%).
  - Labels left at x=112 (anchor end): Leads, Qualified, Demo, Proposal, Won. Bars from x=120. Value at `x=120+w+8`. `Won` bar fill `var(--success)`, value `var(--success)` bold; others `var(--gray-700)`.
  - `<p class="viz-headline">Roughly one in twelve leads closes.</p>`; `<figcaption class="meta">Sales pipeline · this quarter</figcaption>`; `aria-label="Sales pipeline funnel: leads 480, qualified 300, demo 175, proposal 95, won 41."`
  - `<figure class="span-full lg-span-6" ...>`; `<p class="fg-use">Use when: a sales/ops pipeline with named stages (states).</p>`

- [ ] **Step 3: Add the ARR waterfall.** viewBox `0 0 420 240`. Floating bars; up=green, down=red, totals=gray; thin dashed connectors between bar tops. Data ($M), y-scale 0→6M over pixel 200(bottom)→30(top), so `y(v) = 200 - (v/6)*170`:
  - Opening 4.20 (full bar 0→4.20, gray) at x=40 w=50.
  - +New 0.90 (floats 4.20→5.10, green) at x=110.
  - +Expansion 0.55 (floats 5.10→5.65, green) at x=180.
  - −Churn 0.40 (floats 5.65→5.25, red) at x=250.
  - Closing 5.25 (full bar 0→5.25, gray) at x=320 w=50.
  - Each bar w=50. Connector: dashed `var(--gray-300)` from prev bar top-right to next bar top-left. Value labels above each delta bar (`+0.90`, `+0.55`, `−0.40` in their bar color; totals `4.20`/`5.25` in ink). x-labels under: Opening, New, Expansion, Churn, Closing (mono 9px ink-soft).
  - `<p class="viz-headline">Expansion and new logos cover churn — ARR up 25%.</p>`; `<figcaption class="meta">ARR bridge · FY opening → closing ($M)</figcaption>`; `aria-label="ARR waterfall: opening 4.20M, plus new 0.90, plus expansion 0.55, minus churn 0.40, closing 5.25M."`
  - `<figure class="span-full lg-span-6" ...>`; `<p class="fg-use">Use when: a running total built from signed components.</p>`

- [ ] **Step 4: Mirror + verify (light & dark).**

```bash
cp docs/superpowers/reference/infolog-lib-design-system.html /tmp/dslib.html && cp docs/superpowers/reference/infolog-lib-design-system.html /tmp/composer-e2e/spraypixel-state.html
agent-browser open "file:///Users/informationlogistics/Developer/infolog-skills/docs/superpowers/reference/infolog-lib-design-system.html"
agent-browser scrollintoview "#dv-guide"
agent-browser screenshot /tmp/fg-flow-light.png
agent-browser eval "document.documentElement.setAttribute('data-theme','dark')"; agent-browser screenshot /tmp/fg-flow-dark.png
agent-browser console
agent-browser eval "document.documentElement.removeAttribute('data-theme')"
```
Expected: three figures render; funnel bars decrease, Verified/Won green; waterfall up-bars green, churn red, connectors align bar tops; legible both themes; console clean.

- [ ] **Step 5: Commit.**

```bash
git add docs/superpowers/reference/infolog-lib-design-system.html
git commit -m "feat(design-system): field guide — flow family (funnel x2, ARR waterfall)"
```

---

## Task 3: Continuous XY — line, line + scatter, continuous error bars

**Files:**
- Modify: `docs/superpowers/reference/infolog-lib-design-system.html` (insert after Task 2's waterfall figure)

All three viewBox `0 0 420 220`, plot area x∈[40,400], y∈[30,190] (baseline at y=190). Sparse grid: 4 horizontal lines `var(--gray-300)`.

- [ ] **Step 1: Family sub-header.**

```html
    <div class="fg-family"><span class="fg-family-name">Continuous XY</span><span class="fg-q">— how does Y move over X, with what certainty?</span></div>
```

- [ ] **Step 2: Line — p95 latency.** 30 days on x (x = `40 + (day/29)*360`), p95 ms on y, scale 0→400ms (`y = 190 - (ms/400)*160`). Series mostly ~210–230ms, a spike to 340 at day 18 then recovery to ~205. Line `stroke="var(--gray-700)"` `stroke-width="1.5"` `fill="none"` (neutral metric); the breach segment (days 16–20, above SLO) overdrawn `stroke="var(--danger)"`. SLO reference line at 250ms: `<line ... stroke="var(--info)" stroke-dasharray="1 4"/>` + label `SLO 250`. y ticks 0/200/400; x ticks day 1/15/30.
  - `<p class="viz-headline">p95 held under SLO except the day-18 incident.</p>`; `<figcaption class="meta">Response latency p95 · 30 days (ms)</figcaption>`; `aria-label="p95 response latency over 30 days; a spike to 340ms on day 18 breaches the 250ms SLO."` `lg-span-6`. `fg-use`: "Use when: one metric over a continuous time axis."

- [ ] **Step 3: Line + scatter — throughput vs concurrency.** x = concurrency 1..64 (`x = 40 + (c/64)*360`), y = throughput req/s 0..500 (`y = 190 - (t/500)*160`). ~12 scatter points rising then plateauing (e.g. c=2→90, 4→170, 8→300, 16→410, 24→455, 32→475, 40→478, 48→472, 56→470, 64→468) with small jitter; dots `r="3" fill="var(--gray-700)"`. Fitted trend: a smooth `<path>` (rising then flat) `stroke="var(--success)"` `stroke-width="1.5" fill="none"` (more throughput = good).
  - `<p class="viz-headline">Throughput plateaus past ~32 concurrent.</p>`; `<figcaption class="meta">Throughput vs. concurrency · samples + fit</figcaption>`; `aria-label="Throughput rises with concurrency then plateaus around 475 req/s past 32 concurrent."` `lg-span-6`. `fg-use`: "Use when: observed samples plus a fitted relationship."

- [ ] **Step 4: Continuous error bars — forecast queue depth.** x = 30 points (20 actual + 10 forecast). Actual line solid `var(--gray-700)`; forecast line dashed `var(--gray-700) stroke-dasharray="4 3"`. ± band over the forecast region only: a `<path>` polygon filled `fill="color-mix(in srgb, var(--info), white 82%)"` (NOT fill-opacity), widening with horizon. A thin vertical `var(--gray-300)` divider at the now-line + label "forecast →".
  - `<p class="viz-headline">Queue depth forecast holds, with widening uncertainty.</p>`; `<figcaption class="meta">Queue depth · actual + 10-step forecast (± 90%)</figcaption>`; `aria-label="Queue depth: 20 actual points then a 10-step forecast with a widening 90 percent confidence band."` `lg-span-6`. `fg-use`: "Use when: a projection carrying its confidence interval."

- [ ] **Step 5: Mirror + verify (light & dark).** Same recipe as Task 2 Step 4; screenshots `/tmp/fg-xy-light.png`, `/tmp/fg-xy-dark.png`. Expected: band stays lighter than its line in BOTH themes (proves color-mix, not opacity); breach segment red; console clean.

- [ ] **Step 6: Commit.**

```bash
git add docs/superpowers/reference/infolog-lib-design-system.html
git commit -m "feat(design-system): field guide — continuous XY (line, scatter+fit, error band)"
```

---

## Task 4: Model fit & eval — regression, ROC + PR, kNN

**Files:**
- Modify: `docs/superpowers/reference/infolog-lib-design-system.html` (insert after Task 3's error-band figure)

- [ ] **Step 1: Family sub-header.**

```html
    <div class="fg-family"><span class="fg-family-name">Model fit &amp; evaluation</span><span class="fg-q">— does the model fit or classify well?</span></div>
```

- [ ] **Step 2: ML regression — predicted vs. actual.** Square viewBox `0 0 300 300`, plot x∈[45,280] y∈[20,255]. ~25 points scattered tightly around the y=x diagonal (actual on x, predicted on y, both 0–60 min). Diagonal identity line `stroke="var(--info)" stroke-dasharray="1 4"` corner-to-corner of the plot box. Points `r="3" fill="var(--gray-700)"`. Axis labels "actual (min)" / "predicted (min)". R² annotation top-left: `R² 0.89` (mono, ink). NOT illustrative-tagged (representative data, like the existing bar chart).
  - `<p class="viz-headline">Predicted vs. actual completion time — R² 0.89.</p>`; `<figcaption class="meta">Completion-time model · held-out set</figcaption>`; `aria-label="Predicted versus actual completion time; points cluster along the identity line, R-squared 0.89."` `lg-span-4`. `fg-use`: "Use when: model output against ground truth."

- [ ] **Step 3: ROC + PR — abuse classifier.** One figure, two side-by-side mini-plots in viewBox `0 0 420 220`. Left panel (x∈[40,200], unit square): ROC — diagonal baseline `var(--info) stroke-dasharray="1 4"`, ROC curve bowing to top-left `stroke="var(--success)" stroke-width="1.5" fill="none"`, label "ROC · AUC 0.94". Right panel (x∈[250,410]): PR — horizontal baseline at prevalence (~0.12) `var(--info) dashed`, PR curve high then dropping `var(--success)`, label "PR · AP 0.71". Axis labels FPR/TPR and Recall/Precision (mono 9px).
  - `<p class="viz-headline">Abuse classifier — AUC 0.94, precision holds to ~0.8 recall.</p>`; `<figcaption class="meta">Abuse classifier · threshold sweep</figcaption>`; `aria-label="ROC curve with AUC 0.94 and precision-recall curve with average precision 0.71 for the abuse classifier."` `lg-span-6`. `fg-use`: "Use when: classifier quality across every threshold."

- [ ] **Step 4: kNN classification — decision regions (ILLUSTRATIVE).** Square viewBox `0 0 300 300`, plot box [20,280]². Three soft class regions as large rounded `<rect>`/`<path>` shapes filled with `color-mix(in srgb, var(--success), white 84%)`, `color-mix(in srgb, var(--info), white 84%)`, `color-mix(in srgb, var(--danger), white 84%)` (low-chroma so points read on top). ~30 points `r="3"` colored by class (`var(--success)`/`var(--info)`/`var(--danger)`), with 3–4 points sitting in the "wrong" region near the blurred boundary. Axis labels "embed dim 1 / 2".
  - `<p class="viz-headline">Three intent classes (k=15) — boundaries blur where embeddings overlap.</p>`; `<figcaption class="meta">Intent classifier · 2-feature view <span class="fg-tag">illustrative</span></figcaption>`; `aria-label="Illustrative kNN decision regions for three intent classes in a two-feature embedding space; not a computed analysis."` `lg-span-4`. `fg-use`: "Use when: how a classifier partitions a 2-feature space."

- [ ] **Step 5: Mirror + verify (light & dark).** Recipe as before; `/tmp/fg-model-light.png` / `-dark.png`. Expected: regression points hug the diagonal; ROC bows up-left, PR starts high; kNN regions stay pale under points in BOTH themes; the `illustrative` tag is visible on kNN only; console clean.

- [ ] **Step 6: Commit.**

```bash
git add docs/superpowers/reference/infolog-lib-design-system.html
git commit -m "feat(design-system): field guide — model fit & eval (regression, ROC/PR, kNN)"
```

---

## Task 5: High-D projection + Relational — PCA, UMAP, network

**Files:**
- Modify: `docs/superpowers/reference/infolog-lib-design-system.html` (insert after Task 4's kNN figure)

All three are ILLUSTRATIVE (hand-placed; tag required).

- [ ] **Step 1: Family sub-headers (two families).**

```html
    <div class="fg-family"><span class="fg-family-name">High-dimensional projection</span><span class="fg-q">— what structure hides in many dimensions?</span></div>
```
(Add the Relational sub-header in Step 4, before the network figure.)

- [ ] **Step 2: PCA — PC1 vs PC2 (ILLUSTRATIVE).** viewBox `0 0 320 300`, plot [40,300]×[20,250]. Scatter of ~40 points in 3 loose clusters colored `var(--success)`/`var(--info)`/`var(--gray-700)` (domains). Light origin axes `var(--gray-300)`. Optional: two short loading arrows from centre (`<line>` + small arrowhead) labelled e.g. "latency", "cost". Axis labels "PC1 (42% var)" / "PC2 (19% var)".
  - `<p class="viz-headline">Two components capture 61% of embedding variance.</p>`; `<figcaption class="meta">Skill-embedding PCA <span class="fg-tag">illustrative</span></figcaption>`; `aria-label="Illustrative PCA scatter of skill embeddings; PC1 42 percent and PC2 19 percent of variance; not computed."` `lg-span-4`. `fg-use`: "Use when: dominant axes of variation in high-D data."

- [ ] **Step 3: UMAP — skill-embedding clusters (ILLUSTRATIVE).** viewBox `0 0 320 300`. 4–5 well-separated blobs (~12 points each), each blob one color (`--success`/`--info`/`--danger`/`--gray-700` + one `color-mix` lighter). NO meaningful axes — faint box only, axis labels "UMAP-1 / UMAP-2" with a foot-note that axes are not interpretable.
  - `<p class="viz-headline">Skill embeddings cluster by domain under UMAP.</p>`; `<figcaption class="meta">Skill embeddings · UMAP <span class="fg-tag">illustrative</span></figcaption>`; `aria-label="Illustrative UMAP projection of skill embeddings into domain clusters; axes are not interpretable and the projection is stochastic."` `lg-span-4`. `fg-use`: "Use when: exploratory cluster structure (axes not interpretable; stochastic)."

- [ ] **Step 4: Relational sub-header + network graph (ILLUSTRATIVE).**

```html
    <div class="fg-family"><span class="fg-family-name">Relational</span><span class="fg-q">— what connects to what?</span></div>
```
  Network: viewBox `0 0 360 300`. ~10 hand-placed nodes — 3 plugin hubs (larger `r="9" fill="var(--info)"`) and 7 skill nodes (`r="5" fill="var(--gray-700)"`); edges `stroke="var(--gray-300)" stroke-width="1"` drawn BEFORE nodes (so nodes sit on top). One or two skills shared between plugins (hub). Tiny mono labels on the hubs.
  - `<p class="viz-headline">Plugins fan out to skills; a few skills are shared hubs.</p>`; `<figcaption class="meta">Plugin → skill dependency graph <span class="fg-tag">illustrative</span></figcaption>`; `aria-label="Illustrative node-link graph of plugins pointing to skills, with a few shared skill hubs; hand-placed, not computed."` `lg-span-6`. `fg-use`: "Use when: relationships and topology, not magnitudes."

- [ ] **Step 5: Mirror + verify (light & dark).** Recipe as before; `/tmp/fg-projn-light.png` / `-dark.png`. Expected: PCA/UMAP clusters separate clearly; network edges sit under nodes; all three show the `illustrative` tag; console clean both themes.

- [ ] **Step 6: Commit.**

```bash
git add docs/superpowers/reference/infolog-lib-design-system.html
git commit -m "feat(design-system): field guide — projections (PCA, UMAP) + network graph"
```

---

## Task 6: Catch-all — correlation heatmap + methodology

**Files:**
- Modify: `docs/superpowers/reference/infolog-lib-design-system.html` (insert after Task 5's network figure)

- [ ] **Step 1: Family sub-header + methodology prose.**

```html
    <div class="fg-family"><span class="fg-family-name">Anything else</span><span class="fg-q">— a chart the eleven do not name?</span></div>
    <div class="span-full lg-span-6">
      <p class="fg-use" style="max-width: 60ch;">The guide is not a closed list. Any chart not shown — heatmap, treemap, sankey, choropleth (e.g. sales by state), radar, histogram, area — inherits the same six decisions and the house palette: quiet gray context, green up, red down, blue reference, and an <em>illustrative</em> tag whenever the data is not computed. One representative below.</p>
    </div>
```

- [ ] **Step 2: Correlation heatmap (ILLUSTRATIVE).** viewBox `0 0 320 300`. 6×6 grid of cells (metrics: latency, throughput, error rate, queue, cost, CSAT). Cell fill = diverging by correlation r∈[−1,1]: r>0 → `color-mix(in srgb, var(--success), white (100 − |r|*70)%)`; r<0 → `color-mix(in srgb, var(--danger), white (100 − |r|*70)%)`; diagonal r=1 → full `var(--success)`. Author ~6 distinct r values into the cells (symmetric matrix). Row labels left (mono 9px), column labels rotated or abbreviated on top. Small legend strip (−1 red … 0 white … +1 green).
  - `<p class="viz-headline">Latency and error rate move together; cost trades against CSAT.</p>`; `<figcaption class="meta">Ops metric correlation <span class="fg-tag">illustrative</span></figcaption>`; `aria-label="Illustrative 6 by 6 correlation heatmap of operations metrics; green positive, red negative; not computed."` `lg-span-6`. `fg-use`: "Use when: pairwise relationships across many variables (the long-tail representative)."

- [ ] **Step 3: Mirror + verify (light & dark).** Recipe as before; `/tmp/fg-catchall-light.png` / `-dark.png`. Expected: heatmap diverging scale reads in both themes (white-centre cells stay neutral on dark — verify color-mix with white behaves; if a near-white cell vanishes on dark, add a 1px `var(--gray-300)` cell stroke); `illustrative` tag visible; methodology prose present; console clean.

- [ ] **Step 4: Commit.**

```bash
git add docs/superpowers/reference/infolog-lib-design-system.html
git commit -m "feat(design-system): field guide — catch-all (correlation heatmap + methodology)"
```

---

## Task 7: Final verification sweep

**Files:**
- None modified unless a defect is found (then fix in the owning task's figure, re-mirror, re-verify).

- [ ] **Step 1: Mirror parity.**

```bash
md5 -q docs/superpowers/reference/infolog-lib-design-system.html /tmp/dslib.html /tmp/composer-e2e/spraypixel-state.html
```
Expected: three identical hashes.

- [ ] **Step 2: Figure + tag census.**

```bash
agent-browser open "file:///Users/informationlogistics/Developer/infolog-skills/docs/superpowers/reference/infolog-lib-design-system.html"
agent-browser eval "(() => { const g=document.getElementById('dv-guide'); let n=g, figs=0, tags=0; while((n=n.nextElementSibling)){ if(n.tagName==='FIGURE'){figs++; if(n.querySelector('.fg-tag')) tags++;} } return JSON.stringify({figures: figs, illustrativeTags: tags}); })()"
```
Expected: `figures:13, illustrativeTags:5` (kNN, PCA, UMAP, network, heatmap).

- [ ] **Step 3: Accessibility census.**

```bash
agent-browser eval "(() => { const g=document.getElementById('dv-guide'); let n=g, svgs=0, labelled=0; while((n=n.nextElementSibling)){ const s=n.querySelector&&n.querySelector('svg[role=img]'); if(s){svgs++; if(s.getAttribute('aria-label')) labelled++;} } return JSON.stringify({svgs, labelled}); })()"
```
Expected: `svgs:13, labelled:13` (every chart has an aria-label; the 5 illustrative labels say "illustrative").

- [ ] **Step 4: Feedback end-to-end.**

```bash
agent-browser eval "(() => { const t=document.getElementById('fb-dv-guide'); t.value='ship it'; t.dispatchEvent(new Event('input',{bubbles:true})); const ok=document.getElementById('compiled-out').textContent.includes('## 08 · Field guide'); t.value=''; t.dispatchEvent(new Event('input',{bubbles:true})); return ok; })()"
```
Expected: `true`.

- [ ] **Step 5: Full-guide screenshots, both themes, console clean.**

```bash
agent-browser scrollintoview "#dv-guide"
agent-browser screenshot /tmp/fg-final-light.png
agent-browser eval "document.documentElement.setAttribute('data-theme','dark')"
agent-browser screenshot /tmp/fg-final-dark.png
agent-browser console
agent-browser eval "document.documentElement.removeAttribute('data-theme')"
```
Expected: all 13 figures legible in both themes; no clipped SVGs; console empty.

- [ ] **Step 6: Update the handoff doc** `docs/superpowers/2026-05-31-design-system-session-handoff.md` — note §08 field guide complete (13 figures, 5 illustrative), `dv-guide` panel wired, and that the Layout (A) spec remains queued.

- [ ] **Step 7: Commit.**

```bash
git add docs/superpowers/reference/infolog-lib-design-system.html docs/superpowers/2026-05-31-design-system-session-handoff.md
git commit -m "docs(design-system): field guide verified (13 figures, 5 illustrative); handoff sync"
```

---

## Self-review notes (for the author)

- **Spec coverage:** funnel (×2, incl. sales) ✓ T2; waterfall ✓ T2; line ✓ T3; line+scatter ✓ T3; error bars ✓ T3; regression ✓ T4; ROC/PR ✓ T4; kNN ✓ T4; PCA ✓ T5; t-SNE/UMAP ✓ T5; network ✓ T5; catch-all heatmap + methodology + long-tail list ✓ T6; 5 illustrative tags ✓ (T4 kNN, T5 PCA/UMAP/network, T6 heatmap); `dv-guide` feedback ✓ T1; honesty labels + aria ✓ T7 census; light/dark + console + mirror ✓ each task and T7.
- **Placement:** appended after §08's six dimensions, no renumber — matches spec approach 1.
- **Naming consistency:** id `dv-guide`; classes `.fg-family`/`.fg-family-name`/`.fg-q`/`.fg-use`/`.fg-tag` used identically across all tasks.
- **Known risk:** near-white heatmap / band cells on dark — mitigation noted inline (T6 Step 3: add `var(--gray-300)` cell stroke if a cell vanishes).
- **Coordinate convergence is in-browser** by design — the data + formulas are exact; pixel nudging happens via the preview loop, not blind authoring.
