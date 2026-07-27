"""A0: val-split run-to-run spread, and the val-set size it implies.

Reads `eval --split val` stdout logs, classifies each, and reports the spread
of the valid runs plus the task count needed to resolve `accept_delta`.

Usage:  .venv/bin/python a0_stats.py <log> [<log> ...]
        .venv/bin/python a0_stats.py --selftest

Exit 0 on a reportable result. Exit 1 on anything that must NOT be reported.
The exit code is the contract: never record a verdict from an exit-1 run.

Design notes, each earned by a red-team break:
  * `sd == 0` is not the degenerate case; `sd below measurement resolution` is.
    Task scores are quantized to 2 decimals, so on n tasks the smallest
    resolvable sd of means is 0.01/n. Below that, required_n is not estimable
    and printing a number fabricates the mission's headline result.
  * A task scoring exactly 0.00 without the `rollout failed:` marker is the
    signature of silent degradation (empty rollout, judge parse failure).
    Both land inside any plausible-mean band, so the band cannot catch them.
    Quarantine on the zero, not on the mean.
  * required_n uses a chi-square upper bound on sigma, not the point estimate.
    A point estimate from 5 runs carries roughly 70% relative error.
"""
from __future__ import annotations
import os
import re
import statistics
import sys

ACCEPT_DELTA = 0.02          # lib/types.py:53
MIN_RUNS = 5                 # the mission's definition of done requires five
EXPECT_TASKS = 5             # semantic-organization val split; any other n is a defect
SANITY = (0.40, 1.00)        # catastrophic-degradation backstop; history 0.889/0.900
SCORE_QUANT = 0.01           # harness.py prints task scores to 2 decimals
RESOLUTION_MULT = 2          # sd must clear TWO quanta; one is a quantization ladder

# chi-square lower critical values, alpha=0.05, by degrees of freedom (k-1).
# sigma_upper^2 = (k-1) * s^2 / chi2_lower  ->  a conservative required_n.
_CHI2_LOWER = {4: 0.7107, 5: 1.1455, 6: 1.6354, 7: 2.1673, 8: 2.7326, 9: 3.3251}

FORMULA = (
    "sd_task = sd_of_means * sqrt(n); "
    "sigma_upper = sd_task * sqrt((k-1)/chi2_lower(0.05, k-1)); "
    "required_n = (sigma_upper / (accept_delta / 2 / sqrt(2)))^2. "
    "The sqrt(2) treats the gate's two means as independent, which is "
    "conservative: lib/gate.py pairs candidate to incumbent by task_id, and "
    "positive pairing correlation lowers required_n. Note gate.decide applies "
    "a raw threshold and runs no significance test, so required_n answers "
    "'how many tasks until run noise is small next to accept_delta', not "
    "'what n makes a t-test significant'."
)

MEAN_RE = re.compile(r"^VAL mean: ([0-9.]+)$", re.M)
TASK_RE = re.compile(r"^  (\S+): ([01]\.[0-9]+)$", re.M)
COST_RE = re.compile(r"^Cost: \$([0-9.]+)$", re.M)


def classify(path: str) -> dict:
    """Classify one log. status is 'valid', 'void:<why>', or 'quarantine:<why>'."""
    out = {"path": path, "status": "", "mean": None, "n": 0, "cost": 0.0, "detail": ""}
    try:
        text = open(path).read()
    except OSError as e:
        out["status"] = f"void:unreadable ({type(e).__name__})"
        return out

    cost_m = COST_RE.search(text)
    out["cost"] = float(cost_m.group(1)) if cost_m else 0.0
    tasks = [(tid, float(v)) for tid, v in TASK_RE.findall(text)]
    out["n"] = len(tasks)
    mean_m = MEAN_RE.search(text)

    # Void A: a task raised and the broad handler in rollout.py caught it.
    if "rollout failed:" in text:
        out["status"] = "void:rollout-failed"
        return out
    # Void B: the harness crashed. BudgetExceeded propagates (lib/rollout.py:36
    # sits OUTSIDE the try at :37), so a cap breach is a traceback with no mean,
    # no cost line, and no 'rollout failed:' marker.
    if mean_m is None:
        out["status"] = "void:no-mean-line"
        return out
    if not tasks:
        out["status"] = "void:no-task-scores"
        return out

    # Quarantine: a 0.00 task with no failure marker is silent degradation --
    # an empty final_text (sdk.py never checks ResultMessage.is_error) or a
    # judge parse failure (scorer.py falls back to 0.0 with raw judge text).
    zeros = [tid for tid, v in tasks if v == 0.0]
    if zeros:
        out["status"] = f"quarantine:zero-task ({','.join(zeros)})"
        for tid in zeros:
            m = re.search(rf"^  {re.escape(tid)}: 0\.0+$\n(.*)$", text, re.M)
            out["detail"] += f"\n    {tid} rationale: {m.group(1).strip() if m else '<none>'}"
        return out

    mean = float(mean_m.group(1))
    # Strict at the floor: a grader collapsed exactly onto 0.40 is degradation,
    # not a grade, and an inclusive bound admits it.
    if not (SANITY[0] < mean <= SANITY[1]):
        out["status"] = f"void:implausible-mean ({mean:.3f})"
        return out

    out["status"] = "valid"
    out["mean"] = mean
    return out


def report(paths: list[str]) -> int:
    seen, uniq = set(), []
    for p in paths:
        key = os.path.realpath(p)
        if key in seen:
            print(f"skipping duplicate path: {p}")
            continue
        seen.add(key)
        uniq.append(p)

    rows = [classify(p) for p in uniq]
    for r in rows:
        shown = f"{r['mean']:.3f}" if r["mean"] is not None else "--"
        print(f"{r['status']:38s} {r['path']}  mean={shown} tasks={r['n']} "
              f"cost=${r['cost']:.4f}{r['detail']}")

    print(f"\ncost reported across all logs: ${sum(r['cost'] for r in rows):.4f}")
    print("note: cost is advisory only. lib/sdk.py leaves cost at 0.0 when "
          "ResultMessage.total_cost_usd is None, which is the normal case under "
          "Claude Code session auth. Bound this mission by RUN COUNT, not dollars.")

    quarantined = [r for r in rows if r["status"].startswith("quarantine:")]
    if quarantined:
        print(f"\nNOT REPORTABLE: {len(quarantined)} run(s) quarantined on a 0.00 task.")
        print("A zero without a 'rollout failed:' marker is silent degradation, not a "
              "grade. Record the rationales above in the ledger and hand back.")
        return 1

    valid = [r for r in rows if r["status"] == "valid"]
    if len(valid) < MIN_RUNS:
        print(f"\nNOT REPORTABLE: {len(valid)} valid run(s), need {MIN_RUNS}.")
        print("Do not record a verdict.")
        return 1

    counts = {r["n"] for r in valid}
    if len(counts) != 1:
        print(f"\nNOT REPORTABLE: runs disagree on task count: {sorted(counts)}.")
        print("Do not record a verdict.")
        return 1

    n = counts.pop()
    if n != EXPECT_TASKS:
        print(f"\nNOT REPORTABLE: every run scored {n} tasks, expected {EXPECT_TASKS}.")
        print("The val split is 5 tasks (V01-V05). A different count means the split "
              "or the log format changed; more runs cannot fix it. Do not record a verdict.")
        return 1
    k = len(valid)
    means = [r["mean"] for r in valid]
    sd = statistics.stdev(means)
    spread = round(max(means) - min(means), 4)
    resolution = SCORE_QUANT / n

    print(f"\nvalid runs:   {k}")
    print(f"tasks/run:    {n}")
    print(f"val means:    {[f'{x:.3f}' for x in means]}")
    print(f"sd of means:  {sd:.4f}")
    print(f"range:        {spread:.4f}")
    floor = RESOLUTION_MULT * resolution
    print(f"resolution:   {resolution:.4f}  (score quantum {SCORE_QUANT} over {n} tasks); "
          f"reporting floor {floor:.4f}")

    if sd < floor:
        print(f"required n:   NOT ESTIMABLE — sd {sd:.4f} is below the {floor:.4f} "
              f"reporting floor ({RESOLUTION_MULT} x the {resolution:.4f} resolution of "
              f"{n} two-decimal task scores). Means separated by one quantum step form "
              "a ladder, not a measured spread.")
        print(f"VERDICT: no run-to-run noise resolvable at n={n}. The grader looks "
              "deterministic across runs, which CONTRADICTS the plan's diagnosis that "
              "the gate measures noise. Report this and stop. Do not raise the "
              "val-set size on this evidence, and do not report a number.")
        print(f"\nformula: {FORMULA}")
        return 0

    sd_task = sd * n ** 0.5
    chi2 = _CHI2_LOWER.get(k - 1)
    if chi2 is None:
        print(f"NOT REPORTABLE: no chi-square constant for k={k}.")
        return 1
    sigma_upper = sd_task * ((k - 1) / chi2) ** 0.5
    target = ACCEPT_DELTA / 2 / (2 ** 0.5)
    need_point = (sd_task / target) ** 2
    need_upper = (sigma_upper / target) ** 2
    usable = spread < ACCEPT_DELTA

    print(f"per-task sd:  {sd_task:.4f}  (95% upper bound {sigma_upper:.4f})")
    if need_upper < n:
        print(f"required n:   <= {n} — the current split already resolves "
              f"+{ACCEPT_DELTA} (point {need_point:.1f}, upper bound {need_upper:.1f}).")
    else:
        print(f"required n:   {need_upper:.0f}   (95% upper bound; point estimate "
              f"{need_point:.0f}. Use the upper bound: a point estimate from {k} runs "
              "carries ~70% relative error. Confidence: low.)")
    print(f"VERDICT: range {spread:.4f} {'<' if usable else '>='} accept_delta "
          f"{ACCEPT_DELTA} -> gate {'USABLE' if usable else 'UNUSABLE'} at n={n}")
    print(f"\nformula: {FORMULA}")
    return 0


# ── self-check ────────────────────────────────────────────────────────────
# One runnable check. Every case below is a red-team break this script must
# refuse. Run: .venv/bin/python a0_stats.py --selftest
def _selftest() -> int:
    import tempfile, pathlib

    def log(mean, scores, cost="1.2000", rationale="ok"):
        body = f"Running 5 val tasks for semantic-organization...\n\nVAL mean: {mean}\n"
        for i, s in enumerate(scores, 1):
            body += f"  V0{i}: {s}\n    {rationale}\n"
        return body + f"\nCost: ${cost}\n"

    ok = [0.90, 1.00, 0.80, 0.90, 0.82]
    cases = []
    with tempfile.TemporaryDirectory() as d:
        d = pathlib.Path(d)

        def w(name, text):
            p = d / name
            p.write_text(text)
            return str(p)

        varying = [w(f"v{i}.log", log(m, ok)) for i, m in
                   enumerate(["0.884", "0.900", "0.860", "0.920", "0.870"])]
        cases.append(("five varying runs -> reportable", varying, 0, "gate UNUSABLE"))

        ident = [w(f"i{i}.log", log("0.884", ok)) for i in range(5)]
        cases.append(("five identical -> not estimable", ident, 0, "NOT ESTIMABLE"))

        eps = [w(f"e{i}.log", log(m, ok)) for i, m in
               enumerate(["0.884", "0.886", "0.884", "0.885", "0.884"])]
        cases.append(("sd below resolution -> not estimable", eps, 0, "NOT ESTIMABLE"))

        crash = w("c.log", "Traceback...\nlib.budget.BudgetExceeded: Spent $3.01\n")
        cases.append(("crash log -> void", ident[:4] + [crash], 1, "void:no-mean-line"))

        rf = w("rf.log", log("0.700", ok).replace("    ok", "    rollout failed: APIError", 1))
        cases.append(("rollout failed -> void", ident[:4] + [rf], 1, "void:rollout-failed"))

        zero = w("z.log", log("0.684", [0.00, 1.00, 0.80, 0.90, 0.82]))
        cases.append(("0.00 task inside band -> quarantine", ident[:4] + [zero], 1,
                      "quarantine:zero-task"))

        low = w("lo.log", log("0.133", [0.20, 0.13, 0.10, 0.15, 0.12]))
        cases.append(("catastrophic mean -> void", ident[:4] + [low], 1,
                      "void:implausible-mean"))

        cases.append(("four runs -> not reportable", ident[:4], 1, "need 5"))
        cases.append(("duplicates deduped", ident[:4] + [ident[0]], 1, "duplicate"))
        cases.append(("missing file -> void", ident[:4] + ["/nope.log"], 1, "void:unreadable"))

        short = w("s.log", log("0.884", [0.90, 1.00, 0.80]))
        cases.append(("task-count clash -> not reportable", ident[:4] + [short], 1,
                      "disagree on task count"))

        ladder = [w(f"q{i}.log", log(m, ok)) for i, m in
                  enumerate(["0.880", "0.882", "0.884", "0.886", "0.888"])]
        cases.append(("quantization ladder -> not estimable", ladder, 0, "NOT ESTIMABLE"))

        four = [w(f"f{i}.log", log(m, [0.90, 1.00, 0.80, 0.90])) for i, m in
                enumerate(["0.884", "0.900", "0.860", "0.920", "0.870"])]
        cases.append(("all runs 4 tasks -> not reportable", four, 1, "expected 5"))

        floor_ = [w(f"fl{i}.log", log("0.400", [0.40, 0.40, 0.40, 0.40, 0.40]))
                  for i in range(5)]
        cases.append(("mean exactly at sanity floor -> void", floor_, 1,
                      "void:implausible-mean"))

        import io, contextlib
        failures = 0
        for name, paths, want_exit, want_text in cases:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                got_exit = report(paths)
            out = buf.getvalue()
            bad = []
            if got_exit != want_exit:
                bad.append(f"exit {got_exit} != {want_exit}")
            if want_text not in out:
                bad.append(f"missing {want_text!r}")
            # the fabrication guard: no case may ever print a zero required n
            if re.search(r"^required n:   [01]\s*$", out, re.M):
                bad.append("FABRICATED a required n of 0 or 1")
            print(f"{'PASS' if not bad else 'FAIL'}  {name}"
                  + ("" if not bad else f"  -> {'; '.join(bad)}"))
            failures += bool(bad)

    print(f"\n{len(cases) - failures}/{len(cases)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    sys.exit(report(sys.argv[1:]))
