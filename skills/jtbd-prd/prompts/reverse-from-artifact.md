# Prompt — Reverse jobs from an existing artifact

**Purpose:** Given an existing artifact (PRD, landing page, doc, competitor
page), infer which jobs it implicitly serves. Output is **always tagged as
inferred** and never counted as customer evidence.

## Input contract

One of:

- A URL (which will be fetched)
- A pasted markdown or HTML document
- A pasted screenshot transcribed to text

## Output contract

Array of candidate job objects with two mandatory differences from
forward-mode extraction:

- Every evidence entry has `source_id` prefixed `inferred:` (e.g.,
  `inferred:landing-page-2026-05-12`)
- Every evidence entry has `confidence: "low"` regardless of how confident the
  reading feels
- Overall `confidence: "low"` always

The Job Article that consumes this output must include this banner:

```
> NOTE: This article was reverse-derived from an existing artifact.
> Jobs are inferred, not evidenced from customer sources.
> Treat as hypotheses to validate, not conclusions.
```

## Why this mode exists

Three legitimate use cases:

1. **Audit your own existing build** — does the artifact serve a coherent job?
2. **Competitive teardown** — what jobs does a competitor implicitly target?
3. **Hypothesis bootstrapping** — generate candidate jobs that real research can
   confirm or reject.

Never use reverse mode to skip research. The output is a starting point for
interviews, not a substitute for them.

## Procedure

1. Read the entire artifact end to end.
2. List the actions the artifact asks the customer to take.
3. For each action, ask: "What progress would someone be trying to make for
   this action to be valuable?"
4. Draft the job statement with all three slots, using the artifact's own
   language where possible.
5. Cite the verbatim text that hints at each inferred slot.
6. Flag any slot you had to invent without textual support.

## Worked example

### Input fragment

> Tired of stale pull requests? PRBuddy automatically pings the right
> reviewer based on file ownership and past review history. Get back to
> shipping in under 24 hours.

### Output

```json
{
  "id": "JOB-TMP-003",
  "label": "Move stale PRs without manual chasing",
  "context": "When a pull request has been waiting for review long enough that the engineer is blocked from shipping",
  "motivation": "get the right reviewer engaged without manually pinging or guessing who has context",
  "outcome": "the engineer can return to shipping within a working day",
  "evidence": [
    {
      "source_id": "inferred:prbuddy-landing-2026-05-12",
      "role": null,
      "date": "2026-05-12",
      "quote": "Tired of stale pull requests? PRBuddy automatically pings the right reviewer based on file ownership and past review history. Get back to shipping in under 24 hours.",
      "confidence": "low"
    }
  ],
  "confidence": "low",
  "dimensions": {
    "functional": "Reduce the time a pull request waits for the first useful review",
    "emotional": "Avoid the frustration of being blocked on someone else's queue",
    "social": null
  }
}
```

Social dimension left null — no textual hint that other people's perception
matters in this artifact.

## Negative example

### Input fragment

> Welcome to FrobCorp. We make great software.

### Output

```
(no job emitted)
```

Reason: no action verb, no friction named, no progress implied. Marketing
copy that names no job cannot reverse-derive one.

## Edge cases

| Situation | Handling |
|---|---|
| Artifact lists many features | Group into 1–3 dominant jobs; do not emit one job per feature bullet |
| Artifact is a competitor's PRD | Same procedure; tag `source_id: inferred:competitor-<name>` |
| Artifact is your own existing PRD | Useful — exposes whether the PRD has a real job underneath |
| Artifact contradicts itself | Emit each contradictory job separately; the conflict is itself a finding |
| Artifact contains a customer quote | Use as evidence at `confidence: low`, but tag `secondhand: true` |

## Output destination

When reverse mode is the only mode used in a session, the resulting Job
Article must include a `## Status` line:

```
> Status: under-evidenced — derived from artifact only.
> Required next step: validate with ≥3 customer sources before issuing a verdict.
```

The verdict is **never** `validated` from reverse mode alone.

## Verification before returning output

- Every candidate has `inferred:` prefix on `source_id`
- Every candidate has `confidence: low`
- Output Job Article (downstream) gets the inferred-mode banner
- No customer quotes are claimed unless they appear in the artifact
