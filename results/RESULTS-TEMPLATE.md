# Results

Report each verification method as a row, run against a named benchmark version (git tag or Zenodo DOI). Do not consume the answer-key fields (`control_intent_satisfied`, `failure_class`) inside a method under test. Metric definitions are in [`../docs/METHODOLOGY.md`](../docs/METHODOLOGY.md).

## Benchmark version

- Fixture set version (tag / DOI): `vX.Y` / `<doi>`
- Number of cases: `N`
- Class distribution: `correct: _, lint-fail: _, lint-pass-but-intent-unmet: _`

## Method comparison

| Method | false_fix_rate ↓ | intent_detection_rate ↑ | false_alarm_rate ↓ | accuracy ↑ | Notes |
|---|---|---|---|---|---|
| Baseline (lint-only) | | | | | shipped `harness/verify_baseline.py` |
| Intent-verification method A | | | | | describe inputs used; engine not in this repo |
| ... | | | | | |

The headline comparison is **false_fix_rate**: how often a method approves a remediation that does not actually satisfy the control. A credible intent-verification method drives it far below the lint-only baseline **without** inflating `false_alarm_rate` (it must not achieve a low false-fix rate by rejecting everything).

## Per-failure-class breakdown (per method)

| failure_class | n | accepted | false_fix |
|---|---|---|---|
| correct | | | |
| lint-fail | | | |
| lint-pass-but-intent-unmet | | | |

A method's value shows up almost entirely in the `lint-pass-but-intent-unmet` row: that is the class a linter approves and an intent-verifier must reject.

## Optional: provenance / continuity conditions

For the line of work on authenticated provenance and continuity-grounded remediation, report paired conditions (e.g. stateless agent vs. continuity-grounded agent) on the same fixtures, plus the provenance-specific metrics defined in `METHODOLOGY.md` (tamper-detection rate, source-grounding accuracy) once provenance-bearing fixtures are added. Keep method internals out of this repository; report only the measured outcomes here.
