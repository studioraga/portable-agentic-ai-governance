# Prerequisites — M24

This procedure assumes a developer is running M24 for the first time.

## 1. Required baseline

Both Node1 and Node2 must start from the same clean M23 release:

```text
commit: 7f56c13bdc33993998ca8750d0cab9510e3157aa
tag:    m23-enterprise-identity-mfa-pam-v0.23.0
```

Verify:

```bash
git status --short --branch
git rev-parse HEAD
git describe --tags --exact-match
```

Do not continue if the baseline differs.

## 2. Host tools

Required on both nodes:

```bash
python3 --version
git --version
openssl version
tar --version
sha256sum --version | head -1
```

Python 3.10+ is required; CI uses Python 3.12.

## 3. Python environment

From repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
```

## 4. Node roles

**Node1** is the M24 material producer/signing authority for validation. It may hold the generated `signing-private.pem` under ignored runtime material.

**Node2** is verifier-only. It must never receive `signing-private.pem` or any other private-key material.

## 5. Source synchronization

Before cross-node verification, both nodes must contain the exact same M24 source content because Node2 validates `m24-source-manifest.json` digests.

For pre-commit validation apply the M24 patch with `git apply`, not `git am`.

## 6. Safety boundaries

M24 validation does not delete user data, rotate real production keys, change disk encryption, or modify physical media. Sanitization and export flows use deterministic validation records. Production data-disposal operations require separate operator-approved procedures.

## M25 relationship

M25 extends the frozen M24 baseline with explicit network zones, default-deny micro-segmentation, mTLS workload-identity binding, egress allowlisting, network-detection policy and deterministic firewall evidence. This historical document remains authoritative for its original milestone; M25 consumes reusable evidence without rewriting M0-M24 semantics. See `docs/M25-Zero-Trust-Network-Microsegmentation.md`, `docs/Prerequisites-M25.md`, `docs/Deployment-M25.md`, and `docs/Validation-M25.md`. M25 closes the M22 `CISSP-D4-002` engineering gap while physical switch/VLAN enforcement and M26 SOC/DR integration remain environment/future-scope evidence.
## M26 relationship

M26 adds the enterprise operational-security evidence layer for centralized SOC telemetry/correlation, vulnerability-remediation operations, executable incident response, and immutable backup/restore/DR validation. This document retains its original milestone authority; M26 consumes its established controls/evidence without rewriting historical behavior. See `docs/M26-SOC-Vulnerability-Incident-Backup-DR.md`, `docs/Prerequisites-M26.md`, `docs/Deployment-M26.md`, and `docs/Validation-M26.md`.

## M27 relationship

M27 adds the Secure SDLC / DevSecOps / AppSec evidence layer on top of the immutable M0–M26 lineage. This document keeps its original milestone authority; M27 consumes its controls/evidence where relevant and does not retroactively rewrite the historical contract. M27 closes the `CISSP-D6-002` control-plane capability gap with default-deny security testing gates and independently verifiable Node1/Node2 evidence. Simulated local penetration-test evidence validates the workflow only and is not a production penetration-test claim.
