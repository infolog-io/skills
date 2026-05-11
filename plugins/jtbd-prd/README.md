# jtbd-prd

Validate customer need before you build. Produces a **Job Article** that
functions as PRD framing, grounded in Jobs-to-be-Done evidence.

## What it does

Takes customer interviews, support tickets, sales calls, surveys, or existing
artifacts. Extracts candidate jobs, clusters duplicates, scores confidence,
and emits a single canonical Job Article that any subsequent PRD must
reference.

Three modes: **discovery** (raw inputs → jobs), **validation** (hypothesis +
evidence → verdict), **reverse** (artifact → inferred jobs, must be confirmed
by real research).

## When to use

Before writing a PRD, scoping a feature, pivoting an existing build, or
answering "should we build this?" Auto-suggests when you paste a build
proposal without evidence.

## Output

Markdown Job Article with seven fixed sections: primary job statement,
evidence table, dimensions (functional/emotional/social), Ulwick outcome
statements, underserved vs. overserved, build implication, and verdict.

## Verdict gates

| Verdict | Allowed downstream |
|---|---|
| validated | PRD, scoping, design |
| under-evidenced | close evidence gap first |
| unvalidated | pivot or kill |

## Install

```bash
claude plugin marketplace add infolog-io/skills
claude plugin install jtbd-prd@infolog-io
```

## Triggers

`JTBD` · `jobs to be done` · `validate this` · `should I build this` ·
`/jtbd-prd`
