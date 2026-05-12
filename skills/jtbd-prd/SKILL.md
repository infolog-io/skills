---
name: jtbd-prd
description: >
  Validate customer need before any build. Use when about to design, code, ship,
  or scope a feature, product, page, or skill. Gathers evidence from interviews,
  tickets, sales calls, surveys, and artifacts; clusters jobs; scores confidence;
  emits a Job Article that frames the upcoming build as a Jobs-to-be-Done PRD.
  Activates on "JTBD", "jobs to be done", "validate this", "should I build this",
  "is there a real need", "what job does this serve", or "/jtbd-prd". Also
  auto-suggests when the user pastes a build proposal, feature brief, or
  hypothesis without supporting evidence.
---

# jtbd-prd

## Purpose

Sit upstream of every build. Block work that lacks customer evidence. Produce a
single canonical artifact — the **Job Article** — that any subsequent PRD,
spec, or implementation must reference.

Inspired by Christensen's "hire/fire" framing and Tony Ulwick's outcome-driven
phrasing. Defaults to Ulwick form because it is measurable and easier to
extract from raw text.

## When to activate

Activate when the user is about to:

- Build a new feature, product, page, or skill
- Write a PRD or spec
- Pivot or expand an existing build
- Ask "should we build this?" or "is there demand for X?"
- Validate a hypothesis with customer evidence
- Reverse-derive jobs from existing copy, docs, or competitor artifacts

Do not activate for:

- Tactical execution work where the job is already validated
- Pure code refactors with no product-facing change
- Internal tooling with a single known user (the user is the researcher)

## Inputs accepted

| Input type | Format | Example |
|---|---|---|
| Customer interview | Markdown transcript | `interview-2026-04-03-acme-corp.md` |
| Support tickets | Markdown or JSON dump | exported Intercom / Zendesk thread |
| Sales call notes | Markdown | win/loss debrief |
| Survey free-text | CSV column or markdown list | NPS response open-ends |
| Existing artifact (reverse mode) | URL, markdown, or pasted text | published page, competitor PRD |
| Build hypothesis | One-sentence statement | "We want to build X for Y users" |

## Output: the Job Article

A single markdown file conforming to `templates/job-article.md` and
`schemas/job-article.json`. Functions as PRD framing — the build that follows
must reference this article.

Sections in fixed order:

1. **Primary Job Statement** — When… I want to… so I can…
2. **Evidence** — table of quotes with source, role, date, confidence
3. **Job Dimensions** — functional, emotional, social
4. **Outcome Statements** — Ulwick form: minimize/increase/reduce X
5. **Underserved vs. Overserved** — where current solutions fail or overreach
6. **Build Implication** — what the next build must do and avoid
7. **Verdict** — validated / under-evidenced / unvalidated

## Flow

```
1. Identify mode:
   - discovery (raw inputs → jobs)
   - validation (build hypothesis → check against evidence)
   - reverse (existing artifact → inferred jobs)

2. Run the appropriate extractor:
   - prompts/extract-from-interview.md
   - prompts/extract-from-tickets.md
   - prompts/reverse-from-artifact.md

3. Cluster + score:
   - prompts/cluster-and-score.md

4. Render Job Article:
   - templates/job-article.md

5. Issue verdict:
   - prompts/verdict.md
```

## Trigger phrases

| Phrase | Mode |
|---|---|
| "JTBD", "jobs to be done", "/jtbd-prd" | Discovery (default) |
| "validate this", "should I build this", "is there a real need" | Validation |
| "what job does this serve", "reverse JTBD" | Reverse |
| "extract jobs from these interviews" | Discovery |
| user pastes build proposal without evidence | Auto-suggest validation |

## References

- `references/jtbd-framework.md` — Christensen + Ulwick distillation
- `references/job-statement-grammar.md` — the canonical shape
- `references/dimension-tagger.md` — functional / emotional / social rules
- `references/prd-framing.md` — how the Job Article seeds a PRD

## Verdict thresholds

| Confidence | Rule |
|---|---|
| high | ≥5 sources, ≥2 distinct roles, ≥1 measurable outcome |
| medium | ≥3 sources, ≥3 quotes |
| low | <3 sources or single role only |

| Verdict | Rule |
|---|---|
| validated | confidence ≥ medium AND outcome statements measurable |
| under-evidenced | confidence = low OR outcomes ambiguous |
| unvalidated | no customer evidence OR build hypothesis contradicts evidence |

## Output destination

By default, write the Job Article to the working directory the user is in,
named `job-article-<short-slug>.md`. If the working directory is a repo, place
in `docs/jtbd/` if that directory exists; otherwise repo root.

Never write to the infolog-skills repo itself unless explicitly asked.
