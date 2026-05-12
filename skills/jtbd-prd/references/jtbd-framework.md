# JTBD Framework — Christensen + Ulwick distillation

## Two parents, one skill

This skill blends two strands of Jobs-to-be-Done thinking.

**Clayton Christensen — "hire/fire"**: customers do not buy products; they hire
them to make progress in a specific context. When a product no longer makes
progress, they fire it.

**Tony Ulwick — outcome-driven innovation**: jobs decompose into measurable
desired outcomes, phrased as "minimize/increase/reduce X under Y conditions."

We default to Ulwick's outcome form because it is extractable from text and
testable. We keep Christensen's hire/fire as a sanity check: if you cannot
name what the customer is firing, the job is not yet real.

## The shape of a job statement

```
When [situation / trigger / context],
I want to [motivation — verb + object],
so I can [expected outcome / progress made].
```

A job is **not** a feature, not a persona, not a use case.

| Confusion | Why it fails |
|---|---|
| "Salesforce admins want a better dashboard" | persona + feature, no progress |
| "Users want faster search" | feature, no situation |
| "Mobile users want offline mode" | feature + segment, no outcome |
| "When traveling, I want to access docs offline, so I can keep working on a plane" | valid job statement |

## Outcome statements (Ulwick form)

Every job decomposes into 5–15 desired outcomes. Each outcome follows this
strict shape:

```
[Direction verb] the [unit of measure] [object of control] [contextual clarifier]
```

Direction verbs (allowed list):
- **Minimize** the time / effort / risk / cost
- **Increase** the likelihood / accuracy / frequency
- **Reduce** the variability / friction / surprise

Examples:

- Minimize the time it takes to find the right reviewer for a code change
- Increase the likelihood that the first reviewer assigned has relevant context
- Reduce the variability of review turnaround time across teams

Outcomes are **prioritized** by importance and satisfaction:

- **Underserved** (high importance, low satisfaction) = opportunity
- **Overserved** (low importance, high satisfaction) = waste
- **Appropriately served** (balanced) = leave alone

## Hire / fire sanity check

For any proposed job, the model must answer:

1. What product/process/workaround does the customer fire when they adopt the new solution?
2. What product/process/workaround does the customer hire?
3. What is the moment of progress that triggers the swap?

If any of the three are unknown, the job is **under-evidenced**, not
validated.

## Anti-patterns

| Pattern | Why it fails |
|---|---|
| Demographic jobs ("teens want…") | demographics are not contexts |
| Tech jobs ("API users want…") | technology is not a job |
| Solution-jobs ("users want our product to…") | circular — describes adoption, not progress |
| Aspiration without context ("be productive") | not measurable, not falsifiable |
| Single-quote inference | one customer is anecdote, not evidence |

## When to escalate to research

If the model cannot find ≥3 quotes across ≥2 sources for any proposed job, do
not invent jobs. Emit a `next-research.md` listing what to ask and whom to ask.

## Reading list (not read by the skill — for the author)

- Christensen et al., *Competing Against Luck*
- Ulwick, *Jobs to be Done: Theory to Practice*
- Strategyn Outcome-Driven Innovation primer
- Bob Moesta on switch interviews
