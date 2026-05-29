# claude-pip — pre-vetted rule phrasing

When the user invokes `CLAUDE PIP <topic>`, prefer the phrasing here over inventing fresh wording. Consistent rules are easier to follow.

| Topic | Rule (copy verbatim) |
|---|---|
| **TDD** | **Write a failing test FIRST** for any user-visible behavior, before writing code. Confirm the test fails for the right reason (not "fetch error" or syntax). Only then write the minimum code to make it pass. |
| **Plan mode** | **Enter plan mode** for any task with 3+ steps or any architectural decision. No exploratory coding without a plan in hand. |
| **Sub-agents** | **Dispatch a sub-agent** for research, codebase exploration, parallel work, or anything that would consume >2k tokens of main context. One task per sub-agent. |
| **Adversarial review** | **Run an adversarial review** before claiming any feature shipped. 2-minute hostile pass: where could this break, what was tested vs. assumed, what classes of silent failure exist. |
| **End-to-end verification** | **Fetch the deployed page** and grep for the thing the feature is supposed to produce (anchor IDs, button labels, schema markup, expected text) before claiming shipped. "Build green" is not a proxy for "feature works." |
| **Smoke test all paths** | **Smoke-test every affected path**, not just the one most likely to be interesting. If a change touches N pages, check N pages. |
| **Lessons captured** | **Update `tasks/lessons.md`** after every user correction. Name the failure, the fix, the guardrail. |
| **Test the test** | **Watch the test fail first.** A passing test before the implementation exists means the test is vacuously passing — tighten the assertion. |
| **No defensive null guards on required fields** | **NEVER paper over a missing required schema field with a null guard.** Fix the source: the seed is wrong, the schema is wrong, or the locale write orphaned data. |
| **No build-green-as-done** | **NEVER claim "shipped" because the build is green.** The build only proves the code compiles. The test gate is what proves the feature works. |
| **No hardcoded user-visible strings** | **Every user-visible string** goes through a translation layer or a CMS-localized field. No string literals in components rendering text users will read. |

Add new entries here when a topic recurs across projects. Keep each row under 600 characters.
