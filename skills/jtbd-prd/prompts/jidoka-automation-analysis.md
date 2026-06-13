---
type: prompt
---

# Prompt — Jidoka automation analysis

**Purpose:** Analyze each step of a selected workflow against the six
Jidoka principles, score it, and assemble the Automation Map with a
verdict.

## Input contract

The top one to three workflows from `prompts/discover-workflows.md`, broken
into ordered steps. Uses `references/jidoka-framework.md` and
`references/human-in-the-loop-levels.md`.

## The seven questions, per step

1. Separation: is this step repetitive/rule-based, or judgment/relational?
2. Automation level: could AI do it with today's tools — assist,
   supervise, monitor, or fully?
3. Detection: how would you know the AI got it wrong?
4. Stop condition: when must the AI halt and hand to a human?
5. Human role: when a human steps in, do they approve, edit,
   exception-handle, or audit-sample?
6. Countermeasure: when the human corrects the AI, how does that feedback
   improve the system?
7. Stakes: what is the blast radius of a bad automated action here?

## Scoring

Score each step High/Medium/Low on three axes: automation potential,
feasibility, stakes. Step priority = automation potential × feasibility.
Stakes set the human-in-the-loop rung, not the priority.

Pick the rung from `references/human-in-the-loop-levels.md`. High stakes or
a weak detection signal forces a lower rung. If no detection signal or stop
condition exists, the step is Manual or Assisted, however repetitive.

## Output contract

A complete Automation Map per `templates/automation-map.md`, all six
sections, ending in a verdict:

| Verdict | Rule |
|---|---|
| ready-to-automate | ≥1 step with automation potential High, feasibility High, a defined detection signal, and stakes ≤ Medium |
| pilot-with-oversight | automatable steps exist but require Supervised or Monitored oversight; high stakes or a weak detection signal |
| human-led | judgment-dominant, high stakes with no reliable signal, or infeasible with current tools |

## Worked example

Step: "QBR data pull — gather usage metrics from the dashboard."

- Nature: repetitive. Automation level: full.
- Detection signal: row-count and date-range checks against the source.
- Stop condition: a metric is missing or outside expected bounds.
- Human role: audit a sample. HITL rung: Monitored.
- Countermeasure: failed checks tighten the extraction query.
- Scores: automation potential High · feasibility High · stakes Low.

This step alone supports `ready-to-automate` for the QBR-prep workflow.

## Negative case

A step like "decide whether to escalate a churn risk to the exec team" is
judgment, high stakes, with no reliable detection signal. Mark it Manual.
Do not assign an automation level above Assisted.
