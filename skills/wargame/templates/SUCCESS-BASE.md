# SUCCESS — the definition of properly wargamed

A wargame passes only when ALL points hold. Pass/fail per point. No partial credit. Softened grading is how this loop rots.

1. Every move states its expected observation: command output, file state, UI state, or test result you should see if the move worked.

2. Every move carries its most likely failure, the cause that failure signals, and the counter-move.

3. Every fork has a trigger: if you observe X, take route B. No judgment calls left to the executor.

4. Every assumption recon could not settle is marked RECON NEEDED with the exact check that settles it.

5. Abort conditions exist: the moments to stop, write state to the ledger, and hand back rather than improvise. Observed state contradicting a wargame assumption is always an abort.

6. Verification runs are spelled out: exact commands, when to run them, and what pass looks like for each.

7. It survived a red-team pass. The doc records the attack that failed against it, and the patch born from the attack that did not.

8. It is executable blind. A mid-tier model runs the mission end to end without asking a single question; would-be questions get logged, not asked.

## Repo extensions

A repo copies this base into its `SUCCESS.md` and appends its quality bar as points 9+. One point per bar item, phrased as a checkable property of the wargame. A verification-command point (the repo's exact check commands) is mandatory. Graders grade all points, base and extensions alike.
