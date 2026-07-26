# Plan — Align semantic-organization with the Open Knowledge Format (OKF)

## Source

Google Cloud blog: "How the Open Knowledge Format can improve data sharing."
OKF v0.1 represents knowledge as a directory of markdown files with YAML
frontmatter. One required field: `type`. Cross-links form a relationship
graph. `index.md` enables progressive navigation. Vendor-neutral,
version-controlled, human-readable, agent-parseable.

## Core insight

A skill in this marketplace already is an OKF bundle. Same substrate:
markdown plus YAML frontmatter in version control, cross-linked, dual
human/agent readable. OKF is the named open standard behind the existing
`unix-philosophy.md` "compose via plain text" tenet.

## Locked decisions

- Scope: align format conventions only. No OKF export/import bridge.
- `type:` frontmatter: recommended, rewarded by audit, never penalized.
- Keep git as history source of truth. Skip OKF `log.md`.
- No SemVer bump. Repo is pre-0.1 per CLAUDE-PIP.
- OKF is treated as a pinned external dependency, wrapped behind one
  versioned adapter file. A spec bump edits that one file. (See "OKF as a
  versioned dependency.")

## What the adversarial review changed

Codex flagged three defects in the prior draft. Verification confirmed all
three and surfaced a fourth fact that reshapes the design.

1. The prior S5 parsed markdown links. Zero of the 12 skills use markdown
   links; all reference companion files as code-span path tokens. The check
   would have detected nothing.
2. A "reachable from SKILL.md" verdict threshold contradicts progressive
   disclosure. Fixtures, schemas, templates are intentionally unlinked.
3. Downstream consumers hard-code the audit contract:
   `tools/skillopt/adapters/semantic_organization.py` and
   `tools/skillopt/adapters/atomic_brand.py` both assert "8 dimensions
   (S1-S4, P1-P4)". `README.md` asserts "7 dimensions". The contract is
   already inconsistent (README 7, SKILL.md 8, adapters 8).
4. Consequence: a 9th scored dimension forces churn across both adapters,
   the README, the summary template, and fixtures, on top of an existing
   drift.

Resolution: do not add a scored dimension. Add a gating check.

## Change 1 — Reference-integrity gate (not a scored dimension)

The audit already runs a non-scored gate: the forbidden-layout check, which
can force `broken`. Add reference integrity as a peer gate. The
8-dimension scored contract stays frozen, so both SkillOpt adapters remain
valid without edits.

### Reference grammar (fixes Codex finding 1)

A "reference" in a skill file is any of:
- A code-span path token matching
  `(scripts|references|assets|prompts|templates|schemas|fixtures)/<file>`.
- A markdown link `[text](path)` whose target is a repo-relative file.

The check extracts both forms from SKILL.md and from files under
`references/` and `prompts/`, then resolves each against the filesystem.

### Two file classes (fixes Codex finding 2)

- Operational references: files under `references/` and `prompts/` that
  SKILL.md directs the agent to load. Reachability root is SKILL.md OR a
  folder `index.md`.
- Support files: `fixtures/`, `schemas/`, `templates/`, `assets/`.
  Reachability root is `TESTS.md` OR a folder `index.md`. Never required to
  be linked from SKILL.md.

### Gate outcomes

- Dead reference (a path token that does not resolve): force `broken`.
  Peer to a forbidden layout.
- Orphan operational reference (a `references/` or `prompts/` file no root
  reaches): advisory note, not `broken`.
- Support files: never penalized for being unlinked.

### Staged rollout (fixes Codex finding 2, second half)

1. Implement the check as advisory only. Dry-run across all 12 skills.
2. Fix any real dead references found.
3. Only then wire "dead reference → broken" into the verdict rule.

### Files

- `references/audit-rubric.md` — add the gate definition and the reference
  grammar; extend the `broken` verdict rule to include dead references; add
  the gate line to the Final Audit Summary template.
- `SKILL.md` — add the gate to the audit output-format steps and to the
  Verdicts table `broken` row. Dimension count stays eight.
- `prompts/audit-existing-skill.md` — add the gate step before scoring.
- `TESTS.md` — add a dead-reference test case and an orphan-reference test
  case.
- `fixtures/` — add one fixture with a dead code-span reference and one
  with a dead markdown link, plus expected audits.

Verify: dry-run reports zero dead references across the 12 skills before
the verdict rule is enabled; the dead-reference fixtures return `broken`.

## Change 2 — `index.md` folder convention

OKF uses `index.md` per directory for progressive navigation. It also
serves as an alternate reachability root for Change 1. Recommend `index.md`
for any convention folder above five files.

### Files

- `references/folder-roles.md` — document the convention and its role as a
  reachability root.
- `SKILL.md` — note it in the canonical layout.
- Self-application: add `references/index.md` listing this skill's
  references (seven after Change 4).

Verify: `references/index.md` exists and lists every sibling reference.

## Change 3 — OKF `type:` frontmatter (recommended)

Companion files carry no frontmatter today. Add a minimal `type:` so a
bundle is self-describing file-by-file. Vocabulary owned by
`okf-alignment.md`: `reference | prompt | template | schema | fixture`.
Blast radius is this skill only.

### Files

- `references/okf-alignment.md` — owns the vocabulary (created in Change 4).
- `prompts/scaffold-new-skill.md`, `templates/skill-scaffold.md` — emit
  `type:` in companion-file placeholders.
- `references/audit-rubric.md` — gate rewards `type:` presence; absence is
  not penalized.

Verify: scaffold a test skill; placeholders carry `type:`; a skill without
`type:` loses no points.

## Change 4 — OKF as a versioned dependency (the wrapper)

Localize all OKF coupling behind one file so a spec update is a single
edit. `references/okf-alignment.md` is the sole authority that restates OKF
rules. Every other file cites it instead of embedding OKF specifics.

### `references/okf-alignment.md` carries

- Frontmatter pin: `okf_version: "0.1"`, `okf_source: <blog URL>`,
  `okf_retrieved: 2026-06-13`.
- The OKF→skill mapping table.
- The `type:` vocabulary mapping (OKF `type` field ↔ skill folder roles).
- The OKF principle behind Change 1 (cross-links form a graph), with the
  code-span grammar noted as this marketplace's adaptation.
- A "When OKF changes" checklist: bump the version pin, re-diff the mapping
  table, check for new required fields beyond `type`, update the
  vocabulary. One chokepoint.

### Citations from other files (no restated OKF rules)

- `SKILL.md` — add `okf-alignment.md` to the References list.
- `references/unix-philosophy.md` — cross-link OKF as the named standard
  behind the plain-text tenet.
- `references/audit-rubric.md`, `references/folder-roles.md` — cite
  `okf-alignment.md` for the `type:` vocabulary rather than restating it.

Verify: a grep for OKF version/spec terms outside `okf-alignment.md`
returns only citations, never restated rules.

## Change 5 — Reconcile the pre-existing contract drift

Independent of OKF, the audit contract is inconsistent today. Fix as
hygiene so the gate ships on a clean contract.

### Files

- `skills/semantic-organization/README.md` — "7 dimensions" / "7-dim" →
  "8 dimensions". Add a one-line mention of the reference-integrity gate.
- `prompts/audit-existing-skill.md` — "plugin-layer" → "marketplace-layer"
  to match `audit-rubric.md`.
- Confirm `tools/skillopt/adapters/semantic_organization.py` and
  `atomic_brand.py` stay valid (count unchanged at eight). Update their
  rubric strings only if they describe the gate.
- `fixtures/expected-audit.md` — add the gate line to the expected output.

### Completion gate

Repo-wide grep returns no stale tokens:
`7-dim`, `7 dimensions`, `plugin-layer`, and any dimension count other than
eight in skill docs, prompts, README, fixtures, and adapters.

## Self-application

This skill must pass its own audit at `spec-compliant + marketplace-ready`
after the change:
- No dead references; the gate passes.
- `references/index.md` present (seven reference files).
- Companion files carry `type:` frontmatter (recommended tier).

## Phases

1. Author `references/okf-alignment.md` (versioned wrapper) and
   `references/index.md`.
2. Add the reference-integrity gate and grammar to `audit-rubric.md`,
   `SKILL.md`, `audit-existing-skill.md`, as advisory only.
3. Dry-run the gate across all 12 skills. Fix any real dead references.
4. Enable "dead reference → broken" in the verdict rule.
5. Add `index.md` and `type:` conventions to `folder-roles.md`, scaffold
   prompt, template. Add `type:` to this skill's companion files.
6. Reconcile contract drift (Change 5). Run the completion grep gate.
7. Add fixtures plus expected audits; extend `TESTS.md`.
8. Self-audit. Confirm verdict `spec-compliant + marketplace-ready`.

## Out of scope

- OKF export/import bridge (deferred; possible future sibling skill).
- OKF `log.md` (git is history).
- A 9th scored dimension (rejected in favor of a gate).
- SemVer bump.
- Changes to other skills, except the read-only adapter validation in
  Change 5.

## Review

Implemented 2026-06-13. All eight phases complete.

New files:
- `references/okf-alignment.md` — versioned wrapper, `okf_version: "0.1"`.
- `references/index.md` — folder map and reachability root.
- `fixtures/input-dead-reference-skill.md` — dead-reference fixture.

Edited: SKILL.md, audit-rubric.md, folder-roles.md, unix-philosophy
(citation), audit-existing-skill.md, scaffold-new-skill.md, skill-scaffold
template, README.md, TESTS.md, expected-audit.md, two existing fixtures.
`type:` frontmatter added to 15 companion markdown files.

Architecture outcome: reference integrity is a gate, not a ninth scored
dimension. The 8-dimension contract is frozen, so both SkillOpt adapters
(`semantic_organization.py`, `atomic_brand.py`) needed zero edits.

Verification (evidence):
- Dry-run resolver over all 12 skills: zero genuine dead references.
- README 199 words (≤200). SKILL.md 172 lines (<500).
- Stale-contract grep clean except one legitimate contextual hit.
- All eight SKILL.md references resolve.

Pre-existing defects found, NOT fixed (out of OKF scope):
- `fixtures/input-drifted-skill.md` scores S4=2 with a forbidden `utils/`
  folder, but the rubric scores a forbidden folder S4=1 → `broken`. The
  fixture's expected verdict `spec-compliant, marketplace-drift` is
  inconsistent with its own scores. Only the stale verdict vocabulary was
  reconciled.
- `component-composer` references `<theme>/references/{palette,patterns,
  tokens,criteria}.md`; whether bound theme skills provide these is
  unverified.
