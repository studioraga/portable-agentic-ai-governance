> Current development milestone: **M27 — Secure SDLC / DevSecOps / AppSec**. Latest immutable tagged parent: **M26 v0.26.0**.

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

## M25 relationship

M25 extends the frozen M24 baseline with explicit network zones, default-deny micro-segmentation, mTLS workload-identity binding, egress allowlisting, network-detection policy and deterministic firewall evidence. This historical document remains authoritative for its original milestone; M25 consumes reusable evidence without rewriting M0-M24 semantics. See `docs/M25-Zero-Trust-Network-Microsegmentation.md`, `docs/Prerequisites-M25.md`, `docs/Deployment-M25.md`, and `docs/Validation-M25.md`. M25 closes the M22 `CISSP-D4-002` engineering gap while physical switch/VLAN enforcement and M26 SOC/DR integration remain environment/future-scope evidence.
## M26 relationship

M26 adds the enterprise operational-security evidence layer for centralized SOC telemetry/correlation, vulnerability-remediation operations, executable incident response, and immutable backup/restore/DR validation. This document retains its original milestone authority; M26 consumes its established controls/evidence without rewriting historical behavior. See `docs/M26-SOC-Vulnerability-Incident-Backup-DR.md`, `docs/Prerequisites-M26.md`, `docs/Deployment-M26.md`, and `docs/Validation-M26.md`.

## M27 relationship

M27 adds the Secure SDLC / DevSecOps / AppSec evidence layer on top of the immutable M0–M26 lineage. This document keeps its original milestone authority; M27 consumes its controls/evidence where relevant and does not retroactively rewrite the historical contract. M27 closes the `CISSP-D6-002` control-plane capability gap with default-deny security testing gates and independently verifiable Node1/Node2 evidence. Simulated local penetration-test evidence validates the workflow only and is not a production penetration-test claim.

## M28 relationship

M28 adds authority-bound evidence controls for organizational governance, personnel security/training, physical/environmental security, and business-continuity exercises. This document keeps its original milestone authority; M28 consumes its applicable evidence without rewriting historical M0–M27 claims. Real-world HR/facility/BCP controls require authorized production records—local Python validation proves the evidence contract, signatures, freshness and source binding only.

## M29 relationship

M29 aggregates the signed M21 platform prerequisite and M22–M28 enterprise-security evidence into one cross-domain Node1/Node2 validation package. This historical document remains authoritative for its original milestone; M29 consumes its evidence without rewriting its semantics. M29 distinguishes evidence-integrity success from production readiness and remains fail-closed while M21 platform controls or real M27/M28 production evidence are outstanding. See `docs/M29-Enterprise-Cross-Domain-Node1-Node2-Validation.md`, `docs/Prerequisites-M29.md`, `docs/Deployment-M29.md`, and `docs/Validation-M29.md`.
