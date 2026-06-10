---
name: tufte-love
description: >
  Use when designing, reviewing, or refactoring data visualizations,
  dashboards, charts, tables, maps, reports, product metrics views, or
  quantitative UI — including when a user calls one cluttered, busy, ugly,
  confusing, or hard to read, asks to simplify or clean it up, or wants
  chart component code reviewed. Activate on 'tufte audit', 'redesign this
  chart', 'data viz review', 'dashboard review', or '/tufte-love'. Not for
  decorative illustration, branding, or non-quantitative UI polish.
---

# Tufte Love

## Purpose

Create, critique, and improve quantitative displays: charts, dashboards, tables, maps, reports, product analytics UI, and the code that renders them.

Do **not** use it for decorative illustration, generic UI polish, or branding unless the design contains quantitative information.

## Core Rule

A data graphic succeeds when it communicates complex ideas with clarity, precision, and efficiency. It must show the data, tell the truth about the data, enable comparison, reveal structure and outliers, spend ink on evidence, and avoid decoration that competes with evidence.

See `references/tufte-principles.md` — including its Hard Standards section, the pass/fail constraints every graphic must meet.

---

## Operating Mode

When invoked, follow this sequence:

### 1. Identify the analytical job

Before touching the design or code, determine: the question the graphic answers, the reader, the decision it supports, the variables present, the comparisons that matter, the unit of analysis, and the time/space/category/relationship structure.

If the question is unclear, state the ambiguity and propose a better framing.

### 2. Inspect the current visual encoding

Check: chart type, axes and scales, labels and annotations, data density, color, gridlines and borders, legends, sorting, small multiples, outlier and missing-data handling, responsiveness, accessibility — and whether the graphic lies through distortion, truncation, aggregation, or decoration.

### 3. Diagnose failure modes

Classify each issue with a failure code (`data_truth_failure`, `chart_type_failure`, ...). The full 11-code taxonomy — one-line definitions plus the rubric dimension each maps to — is in `references/audit-rubric.md`.

### 4. Recommend the simplest stronger form

Replace weak patterns with stronger ones (pie → sorted dot plot, gauge → bullet chart, dual-axis → indexed lines or small multiples). Chart-selection rules, prefer/avoid lists, and the full replacement table are in `references/chart-patterns.md`.

### 5. Rewrite the design or code

When modifying code: preserve data integrity, separate data transformation from rendering, make scale decisions explicit, and keep accessibility intact.

When writing design feedback: be direct, name the failure, explain why it matters, give the better replacement, and prioritize fixes by decision impact.

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
- Color: [1-5] — [reason]
- Formatting: [1-5] — [reason]
- Recommended next change: [single highest-leverage fix]
- Confidence: [High / Medium / Low]
```

A multi-chart dashboard gets ONE audit block for the surface, with per-chart findings listed under it; add a per-chart block only when the user asks for depth.

---

## Output Formats

Three response templates — design critique, code review, and new-visualization plan — live in `references/output-formats.md`. Each ends with the step-6 audit block.

## Composition

Use the reference files when deeper guidance is needed:

- `references/tufte-principles.md` — core theory, principles, and hard standards.
- `references/audit-rubric.md` — scored audit checklist and failure-code taxonomy.
- `references/chart-patterns.md` — chart selection and replacement patterns.
- `references/output-formats.md` — response templates per mode.
- `references/color-palette.md` — default palettes (Okabe-Ito, viridis, ColorBrewer), color rules, accessibility checks.
- `references/chart-rules-extras.md` — number formatting, typography, time axes, mobile/responsive, interaction, and the publishability gate.
