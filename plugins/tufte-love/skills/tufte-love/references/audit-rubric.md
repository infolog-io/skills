# Tufte Love Audit Rubric

Score each dimension from 1 to 5.

- 1 = broken or misleading
- 2 = weak
- 3 = acceptable
- 4 = strong
- 5 = excellent

## 1. Data Truth

Questions:

- Are units clear?
- Are denominators visible?
- Are scales honest?
- Are transformations disclosed?
- Are outliers preserved or explained?
- Is missing data handled clearly?
- Is uncertainty shown when needed?
- Does the visual avoid implying false causality?

Score:

- 1: Misleading or materially distorted.
- 3: Mostly accurate but missing context.
- 5: Accurate, contextual, and hard to misread.

## 2. Comparison Quality

Questions:

- Can the viewer compare the right things quickly?
- Are related values near each other?
- Are scales consistent?
- Are panels or categories sorted meaningfully?
- Are labels close to the evidence?
- Does the chart make outliers visible?

Score:

- 1: Comparison is difficult or impossible.
- 3: Comparison works with effort.
- 5: Comparison is immediate.

## 3. Data Density

Questions:

- Is the amount of information appropriate for the space?
- Is the chart wasting space on one or two obvious numbers?
- Could a table, sentence, or sparkline do the job better?
- Is density organized rather than chaotic?
- Does the visual show both overview and detail?

Score:

- 1: Mostly empty or bloated.
- 3: Reasonable but could be tighter.
- 5: Rich, readable, and efficient.

## 4. Labeling

Questions:

- Are axes labeled?
- Are units visible?
- Are important marks directly labeled?
- Is the legend avoidable?
- Are annotations used where context changes interpretation?
- Is text concise but sufficient?

Score:

- 1: Reader must guess.
- 3: Basic labels exist.
- 5: Labels are placed where they reduce cognitive load.

## 5. Visual Noise

Questions:

- Are gridlines too heavy?
- Are colors meaningful?
- Are decorative effects competing with data?
- Are borders necessary?
- Are icons or illustrations adding evidence or merely style?
- Is hierarchy clear?

Score:

- 1: Decoration overwhelms evidence.
- 3: Some unnecessary furniture.
- 5: Nearly every mark has a job.

## 6. Chart-Type Fit

Questions:

- Does the chart match the analytical question?
- Would another form support comparison better?
- Is a map actually needed?
- Is a bar chart hiding distribution?
- Is a pie chart preventing precise comparison?
- Is a table better for exact lookup?

Score:

- 1: Wrong chart type.
- 3: Usable but not optimal.
- 5: Form fits the question precisely.

## 7. Interaction

Questions:

- Does interaction reveal detail rather than hide essentials?
- Does the default view already communicate the main point?
- Are tooltips supplemental rather than required?
- Does filtering preserve context?
- Does responsiveness preserve comparison?

Score:

- 1: Interaction hides the evidence.
- 3: Interaction is usable.
- 5: Interaction deepens understanding without becoming necessary.

## Final Audit Summary

Use this format:

```text
Tufte Love Audit
- Data truth: [1-5] — [reason]
- Comparison quality: [1-5] — [reason]
- Data density: [1-5] — [reason]
- Labeling: [1-5] — [reason]
- Visual noise: [1-5] — [reason]
- Chart-type fit: [1-5] — [reason]
- Interaction: [1-5] — [reason]
- Recommended next change: [single highest-leverage fix]
- Confidence: [High / Medium / Low]
```

## Priority Rule

If a chart is beautiful but misleading, score it low.

Truth beats polish.
Comparison beats decoration.
Evidence beats style.
