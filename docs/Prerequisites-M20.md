# M20 Prerequisites

- Frozen M19 source baseline.
- Node1 release authority and Node2 independent verifier.
- For final freeze readiness, signed M19 material must report `validation_mode=LIVE`, `production_validation_complete=true`, and zero failed checks.
- Python environment sufficient to run the repository tests and Ed25519 verification.

## Documentation role

This file is a milestone-specific historical/feature record. For the current repository workflow, use [`../README.md`](../README.md), [`../instruction.md`](../instruction.md), [`Architecture.md`](Architecture.md), [`Validation.md`](Validation.md), and [`Milestones.md`](Milestones.md).


### M22 relationship

This document remains authoritative for its historical milestone scope. M22 does not rewrite that milestone; it inventories and maps its reusable controls/evidence into the enterprise-security foundation and records remaining gaps in `governance/enterprise/m22/gap-register.json`. See `docs/M22-CISSP-Enterprise-Security-Control-Foundation.md`.
