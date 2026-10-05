# Deployment — M23 Enterprise Identity, MFA & PAM

## Pre-commit validation model

Apply M23 with `git apply` when validation must occur before committing. Use `git am` only when you want patch application to create the M23 commit.

## Node1

```bash
./deploy/m23/one_shot_node1.sh
```

This creates `var/m23-material/`, verifies it, deploys Node1 authority material under `~/.config/portable-ai-governance/m23`, and checks that a verifier package can be produced without private keys.

Package verifier material:

```bash
./deploy/m23/package_verifier_material.sh \
  var/m23-material \
  var/m23-verifier.tar.gz
```

Transfer only `var/m23-verifier.tar.gz` and its `.sha256` file to Node2.

## Node2

Synchronize the same uncommitted M23 source tree first, then extract the verifier archive and run:

```bash
./deploy/m23/one_shot_node2.sh /path/to/m23-material
```

or directly:

```bash
./scripts/m23/verify_node2.sh /path/to/m23-material
```

Node2 rejects any file matching `*private*.pem`.

## Production IdP integration boundary

The offline M23 validation keys prove the verifier semantics only. They are not production identity keys. In production, configure the enterprise OIDC issuer/audience and use trusted IdP signing keys/JWKS. Never copy a production IdP signing private key into this repository or Node2 verifier material.


## Production OIDC runtime variables

```bash
export PAG_IDENTITY_PROVIDER=oidc
export PAG_OIDC_ISSUER='https://id.example/realms/enterprise'
export PAG_OIDC_AUDIENCE='portable-ai-governance'
export PAG_OIDC_PUBLIC_KEY='/protected/path/idp-signing-public.pem'
export PAG_OIDC_REQUIRED_ACR='urn:studioraga:aal2'
```

These variables configure verification trust only. Never place the IdP signing private key in PAG or Node2 material.

## M24 relationship

M24 extends the frozen M23 baseline with deterministic asset inventory/ownership/classification, retention and legal-hold handling, evidence-backed sanitization, default-deny DLP/controlled export, and cryptographic key-lifecycle evidence. This historical document remains authoritative for its original milestone; M24 consumes its reusable evidence but does not rewrite M0-M23 semantics. See `docs/M24-Asset-Security-Data-Protection-Crypto-Lifecycle.md`, `docs/Prerequisites-M24.md`, `docs/Deployment-M24.md`, and `docs/Validation-M24.md`. M24 closes only `CISSP-D2-001..003`; M21-dependent Domain-3 platform/hardware-root gaps remain open.

## M25 relationship

M25 extends the frozen M24 baseline with explicit network zones, default-deny micro-segmentation, mTLS workload-identity binding, egress allowlisting, network-detection policy and deterministic firewall evidence. This historical document remains authoritative for its original milestone; M25 consumes reusable evidence without rewriting M0-M24 semantics. See `docs/M25-Zero-Trust-Network-Microsegmentation.md`, `docs/Prerequisites-M25.md`, `docs/Deployment-M25.md`, and `docs/Validation-M25.md`. M25 closes the M22 `CISSP-D4-002` engineering gap while physical switch/VLAN enforcement and M26 SOC/DR integration remain environment/future-scope evidence.
## M26 relationship

M26 adds the enterprise operational-security evidence layer for centralized SOC telemetry/correlation, vulnerability-remediation operations, executable incident response, and immutable backup/restore/DR validation. This document retains its original milestone authority; M26 consumes its established controls/evidence without rewriting historical behavior. See `docs/M26-SOC-Vulnerability-Incident-Backup-DR.md`, `docs/Prerequisites-M26.md`, `docs/Deployment-M26.md`, and `docs/Validation-M26.md`.

## M27 relationship

M27 adds the Secure SDLC / DevSecOps / AppSec evidence layer on top of the immutable M0–M26 lineage. This document keeps its original milestone authority; M27 consumes its controls/evidence where relevant and does not retroactively rewrite the historical contract. M27 closes the `CISSP-D6-002` control-plane capability gap with default-deny security testing gates and independently verifiable Node1/Node2 evidence. Simulated local penetration-test evidence validates the workflow only and is not a production penetration-test claim.
