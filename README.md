> Current development milestone: **M27 — Secure SDLC / DevSecOps / AppSec**. Latest immutable tagged parent: **M26 v0.26.0**.

# Portable Agentic AI Governance

Portable Agentic AI Governance is a deterministic security, governance, regulatory-evidence, and bounded-agent control plane for AI/ML, RAG, GenAI, and agentic systems.

The project is intentionally framework-neutral. An LLM or orchestration framework may propose, summarize, or reason, but it does not replace deterministic authorization, policy, signed evidence, replay protection, bounded execution, human approval, or release verification.

## Current development state

| Item | Value |
|---|---|
| Current development milestone | **M25 — Zero-Trust Network & Micro-segmentation** |
| Package version in working tree | `0.25.0` |
| Latest immutable tagged release | **M24 v0.24.0** |
| M23 tag | `m24-asset-security-data-lifecycle-v0.24.0` |
| M23 release commit | `7f56c13bdc33993998ca8750d0cab9510e3157aa` |
| M25 state | pre-commit / Node1+Node2 validation required before release tag |

M25 is intentionally validated from an uncommitted working tree first. Its signed source manifest binds content digests to the immutable M24 parent instead of pretending the uncommitted tree is already a release.

## What problem does this project solve?

AI governance often fails when policy documents are disconnected from executable controls and evidence. This repository turns governance and security requirements into deterministic, testable control paths with signed artifacts and explicit authority boundaries.

The implementation provides, across M0–M25:

- deterministic trust-kernel primitives;
- identity, RBAC/ABAC, mTLS, request signing, anti-replay, protected secrets, rate limiting, and signed audit;
- software/model supply-chain manifests and vulnerability policy;
- model governance, data provenance, retrieval authorization, embedding policy, AI evaluation, and threat modeling;
- risk, privacy, exception, third-party, and continuous-control evidence;
- bounded read-only, tool-using, approval-controlled, and supervised multi-agent workflows;
- security-operations, containment, recovery, and evidence preservation;
- CRA-oriented product-security, vulnerability, incident, reporting, PSIRT/CVD, update, Annex-I, Annex-VII, production-validation, and release-freeze evidence;
- embedded Linux/platform-security evidence for boot chains, TPM/PCRs, firmware signing/rollback, debug controls, least privilege, MAC capability, and CI/CD gates.

## Node1 and Node2

The repository uses a deliberate two-node trust model.

```mermaid
flowchart LR
    Operator[Developer / Operator]
    Policy[Policies, schemas, source]
    N1[Node1\nRelease + signing authority]
    Evidence[Signed evidence material]
    Public[Verifier-only package\nNo private signing key]
    N2[Node2\nIndependent verifier]
    Decision[PASS / FAIL + evidence gaps]

    Operator --> N1
    Policy --> N1
    N1 --> Evidence
    Evidence --> Public
    Public --> N2
    N2 --> Decision
```

**Node1** is the release/signing authority. It may generate signed milestone material and retain private signing material locally.

**Node2** is an independent verifier. It receives verifier-only material and must reject private signing keys. Node2 proves that release evidence can be validated without inheriting Node1 signing authority.

The terms describe trust roles, not a requirement that every deployment use these exact physical machines.

## What has been validated?

The repository contains deterministic local tests, milestone-specific verification, full regression paths, and cross-node verification.

For the validated M21 v0.21.1 LIVE evidence currently preserved with this source snapshot:

- validation mode: `LIVE`;
- required checks passed: **15**;
- open required checks: **2**;
- `production_ready=false`;
- `cra_conformity_claim=false`.

The two open platform-hardening gaps are intentionally visible:

1. `secure-boot-enabled` — Secure Boot is not enabled on the validated Node1/Node2 baseline.
2. `mac-enforcing` — Node2 does not currently have an enforcing MAC baseline; SELinux remains disabled after the attempted permissive configuration caused a boot failure on that validated Jetson baseline.

A successful verifier run is therefore **not** the same thing as claiming the platform is fully production-hardened.

## Reproduce the current release

The detailed operator procedure lives in [`instruction.md`](instruction.md). The shortest release-oriented path is:

```bash
git clone git@github.com:studioraga/portable-agentic-ai-governance.git
cd portable-agentic-ai-governance
git checkout m21-embedded-linux-platform-security-v0.21.1

export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q tests/platform_security
./scripts/m21/validate_m21_local.sh
./scripts/m21/ci_validate.sh
./scripts/m21/validate_m21_regression.sh
```

The local M21 validation uses deterministic fixture profiles. LIVE Node1/Node2 reproduction requires the platform-profile capture and signing/verifier workflow documented in [`docs/Deployment-M21.md`](docs/Deployment-M21.md) and [`docs/Validation-M21.md`](docs/Validation-M21.md).

## Documentation map

| Need | Start here |
|---|---|
| Understand the project | `README.md` |
| Execute developer/operator workflow | [`instruction.md`](instruction.md) |
| Understand durable architecture | [`docs/Architecture.md`](docs/Architecture.md) |
| Understand validation layers | [`docs/Validation.md`](docs/Validation.md) |
| Understand deployment progression | [`docs/oneshot-deployment.md`](docs/oneshot-deployment.md) |
| Check common prerequisites | [`docs/Prerequisites.md`](docs/Prerequisites.md) |
| See M0–M25 evolution | [`docs/Milestones.md`](docs/Milestones.md) |
| Understand current M21 design | [`docs/M21-Embedded-Linux-Platform-Security-Validation.md`](docs/M21-Embedded-Linux-Platform-Security-Validation.md) |
| Execute M21 validation | [`docs/Validation-M21.md`](docs/Validation-M21.md) |
| Execute M21 deployment | [`docs/Deployment-M21.md`](docs/Deployment-M21.md) |

A complete documentation index is in [`docs/README.md`](docs/README.md).

## Authority and safety boundaries

The project deliberately fails closed around authority:

- an LLM is not an authorization boundary;
- agents cannot accept risk or certify compliance;
- private release signing keys must not be transferred to verifier-only nodes;
- signed approvals are separate from request and evidence signing domains;
- destructive platform operations are outside M21 acceptance;
- M21 does not burn fuses, enroll UEFI keys, flash firmware, or install MAC policy;
- generated CRA-oriented evidence is not a CRA conformity assessment or conformity claim.

## Repository layout

```text
portable-agentic-ai-governance/
├── src/            # deterministic runtime/control implementations
├── governance/     # control, CRA, and platform policy material
├── schemas/        # machine-readable contracts
├── agents/         # signed/static agent definitions
├── scripts/        # validation, build, verification, and evidence workflows
├── deploy/         # milestone-scoped deployment helpers
├── tests/          # positive/negative and regression tests
├── examples/       # bounded examples and reference policy material
├── docs/           # architecture, validation, deployment, milestone documentation
├── README.md       # human orientation
└── instruction.md  # authoritative developer/operator workflow
```

## Release philosophy

A milestone is not complete because a document says it is complete. Release evidence must be executable, reproducible, fail closed where required, and preserve the Node1/Node2 authority boundary.


## M22 enterprise-security extension

M22 extends the frozen M21.1 baseline with the authoritative CISSP-domain / enterprise-security control foundation. See `docs/M22-CISSP-Enterprise-Security-Control-Foundation.md`, `docs/Prerequisites-M22.md`, `docs/Deployment-M22.md`, and `docs/Validation-M22.md`. M0–M21 historical behavior remains unchanged; M22 records alignment and gaps and does not assert CISSP, ISO/IEC 27001, ISO/IEC 42001, or CRA certification/conformity.

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
