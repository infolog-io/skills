# Unix Philosophy for Skills

The Agent Skills spec is loosely modeled on Unix conventions: small,
composable, plain-text, do one thing well. This reference applies the
classic Unix tenets to skill design.

## The four tenets that matter most

### 1. Do one thing and do it well

A skill names one purpose. If a skill needs to choose between two unrelated
audit rubrics, two verdict types, or two output artifacts, it is two
skills wearing a costume.

Tests:
- Can you describe the skill's purpose in one sentence with one verb?
- Does the skill emit one canonical output type?
- Does the skill apply one rubric or framework?

If any answer is no, split the skill.

Examples in this marketplace:
- `jtbd-prd` does one thing: validate customer need via JTBD evidence → Job Article
- `tufte-love` does one thing: audit a data visualization against Tufte principles
- `estimatrix` does one thing: enforce the T-shirt sizing rule
- `atomic-brand` (proposed) does *many* things — that is why it is a skill family, not a skill

### 2. Compose with others through clean interfaces

Skills cooperate. The output of one is the input of another.

Clean interface = plain text that another skill can parse without
prearrangement. Markdown for prose. JSON for structured data. Both
human-readable and machine-readable.

Tests:
- Could another agent consume this skill's output without special parsing?
- Is the output schema declared (frontmatter, JSON schema, or convention)?
- Does the skill avoid emitting binary or proprietary formats unless absolutely required?

Examples:
- `jtbd-prd` emits a markdown Job Article + a JSON schema-validated structure → consumable downstream
- `tufte-love` emits a markdown audit → consumable as a code-review comment, a doc section, or input to another agent
- `learn2kern` (planned) emits a type scale as JSON tokens → consumable by any tool that imports W3C design tokens

### 3. Prefer plain text

Plain text is the universal interface. Binary formats lock skills to one
tool.

- SKILL.md is markdown — plain text
- References are markdown — plain text
- Schemas are JSON — plain text
- Even when scripts emit binaries (a generated image, a PDF), the
  *configuration* and *intent* live in plain text

If a skill needs binary inputs (an image to audit, a PDF to extract), the
binary lives in `assets/` or is passed as a path/URL. The skill's logic
stays in plain text.

### 4. Build small, simple tools; avoid monoliths

The Agent Skills spec encodes this directly via progressive disclosure:
- Metadata: ~100 tokens, always loaded
- SKILL.md body: <5000 tokens recommended, loaded on activation
- References: loaded on demand

A SKILL.md that approaches 500 lines is at the boundary of "still small."
Beyond that, split into reference files. The skill is not the body — the
skill is what gets loaded when needed.

Tests:
- Is SKILL.md under 500 lines?
- Could the skill be understood by reading just the body, with references as appendix?
- Does any single reference file exceed what one person can read in one sitting?

## Secondary tenets

### Make every program a filter

Where possible, skills take input and emit transformed output. They do not
maintain state, do not require setup, do not hold conversational context.

Pure-filter examples:
- `tufte-love` takes a chart description, returns an audit. Stateless.
- `estimatrix` takes a "how long" question, returns a T-shirt size. Stateless.

Not-quite-filter examples (legitimate):
- `jtbd-prd` accumulates evidence across an interview session. Has state, but the state is the artifact (Job Article), not hidden.

### Avoid captive interfaces

A skill should not lock the user into a single way of using it.

- Triggers list multiple phrases, not one
- Outputs are inspectable, not opaque
- Errors are explainable, not blackbox

### Reuse before reinvent

If another skill does the job, defer to it. Cross-reference, do not reimplement.

Examples:
- An `atomic-charts` skill is unnecessary because `tufte-love` already does that. Cross-reference instead.
- A new "voice" skill should defer to the lexicon-check skill family rather than restating its rules.

## Anti-patterns the philosophy rejects

| Pattern | Why it fails |
|---|---|
| A skill that does both audit AND generation AND refactor | Three skills wearing one name |
| A skill whose output requires a specific consumer | Captive interface |
| A skill that hides its logic in a closed-source binary script | Violates plain-text tenet |
| A 2000-line SKILL.md | Violates small/progressive-disclosure tenet |
| A skill that demands setup or authentication to evaluate triggers | Captive interface |

## When the philosophy conflicts with completeness

Tension: "do one thing well" pushes toward many small skills, but reality
often calls for clusters of related capabilities.

Resolution:
- Build one skill at a time
- Spin out a sibling when migration triggers fire (see `references/migration-triggers.md`)
- Use a parent skill as a documented index of the family

Example: `atomic-brand` starts as one skill with concern-folders inside.
When any concern folder meets migration triggers (≥5 prompts, own rubric,
own verdicts), it spins out as a sibling (`atomic-motion`, `atomic-print`).
The parent skill keeps a one-paragraph reference to the spinout. Family
cohesion + small-tools tenet, satisfied together.

## The shortest summary

> "Write programs that do one thing and do it well. Write programs to work
> together. Write programs to handle text streams, because that is a
> universal interface." — Doug McIlroy

Translated for skills:

- Write skills that do one thing and do it well.
- Write skills to work together via markdown and JSON.
- Keep SKILL.md small; push detail to references loaded on demand.
