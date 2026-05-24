# Tufte-Style Principles for Quantitative Display

## 1. Graphical excellence

Graphical excellence means complex ideas are communicated with clarity, precision, and efficiency.

A strong graphic does several jobs at once:

- Shows the data.
- Lets the viewer compare values.
- Reveals patterns across time, space, category, or relationship.
- Makes large data sets coherent.
- Encourages close inspection.
- Avoids distortion.
- Supports decision-making.

The standard is not beauty alone. The standard is truthful analytical compression.

## 2. Data before decoration

Every visible element should earn its place.

Ask:

- Does this mark represent data?
- Does it clarify data?
- Does it help comparison?
- Does it orient the reader?
- Does it explain uncertainty, context, or causality?

If not, remove or reduce it.

Common non-data clutter:

- Heavy borders
- Redundant gridlines
- Background gradients
- Decorative icons
- Drop shadows
- Unnecessary legends
- Oversized titles
- Axis furniture that dominates the data

## 3. Maximize useful data density

High density is not clutter when the structure is clear.

Dense graphics work when they:

- Use small marks.
- Use consistent scales.
- Use direct labels.
- Use repetition.
- Organize by meaningful dimensions.
- Give the reader both overview and detail.

Low-density graphics fail when they use large visual space to communicate one or two numbers that could be written as text.

## 4. Comparison is the heart of evidence

Most quantitative graphics exist to compare.

Useful comparisons include:

- Before vs. after
- Actual vs. expected
- One category vs. another
- Local vs. global
- Outlier vs. distribution
- Current vs. historical
- Rate vs. count
- Absolute vs. normalized value
- Correlation across two variables
- Same measure across geography

A chart that does not clarify comparison is usually decorative reporting.

## 5. Multivariate display is often necessary

Real evidence often requires multiple variables.

Good multivariate graphics combine dimensions such as:

- Time
- Space
- Quantity
- Category
- Direction
- Rate
- Uncertainty
- Group membership
- Sequence
- Cause or intervention point

The goal is not to cram variables in. The goal is to show the structure of the problem.

## 6. Small multiples

Small multiples are repeated views using the same visual structure.

Use them when comparing:

- Regions
- People
- Products
- Cohorts
- Time periods
- Scenarios
- Experimental conditions
- Market segments

Rules:

- Keep scales consistent unless explicitly labeled otherwise.
- Keep layouts predictable.
- Reduce decoration.
- Use titles or direct labels.
- Sort panels by a meaningful variable when possible.

Small multiples are usually better than one overloaded chart with too many colors.

## 7. Time-series discipline

Time-series graphics should preserve temporal structure.

Good time-series graphics:

- Show enough history for context.
- Mark meaningful events or interventions.
- Avoid smoothing that hides important variation.
- Use consistent time intervals.
- Keep labels close to lines.
- Separate seasonal, cyclical, and trend components when useful.
- Avoid dual axes unless the relationship is central and clearly explained.

Time alone does not prove causality. Add context when explaining change.

## 8. Maps only when space matters

Use maps when geography is analytically meaningful.

A map is justified when the reader needs to see:

- Spatial clustering
- Regional variation
- Flow across territory
- Proximity
- Distribution by location
- Geographic outliers

Do not use a map merely because data contains location fields.

For many geographic data sets, sorted dot plots, ranked tables, or small multiples are clearer.

## 9. Relational graphics

Use relational graphics when the analytical question is about association.

Examples:

- Scatterplots
- Connected scatterplots
- Bubble charts, used cautiously
- Matrix plots
- Small-multiple scatterplots

Rules:

- Label outliers.
- Show units.
- Use appropriate scales.
- Avoid overplotting.
- Distinguish correlation from causation.
- Add trend lines only when the statistical relationship is meaningful.

## 10. Tell the truth

A graphic lies when it distorts evidence.

Common lies:

- Truncated axes that exaggerate change.
- Area encodings that inflate differences.
- Inconsistent scales across panels.
- Cherry-picked time windows.
- Missing denominators.
- Suppressed outliers.
- Misleading aggregation.
- Unlabeled uncertainty.
- Visual emphasis that does not match the data.

Truth is not only about accurate numbers. It is also about honest context.

---

<!-- Merged from gist: https://gist.github.com/aparente/e48c353755958621b3c0004593105a90 -->

## Formal definitions and quick reference

The sections above are the practitioner playbook. The definitions below are the named frameworks from *The Visual Display of Quantitative Information* that anchor those rules.

### Lie Factor

```
Lie Factor = Size of effect shown in graphic / Size of effect in data
```

- Lie Factor = 1.0: truthful.
- Lie Factor > 1.05 or < 0.95: distortion.

### Six principles of graphical integrity

1. Representation of numbers should be directly proportional to quantities represented.
2. Clear, detailed, thorough labeling defeats distortion.
3. Show data variation, not design variation.
4. In time-series displays, standardize money (deflate) and use consistent baselines.
5. Dimensions of graphics should not exceed dimensions of data.
6. Graphics must not quote data out of context.

### Data-ink ratio

```
Data-Ink Ratio = Data-ink / Total ink used in graphic
```

Maximize within reason:

1. Erase non-data-ink (decoration, heavy grids, boxes).
2. Erase redundant data-ink (3D when 2D suffices).
3. Revise and edit.

**The eraser test:** if you can erase something without losing data information, erase it.

### Three categories of chartjunk

- **Moiré vibration** — busy patterns and cross-hatching that create visual noise.
- **The Grid** — heavy gridlines compete with data; mute or eliminate them.
- **The Duck** — self-promoting graphics that draw attention to their own design rather than the data.

### Multifunctioning graphical elements

Every graphical element should serve multiple purposes when possible.

- Data points that also serve as labels (scatter plots with text).
- Axes that double as a data series.
- Range-frames where the axis shows the data range, not an arbitrary extent.
- Marginal rugs that turn an axis into a marginal distribution.

### The Tufte test

For any visualization, ask:

1. **Data-Ink:** can I erase any element without losing data?
2. **Integrity:** does the visual effect match the data effect? (Lie Factor ≈ 1)
3. **Chartjunk:** does any element exist for decoration only?
4. **Excellence:** does it reveal the data at multiple levels?
5. **Comparison:** can the viewer easily compare data elements?
6. **Density:** could this show more data in the same space?
7. **Context:** is all necessary context provided (labels, sources, scales)?

For the extended test covering causality, multivariate integration, and layering, see `analytical-design.md`.

<!-- End merged content -->
