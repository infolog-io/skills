# Spec vs. Conventions

Two distinct sources of authority govern a skill in this marketplace.
Confusing them produces over-engineered standards or non-portable skills.

The clean answer: **both live in the same folder.** There is no separate
plugin-wrapper directory. A skill is simultaneously spec-compliant AND
marketplace-installable from one location.

## The two sources of authority

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

### Marketplace layer

Marketplace-specific files layered into the same skill folder.
Conventions exist to make a marketplace coherent and to enable
`claude plugin install`. They live next to spec-required files —
not in a wrapper directory.

Conventions in infolog-io (all live inside `skills/<name>/`):
- `.claude-plugin/plugin.json` — Claude Code plugin manifest
- `README.md` ≤200 words — marketplace listing
- `TESTS.md` — end conditions and test cases
- Convention folders (`prompts/`, `templates/`, `schemas/`, `fixtures/`) when a skill has multiple modes
- Folder naming rules (kebab-case throughout)
- Semantic Organization audit rubric (this skill)

Conventions can evolve. The spec is fixed (until Anthropic revises it).

## The canonical layout (both layers in one folder)

```
<marketplace-repo>/
├── .claude-plugin/
│   └── marketplace.json                ← marketplace manifest
├── skills/
│   └── <skill-name>/                   ← spec + marketplace in one folder
│       ├── .claude-plugin/
│       │   └── plugin.json             ← marketplace
│       ├── SKILL.md                    ← spec (required)
│       ├── README.md                   ← marketplace
│       ├── TESTS.md                    ← marketplace
│       ├── scripts/                    ← spec (optional)
│       ├── references/                 ← spec (optional)
│       ├── assets/                     ← spec (optional)
│       ├── prompts/                    ← convention (optional)
│       ├── templates/                  ← convention (optional)
│       ├── schemas/                    ← convention (optional)
│       └── fixtures/                   ← convention (optional)
└── ...
```

This mirrors Anthropic's reference repo at
https://github.com/anthropics/skills, with `.claude-plugin/plugin.json`
added inside each skill folder to enable Claude Code plugin install.

## Forbidden layouts

The audit returns `broken` on these (regressions to old wrapper forms):

| Forbidden | Why |
|---|---|
| `plugins/<name>/skills/<name>/SKILL.md` | Double-nested wrapper; not canonical |
| `plugins/<name>/SKILL.md` | Wrong top-level folder name (should be `skills/`) |
| `.claude-plugin/plugin.json` at marketplace repo root | Manifest belongs inside each skill folder |

## Accepted convention folders

| Folder | Purpose | Spec equivalent (preferred when fit) |
|---|---|---|
| `prompts/` | Mode-specific instruction files | Could fold into SKILL.md sections or `references/` |
| `templates/` | Canonical output markdown templates | `assets/` |
| `schemas/` | JSON Schema validation contracts | `assets/` |
| `fixtures/` | Input + expected-output test pairs | `assets/` or omitted |

Skills that use these convention folders score 5 on folder discipline
when each is used per its stated purpose.

New skills should default to spec folders. Use convention folders only
when the content does not fit `references/`, `assets/`, or `scripts/`.

## Why the distinction matters

### A spec-compliant skill is portable

A skill that follows the spec works in:
- Claude Code (via plugins)
- Claude Apps (via skill upload)
- Any agent that implements the spec (Codex, Cursor, OpenHands, etc.)
- Custom toolchains

A skill that requires a wrapper directory is harder to port.

### Convention drift is recoverable; spec drift is not

Missing a `TESTS.md`? Add one. Five minutes.
Naming a folder `src/` instead of `scripts/`? Rename. Two minutes.

These are convention drifts. Easy to fix.

Naming the skill `My_PDF_Skill` instead of `pdf-processing`? That breaks
the spec. Any agent that validates against the spec rejects it. Renaming
breaks every reference.

Spec compliance is the floor. Conventions are the polish.

## The contract per layer

### Spec-layer contract

Every consumer can assume:
- Top-level file `SKILL.md` exists at `skills/<name>/SKILL.md`
- Frontmatter has valid `name` and `description`
- Folder structure uses spec names where folders exist
- Body content is under 500 lines (recommended) or has been broken into references

### Marketplace-layer contract (infolog-io)

Every consumer in this marketplace can assume:
- `.claude-plugin/plugin.json` manifest exists inside the skill folder
- `README.md` describes what + when + install in under 200 words
- `TESTS.md` declares end conditions before ship

## Where the earlier standard went wrong

The first version of this rubric required five sub-folders (`references/`,
`prompts/`, `templates/`, `schemas/`, `fixtures/`) at the skill layer. Only
`references/` is in the spec.

The second version introduced a `plugins/<name>/skills/<name>/` wrapper
"for marketplace clarity." That wrapper inverts the Anthropic convention
and buries SKILL.md two levels deep.

**The correction:** spec mandates `SKILL.md`. The three optional spec
folders are `scripts/`, `references/`, `assets/`. Marketplace files
(`plugin.json`, `README.md`, `TESTS.md`) live in the SAME folder. No
wrapper.

## When to escalate from convention to spec proposal

If a convention has been useful across ≥5 skills and proves portable, it
becomes a candidate for proposal to Anthropic for inclusion in the spec.

Until then, conventions stay local to this marketplace.

## Reading the audit output

The audit emits two scores per skill:
- Skill-layer (spec compliance) — 4 dimensions
- Marketplace-layer (conventions) — 4 dimensions

A skill can be `spec-compliant, marketplace-drift` — compliant with
Anthropic's spec but missing infolog-io marketplace files. That is
shippable outside this marketplace; not yet shippable inside it.

A skill that fails the spec layer is broken regardless of marketplace
layer.
