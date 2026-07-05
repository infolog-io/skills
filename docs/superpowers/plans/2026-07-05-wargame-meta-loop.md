# Wargame Meta Loop + Eval System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the wargame meta loop + eval system per the approved spec, then prove it end-to-end on DISCO Mission 001 (RFC-0003 CROW parser) up to the execution handoff.

**Architecture:** A `wargame` plugin skill in infolog-skills carries all mechanics (templates, protocols). Global CLAUDE.md shrinks to the law. DISCO adopts via scaffold + repo SUCCESS extensions. Mission 001 runs BRIEF → WARGAME → GRADE → RED-TEAM in this session; EXECUTE hands off to a cheaper model.

**Tech Stack:** Markdown/YAML artifacts, Claude Code plugin marketplace (infolog-io), python3 for YAML/JSON validation, git.

**Spec:** `docs/superpowers/specs/2026-07-05-wargame-meta-loop-design.md`

**Execution adaptation:** Authoring tasks are judgment-dense and coherence-coupled; they run inline in the authoring session. Recon (Task 8) fans out to read-only subagents. Adversarial grading and red-team (Task 11) use fresh subagents so the graders have no authoring context. Doc tasks verify by parser/grep checks, not pytest.

**Spec erratum resolved here:** the spec writes both `RETRO/` and `RETRO/NNN.md`; this plan normalizes to `docs/retros/NNN-<name>.md`, matching the `docs/missions/` and `docs/wargames/` pattern.

---

## File structure

```
infolog-skills/
  skills/wargame/
    SKILL.md                        # doctrine: triggers, pipeline, protocols
    templates/
      MISSION.md                    # brief template
      WARGAME.md                    # battle-plan template
      SUCCESS-BASE.md               # 8-point rubric + extension mechanism
      LEDGER.md                     # run-log schema (YAML frontmatter entries)
      RETRO.md                      # miss → system patch template
      HANDOFF-CLAUDE.md             # executor prompt, Claude Code
      HANDOFF-CODEX.md              # executor prompt, Codex CLI
      GOAL-CONTRACT.md              # breadth-first drafting contract
      LOOP-REFINEMENT.md            # grade/red-team/patch loop contract
      REPO-ADOPTION.md              # how a repo joins the loop
  .claude-plugin/marketplace.json   # + wargame plugin entry

~/.claude/CLAUDE.md                 # consolidated: -3 sections, +Meta Loop
~/.claude/rules/amazon-writing.md   # + operational-format carve-out line

DISCO/  (branch: meta/wargame-adoption)
  docs/META-LOOP.md                 # filled REPO-ADOPTION output
  docs/missions/001-crow-parser.md  # Mission 001 brief
  docs/wargames/001-crow-parser.md  # Mission 001 wargame
  docs/retros/                      # empty until first retro
  SUCCESS.md                        # base 8 + TERAX extensions 9-14
  LEDGER.md                         # mission log
  TERAX.md                          # + 2-line meta-loop pointer (small merge surface)
```

---

## Phase A — the wargame skill

### Task 1: SKILL.md

**Files:**
- Create: `skills/wargame/SKILL.md`

- [ ] **Step 1: Author SKILL.md.** Frontmatter: `name: wargame`, `description:` (when-to-use, covering triggers: wargame/mission/battle plan/meta loop/plan-then-execute requests, non-trivial feature work). Body sections, all required:
  1. `## The pipeline` — the seven stages with artifact paths, exactly as the spec table.
  2. `## Trigger` — 3+ steps or architectural decision; below threshold skip with one-line ledger note.
  3. `## Effort routing` — wargame + red-team: strongest model, max effort, recon read-only; grade: any model + adversarial subagent; execute: cheapest capable (Sonnet build-loop / Codex).
  4. `## The wargame order` — generalized order text: recon read-only first; fight on paper move by move; expected observation per move; likely failure + cause + counter-move; triggered forks; RECON NEEDED marks; abort conditions; verification runs; "write it so the executor runs end to end without asking a single question."
  5. `## Grading protocol` — self-grade, then adversarial subagent grade (blind-executor roleplay); pass/fail per point, no partial credit; all points or not done.
  6. `## Red-team protocol` — attack the route as the executor; DONE = all points pass AND one honest break attempt fails; two fruitless cycles = stop.
  7. `## BLOCKED discipline` — unfilled `{{PLACEHOLDER}}` = BLOCKED; never invent inputs; write what is needed in the ledger and move on.
  8. `## Decomposition rule` — mission unroutable in one executor session splits into phased missions, each with an acceptance check.
  9. `## Template law` — ask for artifacts, findings, quotes, rewrites; never reasoning transcripts. Operational format carve-out from the narrative writing rule.
  10. `## Templates` — index of the ten template files with one-line purposes.

- [ ] **Step 2: Verify.**
  Run: `python3 -c "import yaml,sys; t=open('skills/wargame/SKILL.md').read(); fm=t.split('---')[1]; d=yaml.safe_load(fm); assert d['name']=='wargame' and len(d['description'])>100; print('frontmatter OK')"`
  Expected: `frontmatter OK`
  Run: `for h in "The pipeline" "Trigger" "Effort routing" "The wargame order" "Grading protocol" "Red-team protocol" "BLOCKED discipline" "Decomposition rule" "Template law" "Templates"; do grep -q "## $h" skills/wargame/SKILL.md || echo "MISSING: $h"; done`
  Expected: no output.

- [ ] **Step 3: Commit.** `git add skills/wargame/SKILL.md && git commit -m "feat(wargame): SKILL.md doctrine for the meta loop"`

### Task 2: MISSION.md + WARGAME.md templates

**Files:**
- Create: `skills/wargame/templates/MISSION.md`
- Create: `skills/wargame/templates/WARGAME.md`

- [ ] **Step 1: Author MISSION.md.** YAML frontmatter fields: `id`, `name`, `repo`, `date`, `status: DRAFT|BLOCKED|WARGAMED|EXECUTING|DONE`, `wargamer`, `executor`. Sections: `## Context` (why now, links), `## The mission` (executor's definition of done, addressed to the executor), `## Materials` (recon reading list), `## Constraints` (quality bar, out of scope), `## Verification` (runs that must pass, pointer to repo SUCCESS.md), `## Routing` (who wargames, who executes). Placeholder rule stated at top: any unfilled `{{...}}` puts the mission in BLOCKED.

- [ ] **Step 2: Author WARGAME.md.** Frontmatter: `mission`, `date`, `status: DRAFT|GRADED|DONE`, `grades:` (map, one key per SUCCESS point, values pass/fail). Sections: `## Recon findings` (facts with sources), `## Moves` (numbered; each move carries: **Do**, **Expect** — the observation if it worked, **Likely failure** — plus the cause it signals, **Counter-move**), `## Forks` (trigger → route, "if you observe X, take route B"), `## RECON NEEDED` (assumption + the exact check that settles it), `## Abort conditions` (including the standing abort: observed state contradicts a wargame assumption), `## Verification runs` (exact commands, when, pass state per run), `## Red-team record` (attacks tried; the failed attack recorded; the patch born from any successful attack).

- [ ] **Step 3: Verify cross-consistency.** Every SUCCESS-BASE point (Task 3) must have a home: points 1-2 → Moves fields; 3 → Forks; 4 → RECON NEEDED; 5 → Abort conditions; 6 → Verification runs; 7 → Red-team record; 8 → the whole doc + HANDOFF log-don't-ask rule.
  Run: `for h in "Recon findings" "Moves" "Forks" "RECON NEEDED" "Abort conditions" "Verification runs" "Red-team record" ; do grep -q "## $h" skills/wargame/templates/WARGAME.md || echo "MISSING: $h"; done`
  Expected: no output.

- [ ] **Step 4: Commit.** `git add skills/wargame/templates/ && git commit -m "feat(wargame): mission + wargame templates"`

### Task 3: SUCCESS-BASE.md + LEDGER.md + RETRO.md

**Files:**
- Create: `skills/wargame/templates/SUCCESS-BASE.md`
- Create: `skills/wargame/templates/LEDGER.md`
- Create: `skills/wargame/templates/RETRO.md`

- [ ] **Step 1: Author SUCCESS-BASE.md.** Full rubric text (product-engineering wording, verbatim from spec-derived list):
  1. Every move states its expected observation: command output, file state, UI state, or test result you should see if the move worked.
  2. Every move carries its most likely failure, the cause that failure signals, and the counter-move.
  3. Every fork has a trigger: if you observe X, take route B. No judgment calls left to the executor.
  4. Every assumption recon could not settle is marked RECON NEEDED with the exact check that settles it.
  5. Abort conditions exist: the moments to stop, write state to the ledger, and hand back rather than improvise. Observed state contradicting a wargame assumption is always an abort.
  6. Verification runs are spelled out: exact commands, when to run them, and what pass looks like for each.
  7. It survived a red-team pass. The doc records the attack that failed against it, and the patch born from the attack that did not.
  8. It is executable blind. A mid-tier model runs the mission end to end without asking a single question; would-be questions get logged, not asked.
  Plus: `## Repo extensions` — repos copy this base into their SUCCESS.md and append points 9+ from their quality bar; every point graded pass/fail, no partial credit.

- [ ] **Step 2: Author LEDGER.md.** Template = header + one example entry. Entry format: `## NNN <name>` followed by a fenced ```yaml block with fields: `mission`, `wargame`, `dates` (`drafted`, `graded`, `executed`), `grades` (map: point number → pass|fail, covering base 8 + repo extensions), `patches` (list: what changed in the wargame during refinement), `actuals`: `executor_model`, `questions_logged` (list of the questions the executor would have asked), `deviations` (list), `forks_predicted` (int), `forks_fired` (int), `forks_unpredicted` (list — each is a named wargame blind spot), `verification` (map: run → pass|fail), `rework_count`, `retro` (path or null), `skip_note` (for below-threshold work: the one-line justification).

- [ ] **Step 3: Author RETRO.md.** Frontmatter: `mission`, `date`. Sections: `## Misses` (each miss: what happened, evidence from ledger actuals), `## Root cause in system terms` (per miss: the template line, rubric point, or CLAUDE.md law that failed to catch it — file + section named), `## Patches applied` (per miss: file changed + the change; a retro without at least one system patch must state why the system needed no change), `## Lessons` (project-level patterns → tasks/lessons.md update). Closing law: RETRO patches the SYSTEM (skill templates, rubric, CLAUDE.md); lessons.md captures PROJECT patterns.

- [ ] **Step 4: Verify.**
  Run: `python3 -c "import yaml; t=open('skills/wargame/templates/LEDGER.md').read(); y=t.split('\`\`\`yaml')[1].split('\`\`\`')[0]; d=yaml.safe_load(y); [d['actuals'][k] for k in ('executor_model','questions_logged','deviations','forks_predicted','forks_fired','forks_unpredicted','verification','rework_count')]; print('ledger schema OK')"`
  Expected: `ledger schema OK`
  Run: `grep -c "^[0-9]\." skills/wargame/templates/SUCCESS-BASE.md`
  Expected: `8`

- [ ] **Step 5: Commit.** `git add skills/wargame/templates/ && git commit -m "feat(wargame): rubric, ledger, retro templates"`

### Task 4: Handoffs + contracts + adoption template

**Files:**
- Create: `skills/wargame/templates/HANDOFF-CLAUDE.md`
- Create: `skills/wargame/templates/HANDOFF-CODEX.md`
- Create: `skills/wargame/templates/GOAL-CONTRACT.md`
- Create: `skills/wargame/templates/LOOP-REFINEMENT.md`
- Create: `skills/wargame/templates/REPO-ADOPTION.md`

- [ ] **Step 1: Author both HANDOFF templates.** Shared required content (each adapted to its tool's conventions — Claude: session start in repo, plugin skills available; Codex: AGENTS.md pointer chain): identify wargame path + mission path; the executor contract, verbatim rules: (a) follow the route move by move; (b) at each move compare observation to Expect, on mismatch consult Likely failure/Counter-move; (c) at forks obey triggers exactly; (d) never ask a question — write it to the ledger entry `questions_logged` and continue if a counter-move covers it, abort if not; (e) at any abort condition: stop, write state to ledger, hand back; (f) run every verification run at its stated time, log results to `actuals.verification`; (g) fill all `actuals` fields before reporting done.

- [ ] **Step 2: Author GOAL-CONTRACT.md.** Generalized from the kit: every mission file in `docs/missions/` gets a first-draft wargame in `docs/wargames/`, logged in LEDGER.md with a self-grade against SUCCESS.md. Rules: missions are wargamed, not executed; recon read-only; breadth first — draft all before polishing any; per-draft ledger entry with honest point-by-point self-grade; unfilled placeholder = BLOCKED, write what is needed, never invent; operate autonomously, finish work before ending a turn; stop when all missions DRAFTED or BLOCKED.

- [ ] **Step 3: Author LOOP-REFINEMENT.md.** Generalized from the kit: each cycle — grade every draft point by point against SUCCESS.md, log grades to LEDGER.md; take the weakest draft, red-team it by playing the executor blind and attacking the route; patch the break, add the branch that catches it next time, upgrade vague moves with expected observations, convert unstated assumptions to RECON NEEDED marks with settling checks; re-grade and log what changed. DONE = all points pass AND one honest break attempt fails. Do not soften grading to finish faster. Stop when every wargame is DONE or BLOCKED, or two consecutive cycles improve nothing.

- [ ] **Step 4: Author REPO-ADOPTION.md.** Checklist a repo runs once: (1) canonical agent doc named, pointer files `CLAUDE.md`/`AGENTS.md` contain its filename (DISCO/TERAX pattern); (2) create `docs/missions/`, `docs/wargames/`, `docs/retros/`; (3) create repo `SUCCESS.md` = copy of base 8 + repo quality bar as points 9+ (verification-command point mandatory); (4) create `LEDGER.md` from template; (5) canonical doc gets a ≤3-line meta-loop pointer (small merge surface on forks); (6) note default wargamer/executor routing.

- [ ] **Step 5: Verify.**
  Run: `grep -l "questions_logged" skills/wargame/templates/HANDOFF-*.md | wc -l`
  Expected: `2`
  Run: `grep -q "two consecutive cycles" skills/wargame/templates/LOOP-REFINEMENT.md && grep -q "BLOCKED" skills/wargame/templates/GOAL-CONTRACT.md && echo "contracts OK"`
  Expected: `contracts OK`

- [ ] **Step 6: Commit.** `git add skills/wargame/templates/ && git commit -m "feat(wargame): handoffs, goal/loop contracts, repo adoption"`

### Task 5: Marketplace registration

**Files:**
- Modify: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Add plugin entry** to the `plugins` array (alphabetical/end position per file's existing order), and bump `metadata.version` minor + update `metadata.description` skill count wording:

```json
{
  "name": "wargame",
  "description": "Meta loop + eval system for product engineering. Wargame missions on paper before execution: BRIEF, WARGAME, GRADE, RED-TEAM, EXECUTE, VERIFY, RETRO. Plans graded pass/fail against an 8-point rubric plus repo extensions, red-teamed until an honest break attempt fails, then handed to a cheaper executor. Ledger tracks predicted-vs-actual; retros patch the system itself.",
  "source": "./skills/wargame",
  "version": "0.1.0",
  "category": "engineering",
  "author": { "name": "Information Logistics" }
}
```

- [ ] **Step 2: Verify.** Run: `python3 -m json.tool .claude-plugin/marketplace.json > /dev/null && python3 -c "import json; d=json.load(open('.claude-plugin/marketplace.json')); assert any(p['name']=='wargame' for p in d['plugins']); print('marketplace OK')"`
  Expected: `marketplace OK`

- [ ] **Step 3: Commit.** `git add .claude-plugin/marketplace.json && git commit -m "feat(marketplace): register wargame plugin v0.1.0"`

---

## Phase B — global config surgery

### Task 6: CLAUDE.md consolidation + writing-rule carve-out

**Files:**
- Modify: `~/.claude/CLAUDE.md`
- Modify: `~/.claude/rules/amazon-writing.md`

- [ ] **Step 1: Back up.** Run: `cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.bak-2026-07-05`

- [ ] **Step 2: Edit CLAUDE.md.**
  Remove: section `### 1. Plan Mode Default` entire; section `### 4. Verification Before Done` entire; section `## Task Management` entire.
  Renumber remaining Workflow Orchestration subsections; rewire `Self-Improvement Loop` first bullet to: "After ANY correction from the user: update tasks/lessons.md with the pattern. Corrections during loop work land in the mission's RETRO first, then distill to lessons.md."
  Insert new section after `## Workflow Orchestration`, full text:

```markdown
## The Meta Loop

Every task with 3+ steps or an architectural decision runs the loop. Smaller tasks skip it; the repo LEDGER.md gets one line saying so.

BRIEF → WARGAME → GRADE → RED-TEAM → EXECUTE → VERIFY → RETRO

1. BRIEF — `docs/missions/NNN-<name>.md`, the executor's definition of done. An unfilled `{{PLACEHOLDER}}` means BLOCKED; never invent inputs.
2. WARGAME — `docs/wargames/NNN-<name>.md`. Strongest model, max effort, recon read-only. Fight the mission on paper per the wargame skill.
3. GRADE — self-grade plus adversarial subagent grade against the repo's SUCCESS.md. Pass/fail per point. No partial credit.
4. RED-TEAM — attack the route. DONE requires one honest break attempt to fail.
5. EXECUTE — cheapest capable model (Sonnet build-loop, Codex). Executor obeys triggers and aborts; it never asks, it logs would-be questions to the ledger.
6. VERIFY — run every verification run the wargame names; log actuals (questions, deviations, forks fired, results).
7. RETRO — `docs/retros/NNN-<name>.md`. Every miss traces to a system file (template, rubric, this section) and patches it.

Law: no execution without a graded wargame, or a one-line ledger note explaining the skip.
Mechanics live in the `wargame` skill (infolog-io marketplace); repos adopt via its REPO-ADOPTION template.
```

- [ ] **Step 3: Append to `~/.claude/rules/amazon-writing.md`:**

```markdown
- Operational artifacts (mission briefs, wargames, ledgers, retros) use move/table structure by design; the narrative rule does not apply to them. Sentence rules still do.
```

- [ ] **Step 4: Verify.** Run: `grep -c "Plan Mode Default\|Verification Before Done\|## Task Management" ~/.claude/CLAUDE.md`
  Expected: `0`
  Run: `grep -q "## The Meta Loop" ~/.claude/CLAUDE.md && grep -q "Operational artifacts" ~/.claude/rules/amazon-writing.md && echo "config OK"`
  Expected: `config OK`
  Then read the full edited file once for orphan references (`todo.md`, renumbering, dangling mentions of removed sections).
  Note: `~/.claude` is not a git repository; the backup file is the rollback path.

---

## Phase C — DISCO adoption

### Task 7: Scaffold DISCO

**Files:**
- Create: `DISCO/docs/META-LOOP.md`, `DISCO/docs/missions/`, `DISCO/docs/wargames/`, `DISCO/docs/retros/`, `DISCO/SUCCESS.md`, `DISCO/LEDGER.md`
- Modify: `DISCO/TERAX.md` (append ≤3 lines)

- [ ] **Step 1: Branch.** Run: `git -C ~/Developer/DISCO checkout -b meta/wargame-adoption`

- [ ] **Step 2: Create SUCCESS.md** = base 8 (Task 3 text verbatim) + DISCO extensions from TERAX.md's quality bar:
  9. Correctness: moves address edge cases, failure modes, and concurrent access. No "works for now" moves.
  10. Performance: any move adding RAM, IPC round-trips, re-renders, or a dependency states the cost and justification.
  11. Security: moves touching IPC, fs, network, or the AI tool surface name the boundary validation. The secret-path deny-list is never bypassed.
  12. UI/UX: user-visible moves define the polished end state.
  13. Architecture: new logic lands in pure, dependency-light functions; Tauri commands and React components stay thin.
  14. Verification runs include `pnpm lint`, `pnpm check-types`, `pnpm test`, `cargo clippy`, `cargo test --locked`; a core-subsystem change adds a test locking the invariant.

- [ ] **Step 3: Create LEDGER.md** from template (header, no entries). Create `docs/META-LOOP.md` = filled REPO-ADOPTION checklist (canonical doc: TERAX.md; routing: wargamer = strongest available at max effort, executor = Sonnet via build-loop-claude-code or Codex). Create the three `docs/` dirs (`.gitkeep` in `retros/`).

- [ ] **Step 4: Append to TERAX.md** (end of file, 3 lines max):

```markdown
## Meta Loop

DISCO runs the wargame meta loop: missions in `docs/missions/`, battle plans in `docs/wargames/`, graded against `SUCCESS.md`, logged in `LEDGER.md`. See `docs/META-LOOP.md`.
```

- [ ] **Step 5: Verify.** Run: `ls ~/Developer/DISCO/docs/missions ~/Developer/DISCO/docs/wargames ~/Developer/DISCO/docs/retros && grep -c "^[0-9]" ~/Developer/DISCO/SUCCESS.md`
  Expected: dirs listed; point count `14`.

- [ ] **Step 6: Commit.** `git -C ~/Developer/DISCO add -A && git -C ~/Developer/DISCO commit -m "docs: adopt wargame meta loop (SUCCESS, LEDGER, missions/wargames/retros)"`

---

## Phase D — Mission 001: the CROW parser

### Task 8: Recon fan-out (read-only subagents, run in parallel)

- [ ] **Step 1: Dispatch three Explore subagents**, prompts must demand: facts with file paths, no recommendations.
  (a) crow.pet inventory: record types on disk vs RFC-0003's mapping table; frontmatter schemas (`schema_version` fields); `scripts/check-*.py` validation behaviors; counts per record type.
  (b) DISCO module pattern: how `src-tauri/src/modules/{fs,git,workspace}` are structured (mod layout, command registration, error types, tests); where frontend TS parsing code would live per existing patterns; whether remark/unified or any md parser is already a dependency (`package.json`, `Cargo.toml`).
  (c) RFC deep-read: RFC-0002 (pipeline placement), RFC-0003 full, RFC-0005 (naming/layout rules), RFC-0006 (scoring/CI hooks the parser must not preclude).

- [ ] **Step 2: Save merged recon notes** to `DISCO/docs/wargames/001-recon-notes.md` (input to the wargame; the wargame's Recon findings section cites it).

### Task 9: Mission brief

**Files:**
- Create: `DISCO/docs/missions/001-crow-parser.md`

- [ ] **Step 1: Author from MISSION template.** Definition of done (from RFC-0003, refined by recon): given a local crow.pet checkout path, DISCO parses records into typed structures per the RFC-0003 mapping table (9 node types, no Concept), preserving provenance/scoring frontmatter; malformed records produce typed errors, not crashes; unit tests cover every mapped record type plus malformed frontmatter; all five SUCCESS point-14 commands pass. Out of scope: rendering, `disco_score` writing, file watching, the semantic-graph query layer beyond typed records. Materials: recon notes, RFC-0002/0003/0005/0006, crow.pet checkout. Routing: executor = Sonnet via build-loop-claude-code (Codex as alternate).

- [ ] **Step 2: Verify.** Run: `grep -c "{{" ~/Developer/DISCO/docs/missions/001-crow-parser.md`
  Expected: `0` (no unfilled placeholders, else status: BLOCKED).

- [ ] **Step 3: Commit.** `git -C ~/Developer/DISCO add docs/missions && git -C ~/Developer/DISCO commit -m "docs(mission-001): CROW parser brief"`

### Task 10: Wargame Mission 001

**Files:**
- Create: `DISCO/docs/wargames/001-crow-parser.md`
- Modify: `DISCO/LEDGER.md`

- [ ] **Step 1: Author the wargame** per WARGAME template at max effort. Route the open architecture question (TS remark/unified vs Rust `modules/crow/`) via recon findings; if recon cannot settle it, it becomes the first RECON NEEDED item with its settling check, and the moves fork on it. Every move: Do/Expect/Likely failure/Counter-move. Verification runs: the five DISCO commands + per-record-type parse fixtures.

- [ ] **Step 2: Self-grade** against all 14 points; write LEDGER entry with grades + honest fails.

- [ ] **Step 3: Commit.** `git -C ~/Developer/DISCO add docs/wargames LEDGER.md && git -C ~/Developer/DISCO commit -m "docs(mission-001): wargame draft + self-grade"`

### Task 11: Adversarial grade + red-team

- [ ] **Step 1: Dispatch a fresh grading subagent** (no authoring context): given SUCCESS.md + the wargame, grade each point pass/fail with the failing line quoted. No partial credit.

- [ ] **Step 2: Dispatch a fresh red-team subagent**: play a mid-tier executor running the route blind; attack it — find the move where you stall, misread an Expect, or face a judgment call; report the exact break point. 

- [ ] **Step 3: Patch the wargame** for every fail and every break; add the fork/branch that catches each break next time; record the red-team results in `## Red-team record`; re-grade; update LEDGER entry (grades + patches list).

- [ ] **Step 4: DONE gate.** All 14 points pass AND one honest break attempt failed. If two consecutive patch cycles improve nothing, stop and log BLOCKED-ON items.

- [ ] **Step 5: Commit.** `git -C ~/Developer/DISCO add docs/wargames LEDGER.md && git -C ~/Developer/DISCO commit -m "docs(mission-001): red-teamed wargame, DONE"`

### Task 12: Execution handoff

- [ ] **Step 1: Write the filled executor prompt** (from HANDOFF-CLAUDE.md) to `DISCO/docs/wargames/001-handoff.md`, plus the exact launch line for the user (e.g. `cd ~/Developer/DISCO && claude --model sonnet`, paste handoff) and the Codex alternate.

- [ ] **Step 2: Commit and report.** Final report: system built, mission 001 wargamed + red-teamed, how to fire the executor, what the retro will need (ledger actuals).

---

## Deferred (post-execution, separate session)

- EXECUTE on cheap model; VERIFY actuals into ledger.
- First RETRO (`docs/retros/001-crow-parser.md`) — needs at least one system patch or a stated reason none was needed.
- Marketplace version bump if templates change from retro patches.
