# tufte-love

A data-visualization auditor grounded in Edward Tufte's principles of
graphical excellence. Audits charts, dashboards, reports, maps, and any
quantitative UI surface; emits a 9-dimension scored audit with the
highest-leverage fix.

## Why

Charts lie quietly. Pies hide ranking. Dual axes invent correlation.
Decoration competes with data. This skill catches the failures and
prescribes the simpler stronger form.

## When to use

- Designing or reviewing a chart, dashboard, or analytical UI
- Auditing a report before publication
- Reviewing code that produces visualizations
- Before shipping any surface that displays numbers

## When not to use

- Decorative illustration without quantitative content
- Generic UI polish (use a different skill)

## What you get

A 9-dimension audit: data truth, comparison quality, density, labeling,
visual noise, chart-type fit, interaction, color, and formatting. Each
scored 1–5 with a reason and one recommended next change.

## Install

```bash
claude plugin marketplace add infolog-io/skills
claude plugin install tufte-love@infolog-io
```

## Triggers

`tufte audit` · `redesign this chart` · `data viz review` · `/tufte-love`
