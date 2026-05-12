# Prompt — Extract jobs from an interview transcript

**Purpose:** Read one customer interview transcript and emit a list of
candidate job statements with cited evidence.

## Input contract

The model receives a markdown transcript with these properties:

- Speakers labeled (e.g., `**Interviewer:**`, `**Customer:**`)
- Date and source ID in the file or in YAML frontmatter
- One interview per file
- May include time-stamps, may include moderator notes

## Output contract

A JSON array of candidate job objects matching `schemas/jtbd-statement.json`,
with these v0 simplifications acceptable at extraction stage:

- `id` may be temporary (`JOB-TMP-001`); final IDs assigned during clustering
- `dimensions.emotional` and `dimensions.social` may be `null` if not voiced
- `outcome_statements` may be empty at extraction stage
- `evidence` must contain ≥1 entry per job, each with a verbatim quote

## Procedure

1. Read the entire transcript end to end before extracting anything.
2. Highlight customer turns only. Ignore interviewer turns except for the
   question that triggered the customer's response.
3. For each customer turn, ask:
   - Did the customer describe a triggering situation? (context slot)
   - Did the customer describe an action they wanted to take? (motivation slot)
   - Did the customer describe progress they wanted to make? (outcome slot)
4. If all three slots are present in or adjacent to a single passage, draft a
   job statement.
5. For each draft, attach the verbatim quote (or quotes) as evidence.
6. Tag dimensions (functional always; emotional/social only if voiced).
7. Reject candidates that fail `references/job-statement-grammar.md` rules.

## Worked example

### Input fragment

> **Customer:** Honestly, the worst part of my week is Friday afternoon. We
> close the books and I have to chase six different people to confirm their
> expenses are submitted. Half of them are on Slack, half are in email, two of
> them will only respond if I walk to their desk. By the time I've got
> everyone, it's 6pm and I'm exhausted and I still don't know if I missed
> someone.

### Output (one candidate job)

```json
{
  "id": "JOB-TMP-001",
  "label": "Close the books on Friday without chasing",
  "context": "When closing the books on Friday afternoon and waiting on expense submissions from six teammates across Slack, email, and in person",
  "motivation": "confirm every expense is submitted in one consolidated view",
  "outcome": "I can finish the week's close before 6pm without wondering if I missed someone",
  "evidence": [
    {
      "source_id": "interview-<file>",
      "role": "<role-if-known>",
      "date": "<date-from-frontmatter>",
      "quote": "Honestly, the worst part of my week is Friday afternoon. We close the books and I have to chase six different people to confirm their expenses are submitted...",
      "confidence": "high"
    }
  ],
  "confidence": "low",
  "dimensions": {
    "functional": "Reduce the time to confirm all expense submissions on close day",
    "emotional": "Avoid the exhaustion and uncertainty of Friday-evening close",
    "social": null
  }
}
```

Aggregate confidence starts at `low` for a single-source extraction; the
clusterer raises it when evidence accumulates.

## Negative example

### Input fragment

> **Customer:** Yeah, I think the dashboard could be better. Like, faster
> maybe? I don't know, it's fine I guess.

### Output

```
(no job emitted)
```

Reason: no triggering context, no specific motivation, no observable outcome.
"Faster dashboard" is a feature wish, not a job. Skipping.

## Edge cases

| Situation | Handling |
|---|---|
| Customer describes a workaround | Capture as `hire_fire.fires` candidate; the job is the progress they sought |
| Customer describes a feeling but no situation | Hold as a dimension candidate, not a job |
| Customer answers "no" or "doesn't matter" | Record as anti-evidence — useful for verdict step |
| Multiple jobs tangled in one passage | Split into multiple candidates; clusterer will dedupe |
| Customer quotes another person | Tag the source_id with `(secondhand)` and downgrade confidence to low |

## Verification before returning output

- Every candidate has all three slots
- Every candidate has ≥1 verbatim evidence quote
- No candidate names the proposed product or feature
- No candidate uses banned phrases from `job-statement-grammar.md`
