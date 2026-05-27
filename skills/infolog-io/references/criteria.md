# infolog-io · Validator criteria

Each criterion has an id (the markdown H2) and a check description. The
composer dispatches mechanical checks first; remaining criteria go to
LLM-as-judge.

---

## text_collision

No text labels overlap each other or data marks. Tick labels touching,
axis labels crossing a data dot, year label merging with month tick — all
violate.

## text_truncation

No text container has hidden overflow content. If text would wrap or
clip, shorten the text or widen the container.

## contrast_failure

Text contrast against effective background ≥ 4.5:1 (WCAG AA). Mark
contrast ≥ 3:1. Computed colors only — not the declared variable.

## font_size_too_small

Every rendered text element ≥ 10px display size. Account for SVG
viewBox downscale — a `font-size: 11px` inside a 360-wide viewBox shown
at 180px is effectively 5.5px, which fails.

## overflow

Body, page container, figures, and tables have `scrollWidth ≤ clientWidth`
at every viewport.

## responsive_break

At mobile viewport (375px), `document.documentElement.scrollWidth ≤ 375`.
No horizontal scroll under any normal interaction.

## chartjunk_decorative_css

No `box-shadow`, `text-shadow`, gradient `background`, or 3D `transform`
on data marks, axes, or chart elements. Decoration that does not encode
data is forbidden.

## hidden_mark

Every data mark has computed `width ≥ 2px`, `height ≥ 2px`, and
`opacity ≥ 0.3`. Marks invisible to a casual reader violate.

## token_compliance

Every CSS property in the `color | background | border | fill | stroke
| font-size | font-family | padding | margin | gap | border-radius`
family resolves to a `var(--...)` reference, not a literal hex or px
value. The `:root` block is exempt.

---

## missing_range_frame

Axes terminate at data extent, not arbitrary round numbers. If the data
range is 12–87, the axis runs from 12 to 87, not 0 to 100. Subjective
judgment — confirmed by LLM-judge.

## insufficient_data_ink

Every visible element earns its place. Erasing any element loses data
information. Heavy gridlines, decorative borders, redundant labels
violate. Subjective judgment — confirmed by LLM-judge.

## comparison_failure

The chart enables the comparison its labels imply. A "vs" or "before/
after" framing demands visible alignment. Subjective judgment.

## hierarchy_failure

Primary data dominates secondary elements visually. Axes recede; data
projects forward. Subjective judgment.

## chartjunk_subjective

Visual decoration competing with evidence beyond CSS-detectable patterns.
Decorative icons, clip art, redundant illustrations, ornamental
typography. Subjective judgment.

## missing_direct_label

When a legend can be replaced by a direct label, the direct label is
preferred. Charts with two or more colors and a legend in the corner
that could instead label lines directly violate. Subjective judgment.

## orphan_widow

No heading, lede, annotation, caption, or footer ends with a final line
shorter than 25% of the block's measure. A single word, date, or short
phrase stranded on its own line is a violation. The drafter applies
`text-wrap: balance` to short prose blocks; the LLM-judge confirms no
visible stranding. Subjective judgment — confirmed by LLM-judge.
