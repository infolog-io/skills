# Refinement loop — drafts become wargames

Use after the goal contract has drafted everything. Paste as a /loop (20m cadence) or run cycles manually. Strongest model, maximum effort.

---

LOOP: refine every draft in `docs/wargames/` until each is properly wargamed. Properly wargamed means every point of `SUCCESS.md` holds, no exceptions.

Each cycle:

1. Grade every draft point by point against `SUCCESS.md`. Log the grades in `LEDGER.md`.
2. Take the weakest draft and red-team it: play the executor following it blind, attack the route, find the move where it breaks.
3. Patch the break. Add the branch that catches it next time. Upgrade vague moves with expected observations. Convert every unstated assumption into a RECON NEEDED mark with its settling check.
4. Re-grade and log what changed under the entry's `patches`.

A wargame is DONE when it passes all points AND one honest attempt to break it fails. Record the surviving attack in the wargame's red-team section. Do not soften the grading to finish faster; a draft that passes on paper but dies at first contact is a failure of this loop.

Stop when every wargame is DONE or BLOCKED, or when two consecutive cycles improve nothing. Post the final ledger state when you stop.
