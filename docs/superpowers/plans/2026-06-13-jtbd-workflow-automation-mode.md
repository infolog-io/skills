# jtbd-prd workflow-automation Mode Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a fourth `workflow-automation` mode to the jtbd-prd skill that reviews a customer's workflows and emits a Jidoka-based Automation Map with a human-in-the-loop design and a readiness verdict.

**Architecture:** Pure content skill. New mode is built from two references, one schema, one template, two prompts, and a paired fixture, then wired into SKILL.md, README.md, and TESTS.md. Leaf files are authored first; SKILL.md is wired last so the reference-integrity gate passes only once every target exists.

**Tech Stack:** Markdown with YAML frontmatter; JSON Schema (draft 2020-12); python3 for verification (json parse, reference resolver, word count). No build system.

> **Post-implementation note (2026-06-13):** Implemented and shipped. Two
> code-quality review rounds refined the design after this plan was written.
> The committed skill under `skills/jtbd-prd/` is the source of truth. The
> vocabulary in this plan is synced; the behavioral refinements below are
> reflected in the shipped skill and the spec, not re-embedded in the task
> code blocks here:
> - `automation_level` vocabulary is `none | partial | most | full` (was
>   `assist | supervise | monitor | full`) to avoid colliding with the HITL
>   rung names and to give Manual-rung steps a value.
> - Map-level verdict = most conservative across selected workflows; the
>   rule applies to each workflow as a whole, not step by step.
> - Leverage formula weights are explicit: High=3, Medium=2, Low=1, with
>   frequency normalized to per-month.
> - Added trigger phrase "how should AI fit my workflow".
> - Shortlist has an empty-state line for the `human-led` verdict.

---

## File Structure

New, under `skills/jtbd-prd/`:
- `references/jidoka-framework.md` — Jidoka distilled + the six-principle mapping.
- `references/human-in-the-loop-levels.md` — the five-rung ladder + selection rule.
- `schemas/automation-map.json` — data contract for the map.
- `templates/automation-map.md` — the artifact shape (conforms to the schema).
- `prompts/discover-workflows.md` — question set A + leverage ranking.
- `prompts/jidoka-automation-analysis.md` — question set B + scoring + assembly + verdict.
- `fixtures/input-workflow-sample.md` — a sample workflow description.
- `fixtures/expected-automation-map.md` — the expected map for that input.

Modified:
- `skills/jtbd-prd/SKILL.md` — wire the mode into modes, flow, inputs, outputs, triggers, references, destination.
- `skills/jtbd-prd/README.md` — three modes → four; stay ≤200 words.
- `skills/jtbd-prd/TESTS.md` — end conditions + test cases for the mode.

Dependency order: references and schema have no dependencies. Template and fixtures conform to the schema. Prompts reference the template and schema. SKILL.md links everything and must come last for the gate.

---

## Task 1: Jidoka framework reference

**Files:**
- Create: `skills/jtbd-prd/references/jidoka-framework.md`

- [ ] **Step 1: Create the reference file**

```markdown
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
| Run autonomously | What automation level fits — none, partial, most, or full? |
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
```

- [ ] **Step 2: Verify the file parses and links resolve**

Run: `cd skills/jtbd-prd && test -f references/jidoka-framework.md && grep -c "human-in-the-loop-levels.md" references/jidoka-framework.md`
Expected: prints `1` (the link target is created in Task 2).

- [ ] **Step 3: Commit**

```bash
git add skills/jtbd-prd/references/jidoka-framework.md
git commit -m "feat(jtbd-prd): add Jidoka framework reference for workflow-automation mode"
```

---

## Task 2: Human-in-the-loop levels reference

**Files:**
- Create: `skills/jtbd-prd/references/human-in-the-loop-levels.md`

- [ ] **Step 1: Create the reference file**

```markdown
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
```

- [ ] **Step 2: Verify both references now cross-link**

Run: `cd skills/jtbd-prd && grep -l "jidoka-framework.md" references/human-in-the-loop-levels.md && grep -l "human-in-the-loop-levels.md" references/jidoka-framework.md`
Expected: both filenames print (the cross-links resolve).

- [ ] **Step 3: Commit**

```bash
git add skills/jtbd-prd/references/human-in-the-loop-levels.md
git commit -m "feat(jtbd-prd): add human-in-the-loop levels reference"
```

---

## Task 3: Automation Map JSON schema

**Files:**
- Create: `skills/jtbd-prd/schemas/automation-map.json`

- [ ] **Step 1: Create the schema (matches the style of `schemas/job-article.json`)**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://infolog.io/schemas/automation-map.json",
  "title": "Automation Map",
  "description": "Workflow-automation artifact produced by jtbd-prd. Workflow inventory, per-step Jidoka analysis, shortlist, human-in-the-loop design, verdict.",
  "type": "object",
  "required": [
    "label",
    "verdict",
    "last_updated",
    "workflow_inventory",
    "selected_workflows",
    "step_analysis",
    "shortlist",
    "human_in_the_loop_design"
  ],
  "additionalProperties": false,
  "properties": {
    "label": { "type": "string", "minLength": 3, "maxLength": 80 },
    "verdict": { "enum": ["ready-to-automate", "pilot-with-oversight", "human-led"] },
    "last_updated": { "type": "string", "format": "date" },
    "workflow_inventory": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["name", "frequency", "time_per_run", "pain", "feasibility", "leverage_rank"],
        "additionalProperties": false,
        "properties": {
          "name": { "type": "string" },
          "frequency": { "type": "string" },
          "time_per_run": { "type": "string" },
          "pain": { "enum": ["High", "Medium", "Low"] },
          "feasibility": { "enum": ["High", "Medium", "Low"] },
          "leverage_rank": { "type": "integer", "minimum": 1 }
        }
      }
    },
    "selected_workflows": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["name", "rationale"],
        "additionalProperties": false,
        "properties": {
          "name": { "type": "string" },
          "rationale": { "type": "string" }
        }
      }
    },
    "step_analysis": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "workflow", "step", "nature", "automation_level", "detection_signal",
          "stop_condition", "human_role", "hitl_rung", "countermeasure",
          "automation_potential", "feasibility", "stakes"
        ],
        "additionalProperties": false,
        "properties": {
          "workflow": { "type": "string" },
          "step": { "type": "string" },
          "nature": { "enum": ["repetitive", "judgment"] },
          "automation_level": { "enum": ["none", "partial", "most", "full"] },
          "detection_signal": { "type": "string" },
          "stop_condition": { "type": "string" },
          "human_role": { "enum": ["approve", "edit", "exception-handle", "audit"] },
          "hitl_rung": { "enum": ["Manual", "Assisted", "Supervised", "Monitored", "Autonomous"] },
          "countermeasure": { "type": "string" },
          "automation_potential": { "enum": ["High", "Medium", "Low"] },
          "feasibility": { "enum": ["High", "Medium", "Low"] },
          "stakes": { "enum": ["High", "Medium", "Low"] }
        }
      }
    },
    "shortlist": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["step", "priority"],
        "additionalProperties": false,
        "properties": {
          "step": { "type": "string" },
          "priority": { "type": "integer", "minimum": 1 }
        }
      }
    },
    "human_in_the_loop_design": { "type": "string", "minLength": 20 }
  }
}
```

- [ ] **Step 2: Verify the schema is valid JSON**

Run: `python3 -c "import json; json.load(open('skills/jtbd-prd/schemas/automation-map.json')); print('valid json')"`
Expected: `valid json`

- [ ] **Step 3: Commit**

```bash
git add skills/jtbd-prd/schemas/automation-map.json
git commit -m "feat(jtbd-prd): add automation-map JSON schema"
```

---

## Task 4: Automation Map template

**Files:**
- Create: `skills/jtbd-prd/templates/automation-map.md`

- [ ] **Step 1: Create the template (six fixed sections matching the schema)**

```markdown
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
- Automation level: {{none | partial | most | full}}
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
```

- [ ] **Step 2: Verify the template has all six sections**

Run: `grep -cE "^## [1-6]\." skills/jtbd-prd/templates/automation-map.md`
Expected: `6`

- [ ] **Step 3: Commit**

```bash
git add skills/jtbd-prd/templates/automation-map.md
git commit -m "feat(jtbd-prd): add automation-map template"
```

---

## Task 5: Workflow-discovery prompt (question set A)

**Files:**
- Create: `skills/jtbd-prd/prompts/discover-workflows.md`

- [ ] **Step 1: Create the prompt**

```markdown
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
```

- [ ] **Step 2: Verify the prompt names its template and downstream prompt**

Run: `cd skills/jtbd-prd && grep -c "templates/automation-map.md\|prompts/jidoka-automation-analysis.md" prompts/discover-workflows.md`
Expected: `2` (the analysis prompt is created in Task 6).

- [ ] **Step 3: Commit**

```bash
git add skills/jtbd-prd/prompts/discover-workflows.md
git commit -m "feat(jtbd-prd): add workflow-discovery prompt"
```

---

## Task 6: Jidoka analysis prompt (question set B)

**Files:**
- Create: `skills/jtbd-prd/prompts/jidoka-automation-analysis.md`

- [ ] **Step 1: Create the prompt**

```markdown
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
2. Automation level: how much of the step can AI do with today's tools —
   none, partial, most, or full?
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
```

- [ ] **Step 2: Verify the prompt references both references and the template**

Run: `cd skills/jtbd-prd && grep -cE "references/jidoka-framework.md|references/human-in-the-loop-levels.md|templates/automation-map.md" prompts/jidoka-automation-analysis.md`
Expected: `3` or more.

- [ ] **Step 3: Commit**

```bash
git add skills/jtbd-prd/prompts/jidoka-automation-analysis.md
git commit -m "feat(jtbd-prd): add Jidoka automation-analysis prompt"
```

---

## Task 7: Paired fixture (input + expected)

**Files:**
- Create: `skills/jtbd-prd/fixtures/input-workflow-sample.md`
- Create: `skills/jtbd-prd/fixtures/expected-automation-map.md`

- [ ] **Step 1: Create the input fixture**

```markdown
---
type: fixture
---

# Fixture input — workflow description

A customer success manager (CSM) describes their work for a
workflow-automation review.

"I manage 40 mid-market accounts. Two processes eat my week.

Onboarding: when a deal closes, I get a handoff doc. I schedule a kickoff,
prep the account config, run the kickoff call, write a success plan, and
wire up integrations. It runs about 8 times a month and takes ~6 hours
each. The kickoff call and success plan need real judgment. Config and
scheduling are the same every time. If the config is wrong the customer
churns early — that's expensive.

QBR prep: every quarter I pull usage metrics from the dashboard, build a
deck, and write talking points. ~20 QBRs a quarter, ~3 hours each. The
data pull is identical every time. The talking points need judgment. A
wrong number in a deck is embarrassing but recoverable."
```

- [ ] **Step 2: Create the expected output fixture**

```markdown
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
- Automation level: most
- Detection signal: config validated against an account-type checklist
- Stop condition: a required field is missing or conflicts with the plan
- Human role: approve
- HITL rung: Supervised
- Countermeasure: each correction adds a checklist rule
- Scores: automation potential High · feasibility Medium · stakes High

### Account onboarding → run kickoff call

- Nature: judgment
- Automation level: partial
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
```

- [ ] **Step 3: Verify the expected fixture has all six sections**

Run: `grep -cE "^## [1-6]\." skills/jtbd-prd/fixtures/expected-automation-map.md`
Expected: `6`

- [ ] **Step 4: Commit**

```bash
git add skills/jtbd-prd/fixtures/input-workflow-sample.md skills/jtbd-prd/fixtures/expected-automation-map.md
git commit -m "test(jtbd-prd): add paired workflow-automation fixture"
```

---

## Task 8: Wire the mode into SKILL.md

**Files:**
- Modify: `skills/jtbd-prd/SKILL.md`

- [ ] **Step 1: Add the workflow-description input row**

Find in the "Inputs accepted" table:

```
| Build hypothesis | One-sentence statement | "We want to build X for Y users" |
```

Replace with:

```
| Build hypothesis | One-sentence statement | "We want to build X for Y users" |
| Workflow description | Markdown or free text | "A CSM onboards 8 accounts/month, then…" |
```

- [ ] **Step 2: Add the Automation Map output section**

Find:

```
## Flow
```

Insert immediately BEFORE it:

```
## Output: the Automation Map (workflow-automation mode)

When the mode is workflow-automation, the skill emits an Automation Map
instead of a Job Article, conforming to `templates/automation-map.md` and
`schemas/automation-map.json`. Six fixed sections: Workflow Inventory,
Selected Workflows, Step Analysis, Automation Shortlist, Human-in-the-Loop
Design, and Verdict.

```

- [ ] **Step 3: Add the mode to the flow block**

Find the closing fence of the Flow code block:

```
5. Issue verdict:
   - prompts/verdict.md
```

Replace with:

```
5. Issue verdict:
   - prompts/verdict.md

workflow-automation mode (separate path):
1. Entry: read a Job Article (downstream) or take a workflow description (cold)
2. Discover workflows: prompts/discover-workflows.md → Workflow Inventory
3. Jidoka analysis on the top 1-3: prompts/jidoka-automation-analysis.md
4. Render: templates/automation-map.md
5. Verdict: ready-to-automate / pilot-with-oversight / human-led
```

- [ ] **Step 4: Add trigger rows**

Find in the "Trigger phrases" table:

```
| user pastes build proposal without evidence | Auto-suggest validation |
```

Replace with:

```
| user pastes build proposal without evidence | Auto-suggest validation |
| "workflow review", "where can AI automate", "automation map" | workflow-automation |
| "human in the loop", "Jidoka", "automate this workflow" | workflow-automation |
```

- [ ] **Step 5: Add the references**

Find the "## References" list and add two bullets after the `prd-framing.md` line:

```
- `references/jidoka-framework.md` — Jidoka distilled + the AI-automation mapping
- `references/human-in-the-loop-levels.md` — the five-rung oversight ladder
```

- [ ] **Step 6: Note the Automation Map destination**

Find:

```
Never write to the infolog-skills repo itself unless explicitly asked.
```

Insert immediately BEFORE it:

```
For workflow-automation mode, write the Automation Map as
`automation-map-<short-slug>.md`, using the same directory rules as the Job
Article.

```

- [ ] **Step 7: Verify the reference-integrity gate passes for jtbd-prd**

Run:
```bash
python3 - <<'PY'
import re, pathlib
sk = pathlib.Path("skills/jtbd-prd")
FOLD = r"(?:scripts|references|assets|prompts|templates|schemas|fixtures)"
tok = re.compile(r'`?\b('+FOLD+r'/[A-Za-z0-9_./-]+)`?')
dead=[]
for f in [sk/"SKILL.md"]+sorted((sk/"references").glob("*.md"))+sorted((sk/"prompts").glob("*.md")):
    for m in tok.finditer(f.read_text()):
        r=m.group(1)
        if '<' in r or '*' in r: continue
        if not ((f.parent/r).exists() or (sk/r).exists()):
            dead.append(f"{f.name} -> {r}")
print("DEAD:", dead if dead else "none")
PY
```
Expected: `DEAD: none`

- [ ] **Step 8: Commit**

```bash
git add skills/jtbd-prd/SKILL.md
git commit -m "feat(jtbd-prd): wire workflow-automation mode into SKILL.md"
```

---

## Task 9: Update README (stay ≤200 words)

**Files:**
- Modify: `skills/jtbd-prd/README.md`

- [ ] **Step 1: Change three modes to four**

Find:

```
Three modes: **discovery** (raw inputs → jobs), **validation** (hypothesis +
evidence → verdict), **reverse** (artifact → inferred jobs, must be confirmed
by real research).
```

Replace with:

```
Four modes: **discovery** (inputs → jobs), **validation** (hypothesis →
verdict), **reverse** (artifact → inferred jobs), and **workflow-automation**
(workflow → where AI can automate, via a Jidoka human-in-the-loop review).
```

- [ ] **Step 2: Add a one-line output note**

Find:

```
Markdown Job Article with seven fixed sections: primary job statement,
evidence table, dimensions (functional/emotional/social), Ulwick outcome
statements, underserved vs. overserved, build implication, and verdict.
```

Replace with:

```
Markdown Job Article with seven fixed sections: job statement, evidence,
dimensions, Ulwick outcomes, underserved vs. overserved, build implication,
verdict. Workflow-automation mode emits an Automation Map instead.
```

- [ ] **Step 3: Verify word count ≤200**

Run: `wc -w skills/jtbd-prd/README.md`
Expected: a number ≤ 200.

- [ ] **Step 4: If over 200, trim**

If Step 3 exceeds 200, find:

```
## When to use

Before writing a PRD, scoping a feature, pivoting an existing build, or
answering "should we build this?" Auto-suggests when you paste a build
proposal without evidence.
```

Replace with:

```
## When to use

Before a PRD, scoping, or a pivot — or when answering "should we build
this?" Auto-suggests when you paste a build proposal without evidence.
```

Re-run `wc -w skills/jtbd-prd/README.md`. Expected: ≤ 200.

- [ ] **Step 5: Commit**

```bash
git add skills/jtbd-prd/README.md
git commit -m "docs(jtbd-prd): add workflow-automation mode to README"
```

---

## Task 10: Update TESTS.md

**Files:**
- Modify: `skills/jtbd-prd/TESTS.md`

- [ ] **Step 1: Add an end condition**

Find:

```
8. README in the plugin root explains in under 200 words what the skill does and when to use it
```

Replace with:

```
8. README in the plugin root explains in under 200 words what the skill does and when to use it
9. workflow-automation mode produces an Automation Map that validates against `schemas/automation-map.json`
```

- [ ] **Step 2: Add test cases after T8**

Find:

```
### T8 — Trigger phrase activation
For each trigger in SKILL.md, the skill description must contain language a model would match on. Verified by reading SKILL.md frontmatter and confirming each trigger phrase appears or maps clearly.
```

Insert immediately AFTER it:

```

### T9 — Workflow discovery
- Input: `fixtures/input-workflow-sample.md`
- Expected: a Workflow Inventory with both workflows, each scored on pain
  and feasibility, ranked by leverage. Onboarding ranks above QBR prep.

### T10 — Jidoka step classification
- Input: the onboarding steps from the fixture
- Expected: "prep account config" is repetitive with High stakes →
  Supervised rung; "run kickoff call" is judgment → Assisted rung.

### T11 — Automation Map end-to-end
- Input: `fixtures/input-workflow-sample.md`
- Expected output: `fixtures/expected-automation-map.md` — all six
  sections, every step carries three scores and a rung, verdict is
  `pilot-with-oversight`.

### T12 — Automation Map schema validation
- Hand-craft one Automation Map; it must pass `schemas/automation-map.json`.
- Negative test: a map missing `verdict` must fail validation.

### T13 — Verdict classification (workflow-automation)
| Scenario | Expected verdict |
|---|---|
| ≥1 step High potential, High feasibility, signal defined, stakes Low | ready-to-automate |
| automatable steps but high stakes / weak signal | pilot-with-oversight |
| judgment-dominant, high stakes, no signal | human-led |
```

- [ ] **Step 3: Verify the new cases are present**

Run: `grep -cE "^### T(9|1[0-3]) " skills/jtbd-prd/TESTS.md`
Expected: `5`

- [ ] **Step 4: Commit**

```bash
git add skills/jtbd-prd/TESTS.md
git commit -m "test(jtbd-prd): add workflow-automation test cases"
```

---

## Task 11: Final verification

**Files:** none (verification only)

- [ ] **Step 1: All declared references resolve (reference-integrity gate)**

Run the Task 8 Step 7 snippet again.
Expected: `DEAD: none`

- [ ] **Step 2: Both JSON schemas parse**

Run: `python3 -c "import json,glob; [json.load(open(f)) for f in glob.glob('skills/jtbd-prd/schemas/*.json')]; print('all schemas valid')"`
Expected: `all schemas valid`

- [ ] **Step 3: README within budget**

Run: `wc -w skills/jtbd-prd/README.md`
Expected: ≤ 200.

- [ ] **Step 4: New companion files carry type frontmatter**

Run: `cd skills/jtbd-prd && for f in references/jidoka-framework.md references/human-in-the-loop-levels.md templates/automation-map.md prompts/discover-workflows.md prompts/jidoka-automation-analysis.md fixtures/input-workflow-sample.md fixtures/expected-automation-map.md; do head -2 "$f" | grep -q "type:" && echo "ok $f" || echo "MISSING $f"; done`
Expected: every line starts with `ok`.

- [ ] **Step 5: Final commit if anything is uncommitted**

```bash
git status --short skills/jtbd-prd
git add skills/jtbd-prd && git commit -m "chore(jtbd-prd): finalize workflow-automation mode" || echo "nothing to commit"
```

---

## Self-Review

Spec coverage:
- Jidoka mapping → Task 1.
- HITL ladder → Task 2.
- Scoring (three H/M/L axes, priority rule) → Tasks 3, 6.
- Automation Map artifact (six sections) → Tasks 3, 4, 7.
- Verdict thresholds → Tasks 6, 10.
- Question set A → Task 5.
- Question set B → Task 6.
- Dual entry → Task 8 (flow block).
- File plan (8 new, 3 edits) → Tasks 1-10.
- Reference-integrity gate → Task 8 Step 7, Task 11 Step 1.

Type consistency: `automation_level` enum is `none|partial|most|full` in the schema (Task 3), the prompt (Task 6), and the template (Task 4). `hitl_rung` and `nature` enums match across schema, template, and fixture. Verdict values `ready-to-automate|pilot-with-oversight|human-led` match across schema, prompt, README, TESTS, and fixture.

No placeholders: every file step shows complete content; verification steps give exact commands and expected output.
