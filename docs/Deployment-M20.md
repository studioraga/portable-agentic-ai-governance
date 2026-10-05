# M20 Deployment

Node1 runs `deploy/m20/one_shot_node1.sh <M19-summary> [output]`, signs the final-freeze evidence, and packages verifier-only material. Node2 receives only the verifier archive and runs `deploy/m20/one_shot_node2.sh`. The scripts deploy configuration/evidence only; they do not flash firmware, update the host OS, or contact external services.

## Documentation role

This file is a milestone-specific historical/feature record. For the current repository workflow, use [`../README.md`](../README.md), [`../instruction.md`](../instruction.md), [`Architecture.md`](Architecture.md), [`Validation.md`](Validation.md), and [`Milestones.md`](Milestones.md).


### M22 relationship

This document remains authoritative for its historical milestone scope. M22 does not rewrite that milestone; it inventories and maps its reusable controls/evidence into the enterprise-security foundation and records remaining gaps in `governance/enterprise/m22/gap-register.json`. See `docs/M22-CISSP-Enterprise-Security-Control-Foundation.md`.
