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
