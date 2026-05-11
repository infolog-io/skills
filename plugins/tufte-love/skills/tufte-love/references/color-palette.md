# Color Palette

Color is a channel. It must carry information or it must recede. Decoration
spends ink without spending evidence — refuse it.

## Default palettes

| Use case | Palette | Why |
|---|---|---|
| Categorical, ≤8 classes | **Okabe-Ito** | Color-blind safe across deuteranopia, protanopia, tritanopia; survives print |
| Categorical, ≤6 classes | **Tableau 10 (muted)** | Designed for charts, not branding; pleasant in long sessions |
| Sequential | **viridis** or **cividis** | Perceptually uniform across lightness; readable in monochrome |
| Diverging | **ColorBrewer RdBu** | Symmetric around zero; preserves direction in CB simulation |
| Neutral default | `#444` mark + `#bbb` reference grid | Most marks should be gray; let the saturated color earn its place |

### Okabe-Ito hex values

```
#000000  black
#E69F00  orange
#56B4E9  sky blue
#009E73  bluish green
#F0E442  yellow
#0072B2  blue
#D55E00  vermillion
#CC79A7  reddish purple
```

### viridis sample points (5 stops)

```
#440154  dark purple   (low)
#3B528B  blue-purple
#21908C  teal
#5DC863  green
#FDE725  yellow         (high)
```

## Rules

### Most of the chart is gray

Default mark color: `#444` or `#666`. Reserve saturated color for the one
mark that carries the comparison. If three marks are highlighted, no mark is
highlighted.

### Color must survive a photocopier

Run a quick monochrome test. Convert the chart to grayscale. If meaning
collapses, color was carrying a job that shape, position, weight, or label
should have carried instead.

### Never rainbow for sequential data

Red-yellow-green or jet palettes are perceptually non-uniform and lose
ordering in CB simulation. Use viridis, cividis, or a single-hue gradient.

### Brand colors are not data colors

Brand palettes are tuned for recognition, not for visual encoding. Pull the
brand's primary accent for the **one** highlighted mark; let everything else
stay gray. Do not encode categories with brand-tier colors.

### Hue ≠ ordinal

If categories have a natural order (severity, time, magnitude), use
luminance or saturation steps within one hue. Different hues imply
categorical equivalence.

### Categorical legend order

Sort by value in the data (descending), or by reading order in the chart.
Never alphabetical when the chart sorts by something else — the legend and
the chart must agree.

### Background is paper

Default to white or `#fafafa`. Dark mode is acceptable when the data marks
are the brightest thing on screen. Never use a colored background that
competes with the data's color encoding.

### Annotations sit one step quieter than data

Title is darker than gridlines. Gridlines are lighter than marks.
Annotations match the visual hierarchy: explanation in dark text, reference
lines in `#aaa`, dashed.

### Highlight by exception

The strongest pattern in a Tufte-style chart is: 90% gray, 10% color. The
viewer's eye lands where you direct it. Two competing highlights destroy the
effect.

## Anti-patterns

| Anti-pattern | Why it fails | Replacement |
|---|---|---|
| Rainbow palette for sequential data | Non-uniform; loses order in CB simulation | viridis or cividis |
| Red/green only for good/bad | ~8% of viewers cannot distinguish | Add shape or position; use blue/orange |
| Saturated color on every mark | No mark can be highlighted | Gray default, color the one that matters |
| Gradient fills on bars | Carry no information | Single neutral fill |
| Brand-palette categorical encoding | Cognitive collision with brand recognition | Okabe-Ito or Tableau 10 |
| 3D depth shading | Implies a dimension that does not exist | 2D |
| Color-only encoding | Inaccessible | Add shape, position, or label as redundancy |

## Worked example

### Before

A churn dashboard shows seven customer cohorts as seven different saturated
hues on one line chart. The legend sits at the right with cohort names. Two
cohorts are red and orange — the user reads "red is bad" but red is
arbitrary.

### After

- Six cohorts in `#bbb` (light gray), one line per cohort, no legend.
- The cohort currently underperforming in `#D55E00` (Okabe-Ito vermillion).
- Direct labels at the right end of each line.
- Title: "Cohort retention — March cohort underperforming since week 4."

The single highlighted line, plus the title, plus direct labels, does the
work the legend and seven hues were attempting. Color now carries meaning;
gray carries context.

## Accessibility

| Check | Pass criteria |
|---|---|
| Contrast against background | Marks ≥ 3:1; text ≥ 4.5:1 (WCAG AA) |
| Color-blind simulation | Run through Coblis or browser plugin; meaning survives |
| Monochrome print | Convert to grayscale; meaning survives |
| Pattern redundancy | Encoding does not depend on color alone |

Color-blind-safe is the floor, not the ceiling. The chart should remain
readable for a viewer with no color perception at all — that constraint
produces better charts for everyone.
