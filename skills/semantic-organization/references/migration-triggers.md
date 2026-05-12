# Migration Triggers

Folders grow. Sometimes a folder becomes a full skill in disguise. This
reference defines when a folder should be promoted to a sibling skill and
when it should stay where it is.

## The decision tree

```
Should this folder become its own sibling skill?

│
├─ Does it have its own audit rubric or verdict semantics?
│   ├─ Yes → promote-to-sibling-skill
│   └─ No  → continue
│
├─ Does it have ≥5 prompts inside it?
│   ├─ Yes → promote-to-sibling-skill
│   └─ No  → continue
│
├─ Does it have its own user-facing triggers separate from the parent?
│   ├─ Yes → promote-to-sibling-skill
│   └─ No  → continue
│
├─ Would it install and operate without the parent skill?
│   ├─ Yes → promote-to-sibling-skill
│   └─ No  → continue
│
├─ Does it already have a manifest (`.claude-plugin/plugin.json`)?
│   ├─ Yes → already-its-own-skill — move it out of the parent
│   └─ No  → stay-as-folder
```

## Trigger conditions (any one promotes)

| # | Condition | Why this triggers promotion |
|---|---|---|
| 1 | Folder has its own audit rubric (scored dimensions) | Rubrics are sibling-skill-scale work |
| 2 | Folder has ≥5 prompt files | Five prompts means a real surface area |
| 3 | Folder has its own user-facing trigger phrases | Users will look for it by name |
| 4 | Folder has independent verdict semantics (validated/drifting/broken etc.) | Verdicts define a skill, not a sub-component |
| 5 | Folder would install and run without the parent | True independence test |
| 6 | Folder has its own README or documentation set | The folder is already documented as standalone |
| 7 | Folder has its own version history different from parent | Versioning divergence is a strong signal |

## Anti-triggers (folder should stay)

| Condition | Why it stays |
|---|---|
| Folder has 1–4 prompts only | Below the surface-area threshold |
| Folder imports heavily from parent's references | Coupling means it isn't independent |
| Folder is a configuration variant of the parent | Variants are folders, not skills |
| Folder is purely test data or scaffolding | Fixtures and templates never become skills |
| Folder's only purpose is to organize within the parent | Organizational sub-folders stay where they are |

## Worked examples

### Example 1 — promote

A parent skill's `concerns/motion/` sub-folder reaches 6 prompts (audit
motion-curve usage, audit duration ranges, audit easing fairness, audit
reduced-motion support, suggest motion-token tree, refactor motion to
tokens) and gains its own rubric for motion-specific scores.

**Verdict:** `promote-to-sibling-skill`. The folder becomes its own
installable skill in the marketplace, with the parent owning the token
contract via shared interface conventions.

### Example 2 — stay

A skill's `prompts/` folder has five prompts (e.g., extract-from-interview,
extract-from-tickets, reverse-from-artifact, cluster-and-score, verdict).
Each prompt is a mode of the same skill, not a separate audit. All share
the same verdict semantics and feed the same canonical output artifact.

**Verdict:** `stay-as-folder`. Five prompts but unified purpose — this is a
healthy `prompts/` folder, not a sibling skill in disguise.

### Example 3 — already its own skill

A folder inside a skill contains its own `.claude-plugin/plugin.json` with
a different `name` field. Someone built a skill-inside-a-skill.

**Verdict:** `already-its-own-skill`. Move it out of the parent to
`plugins/<its-name>/` and register it in the marketplace.

## Migration plan (when promotion is the verdict)

Emit this plan:

```
Migration: <parent-skill>/<folder> → plugins/<new-name>

1. Create plugins/<new-name>/ with the standard scaffold
2. Move <folder>'s contents into plugins/<new-name>/skills/<new-name>/
3. Distribute by role:
   - references go into references/
   - prompts go into prompts/
   - schemas go into schemas/
   - templates go into templates/
   - fixtures go into fixtures/
4. Add plugin.json with name = <new-name>
5. Add README.md (≤200 words) and TESTS.md
6. Register in marketplace.json
7. In the parent skill, replace the moved content with a reference:
   "<concern> moved to <new-name> — install separately"
8. Run audit on both parent and new sibling — both must score ≥4 on every dimension
```

## Anti-pattern: promoting too eagerly

Promote when triggers are met, not when the folder feels important. A
3-prompt folder that performs a coherent sub-task should stay as a folder.
Premature promotion produces under-documented stub-skills that confuse the
marketplace.

## Anti-pattern: refusing to promote

Equally bad: a parent skill that has grown to 30 prompts and 4 audit
rubrics because nothing has been spun out. The parent becomes unreadable.
If the migration triggers fire and the folder is not promoted, that's the
same kind of decision drift as never sizing a task.
