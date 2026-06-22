# Methodology

RIV-Bench measures one thing precisely: whether a verification method can tell, for a proposed remediation, that the control's **intent** is satisfied — distinguishing genuine fixes from changes that pass a linter while leaving the control violated.

## 1. The unit of evaluation: a remediation case

Each fixture is a single case describing a finding and a proposed fix. Cases conform to [`schema/remediation-case.schema.json`](../schema/remediation-case.schema.json). The fields that drive scoring are:

- `lint_status` — `pass` or `fail`. Whether the candidate remediation is syntactically/structurally valid and applies cleanly under a standard validator. This is the signal a linter-only pipeline relies on.
- `control_intent_satisfied` — ground-truth boolean. Whether the control's intent is *actually* satisfied after the candidate remediation, judged against the `intent_predicate`.
- `failure_class` — one of `correct`, `lint-fail`, `lint-pass-but-intent-unmet` (see below).
- `intent_predicate` — the checkable condition that defines satisfaction for this control, expressed against required-configuration state (see [`schema/control-intent-predicate.schema.json`](../schema/control-intent-predicate.schema.json)). This is the authoritative ground truth a verifier is graded against.

A case is **not** a request to run live infrastructure. It is a labeled artifact: the misconfiguration, the candidate change, the linter's verdict, and the ground-truth intent verdict.

## 2. Failure taxonomy

| Class | `lint_status` | `control_intent_satisfied` | Description |
|---|---|---|---|
| `correct` | pass | true | Valid change that genuinely satisfies the control |
| `lint-fail` | fail | false | Invalid change; a linter already rejects it |
| `lint-pass-but-intent-unmet` | pass | false | **The silent failure**: passes a linter, control still violated |

A useful fixture set is weighted toward `lint-pass-but-intent-unmet`, because that is the class that separates intent-verification from syntax-checking. It must also contain `correct` cases (to detect false alarms) and at least some `lint-fail` cases (to confirm a method does not simply reject everything).

## 3. What a method outputs

A verification method under test consumes a case (minus the ground-truth labels) and outputs a single decision:

- `accept` — the method asserts the control's intent is satisfied.
- `reject` — the method asserts it is not.

The method may use any inputs in the case except `control_intent_satisfied` and `failure_class` (those are the held-out answer key). A linter-only baseline, for example, outputs `accept` iff `lint_status == pass`.

## 4. Metrics

Define the positive class as "the remediation genuinely satisfies the control's intent" (`control_intent_satisfied == true`). For a method's decisions over the fixture set:

- **TP** — accepted and intent satisfied.
- **FP** — accepted but intent **not** satisfied. *These are false-fixes: the dangerous outcome.*
- **TN** — rejected and intent not satisfied.
- **FN** — rejected but intent was satisfied (a correct fix wrongly blocked).

From these:

```
false_fix_rate        = FP / (TP + FP)        # of approved remediations, fraction not actually compliant
intent_detection_rate = TN / (TN + FP)        # of truly-noncompliant remediations, fraction correctly rejected
false_alarm_rate      = FN / (TP + FN)        # of truly-compliant remediations, fraction wrongly rejected
accuracy              = (TP + TN) / (TP + TN + FP + FN)
```

The headline number is **false_fix_rate**. A linter-only baseline drives it high precisely on the `lint-pass-but-intent-unmet` cases; an intent-verification method aims to drive it toward zero **without** inflating `false_alarm_rate`. Report all four metrics, plus a per-`failure_class` breakdown, so a method cannot hide false-fixes behind good aggregate accuracy.

## 5. Reporting comparable conditions

To make results meaningful, report each method as a row in [`results/RESULTS-TEMPLATE.md`](../results/RESULTS-TEMPLATE.md). Recommended conditions:

- **Baseline (lint-only)** — the shipped `verify_baseline.py`. The floor.
- **Intent-verification method** — any method that checks against required-configuration intent (e.g., ComplyForm's engine). Results reported here; the engine itself is not part of this repository.
- Optional research conditions for the provenance/continuity dimension: a stateless agent vs. a continuity-grounded agent, to test whether durable, source-grounded context reduces false-fixes. RIV-Bench scores the remediation verdicts; provenance-specific metrics (tamper-detection rate, source-grounding accuracy) are defined for that line of work but require fixtures with provenance metadata, which are out of scope for this initial release.

## 6. Reproducibility rules

- Fixtures are fixed and versioned; a result must name the benchmark version (git tag / Zenodo DOI) it was run against.
- The answer-key fields (`control_intent_satisfied`, `failure_class`) must not be consumed by a method under test.
- New cases are added, not edited; changing a label is a new version. See [`CONTRIBUTING.md`](../CONTRIBUTING.md).

## 7. Boundaries

RIV-Bench grades *verification of intent on representative cases*. It does not execute changes against live cloud or OT systems, does not include ComplyForm's proprietary requirement corpus, and does not prescribe a verification method. Those boundaries are deliberate: they keep the benchmark public, safe to publish, and neutral across methods.
