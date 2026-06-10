# Full procedures — `PRUNE THE PIP` and `PROMOTE THE PIP`

Both procedures show a diff and wait for explicit user approval before writing. Prune may propose verdicts; promote never proposes — it lists, the user picks.

## `PRUNE THE PIP` — audit + drop stale rules

Argument forms: `PRUNE THE PIP` (all-caps command), or phrase-triggered asks like "prune PIP before compact" / "audit CLAUDE-PIP".

1. **Read state.** Load `<project-root>/.claude/CLAUDE-PIP.md` AND scan working-directory `CLAUDE.md` files (CWD up to project root) for PIP markers. Also read neighbors for duplication checks: project `CLAUDE.md`, `DESIGN.md`, any project lessons file, `~/.claude/CLAUDE.md`, `~/.claude/rules/*.md`.
2. **Render the rules as a categorized table** (see [categorization.md](categorization.md)). One row per rule.
3. **Evaluate each rule** against four checks:
   - **File references resolve?** Every path in the rule must exist.
   - **Component references resolve?** Named components must still exist in the codebase (grep).
   - **Duplicated elsewhere?** Search the neighbor files for the rule's substance.
   - **Hedge words snuck in?** Find "should", "consider", "usually", "probably", "might".
4. **Assign verdicts. Default is `keep`** — carry-forward is the point of the file; rules persist across sessions unless explicitly dropped or promoted.
   - `keep` (default): rule is current, or no concrete reason to drop.
   - `refine`: wording needs tightening; the substance is right. Hedge words always map here — they are a wording defect, never a drop reason.
   - `drop`: concrete defect only — broken file/component reference, or exact duplicate already in a neighbor file. "Feels stale" or "haven't seen it fire" do not qualify.
   - `move-elsewhere`: hint only — tell the user to invoke `PROMOTE THE PIP`. Prune does not act on this verdict.
5. **Show the diff** as a markdown report; group by verdict. Wait for approval.
6. **On approve, apply** in place (refine = rewrite preserving id; drop = delete the full `pip:start`/`pip:end` range).
7. **Report** the post-prune count.

If unsure between keep and drop, choose keep — dropping is the destructive choice.

## `PROMOTE THE PIP` — graduate stable rules to canonical homes

Argument forms:

- `PROMOTE THE PIP` → render the categorized table, wait for the user to call out rules
- `PROMOTE THE PIP 2,3,4` → promote those rule numbers using the default destination per category
- `PROMOTE THE PIP all framework gotchas` → bulk-select by category
- `PROMOTE THE PIP 5 to DESIGN.md` → override the default destination for that rule

1. **Read state.** Load `CLAUDE-PIP.md`. Locate destination files (create-if-missing requires user approval): project `CLAUDE.md`, project `DESIGN.md`, `~/.claude/CLAUDE.md`, `~/.claude/rules/`.
2. **Render rules as a categorized table** with a destination column ([categorization.md](categorization.md)).
3. **Wait for the user to call out which rules to promote.** The skill never auto-graduates. Acceptable responses: `promote N` / `promote N,M,P` / `promote category <name>` / `promote 5 to <file>` / `promote all` / `cancel`. Silence aborts.
4. **Build the diff** only for the rules the user named, grouped by destination file.
5. **Final confirmation** before writing. Wait for `apply` / `go` / `yes`.
6. **Apply**: append to destination (convert PIP-style imperative to declarative when destination is prose), then remove the `pip:start`/`pip:end` range from `CLAUDE-PIP.md`. Preserve the file and the `@.claude/CLAUDE-PIP.md` import in `CLAUDE.md` even if PIP ends empty.
