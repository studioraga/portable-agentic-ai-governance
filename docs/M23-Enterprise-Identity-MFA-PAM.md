# M23 — Enterprise Identity, MFA & PAM

## Purpose

M23 closes the three CISSP Domain 5 gaps cataloged by the immutable M22 enterprise-security baseline without rewriting M22. It adds deterministic enterprise-identity evidence, MFA policy enforcement, entitlement review, privileged-access management (PAM), just-in-time (JIT) elevation, break-glass controls, segregation of duties, signed evidence, and independent Node2 verification.

M23 does **not** claim CISSP, ISO/IEC 27001, ISO/IEC 42001, or CRA certification/conformity.

## Immutable parent

- Commit: `f020822162591f7d279f7004dea628efb7989525`
- Tag: `m22-enterprise-security-foundation-v0.22.0`

Historical M0–M22 artifacts remain unchanged.

## Control objectives

| Control | Objective |
|---|---|
| ENT-IAM-001 | Federated enterprise identity contract |
| ENT-IAM-002 | Strong MFA context for human access |
| ENT-IAM-003 | Phishing-resistant MFA for privileged access |
| ENT-IAM-004 | Owner-approved, scoped, expiring entitlements |
| ENT-IAM-005 | Periodic entitlement review evidence |
| ENT-PAM-001 | Signed bounded JIT privilege grants |
| ENT-PAM-002 | TTL + single-use replay rejection |
| ENT-PAM-003 | Independent approval + session evidence binding |
| ENT-PAM-004 | Dual-approval short-lived break-glass + post-review |
| ENT-SOD-001 | No self-approval / segregation of duties |

## Federation model

M23 defines an OIDC claims contract. The offline validation profile uses Ed25519-signed compact tokens so Node1 and Node2 can verify issuer, audience, subject, expiry, issued-at time, authentication time, `amr`, `acr`, roles, groups, and attributes without a cloud dependency.

The generated federation private key is **validation-only**. Production deployments SHALL use an enterprise IdP and trust only its configured signing keys/JWKS. M23 does not ship a production IdP private key.

## MFA model

Human access requires MFA context. Privileged access additionally requires phishing-resistant evidence. The reference policy recognizes WebAuthn/FIDO2/PIV/smartcard/hardware-key methods as phishing-resistant. OTP-only assertions are intentionally rejected for privileged access.

## PAM/JIT model

A JIT grant is:

- signed;
- bound to one subject;
- bound to one action;
- resource-prefix scoped;
- time limited;
- independently approved;
- single use.

Replay is denied through a consumed-grant ledger.

## Break-glass model

Break-glass elevation requires:

- emergency flag;
- meaningful reason;
- two independent approvers distinct from the subject;
- maximum 900-second TTL;
- single-use grant;
- mandatory post-review evidence flag.

## M22 gap closure

M23 records closure in `governance/enterprise/m23/m23-gap-closure.json` rather than modifying `governance/enterprise/m22/gap-register.json`.

- `CISSP-D5-001`: PARTIAL -> EVIDENCED
- `CISSP-D5-002`: GAP -> EVIDENCED
- `CISSP-D5-003`: GAP -> EVIDENCED

## Node roles

### Node1

Node1 is the evidence producer and validation authority. It generates validation-only federation/PAM/signing keys, signed positive vectors, the M23 source manifest, and the signed M23 identity manifest.

### Node2

Node2 receives verifier-only material: public keys, signed manifests, policy/mapping/gap-closure material and signed positive vectors. It must never receive M23 private keys.

## Claim boundaries

Every M23 manifest keeps the following false:

- `cissp_certification_claim`
- `iso_iec_27001_certification_claim`
- `iso_iec_42001_certification_claim`
- `cra_conformity_claim`

## Next milestone

M24 addresses asset security, data protection, DLP and data lifecycle controls. M23 must not be expanded to close M24 gaps.

## M24 relationship

M24 extends the frozen M23 baseline with deterministic asset inventory/ownership/classification, retention and legal-hold handling, evidence-backed sanitization, default-deny DLP/controlled export, and cryptographic key-lifecycle evidence. This historical document remains authoritative for its original milestone; M24 consumes its reusable evidence but does not rewrite M0-M23 semantics. See `docs/M24-Asset-Security-Data-Protection-Crypto-Lifecycle.md`, `docs/Prerequisites-M24.md`, `docs/Deployment-M24.md`, and `docs/Validation-M24.md`. M24 closes only `CISSP-D2-001..003`; M21-dependent Domain-3 platform/hardware-root gaps remain open.

## M25 relationship

M25 extends the frozen M24 baseline with explicit network zones, default-deny micro-segmentation, mTLS workload-identity binding, egress allowlisting, network-detection policy and deterministic firewall evidence. This historical document remains authoritative for its original milestone; M25 consumes reusable evidence without rewriting M0-M24 semantics. See `docs/M25-Zero-Trust-Network-Microsegmentation.md`, `docs/Prerequisites-M25.md`, `docs/Deployment-M25.md`, and `docs/Validation-M25.md`. M25 closes the M22 `CISSP-D4-002` engineering gap while physical switch/VLAN enforcement and M26 SOC/DR integration remain environment/future-scope evidence.
## M26 relationship

M26 adds the enterprise operational-security evidence layer for centralized SOC telemetry/correlation, vulnerability-remediation operations, executable incident response, and immutable backup/restore/DR validation. This document retains its original milestone authority; M26 consumes its established controls/evidence without rewriting historical behavior. See `docs/M26-SOC-Vulnerability-Incident-Backup-DR.md`, `docs/Prerequisites-M26.md`, `docs/Deployment-M26.md`, and `docs/Validation-M26.md`.

## M27 relationship

M27 adds the Secure SDLC / DevSecOps / AppSec evidence layer on top of the immutable M0–M26 lineage. This document keeps its original milestone authority; M27 consumes its controls/evidence where relevant and does not retroactively rewrite the historical contract. M27 closes the `CISSP-D6-002` control-plane capability gap with default-deny security testing gates and independently verifiable Node1/Node2 evidence. Simulated local penetration-test evidence validates the workflow only and is not a production penetration-test claim.
