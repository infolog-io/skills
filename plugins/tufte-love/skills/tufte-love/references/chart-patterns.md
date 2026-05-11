# Chart Selection and Replacement Patterns

## Use a table when

- Exact lookup matters.
- There are few values.
- Users need to compare named items precisely.
- Sorting and scanning matter more than visual trend.

Improve tables with:

- Meaningful sorting
- Right-aligned numbers
- Clear units
- Conditional emphasis only when useful
- Small inline bars or sparklines when trend matters

## Use a line chart when

- Time is the main structure.
- Continuity matters.
- Trend, volatility, or seasonality matters.
- Multiple related series need comparison.

Avoid:

- Too many colored lines.
- Unlabeled series.
- Dual axes.
- Smoothing without disclosure.
- Time windows that hide relevant history.

## Use a bar chart when

- Comparing magnitudes across categories.
- Values start from a meaningful zero.
- Categories are discrete.

Prefer:

- Horizontal bars for long labels.
- Sorting by value unless natural order matters.
- Direct labels for key values.

Avoid:

- 3D bars.
- Overly thick bars.
- Gradients.
- Decorative fills.

## Use a dot plot when

- Comparing many categories.
- Ranking matters.
- Space is limited.
- Differences are more important than filled area.

Dot plots are often cleaner than bar charts.

## Use a scatterplot when

- Relationship between two quantitative variables matters.
- Outliers matter.
- Clustering matters.
- Correlation or non-correlation matters.

Improve with:

- Labeled outliers
- Reference lines
- Transparency for overplotting
- Faceting by group
- Explicit units

## Use small multiples when

- One chart is overloaded.
- The same comparison repeats across groups.
- The reader needs pattern recognition.
- Consistent structure matters.

Small multiples are preferred for:

- Regional comparisons
- Cohort comparisons
- Product comparisons
- Scenario comparisons
- Repeated time-series

## Use a map when

- Spatial pattern is the point.
- Proximity or region matters.
- The viewer needs geographic distribution.

Avoid maps when:

- Ranking is the point.
- The geography is incidental.
- Population normalization is missing.
- Area size distorts perceived importance.

## Use a slopegraph when

- Comparing two points in time.
- Showing rank or value change.
- Before/after matters.

Rules:

- Label both endpoints.
- Use direct labels.
- Highlight meaningful changes.
- Avoid too many crossing lines unless crossing is the point.

## Use a connected scatterplot when

- Two variables change together over time.
- The path matters.
- Directionality matters.

Rules:

- Label start and end.
- Mark time intervals.
- Use cautiously; readers may need guidance.

## Use annotation when

- A spike has a known cause.
- A policy, launch, outage, or intervention changes interpretation.
- A threshold matters.
- A comparison needs explanation.

Annotation should explain evidence, not decorate it.

## Replace these weak patterns

| Weak pattern | Replace with |
|---|---|
| Pie chart with many slices | Sorted bar chart or dot plot |
| Dashboard card with one big number and no context | KPI with sparkline and benchmark |
| Dual-axis chart | Indexed line chart, small multiples, or normalized comparison |
| Choropleth for ranked values | Sorted dot plot plus optional map |
| 3D chart | 2D chart |
| Overloaded multi-line chart | Small multiples |
| Legend far from data | Direct labels |
| Decorative infographic | Evidence-first annotated graphic |
| Gauge chart | Bullet chart or target line |
| Donut chart | Labeled bar or compact table |

## Implementation standards

When coding charts:

- Keep data transformation separate from rendering.
- Name variables by analytical meaning, not visual appearance.
- Make scale domains explicit when comparison depends on them.
- Use consistent scale domains across small multiples.
- Add accessible text summaries.
- Ensure tooltips are not the only place where values appear.
- Avoid animation that changes interpretation.
- Test with edge cases:
  - zero values
  - null values
  - outliers
  - long labels
  - narrow screens
  - many categories
  - single-category data
  - negative values

## Worked example: dashboard pie chart → sorted dot plot

### Before

A SaaS pricing dashboard shows "Revenue by plan" as a 6-slice pie chart. Each slice has a different gradient fill. The legend sits on the right, sorted alphabetically. Slice labels show the plan name only, not the revenue value.

Failure modes:

- `comparison_failure`: viewer cannot rank plans by revenue without scanning the legend.
- `chart_type_failure`: pies prevent precise comparison between similar-sized slices.
- `decoration_failure`: gradients carry no information.
- `labeling_failure`: the legend forces the eye to bounce between chart and key.

### After

Replace with a horizontal dot plot:

- One dot per plan, sorted by revenue descending.
- Plan name as the left-axis label.
- Revenue value as a direct right-of-dot label, formatted as `$24K`.
- Single neutral fill for all dots.
- Faint vertical reference line at the previous-period total.

Result:

- Ranking is immediate.
- Magnitude differences are precise.
- The reference line answers "is this growing?" without a second chart.

### Audit

```text
Tufte Love Audit
- Data truth: 5 — units, denominator, and reference period all visible
- Comparison quality: 5 — sorted dots make ranking and magnitude immediate
- Data density: 4 — adds prior-period reference without crowding
- Labeling: 5 — direct labels eliminate the legend
- Visual noise: 5 — single fill, no gradients, no borders
- Chart-type fit: 5 — dot plot fits ranking-with-magnitude better than pie
- Interaction: 3 — static; tooltip could surface plan-level breakdown
- Recommended next change: split into small multiples by cohort
- Confidence: High
```
