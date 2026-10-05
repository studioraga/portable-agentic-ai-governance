# M27 Prerequisites

## Immutable parent

M27 must start from commit `82b9331edbe1d12f30b6283b15584ac506038018`, tag `m26-soc-incident-backup-dr-v0.26.0`.

## Minimum software

- Git
- Python 3.10+
- `venv`
- `pytest` via the project development extra
- OpenSSL/cryptography support already required by previous milestones

## Optional production AppSec tooling

The deterministic validation adapters do not install external scanners. For production evidence, integrate approved tools such as:

- SAST: Semgrep, Bandit, CodeQL
- Secret scanning: Gitleaks, TruffleHog
- SCA: OSV-Scanner, Grype, Trivy
- IaC/container: Checkov, Trivy, Hadolint
- DAST/API: OWASP ZAP, Schemathesis
- Fuzzing: Atheris, Hypothesis, libFuzzer, AFL++
- Penetration test: authorized independent internal or external assessor

Do not place scanner API tokens, private keys, proprietary reports, or raw sensitive payloads in Git. Generated M27 material belongs under ignored `var/m27-*` paths.

## M28 relationship

M28 adds authority-bound evidence controls for organizational governance, personnel security/training, physical/environmental security, and business-continuity exercises. This document keeps its original milestone authority; M28 consumes its applicable evidence without rewriting historical M0–M27 claims. Real-world HR/facility/BCP controls require authorized production records—local Python validation proves the evidence contract, signatures, freshness and source binding only.

## M29 relationship

M29 aggregates the signed M21 platform prerequisite and M22–M28 enterprise-security evidence into one cross-domain Node1/Node2 validation package. This historical document remains authoritative for its original milestone; M29 consumes its evidence without rewriting its semantics. M29 distinguishes evidence-integrity success from production readiness and remains fail-closed while M21 platform controls or real M27/M28 production evidence are outstanding. See `docs/M29-Enterprise-Cross-Domain-Node1-Node2-Validation.md`, `docs/Prerequisites-M29.md`, `docs/Deployment-M29.md`, and `docs/Validation-M29.md`.
