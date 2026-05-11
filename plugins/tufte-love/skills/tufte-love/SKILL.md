---
name: tufte-love
description: >
  Use this skill when designing, reviewing, or refactoring data visualizations,
  dashboards, analytical graphics, reports, charts, maps, product metrics views,
  or quantitative UI surfaces. Applies Tufte-style graphical excellence:
  show the data, maximize meaningful comparison, reduce non-data ink, preserve
  statistical truth, increase useful density, and make complex ideas clear.
  Activate with 'tufte audit', 'redesign this chart', 'data viz review', or '/tufte-love'.
---

# Tufte Love

## Purpose

This skill helps Claude Code create, critique, and improve quantitative displays.

Use it for:

- Data visualization components
- Dashboards and metric surfaces
- Charts, tables, maps, timelines, and analytical infographics
- Before/after visualization refactors
- Product analytics UI
- Executive reporting views
- Data-rich landing page graphics
- Code reviews involving chart libraries

Do **not** use it for decorative illustration, generic UI polish, or branding unless the design contains quantitative information.

## Core Rule

A data graphic succeeds when it communicates complex ideas with clarity, precision, and efficiency.

The graphic must:

1. Show the data.
2. Tell the truth about the data.
3. Enable comparison.
4. Reveal structure, causality, outliers, or change.
5. Use space and ink in service of evidence.
6. Avoid decoration that competes with evidence.

See `references/tufte-principles.md`.

---

## Operating Mode

When invoked, follow this sequence:

### 1. Identify the analytical job

Before touching the design or code, determine:

- What question is the graphic answering?
- Who is reading it?
- What decision should it support?
- What variables are present?
- What comparisons matter?
- What is the unit of analysis?
- What time, space, category, or relationship structure exists?

If the question is unclear, state the ambiguity and propose a better framing.

### 2. Inspect the current visual encoding

Check:

- Chart type
- Axes and scales
- Labels and annotations
- Data density
- Use of color
- Gridlines and borders
- Legends
- Sorting
- Small multiples
- Outlier handling
- Missing-data handling
- Responsiveness
- Accessibility
- Whether the graphic lies through distortion, truncation, aggregation, or decoration

### 3. Diagnose failure modes

Classify issues using this taxonomy:

- `data_truth_failure`
- `comparison_failure`
- `density_failure`
- `labeling_failure`
- `chart_type_failure`
- `scale_failure`
- `decoration_failure`
- `interaction_failure`
- `accessibility_failure`
- `narrative_failure`
- `implementation_failure`

### 4. Recommend the simplest stronger form

Prefer:

- Direct labels over legends
- Small multiples over overloaded single charts
- Tables for exact lookup
- Lines for time-series
- Scatterplots for relationships
- Maps only when geography is analytically meaningful
- Slopegraphs for before/after comparisons
- Dot plots over bars when precise comparison matters
- Sparklines or compact timelines for dense temporal views
- Annotation where interpretation depends on context

Avoid:

- 3D charts
- Exploded pies
- Gratuitous gradients
- Oversized legends
- Decorative icon arrays
- Truncated axes without explicit warning
- Dual-axis charts unless unavoidable and clearly labeled
- Chartjunk that increases cognitive load

See `references/chart-patterns.md`.

### 5. Rewrite the design or code

When modifying code:

- Preserve data integrity.
- Prefer semantic chart abstractions.
- Separate data transformation from rendering.
- Make scale decisions explicit.
- Add comments only where they clarify non-obvious analytical decisions.
- Use accessible labels and keyboard-readable summaries.
- Ensure responsive behavior does not destroy comparison.

When writing design feedback:

- Be direct.
- Name the failure.
- Explain why it matters.
- Give the better replacement.
- Prioritize fixes by decision impact.

### 6. Produce a final audit

Always end with:

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

---

## Output Formats

### For design critique

Use:

```md
## BLUF

[One-sentence diagnosis.]

## What is working

- ...

## What is failing

| Issue | Why it matters | Fix |
|---|---|---|
| ... | ... | ... |

## Recommended redesign

- Primary chart:
- Secondary chart:
- Labels:
- Annotations:
- Interaction:
- Responsive behavior:

## Tufte Love Audit

[Use the format block from Operating Mode step 6.]
```

### For code review

Use:

```md
## BLUF

[One-sentence engineering/design diagnosis.]

## Code-level issues

| File / component | Issue | Fix |
|---|---|---|
| ... | ... | ... |

## Visualization issues

| Issue | Risk | Fix |
|---|---|---|
| ... | ... | ... |

## Suggested implementation

[Patch, component rewrite, or pseudocode.]

## Tufte Love Audit

[Use the format block from Operating Mode step 6.]
```

### For generating a new visualization

Use:

```md
## Visualization plan

- User question:
- Decision supported:
- Data fields:
- Recommended chart:
- Why this chart:
- Encoding:
- Labels:
- Annotations:
- Interaction:
- Failure modes to avoid:

## Implementation

[Code or component.]

## Tufte Love Audit

[Use the format block from Operating Mode step 6.]
```

---

## Hard Standards

The graphic must not:

- Hide the denominator.
- Confuse correlation with causation.
- Use area or volume to encode linear values unless mathematically correct.
- Make decorative elements more prominent than data.
- Require a legend when direct labeling is feasible.
- Use color as the only channel for meaning.
- Remove context needed to interpret the trend.
- Aggregate away the important variation.
- Use a map when the geography is irrelevant.
- Use animation where a static comparison would be clearer.

The graphic should:

- Expose comparisons quickly.
- Put labels near the evidence.
- Use consistent scales across comparable panels.
- Preserve outliers unless there is a stated analytical reason.
- Show uncertainty when uncertainty matters.
- Support both overview and detail.
- Treat white space as structure, not filler.
- Make the important thing visually inevitable.

---

## Composition

Use the reference files when deeper guidance is needed:

- `references/tufte-principles.md`
  - Core theory and principles.
- `references/audit-rubric.md`
  - Scored audit checklist.
- `references/chart-patterns.md`
  - Chart selection and replacement patterns.
