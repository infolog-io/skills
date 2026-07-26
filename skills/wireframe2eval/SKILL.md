---
name: wireframe2eval
description: >
  Turn a redesign into a content contract. Extracts every heading, CTA,
  and paragraph from the live source pages into a machine-readable
  inventory, then generates an eval that fails when the redesign silently
  drops any of it. Content loss during a redesign is invisible in review
  and expensive in search rankings; this makes it a failing check instead.
  Use when redesigning, replatforming, or consolidating an existing site,
  when a wireframe or mockup needs to become production pages without
  losing copy, when migrating multiple properties into one estate, or on
  "don't lose the content", "content parity", "did we drop anything",
  "wireframe2eval", "/wireframe2eval". Not for greenfield sites with no
  existing content to preserve.
---

# wireframe2eval

A wireframe shows structure. It does not show what the redesign quietly threw away.

Redesigns lose content by omission, not by decision. A section nobody remembers gets left out of the new layout, and the loss surfaces months later as a ranking drop or a support ticket. Nobody signs off on it, because nobody sees it. Design review looks at what is on the page, never at what used to be.

This skill converts the source pages into a contract the redesign must satisfy, then holds the redesign to it mechanically.

## The pipeline

EXTRACT → INVENTORY → WIREFRAME → EVAL → DECIDE

The eval runs from the first commit, when it fails almost completely. That is correct. The failure count is the migration's remaining work, and it only ever goes down.

## 1. EXTRACT

Pull the live content from every source property the redesign consolidates. One extraction per source page, per line of business or section.

Capture only what carries meaning: `h1`, `h2`, `h3`, CTA labels, and paragraphs over 40 characters. Skip nav chrome, cookie banners, and boilerplate — they are structure, not content, and they inflate the inventory until it stops being read.

Extract from the rendered DOM, not the HTML source. Page builders and client-side rendering mean `curl` and the browser disagree, and the browser is what users and crawlers see.

```
agent-browser open "https://<source>/"
agent-browser eval '<extraction expression>'
```

Record the source URL and extraction date in the inventory. An inventory with no provenance cannot be re-derived when the source changes.

## 2. INVENTORY

One JSON file, committed, versioned, reviewed like code.

```json
{
  "generated": "YYYY-MM-DD",
  "lines": {
    "<line>": {
      "source": "https://…",
      "required": { "h1": [], "headings": [], "ctas": [], "paragraphs": [] },
      "mapped":  [{ "from": "…", "to": "…", "reason": "…" }],
      "dropped": [{ "text": "…", "reason": "…" }]
    }
  }
}
```

`required` is the contract. `mapped` and `dropped` are the only two ways out of it, and both demand a written reason. A reason field with "n/a" in it is a defect the reviewer should reject.

## 3. WIREFRAME

The wireframe is the structure the inventory pours into. Build it with real tokens and real chrome, but treat body sections as slots that content fills — the wireframe is a template, not a page.

Never let the wireframe carry invented marketing copy. Placeholder copy reads as finished work in review, and it competes with the real content for the slot it occupies. Use labelled empty slots, or the real source copy, and nothing in between.

## 4. EVAL

One script, no dependencies, four verdicts per item:

| Verdict | Meaning |
|---|---|
| `present` | Found verbatim in the redesigned page, whitespace and case normalised |
| `mapped` | Deliberately rewritten; the replacement string must also be present |
| `dropped` | Deliberately removed, with a recorded reason |
| `MISSING` | Gone, with no decision recorded — the failure the eval exists to catch |

Silence is failure. An item that is neither present nor declared is `MISSING`, and `MISSING` exits non-zero.

Match on normalised text extracted from the rendered page: strip scripts, styles, comments, and tags, collapse whitespace, decode entities, lowercase. Match verbatim by default. Fuzzy matching defeats the purpose — "close enough" is how a rewrite that changed the meaning passes.

A page that does not exist yet is SKIPPED, and skipped is not passed. Exit with a distinct code so a half-built migration cannot be reported as green.

## 5. DECIDE

Work the `MISSING` list down. Each item gets exactly one of three dispositions:

- Carry it into the new page verbatim.
- Declare it `mapped`, naming the replacement and why the rewrite is an improvement.
- Declare it `dropped`, naming why the content should not exist.

The eval passes when the list is empty. The `dropped` list then doubles as the redesign's content changelog — the one artifact that says, in writing, what the redesign chose to stop saying.

## Wiring it in

Run it per page during the build, and across every page before ship:

```
node evals/content-parity.mjs <page.html> <line>
node evals/content-parity.mjs --all
```

Add `--all` to CI. A redesign branch that drops content fails the build, and the diff shows exactly which strings went.

## Failure modes

**The inventory rots.** The source keeps shipping while the redesign is built. Re-extract before ship and diff the inventory; new source content is new required content, or an explicit decision not to carry it.

**The eval passes on a page nobody rendered.** Presence in HTML is not visibility. Pair the parity eval with a rendered check — content inside a collapsed accordion or a `display: none` block passes a text match while being invisible to users.

**Everything gets declared dropped.** If the `dropped` list grows faster than the `present` count, the redesign is not a redesign. Escalate rather than rubber-stamping reasons.

**Chrome pollutes the inventory.** Nav labels and footer links repeat on every page and drown the real content. Extract them once as structure, not per-page as content.
