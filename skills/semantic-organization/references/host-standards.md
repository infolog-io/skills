---
type: reference
---

# Host Standards

The portable Agent Skills format and each host's distribution conventions
are related but not identical. This skill treats the target host as an
explicit facet during scaffold and audit.

Sources checked 2026-06-14:
- Agent Skills specification: https://agentskills.io/specification
- Anthropic Agent Skills docs: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Claude Code plugin docs: https://code.claude.com/docs/en/plugins-reference
- OpenAI Codex skills docs: https://developers.openai.com/codex/skills
- OpenAI Codex AGENTS.md docs: https://developers.openai.com/codex/guides/agents-md

## Target host profiles

| Profile | Root path | Required skill files | Host-specific layer |
|---|---|---|---|
| `agent-skills-portable` | `<skill-name>/` | `SKILL.md` with `name` and `description` | Optional `scripts/`, `references/`, `assets/` |
| `infolog-marketplace` | `skills/<skill-name>/` | Portable skill files plus `README.md`, `TESTS.md`, `.claude-plugin/plugin.json` | Root `.claude-plugin/marketplace.json` registers `./skills/<skill-name>` |
| `codex-repo-skill` | `.agents/skills/<skill-name>/` | Portable skill files | Optional `agents/openai.yaml`; descriptions must be concise and trigger-front-loaded |
| `claude-code-plugin-package` | plugin package root | Claude Code plugin manifest and components | `.claude-plugin/plugin.json`; skill path may be configured by plugin manifest |

## Default for this repo

This marketplace uses `infolog-marketplace` by default:

```
skills/<skill-name>/
├── .claude-plugin/plugin.json
├── SKILL.md
├── README.md
└── TESTS.md
```

Do not introduce a `plugins/<name>/skills/<name>/` wrapper in this repo.
That wrapper can be valid in a standalone Claude Code plugin package, but
it is intentionally not this marketplace's layout.

## Generation rules

1. Ask or infer `target_host`; default to `infolog-marketplace` in this repo.
2. Generate paths for the target host, not for every host at once.
3. Preserve the portable Agent Skills core whenever possible.
4. Keep host-specific metadata at the host layer.
5. Explain tradeoffs when a user asks for a host layout that conflicts with
   this repo's marketplace convention.

## Audit rules

The host-standard facet answers: "Does this structure satisfy the host it
claims to target?"

- Under `agent-skills-portable`, missing marketplace files are not spec
  failures.
- Under `infolog-marketplace`, missing marketplace files lower the
  marketplace-layer scores.
- Under `codex-repo-skill`, a repo-local skill belongs under
  `.agents/skills/<skill-name>/`, and descriptions should front-load the
  activation keywords because Codex may shorten skill descriptions in the
  initial skill list.
- Under `claude-code-plugin-package`, validate the plugin manifest and the
  manifest's skill path, but do not import that wrapper into this repo
  unless the user is building an external package.

## Worked example

A user asks: "Scaffold a Codex-local skill named release-notes."

Verdict: generate `.agents/skills/release-notes/SKILL.md` with concise
frontmatter and optional `references/` or `scripts/` only if needed. Do not
create `.claude-plugin/plugin.json`, because the user asked for a Codex
repo-local skill, not an infolog marketplace skill.
