# Self-Improvement Policy

## Meaning of self-improving

This skill improves through persistent, inspectable project memory. It does not train model weights and it does not silently rewrite its own canonical instructions.

The public bundle includes an approved baseline in `references/learned-rules.md` and compact provenance under `assets/training/`. New project feedback belongs in project state so one project's preferences do not silently alter the distributed skill.

## State directory

Create and read:

```text
.Brendan-Drawing-Style-Skill/
  learned-rules.md
  candidate-rules.md
  feedback.jsonl
  structure-examples.jsonl
  source-additions/
    manifest.json
    style/
    lettering/
  runs/
```

## Promotion rules

- Explicit user statements such as “always,” “never,” “make this canonical,” or “add this to the style” may be promoted immediately with `--user-approved`.
- Repeated failure tags become candidates after two occurrences; candidates are not active rules.
- Promote a candidate only after user approval.
- A new style source must be original Brendan art. Add approved generated or reconstructed references as `kind: structure` with `style_authority: false`.

## Anti-corruption rules

- Never add generated artwork to style or lettering authority.
- Never weaken thresholds to manufacture a pass.
- Never infer a global preference from one ambiguous reaction.
- Never overwrite bundled source art.
- Accepted generated images can be logged only as `structure_only: true`.
- Learned project rules may tighten canonical rules, but may not contradict actual source art without explicit user instruction.

## Feedback tags

Recommended tags:
- `generic-typography`
- `pastel-drift`
- `cream-background`
- `drawing-too-clean`
- `corporate-infographic`
- `eye-overuse`
- `robot-overuse`
- `box-overuse`
- `icon-repetition`
- `too-much-microcopy`
- `missing-requirement`
- `incoherent-flow`
- `lazy-ai-rendering`
- `not-interesting`
