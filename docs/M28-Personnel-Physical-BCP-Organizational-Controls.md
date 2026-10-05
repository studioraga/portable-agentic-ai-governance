# M28 — Personnel, Physical, BCP & Organizational Controls

M28 extends the enterprise security evidence/control plane into controls that cannot honestly be proven by software alone. It validates **authority, freshness, scope, completeness, segregation of duties, source binding, signatures, and independent verification** of personnel, physical/environmental, governance and business-continuity evidence.

## Security boundary

Python does **not** prove that screening occurred, a badge reader is functioning, CCTV was inspected, fire suppression passed inspection, or a real BCP exercise occurred. Production readiness requires authoritative records from HR/security, facilities/safety, executives/risk owners and continuity owners. Local fixtures are marked `SIMULATED_SCHEMA_VALIDATION_ONLY` and are rejected by production-mode validators.

## Controls

`ENT-GOV-001/002`, `ENT-PEOPLE-001/002/003`, `ENT-PHYS-001/002`, `ENT-ENV-001`, and `ENT-BCP-001/002` establish evidence contracts for governance/RACI/due care, personnel lifecycle and training, physical access/visitor/surveillance/tamper controls, environmental resilience, and organizational BCP exercises.

## CISSP gap closure

M28 records `CISSP-D1-001`, `CISSP-D1-004`, and `CISSP-D7-004` as evidenced at the authority-bound evidence-control-plane level. M26 remains authoritative for technical backup/restore/RPO/RTO evidence under `CISSP-D7-003`; M28 adds organizational continuity ownership and exercise evidence.

## Node roles

Node1 builds and signs the evidence package. Node2 receives public/verifier material only and verifies manifest signatures, artifact hashes, source digests and claim boundaries.

## M29 relationship

M29 aggregates the signed M21 platform prerequisite and M22–M28 enterprise-security evidence into one cross-domain Node1/Node2 validation package. This historical document remains authoritative for its original milestone; M29 consumes its evidence without rewriting its semantics. M29 distinguishes evidence-integrity success from production readiness and remains fail-closed while M21 platform controls or real M27/M28 production evidence are outstanding. See `docs/M29-Enterprise-Cross-Domain-Node1-Node2-Validation.md`, `docs/Prerequisites-M29.md`, `docs/Deployment-M29.md`, and `docs/Validation-M29.md`.
