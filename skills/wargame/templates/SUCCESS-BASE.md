# SUCCESS — the definition of properly wargamed

A wargame passes only when ALL points hold. Pass/fail per point. No partial credit. Softened grading is how this loop rots.

1. Every move states its expected observation: command output, file state, UI state, or test result you should see if the move worked.

2. Every move carries its most likely failure, the cause that failure signals, and the counter-move.

3. Every fork has a trigger: if you observe X, take route B. No judgment calls left to the executor.

4. Every assumption recon could not settle is marked RECON NEEDED with the exact check that settles it.

5. Abort conditions exist: the moments to stop, write state to the ledger, and hand back rather than improvise. Observed state contradicting a wargame assumption is always an abort. So is any move that would edit an artifact the executor is graded against — rubric, inventory, fixture set, golden file, mission brief. The route names those artifacts as read-only.

6. Verification runs are spelled out: exact commands, when to run them, and what pass looks like for each.

7. Every verification command is validated before the route trusts it. The wargame records it run against a known-good input, passing, and a known-bad input, failing. A check never seen to fail is not a check. The record is OBSERVED OUTPUT, pasted. A validation entry phrased as what the command "must", "will", or "should" print is a prediction, and a prediction fails this point — including one that names the right pass state. Recording a command's current failing state as its known-good observation also fails.

8. It survived a red-team pass. The doc records the attack that failed against it, and the patch born from the attack that did not.

9. It is executable blind. A mid-tier model runs the mission end to end without asking a single question; would-be questions get logged, not asked.

10. Every script, formula, or computation the route ships to PRODUCE its deliverable is exercised on degenerate input before the route trusts it, and its refusal behaviour is named. Point 7 covers commands that CHECK the work; this point covers code that MAKES it, which point 7 never sees. Degenerate means at minimum: the all-identical input, the empty or single-element input, the input one quantum off the boundary, and the input that arrives when an upstream step half-failed. For each, the doc records what the code printed and why that is a refusal rather than a number. A computation that returns a confident value on garbage is worse than one that crashes, because the route reports it. Any threshold or constant the code branches on is named here with the reasoning for its value.

11. Every done-condition in the mission brief is either routed by a move or explicitly deferred in Decomposition with an exact count. Point 5 stops the route from EDITING the brief; this point stops it from silently NOT COVERING the brief. A route that drops a deliverable without a deferral cannot satisfy the mission it claims to execute, and the mismatch surfaces only after execution.

## Repo extensions

A repo copies this base into its `SUCCESS.md` and appends its quality bar as points 12+. One point per bar item, phrased as a checkable property of the wargame. A verification-command point (the repo's exact check commands) is mandatory. Graders grade all points, base and extensions alike.

A repo carrying an older base adopts new points by inserting each after the base point it follows and renumbering everything below it, base and extensions alike. The 8-point base gains point 7 after its verification-command point; the 9-point base gains points 10 and 11 after "executable blind". Ledger entries written under the old numbering keep it; note the base version in the entry that renumbers.
