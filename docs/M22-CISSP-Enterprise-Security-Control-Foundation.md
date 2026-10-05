# M22 — CISSP / Enterprise Security Control Foundation

## Objective

M22 extends Portable Agentic AI Governance from the frozen M21.1 platform-security baseline into an enterprise security evidence and control-plane foundation. It does **not** claim that an organization, product, or repository is “CISSP certified” or “CISSP compliant.” CISSP is a professional certification knowledge framework. M22 uses its eight domains as an enterprise-security coverage taxonomy and maps that taxonomy to NIST CSF 2.0, ISO/IEC 27001:2022 themes, the existing CRA program, and ISO/IEC 42001:2023 themes.

## Immutable parent baseline

- parent commit: `ea952069938a6435ccb298f5424bab158197ce05`
- released M21 tag: `m21-embedded-linux-platform-security-v0.21.1`
- M0–M21 behavior and evidence contracts remain historical and immutable.

## Security invariant

`Reasoning != Authority`

M22 preserves deterministic authorization, evidence-before-claim, fail-closed validation, and independent Node2 verification.

## Authoritative M22 artifacts

- `governance/enterprise/m22/cissp-domain-catalog.json`
- `governance/enterprise/m22/enterprise-security-requirements.json`
- `governance/enterprise/m22/enterprise-control-mapping.json`
- `governance/enterprise/m22/gap-register.json`
- `governance/enterprise/m22/evidence-policy.json`

M22 contains 23 enterprise-security alignment requirements spanning all eight CISSP domains. `EVIDENCED` means the current repository has a deterministic control/evidence basis; `PARTIAL` means material capability exists but the enterprise requirement is not complete; `GAP` means a later milestone must implement the missing control.

## Framework boundaries

M22 records high-level references only and does not reproduce proprietary ISO standard text. The ISO references are alignment aids and are not certification decisions.

Authoritative public references:

- ISC2 CISSP Exam Outline: https://www.isc2.org/certifications/cissp/cissp-certification-exam-outline
- NIST CSF 2.0: https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20
- ISO/IEC 27001:2022 overview: https://www.iso.org/standard/27001
- ISO/IEC 42001:2023 overview: https://www.iso.org/standard/81230.html
- CRA authoritative source already recorded in `governance/cra/cra-requirements.json`.

## Claim boundaries

The following are always false in M22 material:

- `cissp_certification_claim`
- `iso_iec_27001_certification_claim`
- `iso_iec_42001_certification_claim`
- `cra_conformity_claim`

M22 is an evidence/control-foundation milestone, not a conformity-assessment authority.

## Node roles

### Node1

Node1 is the M22 evidence producer and signing authority. It may hold the ephemeral/private M22 signing key and creates the signed control-foundation material.

### Node2

Node2 is verifier-only. It must receive only the public key and verifier material. Any private signing key in the Node2 package is a hard failure.

## Source binding before commit

M22 supports validation while `.git` still contains uncommitted M22 changes. `m22-source-manifest.json` hashes the M22 source/governance files and separately binds the work to the immutable M21.1 parent commit. This avoids claiming that an uncommitted tree is a release while still making Node1/Node2 verification deterministic.

After validation, commit the exact validated tree, rebuild M22 material, rerun verification, and tag the release.

## Planned closure milestones

- M23 — enterprise identity, MFA and PAM
- M24 — asset/data protection, lifecycle and DLP
- M25 — zero-trust network and segmentation
- M26 — SOC, vulnerability, IR, immutable backup and DR
- M27 — secure SDLC / DevSecOps / application security
- M28 — personnel, physical, BCP and organizational controls
- M29 — enterprise Node1/Node2 cross-domain validation
- M30 — enterprise-security production freeze

## M23 relationship

M23 extends the frozen M22 enterprise-security foundation with enterprise human identity, OIDC federation evidence, strong MFA context, phishing-resistant privileged authentication, expiring entitlement review, signed single-use JIT privilege grants, dual-approved break-glass access, segregation of duties, and independent Node1/Node2 verification. The authoritative M23 documents are `docs/M23-Enterprise-Identity-MFA-PAM.md`, `docs/Prerequisites-M23.md`, `docs/Deployment-M23.md`, and `docs/Validation-M23.md`. Historical M0-M22 behavior and evidence remain immutable.

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
