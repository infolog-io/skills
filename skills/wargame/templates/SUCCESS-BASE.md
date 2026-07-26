# SUCCESS — the definition of properly wargamed

A wargame passes only when ALL points hold. Pass/fail per point. No partial credit. Softened grading is how this loop rots.

1. Every move states its expected observation: command output, file state, UI state, or test result you should see if the move worked.

2. Every move carries its most likely failure, the cause that failure signals, and the counter-move.

3. Every fork has a trigger: if you observe X, take route B. No judgment calls left to the executor.

4. Every assumption recon could not settle is marked RECON NEEDED with the exact check that settles it.

5. Abort conditions exist: the moments to stop, write state to the ledger, and hand back rather than improvise. Observed state contradicting a wargame assumption is always an abort. So is any move that would edit an artifact the executor is graded against — rubric, inventory, fixture set, golden file, mission brief. The route names those artifacts as read-only.

6. Verification runs are spelled out: exact commands, when to run them, and what pass looks like for each.

7. Every verification command is validated before the route trusts it. The wargame records it run against a known-good input, passing, and a known-bad input, failing. A check never seen to fail is not a check.

8. It survived a red-team pass. The doc records the attack that failed against it, and the patch born from the attack that did not.

9. It is executable blind. A mid-tier model runs the mission end to end without asking a single question; would-be questions get logged, not asked.

## Repo extensions

A repo copies this base into its `SUCCESS.md` and appends its quality bar as points 10+. One point per bar item, phrased as a checkable property of the wargame. A verification-command point (the repo's exact check commands) is mandatory. Graders grade all points, base and extensions alike.

A repo already carrying an older base (8 points, extensions from 9) adopts point 7 by inserting it after its verification-command point and renumbering everything below it, base and extensions alike. Ledger entries written under the old numbering keep it; note the base version in the entry that renumbers.
