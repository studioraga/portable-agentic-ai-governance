# Validation — M14

```bash
python3 -m pytest -q tests/cra_reporting
./scripts/m14/validate_m14_local.sh
./scripts/m14/validate_m14_regression.sh
```

Acceptance requires AEV and severe-incident coverage, all three reporting stages, signature/digest verification, M11/M12/M13 baseline bindings, zero SRP/network side effects, Assigned Representative handoff, Node2 private-key rejection, and tamper rejection.

## M15 integration

M15 consumes the existing milestone evidence through the frozen M11–M14 contracts to prepare PSIRT/CVD, component-maintainer coordination, fixed-vulnerability advisory and Article 14(8) user-notification evidence. This document's original milestone authority is unchanged: M15 adds no automatic external dispatch, public disclosure, user notification, maintainer contact, ENISA submission or CRA conformity claim. See `docs/M15-CRA-PSIRT-CVD-User-Notification.md`, `docs/Deployment-M15.md`, and `docs/Validation-M15.md`.

## M16 integration — CRA Secure Update & Product Lifecycle
M16 consumes the existing milestone evidence without rewriting its historical responsibility. It adds support-period/lifecycle evidence, signed secure-update metadata and payload verification, anti-rollback decisions, update-retention/free-update policy checks, and end-of-support notification preparation. M16 keeps host OS/firmware modification and network rollout out of acceptance; see `docs/M16-CRA-Secure-Update-Product-Lifecycle.md`, `docs/Deployment-M16.md`, and `docs/Validation-M16.md`.

## M17 — CRA Annex-I Compliance Evidence integration

M17 consumes the existing M3–M16 security, vulnerability, incident, reporting, PSIRT/CVD and secure-update evidence and binds it to all Annex I Part I/II requirement rows from the frozen M11 CRA matrix. M17 records `EVIDENCED`, `PARTIAL` and `GAP` states with SHA-256 evidence references; it does not mutate M11 requirement status, perform conformity assessment, generate the Annex VII technical file, or claim CRA conformity. See `docs/M17-CRA-Annex-I-Compliance-Evidence.md` and `docs/Validation-M17.md`.

## M18 integration

M18 assembles the CRA Article 31 / Annex VII technical-documentation evidence file from the evidence produced by M3-M17. This document remains an input/reference to that assembly; M18 does not retroactively change this milestone's scope. The M18 technical file is explicitly a draft evidence package: it makes no CRA conformity claim, does not perform a conformity assessment, does not authorize CE marking, and does not fabricate the EU Declaration of Conformity. Product-specific production/security test evidence that remains incomplete is carried forward to M19 as an explicit readiness gap.
