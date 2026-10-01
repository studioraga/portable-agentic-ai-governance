# Deployment — M12

## Node1

```bash
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
./scripts/m12/validate_m12_local.sh
./deploy/m12/one_shot_node1.sh "$PWD/var/m12-material"
./deploy/m12/package_verifier_material.sh "$PWD/var/m12-material" "$PWD/var/m12-verifier.tar.gz"
( cd var && sha256sum -c m12-verifier.tar.gz.sha256 )
```

Transfer only `m12-verifier.tar.gz` and its checksum to Node2.

## Node2

```bash
sha256sum -c m12-verifier.tar.gz.sha256
rm -rf /tmp/m12-verifier && mkdir -m700 /tmp/m12-verifier
tar -xzf m12-verifier.tar.gz -C /tmp/m12-verifier
./deploy/m12/one_shot_node2.sh /tmp/m12-verifier/m12-material
```

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.

## M14 integration — CRA reporting / ENISA SRP evidence pack

M14 consumes the frozen M11 requirement baseline, M12 vulnerability/exploitation intelligence and M13 incident/statutory-clock evidence to build signed Early Warning, 72-hour Notification and Final Report evidence packs. M14 is an internal preparation and verification layer only: it performs no CRA SRP/network submission, makes no conformity claim, preserves Node1 signing authority / Node2 verifier-only separation, and requires an authorised Assigned Representative to complete the current SRP web-interface workflow. See `docs/M14-CRA-Reporting-ENISA-SRP-Evidence-Pack.md`, `docs/Prerequisites-M14.md`, `docs/Deployment-M14.md`, and `docs/Validation-M14.md`.

## M15 integration

M15 consumes the existing milestone evidence through the frozen M11–M14 contracts to prepare PSIRT/CVD, component-maintainer coordination, fixed-vulnerability advisory and Article 14(8) user-notification evidence. This document's original milestone authority is unchanged: M15 adds no automatic external dispatch, public disclosure, user notification, maintainer contact, ENISA submission or CRA conformity claim. See `docs/M15-CRA-PSIRT-CVD-User-Notification.md`, `docs/Deployment-M15.md`, and `docs/Validation-M15.md`.
