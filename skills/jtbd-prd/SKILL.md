---
name: jtbd-prd
description: 'Use when the user is about to build, scope, or write a PRD or spec for a feature, product, page, or skill and customer need is unproven. Activates on "JTBD", "jobs to be done", "/jtbd-prd", "validate this", "should I build this", "is there a real need", "what job does this serve", "reverse JTBD", "analyze these interviews", or "turn these transcripts/tickets into requirements". Also use when the user pastes a build proposal, feature brief, or hypothesis without supporting customer evidence.'
---

# jtbd-prd

## Purpose

Sit upstream of every build. Block work that lacks customer evidence. Produce
a single canonical artifact — the **Job Article** — that any subsequent PRD,
spec, or implementation must reference. Framework background lives in
`references/jtbd-framework.md`.

## When to activate

Activate when the user is about to build a new feature, product, page, or
skill; write a PRD or spec; pivot or expand an existing build; validate a
hypothesis against customer evidence; or reverse-derive jobs from existing
copy, docs, or competitor artifacts.

Do not activate for:

- Tactical execution work where the job is already validated
- Pure code refactors with no product-facing change
- Internal tooling with a single known user (the user is the researcher)

## Inputs accepted

Interview transcripts, support-ticket dumps (markdown or JSON), sales call
notes, survey free-text, existing artifacts (URL or pasted text — reverse
mode), or a one-sentence build hypothesis.

## Output: the Job Article

A single markdown file with seven fixed sections, from Primary Job Statement
through Verdict — see `templates/job-article.md` and
`schemas/job-article.json`. Job statements follow the canonical grammar in
`references/job-statement-grammar.md`.

## Flow

```
1. Identify mode from the trigger table below.

Discovery / reverse:
2. Run the matching extractor:
   - prompts/extract-from-interview.md
   - prompts/extract-from-tickets.md
   - prompts/reverse-from-artifact.md
3. Cluster + score confidence: prompts/cluster-and-score.md
4. Render Job Article: templates/job-article.md
5. Issue verdict: prompts/verdict.md

Validation (build hypothesis present):
2. Ask the user for evidence inputs: interviews, tickets, surveys, analytics.
3. Evidence exists → run discovery steps 2–5 on it, scoped to the hypothesis;
   the verdict step compares the hypothesis to the evidenced job.
4. No evidence → run prompts/reverse-from-artifact.md on the brief, then issue
   verdict = unvalidated via prompts/verdict.md with concrete next_actions
   (whom to interview, which tickets to pull).
```

## Trigger phrases

| Phrase | Mode |
|---|---|
| "JTBD", "jobs to be done", "/jtbd-prd" | Discovery (default) |
| "validate this", "should I build this", "is there a real need" | Validation |
| "what job does this serve", "reverse JTBD" | Reverse |
| "extract jobs from these interviews", "analyze these interviews" | Discovery |
| "turn these transcripts/tickets into requirements" | Discovery |
| user pastes build proposal without evidence | Auto-suggest validation |

## Scoring and verdict

Confidence is computed only from the canonical threshold table (including the
dimension-downgrade rule) in `prompts/cluster-and-score.md`. Verdict mapping
lives only in `prompts/verdict.md`. Do not restate either table elsewhere.

## References

- `references/jtbd-framework.md` — Christensen + Ulwick distillation
- `references/job-statement-grammar.md` — the canonical shape
- `references/dimension-tagger.md` — functional / emotional / social rules
- `references/prd-framing.md` — how the Job Article seeds a PRD

## Output destination

Write the Job Article to the user's working directory as
`job-article-<short-slug>.md`. If the directory is a repo and `docs/jtbd/`
exists, place it there; otherwise repo root. Never write to the
infolog-skills repo itself unless explicitly asked.
