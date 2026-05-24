# Chart Rules Extras

Additional rules beyond core Tufte principles, chart-pattern selection, and
color. These cover formatting, typography, interaction, mobile, and the
small details that separate a good chart from a publishable one.

## Number formatting

| Rule | Why |
|---|---|
| Right-align numeric columns | Eye lands on magnitude, not digit width |
| Align decimal points | Allows visual comparison of fractional values |
| Use thousands separators (`24,000` not `24000`) | Reduces parse time for large numbers |
| Or abbreviate consistently (`$24K`, `$24M`) | Saves space; consistent suffix style |
| Units in axis title, not every tick | Tick labels stay short; title carries unit once |
| Currency symbol on first and last tick only | Repetition adds noise |
| Percentages with one decimal max (`12.4%` not `12.43%`) | Spurious precision implies false accuracy |
| Negative numbers: minus sign, never parentheses in charts | Parentheses suit accounting tables, not charts |

## Typography

| Rule | Why |
|---|---|
| Sans-serif for axis labels, ticks, legends | Better at small sizes |
| Same typeface throughout the chart | Mixing fonts adds noise |
| Title is the largest element | Cognitive entry point |
| Title ≥ 14px in production | Mobile and screen-reader friendly |
| Annotation text matches body text size | Annotations are reading material, not chrome |
| Avoid italic for emphasis | Use weight or color instead |
| Avoid all-caps for axis labels | Reduces readability of long labels |

## Labeling and annotation

| Rule | Why |
|---|---|
| Always label the highest and lowest mark | Direct labels at extremes carry most of the legend's work |
| Reference lines: dashed `#aaa`, labeled inline | Solid lines compete with data marks |
| Annotation arrows should not cross the data | Arrows steal attention |
| Annotations sit in white space, not on marks | Marks own the data; whitespace owns the meta |
| When the chart shows the moment of a launch, outage, or policy change, annotate it | Context separates "trend" from "consequence" |

## Number-formatting consistency

| Within a chart | Rule |
|---|---|
| One currency style | `$24K` and `$24,000` in the same chart is a failure |
| One date format | `Apr 12` and `4/12/2026` in the same chart is a failure |
| One decimal precision per axis | Mixed precision implies different accuracy |
| One time-zone if temporal | UTC vs. local in the same chart loses meaning |

## Time axes

| Rule | Why |
|---|---|
| Show units (years, months, weeks) | "Jan" is ambiguous across years |
| Show the full range; do not truncate the start of time | Truncation hides regime changes |
| Annotate when the unit changes (daily → weekly aggregation) | Aggregation changes what the line means |
| Highlight weekends, holidays, or fiscal-quarter boundaries when relevant | Patterns often align to calendar structure |
| Sparklines: word-sized, no axes, dot for current value | Lives in reading flow, not above it |

## Interaction (when the chart is interactive)

| Rule | Why |
|---|---|
| Default view answers the headline question | Interaction is for follow-up, not for the main point |
| Tooltips enrich; the chart works without them | Tooltip-only data is invisible to PDFs and screen readers |
| Tooltips show: name, value, comparison, and context | Not just the value |
| Filters preserve scale across states | Switching cohorts must not rescale the y-axis silently |
| Hover state highlights one mark, dims others | The standard "spotlight" interaction |
| Click-to-isolate is reversible | Always provide reset |
| Animation only for transitions between states | Never animate the first reveal of static data |
| Animation duration ≤ 400ms | Longer feels slow; shorter feels janky |

## Scatterplots and dense data

| Rule | Why |
|---|---|
| Alpha for overplotting: `opacity: 0.3` or lower when N > 200 | Otherwise the densest region looks the same as a single point |
| Label outliers, not the center | The center is obvious; the outliers carry the story |
| Reference lines on scatterplots: x=y diagonal, regression, or threshold | Anchor the viewer's interpretation |
| Marginal histograms or rugs for distribution | Adds density without adding chart |
| Consider hexbin or 2D density for N > 5000 | Individual points become noise |

## Mobile and responsive

| Rule | Why |
|---|---|
| Cut decoration first on small screens | Legends, gridlines, borders, footnotes |
| Direct labels replace legends below 600px | Legend wraps eat vertical space |
| Sort and truncate before scrolling | Top-N matters more than scroll on phones |
| Tick density: roughly one per 80px of axis | Crowded ticks become unreadable |
| Touch targets ≥ 44px for interactive elements | iOS HIG floor |
| Tooltips on tap, not on touch — and dismissible | Touch != hover |

## Implementation

| Rule | Why |
|---|---|
| Separate data transformation from rendering | Testable, replaceable, debuggable |
| Make scale domains explicit | Same domain across small multiples is non-negotiable |
| Name variables by analytical meaning, not visual appearance | `revenue_y` beats `barHeight` |
| Add `aria-label` or text summary for screen readers | Charts without text are charts that exclude |
| Test edge cases: zero, null, outlier, long label, narrow screen, single category, negatives | Edge cases are where charts lie |
| Avoid CSS hover-only encoding | Hover does not exist on touch devices |

## Print and export

| Rule | Why |
|---|---|
| Monochrome must work | Convert to grayscale; meaning survives |
| Resolution: vector when possible, ≥ 300dpi raster when not | Charts get rescaled |
| Embed fonts or fall back gracefully | Missing fonts destroy alignment |
| Width-of-text figure (one column) vs. width-of-page (two column) | Plan the layout, not just the chart |

## The "publishable" gate

A chart is publishable when:

- A reader can pick up the page cold and understand the chart in under 10 seconds
- The chart works in grayscale
- The chart works at 60% size
- Removing the legend does not make the chart unreadable
- A screen reader can describe what the chart says
- A peer can find one fact in the chart faster than they could in the underlying table

If any of these fail, the chart is not yet publishable.
