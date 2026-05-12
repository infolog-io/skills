# Prompt — Propose semantic renames

**Purpose:** Given a file or folder name, evaluate it against
`references/naming-rules.md` and propose a rename if needed. Refuse to
rename canonical names.

## Input contract

A file or folder path, plus the folder it lives in (to determine the role
context).

## Output contract

```
Original: <path>
Verdict: keep | rename | delete
Proposed: <new-path>  (only if rename)
Reasoning: 1 sentence per rule violated
```

## Procedure

1. Check the path against the forbidden-folders list from
   `references/folder-roles.md`.
2. Check the name against the case rule (must be kebab-case).
3. Check whether the name matches the role of its folder (noun for
   references, verb-led for prompts, etc.).
4. Check for forbidden tokens (`_v1`, `_old`, `temp`, etc.).
5. Check whether the name is specific enough (not generic like `prompt.md`).
6. If the name is a reserved canonical name (`SKILL.md`, `README.md`,
   `TESTS.md`, `plugin.json`, `marketplace.json`), refuse to rename.

## Worked examples

### Example 1 — rename

**Input:** `skills/my-skill/prompts/Prompt1.md`

**Checks:**
- Case: fails (PascalCase, not kebab-case)
- Role match: fails (folder is `prompts/`, name is not verb-led)
- Specificity: fails (generic + numbered)

**Verdict:** `rename`

**Proposed:** `skills/my-skill/prompts/<verb-led-action-name>.md`

**Reasoning:** PascalCase rejected; prompts must be verb-led; generic
numbered names carry no meaning.

(The model should ask the author for the verb and object — it cannot guess
what the prompt does from the name alone.)

### Example 2 — delete (forbidden folder)

**Input:** `skills/my-skill/utils/`

**Checks:**
- Forbidden folder: yes

**Verdict:** `delete`

**Reasoning:** `utils/` is a catch-all. Split contents into role-named folders
or delete if unused.

### Example 3 — keep (canonical)

**Input:** `references/`

**Verdict:** `keep`

**Reasoning:** Canonical folder. Refuse to rename to non-canonical names
like `docs/`, `knowledge/`, `theory/`.

### Example 4 — keep (already semantic)

**Input:** `prompts/extract-from-interview.md`

**Checks:**
- Case: pass
- Role match: pass (verb-led, in prompts/)
- Forbidden tokens: pass
- Specificity: pass (names action and target)

**Verdict:** `keep`

## Reserved names — refuse to rename

| Name | Why |
|---|---|
| `SKILL.md` | Platform-required entry point |
| `README.md` | Platform-required overview |
| `TESTS.md` | Standard project test plan |
| `plugin.json` | Manifest |
| `marketplace.json` | Marketplace manifest |
| Canonical folders: `references/`, `prompts/`, `templates/`, `schemas/`, `fixtures/` | These names mean specific roles |

If asked to rename any of these to a non-canonical alternative, refuse and
cite the rule.

## Edge cases

| Situation | Handling |
|---|---|
| Name uses kebab-case but is overly long (e.g., 8+ words) | Suggest tightening, but keep is acceptable |
| Name includes a date (`audit-2026-04-12.md`) | Keep if the file is genuinely time-bound (log, dated report); otherwise rename |
| Name is in a non-English language | Keep if the skill is intentionally localized; flag for normalization otherwise |
| Author insists on a non-canonical name despite advice | Document the exception in TESTS.md's out-of-scope section |

## Verification before returning output

- The verdict is one of `keep` / `rename` / `delete`
- If rename, the proposed name passes all naming rules
- If delete, the contents are addressed (where do they go?)
- Reasoning cites the specific rule(s) violated
