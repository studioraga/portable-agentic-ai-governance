# M17 Validation

Run focused tests and local acceptance:

```bash
python3 -m pytest -q tests/cra_annex_evidence
./scripts/m17/validate_m17_local.sh
```

Release gate:

```bash
./scripts/m17/validate_m17_regression.sh
```

Acceptance requires all 22 Annex I rows, 14 Part I + 8 Part II, digest-valid evidence references, explicit gaps, no CRA conformity claim, and M11–M16 baseline bindings.
