# jtbd-prd

Validate customer need before you build. Produces a **Job Article** that
functions as PRD framing, grounded in Jobs-to-be-Done evidence.

## What it does

Takes customer interviews, support tickets, sales calls, surveys, or existing
artifacts. Extracts candidate jobs, clusters duplicates, scores confidence,
and emits a Job Article any subsequent PRD must reference.

Four modes: **discovery** (inputs → jobs), **validation** (hypothesis →
verdict), **reverse** (artifact → inferred jobs), and **workflow-automation**
(workflow → where AI can automate, via a Jidoka human-in-the-loop review).

## When to use

Before a PRD, scoping, or a pivot — or when answering "should we build
this?" Auto-suggests when you paste a build proposal without evidence.

## Output

Markdown Job Article with seven fixed sections: job statement, evidence,
dimensions, Ulwick outcomes, underserved vs. overserved, build implication,
verdict. Workflow-automation mode emits an Automation Map instead.

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
