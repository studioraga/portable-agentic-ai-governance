# Validation — M26

Run on Node1:

```bash
python3 -m pytest -q tests/operational_security
python3 -m pytest -q tests/acceptance/test_framework_mapping.py
./scripts/m26/validate_m26_local.sh
./deploy/m26/one_shot_node1.sh
./scripts/m26/verify_node1.sh var/m26-material
```

On Node2, verify the checksum, extract the verifier archive and run `./scripts/m26/verify_node2.sh /tmp/m26-node1/m26-material`.

Negative tests must reject an unapproved SOC telemetry source, out-of-order incident transitions, non-immutable backup policy, restore digest mismatch, private-key leakage, and tampered signed artifacts.

## M27 relationship

M27 adds the Secure SDLC / DevSecOps / AppSec evidence layer on top of the immutable M0–M26 lineage. This document keeps its original milestone authority; M27 consumes its controls/evidence where relevant and does not retroactively rewrite the historical contract. M27 closes the `CISSP-D6-002` control-plane capability gap with default-deny security testing gates and independently verifiable Node1/Node2 evidence. Simulated local penetration-test evidence validates the workflow only and is not a production penetration-test claim.

## M28 relationship

M28 adds authority-bound evidence controls for organizational governance, personnel security/training, physical/environmental security, and business-continuity exercises. This document keeps its original milestone authority; M28 consumes its applicable evidence without rewriting historical M0–M27 claims. Real-world HR/facility/BCP controls require authorized production records—local Python validation proves the evidence contract, signatures, freshness and source binding only.

## M29 relationship

M29 aggregates the signed M21 platform prerequisite and M22–M28 enterprise-security evidence into one cross-domain Node1/Node2 validation package. This historical document remains authoritative for its original milestone; M29 consumes its evidence without rewriting its semantics. M29 distinguishes evidence-integrity success from production readiness and remains fail-closed while M21 platform controls or real M27/M28 production evidence are outstanding. See `docs/M29-Enterprise-Cross-Domain-Node1-Node2-Validation.md`, `docs/Prerequisites-M29.md`, `docs/Deployment-M29.md`, and `docs/Validation-M29.md`.
