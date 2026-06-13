---
type: reference
okf_version: "0.1"
okf_source: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/
okf_retrieved: 2026-06-13
---

# OKF Alignment

This file is the single authority for how this marketplace aligns with the
Open Knowledge Format (OKF). No other file restates OKF rules. They cite
this one. A spec bump is edited here, then propagates through citations.

## The insight

A skill in this marketplace is already an OKF bundle. OKF v0.1 represents
knowledge as a directory of markdown files with YAML frontmatter, in
version control, cross-linked, readable by humans and parseable by agents.
A skill is the same substrate plus two added layers: the Agent Skills spec
and this marketplace's conventions. OKF is the named open standard behind
the "compose via plain text" tenet in [unix-philosophy.md](unix-philosophy.md).

Confidence: high. Source is the OKF v0.1 announcement, retrieved 2026-06-13.

## OKF to skill mapping

| OKF v0.1 concept | Skill equivalent | Notes |
|---|---|---|
| Directory of markdown + YAML frontmatter | The skill folder | Identical substrate. |
| Required `type` field on every concept | `type:` on companion files | Recommended tier here, not required. See vocabulary below. |
| Cross-links form a relationship graph | References between SKILL.md and companion files | This marketplace uses code-span path tokens, not markdown links. See "Reference grammar". |
| `index.md` per directory | `index.md` per convention folder | Recommended above five files. Serves as a reachability root. See [folder-roles.md](folder-roles.md). |
| `log.md` chronological history | Not adopted | Git history is the source of truth. See [folder-roles.md](folder-roles.md). |
| Vendor-neutral, portable, open | Plain-text, composable skill | See [unix-philosophy.md](unix-philosophy.md). |
| Producer and consumer separated | Skill emits markdown + JSON another agent consumes | Clean-interface tenet. |

## The `type:` vocabulary

OKF requires one field: `type`. This marketplace maps `type` to the file's
folder role. Use these values in companion-file frontmatter.

| `type:` value | Folder | Role |
|---|---|---|
| `reference` | `references/` | Domain knowledge, frameworks, lookup tables. |
| `prompt` | `prompts/` | Mode-specific instruction file. |
| `template` | `templates/` | Canonical output shape. |
| `schema` | `schemas/` | JSON Schema contract. |
| `fixture` | `fixtures/` | Test input or expected output. |

The folder already encodes role. `type:` makes a file self-describing when
read outside its folder, which is what an OKF consumer needs.

## Reference grammar

OKF turns a directory into a graph through cross-links. This marketplace
does not use markdown links in SKILL.md. It uses code-span path tokens.
The reference-integrity gate in [audit-rubric.md](audit-rubric.md) resolves
both forms:

- A code-span path token: `references/<file>`, `prompts/<file>`,
  `templates/<file>`, `schemas/<file>`, `fixtures/<file>`, `scripts/<file>`,
  `assets/<file>`.
- A markdown link `[text](path)` to a repo-relative file.
- A cross-skill token with a sibling-skill prefix: `<skill-name>/references/<file>`.
  Resolved against the marketplace `skills/` root, not the local folder.

OKF-native bundles favor markdown links. Skills favor code-span tokens.
The gate accepts both so a skill stays consumable by OKF tooling.

The gate does not resolve four categories. They are not references:

- Placeholders: any token containing `<...>`, e.g. `<theme>/references/tokens.md`.
- Globs: any token containing `*`, e.g. `assets/template-*.json`.
- Illustrative paths inside example trees, code blocks, or prose lists.
- The grammar's own documentation, e.g. `[text](path)`.

A dry-run resolver over all 12 skills on 2026-06-13 found zero genuine dead
references. Every raw match fell into the four exempt categories above. A
mechanical resolver over-reports these, so the auditing agent applies the
exemptions; the resolver only aids it. Confidence: high.

## When OKF changes

OKF is a pinned external dependency. When Google ships a new version,
update this file only, then run the citation check.

1. Bump `okf_version` in this file's frontmatter.
2. Re-fetch `okf_source`. Update `okf_retrieved`.
3. Diff the new spec against the mapping table. Update changed rows.
4. Check for new required fields beyond `type`. Decide adopt or defer.
5. Update the `type:` vocabulary if OKF's type model changed.
6. Run: `grep -rn "OKF\|okf_version\|Open Knowledge Format" skills/semantic-organization`
   outside this file. Every hit must be a citation, never a restated rule.

## Wrapping rule

The whole point of this file is to localize OKF coupling. If OKF specifics
appear anywhere else in the skill, that is drift. Move the rule here and
leave a citation behind.
