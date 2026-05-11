# Job Article: Triage stale PRs on Monday morning

> **Status:** under-evidenced · **Confidence:** low · **Last updated:** 2026-04-12

## Primary Job Statement

When opening Slack on Monday morning to a backlog of pull requests waiting on
my review, I want to see them in one place with enough context to triage
quickly, so I can decide what to review and what to hand off before the
team's standup.

## Evidence

| # | Source | Role | Date | Quote | Confidence |
|---|---|---|---|---|---|
| 1 | interview-acme-2026-04-12 | Senior Engineer | 2026-04-12 | "I open Slack and immediately see twelve pings from people waiting on my review. Half the time I don't even know which PR they're talking about. By the time I've triaged them I've lost ninety minutes and the team's already in standup." | high |
| 2 | interview-acme-2026-04-12 | Senior Engineer | 2026-04-12 | "Just give me a queue, sorted by what's been waiting longest, with enough context that I can decide whether to review it or hand it off to someone better suited." | high |
| 3 | interview-acme-2026-04-12 | Senior Engineer | 2026-04-12 | "I'm reading the diff, the description, trying to remember what we even decided about this feature in the design review. It's exhausting." | medium |

**Total:** 3 quotes across 1 source, 1 distinct role.

## Job Dimensions

- **Functional:** Reduce the time spent triaging incoming PR review requests on Monday morning
- **Emotional:** Avoid the exhaustion of cold-starting on every queued PR
- **Social:** not-yet-evidenced

## Outcome Statements (Ulwick form)

1. Minimize the time to triage a backlog of waiting PRs at the start of the day
2. Increase the proportion of triaged PRs that get reviewed by someone with prior context
3. Reduce the variability of Monday-morning ramp time across weeks

## Underserved vs. Overserved

**Underserved (high importance, low satisfaction):**
- Consolidated view of waiting PRs with context attached
- Mechanism to hand off a PR to someone with more relevant history
- A way to know which PRs are actually waiting on the reviewer vs. waiting on the author

**Overserved (low importance, high satisfaction):**
- Notification volume — current bot pings even when the PR is not the reviewer's turn

## Hire / Fire

- **Fires:** Manual Slack pings, ad-hoc cross-referencing across channels, the existing daily reminder bot (muted by most engineers)
- **Hires:** A consolidated triage view with context and routing
- **Trigger:** Monday morning ramp-up time exceeding 90 minutes before any productive review work begins

## Build Implication (PRD framing)

The build that inherits this article must:

- Address outcome statements: 1 and 2
- Avoid expanding into: notification volume (overserved area)
- Be measurable against: median Monday-morning time-to-first-meaningful-review-action
- Honor this constraint from evidence: "I open Slack and immediately see twelve pings from people waiting on my review. Half the time I don't even know which PR they're talking about."

## Verdict

- [ ] Validated — proceed to PRD
- [x] **Under-evidenced** — return when confidence ≥ medium across ≥3 sources
- [ ] Unvalidated — do not build; pivot or kill

**Reasoning:** Three strong quotes but a single source and a single role. Confidence threshold for `medium` requires ≥3 sources. Social dimension is not yet evidenced. Run the listed next research to escalate.

## Next research (if under-evidenced)

- Does this same friction appear for engineers at smaller companies (<20 engineers)? — Ask 2 engineers at an early-stage company
- Does the friction appear for non-senior engineers, or is it concentrated in senior reviewers? — Ask 2 mid-level engineers
- Is there a measurable social cost (manager noticing, peer perception)? — Probe in next interview's follow-up section

## Revision history

- 2026-04-12: Initial draft from 1 source, verdict = under-evidenced
