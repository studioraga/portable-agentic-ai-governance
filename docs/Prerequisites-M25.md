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
