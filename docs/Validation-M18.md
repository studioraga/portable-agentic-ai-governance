# M18 Validation

Focused validation:

```bash
python3 -m pytest -q tests/cra_technical_file
./scripts/m18/validate_m18_local.sh
```

Release regression:

```bash
./scripts/m18/validate_m18_regression.sh
```

Acceptance requires eight Annex VII sections, all referenced evidence present/digest-bound, explicit EU Declaration GAP, PARTIAL test-report readiness pending M19, signed material verification, Node1/Node2 private-key separation, tamper rejection, and no CRA conformity claim.
