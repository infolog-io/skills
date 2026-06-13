---
type: template
---

# Automation Map — {{label}}

Verdict: {{ready-to-automate | pilot-with-oversight | human-led}}
Last updated: {{YYYY-MM-DD}}

## 1. Workflow Inventory

| Workflow | Frequency | Time/run | Pain | Feasibility | Leverage rank |
|---|---|---|---|---|---|
| {{name}} | {{e.g. daily}} | {{e.g. 45 min}} | {{High/Medium/Low}} | {{High/Medium/Low}} | {{1}} |

## 2. Selected Workflows

- **{{name}}** — {{why this one was selected for analysis}}

## 3. Step Analysis

### {{workflow}} → {{step}}

- Nature: {{repetitive | judgment}}
- Automation level: {{assist | supervise | monitor | full}}
- Detection signal: {{how we know the AI erred}}
- Stop condition: {{when the AI halts and escalates}}
- Human role: {{approve | edit | exception-handle | audit}}
- HITL rung: {{Manual | Assisted | Supervised | Monitored | Autonomous}}
- Countermeasure: {{how a correction improves the system}}
- Scores: automation potential {{H/M/L}} · feasibility {{H/M/L}} · stakes {{H/M/L}}

## 4. Automation Shortlist

Steps ranked by priority (automation potential × feasibility).

1. {{step}} — priority {{1}}

## 5. Human-in-the-Loop Design

{{One paragraph: how oversight works across the selected workflows — which
rungs, who approves, what the andon cord is, how corrections feed back.}}

## 6. Verdict

{{ready-to-automate | pilot-with-oversight | human-led}} — {{one-sentence rationale}}
