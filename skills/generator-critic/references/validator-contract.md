# Validator Contract

Abstract interface for the critic role in a generator-critic loop. The
critic scores a candidate artifact against declared criteria. A concrete
consumer implements artifact-specific mechanical checks and chooses an
LLM-judge prompt; the dispatch and aggregation logic below is shared.

## Two-layer hybrid

### Mechanical layer

Deterministic checks implemented as pure functions over extracted
artifact data. Each check has a criterion id and returns the shared
validator output shape (see below).

The consumer provides:
- A registry of `criterion_id → check_function`
- An adapter that extracts artifact data and dispatches to the check
  (e.g., for HTML artifacts: `runInBrowser` reads the DOM via
  `getBoundingClientRect`, `getComputedStyle`, etc.)

The consumer's checks must be:
- **Pure** — operate on plain-object inputs only; no I/O, no globals
- **Deterministic** — same input always returns same output
- **Fast** — sub-second per check is the target

### LLM-as-judge layer

A vision LLM call for criteria that cannot be checked mechanically. The
consumer provides:
- A prompt template that includes the criterion text + the rendered
  artifact (e.g., screenshot, source, tree)
- A response schema matching the output shape below

## Dispatch rule

For each criterion in the active rule set:

1. If a built-in mechanical check exists for this criterion id, run it
   first. Trust the result.
2. If the mechanical check throws or returns an error, fall back to
   LLM-as-judge for this criterion.
3. If no built-in mechanical check exists for this criterion id, use
   LLM-as-judge.

Mechanical is authoritative when available. LLM-judge fills the gaps.

## Output shape

Every check (mechanical or LLM) returns:

```json
{
  "id": "criterion_id",
  "result": "pass" | "fail",
  "context": "<consumer-specific scope label, e.g., viewport>",
  "evidence": "<one-line description of what failed; optional on pass>",
  "suggested_fix": "<one-line hint for the drafter; optional on pass>"
}
```

The `context` field is consumer-defined. For HTML artifacts it's a
viewport label (`"mobile" | "tablet" | "desktop"`); for code artifacts
it might be a file path; for schemas it might be a type name.

## Iteration per context

If the consumer defines multiple contexts (multiple viewports, multiple
target files, multiple schema variants), the validator runs the full
criterion set in each context. Results are tagged with the context label
and concatenated.

## Aggregation

After all contexts have been validated, the orchestrator concatenates
the failure lists verbatim with context labels preserved. Same criterion
failing in multiple contexts appears multiple times. No deduplication —
the drafter needs per-context detail.

## LLM-judge prompt template (abstract)

```
You are a critic for <artifact-type>. Below are the criteria to check.
For each criterion id listed as "check this", evaluate the candidate.
Return ONLY a JSON array matching this schema:

[{"id": "...", "result": "pass" | "fail",
  "context": "<context label>",
  "evidence": "...", "suggested_fix": "..."}]

Criteria to check:
<concatenated criterion text>

Context: <context label>

Candidate: <attached artifact / screenshot / source>
```

The consumer's validator-protocol.md fills in artifact-type, criterion
text source, and context label scheme.

## Consumer responsibility

The consumer's `validator-protocol.md` declares:
- Which criteria are mechanical (and where the implementations live)
- Which criteria are LLM-judge (and the prompt extension)
- The context label scheme
- The artifact extraction adapter

The consumer never weakens the abstract dispatch rule (mechanical first,
LLM fallback for unimplemented).
