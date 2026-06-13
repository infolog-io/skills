---
type: reference
---

# Jidoka Framework

Jidoka (自働化) is a pillar of the Toyota Production System. The usual
translation is "autonomation": automation with a human touch. A machine
runs repetitive work on its own. It detects an abnormality, stops
immediately, and signals a human. The cause is fixed so the same defect
cannot recur.

Source: Taiichi Ohno, Toyota Production System. Confidence: high.

## Why it maps to AI automation

AI automating a workflow step has the same shape. The model runs a
repetitive step. It must detect when its own output is unreliable, stop,
and escalate to a human. Each correction should improve the system.

## The six principles, applied per step

| Principle | Plain-language analysis question |
|---|---|
| Separate human work from machine work | Is this step repetitive/rule-like or judgment/relational? |
| Run autonomously | What automation level fits — assist, supervise, monitor, or full? |
| Detect the abnormality | What signal reveals the AI got it wrong? |
| Stop the line (andon) | Under what condition must the AI halt and escalate? |
| Human corrects | What is the human role — approve, edit, exception-handle, audit? |
| Root cause / poka-yoke | How does each correction improve the system? |

## The two non-negotiables

A step is safe to automate only when two Jidoka conditions hold:

1. A detection signal exists. Without a way to know the AI erred, there is
   no andon cord, so automation runs blind.
2. A stop condition is defined. The AI must know when to defer.

When either is missing, the step stays human-led or assisted, however
repetitive it is. See [human-in-the-loop-levels.md](human-in-the-loop-levels.md).

## Worked example

Step: categorize an inbound support ticket.

- Separation: repetitive classification — machine work.
- Detection signal: model confidence score plus a weekly human audit.
- Stop condition: confidence below threshold, or a new product area.
- Human role: approve low-confidence cases; audit a sample of the rest.
- Countermeasure: misclassifications become new labeled examples.
