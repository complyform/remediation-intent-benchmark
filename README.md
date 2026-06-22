# Remediation Intent Verification Benchmark (RIV-Bench)

> A reproducible benchmark for a single question: **when an automated remediation is applied to fix a compliance finding, does it actually satisfy the control's *intent* — or does it merely pass a syntactic linter while leaving the control unmet?**

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20804481.svg)](https://doi.org/10.5281/zenodo.20804481)

RIV-Bench is the open benchmark behind ComplyForm's research on **verifiable trust in autonomous compliance remediation**. It exists because the most dangerous failure in automated remediation is *silent*: a change that returns a clean exit code, passes a configuration linter, and reports success — while the underlying control is still violated. In a cloud account that costs money; on critical infrastructure and OT, where you often cannot re-run a plan to validate and a wrong change has physical consequences, it is disqualifying.

This repository is **disclosure-safe by design**. It contains the *problem*, the *evaluation methodology*, a *fixture set*, and a *naive baseline* you can run today. It does **not** contain ComplyForm's production intent-verification engine or its proprietary multi-framework requirement corpus — those are described and their results reported, not shipped.

## Scope

Fixtures are drawn **only from openly available control frameworks**: the CIS Benchmarks for AWS, Azure, and GCP, and SOC 2. These are the same frameworks ComplyForm offers in its free Community tier, so nothing proprietary is disclosed here. The methodology generalizes to any framework with machine-readable required-configuration ground truth.

## The failure taxonomy this benchmark measures

Every fixture is a `(misconfiguration, candidate_remediation)` pair with a ground-truth label in one of three classes:

| Class | Meaning | Why it matters |
|---|---|---|
| `correct` | Remediation is valid **and** satisfies the control's intent | A verifier must not flag these as wrong (no false alarms) |
| `lint-fail` | Remediation is syntactically/structurally invalid | The easy case — a linter already catches it |
| `lint-pass-but-intent-unmet` | Remediation **passes a linter** but the control is **still violated** | The silent, dangerous case this benchmark exists to expose |

The research claim RIV-Bench is built to test: a method that verifies a remediation against the control's **intent** (the authoritative required-configuration state) detects the `lint-pass-but-intent-unmet` class that linter-only checking approves. The included baseline demonstrates the gap; closing it is the research.

## What's in here

```
docs/PROBLEM.md         The research problem, stated for a general reader
docs/METHODOLOGY.md     Benchmark design, metric definitions, evaluation protocol
schema/                 JSON Schemas for fixtures and control-intent predicates
fixtures/               Labeled (misconfiguration, candidate_remediation) cases
harness/verify_baseline.py   A naive lint-only baseline you can run today
results/RESULTS-TEMPLATE.md   Template for reporting a benchmark run
```

## Run the baseline

The baseline is a deliberately naive verifier: it accepts a remediation **iff it passes the linter**. Run it over the fixtures to see it approve the silent-failure cases — i.e. to see the gap a real intent-verifier must close.

```bash
pip install pyyaml
python harness/verify_baseline.py --fixtures fixtures
```

It prints a confusion matrix against ground truth and a **false-fix rate**: of the remediations the baseline approved, the fraction that do not actually satisfy the control. See `docs/METHODOLOGY.md` for exact definitions.

## How to cite

If you use RIV-Bench, please cite it via the metadata in [`CITATION.cff`](CITATION.cff). Once archived to Zenodo, cite the versioned DOI.

## Related

- ComplyForm GitHub Action (product): https://github.com/complyform/complyform-action
- ComplyForm: https://complyform.dev

## License

Code in this repository is licensed under Apache-2.0 (see [`LICENSE`](LICENSE)). The fixture data and documentation are additionally offered for academic reuse under CC-BY-4.0; attribute via `CITATION.cff`.

## A note on what this benchmark is not

RIV-Bench does not claim a solution. It defines a problem precisely, makes it measurable, and ships a baseline that fails on the interesting cases on purpose. Results for any intent-verification method — including ComplyForm's — belong in `results/`, reported against this fixed, public yardstick.
