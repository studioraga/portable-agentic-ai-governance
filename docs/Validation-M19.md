# Validation — M19

Local deterministic acceptance:

```bash
./scripts/m19/validate_m19_local.sh
```

Full release gate:

```bash
./scripts/m19/validate_m19_regression.sh
```

Fixture acceptance is always `SIMULATED`. Production acceptance additionally requires LIVE profiles from both nodes, all ten required validation cases passing, and `production_validation_complete=true`. Negative tests must prove signed-material tamper rejection and private-key rejection on Node2.
