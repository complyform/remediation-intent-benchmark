# Fixtures

Each file here is one labeled remediation case conforming to [`../schema/remediation-case.schema.json`](../schema/remediation-case.schema.json). Cases are grouped by framework: `cis-aws/`, `cis-azure/`, `cis-gcp/`, `soc2/`. All frameworks used here are openly available; no proprietary control content appears.

## What a case captures

- A real misconfiguration that violates a named control.
- A **candidate remediation** — the change whose intent-satisfaction is being judged.
- `lint_status` — whether a standard validator would accept the candidate.
- `intent_predicate` — the authoritative condition(s) that define satisfaction, evaluated over the whole relevant configuration.
- `control_intent_satisfied` + `failure_class` — the ground-truth answer key.

The interesting cases are `lint-pass-but-intent-unmet`: the candidate parses and validates, but the control is still violated. Those are the ones a linter-only pipeline approves and an intent-verifier must catch.

## Control numbering

CIS Benchmark item numbers change across benchmark versions. `control_ref` here is **descriptive**, naming what the control requires rather than pinning a version-specific number. SOC 2 criteria (e.g. CC6.x) are referenced by trust-services criterion, with a representative technical interpretation, since SOC 2 itself does not prescribe specific configurations.

## Adding cases

- Add a new file; do not edit an existing case's labels. Changing a label is a new benchmark version.
- Validate against the schema before submitting.
- Prefer cases that expose a *new* way to pass a linter while missing intent (a new entry for a predicate's `common_bypasses`).
- Keep snippets minimal — enough to make the case unambiguous, no more.

See [`../CONTRIBUTING.md`](../CONTRIBUTING.md).
