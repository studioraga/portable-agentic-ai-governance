# Prerequisites — M23 Enterprise Identity, MFA & PAM

## Repository baseline

Start from the clean M22 release:

```bash
git rev-parse HEAD
# f020822162591f7d279f7004dea628efb7989525

git describe --tags --exact-match
# m22-enterprise-security-foundation-v0.22.0
```

M23 may be validated while uncommitted because `m23-source-manifest.json` binds the M23 source content by SHA-256 while separately preserving the immutable M22 Git parent.

## Software

Required on both nodes:

- Python 3.10+
- OpenSSL with Ed25519 support
- Git
- tar, sha256sum
- pytest for source validation

No external IdP is required for the deterministic offline validation profile. Production deployment of the federation contract requires a real enterprise OIDC IdP and its trusted signing keys/JWKS.

## Security prerequisites

- Node1 may hold validation-only M23 private keys.
- Node2 must receive only public/verifier material.
- Production privileged access must require phishing-resistant MFA evidence.
- Self-approved JIT elevation is forbidden.
- Break-glass requires two independent approvers and post-review.

## Environment

```bash
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
```


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
