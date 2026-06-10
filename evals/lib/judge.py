"""LLM judge for description purity.

The static DESC-PURITY check is a verb-list heuristic; this judge is the
authoritative pass. The rule (from Anthropic's skill-authoring best
practices): a description must state only WHEN to use the skill —
triggering conditions, symptoms, activation phrases. If it summarizes the
skill's process/workflow/outputs, Claude may act on the description and
never read the skill body.
"""

from . import llm

PROMPT = """You are auditing Claude Code skill descriptions against this rule:

  A skill description must describe ONLY when to use the skill (triggering
  conditions, symptoms, quoted activation phrases), in third person.
  It must NOT summarize the skill's process, workflow, internal modes,
  rubric, or outputs — that causes the model to act on the description
  and skip the skill body. Capability-scope phrases ("Covers X, Y, Z")
  are borderline-acceptable when they aid routing; step-by-step process
  ("first does A, then emits B") is a violation.

DESCRIPTIONS:
%s

For each, judge whether it violates the rule. Reply with ONLY a JSON array:
[{"skill": "<name>", "violates": true|false,
  "offending_phrases": ["..."], "rewrite_hint": "<one line or empty>"}]
"""


def run(skills, backend=None, model=None):
    """skills: {name: description}. Returns result dict."""
    block = "\n\n".join("### %s\n%s" % (n, d) for n, d in sorted(skills.items()))
    raw = llm.complete(PROMPT % block, backend=backend, model=model, tag="judge")
    verdicts = llm.extract_json(raw)
    by_name = {v.get("skill"): v for v in verdicts}
    results = []
    clean = 0
    for name in sorted(skills):
        v = by_name.get(name, {"violates": None})
        ok = v.get("violates") is False
        clean += ok
        results.append({
            "skill": name, "pass": ok,
            "offending_phrases": v.get("offending_phrases") or [],
            "rewrite_hint": v.get("rewrite_hint") or "",
        })
    return {
        "tier": "judge",
        "score": "%d/%d clean" % (clean, len(skills)),
        "pass": clean == len(skills),
        "results": results,
    }
