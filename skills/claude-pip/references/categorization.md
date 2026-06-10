# Rule categorization

Every PIP rule maps to exactly one category. Categorization drives `PRUNE THE PIP` and `PROMOTE THE PIP` — what to drop, what to graduate, where graduates go.

| Category | Heuristic — what the rule looks like | Promote destination |
|---|---|---|
| **Behavioral / process** | Cross-project disciplines. "Write a failing test FIRST", "Enter plan mode", "Dispatch a sub-agent for X". Not tied to a specific file or component. | `~/.claude/CLAUDE.md` (user-global) or `~/.claude/rules/<topic>.md` |
| **Framework gotcha** | Framework- or CMS-specific traps: required status fields, env-var prefixes on scripts, locale/fallback behavior, redeploy-after-script requirements. References the framework, its models/collections, or its package scripts. | Project `CLAUDE.md` under the relevant framework section |
| **Design lock** | "X is the canonical Y. Locked design contract: ... Any visual change requires explicit user approval." References a specific component file (`src/components/...`) and pins geometry, tokens, typography, or motion. | Project `DESIGN.md` under "Locked components" |
| **Spec-frozen** | "Before editing X, read the spec at Y." Gates a work-in-progress surface against an approved design doc. | Project `DESIGN.md` under "Locked components", or removed once the spec has fully shipped |
| **Workflow gotcha** | Project-tooling-specific. "Run the seed validator after touching blocks/seeds", "Use pnpm not npm in this package." | Project `CLAUDE.md` under the relevant tooling section, or the project's lessons file |
| **Other** | Doesn't fit any of the above. | Surface to the user; ask where it belongs. |

## Rendering the table

When listing rules (during prune, promote, or on request), render them as a categorized table:

```
| # | Rule (short) | Category | What it enforces (terse) |
```

Short name 4–6 words; enforcement column ≤ 25 words. The full rule body stays in the file; the table is the navigation surface.
