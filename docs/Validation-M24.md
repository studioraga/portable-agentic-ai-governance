# Validation — M24

## Validation objectives

M24 must prove positive functionality and fail-closed behavior for asset registration, retention/legal hold, sanitization, DLP/export decisions, cryptographic lifecycle, signed evidence and Node1/Node2 separation.

## Local validation

```bash
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m pytest -q tests/asset_security
./scripts/m24/validate_m24_local.sh
```

## Required negative tests

The unit suite must reject at least:

1. unregistered assets;
2. disposal while legal hold is active;
3. restricted sanitization without approval;
4. export to an unapproved destination;
5. unencrypted sensitive export;
6. self-approved sensitive export;
7. export containing configured sensitive-data patterns;
8. overdue active cryptographic keys.

## Node1 validation

```bash
./deploy/m24/one_shot_node1.sh
./scripts/m24/verify_node1.sh var/m24-material
```

Expected result:

```text
PASS: Node1 M24 authority and verifier-package isolation verified
```

## Node2 validation

```bash
./deploy/m24/one_shot_node2.sh /path/to/m24-verifier.tar.gz
```

or after manual extraction:

```bash
./scripts/m24/verify_node2.sh /tmp/m24-node1/m24-material
```

Expected result:

```text
PASS: Node2 M24 verifier-only asset/data evidence verified
```

## Manual tamper rejection test

```bash
cp -a /tmp/m24-node1/m24-material /tmp/m24-tampered
printf '\n' >> /tmp/m24-tampered/m24-gap-closure.json
python3 scripts/m24/validate_m24_node.py --material /tmp/m24-tampered --repo-root "$PWD"
```

The command must exit non-zero.

## Runtime/private material hygiene

```bash
git check-ignore var/m24-material/probe
```

and:

```bash
if tar -tzf var/m24-verifier.tar.gz | grep -Eqi 'private.*pem'; then
  exit 1
fi
```

## Regression gate before commit

```bash
./scripts/m24/validate_m24_regression.sh
git diff --check
git status
```

For a final physical release qualification, also run the complete repository test suite on Node1 without sandbox time limits:

```bash
python3 -m pytest -q
```

## M25 relationship

M25 extends the frozen M24 baseline with explicit network zones, default-deny micro-segmentation, mTLS workload-identity binding, egress allowlisting, network-detection policy and deterministic firewall evidence. This historical document remains authoritative for its original milestone; M25 consumes reusable evidence without rewriting M0-M24 semantics. See `docs/M25-Zero-Trust-Network-Microsegmentation.md`, `docs/Prerequisites-M25.md`, `docs/Deployment-M25.md`, and `docs/Validation-M25.md`. M25 closes the M22 `CISSP-D4-002` engineering gap while physical switch/VLAN enforcement and M26 SOC/DR integration remain environment/future-scope evidence.
## M26 relationship

M26 adds the enterprise operational-security evidence layer for centralized SOC telemetry/correlation, vulnerability-remediation operations, executable incident response, and immutable backup/restore/DR validation. This document retains its original milestone authority; M26 consumes its established controls/evidence without rewriting historical behavior. See `docs/M26-SOC-Vulnerability-Incident-Backup-DR.md`, `docs/Prerequisites-M26.md`, `docs/Deployment-M26.md`, and `docs/Validation-M26.md`.

## M27 relationship

M27 adds the Secure SDLC / DevSecOps / AppSec evidence layer on top of the immutable M0–M26 lineage. This document keeps its original milestone authority; M27 consumes its controls/evidence where relevant and does not retroactively rewrite the historical contract. M27 closes the `CISSP-D6-002` control-plane capability gap with default-deny security testing gates and independently verifiable Node1/Node2 evidence. Simulated local penetration-test evidence validates the workflow only and is not a production penetration-test claim.

## M28 relationship

M28 adds authority-bound evidence controls for organizational governance, personnel security/training, physical/environmental security, and business-continuity exercises. This document keeps its original milestone authority; M28 consumes its applicable evidence without rewriting historical M0–M27 claims. Real-world HR/facility/BCP controls require authorized production records—local Python validation proves the evidence contract, signatures, freshness and source binding only.

## M29 relationship

M29 aggregates the signed M21 platform prerequisite and M22–M28 enterprise-security evidence into one cross-domain Node1/Node2 validation package. This historical document remains authoritative for its original milestone; M29 consumes its evidence without rewriting its semantics. M29 distinguishes evidence-integrity success from production readiness and remains fail-closed while M21 platform controls or real M27/M28 production evidence are outstanding. See `docs/M29-Enterprise-Cross-Domain-Node1-Node2-Validation.md`, `docs/Prerequisites-M29.md`, `docs/Deployment-M29.md`, and `docs/Validation-M29.md`.
