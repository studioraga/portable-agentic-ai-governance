# Validation — M23 Enterprise Identity, MFA & PAM

## Local validation

```bash
./scripts/m23/validate_m23_local.sh
```

It runs M23 unit/negative tests, builds signed material, validates it with private keys present, deletes all validation private keys, and validates the verifier-only material again.

## Regression

```bash
./scripts/m23/validate_m23_regression.sh
```

This runs the full repository test suite, M22 validation, and M23 validation.

## Required positive tests

- valid federated assertion accepted;
- WebAuthn/FIDO2 authentication context accepted for privileged access;
- scoped JIT grant accepted;
- dual-approved break-glass grant accepted;
- post-review flag present on emergency grant.

## Required negative tests

- OTP-only privileged assertion rejected;
- wrong issuer rejected;
- wrong audience rejected;
- expired assertion rejected;
- self-approved JIT rejected;
- JIT replay rejected;
- resource outside JIT scope rejected;
- break-glass without second independent approver rejected;
- Node2 private-key material rejected;
- tampered signed manifest rejected.

## Node1

```bash
./scripts/m23/verify_node1.sh var/m23-material
```

Expected final line:

```text
PASS: Node1 M23 identity/PAM authority and verifier-package isolation verified
```

## Node2

```bash
./scripts/m23/verify_node2.sh /path/to/m23-material
```

Expected final line:

```text
PASS: Node2 M23 verifier-only identity/MFA/PAM evidence verified
```

## Release gate

Do not commit/tag M23 unless:

1. full regression passes;
2. Node1 verification passes;
3. Node2 verification passes;
4. verifier archive contains no private key;
5. `git diff --check` passes;
6. claim boundaries remain false.

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
