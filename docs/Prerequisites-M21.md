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

## M25 relationship

M25 extends the frozen M24 baseline with explicit network zones, default-deny micro-segmentation, mTLS workload-identity binding, egress allowlisting, network-detection policy and deterministic firewall evidence. This historical document remains authoritative for its original milestone; M25 consumes reusable evidence without rewriting M0-M24 semantics. See `docs/M25-Zero-Trust-Network-Microsegmentation.md`, `docs/Prerequisites-M25.md`, `docs/Deployment-M25.md`, and `docs/Validation-M25.md`. M25 closes the M22 `CISSP-D4-002` engineering gap while physical switch/VLAN enforcement and M26 SOC/DR integration remain environment/future-scope evidence.
## M26 relationship

M26 adds the enterprise operational-security evidence layer for centralized SOC telemetry/correlation, vulnerability-remediation operations, executable incident response, and immutable backup/restore/DR validation. This document retains its original milestone authority; M26 consumes its established controls/evidence without rewriting historical behavior. See `docs/M26-SOC-Vulnerability-Incident-Backup-DR.md`, `docs/Prerequisites-M26.md`, `docs/Deployment-M26.md`, and `docs/Validation-M26.md`.

## M27 relationship

M27 adds the Secure SDLC / DevSecOps / AppSec evidence layer on top of the immutable M0–M26 lineage. This document keeps its original milestone authority; M27 consumes its controls/evidence where relevant and does not retroactively rewrite the historical contract. M27 closes the `CISSP-D6-002` control-plane capability gap with default-deny security testing gates and independently verifiable Node1/Node2 evidence. Simulated local penetration-test evidence validates the workflow only and is not a production penetration-test claim.
