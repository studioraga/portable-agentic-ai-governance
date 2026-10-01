# Deployment — M14

Node1:

```bash
./deploy/m14/one_shot_node1.sh "$PWD/var/m14-material"
./scripts/m14/verify_node1.sh "$PWD/var/m14-material"
./deploy/m14/package_verifier_material.sh "$PWD/var/m14-material" "$PWD/var/m14-verifier.tar.gz"
```

Node2:

```bash
./deploy/m14/one_shot_node2.sh /tmp/m14-verifier/m14-material
./scripts/m14/verify_node2.sh "$HOME/.config/portable-ai-governance/m14"
```

M14 does not submit through the CRA SRP. The evidence pack is handed to an authorised Assigned Representative for portal entry/review.

## M15 integration

M15 consumes the existing milestone evidence through the frozen M11–M14 contracts to prepare PSIRT/CVD, component-maintainer coordination, fixed-vulnerability advisory and Article 14(8) user-notification evidence. This document's original milestone authority is unchanged: M15 adds no automatic external dispatch, public disclosure, user notification, maintainer contact, ENISA submission or CRA conformity claim. See `docs/M15-CRA-PSIRT-CVD-User-Notification.md`, `docs/Deployment-M15.md`, and `docs/Validation-M15.md`.
