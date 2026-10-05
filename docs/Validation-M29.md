# M29 Validation

Run:

```bash
python -m pytest -q tests/enterprise_validation
python -m pytest -q tests/acceptance/test_framework_mapping.py
./scripts/m29/validate_m29_local.sh
./scripts/m29/validate_m29_regression.sh
```

M29 succeeds when evidence integrity and verifier independence pass. `production_ready=false` is the correct current result while production gates remain open.

Negative tests must include tampering with `m29-requirement-matrix.json` or another signed artifact and confirming a non-zero verifier exit.
