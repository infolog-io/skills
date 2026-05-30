# infolog-io · Patterns

Preferred chart patterns. The drafter consults these before composing.
When a pattern fits, use it.

## Time-series → line chart, not bar

Lines preserve sequence. Bars imply discrete intervals. Use line for any
ordered continuous quantity over time.

## Many-to-many comparison → small multiples

A single overloaded chart with N colors fails. N panels with identical
encoding, sorted meaningfully, succeeds. Use small multiples for any
comparison across categories, regions, cohorts, or time periods.

## Part-to-whole → bar or table, never pie

Pies prevent precise comparison. Bars and tables enable it. If exact
values matter, use a table.

## Tiny N (≤ 5) → table

When you have ≤ 5 data points, a table is more honest than a chart. The
chart pretends pattern; the table shows truth.

## Trend at a glance → sparkline

For each row in a metrics table, append a sparkline of the last 30 days.
Sparkline ≤ 80px wide, ≤ 16px tall, no axis. End-value labeled.

## Before vs after → slopegraph

Two ordered points per entity. Connect with a line. Sort by ending
value. Direct labels on left and right.

## Distribution + comparison → dot plot, not bar

Dots are more precise than bars. Each row: category label on left,
horizontal line + dot at value. Sort by value.

## Categorical magnitude → strip plot

When you want to show the spread of individual values within a category.
Each entity is one dot on a horizontal axis.

## Range-frame axes

Axis lines start at the minimum data value and end at the maximum. The
axis communicates the data extent without explicit annotation.

## Direct labels over legends

When two or more colors encode categories, label the lines directly at
their right edge instead of using a legend. Eye doesn't have to bounce
between key and chart.

## One highlight per chart

90% gray + 10% color. At most one mark uses `--accent-warm`. Two
highlights destroy the focal effect.

## Words integrate with numbers

Sentence fragments next to data: "Revenue trended up ▁▂▄▆▇ over Q3."
Sparkline inline. Don't segregate "narrative" from "chart".

## Footer with provenance

Every artifact carries a footer line: source, date pulled, methodology
note if needed. Tufte: thoroughly describe the evidence.
