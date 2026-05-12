# How the Job Article seeds a PRD

The Job Article is not a PRD. It is the framing layer that any PRD must
inherit. Without it, a PRD is a solution in search of a problem.

## The relationship

```
Job Article         →   PRD                     →   Implementation
(why customer       (what we will build         (how it gets built)
 needs anything)     to serve the job)
```

A Job Article answers "is there a real need?" A PRD answers "given that need,
what exactly are we building, for whom, with what tradeoffs?" If a PRD does
not reference an upstream Job Article, the build is unvalidated by default.

## What the PRD inherits

Every section of the Job Article maps to a constraint or input the PRD must
honor.

| Job Article section | PRD inherits |
|---|---|
| Primary Job Statement | Problem statement |
| Evidence | Validation appendix; cited in scope discussions |
| Job Dimensions | Acceptance criteria — must address functional + at least one of emotional/social |
| Outcome Statements | Success metrics — at least one PRD metric must map to an outcome statement |
| Underserved | In-scope opportunity |
| Overserved | Anti-goals; do-not-build list |
| Build Implication | Solution scoping constraints |
| Verdict | Gate — only validated jobs proceed to PRD |

## Inversion check

Before writing a PRD, the author must be able to answer:

1. Which outcome statement is the build trying to move?
2. By how much, measured how?
3. What overserved area must the build avoid expanding into?
4. What evidence quote would the build fail if it ignored?

If any answer is "I don't know," return to the Job Article and close the gap.

## How the verdict gates downstream work

| Verdict | PRD allowed? | What to do next |
|---|---|---|
| validated | Yes | Write the PRD, reference this article |
| under-evidenced | No | Run `next-research.md` items until verdict reaches medium |
| unvalidated | No | Pivot or kill — do not write a PRD against this hypothesis |

## Where Job Articles live

Default: in the repo where the build will happen, under `docs/jtbd/`.

| Repo type | Path |
|---|---|
| Has `docs/` directory | `docs/jtbd/job-<slug>.md` |
| Has `notes/` directory | `notes/jtbd/job-<slug>.md` |
| No conventional location | repo root: `job-<slug>.md` |

Filename slug should be 3–5 words describing the customer's job, not the
proposed solution. Good: `triage-stale-prs.md`. Bad: `review-dashboard.md`.

## Versioning Job Articles

When customer evidence updates, the article should be revised, not replaced.

Add a `## Revision history` section:

```
## Revision history
- 2026-05-12: Initial draft from 5 interviews, verdict = under-evidenced
- 2026-05-18: Added 3 ticket sources, verdict = validated
- 2026-06-01: Outcome statement #2 refined after pilot user feedback
```

Job Articles age. Re-validate every quarter if the build is ongoing or if the
market context shifts materially.

## When a build outgrows its Job Article

If the build scope expands beyond what the Job Article evidenced, the article
must be revised or a new one written. A PRD that drifts from its Job Article
is the most common path to shipping the wrong thing well.
