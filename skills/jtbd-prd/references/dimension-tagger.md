# Dimension Tagger — functional / emotional / social

Every job has three dimensions. A statement is incomplete until each is named.

## Functional dimension

The practical, observable progress the customer is making.

Heuristic: ask "what task is getting done, and how would a stopwatch or
counter measure success?"

Examples:

- Reduce the time to find the right reviewer
- Increase the share of imports that complete on the first try
- Minimize the number of context switches during a code review

Functional outcomes are the easiest to extract from text and the easiest to
build against.

## Emotional dimension

How the customer wants to feel during or after the job.

Heuristic: ask "what feeling is the customer avoiding or seeking?"

Examples:

- Avoid the dread of opening a Monday morning with 40 stale PRs
- Feel confident the import did not silently lose data
- Stop feeling like a bottleneck on the team

Emotional outcomes are often unstated. The extractor should look for words
like "frustrating," "worried," "nervous," "proud," "embarrassed," "stuck,"
"relief," "confident," "anxious."

## Social dimension

How the customer wants to be perceived by others while doing the job.

Heuristic: ask "who is watching, and what do they want to be seen doing or
not doing?"

Examples:

- Be seen by the team as someone who unblocks others, not someone who blocks them
- Avoid asking the same question in #help-channel twice in one week
- Show the manager that I am keeping pace with the team

Social outcomes are the hardest to extract because customers rarely state
them directly. Listen for references to other people, teams, managers,
customers, communities, or to reputation, credibility, trust.

## Tagging procedure

For each extracted job:

1. Identify the functional outcome (default — every job has one)
2. Identify the emotional outcome (look for feeling words)
3. Identify the social outcome (look for references to other people)

If any dimension cannot be inferred from the evidence, mark it as
`not-yet-evidenced` rather than inventing one.

## Worked example

**Quote**: "I dread Mondays because I open Slack and see twelve pings from
people waiting on my review. Half the time I don't even know which PR they're
talking about, and I feel like everyone's stalled on me."

**Functional**: Reduce the time it takes to triage incoming review requests
on Monday morning.

**Emotional**: Avoid dread of opening Slack on Monday. Stop feeling like a
bottleneck.

**Social**: Avoid being seen by the team as the person blocking everyone's
work.

All three dimensions are present and supported by the same quote — a strong
extraction.

## Anti-patterns

| Pattern | Why it fails |
|---|---|
| Restating the feature as an emotional outcome | "feel productive" — too generic |
| Tagging social outcomes the customer did not voice | inventing audience |
| Skipping emotional because it feels "soft" | emotional is often the actual driver |
| Functional outcome with no unit of measure | "be efficient" is not measurable |

## Output format

Each Job Article must list dimensions explicitly:

```
## Job Dimensions

Functional: [outcome statement]
Emotional: [outcome statement | not-yet-evidenced]
Social: [outcome statement | not-yet-evidenced]
```

If two of three dimensions are `not-yet-evidenced`, downgrade confidence by
one level. If all three are evidenced from quotes, the job is fully formed.
