# M15 Validation

```bash
python3 -m pytest -q tests/cra_psirt
./scripts/m15/validate_m15_local.sh
./scripts/m15/validate_m15_regression.sh
./scripts/m15/verify_node1.sh "$PWD/var/m15-material"
./scripts/m15/verify_node2.sh "$HOME/.config/portable-ai-governance/m15"
```

Acceptance requires signed/digest-bound evidence, PSIRT/CVD/user-notification coverage, unchanged M11–M14 bindings, no external side effects, verifier-only Node2 material, tamper rejection and private-key rejection.

## M16 integration — CRA Secure Update & Product Lifecycle
M16 consumes the existing milestone evidence without rewriting its historical responsibility. It adds support-period/lifecycle evidence, signed secure-update metadata and payload verification, anti-rollback decisions, update-retention/free-update policy checks, and end-of-support notification preparation. M16 keeps host OS/firmware modification and network rollout out of acceptance; see `docs/M16-CRA-Secure-Update-Product-Lifecycle.md`, `docs/Deployment-M16.md`, and `docs/Validation-M16.md`.
