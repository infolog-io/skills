# Output Formats

Three response templates, one per mode. Every template ends with the
canonical `Tufte Love Audit` block defined in SKILL.md step 6.

## For design critique

Use:

```md
## BLUF

[One-sentence diagnosis.]

## What is working

- ...

## What is failing

| Issue | Why it matters | Fix |
|---|---|---|
| ... | ... | ... |

## Recommended redesign

- Primary chart:
- Secondary chart:
- Labels:
- Annotations:
- Interaction:
- Responsive behavior:

## Tufte Love Audit

[Use the format block from SKILL.md Operating Mode step 6.]
```

## For code review

Use:

```md
## BLUF

[One-sentence engineering/design diagnosis.]

## Code-level issues

| File / component | Issue | Fix |
|---|---|---|
| ... | ... | ... |

## Visualization issues

| Issue | Risk | Fix |
|---|---|---|
| ... | ... | ... |

## Suggested implementation

[Patch, component rewrite, or pseudocode.]

## Tufte Love Audit

[Use the format block from SKILL.md Operating Mode step 6.]
```

## For generating a new visualization

Use:

```md
## Visualization plan

- User question:
- Decision supported:
- Data fields:
- Recommended chart:
- Why this chart:
- Encoding:
- Labels:
- Annotations:
- Interaction:
- Failure modes to avoid:

## Implementation

[Code or component.]

## Tufte Love Audit

[Use the format block from SKILL.md Operating Mode step 6.]
```
