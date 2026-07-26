---
name: product-explainer
description: >
  Brief an owner, stakeholder, or newcomer on any product at the right
  altitude, and maintain the living ephemera that carry the story: state map,
  plan page, decision tables, ratification records, low-fidelity wireframes.
  Use when asked "where are we", "give me the 10,000-foot view", "what is this
  product", "what's the status", when an owner forgets context mid-decision,
  when open questions need collecting or ratifying, or when a milestone lands
  and the owner asked to be pinged. Product-agnostic: pairs with a per-product
  product card kept in the product's own repo.
---

# product-explainer

## Purpose

Turn an in-flight product into one explainable story: what it is, what is decided, what is built, what is next, and what only the owner can do. The protocol exists because owners lose context between sessions; the fix is altitude and ephemera, never more detail.

## The seven rules

1. **Altitude first.** Open with one sentence saying what the product IS. Detail follows only after that sentence lands. An owner saying "I don't remember any of this" is a zoom-out signal, never a push-detail signal.
2. **State map before roadmap.** Show shipped versus planned as labeled tiers. Built earns a checkmark and a date; unbuilt earns a phase number. Never mix tiers in one list.
3. **Decisions as tables, conflicts stated openly.** Every open decision gets: options, case for, case against, ONE recommendation with its argument named. When evidence contradicts the owner's stated instinct, say so in the same breath as the recommendation. Keep both options drawn until ratified.
4. **Working answers, never blocks.** Fill every unknown with a defensible default, label it a working answer, and name the review point where the owner ratifies or reverses. Work proceeds; nothing waits on an unanswered question.
5. **Statuses are words plus numbers.** Fixed vocabulary: DRAFT, GO, DONE, QUEUED, OPEN, BLOCKED. Attach measured numbers (deltas, counts, hashes), never adjectives. "Verified" only after the check ran with output in hand; UI claims stay flagged pixels-pending until a human-viewable screenshot exists.
6. **Ephemera live at stable links.** One plan page, one wireframe deck, redeployed to the same URL on every change. The plan page footer always carries: repo, branch, latest commit, governance chain, and the actions only the owner can take.
7. **Ping discipline.** Notify only when the thing they asked about is done, or when blocked on an owner-only action. Lead with the action, then the outcome, under 200 characters.

## The product card

One per product, kept in the product's repo and kept current. Unfilled placeholder means "unknown"; say unknown, never invent.

```markdown
# {{PRODUCT}} card (as of {{DATE}})

One-liner: {{PRODUCT}} is {{CATEGORY}}: {{3-5 word verb tagline}}.
Not: {{what it is explicitly NOT, incl. dropped lineage}}.
Horizon: {{the larger vision current work feeds}}.

Decided (ratified only):
- {{decision}} ({{date}}, {{argument in one clause}})

Kept: {{surfaces}}. Cut: {{surfaces}}.   <- only if a subtraction happened

State map: {{see ladder format}}
Latest milestone numbers: {{measured deltas, counts, hashes}}
Open items (owner-only): {{numbered actions}}
Governance chain: {{doc A}} outranks {{doc B}} outranks {{doc C}}.
Links: {{repo}} | {{plan page}} | {{wireframe deck}}
```

## Formats

### State map ladder

```
SHIPPED ........ {{component}} ({{proof}})   {{component}}   {{component}}
DONE {{date}} .. {{milestone}}: {{what changed}}; {{headline numbers}}
QUEUED ......... {{next bounded work}} ({{source of its scope}})
PLANNED ........ {{n}} {{name}} -> {{n}} {{name}} -> {{n}} {{name}}
AFTER .......... {{deferred-by-owner items, attributed}}
```

### Decision table

| Q | Option | Case for | Case against | Recommendation |
|---|---|---|---|---|
| {{id}} | A | strongest honest case | strongest honest case | ONE pick, argument named |
|        | B | ... | ... | owner-instinct conflicts stated here, openly |

### Ratification record

`ANSWERED {{date}}, owner, at {{review point}}: {{DECISION}}. Reverses/confirms {{prior working answer}}. {{one-line argument}}.`

### Plan page anatomy

Eyebrow (status + date) -> product name -> thesis line -> the pivot/summary paragraph -> Decided list -> ratify card (open questions with working answers and contest flags) -> requirements table -> mission list with statuses -> review links -> footer (repo, branch, commit, governance, owner actions). Mobile-first; the owner reads it on a phone.

### Wireframe conventions

Low fidelity only: boxes, real label text, no styling; if it looks like the app it is too high fidelity. Every screen gets empty, populated, and error variants where flows define them. Numbered callouts tie to findings. Contested decisions get BOTH options drawn side by side, each with a one-paragraph case, ending in one recommendation. In portable text, wireframes render as ASCII:

```
+------ header: {{regions}} --------------------------------+
| {{left rail}} | {{center surface}}      | {{right rail}}  |
|               | [{{state A}} | {{state B}}]                |
+---------------+-------------------------+-----------------+
| {{statusbar: context, counts, save state}}                |
+-----------------------------------------------------------+
```

### Ping format

`{{PRODUCT}} {{milestone}} done: {{headline numbers}}. Need you: {{owner-only action}}.` Under 200 characters, action first when one exists.

## Maintenance loop

- A milestone lands: update the state map tier, the numbers block, and the plan page footer commit hash the same day. Redeploy to the same URL.
- A decision ratifies: append the ratification record to the product card AND strike the working answer everywhere it appears. Same day.
- The owner reverses something: the record says "reverses", never silently rewrites history.
- A new unknown appears: it enters as a working answer with a named review point, never as a blocker.
- Instantiating for a product: copy the product card template into the product's repo, fill it, and optionally wrap card plus protocol into a per-product skill (worked example: skillstud.io's `skillstudio-explainer`).
