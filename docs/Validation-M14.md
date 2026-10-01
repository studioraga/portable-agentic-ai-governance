# Validation — M14

```bash
python3 -m pytest -q tests/cra_reporting
./scripts/m14/validate_m14_local.sh
./scripts/m14/validate_m14_regression.sh
```

Acceptance requires AEV and severe-incident coverage, all three reporting stages, signature/digest verification, M11/M12/M13 baseline bindings, zero SRP/network side effects, Assigned Representative handoff, Node2 private-key rejection, and tamper rejection.
