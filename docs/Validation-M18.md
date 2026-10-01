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

## M19 integration — CRA Node1/Node2 Production Validation

M19 consumes this milestone's evidence as part of the heterogeneous Node1/Node2 production-validation chain. The M19 signed validation bundle binds the frozen CRA baselines, checks source/version/platform parity and verifier-key isolation, and supplies a production-evidence candidate for Annex I Part II(3) regular product-security testing. M19 does not rewrite this milestone's historical claims, perform conformity assessment, or make a CRA conformity claim.
