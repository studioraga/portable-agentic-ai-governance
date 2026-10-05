# Prerequisites — M25 Zero-Trust Network & Micro-segmentation

## Required baseline

The repository must start from the immutable M24 release:

```text
commit: 62a1713ff468117cefc256c03d2a71f26928f8cc
tag:    m24-asset-security-data-lifecycle-v0.24.0
```

Check on both Node1 and Node2:

```bash
git status
git rev-parse HEAD
git describe --tags --exact-match
```

The working tree should be clean before applying the M25 patch.

## Software

Both nodes require Python 3, Git, OpenSSL and the repository development dependencies. For a first-time setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
```

`nft` is optional for syntax review; M25 validation itself does not modify the firewall.

## Network information to collect before production application

Document the actual Node1/Node2 management IPs, verifier path, monitoring destinations, switch/VLAN ownership, permitted external update endpoints, and any routes that must remain available for recovery. The example `10.25.x.0/24` CIDRs in M25 are policy-reference zones, not an instruction to renumber the user's current lab.

## Safety

Do not apply generated firewall rules over an SSH-only management path without an out-of-band recovery method. First validate M25 in evidence-only mode, compare generated rules with actual interfaces/routes, then apply production changes under an approved change procedure.
## M26 relationship

M26 adds the enterprise operational-security evidence layer for centralized SOC telemetry/correlation, vulnerability-remediation operations, executable incident response, and immutable backup/restore/DR validation. This document retains its original milestone authority; M26 consumes its established controls/evidence without rewriting historical behavior. See `docs/M26-SOC-Vulnerability-Incident-Backup-DR.md`, `docs/Prerequisites-M26.md`, `docs/Deployment-M26.md`, and `docs/Validation-M26.md`.

## M27 relationship

M27 adds the Secure SDLC / DevSecOps / AppSec evidence layer on top of the immutable M0–M26 lineage. This document keeps its original milestone authority; M27 consumes its controls/evidence where relevant and does not retroactively rewrite the historical contract. M27 closes the `CISSP-D6-002` control-plane capability gap with default-deny security testing gates and independently verifiable Node1/Node2 evidence. Simulated local penetration-test evidence validates the workflow only and is not a production penetration-test claim.

## M28 relationship

M28 adds authority-bound evidence controls for organizational governance, personnel security/training, physical/environmental security, and business-continuity exercises. This document keeps its original milestone authority; M28 consumes its applicable evidence without rewriting historical M0–M27 claims. Real-world HR/facility/BCP controls require authorized production records—local Python validation proves the evidence contract, signatures, freshness and source binding only.

## M29 relationship

M29 aggregates the signed M21 platform prerequisite and M22–M28 enterprise-security evidence into one cross-domain Node1/Node2 validation package. This historical document remains authoritative for its original milestone; M29 consumes its evidence without rewriting its semantics. M29 distinguishes evidence-integrity success from production readiness and remains fail-closed while M21 platform controls or real M27/M28 production evidence are outstanding. See `docs/M29-Enterprise-Cross-Domain-Node1-Node2-Validation.md`, `docs/Prerequisites-M29.md`, `docs/Deployment-M29.md`, and `docs/Validation-M29.md`.
