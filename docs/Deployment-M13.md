# M13 Deployment

Node1:

```bash
./deploy/m13/one_shot_node1.sh "$PWD/var/m13-material"
./scripts/m13/verify_node1.sh "$PWD/var/m13-material"
./deploy/m13/package_verifier_material.sh "$PWD/var/m13-material" "$PWD/var/m13-verifier.tar.gz"
```

Node2:

```bash
./deploy/m13/one_shot_node2.sh /tmp/m13-verifier/m13-material
./scripts/m13/verify_node2.sh "$HOME/.config/portable-ai-governance/m13"
```

## M14 integration — CRA reporting / ENISA SRP evidence pack

M14 consumes the frozen M11 requirement baseline, M12 vulnerability/exploitation intelligence and M13 incident/statutory-clock evidence to build signed Early Warning, 72-hour Notification and Final Report evidence packs. M14 is an internal preparation and verification layer only: it performs no CRA SRP/network submission, makes no conformity claim, preserves Node1 signing authority / Node2 verifier-only separation, and requires an authorised Assigned Representative to complete the current SRP web-interface workflow. See `docs/M14-CRA-Reporting-ENISA-SRP-Evidence-Pack.md`, `docs/Prerequisites-M14.md`, `docs/Deployment-M14.md`, and `docs/Validation-M14.md`.

## M15 integration

M15 consumes the existing milestone evidence through the frozen M11–M14 contracts to prepare PSIRT/CVD, component-maintainer coordination, fixed-vulnerability advisory and Article 14(8) user-notification evidence. This document's original milestone authority is unchanged: M15 adds no automatic external dispatch, public disclosure, user notification, maintainer contact, ENISA submission or CRA conformity claim. See `docs/M15-CRA-PSIRT-CVD-User-Notification.md`, `docs/Deployment-M15.md`, and `docs/Validation-M15.md`.
