# Spec — §08 Chart field guide (11 chart types)

Date: 2026-05-31
Branch: `feat/component-composer` (repo: infolog-skills)
Canonical page: `docs/superpowers/reference/infolog-lib-design-system.html`
Status: approved framing, pre-implementation.

## Context

§08 "Charts" is a doctrine, not a catalog. It opens *"An effective chart decides
six things"* and runs six `viz-chapter` blocks — Goal, Marks, Axes, Descriptions,
Accessibility, Color. Each chapter carries lint rules plus one example chart that
illustrates that dimension. The current mark vocabulary: line, bar, dot plot,
cumulative line, candlestick, seven sparkline variants, the a11y bar.

The user wants eleven more chart types represented. The risk: turning a disciplined
doctrine into a Plotly clone gallery. This spec adds the types without breaking the
doctrine.

## Goal

Add a **chart field guide** to §08 that demonstrates 11 chart types in the house
style, organized by the job each chart does, with an explicit honesty split between
charts we render for real and charts we represent illustratively.

Success criteria:
- Field guide appended after the six dimensions; the six chapters stay untouched.
- All 11 types present, each with a domain-themed example (AI/ML, finance, or ops);
  the funnel ships two (agent run + sales pipeline).
- A catch-all sixth group covers the long tail: methodology + one representative.
- 7 named types rendered as real house-style SVGs; the represent charts plus the
  catch-all heatmap carry an "illustrative" tag.
- One feedback panel wired via the data-driven `VIZ` array.
- Verified light + dark, console clean, byte-mirrored to both `/tmp` copies.

## Framing decision (approved)

Organize by **the question each chart answers**, not by chart name. This honors the
Goal dimension (match chart to question). Placement: **append a field guide after
the six dimensions** (approach 1 of 3). Doctrine first, applied vocabulary second.
No renumber, no feedback-array churn beyond one added `VIZ` entry.

The **honesty split** is itself on-doctrine. Charts needing data or compute we cannot
reproduce in a static reference get a visible *illustrative — house treatment, not a
computed analysis* tag. Charts we can render honestly do not.

## The 11 charts

| Family | Type | Question it answers | Domain example | Treatment |
|---|---|---|---|---|
| **Flow / stages** | Funnel | Where does volume drop through a sequence? | Two figures: agent run (dispatched → tool-call → response → verified) + sales pipeline (lead → qualified → demo → proposal → won) | Implement — ordered bars, % drop labels |
| | Waterfall | What moved the total? | ARR bridge: opening + new + expansion − churn = closing | Implement — floating bars, green up / red down, connectors |
| **Continuous XY** | Line | How does Y move over a continuous X? | p95 response latency, 30 days | Implement — path, sparse grid |
| | Line + scatter | Observed points vs. a trend? | Throughput vs. concurrency, samples + fitted trend | Implement — dots + line |
| | Continuous error bars | How does Y move, with what certainty? | Forecast queue depth, ± 90% band | Implement — path + ± area (color-mix, not opacity) |
| **Model fit & eval** | ML regression | Does the model fit? | Predicted vs. actual completion time, fit + R² | Implement — scatter + fit line |
| | ROC & PR curves | How good is the classifier across thresholds? | Abuse classifier: ROC (AUC) + PR at prevalence | Implement — curve + baseline reference |
| | kNN classification | How does the classifier partition space? | Embedding space, 3 intent classes | **Represent** — illustrative decision regions |
| **High-D projection** | PCA | What are the dominant axes of variation? | Embedding variance, PC1 vs PC2 by domain | **Represent** — illustrative scatter (+ optional loading arrows) |
| | t-SNE / UMAP | What cluster structure hides in high-D data? | UMAP of skill embeddings, clusters by domain | **Represent** — illustrative clustered scatter |
| **Relational** | Network graph | What connects to what? | Skill dependency graph (plugin → skill edges) | **Represent** — curated node-link, hand-placed |
| **Anything else** | Catch-all | Any chart the eleven do not name? | Correlation heatmap (spans ML, finance, ops) + the long-tail list | **Represent** — one representative, illustrative; the rest inherit the doctrine |

Split: 7 named types implemented (the funnel ships two figures — agent run + sales
pipeline), 4 represented, plus the catch-all representative (illustrative). Network is
already covered under Relational; the catch-all is for genuinely unlisted types —
heatmap, treemap, sankey, choropleth / map (e.g., sales by state), radar,
histogram / area.

## Structure

The field guide is one block appended inside `<section id="dataviz">`, after the
sixth chapter (Color). It is visually distinct from the lint-ruled chapters so the
doctrine stays special — no `viz-chapter-code` letter, no lint table.

- **Block header:** eyebrow + headline ("The six decisions, applied") + a lede that
  names the honesty split.
- **Five job families + a catch-all group:** each family a light sub-header (family
  name + the job question), then its figures.
- **Catch-all group ("Anything else"):** a short methodology — any unnamed chart still
  obeys the six decisions and the house style, honesty-tagged if uncomputed — plus the
  long-tail list and one built representative (a correlation heatmap).
- **Per-figure anatomy:** `<figure>` with the inline SVG, a `viz-headline` takeaway
  (D01) for the larger charts, a one-line "use when," and — for the four represent
  charts — a visible "Illustrative" tag in the figcaption.
- **Layout:** small-multiples grid. Figures span `lg-span-4` or `lg-span-6` by
  complexity; viewBox ~320–420 × 200–240, matching existing example charts.

## House-style constraints (non-negotiable)

These mirror the existing §08 charts. Implementation must match, not reinvent:

- Inline SVG, `viewBox`, `role="img"` + `aria-label` (or `<title>`), `width:100%; height:auto`.
- Colors via `var(--success / --danger / --info / --ink / --gray-*)`. Green up, red
  down, blue reference/neutral, gray everything else.
- Two-shade fills via `color-mix(in srgb, X, white N%)`, never `fill-opacity` (opacity
  inverts lighter/darker on dark backgrounds — known gotcha).
- Sparse grid: 4–5 horizontal lines max, light weight.
- Larger charts headline their takeaway above the frame (D01).
- Theme-robust: legible in light and dark with no per-theme overrides beyond tokens.

## Honesty labeling (the 4 represent charts)

kNN, PCA, t-SNE/UMAP, network, and the catch-all heatmap each carry a short, visible
tag — `Illustrative — house treatment, not a computed analysis` — in the figcaption.
The data is curated to look right, not computed. t-SNE/UMAP additionally note these projections are
stochastic and non-reproducible. This labeling is a feature, not an apology: it is
the honest-data-viz doctrine applied to its own limits.

## Feedback panel

Add one entry to the `VIZ` array (the data-driven feedback system):
`{ id: 'dv-guide', label: '08 · Field guide' }`. The field-guide block gets
`id="dv-guide"` so the panel injects after it. `ALL` already concatenates `VIZ`, so
compiled order tracks DOM. One panel for the whole guide now; splittable per-family
later if iteration demands it (YAGNI).

## Accessibility

Every figure SVG carries `role="img"` and a descriptive `aria-label`. The four
represent charts state "illustrative" in both the visible tag and the aria-label, so
a screen-reader user is not told a fabricated dataset is real. No keyboard
interaction is added here; the a11y chapter's exemplar remains the interactive
reference.

## Non-goals

- No runtime data, no `fetch`, no JS charting library. Every chart is static SVG.
- No Plotly clone. We borrow each chart's *question and form*, rendered quiet.
- No new top-level section, no renumber. The guide lives inside §08.
- No computed ML. The represent charts and the catch-all heatmap are curated illustrations.
- The catch-all is methodology + one representative, not an exhaustive long-tail catalog.

## Deferred to the implementation plan

- Per-chart SVG coordinate construction, cross-referenced to the Plotly source pages
  for canonical form (PR-curve baseline = prevalence; biplot loadings as arrows;
  UMAP cluster separation).
- Build phasing: scaffold block → 7 implement → 4 represent → wire feedback → verify.
- Exact figure spans and small-multiples breakpoints.

## Verification criteria

- All named-type figures render (the funnel shows two), plus the catch-all heatmap;
  the five illustrative figures (kNN, PCA, UMAP, network, heatmap) show the tag.
- `dv-guide` feedback panel injects; typing produces a `## 08 · Field guide` block in
  the compiled coda; counter increments.
- Console clean in light and dark.
- Canonical mirrored to `/tmp/dslib.html` and
  `/tmp/composer-e2e/spraypixel-state.html` (md5-identical).
