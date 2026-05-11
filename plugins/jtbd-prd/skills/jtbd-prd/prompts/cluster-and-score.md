# Prompt — Cluster candidate jobs and score confidence

**Purpose:** Take the raw candidate job list from one or more extractors,
merge duplicates, and compute aggregate confidence.

## Input contract

A flat array of candidate job objects (output of any extract-* prompt). May
contain:

- Duplicate jobs across sources
- Near-duplicates that should merge
- Jobs that only one source mentioned
- Candidates from forward mode and reverse mode mixed together

## Output contract

A deduplicated array of job objects with:

- Final `id` assignments (`JOB-001`, `JOB-002`, ...)
- Aggregated `evidence` from all merged candidates
- Recomputed aggregate `confidence` per the threshold table
- `evidence_summary` populated: `n_quotes`, `n_sources`, `n_roles`
- `related_jobs` filled where adjacent jobs are connected but distinct

## Clustering rules

Two candidates merge into one job when **all** of these are true:

1. Same triggering context (or contexts that are subsets of each other)
2. Same motivation verb-and-object family (e.g., "find a reviewer" and
   "identify the right reviewer" merge; "find a reviewer" and "ping the
   reviewer" do not)
3. Same observable outcome (or outcomes that describe the same progress at
   different granularities)

Two candidates stay separate (but mark `related_jobs`) when:

- Same context but different motivation
- Same motivation but different context
- Same outcome but different path to it

## Worked merge example

### Input

```
Candidate A (from interview-12):
  context: "When a PR has been open more than a day with no review..."
  motivation: "find someone with relevant context to look at it"
  outcome: "the PR can be merged before the standup"

Candidate B (from ticket-2841):
  context: "When a pull request is sitting unreviewed for over 24 hours..."
  motivation: "identify a teammate who knows the code"
  outcome: "the change can land in time for the team's daily sync"
```

### Output

```json
{
  "id": "JOB-001",
  "label": "Get a stale PR reviewed before the next standup",
  "context": "When a pull request has been open longer than a working day without review",
  "motivation": "find a teammate with relevant context to review it",
  "outcome": "the change can land before the team's next sync",
  "evidence": [
    { "source_id": "interview-12", "quote": "...", "confidence": "high" },
    { "source_id": "ticket-2841", "quote": "...", "confidence": "medium" }
  ],
  "confidence": "low",
  "evidence_summary": { "n_quotes": 2, "n_sources": 2, "n_roles": 1 }
}
```

Aggregate confidence is `low` despite two sources because both quotes came
from engineers (1 role). Confidence thresholds require ≥2 distinct roles for
medium.

## Confidence thresholds (apply after merging)

| Evidence pattern | Confidence |
|---|---|
| ≥5 sources AND ≥2 distinct roles AND ≥1 measurable outcome quote | high |
| ≥3 sources AND ≥3 quotes | medium |
| <3 sources OR single role only | low |

Reverse-mode evidence does **not** count toward confidence calculation. It
appears in the evidence table but is filtered before threshold evaluation.

## Outcome statement synthesis

After merging, draft 3–7 Ulwick-form outcome statements per job. Each must:

- Start with `Minimize`, `Increase`, or `Reduce`
- Name a unit of measure (time, count, percentage, variability, etc.)
- Name the object of control (the thing being moved)
- Include a contextual clarifier where useful

Pull units of measure from the customer's own language where possible. "Get
back to shipping in under 24 hours" → unit_of_measure = "time", value frame =
"within a working day."

## Underserved / overserved tagging

For each job:

- **Underserved:** what the evidence shows customers struggling with most.
  Quote-backed. Becomes the build's opportunity.
- **Overserved:** what current solutions (including yours) already handle
  well or over-deliver on. Becomes the build's anti-goal.

If evidence does not name overserved areas, leave the section empty rather
than inventing one.

## Anti-evidence handling

Some quotes will be **anti-evidence** — explicit signals that the job is not
real for that customer. Examples:

- "Honestly it's not a big deal, we just live with it."
- "We tried that and it didn't help."
- "I wouldn't pay for that."

Anti-evidence does not erase a job, but it must appear in the evidence table
with `confidence: "low"` and a note. If anti-evidence outnumbers
pro-evidence, the verdict step will downgrade.

## Verification before returning output

- Every merged job retains its full evidence list
- No evidence is dropped during the merge
- Confidence is computed from the threshold table, not vibes
- `related_jobs` list is symmetric (A → B implies B → A)
