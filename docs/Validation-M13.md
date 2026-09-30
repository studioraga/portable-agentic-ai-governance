# M13 Validation

```bash
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
./scripts/m13/validate_m13_local.sh
./scripts/m13/validate_m13_regression.sh
```

Required positive coverage includes Article 14(5)(a), Article 14(5)(b), NOT_SEVERE, INCOMPLETE, AEV and severe-incident clock families, awareness-journal integrity and M11/M12 digest bindings. Required negative validation includes tampered material rejection, private-key rejection on Node2, awareness-journal chain rejection and private-key-free verifier packaging.
