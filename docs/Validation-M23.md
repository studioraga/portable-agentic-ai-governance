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
