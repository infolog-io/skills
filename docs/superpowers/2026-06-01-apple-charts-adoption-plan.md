# Plan — adopt Apple chart styles/rules across §08 field guide

Date: 2026-06-01 · Branch `feat/component-composer` · file:
`docs/superpowers/reference/infolog-lib-design-system.html`

Sources (user-specified): Apple WWDC22 **"Design an Effective Chart"** (110342) +
**"Design App Experiences with Charts"** (110340) + HIG "Charts". Two asks:
(1) the node-link network is hard to read — redesign it; (2) apply one consistent
coloring convention to every chart, per Apple.

## Apple rules we adopt (distilled, with quotes)

- **Color is additive, never the sole encoding.** "Use color as an addition… not the
  only means to convey critical information." Pair color with position, label, or symbol.
- **Categorical series need redundant symbols.** Apple's example marks San Francisco with
  circles, Cupertino with squares — shape *and* color. Support "Differentiate Without Color."
- **Balance saturation/luminosity** so no color dominates and implies false hierarchy.
- **Consistent color meaning** across every chart in the system.
- **Use one stronger color/weight intentionally** to draw attention (highlight the notable mark).
- **Familiar forms first; a novel form must be prominent and clearly introduced.**
- **Descriptions state the takeaway** (already done: each figure has a headline + use-note).
- Support Dark/Light/Increase-Contrast (already done).

## Current state — audit (ground-truth, verified by grep + browser)

**Already consistent and Apple-aligned — DO NOT touch (avoid churn):**
- Semantic green=up/good, red=down/bad: skills-shipped line, slopegraph, OHLC, both
  funnels, ARR waterfall, correlation heatmap, latency breach overlay.
- Reference/baseline = blue (`info`): latency SLO, ROC + PR no-skill diagonals, completion
  identity line. Consistent.
- Neutral observed data = `gray-700`: latency line, completion points, candle context.
- Positive-direction metric = green: skills-shipped + throughput lines (coherent: green
  only when "up = good"; latency stays neutral gray because "up = bad").
- ROC + PR are both green curves in separate panels — consistent, not a collision.

**The real violations (what this plan fixes):**
1. **Categorical charts reuse semantic colors as arbitrary cluster IDs.** PCA
   (green/blue/gray), UMAP (green/blue/red/gray), kNN (green/blue/red). Here red ≠ "bad"
   and green ≠ "good" — it collides with the semantic system.
2. **Color-alone distinction.** Those clusters are all circles; only fill differs. Violates
   "never rely on color alone / add symbols."
3. **Network node-link is hard to read.** 8 of 11 nodes unlabeled, ~10 thin edges cross in
   the center, no legend, no grouping. A node-link is a *novel* form → Apple says it must be
   prominent and clearly introduced; this one is neither.

## The unified convention (encode as a short comment block at the top of `#dataviz`)

| Role | Color | Redundant channel |
|------|-------|-------------------|
| positive / up / gain / good outcome | green `--success` | position, sign, label |
| negative / down / loss / breach | red `--danger` | position, sign, label |
| reference / baseline / model fit | blue `--info` | dashed style, label |
| neutral observed data / context | `--gray-700` | — |
| axes / gridlines / scaffolding | `--gray-500` / `--gray-300` | — |
| **categorical (no good/bad meaning)** | balanced palette + **distinct symbol per category** | **shape + label/position** |
| intentional emphasis (the notable one) | stronger weight/one accent | size/label |

Rule: **semantic hues keep fixed meaning; categories are encoded by SHAPE first, color second.**

---

## Part A — Network redesign (the explicit ask)

Goal: answer "what connects to what?" at a glance, and show which skills are shared.
Keep the house palette (blue plugin / gray skill / gray edges).

Recommended: **labeled bipartite fan-out.**
- Plugins as a left column (3 blue nodes), each **labeled**.
- Distinct skills as a right column, each **labeled** with its real marketplace name.
- Edges left→right, ordered to minimize crossings.
- **Shared skills** (html-sketch, generator-critic) emphasized — thin `info` ring + placed
  in the band between their two parent plugins; both incoming edges visible.
- Tiny inline key: `● plugin   ● skill   ◌ shared`.
- Redundant encoding: node type = color **+** column **+** label; shared = ring **+** position.
- Converge pixels in-browser (light + dark).

Alternative if bipartite is cramped at half-width: keep top-down grouped layout but label
every node, group each plugin's skills beneath it, ring the shared ones, add the key.

## Part B — Categorical-color discipline (PCA / UMAP / kNN)

Apply Apple's "shape + color, balanced palette."
- Distinct **symbol per cluster**: circle ●, square ■, triangle ▲, diamond ◆.
- Swap the semantic **red** out of arbitrary clusters (red stays reserved for "bad/down").
  Candidate categorical set: blue / gray-700 / `--ink-soft` / (green only if a cluster is
  genuinely positive — it isn't here, so treat clusters as neutral categories).
- Balance saturation so no cluster dominates; kNN region tints follow their point colors.
- Keep the `illustrative` tag. Verify clusters distinguishable in greyscale.

## Part C — Minor (low priority, confirm)

- Language dot-plot: blue leader dot is intentional emphasis — likely keep.
- Add a one-line palette-convention comment near the top of `#dataviz`.

## Keep unchanged (no churn)

Funnels, waterfall, heatmap, slopegraph, OHLC, skills-shipped, latency, throughput, queue
forecast, completion scatter, ROC/PR — all already follow the convention.

## Verification (each step)

- `cp` to `/tmp/dslib.html` + `/tmp/composer-e2e/spraypixel-state.html`; `md5` all three.
- Browser (file://, both themes): legibility, no clip/collision, console clean.
- Greyscale / Differentiate-Without-Color check on categorical charts.
- Commit per logical unit; push HELD.

## Decisions taken + status

User chose **bipartite fan-out** (network) and **symbols + balanced color** (projections).

- **Part A — DONE** (`ce6b8e6`). Network rebuilt as a labeled bipartite fan-out: plugins
  left, skills right, every node labeled, zero edge crossings, shared hubs ringed, inline
  key. Verified light + dark.
- **Part B — DONE** (`360671c`). PCA / UMAP / kNN clusters now carry distinct shapes
  (circle / square / triangle / diamond); semantic red dropped from arbitrary clusters
  (→ neutral ink-soft triangle + neutral kNN region tint); per-point radius jitter kept.
  Passes greyscale / Differentiate-Without-Color. Verified light + dark.
- **Part C — not done** (optional): a palette-convention comment block in `#dataviz`.
  Skipped as non-functional; easy to add if wanted.

Palette-constraint note: the house palette has only two vivid hues once red is reserved
(green, blue), so the two "neutral" projection clusters lean on shape + position rather
than hue. The greyscale test confirms this is sufficient. A 4th balanced categorical hue
would require expanding the token set (deliberately not done).

Push still HELD.
