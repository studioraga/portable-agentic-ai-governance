# Deployment — M28

M28 does not automate personnel decisions, building controls or continuity exercises. On Node1 run `./deploy/m28/one_shot_node1.sh` to build the signed evidence package. Transfer only `var/m28-verifier.tar.gz` and its `.sha256` file to Node2. Replace simulated records with authorized production records only through an approved organizational process; do not copy sensitive HR source data into Git.

## M29 relationship

M29 aggregates the signed M21 platform prerequisite and M22–M28 enterprise-security evidence into one cross-domain Node1/Node2 validation package. This historical document remains authoritative for its original milestone; M29 consumes its evidence without rewriting its semantics. M29 distinguishes evidence-integrity success from production readiness and remains fail-closed while M21 platform controls or real M27/M28 production evidence are outstanding. See `docs/M29-Enterprise-Cross-Domain-Node1-Node2-Validation.md`, `docs/Prerequisites-M29.md`, `docs/Deployment-M29.md`, and `docs/Validation-M29.md`.
