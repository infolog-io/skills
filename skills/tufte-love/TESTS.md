# tufte-love — Tests & End Conditions

## Profile

**Full-shape skill.** Uses `references/` (spec-canonical). Other folders
follow on-demand as the skill grows.

## End conditions (skill ships when all are true)

1. Plugin installs cleanly via `claude plugin install tufte-love@infolog-io`
2. Skill activates on every trigger phrase listed in SKILL.md
3. All six reference files exist (`tufte-principles`, `audit-rubric`, `chart-patterns`, `output-formats`, `color-palette`, `chart-rules-extras`)
4. The canonical audit block lives in SKILL.md step 6 only (9 dimensions); `references/audit-rubric.md` points to it rather than redefining it
5. README ≤200 words

## Test cases

### T1 — Pie chart with many slices
- Input: dashboard description with a 6-slice pie chart for "revenue by plan"
- Expected: `chart_type_failure` flagged; replacement = sorted dot plot; audit reflects the change
- Verify: comparison-quality score rises after replacement

### T2 — Dual-axis chart audit
- Input: a chart with sales (left axis) and percent margin (right axis) on the same plot
- Expected: `chart_type_failure` flagged; replacement = small multiples or indexed line chart
- Verify: data-truth score addresses the misleading scale comparison

### T3 — Color-only encoding
- Input: a categorical chart where the only distinguishing channel is hue
- Expected: `color` dim scores ≤3; mono-survival test flagged; recommendation = add shape or position as redundant channel

### T4 — Rainbow palette for sequential data
- Input: a heatmap or choropleth using red-yellow-green hues for an ordinal scale
- Expected: `color` dim scores 1-2; replacement = viridis or single-hue gradient

### T5 — Sparkline in a dashboard
- Input: a KPI card showing one big number with no context
- Expected: `density_failure` flagged; replacement = KPI with sparkline and benchmark

### T6 — Final audit format
- Output: a `Tufte Love Audit` block containing 9 numeric scores (data truth, comparison, density, labeling, visual noise, chart-type fit, interaction, color, formatting), a recommended next change, and a confidence level
- Verify: format matches the canonical block in SKILL.md step 6 (the single source; `references/audit-rubric.md` defers to it)

### T7 — Mode selection (critique vs. code review vs. generation)
- Input mode 1: a design mockup → emit design critique format (from `references/output-formats.md`)
- Input mode 2: a code snippet → emit code-review format
- Input mode 3: "build a visualization for X data" → emit visualization-plan format

### T8 — Multi-chart dashboard scope
- Input: a dashboard with four charts, "tufte audit" requested
- Expected: ONE audit block for the surface, with per-chart findings listed under it
- Verify: per-chart audit blocks appear only when the user asks for depth

## Acceptance rubric per artifact

| Artifact | Must |
|---|---|
| SKILL.md | Names every reference file; canonical audit block (sole definition); trigger phrases; one-block-per-dashboard rule |
| `references/tufte-principles.md` | Core principles distillation; hard standards (must-not / should) |
| `references/audit-rubric.md` | 9 scored dimensions with questions and score anchors; 11-code failure taxonomy mapped to dimensions; pointer to SKILL.md step 6 block |
| `references/chart-patterns.md` | When-to-use table; weak-pattern replacement table; worked example with full 9-dimension audit |
| `references/output-formats.md` | Design-critique, code-review, and visualization-plan templates |
| `references/color-palette.md` | Default palettes (Okabe-Ito, viridis, ColorBrewer); accessibility checks |
| `references/chart-rules-extras.md` | Number formatting, typography, time axes, interaction, mobile, print |

## Out of scope for v1

- Live chart rendering or screenshot diffing
- Automated extraction of charts from PDFs or screenshots
- Direct integration with chart libraries (D3, Vega, Recharts)
- Accessibility checks beyond color contrast and CB simulation
- Internationalization of typography rules
