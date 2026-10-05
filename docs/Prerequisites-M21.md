# M21 Prerequisites

M21 uses the common repository prerequisites plus platform-observation tools appropriate to each node.

## Required repository/runtime baseline

Both nodes require:

- the same selected M21 source release;
- Python 3.10+;
- Git;
- OpenSSL/runtime crypto dependencies used by the project;
- standard Linux user/file utilities;
- systemd userspace for the reference service contract.

For v0.21.1, both nodes should resolve the release to:

```text
m21-embedded-linux-platform-security-v0.21.1
e83ebf03c6d1ce2f4076ab8e3dae8282e4aeb880
```

## Useful LIVE observation tools

M21 can make use of:

- `mokutil`;
- `fwupdmgr`;
- `systemd-analyze`;
- `aa-status` / `apparmor_parser`;
- `getenforce` where SELinux userspace is present;
- `capsh`;
- `setpriv`;
- `tpm2-tools`.

Absence of an optional observation tool is recorded as capability state; it must not silently become evidence that the control is enabled.

## Node2 Jetson

Jetson evidence may additionally use NVIDIA platform information and read-only fuse-inspection tooling when already installed and operator-authorized.

M21 does not invoke fuse-programming, firmware-flashing, or irreversible Secure Boot provisioning commands.

## Authority prerequisite

Node1 may contain M21 private signing material during evidence generation. Node2 must not.


### M22 relationship

This document remains authoritative for its historical milestone scope. M22 does not rewrite that milestone; it inventories and maps its reusable controls/evidence into the enterprise-security foundation and records remaining gaps in `governance/enterprise/m22/gap-register.json`. See `docs/M22-CISSP-Enterprise-Security-Control-Foundation.md`.

## M23 relationship

This historical milestone document remains authoritative for its original scope. M23 does not rewrite it; M23 consumes the existing identity/authorization/evidence lineage and adds enterprise federation, strong/phishing-resistant MFA policy, entitlement review, PAM/JIT, break-glass, segregation-of-duties, and Node1/Node2 verifier evidence. See `docs/M23-Enterprise-Identity-MFA-PAM.md`.

## M24 relationship

M24 extends the frozen M23 baseline with deterministic asset inventory/ownership/classification, retention and legal-hold handling, evidence-backed sanitization, default-deny DLP/controlled export, and cryptographic key-lifecycle evidence. This historical document remains authoritative for its original milestone; M24 consumes its reusable evidence but does not rewrite M0-M23 semantics. See `docs/M24-Asset-Security-Data-Protection-Crypto-Lifecycle.md`, `docs/Prerequisites-M24.md`, `docs/Deployment-M24.md`, and `docs/Validation-M24.md`. M24 closes only `CISSP-D2-001..003`; M21-dependent Domain-3 platform/hardware-root gaps remain open.
