---
type: reference
---

# Human-in-the-Loop Levels

A ladder of five rungs. It gives shared vocabulary to the "automation
level" and "human role" answers in the Jidoka analysis. See
[jidoka-framework.md](jidoka-framework.md).

| Rung | AI does | Human does | Fits when |
|---|---|---|---|
| Manual | nothing | everything | judgment-dominant; high stakes; no detection signal |
| Assisted | drafts a suggestion | does the work | low trust; creative or relational step |
| Supervised (HITL) | acts | approves each action before it lands | medium stakes; detection signal exists |
| Monitored (HOTL) | acts and lands | spot-checks; can intervene | low-medium stakes; reliable signal |
| Autonomous | acts and lands | audits samples periodically | low stakes; strong signal; reversible action |

## How to pick a rung

Two factors set the rung: stakes and detection-signal quality.

- High stakes OR a weak signal forces a lower rung.
- Low stakes AND a strong signal allow a higher rung.
- A reversible action allows one rung higher than an irreversible one.

Start one rung lower than the analysis suggests. Raise the rung as the
detection signal proves reliable in production. This mirrors Jidoka's
build-quality-in discipline.

## Worked example

A step with medium stakes and a model confidence score starts at
Supervised. After a month of high agreement between AI and the human
approver, it moves to Monitored.
