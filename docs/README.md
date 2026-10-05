# Documentation Index

This directory separates durable architecture and operating contracts from milestone-specific historical records.

## Canonical documentation

| Document | Purpose |
|---|---|
| [`Architecture.md`](Architecture.md) | Architecture and trust boundaries that remain valid across milestones |
| [`Validation.md`](Validation.md) | Common validation/evidence layers |
| [`Prerequisites.md`](Prerequisites.md) | Common host, Python, Git, and runtime prerequisites |
| [`oneshot-deployment.md`](oneshot-deployment.md) | Progressive one-shot deployment contract and current milestone mapping |
| [`Milestones.md`](Milestones.md) | M0–M21 evolution and current release state |
| [`Documentation-Audit-M21.1.md`](Documentation-Audit-M21.1.md) | Commit-by-commit documentation audit and refactor rationale |

## Current milestone

- [`M21-Embedded-Linux-Platform-Security-Validation.md`](M21-Embedded-Linux-Platform-Security-Validation.md)
- [`Prerequisites-M21.md`](Prerequisites-M21.md)
- [`Deployment-M21.md`](Deployment-M21.md)
- [`Validation-M21.md`](Validation-M21.md)

## Historical milestone records

Milestone-specific files such as `M8-*.md`, `Prerequisites-M8.md`, `Deployment-M8.md`, and `Validation-M8.md` describe the milestone that introduced that capability. They should be read as historical/feature-specific records, not as substitutes for the canonical current workflow.

When a historical document and a current canonical document differ on release status or operating procedure, prefer:

1. the source code and tests at the selected Git tag;
2. `README.md` / `instruction.md` for current orientation and execution;
3. canonical docs in this directory;
4. milestone-specific historical docs for feature detail.


## M22 enterprise-security extension

M22 extends the frozen M21.1 baseline with the authoritative CISSP-domain / enterprise-security control foundation. See `docs/M22-CISSP-Enterprise-Security-Control-Foundation.md`, `docs/Prerequisites-M22.md`, `docs/Deployment-M22.md`, and `docs/Validation-M22.md`. M0–M21 historical behavior remains unchanged; M22 records alignment and gaps and does not assert CISSP, ISO/IEC 27001, ISO/IEC 42001, or CRA certification/conformity.


### M22 relationship

This document remains authoritative for its historical milestone scope. M22 does not rewrite that milestone; it inventories and maps its reusable controls/evidence into the enterprise-security foundation and records remaining gaps in `governance/enterprise/m22/gap-register.json`. See `docs/M22-CISSP-Enterprise-Security-Control-Foundation.md`.

## M23 relationship

M23 extends the frozen M22 enterprise-security foundation with enterprise human identity, OIDC federation evidence, strong MFA context, phishing-resistant privileged authentication, expiring entitlement review, signed single-use JIT privilege grants, dual-approved break-glass access, segregation of duties, and independent Node1/Node2 verification. The authoritative M23 documents are `docs/M23-Enterprise-Identity-MFA-PAM.md`, `docs/Prerequisites-M23.md`, `docs/Deployment-M23.md`, and `docs/Validation-M23.md`. Historical M0-M22 behavior and evidence remain immutable.

## M24 relationship

M24 extends the frozen M23 baseline with deterministic asset inventory/ownership/classification, retention and legal-hold handling, evidence-backed sanitization, default-deny DLP/controlled export, and cryptographic key-lifecycle evidence. This historical document remains authoritative for its original milestone; M24 consumes its reusable evidence but does not rewrite M0-M23 semantics. See `docs/M24-Asset-Security-Data-Protection-Crypto-Lifecycle.md`, `docs/Prerequisites-M24.md`, `docs/Deployment-M24.md`, and `docs/Validation-M24.md`. M24 closes only `CISSP-D2-001..003`; M21-dependent Domain-3 platform/hardware-root gaps remain open.

### M24 authoritative documents

- `M24-Asset-Security-Data-Protection-Crypto-Lifecycle.md`
- `Prerequisites-M24.md`
- `Deployment-M24.md`
- `Validation-M24.md`
