---
type: prompt
---

# Prompt — Discover workflows

**Purpose:** Surface the few high-leverage workflows a person does, end to
end, and rank them for Jidoka analysis.

## Input contract

Either a Job Article (downstream entry) or a free-text description of the
person's role and work (cold entry). If neither is rich enough, ask the
eight questions below directly.

## The eight questions

1. Walk me through a typical week or month. Name the 3-5 processes you
   spend the most time on, end to end.
2. For each: what triggers it, and what does "done" look like?
3. How often does it run, and how long per run?
4. What are the steps in order, and who or what is involved at each?
5. Which steps are identical every time, and which need judgment?
6. Where does the workflow break, get reworked, or bottleneck?
7. What systems, data, or tools does each step touch?
8. What is the cost of a mistake at each step?

## Output contract

A Workflow Inventory table (section 1 of `templates/automation-map.md`):
one row per workflow with frequency, time per run, pain (H/M/L),
feasibility (H/M/L), and a leverage rank.

Leverage rank = order by frequency × time × pain × feasibility, highest
first. The top one to three workflows pass to
`prompts/jidoka-automation-analysis.md`.

## Worked example

Input: "I'm a customer success manager. Most of my time goes to onboarding
new accounts and prepping quarterly business reviews."

Output (excerpt):

| Workflow | Frequency | Time/run | Pain | Feasibility | Leverage rank |
|---|---|---|---|---|---|
| Account onboarding | 8/month | 6 hrs | High | Medium | 1 |
| QBR prep | 20/quarter | 3 hrs | Medium | High | 2 |

## Negative case

Input: "I want AI to do my job." With no described workflow, do not invent
one. Ask the eight questions first. Refuse to produce an inventory from no
evidence.
