# Validation — M28

Run `python3 -m pytest -q tests/organizational_security`, then `./scripts/m28/validate_m28_local.sh`. Node1 generates persistent evidence with `./deploy/m28/one_shot_node1.sh` and verifies it using `./scripts/m28/verify_node1.sh var/m28-material`. Node2 extracts the verifier tar and runs `./scripts/m28/verify_node2.sh <material-dir>`. Tampering with any manifest-bound artifact must produce a non-zero verifier exit. Production validation must reject simulated evidence and require authorized real-world records.

## M29 relationship

M29 aggregates the signed M21 platform prerequisite and M22–M28 enterprise-security evidence into one cross-domain Node1/Node2 validation package. This historical document remains authoritative for its original milestone; M29 consumes its evidence without rewriting its semantics. M29 distinguishes evidence-integrity success from production readiness and remains fail-closed while M21 platform controls or real M27/M28 production evidence are outstanding. See `docs/M29-Enterprise-Cross-Domain-Node1-Node2-Validation.md`, `docs/Prerequisites-M29.md`, `docs/Deployment-M29.md`, and `docs/Validation-M29.md`.
