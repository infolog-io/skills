---
type: fixture
---

# Fixture expected — Automation Map

Expected Automation Map for `input-workflow-sample.md`.

## 1. Workflow Inventory

| Workflow | Frequency | Time/run | Pain | Feasibility | Leverage rank |
|---|---|---|---|---|---|
| Account onboarding | 8/month | 6 hrs | High | Medium | 1 |
| QBR prep | 20/quarter | 3 hrs | Medium | High | 2 |

## 2. Selected Workflows

- **Account onboarding** — highest leverage; mixed repetitive/judgment steps.
- **QBR prep** — high feasibility; a clean automation win.

## 3. Step Analysis

### Account onboarding → prep account config

- Nature: repetitive
- Automation level: supervise
- Detection signal: config validated against an account-type checklist
- Stop condition: a required field is missing or conflicts with the plan
- Human role: approve
- HITL rung: Supervised
- Countermeasure: each correction adds a checklist rule
- Scores: automation potential High · feasibility Medium · stakes High

### Account onboarding → run kickoff call

- Nature: judgment
- Automation level: assist
- Detection signal: none reliable
- Stop condition: always human-led
- Human role: edit
- HITL rung: Assisted
- Countermeasure: AI prep notes improve from call outcomes
- Scores: automation potential Low · feasibility Low · stakes High

### QBR prep → data pull

- Nature: repetitive
- Automation level: full
- Detection signal: row-count and date-range checks against the source
- Stop condition: a metric is missing or out of bounds
- Human role: audit
- HITL rung: Monitored
- Countermeasure: failed checks tighten the extraction query
- Scores: automation potential High · feasibility High · stakes Low

## 4. Automation Shortlist

1. QBR prep → data pull — priority 1
2. Account onboarding → prep account config — priority 2

## 5. Human-in-the-Loop Design

Start QBR data pull at Monitored with weekly sample audits. Keep onboarding
config at Supervised — high churn stakes demand per-account approval until
the checklist proves reliable. Kickoff calls stay human-led with AI prep
notes only.

## 6. Verdict

pilot-with-oversight — strong automatable steps exist, but the highest-
leverage workflow's config step carries high stakes and needs supervision.
