# M19 — CRA Node1/Node2 Production Validation

M19 converts the repository's prior CRA evidence into a signed, heterogeneous-node production-validation record. Node1 is the validation/signing authority; Node2 is the independent verifier target. Local fixture acceptance is explicitly `SIMULATED` and cannot set `production_validation_complete=true`.

## CRA scope

The primary M11 row is `CRA-REQ-060` / Annex I Part II(3): effective and regular product-security tests and reviews. M19 also reports closure candidates for the M17 evidence gaps, but does not mutate M11 or M17. Product-specific secure-default/reset, other-device/network availability impact, and secure data-removal/transfer remain explicit gaps unless separately demonstrated.

## Live workflow

1. Apply the uncommitted M19 source to both nodes from the same M18 base.
2. Node2 captures and transfers an unsigned live runtime profile to Node1.
3. Node1 captures its own live profile, checks platform/source/version parity and signs the M19 validation bundle.
4. Node1 transfers only verifier material to Node2.
5. Node2 recollects its current live profile and independently verifies the signed bundle.

## Boundaries

M19 performs no destructive test, firmware flash, host update, external network side effect, conformity assessment, or CRA conformity claim.

## M20 integration

M20 consumes the frozen evidence and controls from this milestone as part of the enterprise one-shot deployment/final-production-freeze chain. It does not rewrite this milestone or imply CRA conformity. Final-freeze readiness requires successful M19 live production validation. The M20 secure-agentic Node1/Node2 demonstration reuses the M10 constrained-authority topology and signed human-disposition model for traceable GenAI/agentic governance.
## M21 integration — Embedded Linux & Platform Security

M21 extends the frozen M0–M20 governance/CRA baseline into demonstrable platform security for BIOS/UEFI, Jetson/embedded boot firmware, BMC/device firmware inventory, firmware signing and anti-rollback, debug restrictions, Linux least privilege and systemd isolation, AppArmor/SELinux capability evidence, TPM/DICE roots of trust, platform threat modeling and CI/CD gates. It is non-destructive: live acceptance observes platform state and uses synthetic firmware for signing/rollback demonstrations; it never burns fuses, enrolls UEFI keys or flashes firmware. See `docs/M21-Embedded-Linux-Platform-Security-Validation.md`.

## Documentation role

This file is a milestone-specific historical/feature record. For the current repository workflow, use [`../README.md`](../README.md), [`../instruction.md`](../instruction.md), [`Architecture.md`](Architecture.md), [`Validation.md`](Validation.md), and [`Milestones.md`](Milestones.md).


### M22 relationship

This document remains authoritative for its historical milestone scope. M22 does not rewrite that milestone; it inventories and maps its reusable controls/evidence into the enterprise-security foundation and records remaining gaps in `governance/enterprise/m22/gap-register.json`. See `docs/M22-CISSP-Enterprise-Security-Control-Foundation.md`.

## M23 relationship

This historical milestone document remains authoritative for its original scope. M23 does not rewrite it; M23 consumes the existing identity/authorization/evidence lineage and adds enterprise federation, strong/phishing-resistant MFA policy, entitlement review, PAM/JIT, break-glass, segregation-of-duties, and Node1/Node2 verifier evidence. See `docs/M23-Enterprise-Identity-MFA-PAM.md`.

## M24 relationship

M24 extends the frozen M23 baseline with deterministic asset inventory/ownership/classification, retention and legal-hold handling, evidence-backed sanitization, default-deny DLP/controlled export, and cryptographic key-lifecycle evidence. This historical document remains authoritative for its original milestone; M24 consumes its reusable evidence but does not rewrite M0-M23 semantics. See `docs/M24-Asset-Security-Data-Protection-Crypto-Lifecycle.md`, `docs/Prerequisites-M24.md`, `docs/Deployment-M24.md`, and `docs/Validation-M24.md`. M24 closes only `CISSP-D2-001..003`; M21-dependent Domain-3 platform/hardware-root gaps remain open.

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
