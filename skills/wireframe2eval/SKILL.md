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

The eval runs before the first line of content is carried, when it fails almost completely. That is correct. The failure count is the migration's remaining work, and it only ever goes down.

## 1. EXTRACT

Pull the live content from every source property the redesign consolidates. One extraction per source page, per line of business or section.

Capture only what carries meaning: `h1`, `h2`, `h3`, CTA labels, and paragraphs over 40 characters. Skip nav chrome, cookie banners, and boilerplate — they are structure, not content, and they inflate the inventory until it stops being read.

Extract from the rendered DOM, not the HTML source. Page builders and client-side rendering mean `curl` and the browser disagree, and the browser is what users and crawlers see.

```
agent-browser open "https://<source>/"
agent-browser eval '<extraction expression>'
```

Record one inventory item per element. Never concatenate two elements into one string — see the last failure mode.

Record the source URL and extraction date in the inventory. An inventory with no provenance cannot be re-derived when the source changes.

## 2. INVENTORY

One JSON file, committed, versioned, reviewed like code.

```json
{
  "generated": "YYYY-MM-DD",
  "lines": {
    "<line>": {
      "source": "https://…",
      "page": "pages/index.html",
      "required": { "h1": [], "headings": [], "ctas": [], "paragraphs": [] },
      "mapped":  [{ "from": "…", "to": "…", "reason": "…" }],
      "dropped": [{ "text": "…", "reason": "…" }]
    }
  }
}
```

`required` is the contract. `page` is the file the eval measures. `mapped` and `dropped` are the only two ways out of the contract, and both demand a written reason. A reason field with "n/a" in it is a defect the reviewer should reject.

**Law: the inventory is read-only to whoever is graded by it.** The executor or agent building the pages never edits `content-inventory.json`. Moving a string into `dropped` to turn the eval green is the exact failure the eval exists to catch, committed by the party the eval is watching. Inventory edits come from the extractor, or from a reviewer who did not build the pages, and they land in their own commit. An executor that can edit its own contract has no contract.

## 3. WIREFRAME

The wireframe is the structure the inventory pours into. Build it with real tokens and real chrome, but treat body sections as slots that content fills — the wireframe is a template, not a page.

Never let the wireframe carry invented marketing copy. Placeholder copy reads as finished work in review, and it competes with the real content for the slot it occupies. Use labelled empty slots, or the real source copy, and nothing in between.

A wireframe that previews several variants holds all of them in one file, hidden by CSS. That file is a template and never a page under test. The next section says why.

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

### Prove it fails first

Run the eval before any content is carried, and record the failing count as the baseline. An eval first run after the content is already in place has never been observed to fail, and a check that cannot fail is not a check.

In the reference run the eval returned 87 of 98 MISSING against the placeholder wireframe, then 77 after the first content pass. The first number is what makes the second one mean anything.

```
node evals/content-parity.mjs --all --baseline evals/parity-baseline.json
```

The first run writes the baseline. Every run after fails on any per-line increase, so an item cannot regress from `present` to `MISSING` while the overall count is still large.

### The union trap

Measure parity against the page a user gets, never against a template that holds every variant at once.

A multi-variant wireframe keeps all variants in one file and hides the inactive ones with CSS. The eval strips tags and matches text, so it counts every variant's copy as present no matter which variant is active. The per-line number is a union across variants. It is inflated, and it is not a score.

Verified on the reference run. The wireframe hides variants with `[data-when] { display: none }` and reveals them with `html[data-line="X"] [data-when~="X"]`, gating 49 elements in one file. Matching the raw template scores storage 21, marine 17, RV 13. Matching the same lines against the rendered text of the projected single-variant page scores 20, 14, 11. Seven of the 51 `present` items — `Service`, `Get a Free Demo`, `Slips & Storage`, `POS & Billing`, `Reporting & Back Office`, `Channel Manager`, `Enterprise` — sat in the DOM and were invisible to the variant that claimed them.

The error runs both ways. One storage `h1` matched the rendered page and missed the template, because the marine and RV pre-titles sit between its two halves in source order.

The fix is to project the template into one file per variant and run the eval on the projection. Until the projector exists, run against rendered text and treat the template number as an upper bound.

The eval warns when it sees the variant attribute in a page it is matching as raw HTML. Set the attribute with `--variant-attr=<name>` if yours is not `data-when`.

### Presence is not visibility

Content inside a collapsed accordion, a `display: none` variant block, or a zero-height container matches the text eval while being invisible to users and ambiguous to crawlers. Pair every parity run with a rendered check.

```
agent-browser open "file:///abs/path/page.html"
agent-browser set viewport 1280 900
agent-browser eval "JSON.stringify(document.body.innerText)" > rendered.json
node evals/content-parity.mjs rendered.json <line> --rendered
```

`innerText` returns only what layout renders, so hidden variants and collapsed panels drop out of the match. `textContent` does not — it returns the union, which is the bug.

Set the viewport with `agent-browser set viewport <w> <h>`. The `--viewport` flag on `open` is silently ignored when a page is already open: verified, the page stayed at 1280x900 after `open … --viewport 375x812`, and `set viewport 375 812` moved it. `agent-browser eval` prints its result as JSON, so a `JSON.stringify` result arrives double-encoded; the eval unwraps both layers.

Run the rendered check at the narrowest supported width too. A block that renders at 1280 and collapses at 375 is visible content on one device and hidden content on the other.

## 5. DECIDE

Work the `MISSING` list down. Each item gets exactly one of three dispositions:

- Carry it into the new page verbatim.
- Declare it `mapped`, naming the replacement and why the rewrite is an improvement.
- Declare it `dropped`, naming why the content should not exist.

**A deferral carries a number.** A migration that ships in phases records the exact remaining `MISSING` count per line and names the phase that closes it. "Body content lands later" is a loss. "185 items remaining — 77 storage, 59 marine, 49 RV — closed by mission 002" is a plan. The number goes in the ledger and in the baseline file, so the next phase inherits a target instead of a feeling.

The eval passes when the list is empty. The `dropped` list then doubles as the redesign's content changelog — the one artifact that says, in writing, what the redesign chose to stop saying.

## Wiring it in

Run it per page during the build, and across every page before ship:

```
node evals/content-parity.mjs <page.html> <line>
node evals/content-parity.mjs rendered.json <line> --rendered
node evals/content-parity.mjs --all --baseline evals/parity-baseline.json
```

| Exit | Meaning |
|---|---|
| 0 | Every inventory item accounted for |
| 1 | Content lost, or a count regressed against the baseline |
| 2 | Bad usage, missing inventory, or a line with no `page` declared |
| 3 | Pages not emitted yet — skipped, and skipped is not passed |

Add `--all` to CI and treat 3 as a failure until every page exists. A redesign branch that drops content fails the build, and the diff shows exactly which strings went.

## Failure modes

**The inventory rots.** The source keeps shipping while the redesign is built. Re-extract before ship and diff the inventory; new source content is new required content, or an explicit decision not to carry it.

**Everything gets declared dropped.** If the `dropped` list grows faster than the `present` count, the redesign is not a redesign. Escalate rather than rubber-stamping reasons.

**Chrome pollutes the inventory.** Nav labels and footer links repeat on every page and drown the real content. Extract them once as structure, not per-page as content.

**Normalisation hides a real match.** A concatenated string matches only if nothing sits between its parts in source order, and in a multi-variant template something usually does. Extract one item per element, and the eval stops reporting `MISSING` for content that is on the page.
