# Spec vs. Conventions

Two distinct sources of authority govern a skill in this marketplace.
Confusing them produces over-engineered standards or non-portable skills.

## The two layers

### Spec layer

The Agent Skills specification at https://agentskills.io/specification.
This is the truth that makes a skill a skill. Every skill, regardless of
where it ships, must comply. Spec rules are non-negotiable.

What the spec defines:
- One required file: `SKILL.md` with frontmatter (`name`, `description`)
- Three optional canonical folders: `scripts/`, `references/`, `assets/`
- Naming rules for the skill name
- Body content rules (≤500 lines recommended)
- Progressive disclosure model: metadata always, body on activation, resources on demand

What the spec does NOT define:
- README.md (presence, length, content)
- TESTS.md (presence, content)
- Plugin manifest (`plugin.json`)
- Marketplace layout
- Audit rubrics
- Verdict semantics

### Convention layer

Marketplace-specific rules layered on top of the spec. Conventions exist
to make a marketplace coherent, not to validate a skill.

Conventions in infolog-io:
- Plugin wrapper: `plugins/<name>/skills/<name>/`
- `.claude-plugin/plugin.json` at plugin root (required by Claude Code, not by spec)
- `README.md` ≤200 words at plugin root (marketplace listing)
- `TESTS.md` at plugin root (forces "definition of done")
- Folder naming for non-spec folders if any (kebab-case)
- Semantic Organization audit rubric (this skill)

Conventions can evolve. The spec is fixed (until Anthropic revises it).

### Accepted non-spec folders in this marketplace

Some skills in this marketplace use folders that the spec does not name.
These are accepted as marketplace conventions and the audit does not
penalize them when used per their stated purpose. They are non-canonical:
new skills should prefer the spec folders unless a clear need arises.

| Folder | Purpose | Spec equivalent (preferred) |
|---|---|---|
| `prompts/` | Mode-specific instruction files when a skill has many operating modes | Could fold into SKILL.md sections, or move to `references/` |
| `templates/` | Canonical output markdown templates | `assets/` |
| `schemas/` | JSON Schema validation contracts | `assets/` |
| `fixtures/` | Input + expected-output test pairs | `assets/` or omitted |

Existing skills (`jtbd-prd`, `semantic-organization`) that use these
folders score 5 on folder discipline as long as they are documented in the
skill's SKILL.md under a "Folder rationale" section or are referenced from
SKILL.md.

New skills should default to spec folders. Use the convention folders only
when the content does not fit `references/`, `assets/`, or `scripts/`.

## Why the distinction matters

### A spec-compliant skill is portable

A skill that follows the spec works in:
- Claude Code (via plugins)
- Claude Apps (via skill upload)
- Any agent that implements the spec
- Custom toolchains

A skill that follows only your local marketplace conventions does not.

### Convention drift is recoverable; spec drift is not

Missing a `TESTS.md`? Add one. Five minutes.
Naming a folder `src/` instead of `scripts/`? Rename. Two minutes.

These are convention drifts. Easy to fix.

Naming the skill `My_PDF_Skill` instead of `pdf-processing`? That breaks
the spec. Any agent that validates against the spec rejects it. Renaming
breaks every reference.

Spec compliance is the floor. Conventions are the polish.

## The contract per layer

### Skill-layer contract (spec)

Every consumer can assume:
- Top-level file `SKILL.md` exists
- Frontmatter has valid `name` and `description`
- Folder structure uses spec names where folders exist
- Body content is under 500 lines (recommended) or has been broken into references

### Plugin-layer contract (marketplace)

Every consumer in this marketplace can assume:
- `plugin.json` manifest exists for installation
- `README.md` describes what + when + install in under 200 words
- `TESTS.md` declares end conditions before ship

## Where my earlier standard went wrong

The first version of this audit rubric required five sub-folders
(`references/`, `prompts/`, `templates/`, `schemas/`, `fixtures/`) at the
skill layer. Only `references/` is in the spec. The other four were
invented and required for skills that had no need for them.

The correction: spec mandates `SKILL.md`. The three optional spec folders
are `scripts/`, `references/`, `assets/`. Anything else is a convention,
and conventions cannot be required at the skill layer.

Single-rule meta-skills (claude-pip, estimatrix) are spec-compliant with
just `SKILL.md`. The marketplace adds plugin.json + README + TESTS. That
is the minimum bar.

## When to escalate from convention to spec proposal

If a convention has been useful across ≥5 skills and proves portable, it
becomes a candidate for proposal to Anthropic for inclusion in the spec.

Until then, conventions stay local to this marketplace.

## Reading the audit output

The audit emits two scores per skill:
- Skill-layer (spec compliance) — 4 dimensions
- Plugin-layer (marketplace conventions) — 4 dimensions

A skill can be `spec-compliant, marketplace-drift` — compliant with
Anthropic's spec but missing infolog-io conventions. That is shippable
outside this marketplace; not yet shippable inside it.

A skill that fails the skill layer is broken regardless of the plugin
layer.
