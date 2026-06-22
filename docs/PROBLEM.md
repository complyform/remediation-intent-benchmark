# The Problem: Verifying Remediation Intent, Not Remediation Syntax

## Summary

Automated tools can now detect compliance misconfigurations in infrastructure-as-code and propose, or apply, fixes. The open problem is not detection or generation — it is **verification**: confirming that a proposed change actually satisfies the *intent* of the control it claims to fix. Today's tooling can confirm a change is syntactically valid and that a plan applies cleanly. Nothing in the standard pipeline confirms the control is genuinely satisfied afterward. This gap produces a specific, dangerous failure mode and is the reason automated remediation is not trusted on high-consequence infrastructure.

## The silent failure

Consider an automated remediation pipeline. A finding is raised, a change is proposed, the change parses, a validator passes, a plan diff looks reasonable, and the tool reports success. Every signal is green. Yet the control can still be violated, because **passing a linter is not the same as satisfying a control's intent**:

- An AWS S3 public-access remediation can set some — but not all — of the four block-public-access settings, and add no guard against a public bucket *policy*. Valid configuration; bucket still reachable.
- A CloudTrail-encryption remediation can reference a KMS key whose key policy does not grant the CloudTrail service permission to use it. Valid configuration; encryption setup is operationally broken.
- A network remediation can narrow one over-permissive rule while another rule, or another protocol, still exposes a management port to the internet. Valid configuration; intent unmet across rules.
- A GCP bucket remediation can remove a public `allUsers` grant while an `allAuthenticatedUsers` grant — any Google account — remains. Valid configuration; still effectively public.

In each case a syntactic or single-resource check passes. The control's intent is not met. The pipeline reports success.

## Why this is acute for critical infrastructure and OT

In cloud environments the cost of a silent false-fix is risk and remediation churn. In operational technology and other critical-infrastructure settings the cost is higher and the safety net is thinner:

- **You often cannot validate by replay.** There is no `plan` step that re-derives ground truth for a running physical process; verification must be done before commit, from a model of intent, not by trying the change and observing.
- **Patch windows are long and changes are heavy.** A wrong change is not a quick rollback; it can fault a controller or require a maintenance window measured in weeks.
- **The blast radius is physical.** "Reported success while the control is unmet" is not an inconvenience; it is an undetected exposure on a system that protects something physical.

This is why an automated remediation, however capable, is gated behind manual review in these environments. The missing primitive is trustworthy verification: a way to prove a proposed change satisfies the control's intent *before* it is trusted.

## What "verifying intent" requires

Three properties must hold and be demonstrable for a remediation to be trustworthy:

1. **Correctness against intent.** The change must satisfy the control's intent — checked against authoritative required-configuration ground truth — not merely pass a syntactic linter. This is hard because controls across frameworks can contradict, so a change can satisfy one control while violating another, and intent is frequently a property of the *whole* configuration (multiple rules, cross-resource references), not a single line.
2. **Authenticated provenance.** When the proposing agent is autonomous and accumulates memory over time, the change must be bound to the authoritative evidence it derived from, to an untampered record, and to an authorization envelope — so a reviewer can confirm not only that the change is correct but that it was *legitimately produced* and not the output of drifted or poisoned memory.
3. **Bounded behavior.** On infrastructure that cannot be validated by replay, the agent's remediation behavior must be bounded with measurable false-fix and drift rates, and the verification must act as a hard pre-commit gate.

## What this benchmark contributes

RIV-Bench operationalizes property (1) — correctness against intent — into a measurable, public yardstick:

- A labeled fixture set of `(misconfiguration, candidate_remediation)` pairs across openly available frameworks, each tagged `correct`, `lint-fail`, or `lint-pass-but-intent-unmet`.
- A precise definition of the **false-fix rate** and related metrics (see `METHODOLOGY.md`).
- A naive lint-only baseline that, by construction, approves the silent-failure class — making the gap reproducible and quantifiable.

It does not publish a solution method. It makes the problem concrete enough that any method — including a continuity-grounded, provenance-authenticating one — can be measured against a fixed standard, and so that the difference between "passes a linter" and "satisfies the control" stops being a matter of assertion.
