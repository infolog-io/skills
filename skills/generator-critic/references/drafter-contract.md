# Drafter Contract

Abstract interface for the drafter role in a generator-critic loop. A
concrete consumer (e.g., `component-composer`) implements an
artifact-specific drafter that satisfies this contract.

## Role

The drafter is an LLM agent that emits a single artifact matching the
consumer's declared format and rules. It does not orchestrate; it does
not validate; it does not decide when to stop. It accepts inputs,
produces output, and trusts the orchestrator with everything else.

## Iteration 1 input

The drafter receives:

1. **Job description** — natural-language goal for the artifact.
2. **Data / source material** — whatever the artifact is built from
   (a dataset, a code change, a transcript, a spec).
3. **Format config** — concrete rules the artifact must follow (output
   format, style guide, naming conventions, structural requirements).
   In `component-composer` this is `output-style.md` + theme palette.
4. **Quality criteria** — the rules the critic will use to score the
   output. The drafter is responsible for proactive compliance, not
   discovery during validation.
5. **Optional starting template** — a skeleton the drafter may freely
   modify.

The consumer's drafter-protocol.md specifies the concrete shape of each
input.

## Iteration N input (N > 1)

All iteration-1 inputs plus:

1. **Previous artifact source** — the full output from iteration N-1,
   verbatim.
2. **Validator failure list (JSON)** — every `{ id, result: "fail",
   evidence, suggested_fix, ...context }` from the critic.
3. **Orchestrator NL summary** — one line per failure, suitable for a
   chat context. The consumer's loop-protocol generates this from the
   failure list before passing to the drafter.

## Output

One artifact matching the format config. Nothing else — no preamble, no
explanation, no markdown wrapper. The orchestrator parses the artifact
directly.

## Behavior rules

These are abstract; consumers may add format-specific rules. None of the
abstract rules may be overridden.

1. **Address every failure.** On iteration N, the drafter must respond
   to every entry in the failure list. Silent dismissals create stuck
   loops.
2. **No new failures.** When fixing one failure, do not introduce
   another. Verify mentally before emitting.
3. **Preserve intent.** Do not rewrite the entire artifact between
   iterations unless the previous structure is unsalvageable. Prefer
   surgical edits.
4. **Trust the config.** Do not invent fields, classes, tokens, or
   structural patterns that are not in the format config or already
   present in the previous artifact.
5. **Output the artifact only.** The orchestrator does not parse natural
   language from the drafter response.

## Failure handling

If the drafter cannot satisfy a failure (e.g., a criterion conflicts
with the data), it emits the artifact as-is and the loop detects stuck
state on the next iteration. The drafter does not raise exceptions or
emit error messages — it produces what it can produce.

## Consumer responsibility

The consumer's `drafter-protocol.md` extends this contract with
format-specific rules (e.g., HTML structural requirements, code style,
schema discipline). The consumer never weakens the abstract behavior
rules above.
