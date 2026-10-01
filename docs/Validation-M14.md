# Validation — M14

```bash
python3 -m pytest -q tests/cra_reporting
./scripts/m14/validate_m14_local.sh
./scripts/m14/validate_m14_regression.sh
```

Acceptance requires AEV and severe-incident coverage, all three reporting stages, signature/digest verification, M11/M12/M13 baseline bindings, zero SRP/network side effects, Assigned Representative handoff, Node2 private-key rejection, and tamper rejection.

## M15 integration

M15 consumes the existing milestone evidence through the frozen M11–M14 contracts to prepare PSIRT/CVD, component-maintainer coordination, fixed-vulnerability advisory and Article 14(8) user-notification evidence. This document's original milestone authority is unchanged: M15 adds no automatic external dispatch, public disclosure, user notification, maintainer contact, ENISA submission or CRA conformity claim. See `docs/M15-CRA-PSIRT-CVD-User-Notification.md`, `docs/Deployment-M15.md`, and `docs/Validation-M15.md`.
