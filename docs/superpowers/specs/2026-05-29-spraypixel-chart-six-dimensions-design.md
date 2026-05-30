# spraypixel chart system — six dimensions of an effective chart

Date: 2026-05-29
Status: approved design, pending implementation
Target page: `/tmp/composer-e2e/spraypixel-state.html` §07
Eventual home: `spraypixel-skills` repo (graduation deferred)

## Goal

Expand §07 from a color-only chart lint into a six-dimension chart system. The
section today formalizes R01–R10, ten rules that all govern color. An effective chart decides six things, drawn from the data-viz
canon (Tufte, Bertin, Cleveland, Brewer). Color is one.
This work adds the other five and reframes color as the sixth.

The user picked: prove on the page first, broad survey across all six
dimensions with one specimen each, teach by exemplar plus prose anti-pattern.

## The reframe (philosophy)

§07 stops being "Data viz, a color lint." It becomes "An effective chart decides
six things." R01–R10 are not demoted or rewritten. They become Chapter 6 of 6,
the one chapter already finished to high rigor.

The intellectual claim: color discipline is necessary, not sufficient. A chart
that nails color but picks the wrong mark, or lies with a truncated axis, still
fails. Tufte governs the ink. The six dimensions govern the decisions made before the ink.
The section credits both lineages.

## Naming scheme

R01–R10 stay as-is for Color. Each new chapter gets a letter prefix. This
matches the page's existing R-code idiom and the infolog rubric style (S1, P1).

| Prefix | Chapter |
|---|---|
| G | Goal |
| M | Marks |
| X | Axes |
| D | Descriptions |
| A | Accessibility |
| R | Color (unchanged) |

## The six chapters

Each chapter carries one exemplar specimen plus a compact rule cluster.
Anti-patterns are described in the rule text, never rendered. This matches the
page's current philosophy: it lists removed anti-patterns in prose, it does not
draw bad examples.

### G — Goal

Rules:
- G01 core-question-first: name the one question the chart answers before drawing.
- G02 design-for-focus: one chart, one variable cluster. Resist crowding.
- G03 familiar-forms: prefer bar and line. Novel forms need onboarding.

Exemplar: the existing cumulative line. It answers one question (is the count
growing?) in a familiar form. Reused, not rebuilt.

### M — Marks

Rules:
- M01 line-is-trend: line marks for rates of change and continuous trends.
- M02 bar-is-discrete: bar marks for discrete categories, cumulative sums, and
  time series that can drop to zero without breaking continuity.
- M03 point-is-relationship: point marks for relationships between two
  properties, clusters, and outliers. Avoid raw points for dense noisy data.

Exemplars: three existing charts already demonstrate the three marks. Cumulative
line serves M01. Explicit-zero bar serves M02. Dot plot serves M03. Reused.

### X — Axes

Rules:
- X01 bars-start-at-zero: a bar's y-axis lower bound must be zero. Height must
  encode proportion truthfully.
- X02 fixed-vs-dynamic-range: fixed range when limits carry fixed meaning
  (0–100%). Dynamic range when small variations matter and a zero baseline would
  flatten them.
- X03 intuitive-ticks: label with familiar increments (5, 10, 25), not
  math-driven splits (1, 6, 11).
- X04 sparse-grid: 4–5 horizontal grid lines. Lighter and fewer when the chart
  supports tap-to-inspect.

Exemplars: explicit-zero bar serves X01. OHLC candlestick serves X02 (price
ranges do not start at zero). Reused.

### D — Descriptions

Rules:
- D01 headline-the-takeaway: text above the chart states the primary insight. Do
  not make the reader derive the trend unaided.
- D02 macro-medium-micro: layer context at three levels. Macro is the whole
  dataset. Medium is a meaningful subset. Micro is a specific focus point.

Exemplar: the cumulative line gains a three-level caption demonstrating D02.
This is a small modification to an existing chart, not a new build.

### A — Accessibility

Rules:
- A01 context-then-value: labels say "June 6, 850 pancakes," not "850." No
  abbreviations. "June 6" not "6/6." "60 minutes" not "60m."
- A02 visible-focus: focus rings are large, thick, and high-contrast against
  chart elements.
- A03 input-parity: every touch or mouse gesture maps to keyboard, screen
  readers, voice input, and switch access.
- A04 sonification (note only): expose data points for a pitch-shifted
  audio readout. Documented as a rule; the
  HTML specimen cannot render audio, so this is text plus an aria note.

Exemplar: ONE genuinely new specimen. A small chart with a visible focus ring on
the selected mark and a live label readout rendering "June 6, 850 units" in the
A01 format. This is the only dimension with zero coverage today, so it earns the
single new build.

### R — Color

R01–R10 unchanged. Exemplified by every existing chart. The cluster gains one
framing sentence on the color dimension (color enhances, never the sole
channel; mute to direct focus; test against color blindness, dark mode, and
high-contrast modes).

## Material build list

| Item | Action | Cost |
|---|---|---|
| §07 header + deck | rewrite to six-dimension frame | text |
| G/M/X/D/A rule clusters | write new | text |
| R01–R10 | keep, add one framing line | text |
| Six existing charts | wrap under chapter headers, label which dimension each exemplifies | reorg |
| Cumulative line | add macro/medium/micro caption (D02) | small modify |
| Accessibility specimen | build new: focus ring + accessible label readout | 1 new chart |

Net new drawing: one chart plus one caption modification. Everything else is
reframe and rule text. This honors "one specimen per dimension" by promoting
existing charts into the dimension frame, and spends the build budget on the one
real gap.

## Out of scope

- No wrong-then-right paired specimens. The user chose exemplar plus prose.
- No sonification implementation. Documented as a rule, noted in aria.
- No graduation to spraypixel-skills this pass. Prove on the page first.
- No new chart types beyond the Accessibility specimen.
- No changes to the existing palette or token work from earlier this session.

## Verification

- Reload preview, confirm no console errors.
- Confirm heading outline stays clean (chapter headers must not reintroduce an
  h-level skip; use the same h2-at-h3-scale pattern established earlier).
- Confirm the Accessibility specimen's focus ring is keyboard-reachable and the
  label readout renders the A01 format literally.
- Confirm the macro/medium/micro caption reads at all three levels.
- Screenshot §07 in light and dark via agent-browser.
- Re-run the em-dash and all-caps checks on new copy.

## Graduation path (future, not this pass)

When the page proves out, the six-chapter structure graduates to
`spraypixel-skills` as prose reference files under
`skills/spraypixel/references/`, matching the repo's house style (H2 sections and
tables, not R-codes). The page keeps the R-code lint; the repo gets the prose.
