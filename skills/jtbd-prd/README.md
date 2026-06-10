# jtbd-prd

Validate customer need before you build. Produces a **Job Article** that
functions as PRD framing, grounded in Jobs-to-be-Done evidence.

## What it does

Takes customer interviews, support tickets, sales calls, surveys, or existing
artifacts. Extracts candidate jobs, clusters duplicates, scores confidence,
and emits a single canonical Job Article that any subsequent PRD must
reference.

Three modes: **discovery** (raw inputs → jobs), **validation** (hypothesis →
gather evidence and run discovery, or verdict = unvalidated with concrete
next actions), **reverse** (artifact → inferred jobs, must be confirmed by
real research).

## When to use

Before writing a PRD, scoping a feature, or answering "should we build
this?" Auto-suggests when you paste a build proposal without evidence.

## Output

A Job Article with seven fixed sections, from primary job statement through
verdict, written as `job-article-<short-slug>.md`.

## Verdict gates

validated → PRD, scoping, design · under-evidenced → close the evidence gap
first · unvalidated → pivot or kill.

## Install

```bash
claude plugin marketplace add infolog-io/skills
claude plugin install jtbd-prd@infolog-io
```

## Triggers

`JTBD` · `jobs to be done` · `/jtbd-prd` · `validate this` ·
`should I build this` · `reverse JTBD` · `analyze these interviews` ·
`turn these transcripts/tickets into requirements`
