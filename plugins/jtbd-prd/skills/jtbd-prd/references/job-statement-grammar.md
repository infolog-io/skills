# Job Statement Grammar

## Canonical shape

```
When [context], I want to [motivation], so I can [outcome].
```

Three slots. All three are required. Missing any slot means the statement is
not yet a job — it is a fragment.

## Slot definitions

### `[context]`

The triggering situation. Specific enough that two readers would picture the
same scene. Includes time, place, role, prior event, or constraint.

Good:
- "When a pull request has been open for more than 24 hours without review"
- "When I land in a city I have never visited"
- "When the data import fails halfway through a 10,000-row file"

Bad (too abstract, fails the "two readers, same scene" test):
- "When I'm working"
- "When I need help"
- "When using the app"

### `[motivation]`

The verb-and-object the customer is reaching for. Must be an action, not a
state.

Good:
- "find a teammate who has context on the change"
- "decide which restaurant to walk to"
- "recover the rows that did import and retry only the failed ones"

Bad:
- "be productive" (state, not action)
- "have a good time" (state)
- "use the feature" (circular)

### `[outcome]`

The progress made when the motivation is satisfied. Must be observable —
something the customer or a third party could measure or witness.

Good:
- "the PR can be merged before standup"
- "I sit down to eat within 20 minutes of landing"
- "the import completes without losing my place"

Bad:
- "feel less frustrated" (not observable from outside)
- "have a better experience" (vague)
- "save time" (no anchor)

## Validation rules

| Rule | Pass | Fail |
|---|---|---|
| Each slot has ≥4 words of specificity | "When the import fails halfway through a large file" | "When I'm stuck" |
| `[motivation]` starts with a verb | "find a teammate who…" | "frustration with…" |
| `[outcome]` is observable | "merged before standup" | "feel productive" |
| Statement does not name your product | "find context on the change" | "use our review dashboard" |
| Statement does not name a persona | "When a PR has been open >24h" | "When a senior engineer…" |

## Worked transformations

### Bad → Good

| Bad | Why it's bad | Good rewrite |
|---|---|---|
| "Users want faster search" | feature, no context, no outcome | When searching across 5+ years of archive, I want to find a known document in under 10 seconds, so I can cite it in a live meeting |
| "Admins want better permissions" | feature, vague | When onboarding a new contractor, I want to grant time-boxed access to specific repos, so I can avoid leaving stale permissions after the contract ends |
| "Make the app faster" | not a job at all | When pulling up customer history on a sales call, I want the page to load before the customer finishes their question, so I can answer with the data in front of me |

## Negative grammar — phrases to reject

If the extractor produces any of these forms, mark the output as malformed:

- "Users want our product to…"
- "Customers should…"
- "It would be nice if…"
- "I think people would…"
- "Make X easier"
- "Improve Y"
- Any sentence without all three slots

## Length guidance

- `[context]`: 6–20 words
- `[motivation]`: 4–15 words
- `[outcome]`: 6–20 words
- Total: 20–50 words

Shorter than 20 words usually means slots are underspecified. Longer than 50
usually means multiple jobs are tangled and need splitting.
