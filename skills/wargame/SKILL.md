---
name: wargame
description: Use for any product-engineering task with 3+ steps or an architectural decision, and whenever the user says wargame, mission, battle plan, or meta loop. Runs the meta loop BRIEF → WARGAME → GRADE → RED-TEAM → EXECUTE → VERIFY → RETRO. The strongest model fights the mission on paper first; the graded, red-teamed battle plan then hands to a cheaper executor (Sonnet build-loop or Codex) that runs it blind. Also use when adopting the loop in a new repo (REPO-ADOPTION template) or when grading or red-teaming an existing wargame.
---

# Wargame — the meta loop

You pay for judgment once. Execution is commodity. This skill turns a mission into a battle plan a mid-tier model runs blind, and turns every run into eval data that patches the system.

## The pipeline

BRIEF → WARGAME → GRADE → RED-TEAM → EXECUTE → VERIFY → RETRO

| Stage | Artifact | Actor |
|---|---|---|
| BRIEF | `docs/missions/NNN-<name>.md` | Human + strongest model |
| WARGAME | `docs/wargames/NNN-<name>.md` | Strongest model, max effort, recon read-only |
| GRADE | `LEDGER.md` entry | Self-grade + fresh adversarial subagent |
| RED-TEAM | Red-team record in the wargame | Strongest model + fresh executor-roleplay subagent |
| EXECUTE | The deliverable | Cheapest capable executor via HANDOFF template |
| VERIFY | `actuals` block in `LEDGER.md` | Executor |
| RETRO | `docs/retros/NNN-<name>.md` | Strongest model |

## Trigger

A task with 3+ steps or an architectural decision runs the loop. Below that threshold, skip it and add a one-line `skip_note` entry to LEDGER.md. The law: no execution without a graded wargame, or that one-line note.

One wargamer per mission: before GRADE, claim the mission in its ledger entry (`claimed_by:` plus session identity). A session observing a live claim stands down to audit-only.

## Effort routing

Wargaming and red-teaming are judgment-dense and token-light: strongest available model, maximum reasoning effort, no edit loops. Grading needs adversarial reading, not genius: any capable model, but always a fresh subagent with no authoring context. Execution goes to the cheapest model that passes verification: Sonnet via build-loop-claude-code, or Codex via HANDOFF-CODEX.

## The wargame order

You are not executing the mission. You are wargaming it. A cheaper executor runs the brief later; your job is the route it will follow.

Recon first, read-only. Read everything the mission's Materials list names. Run nothing that changes state. Every load-bearing claim carries a verbatim disk quote; a summary is not evidence. A symbol a move orders the executor to use carries its providing import line, quoted from disk. A claim that is the OUTPUT of a regex or string transform applied to corpus data (a count, a resolved/unresolved split) is verified by running that exact transform against every matching instance, not by reading representative samples — samples prove a shape is plausible, not a count. The same run-don't-infer rule covers branch-behavior claims: an assertion about which code path produces which observable state (a field value, an error variant, an exit code) names and quotes the producing constructor site, or is traced/executed against the real code — never inferred from surrounding code. Before routing a new external-process spawn or binary invocation, search the WHOLE codebase for prior art solving the same problem class, not only the modules the mission's Materials already name — a solved-elsewhere precedent must be reused or explicitly rejected with a stated reason. A wargame consuming a contract from a sibling wargame (a split mission, a dependency mission) quotes the providing wargame's exact move text, same as a disk quote — a paraphrased contract is not evidence. Before routing, read every prior retro's "Patches applied" list for the repo: each established discipline (collision-abort-before-write, zero-mutation-before-refusal, grant-site naming, chrome escaping, fixture reachability, …) is a checklist item — applied to this route, or explicitly N/A with a reason. A discipline a prior mission earned through a real break is never rediscovered per mission. When a route depends on a CLI, recon records the exact working invocation, verified by running it, including the flags that fail SILENTLY (a viewport flag ignored because a page is already open; a screenshot that reports success and writes no file when handed a relative path). A tool that reports success without doing the work is the most expensive class of recon miss, because every downstream observation is mislabeled rather than missing. An agent's scratch-cleanup reverts ONLY files it created or modified itself; an uncommitted change it did not author is another session's live work.

Then fight the mission on paper, move by move:

- Every move states its expected observation: exactly what you should see if it worked.
- Every move carries its most likely failure, the cause that failure signals, and the counter-move.
- Every fork gets a trigger: if you observe X, take route B.
- Every assumption recon could not settle gets marked RECON NEEDED with the exact check that settles it.
- Every verification command is validated before the route trusts it: run it against a known-good input and a known-bad input, and record both outcomes. A check never seen to fail is not a check. A DOM count on a page holding hidden variants, or a grep over a regenerated file, passes a correct target and a broken one alike.
- End with abort conditions, and the verification runs the executor performs, with what pass looks like for each.

Write it so the executor runs the brief end to end without asking a single question.

## Versioning a wargame

A wargame whose route changes materially before GRADE is rewritten and versioned, not patched. Bump `version:` in the frontmatter and open the body with what changed, why it changed, and which parts of the prior version survive. Patching a changed route leaves one document describing two incompatible plans, and the executor runs whichever half it reads first.

## Grading protocol

Two grades, both against the repo's SUCCESS.md, both pass/fail per point. No partial credit. First a self-grade, logged honestly in the ledger. Then a fresh subagent with no authoring context grades blind and quotes the failing line for every fail. A wargame is not done until every point passes. Every decision the brief delegates to the wargamer gets an explicit disposition line: SETTLED, citing the section that settles it, or DROPPED, with the reason. A self-grade claiming a decision settled cites that section — a paraphrase or a neighboring rule does not satisfy a distinct requirement.

## Red-team protocol

Attack the route before reality does. A fresh subagent plays a mid-tier executor running the route blind and reports the move where it stalls, misreads an Expect, or faces a judgment call. Patch every break. A patched fact re-verifies its sibling details — syntax, format, count — with fresh disk quotes. Add the branch that catches it next time. A safety or cleanup guarantee (restoration, rollback, teardown) proven only inside a test harness that bypasses the actual production code path is not proven for the route — attack whether the guarantee holds when a real caller exercises the real command, not only when a test drives an equivalent path around it. DONE requires all points passing AND one honest break attempt failing. Two consecutive fruitless cycles: stop, log what remains.

## BLOCKED discipline

An unfilled `{{PLACEHOLDER}}` means the mission is BLOCKED. Never invent the missing input. Write what you need in the ledger entry and move on.

## Contract immutability

Any artifact the executor is graded against is READ-ONLY to the executor: the rubric, the content inventory, the fixture set, the golden file, the mission brief. An executor that can edit its contract has no contract. A failing check gets logged and handed back; it is never silenced by editing the check. The wargame names these artifacts and makes editing one an abort condition, so the law is enforced by the route rather than by the executor's restraint.

## Decomposition rule

A mission the wargame cannot route in one executor session splits into phased missions. Each phase gets its own acceptance check the executor runs before starting the next. Sequence phases by risk retired per unit of work. A phase that defers work records the EXACT remaining count, measured not estimated, and names the mission that closes it. A deferral with a number is a plan; a deferral without one is a loss disguised as scope.

## Template law

Ask for artifacts, findings, quotes, and rewrites. Never ask a model to reproduce its reasoning; artifacts are gradeable, thinking transcripts are not. Wargames, ledgers, briefs, and retros are operational formats: move and table structure is the format. Sentence rules still apply inside moves.

## Templates

| File | Purpose |
|---|---|
| `templates/MISSION.md` | The brief: executor's definition of done |
| `templates/WARGAME.md` | The battle plan |
| `templates/SUCCESS-BASE.md` | Base 9-point rubric + repo extension mechanism |
| `templates/LEDGER.md` | Run log: grades, patches, execution actuals |
| `templates/RETRO.md` | Miss → system patch |
| `templates/HANDOFF-CLAUDE.md` | Executor prompt, Claude Code |
| `templates/HANDOFF-CODEX.md` | Executor prompt, Codex CLI |
| `templates/GOAL-CONTRACT.md` | Breadth-first drafting contract |
| `templates/LOOP-REFINEMENT.md` | Grade, red-team weakest, patch loop |
| `templates/REPO-ADOPTION.md` | One-time repo adoption checklist |
