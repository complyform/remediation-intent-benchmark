#!/usr/bin/env python3
"""
RIV-Bench baseline verifier.

This is a DELIBERATELY NAIVE baseline: it accepts a remediation if and only if it
passes the linter (lint_status == "pass"). Run over the fixtures, it approves the
`lint-pass-but-intent-unmet` cases by construction -- which is the whole point. The
gap it produces is the gap a real intent-verification method must close.

This file does NOT implement intent verification. ComplyForm's intent-verification
engine and its multi-framework requirement corpus are not part of this repository;
their results are reported in results/ against this same fixture set.

Usage:
    pip install pyyaml
    python harness/verify_baseline.py --fixtures fixtures
"""

import argparse
import glob
import os
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

REQUIRED_FIELDS = ("id", "lint_status", "control_intent_satisfied", "failure_class")


def load_cases(fixtures_dir):
    paths = sorted(glob.glob(os.path.join(fixtures_dir, "**", "*.yaml"), recursive=True))
    cases = []
    for path in paths:
        with open(path, "r", encoding="utf-8") as fh:
            case = yaml.safe_load(fh)
        missing = [f for f in REQUIRED_FIELDS if f not in case]
        if missing:
            sys.exit(f"{path}: missing required field(s): {', '.join(missing)}")
        case["_path"] = path
        cases.append(case)
    if not cases:
        sys.exit(f"No fixture .yaml files found under {fixtures_dir!r}")
    return cases


def baseline_decision(case):
    """Naive baseline: accept iff the candidate remediation passes the linter."""
    return case["lint_status"] == "pass"


def score(cases):
    # Positive class = "remediation genuinely satisfies the control's intent".
    tp = fp = tn = fn = 0
    per_class = {}
    false_fixes = []

    for case in cases:
        accepted = baseline_decision(case)
        satisfied = bool(case["control_intent_satisfied"])
        cls = case["failure_class"]
        per_class.setdefault(cls, {"n": 0, "accepted": 0, "false_fix": 0})
        per_class[cls]["n"] += 1
        if accepted:
            per_class[cls]["accepted"] += 1

        if accepted and satisfied:
            tp += 1
        elif accepted and not satisfied:
            fp += 1
            per_class[cls]["false_fix"] += 1
            false_fixes.append(case["id"])
        elif not accepted and not satisfied:
            tn += 1
        else:  # not accepted and satisfied
            fn += 1

    return tp, fp, tn, fn, per_class, false_fixes


def rate(num, den):
    return (num / den) if den else 0.0


def main():
    ap = argparse.ArgumentParser(description="RIV-Bench naive lint-only baseline.")
    ap.add_argument("--fixtures", default="fixtures", help="Path to the fixtures directory.")
    args = ap.parse_args()

    cases = load_cases(args.fixtures)
    tp, fp, tn, fn, per_class, false_fixes = score(cases)
    total = tp + fp + tn + fn

    print(f"\nRIV-Bench baseline (lint-only) over {total} cases from {args.fixtures!r}\n")

    print("Confusion matrix (positive = remediation truly satisfies control intent):")
    print(f"  TP (accepted, satisfied)     : {tp}")
    print(f"  FP (accepted, NOT satisfied) : {fp}   <- false-fixes (the dangerous outcome)")
    print(f"  TN (rejected, NOT satisfied) : {tn}")
    print(f"  FN (rejected, satisfied)     : {fn}\n")

    print("Metrics:")
    print(f"  false_fix_rate        = {rate(fp, tp + fp):.3f}   (of approved remediations, fraction not actually compliant)")
    print(f"  intent_detection_rate = {rate(tn, tn + fp):.3f}   (of truly-noncompliant remediations, fraction correctly rejected)")
    print(f"  false_alarm_rate      = {rate(fn, tp + fn):.3f}   (of truly-compliant remediations, fraction wrongly rejected)")
    print(f"  accuracy              = {rate(tp + tn, total):.3f}\n")

    print("Per failure_class:")
    print(f"  {'class':<28} {'n':>3} {'accepted':>9} {'false_fix':>10}")
    for cls in ("correct", "lint-fail", "lint-pass-but-intent-unmet"):
        row = per_class.get(cls, {"n": 0, "accepted": 0, "false_fix": 0})
        print(f"  {cls:<28} {row['n']:>3} {row['accepted']:>9} {row['false_fix']:>10}")

    if false_fixes:
        print("\nFalse-fixes approved by the lint-only baseline:")
        for cid in false_fixes:
            print(f"  - {cid}")
        print(
            "\nEach of these passes a linter while leaving the control violated. Closing this gap"
            "\n-- driving false_fix_rate toward zero without inflating false_alarm_rate -- is the"
            "\nresearch the benchmark exists to measure."
        )
    print()


if __name__ == "__main__":
    main()
