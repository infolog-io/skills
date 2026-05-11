# Job Article: {{short_job_label}}

> **Status:** {{verdict}} · **Confidence:** {{confidence}} · **Last updated:** {{date}}

## Primary Job Statement

When {{context}}, the user wants to {{motivation}}, so they can {{outcome}}.

## Evidence

| # | Source | Role | Date | Quote | Confidence |
|---|---|---|---|---|---|
| 1 | {{source_id}} | {{role}} | {{date}} | "{{quote}}" | {{q_confidence}} |
| 2 | {{source_id}} | {{role}} | {{date}} | "{{quote}}" | {{q_confidence}} |
| 3 | {{source_id}} | {{role}} | {{date}} | "{{quote}}" | {{q_confidence}} |

**Total:** {{n_quotes}} quotes across {{n_sources}} sources, {{n_roles}} distinct roles.

## Job Dimensions

- **Functional:** {{functional_outcome}}
- **Emotional:** {{emotional_outcome | "not-yet-evidenced"}}
- **Social:** {{social_outcome | "not-yet-evidenced"}}

## Outcome Statements (Ulwick form)

1. {{Minimize|Increase|Reduce}} the {{unit_of_measure}} {{object_of_control}} {{contextual_clarifier}}
2. {{Minimize|Increase|Reduce}} the {{unit_of_measure}} {{object_of_control}} {{contextual_clarifier}}
3. {{Minimize|Increase|Reduce}} the {{unit_of_measure}} {{object_of_control}} {{contextual_clarifier}}

## Underserved vs. Overserved

**Underserved (high importance, low satisfaction):**
- {{what_customer_struggles_with}}
- {{what_current_solutions_miss}}

**Overserved (low importance, high satisfaction):**
- {{what_current_solutions_overdeliver_on}}

## Hire / Fire

- **Fires:** {{current_workaround_or_product_being_replaced}}
- **Hires:** {{new_solution_being_adopted}}
- **Trigger:** {{moment_of_progress_that_caused_the_swap}}

## Build Implication (PRD framing)

The build that inherits this article must:

- Address outcome statements: {{outcome_indexes}}
- Avoid expanding into: {{overserved_area}}
- Be measurable against: {{success_metric_tied_to_outcome}}
- Honor this constraint from evidence: "{{verbatim_quote_that_must_not_be_violated}}"

## Verdict

- [ ] **Validated** — proceed to PRD
- [ ] **Under-evidenced** — return when confidence ≥ medium across ≥3 sources
- [ ] **Unvalidated** — do not build; pivot or kill

## Next research (if under-evidenced)

- {{question_to_ask}} — ask {{whom_to_ask}}
- {{question_to_ask}} — ask {{whom_to_ask}}

## Revision history

- {{date}}: Initial draft from {{n_sources}} sources, verdict = {{verdict}}
