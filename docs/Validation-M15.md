# M15 Validation

```bash
python3 -m pytest -q tests/cra_psirt
./scripts/m15/validate_m15_local.sh
./scripts/m15/validate_m15_regression.sh
./scripts/m15/verify_node1.sh "$PWD/var/m15-material"
./scripts/m15/verify_node2.sh "$HOME/.config/portable-ai-governance/m15"
```

Acceptance requires signed/digest-bound evidence, PSIRT/CVD/user-notification coverage, unchanged M11–M14 bindings, no external side effects, verifier-only Node2 material, tamper rejection and private-key rejection.
