# Design — jtbd-prd workflow-automation mode

Date: 2026-06-13. Status: approved in brainstorming, pending spec review.

## Purpose

Add a fourth mode to the jtbd-prd skill. The mode reviews a customer's
large-scale workflows and finds where AI can automate pieces. It uses a
Jidoka process to place each step on a human-in-the-loop spectrum. It emits
a structured Automation Map with a readiness verdict.

## Decisions locked in brainstorming

1. Packaging: a new `workflow-automation` mode inside jtbd-prd, not a
   sibling skill.
2. Composition: dual entry. Runs downstream of a Job Article when one
   exists, or cold on a workflow description.
3. Output: a structured Automation Map plus verdict, in the Job Article's
   style (markdown artifact + JSON schema).
4. Jidoka framing: named spine, plain-language surface. The six principles
   drive structure; questions and artifact use plain terms.
5. Scoring: lightweight. Each step scored High/Medium/Low on three axes.

## The Jidoka mapping

Jidoka is Toyota's autonomation: automation with a human touch. The machine
runs repetitive work autonomously. It stops and signals a human the moment
an abnormality appears. The root cause is fixed so the defect cannot recur.

Each workflow step is analyzed against six principles.

| Jidoka principle | Plain-language analysis question |
|---|---|
| Separate human work from machine work | Is this step repetitive/rule-like or judgment/relational? |
| Run autonomously | What automation level fits — assist, supervise, monitor, or full? |
| Detect the abnormality | What signal reveals the AI got it wrong? |
| Stop the line | Under what condition must the AI halt and escalate? |
| Human corrects | What is the human role — approve, edit, exception-handle, audit? |
| Root cause / poka-yoke | How does each correction improve the system? |

## Question set A — workflow discovery

Asked to the reviewee to surface the few high-leverage workflows.

1. Walk me through a typical week or month. Name the 3-5 processes you
   spend the most time on, end to end.
2. For each: what triggers it, and what does "done" look like?
3. How often does it run, and how long per run?
4. What are the steps in order, and who or what is involved at each?
5. Which steps are identical every time, and which need judgment?
6. Where does the workflow break, get reworked, or bottleneck?
7. What systems, data, or tools does each step touch?
8. What is the cost of a mistake at each step?

Prioritization rule: rank workflows by frequency × time × pain ×
feasibility. The top one to three workflows proceed to Jidoka analysis.

## Question set B — Jidoka analysis

Run per selected workflow step. The six principles become direct questions.

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

## Human-in-the-loop ladder

Shared vocabulary for the "automation level" and "human role" answers.

| Rung | AI does | Human does | Fits when |
|---|---|---|---|
| Manual | nothing | everything | judgment-dominant; high stakes; no signal |
| Assisted | drafts a suggestion | does the work | low trust; creative or relational step |
| Supervised (HITL) | acts | approves each action before it lands | medium stakes; detection signal exists |
| Monitored (HOTL) | acts and lands | spot-checks; can intervene | low-medium stakes; reliable signal |
| Autonomous | acts and lands | audits samples periodically | low stakes; strong signal; reversible |

Stakes and detection-signal quality set the rung. High stakes or a weak
signal forces a lower rung.

## Scoring

Each step scored High/Medium/Low on three axes.

- Automation potential: how much of the step AI can take.
- Feasibility: whether current tools and data support it.
- Stakes: blast radius of an error.

Step priority = automation potential × feasibility. Stakes set the
human-in-the-loop rung, not the priority. A high-potential, high-
feasibility, low-stakes step is the first to automate.

## Output — the Automation Map

A markdown file conforming to `templates/automation-map.md` and
`schemas/automation-map.json`. Sections in fixed order.

1. Workflow Inventory — every workflow surfaced, with frequency, time,
   pain, feasibility, and leverage rank.
2. Selected Workflows — the top one to three, with rationale.
3. Step Analysis — per step: repetition-vs-judgment, automation level,
   detection signal, stop condition, human role and rung, countermeasure,
   stakes, and the three scores.
4. Automation Shortlist — steps ranked by priority, ready to pilot.
5. Human-in-the-Loop Design — how oversight works across the selected
   workflows.
6. Verdict — automation readiness.

## Verdict thresholds

| Verdict | Rule |
|---|---|
| ready-to-automate | ≥1 step with automation potential High, feasibility High, a defined detection signal, and stakes ≤ Medium |
| pilot-with-oversight | automatable steps exist but require Supervised or Monitored oversight; high stakes or a weak detection signal |
| human-led | judgment-dominant, high stakes with no reliable signal, or infeasible with current tools |

## Files

New, under `skills/jtbd-prd/`:

- `prompts/discover-workflows.md` (`type: prompt`) — question set A plus
  prioritization.
- `prompts/jidoka-automation-analysis.md` (`type: prompt`) — question set
  B, scoring, map assembly, verdict.
- `references/jidoka-framework.md` (`type: reference`) — Jidoka distilled,
  the mapping table, a citation.
- `references/human-in-the-loop-levels.md` (`type: reference`) — the
  ladder and selection rules.
- `templates/automation-map.md` (`type: template`) — the artifact shape.
- `schemas/automation-map.json` — JSON Schema for the map.
- `fixtures/input-workflow-sample.md` (`type: fixture`) — a sample
  workflow description.
- `fixtures/expected-automation-map.md` (`type: fixture`) — expected
  output.

Edited:

- `SKILL.md` — add the mode to the flow, modes, triggers, inputs, outputs,
  references, and output destination. Every new reference and prompt is
  linked from SKILL.md so the reference-integrity gate passes.
- `README.md` — add the mode; keep ≤200 words.
- `TESTS.md` — add end conditions and test cases for the mode.

No version bump. The repo is pre-0.1 per CLAUDE-PIP.

## Flow

```
workflow-automation mode:
1. Entry:
   - downstream: read an existing Job Article for context
   - cold: take a workflow description from the user
2. Discover workflows:
   - prompts/discover-workflows.md → Workflow Inventory + leverage rank
3. Jidoka analysis on the top 1-3:
   - prompts/jidoka-automation-analysis.md → Step Analysis + scores
4. Render Automation Map:
   - templates/automation-map.md
5. Issue verdict:
   - ready-to-automate / pilot-with-oversight / human-led
```

## Triggers

| Phrase | Mode |
|---|---|
| "workflow review", "where can AI automate", "automation map" | workflow-automation |
| "how should AI fit my workflow", "human in the loop" | workflow-automation |
| "Jidoka", "automate this workflow" | workflow-automation |

## Testing

- Cold entry: a workflow description yields a complete Automation Map with
  all six sections and a verdict.
- Downstream entry: a Job Article plus workflow yields a map that
  references the validated job.
- A judgment-dominant, high-stakes workflow returns `human-led`.
- A repetitive, low-stakes, feasible workflow returns `ready-to-automate`.
- Every step in Step Analysis carries all three scores and a rung.
- The map validates against `schemas/automation-map.json`.
- An audit of jtbd-prd passes the reference-integrity gate.

## Out of scope

- Full ROI or dollar-impact estimation.
- Building or running the automations.
- Vendor or model selection.
- Changes to the existing discovery, validation, and reverse modes, beyond
  adding the new mode alongside them.
