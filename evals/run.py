#!/usr/bin/env python3
"""skill-evals — repeatable quality evals for the skills in this marketplace.

Usage:
  python3 evals/run.py static   [--skill NAME] [--strict] [--json]
  python3 evals/run.py triggers [--backend api|cli|mock] [--model ID]
  python3 evals/run.py judge    [--backend ...]
  python3 evals/run.py apply    --skill NAME [--backend ...]
  python3 evals/run.py all      [--skill NAME] [--save-baseline]
  python3 evals/run.py compare  evals/baselines/<file>.json

Tiers:
  static   no LLM. Frontmatter, description rules, body budgets, dead/orphan
           refs, README/TESTS presence, plugin.json + marketplace sync.
  triggers LLM routes realistic user messages using ONLY frontmatter.
  judge    LLM verdict on description purity (WHEN, not WHAT).
  apply    LLM walks pressure scenarios against the full skill bundle.

Exit codes: 0 pass, 1 findings/failures, 2 usage or backend error.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import apply as apply_mod          # noqa: E402
from lib import judge, llm, report, static_checks, triggers  # noqa: E402


def repo_root_from(args):
    if args.repo:
        return os.path.abspath(args.repo)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def list_skills(repo_root, only=None):
    sdir = os.path.join(repo_root, "skills")
    names = sorted(n for n in os.listdir(sdir)
                   if os.path.isfile(os.path.join(sdir, n, "SKILL.md")))
    if only:
        if only not in names:
            print("error: no skill named %r under %s" % (only, sdir),
                  file=sys.stderr)
            sys.exit(2)
        names = [only]
    return names


def run_static(repo_root, only=None, strict=False):
    names = list_skills(repo_root, only)
    results = {n: static_checks.check_skill(os.path.join(repo_root, "skills", n))
               for n in names}
    repo_findings = [] if only else static_checks.check_repo(repo_root, names)
    if strict:
        results = {n: [("FAIL" if s == "WARN" else s, c, m) for s, c, m in f]
                   for n, f in results.items()}
        repo_findings = [("FAIL" if s == "WARN" else s, c, m)
                         for s, c, m in repo_findings]
    return results, repo_findings


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("tier", choices=["static", "triggers", "judge", "apply",
                                    "all", "compare"])
    p.add_argument("baseline", nargs="?", help="baseline file (compare only)")
    p.add_argument("--skill", help="limit to one skill")
    p.add_argument("--repo", help="repo root (default: parent of evals/)")
    p.add_argument("--backend", choices=["api", "cli", "mock"])
    p.add_argument("--model", help="model id for LLM tiers")
    p.add_argument("--strict", action="store_true", help="treat WARN as FAIL")
    p.add_argument("--json", action="store_true", help="emit scorecard JSON")
    p.add_argument("--save-baseline", action="store_true")
    args = p.parse_args()

    repo_root = repo_root_from(args)
    cases_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cases")

    static_results = repo_findings = trig = jud = None
    apply_results = []
    try:
        if args.tier in ("static", "all"):
            static_results, repo_findings = run_static(repo_root, args.skill,
                                                       args.strict)
        if args.tier in ("triggers", "all"):
            skills = triggers.collect_descriptions(repo_root)
            trig = triggers.run(repo_root, skills,
                                os.path.join(cases_dir, "routing.json"),
                                backend=args.backend, model=args.model)
        if args.tier in ("judge", "all"):
            skills = triggers.collect_descriptions(repo_root)
            jud = judge.run(skills, backend=args.backend, model=args.model)
        if args.tier in ("apply", "all"):
            scen_dir = os.path.join(cases_dir, "scenarios")
            for name in list_skills(repo_root, args.skill):
                if args.tier == "all" and not os.path.isfile(
                        os.path.join(scen_dir, name + ".json")):
                    continue  # `all` runs apply only where scenarios exist
                apply_results.append(
                    apply_mod.run(repo_root, name, backend=args.backend,
                                  model=args.model, cases_dir=scen_dir))
        if args.tier == "compare":
            if not args.baseline:
                print("usage: run.py compare <baseline.json>", file=sys.stderr)
                sys.exit(2)
            static_results, repo_findings = run_static(repo_root,
                                                       strict=args.strict)
            card = report.assemble(repo_root, static_results, repo_findings)
            text, regressed = report.compare(card, args.baseline)
            print(text)
            sys.exit(1 if regressed else 0)
    except llm.BackendUnavailable as e:
        print("backend error: %s" % e, file=sys.stderr)
        sys.exit(2)

    card = report.assemble(repo_root, static_results, repo_findings,
                           trig, jud, apply_results or None)
    print(json.dumps(card, indent=2) if args.json else report.render(card))
    if args.save_baseline:
        path = report.save_baseline(card, repo_root)
        print("baseline saved: %s" % os.path.relpath(path, repo_root),
              file=sys.stderr)
    sys.exit(0 if card["pass"] else 1)


if __name__ == "__main__":
    main()
