# Validation — M11 CRA Product Security Foundation

Run on Node1:

```bash
./scripts/m11/validate_m11_local.sh
./deploy/m11/one_shot_node1.sh ./var/m11-material
./deploy/m11/package_verifier_material.sh ./var/m11-material ./var/m11-verifier.tar.gz
(
    cd ./var
    sha256sum -c m11-verifier.tar.gz.sha256
)
```

Negative checks covered by pytest include duplicate/invalid mappings, missing implementation paths, tampered requirement matrices, and the no-conformity-claim invariant.

Node2 acceptance requires verifier-only material and fails if `signing-private.pem` is present:

```bash
mkdir -p /tmp/m11-verifier && tar -xzf m11-verifier.tar.gz -C /tmp/m11-verifier
./deploy/m11/one_shot_node2.sh /tmp/m11-verifier/m11-material
```

## M12 hand-off

M12 consumes the signed/frozen M11 CRA requirement matrix without altering M11's 92-row baseline. M12 validation additionally binds its manifest to the SHA-256 of `governance/cra/cra-requirements.json`, so a changed M11 baseline invalidates M12 verification.

## M13 integration boundary

M13 adds deterministic CRA Article 14(5) severe-incident classification and a signed statutory-clock evidence layer. It consumes M9 security-event facts and M12 AEV candidate evidence while preserving M11 as the authoritative CRA requirement baseline. M13 records an immutable manufacturer-awareness T0, derives the applicable 24-hour and 72-hour deadlines, derives the AEV final-report deadline from corrective/mitigating-measure availability, and derives the severe-incident final-report deadline as one calendar month after the incident notification. M13 does **not** submit to ENISA/SRP, generate the M14 reporting pack, or make a CRA conformity claim. See `docs/M13-CRA-Incident-Classification-Statutory-Clock.md`, `docs/Prerequisites-M13.md`, `docs/Deployment-M13.md`, and `docs/Validation-M13.md`.

## M14 integration — CRA reporting / ENISA SRP evidence pack

M14 consumes the frozen M11 requirement baseline, M12 vulnerability/exploitation intelligence and M13 incident/statutory-clock evidence to build signed Early Warning, 72-hour Notification and Final Report evidence packs. M14 is an internal preparation and verification layer only: it performs no CRA SRP/network submission, makes no conformity claim, preserves Node1 signing authority / Node2 verifier-only separation, and requires an authorised Assigned Representative to complete the current SRP web-interface workflow. See `docs/M14-CRA-Reporting-ENISA-SRP-Evidence-Pack.md`, `docs/Prerequisites-M14.md`, `docs/Deployment-M14.md`, and `docs/Validation-M14.md`.

## M15 integration

M15 consumes the existing milestone evidence through the frozen M11–M14 contracts to prepare PSIRT/CVD, component-maintainer coordination, fixed-vulnerability advisory and Article 14(8) user-notification evidence. This document's original milestone authority is unchanged: M15 adds no automatic external dispatch, public disclosure, user notification, maintainer contact, ENISA submission or CRA conformity claim. See `docs/M15-CRA-PSIRT-CVD-User-Notification.md`, `docs/Deployment-M15.md`, and `docs/Validation-M15.md`.
