# Prompt — Extract jobs from support tickets

**Purpose:** Read a batch of support tickets and emit candidate job
statements. Tickets differ from interviews: customers do not narrate context,
they describe friction. The extractor must reconstruct the job.

## Input contract

A markdown or JSON dump of one or more support conversations. Each conversation has:

- Ticket ID
- Subject
- Customer messages (the only signal that matters for JTBD)
- Optional: agent replies (use only to infer context, not as evidence)
- Optional: tags, dates, customer role

## Output contract

Same as `extract-from-interview.md` — array of objects matching
`schemas/jtbd-statement.json` with v0 simplifications.

## Key differences from interviews

| Interview signal | Ticket signal |
|---|---|
| Customer narrates context | Reader infers context from what broke |
| Customer states motivation explicitly | Customer states friction; motivation is reverse-engineered |
| Customer often states outcome | Outcome is implicit in what they want unstuck |
| 1 source per file | Often 1 source per ticket, many tickets per file |

## Procedure

1. Read each ticket as a unit. Do not extract until the whole conversation is read.
2. Identify the friction: what stopped working, was confusing, or was missing?
3. Reverse-engineer the context: what was the customer trying to do when they
   hit the friction?
4. Reverse-engineer the motivation: what action were they reaching for?
5. Reverse-engineer the outcome: what progress did they want?
6. Quote the verbatim text that supports each inference.
7. Mark confidence: `low` by default for ticket-derived jobs (less narrative
   than interviews); raise to `medium` if the customer's own words explicitly
   name all three slots.

## Worked example

### Input ticket

```
Subject: CSV import keeps failing at row 4,832
Customer: I'm trying to import our 2025 transactions before our audit on
Monday. The file is about 9,000 rows. Every time I import, it stops at row
4,832 with a generic error. I've checked that row — nothing weird about it.
I can't tell if anything before it actually got saved or if I need to start
from scratch each time. Please advise.
```

### Output

```json
{
  "id": "JOB-TMP-002",
  "label": "Import large historical data before a deadline",
  "context": "When importing a large historical dataset (thousands of rows) against a hard external deadline like an audit",
  "motivation": "complete the import once and verify what was actually saved when something fails partway through",
  "outcome": "I meet the deadline without losing my place or starting from scratch on every retry",
  "evidence": [
    {
      "source_id": "ticket-<id>",
      "role": "<role-if-known>",
      "date": "<date-if-known>",
      "quote": "Every time I import, it stops at row 4,832 with a generic error. I've checked that row — nothing weird about it. I can't tell if anything before it actually got saved or if I need to start from scratch each time.",
      "confidence": "medium"
    }
  ],
  "confidence": "low",
  "dimensions": {
    "functional": "Reduce the time and rework caused by partial import failures",
    "emotional": "Avoid the anxiety of an external deadline with no visibility into progress",
    "social": "Avoid being seen as the person who missed the audit deadline"
  }
}
```

Social dimension was inferred from "audit on Monday" — a reputational deadline
with stakeholders watching. Mark with confidence `low` if no explicit voicing.

## Negative example

### Input ticket

```
Subject: Login broken
Customer: Cannot log in. Please fix.
```

### Output

```
(no job emitted)
```

Reason: friction is reported but no context, motivation, or outcome can be
inferred. This is a bug report, not a job. Useful for product, useless for
JTBD.

## Volume handling

When given a batch of ≥10 tickets:

1. First pass: skim all tickets, group by surface friction theme.
2. Second pass: pick representative tickets per theme (1–3 per theme).
3. Extract jobs from representatives only. Note the theme frequency in
   `evidence_summary` later.
4. Do not extract one job per ticket — that overstates evidence diversity.

## Edge cases

| Situation | Handling |
|---|---|
| Ticket is purely a feature request | Skip — feature requests are not jobs |
| Ticket is a complaint with no action verb | Skip — capture sentiment elsewhere |
| Customer's role is visible in signature | Capture; raises social-dimension confidence |
| Ticket thread spans weeks | Use the customer's first message for context; later messages for outcome confirmation |
| Customer quotes a colleague | Tag `(secondhand)` and downgrade confidence |

## Verification before returning output

- Each candidate has all three slots, even if inferred
- Each candidate cites a verbatim quote from the customer (not the agent)
- No candidate is a 1:1 paraphrase of "fix this bug"
