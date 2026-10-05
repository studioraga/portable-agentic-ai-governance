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
