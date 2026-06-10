"""Scorecard assembly, rendering, baseline snapshots, and comparison."""

import json
import os
import subprocess


def git_sha(repo_root):
    try:
        out = subprocess.run(["git", "-C", repo_root, "rev-parse", "--short", "HEAD"],
                             capture_output=True, text=True)
        return out.stdout.strip() or "nogit"
    except OSError:
        return "nogit"


def assemble(repo_root, static_results=None, repo_findings=None,
             triggers_result=None, judge_result=None, apply_results=None):
    """Build the scorecard dict from whichever tiers ran."""
    card = {"repo": os.path.basename(os.path.abspath(repo_root)),
            "git": git_sha(repo_root), "tiers": {}}
    if static_results is not None:
        skills = {}
        total_fail = total_warn = 0
        for name, findings in sorted(static_results.items()):
            fails = [f for f in findings if f[0] == "FAIL"]
            warns = [f for f in findings if f[0] == "WARN"]
            total_fail += len(fails)
            total_warn += len(warns)
            skills[name] = {
                "pass": not fails, "fails": len(fails), "warns": len(warns),
                "findings": [{"severity": s, "code": c, "msg": m}
                             for s, c, m in findings],
            }
        repo_f = [{"severity": s, "code": c, "msg": m}
                  for s, c, m in (repo_findings or [])]
        total_fail += sum(1 for f in repo_f if f["severity"] == "FAIL")
        total_warn += sum(1 for f in repo_f if f["severity"] == "WARN")
        card["tiers"]["static"] = {
            "pass": total_fail == 0,
            "score": "%d FAIL / %d WARN" % (total_fail, total_warn),
            "skills": skills, "repo_findings": repo_f,
        }
    if triggers_result is not None:
        card["tiers"]["triggers"] = triggers_result
    if judge_result is not None:
        card["tiers"]["judge"] = judge_result
    if apply_results:
        booled = [r["pass"] for r in apply_results if r["pass"] is not None]
        card["tiers"]["apply"] = {
            "pass": all(booled) if booled else None,
            "skills": apply_results,
        }
    card["pass"] = all(t.get("pass") is not False for t in card["tiers"].values())
    return card


def render(card):
    lines = []
    lines.append("skill-evals — %s @ %s" % (card["repo"], card["git"]))
    lines.append("=" * 56)
    st = card["tiers"].get("static")
    if st:
        lines.append("STATIC   %-6s %s" % ("PASS" if st["pass"] else "FAIL", st["score"]))
        for name, s in st["skills"].items():
            flag = "ok " if s["pass"] else "FAIL"
            lines.append("  %-24s %s  %dF/%dW" % (name, flag, s["fails"], s["warns"]))
            for f in s["findings"]:
                lines.append("      [%s] %s: %s" % (f["severity"], f["code"], f["msg"]))
        for f in st["repo_findings"]:
            lines.append("  repo  [%s] %s: %s" % (f["severity"], f["code"], f["msg"]))
    tr = card["tiers"].get("triggers")
    if tr:
        lines.append("TRIGGERS %-6s %s" % ("PASS" if tr["pass"] else "FAIL", tr["score"]))
        for r in tr["results"]:
            if not r["pass"]:
                lines.append("  MISS #%d %r -> %s (expected %s)"
                             % (r["id"], r["message"][:50], r["choice"], r["expect"]))
    jd = card["tiers"].get("judge")
    if jd:
        lines.append("JUDGE    %-6s %s" % ("PASS" if jd["pass"] else "FAIL", jd["score"]))
        for r in jd["results"]:
            if not r["pass"]:
                lines.append("  %-24s offending: %s" % (r["skill"],
                             "; ".join(r["offending_phrases"])[:120]))
    ap = card["tiers"].get("apply")
    if ap:
        ap_flag = "SKIP" if ap["pass"] is None else ("PASS" if ap["pass"] else "FAIL")
        lines.append("APPLY    %-6s" % ap_flag)
        for sk in ap["skills"]:
            lines.append("  %-24s %s %s" % (sk["skill"],
                         "ok " if sk["pass"] else ("--" if sk["pass"] is None else "FAIL"),
                         sk["score"]))
            for r in sk.get("results", []):
                for g in r["gaps"]:
                    lines.append("      [%s] %s: %s" % (g.get("severity", "?"),
                                 g.get("where", "?"), g.get("issue", "")))
    lines.append("-" * 56)
    lines.append("OVERALL  %s" % ("PASS" if card["pass"] else "FAIL"))
    return "\n".join(lines)


def save_baseline(card, repo_root):
    import datetime
    d = os.path.join(repo_root, "evals", "baselines")
    os.makedirs(d, exist_ok=True)
    fn = "%s-%s.json" % (datetime.date.today().isoformat(), card["git"])
    path = os.path.join(d, fn)
    json.dump(card, open(path, "w", encoding="utf-8"), indent=2)
    return path


def compare(card, baseline_path):
    """Diff current card against a saved baseline. Returns text summary."""
    base = json.load(open(baseline_path, encoding="utf-8"))
    lines = ["compare: %s (%s) -> current (%s)"
             % (os.path.basename(baseline_path), base.get("git"), card.get("git"))]
    b_st = base.get("tiers", {}).get("static", {}).get("skills", {})
    c_st = card.get("tiers", {}).get("static", {}).get("skills", {})
    for name in sorted(set(b_st) | set(c_st)):
        b = b_st.get(name, {"fails": "-", "warns": "-"})
        c = c_st.get(name, {"fails": "-", "warns": "-"})
        if (b.get("fails"), b.get("warns")) != (c.get("fails"), c.get("warns")):
            lines.append("  %-24s %sF/%sW -> %sF/%sW"
                         % (name, b.get("fails"), b.get("warns"),
                            c.get("fails"), c.get("warns")))
    regressed = False
    for name in sorted(set(b_st) | set(c_st)):
        b_f = b_st.get(name, {}).get("fails", 0)
        c_f = c_st.get(name, {}).get("fails", 0)
        b_w = b_st.get(name, {}).get("warns", 0)
        c_w = c_st.get(name, {}).get("warns", 0)
        if isinstance(c_f, int) and isinstance(b_f, int) and \
                (c_f > b_f or c_w > b_w):
            regressed = True
    for tier in ("triggers", "judge"):
        b = base.get("tiers", {}).get(tier, {}).get("score")
        c = card.get("tiers", {}).get(tier, {}).get("score")
        if c is not None and b != c:
            lines.append("  %-24s %s -> %s" % (tier, b, c))
    if len(lines) == 1:
        lines.append("  no changes")
    return "\n".join(lines), regressed
