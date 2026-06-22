# Contributing to RIV-Bench

RIV-Bench is a fixed, versioned yardstick. The most valuable contribution is a new
case that exposes a way to pass a linter while missing a control's intent.

## Adding a case

1. Create a new file under `fixtures/<framework>/`, named `case-NNNN-short-slug.yaml`.
2. Conform to [`schema/remediation-case.schema.json`](schema/remediation-case.schema.json).
3. Use **openly available** frameworks only (CIS AWS/Azure/GCP, SOC 2). Do not add
   content from gated/commercial frameworks.
4. Set the ground-truth fields honestly: `lint_status`, `intent_predicate`,
   `control_intent_satisfied`, `failure_class`.
5. Prefer `lint-pass-but-intent-unmet` cases, and document the trap under the
   predicate's `common_bypasses`.
6. Keep snippets minimal and self-contained.

## Reproducibility rules

- **Do not edit the labels of an existing case.** Relabeling is a new benchmark version.
- New cases are additive; cut a new tag (and Zenodo version) when the set changes.
- A reported result must name the benchmark version (git tag / DOI) it ran against.

## What does not belong here

- ComplyForm's verification engine or any proprietary requirement corpus.
- Method internals. Report a method's measured outcomes in `results/`, not its code.
- Live cloud or OT credentials, state, or any real environment data.

## Checks before opening a PR

- `python harness/verify_baseline.py --fixtures fixtures` runs cleanly.
- New files validate against the schema.
