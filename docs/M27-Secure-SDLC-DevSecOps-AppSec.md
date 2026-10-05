# M27 — Secure SDLC / DevSecOps / AppSec

M27 extends the enterprise security control plane with deterministic application-security release gates. It closes the M22 `CISSP-D6-002` capability gap without changing any historical M0–M26 release.

## Security objectives

M27 requires evidence for SAST, DAST/API security testing, secret scanning, software-composition analysis (SCA), IaC/container scanning, fuzzing, and an independently authored penetration-test report. A release is denied when a required category is missing or an unresolved critical/high finding remains.

## Authority model

`Reasoning != Authority` remains unchanged. Scanner output is evidence; it does not grant release authority. Release authority is a deterministic policy decision over source-bound evidence. Node1 may produce/sign M27 material; Node2 only verifies it.

## Production versus validation evidence

The repository contains deterministic local validation adapters so the control plane can be tested offline. These adapters are not substitutes for Semgrep/Bandit/CodeQL, Gitleaks/TruffleHog, OSV-Scanner/Grype/Trivy, Checkov/Trivy/Hadolint, ZAP/Schemathesis, Atheris/Hypothesis/libFuzzer/AFL++, or an authorized independent penetration test.

`production_pentest_completed_claim` remains `false`. Before M30 production readiness, simulated pentest evidence must be replaced with real authorized evidence of type `AUTHORIZED_EXTERNAL_OR_INDEPENDENT_INTERNAL`.

## M27 controls

- `ENT-APPSEC-001` — SAST release gate
- `ENT-APPSEC-002` — DAST/API security gate
- `ENT-APPSEC-003` — secret-scanning gate
- `ENT-APPSEC-004` — SCA gate
- `ENT-APPSEC-005` — IaC/container security gate
- `ENT-APPSEC-006` — fuzzing crash/hang gate
- `ENT-APPSEC-007` — independent penetration-test evidence gate
- `ENT-SDLC-001` — default-deny secure-SDLC release gate
- `ENT-SDLC-002` — signed, source-bound AppSec release evidence

## Gap closure

M22 records `CISSP-D6-002` as `GAP`. M27 records a new closure artifact rather than editing the M22 history. The closure scope is `CONTROL_PLANE_CAPABILITY`; actual production scanner/pentest evidence remains a later release-readiness input.

## M28 relationship

M28 adds authority-bound evidence controls for organizational governance, personnel security/training, physical/environmental security, and business-continuity exercises. This document keeps its original milestone authority; M28 consumes its applicable evidence without rewriting historical M0–M27 claims. Real-world HR/facility/BCP controls require authorized production records—local Python validation proves the evidence contract, signatures, freshness and source binding only.

## M29 relationship

M29 aggregates the signed M21 platform prerequisite and M22–M28 enterprise-security evidence into one cross-domain Node1/Node2 validation package. This historical document remains authoritative for its original milestone; M29 consumes its evidence without rewriting its semantics. M29 distinguishes evidence-integrity success from production readiness and remains fail-closed while M21 platform controls or real M27/M28 production evidence are outstanding. See `docs/M29-Enterprise-Cross-Domain-Node1-Node2-Validation.md`, `docs/Prerequisites-M29.md`, `docs/Deployment-M29.md`, and `docs/Validation-M29.md`.
